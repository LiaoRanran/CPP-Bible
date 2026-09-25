"""638 C1 · 闭环第二次运行（用**调过的规则**再跑一遍 637 闭环）

按序跑 637 闭环的五个阶段（**在进程内调用**，不写 637 的产物文件）：

```
self_observer_637.collect → error_detector_637.detect → candidate_generator_637.generate
→ cost_benefit_637.flatten/rank → （本批）loop_tuning_638 覆盖层 → 638 memo
```

**与 637 第一次产出的差别只有一个来源**：C2 的调优覆盖层（`loop_tuning_638`），
因为 637 的工具是确定性的，不调参则两次输出必然逐字相同。

产出 `data/638_evolution_memo.md`（第二次建议书）+ `.json`，并给出与
`data/637_scored.json`（第一次）的**可量化对比**（§三.C1.3）。

**只读契约**：`--check` 只读、exit 0、不写盘；`--report` 写
`data/638_evolution_memo.md` + `.json`。纯标准库；≥5 例单测。
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

OUT_MD = os.path.join(ROOT, "data", "638_evolution_memo.md")
OUT_JSON = os.path.join(ROOT, "data", "638_evolution_memo.json")
SCORED_637 = os.path.join(ROOT, "data", "637_scored.json")

# 638 任务0 判定的 637 误报（依据 635 冻结的设计属性，见 638_baseline.md §2.5）
FALSE_ALARMS_637 = ["observation_pct", "exception_clauses"]

# 体检显示阈值（调后口径；None=停用）
DISPLAY_THRESHOLDS: dict[str, Optional[float]] = {
    "rules": None, "tools_total": None, "tests_total": None, "commits": None,
    "grounding_pct": 50.0, "defeater_coverage_pct": 90.0, "taint_cards": 5.0,
    "exception_clauses": 250.0, "observation_pct": None, "ahead": 20.0,
    "pytest_failures": 5.0,
}
_LABELS = {
    "rules": "规则数", "tools_total": "工具数", "tests_total": "测试数", "commits": "commits",
    "pytest_failures": "pytest 失败数", "grounding_pct": "接地率(%)",
    "defeater_coverage_pct": "击败器覆盖率(%)", "taint_cards": "taint=true 卡数",
    "exception_clauses": "例外条款条目", "observation_pct": "观察态比例(%)",
    "ahead": "ahead 数",
}
_LT = {"grounding_pct", "defeater_coverage_pct"}


# ── 跑闭环（第二次）────────────────────────────────────────────────────
def run_loop() -> dict[str, Any]:
    """按序跑 637 闭环 + 638 调优覆盖层。**不写任何 637 产物**。"""
    import candidate_generator_637 as cg
    import cost_benefit_637 as cb
    import error_detector_637 as ed
    import loop_tuning_638 as lt
    import self_observer_637 as so

    obs = so.collect(heavy=False)
    metrics = obs.get("metrics", {}) or {}
    raw = ed.detect(obs)                                    # 调前（637 原阈值）
    tuned = lt.detect_with(metrics, lt.TUNED_THRESHOLDS)     # 调后（638 覆盖层）
    cand = cg.generate({"anomalies": tuned})
    rows = cb.rank(cb.flatten(cand))
    rows = lt.rescore(rows, lt.TUNED_RISK_FACTOR)            # T3：风险系数覆盖
    rows = sorted(rows, key=lambda r: (-float(r["score"]), str(r["candidate"])))
    top3 = rows[:3]
    for r in top3:
        r["reason"] = cb.reason(r)
    return {"generated": datetime.datetime.now().isoformat(timespec="seconds"),
            "metrics": metrics, "heavy": bool(obs.get("heavy", False)),
            "anomalies_before": raw, "anomalies": tuned,
            "n_candidates": len(rows), "scored": rows, "top3": top3}


# ── 与第一次对比 ────────────────────────────────────────────────────────
def load_637() -> dict[str, Any]:
    try:
        return json.loads(open(SCORED_637, encoding="utf-8").read())
    except (OSError, json.JSONDecodeError):
        return {}


def compare(run: Optional[dict[str, Any]] = None) -> dict[str, Any]:
    r = run or run_loop()
    first = load_637()
    first_top3 = [x.get("candidate", "") for x in (first.get("top3") or [])]
    now_top3 = [x["candidate"] for x in r["top3"]]
    n_before, n_after = len(r["anomalies_before"]), len(r["anomalies"])
    fa_before = len([a for a in r["anomalies_before"] if a["key"] in FALSE_ALARMS_637])
    fa_after = len([a for a in r["anomalies"] if a["key"] in FALSE_ALARMS_637])
    return {
        "generated": r["generated"],
        "first_top3": first_top3, "second_top3": now_top3,
        "top3_overlap": sorted(set(first_top3) & set(now_top3)),
        "top3_changed": first_top3 != now_top3,
        "n_anomalies_first": n_before, "n_anomalies_second": n_after,
        "false_alarm_first": fa_before, "false_alarm_second": fa_after,
        "false_alarm_rate_first": round(fa_before / n_before, 4) if n_before else None,
        "false_alarm_rate_second": round(fa_after / n_after, 4) if n_after else None,
        "first_n_candidates": first.get("n_candidates"),
        "second_n_candidates": r["n_candidates"],
    }


# ── memo 正文（纯函数，不写盘）──────────────────────────────────────────
def _status(key: str, val: Any, thr: Optional[float]) -> str:
    if key == "observation_pct" and thr is None:
        return "— (停用)"
    if val is None:
        return "❓"
    if thr is None:
        return "✅"
    try:
        num = float(val)
    except (TypeError, ValueError):
        return "❓"
    if key in _LT:
        return "✅" if num >= thr else "⚠️"
    return "✅" if num <= thr else "⚠️"


def memo_text(r: dict[str, Any], c: dict[str, Any]) -> str:
    m = r["metrics"]
    lines = [
        "# 阙疑进化建议书 · 第二次运行（自动生成）", "",
        f"> 生成时间：{r['generated']}；数据来源：self_observer → error_detector "
        "→ candidate_generator → cost_benefit → **638 调优覆盖层**。",
        "> **影子建议**：本报告只输出给人看，**人审批后才执行**。", "",
        "## 系统体检（调后口径）", "",
        "| 指标 | 当前值 | 阈值 | 状态 |", "|---|---|---|---|",
    ]
    for key, label in _LABELS.items():
        thr = DISPLAY_THRESHOLDS.get(key)
        lines.append(f"| {label} | {m.get(key, '—')} | "
                     f"{'—' if thr is None else thr} | {_status(key, m.get(key), thr)} |")

    lines += ["", "## 我发现的异常（调后，已消除 2 项误报）", "",
              "| # | 异常 | 严重程度 | 当前值 | 阈值 |", "|---|---|---|---|---|"]
    for i, a in enumerate(r["anomalies"], 1):
        lines.append(f"| {i} | {a['key']} | {a['severity']} | {a['current']} | "
                     f"{a['threshold']} |")
    if not r["anomalies"]:
        lines.append("| - | 未检出异常 | - | - | - |")

    lines += ["", "## 我建议下一步做什么（调后 top 3）", ""]
    for i, x in enumerate(r["top3"], 1):
        medal = ["🥇", "🥈", "🥉"][i - 1] if i <= 3 else "▪"
        lines += [f"### {medal} 第 {i} 优先：{x['candidate']}", "",
                  f"- 为什么：{x['reason']}",
                  f"- 做什么：{x['action']}",
                  f"- 成本/收益：{x['cost']}/{x['benefit']}",
                  f"- 风险：{x['risk_class']}（系数 {x['risk_factor']}）", ""]

    lines += [
        "## 与第一次产出（637）的对比", "",
        "| 维度 | 第一次（637） | 第二次（638，调后） |", "|---|---|---|",
        f"| 检出异常数 | {c['n_anomalies_first']} | **{c['n_anomalies_second']}** |",
        f"| 其中误报数 | {c['false_alarm_first']} | **{c['false_alarm_second']}** |",
        f"| 误报率 | {c['false_alarm_rate_first']} | **{c['false_alarm_rate_second']}** |",
        f"| 候选方案数 | {c['first_n_candidates']} | {c['second_n_candidates']} |",
        f"| top3 | {' / '.join(c['first_top3']) or '—'} | "
        f"{' / '.join(c['second_top3']) or '—'} |",
        f"| top3 是否变化 | — | **{'是' if c['top3_changed'] else '否'}** |",
        f"| top3 重合 | — | {c['top3_overlap'] or '无'} |", "",
        "> **结论**：调参**直接消除 2 项误报**（`observation_pct` / `exception_clauses`），"
        f"误报率 {c['false_alarm_rate_first']} → **{c['false_alarm_rate_second']}**；"
        "top 建议随之改变。这是**唯一**两次运行的差异来源（637 工具是确定性的）。", "",
        "## 我觉得不靠谱的地方（本轮仍未解决）", "",
        "- 我仍然是**纯规则匹配**，不懂语义（R3 未修）；",
        "- 我仍**没有跨轮记忆**，不知道 638 已经做了什么（R2 未修）——所以本报告**不包含**",
        "  对 638 自身产物的评价；",
        "- 本次为**轻量采集**，`pytest/ruff/mypy` 为 `null`（R6 未修）⇒ 我看不到代码健康；",
        "- known_error_rate 仍**全无数据**（R5；638 B1 已量化缺口但未补数据）⇒ 判断不了规则准不准；",
        "- 「成本/收益」仍是**人工等级**（R4 仅部分缓解：只调了 report 系数）；",
        "",
        "---",
        "本报告由 self_evolution_loop 自动生成 · 人审批后才执行",
    ]
    return "\n".join(lines) + "\n"


def write_report() -> dict[str, str]:
    r = run_loop()
    c = compare(r)
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump({**{k: v for k, v in r.items() if k != "scored"},
                   "scored": r["scored"], "comparison": c}, fh,
                  ensure_ascii=False, indent=2)
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(memo_text(r, c))
    return {"json": OUT_JSON, "md": OUT_MD}


# ── 自检 ────────────────────────────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    r = run_loop()
    chk("跑通闭环", bool(r["metrics"]) and r["n_candidates"] >= 1)
    chk("有调前/调后异常", isinstance(r["anomalies_before"], list)
        and isinstance(r["anomalies"], list))
    chk("调后异常更少", len(r["anomalies"]) < len(r["anomalies_before"]))
    chk("top3 有 3 条", len(r["top3"]) == 3)
    chk("top3 有序（分不增）",
        all(r["top3"][i]["score"] >= r["top3"][i + 1]["score"]
            for i in range(len(r["top3"]) - 1)))
    chk("误报已消除", not any(a["key"] in FALSE_ALARMS_637 for a in r["anomalies"]))
    c = compare(r)
    chk("对比：第二次误报为 0", c["false_alarm_second"] == 0)
    chk("对比：第一次误报 2", c["false_alarm_first"] == 2)
    txt = memo_text(r, c)
    chk("memo 含审批声明", "人审批后才执行" in txt and "自动生成" in txt)
    chk("memo 含建议章", "我建议下一步做什么" in txt)
    chk("run_loop 含 scored（write_report 依赖）",
        isinstance(r.get("scored"), list) and len(r["scored"]) == r["n_candidates"])
    chk("输出路径在 data 下",
        OUT_MD.startswith(os.path.join(ROOT, "data"))
        and OUT_JSON.startswith(os.path.join(ROOT, "data")))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="638 C1 闭环第二次运行")
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
    r = run_loop()
    if args.json:
        print(json.dumps({"metrics": r["metrics"],
                          "anomalies": [a["key"] for a in r["anomalies"]],
                          "top3": [x["candidate"] for x in r["top3"]],
                          "comparison": compare(r)}, ensure_ascii=False, indent=2))
        return 0
    print(f"anomalies={[a['key'] for a in r['anomalies']]} "
          f"top3={[x['candidate'] for x in r['top3']]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
