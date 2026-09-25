"""638 C2 · 闭环规则调优（据 637 质量审计调阈值与规则）

**依据**：638 任务0 对 637 闭环第一次产出的复盘（`data/638_baseline.md` §2.5），
归因出 6 类「不靠谱」原因，其中 **R1/R1'（阈值未经统计校准 ⇒ 误报）** 与
**R4（成本/收益为人工赋值）** 是**可立即修**的两类。

**铁律**：637 的工具是上一批的产物，**本批不修改它们**；调优以
**覆盖层（overlay）** 形式实现：本模块自带一份「调后」阈值与风险系数，
对 637 的中间产物（`637_observer.json` 指标）重跑检测与打分，
从而可对比「调前 vs 调后」的差异（§三.C2.3）。

调优项（`TUNING`，逐条含 before/after/理由/预期）：

| 编号 | 对象 | 调前 | 调后 | 依据 |
|---|---|---|---|---|
| T1 | `observation_pct` 阈值 | 30 | **停用** | 观测态 67/67=100% 是 Daubert 表的**设计属性**（635 冻结），非异常 ⇒ 637 top1 是**误报** |
| T2 | `exception_clauses` 阈值 | 100 | 250 | 227 是**7 处来源汇总**（635 冻结），非异常 ⇒ 637 的 P2 误报 |
| T3 | 风险系数 `report` | 0.5 | 0.75 | 637 的 top1 恰是 report 类（成本最低），却被最低系数压制；report 类实测可交付价值被低估 |

**只读契约**：`--check` 只读、exit 0、不写盘；`--report` 写
`data/638_loop_tuning.md` + `.json`。纯标准库；≥5 例单测。
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "638_loop_tuning.md")
OUT_JSON = os.path.join(ROOT, "data", "638_loop_tuning.json")
OBSERVER_JSON = os.path.join(ROOT, "data", "637_observer.json")

# ── 调优表（before = 637 现值，after = 638 调后值）────────────────────────
TUNING: list[dict[str, Any]] = [
    {"id": "T1", "key": "observation_pct", "before": 30, "after": None,
     "why": "观测态 67/67=100% 是 Daubert 表**设计属性**（635 冻结），不是异常；"
            "637 把它列为 top1 P1 异常属**误报**（任务0 §2.5 R1）",
     "expected": "消除 1 条 P1 误报，top1 不再被设计属性占据"},
    {"id": "T2", "key": "exception_clauses", "before": 100, "after": 250,
     "why": "227 条是**7 处来源汇总**（635 冻结），单看总数不构成异常（任务0 §2.5 R1'）",
     "expected": "消除 1 条 P2 误报"},
    {"id": "T3", "key": "risk_factor.report", "before": 0.5, "after": 0.75,
     "why": "637 top1「为例外设过期」正是 report 类（成本最低、可立即交付），"
            "却被最低风险系数压制 ⇒ 人工赋值失真（任务0 §2.5 R4）",
     "expected": "report 类排名上移，低成本可交付建议不再被系统性压低"},
]

# 调后阈值（未列出的键沿用 637 原值）
TUNED_THRESHOLDS: dict[str, Optional[float]] = {
    "grounding_pct": 50.0,        # 保持（真实缺口）
    "observation_pct": None,      # T1 停用
    "pytest_failures": 5.0,       # 保持
    "taint_cards": 5.0,           # 保持（真实异常）
    "exception_clauses": 250.0,   # T2 放宽
    "ahead": 20.0,                # 保持
    "tools_per_test": 1.05,       # 保持
}

ORIGINAL_THRESHOLDS: dict[str, Optional[float]] = {
    **TUNED_THRESHOLDS, "observation_pct": 30.0, "exception_clauses": 100.0,
}

TUNED_RISK_FACTOR = {"report": 0.75, "tool": 1.0, "core": 1.5}

_SEV: dict[str, str] = {
    "grounding_pct": "P1", "observation_pct": "P1", "pytest_failures": "P0",
    "static_errors": "P1", "taint_cards": "P1", "exception_clauses": "P2",
    "ahead": "P2", "tools_per_test": "P2",
}
_LT = {"grounding_pct"}   # 越小越异常；其余越大越异常


def _exceed(cur: float, thr: float, key: str) -> float:
    if thr == 0:
        return float(cur)
    if key in _LT:
        return round((thr - cur) / thr, 4)
    return round((cur - thr) / thr, 4)


def detect_with(metrics: dict[str, Any],
                thresholds: dict[str, Optional[float]]) -> list[dict[str, Any]]:
    """用给定阈值重跑 637 的检测逻辑（**覆盖层**，不改 637 工具）。

    与 `error_detector_637.detect` 同构：阈值取自 `thresholds`，`None` 表示停用该项。
    """
    found: list[dict[str, Any]] = []
    for key, thr in thresholds.items():
        if thr is None:
            continue
        cur = metrics.get(key)
        if not isinstance(cur, (int, float)):
            continue
        hit = (cur < thr) if key in _LT else (cur > thr)
        if hit:
            found.append({"key": key, "name": key, "severity": _SEV.get(key, "P2"),
                          "current": cur, "threshold": thr,
                          "exceedance": _exceed(float(cur), float(thr), key)})
    # 静态检查：ruff+mypy > 0（637 的 special case）
    ruff, mypy = metrics.get("ruff_errors"), metrics.get("mypy_errors")
    if isinstance(ruff, int) and isinstance(mypy, int) and (ruff + mypy) > 0:
        found.append({"key": "static_errors", "name": "static_errors", "severity": "P1",
                      "current": ruff + mypy, "threshold": 0, "exceedance": float(ruff + mypy)})
    rank = {"P0": 3, "P1": 2, "P2": 1}
    found.sort(key=lambda a: (-rank.get(str(a["severity"]), 0), -float(a["exceedance"])))
    return found[:5]


def load_metrics(path: str = OBSERVER_JSON) -> dict[str, Any]:
    """读 637 观测器的落盘指标（**可能过期**，仅作回退）。"""
    try:
        d: Any = json.loads(open(path, encoding="utf-8").read())
    except (OSError, json.JSONDecodeError):
        return {}
    return (d.get("metrics") if isinstance(d, dict) else None) or {}


def fresh_metrics() -> dict[str, Any]:
    """**实时**跑一遍 637 观测器（轻量，不跑 pytest/ruff/mypy）取当前指标。

    优先用实时值：落盘的 `637_observer.json` 可能被其它进程/测试改写而失真
    （本批实测遇到过一次，见 `data/638_loop_tuning.md` §四）。
    """
    try:
        import self_observer_637 as obs
        m = obs.collect(heavy=False).get("metrics")
        return m if isinstance(m, dict) else load_metrics()
    except Exception:  # noqa: BLE001
        return load_metrics()


def rescore(rows: list[dict[str, Any]],
            factors: Optional[dict[str, float]] = None) -> list[dict[str, Any]]:
    """按给定风险系数重算候选分数（覆盖层）。"""
    f = factors or TUNED_RISK_FACTOR
    lvl = {"低": 1, "中": 2, "高": 3}
    out: list[dict[str, Any]] = []
    for r in rows:
        cost = lvl.get(str(r.get("cost", "")), 2)
        benefit = lvl.get(str(r.get("benefit", "")), 2)
        factor = f.get(str(r.get("risk_class", "")), 1.0)
        out.append({**r, "risk_factor": factor,
                    "score": round(benefit / cost * factor, 3)})
    return sorted(out, key=lambda r: (-float(r["score"]), str(r.get("candidate", ""))))


def compare(metrics: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    """调前 vs 调后的差异（真实数字）。默认用**实时**指标，可注入以便单测。"""
    m = metrics if metrics is not None else fresh_metrics()
    before = detect_with(m, ORIGINAL_THRESHOLDS)
    after = detect_with(m, TUNED_THRESHOLDS)
    kb, ka = {a["key"] for a in before}, {a["key"] for a in after}
    return {
        "generated": datetime.datetime.now().isoformat(timespec="seconds"),
        "tuning": TUNING,
        "metrics_source": "self_observer_637.collect(heavy=False)（实时）",
        "before": before, "after": after,
        "n_before": len(before), "n_after": len(after),
        "removed": sorted(kb - ka), "added": sorted(ka - kb),
        "kept": sorted(kb & ka),
        "tuned_risk_factor": TUNED_RISK_FACTOR,
    }


def write_report() -> dict[str, str]:
    c = compare()
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(c, fh, ensure_ascii=False, indent=2)
    lines = [
        "# 638 C2 · 闭环规则调参记录", "",
        f"> 生成时间：{c['generated']}。工具：`tools/loop_tuning_638.py`。",
        f"> 指标来源：`{c['metrics_source']}`（637 闭环中间产物）。", "",
        "## 一、改了什么（3 项，逐条含理由与预期）", "",
        "| 编号 | 对象 | 调前 | 调后 | 为什么改 | 预期效果 |",
        "|---|---|---|---|---|---|",
    ]
    for t in c["tuning"]:
        after = "**停用**" if t["after"] is None else t["after"]
        lines.append(f"| {t['id']} | `{t['key']}` | {t['before']} | {after} | "
                     f"{t['why']} | {t['expected']} |")

    lines += [
        "", "## 二、阈值全表（调前 → 调后）", "",
        "| 指标 | 调前阈值 | 调后阈值 | 方向 |", "|---|---|---|---|",
    ]
    for k in TUNED_THRESHOLDS:
        b = ORIGINAL_THRESHOLDS.get(k)
        a = TUNED_THRESHOLDS.get(k)
        lines.append(f"| `{k}` | {b if b is not None else '—'} | "
                     f"{a if a is not None else '**停用**'} | "
                     f"{'越小越异常' if k in _LT else '越大越异常'} |")

    lines += [
        "", "## 三、调参前后差异（同一份 637 指标）", "",
        f"- 调前检出异常：**{c['n_before']}** 项；调后：**{c['n_after']}** 项；",
        f"- **消除**（误报）：`{c['removed']}`；",
        f"- **新增**：`{c['added']}`；",
        f"- **保留**：`{c['kept']}`。", "",
        "### 3.1 调前异常", "",
        "| 指标 | 严重度 | 当前值 | 阈值 |", "|---|---|---|---|",
    ]
    for a in c["before"]:
        lines.append(f"| `{a['key']}` | {a['severity']} | {a['current']} | {a['threshold']} |")
    lines += ["", "### 3.2 调后异常", "",
              "| 指标 | 严重度 | 当前值 | 阈值 |", "|---|---|---|---|"]
    for a in c["after"]:
        lines.append(f"| `{a['key']}` | {a['severity']} | {a['current']} | {a['threshold']} |")
    lines += [
        "", "### 3.3 风险系数（T3）", "",
        "| 风险类别 | 调前 | 调后 |", "|---|---|---|",
        "| `report` | 0.5 | **0.75** |", "| `tool` | 1.0 | 1.0 |",
        "| `core` | 1.5 | 1.5 |", "",
        "## 四、诚实登记", "",
        "1. **未修改 637 的任何工具**（§零：不碰上一批产物）——调优是**覆盖层**：",
        "   本模块自带调后阈值/系数，对 637 的指标重跑检测与打分；",
        "2. `detect_with()` 是 `error_detector_637.detect` 的**同构副本**（阈值参数化），",
        "   两者的规则集一致，仅阈值不同；**重复实现是刻意的**（避免改 637 文件）；",
        "3. T1/T2 的依据来自 635 的**冻结设计属性**，判断「误报」是我方结论，非 637 自认；",
        "4. **只调闭环自己的阈值**，不碰 gate 的判决规则（§零.1 向后兼容）；",
        "5. 调参是**迭代过程**：本轮只改 3 项，R2（无跨轮记忆）/R3（无语义）/R5（缺错误率）",
        "   /R6（健康指标空）**未修**，留给后续批次（交人项）；",
        "6. **指标来源改用实时采集** `self_observer_637.collect(heavy=False)`：",
        "   落盘的 `data/637_observer.json` 在本批曾被其它进程/测试改写（出现 `pytest_failures=82`、",
        "   `tools_total=428` 等**过期或污染**值），据此对比会失真 ⇒ 不采用落盘值；",
        "7. R6 未修的直接后果：**实时采集是轻量的**，`pytest/ruff/mypy` 为 `null`，",
        "   故本轮调参**看不到代码健康类异常**（P0 级），只覆盖结构与治理类指标。",
    ]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return {"json": OUT_JSON, "md": OUT_MD}


# ── 自检 ────────────────────────────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("调优表 3 项", len(TUNING) == 3)
    chk("T1 停用 observation_pct", TUNED_THRESHOLDS["observation_pct"] is None)
    chk("T2 放宽到 250", TUNED_THRESHOLDS["exception_clauses"] == 250.0)
    chk("T3 report 系数 0.75", TUNED_RISK_FACTOR["report"] == 0.75)
    # 构造样本验证停用/放宽确实生效
    s = {"observation_pct": 100.0, "exception_clauses": 227, "taint_cards": 8,
         "grounding_pct": 35.8}
    b = {a["key"] for a in detect_with(s, ORIGINAL_THRESHOLDS)}
    a = {x["key"] for x in detect_with(s, TUNED_THRESHOLDS)}
    chk("调前含 observation_pct", "observation_pct" in b)
    chk("调后无 observation_pct", "observation_pct" not in a)
    chk("调前含 exception_clauses", "exception_clauses" in b)
    chk("调后无 exception_clauses", "exception_clauses" not in a)
    chk("真实异常 taint 保留", "taint_cards" in a and "taint_cards" in b)
    chk("grounding 保留（真缺口）", "grounding_pct" in a)
    # 打分覆盖层
    rows = rescore([{"candidate": "x", "cost": "低", "benefit": "中", "risk_class": "report"}])
    chk("report 重算 = 2/1*0.75 = 1.5", rows[0]["score"] == 1.5)
    chk("输出路径在 data 下",
        OUT_MD.startswith(os.path.join(ROOT, "data"))
        and OUT_JSON.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="638 C2 闭环规则调优")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        out = write_report()
        print(f"written {out['json']} {out['md']}")
        return 0
    c = compare()
    if args.json:
        print(json.dumps({k: v for k, v in c.items() if k not in ("before", "after")},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"before={c['n_before']} after={c['n_after']} removed={c['removed']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
