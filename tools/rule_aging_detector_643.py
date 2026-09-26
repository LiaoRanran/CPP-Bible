"""643 E2 · **规则老化检测器**（抗 Goodhart #2）。

**定位**：检测规则**老化/过严/被绕过**，输出 `保留/收紧/拆分/退役` 建议，
并按 A3-G3 **带 n 与「不判」档**（样本不足 ⇒ 不出建议）。

**"时间轴"的口径（必须先读）**：本仓**没有**带日期的逐规则命中明细 ⇒
inbox 要的"最近 30 天趋势"**无法直接算**。本工具改用**可复算的替代轴**：

| 轴 | 来源 | 可算什么 | 不能算什么 |
|---|---|---|---|
| **轮次轴**（本工具用） | 624 `heatmap`（R1–R6 六轮变异跑批） | 触达**趋势**（`trend` = 后半程触达 − 前半程触达） | **真实日历时间**的下降 |
| **误报率** | 642 追踪器（**67/67 为代理**） | 只有代理值 ⇒ **不据此下结论** | 真实误报率趋势 |
| **逃逸关联** | B4/D1 的逃逸与责任错配案例 | 哪些规则**被最近逃逸绕过/错配** | 逐条时间序列 |

**建议判据（机械；样本不足 ⇒ `insufficient_data`）**：

| 建议 | 判据 |
|---|---|
| `退役候选` | 六轮**全未触达** 且 被逃逸关联过 |
| `收紧候选` | `trend ≤ -2`（后半程明显少触达）且 非退役 |
| `拆分候选` | 被 ≥2 条逃逸案例关联（可能是两条规则被塞进一条） |
| `保留` | 上述都不满足 且 `touched ≥ 1` |
| `insufficient_data` | `touched == 0` 且**无**逃逸关联（**没有证据 ⇒ 不判**） |

只读契约：`--check` 只读、exit 0；`--report` 写 `data/643_rule_aging.md` + `.json`。纯标准库；≥6 例单测。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import escape_root_cause_643 as D1  # noqa: E402
import gate_engine as ge  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "643_rule_aging.md")
OUT_JSON = os.path.join(ROOT, "data", "643_rule_aging.json")
VFDR = os.path.join(ROOT, "data", "vfdr_report_v2_624.json")
TREND_THRESHOLD = -2
TRY_DAYS = 30


def rounds_of(row: dict[str, bool]) -> list[str]:
    return sorted(k for k, v in row.items() if v)


def trend_of(row: dict[str, bool]) -> Optional[int]:
    """后半程触达 − 前半程触达（纯函数）。轮次无法对半 ⇒ None。"""
    keys = sorted(row)
    if len(keys) < 2:
        return None
    half = len(keys) // 2
    first = sum(1 for k in keys[:half] if row[k])
    second = sum(1 for k in keys[half:] if row[k])
    return second - first


def verdict(touched: int, trend: Optional[int], n_escape_links: int) -> tuple[str, str]:
    """(建议, 理由)（纯函数，判据顺序固定）。"""
    if touched == 0 and n_escape_links == 0:
        return "insufficient_data", "六轮无触达且无逃逸关联 ⇒ **没有证据 ⇒ 不判**"
    if touched == 0 and n_escape_links:
        return "退役候选", "六轮全未触达且被逃逸关联 ⇒ 规则可能已死/被绕过"
    if n_escape_links >= 2:
        return "拆分候选", f"被 {n_escape_links} 条逃逸案例关联 ⇒ 可能一条规则管了两件事"
    if trend is not None and trend <= TREND_THRESHOLD:
        return "收紧候选", f"轮次趋势 {trend} ≤ {TREND_THRESHOLD} ⇒ 后半程明显少触达（老化/条件漂移）"
    return "保留", "有触达且无老化证据"


def assess() -> dict[str, Any]:
    hm = {}
    if os.path.exists(VFDR):
        try:
            hm = json.loads(open(VFDR, encoding="utf-8").read()).get("heatmap", {})
        except (OSError, json.JSONDecodeError):
            hm = {}
    d1 = D1.attributable()
    links: dict[str, int] = {}
    for c in d1["cases"]:
        t = str(c.get("target") or "")
        if t.startswith(("ATOM-", "EV-", "CARD-", "PED-", "OBS-", "AUTO-")):
            links[t] = links.get(t, 0) + 1
    rows: list[dict[str, Any]] = []
    for r in ge.RULES:
        row = hm.get(r.id, {})
        touched = len(rounds_of(row))
        tr = trend_of(row) if row else None
        n_links = links.get(r.id, 0)
        v, why = verdict(touched, tr, n_links)
        rows.append({"rule_id": r.id, "severity": r.severity, "rounds_total": len(row),
                     "touched": touched, "trend": tr, "escape_links": n_links,
                     "verdict": v, "why": why})
    by_v: dict[str, int] = {}
    for x in rows:
        by_v[x["verdict"]] = by_v.get(x["verdict"], 0) + 1
    return {"rows": rows, "n_rules": len(rows), "by_verdict": by_v,
            "trend_threshold": TREND_THRESHOLD,
            "unavailable": [
                f"**最近 {TRY_DAYS} 天的命中趋势**：本仓**没有带日期的逐规则命中明细**"
                " ⇒ 只能用**轮次轴**（6 轮变异跑批）替代，**不等于日历时间**",
                "**误报率趋势**：642 追踪器 67/67 为**代理值** ⇒ 不据此下结论（A3 教训 3）",
                "**每条逃逸的时间归属**：逃逸案例无时间字段 ⇒ 只能算\"关联数\"，不能算\"最近\"",
            ]}


def write_report() -> str:
    a = assess()
    interest = [r for r in a["rows"] if r["verdict"] != "保留"]
    lines = [
        "# 643 E2 · 规则老化检测（抗 Goodhart #2）", "",
        f"> 规模 **{a['n_rules']}** 条规则；建议分布 `{a['by_verdict']}`；"
        f"趋势阈值 `≤ {a['trend_threshold']}`；日历窗口 **{TRY_DAYS} 天（不可用，见下）**。", "",
        "## 一、建议清单（非「保留」项）", "",
        "| 规则 | 级别 | 触达轮数 | 趋势 | 逃逸关联 | 建议 | 理由 |",
        "|---|---|---|---|---|---|---|"]
    for r in sorted(interest, key=lambda x: (x["verdict"], x["rule_id"])):
        lines.append(f"| `{r['rule_id']}` | {r['severity']} | {r['touched']}/{r['rounds_total']} | "
                     f"{'—' if r['trend'] is None else r['trend']} | {r['escape_links']} | "
                     f"**{r['verdict']}** | {r['why']} |")
    if not interest:
        lines.append("| — | — | — | — | — | 无 | — |")
    lines += ["", "## 二、⚠️ 口径替代与数据缺口", ""]
    for u in a["unavailable"]:
        lines.append(f"- {u}")
    lines += ["", "> 这三项**不是漏做**而是**数据缺该维度**；本工具**不编造趋势**。", "",
              "## 三、判据（可复算）", "",
              "| 建议 | 判据 |", "|---|---|",
              "| `退役候选` | 六轮全未触达 **且** 有逃逸关联 |",
              "| `拆分候选` | 被 ≥2 条逃逸案例关联 |",
              f"| `收紧候选` | `trend ≤ {TREND_THRESHOLD}`（后半程明显少触达） |",
              "| `保留` | 有触达且无老化证据 |",
              "| `insufficient_data` | 零触达且零关联 ⇒ **没有证据 ⇒ 不判** |", "",
              "## 诚实登记", "",
              "1. **轮次轴 ≠ 日历时间**：6 轮跑批的间隔由批次节奏决定，"
              "**不能**解释为「最近 30 天」；",
              "2. **代理误报率不进判据**（A3 教训 2）：67/67 是代理值，用它判老化等于自欺；",
              "3. **`insufficient_data` 是「结论」不是失败**：没有证据时给"
              "「保留/退役」都是编；",
              "4. **阈值 `trend ≤ -2` 是本批经验值**（边界已在单测固定）；",
              "5. 本工具**只读**：不改规则、不重钉台账。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(a, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    row = {"R1": True, "R2": True, "R3": False, "R4": False, "R5": False, "R6": False}
    chk("趋势：前半 2 触达 / 后半 0 ⇒ -2", trend_of(row) == -2, str(trend_of(row)))
    chk("趋势：全触达 ⇒ 0", trend_of({f"R{i}": True for i in range(1, 7)}) == 0)
    chk("趋势：单轮 ⇒ None（不可对半）", trend_of({"R1": True}) is None)
    chk("趋势：空 ⇒ None", trend_of({}) is None)

    chk("零触达零关联 ⇒ insufficient_data（不判）",
        verdict(0, None, 0)[0] == "insufficient_data")
    chk("零触达有关联 ⇒ 退役候选", verdict(0, None, 1)[0] == "退役候选")
    chk("≥2 关联 ⇒ 拆分候选（优先于收紧）", verdict(3, -5, 2)[0] == "拆分候选")
    chk("趋势越阈 ⇒ 收紧候选", verdict(3, -2, 0)[0] == "收紧候选")
    chk("趋势差一格不触发", verdict(3, -1, 0)[0] == "保留")

    a = assess()
    chk("67 规则在册且分布自洽",
        a["n_rules"] == 67 and sum(a["by_verdict"].values()) == 67)
    chk("数据缺口登记非空", len(a["unavailable"]) >= 3)
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="643 E2 规则老化检测")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写报告")
    ap.add_argument("--json", action="store_true", help="打印（JSON）")
    x = ap.parse_args(argv)
    if x.check:
        return selftest()
    if x.report:
        print(f"written {write_report()}")
        return 0
    a = assess()
    if x.json:
        print(json.dumps({"by_verdict": a["by_verdict"],
                          "unavailable": a["unavailable"]}, ensure_ascii=False, indent=2))
        return 0
    print(f"[rule-aging] {a['n_rules']} 规则 ⇒ {a['by_verdict']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
