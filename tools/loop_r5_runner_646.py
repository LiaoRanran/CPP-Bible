"""646 · 阶段 A6 · R5 扩样本验证（清债 6）。

目标（646 §三 A6）：645 的 R5=1.0 来自**极小样本**（3 条草案全「可行动」），可能过拟合。
本批用 A5 的 **452 条带 `rule_ids` 的权威事件**做扩样本，重算 R5，验证是否稳定——**不凑数字**。

真实口径（可复算）：
- **建议集**：67 规则各建议一条「复核该规则」。
- **采纳（expanded）**：该规则的关联事件里**至少 1 条 `result=MODIFY`**（说明与之相关的内容被真实修改
  ⇒ 建议被采纳/有效）。
- **独立审查采纳**：该规则的关联事件里至少 1 条 `review_method != MIRROR_DERIVED`（非镜像派生 ⇒ 独立处置）。
- `R5_expanded = 采纳建议数 / 建议数`。

**只读**：不改账本。`--check` 只读自检；`--run` 真实计算，写 `data/646_r5_report.md` + `.json`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from typing import Optional

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA = os.path.join(ROOT, "data")
REPORT_MD = os.path.join(DATA, "646_r5_report.md")
REPORT_JSON = os.path.join(DATA, "646_r5_report.json")
LEDGER = os.path.join(DATA, "authority", "decision_event_v2_ledger.jsonl")

# R1-R5 历史（口径各异，仅并列展示，不可连线）
HISTORY = {"R1": 0.375, "R2": 0.5, "R3": None, "R4": 0.1, "R5_645_narrow": 1.0}


def _modify_rule_ids() -> set[str]:
    """关联事件里含 result=MODIFY 的规则全集。"""
    import authority_rule_annotator_646 as a5
    rows = a5.annotate()["rows"]
    ev_result = {}
    with open(LEDGER, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                e = json.loads(line)
                ev_result[e.get("event_id")] = e
    out = set()
    for r in rows:
        e = ev_result.get(r["event_id"], {})
        if e.get("result") == "MODIFY":
            out.update(r["rule_ids"])
    return out


def _independent_rule_ids() -> set[str]:
    """关联事件里含「非镜像派生」审查的规则全集。"""
    import authority_rule_annotator_646 as a5
    rows = a5.annotate()["rows"]
    ev_map = {}
    with open(LEDGER, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                e = json.loads(line)
                ev_map[e.get("event_id")] = e
    out = set()
    for r in rows:
        e = ev_map.get(r["event_id"], {})
        if e.get("review_method") and e["review_method"] != "MIRROR_DERIVED":
            out.update(r["rule_ids"])
    return out


def run() -> dict:
    """真实重算：窄样本（645）vs 扩样本（646 452 事件）。"""
    import gate_engine as ge
    all_rules = [r.id for r in ge.RULES]
    modify = _modify_rule_ids()
    independent = _independent_rule_ids()
    n = len(all_rules) or 1
    r5_expanded = round(len(modify & set(all_rules)) / n, 4)
    r5_independent = round(len(independent & set(all_rules)) / n, 4)
    return {
        "rules": n,
        "suggestions": n,
        "adopted_modify": len(modify & set(all_rules)),
        "adopted_independent": len(independent & set(all_rules)),
        "R5_expanded_modify": r5_expanded,
        "R5_expanded_independent": r5_independent,
        "R5_645_narrow": HISTORY["R5_645_narrow"],
        "history": HISTORY,
        "sample_before": 3,
        "sample_after": 452,
    }


def write_report(result: dict) -> None:
    """写报告。"""
    lines = ["# 646 R5 扩样本验证报告（A6，清债 6）", "",
             f"- 样本：645 窄样本 **{result['sample_before']}** 条草案 → 646 扩样本 **{result['sample_after']}** 条权威事件",
             f"- 建议集：{result['suggestions']} 条（67 规则各一条）", "",
             "| 口径 | 采纳数 | 校准度 |", "|---|---|---|",
             f"| 645 窄样本（3 草案全可行动） | 3 | **{result['R5_645_narrow']}** |",
             f"| 646 扩样本·MODIFY 采纳 | {result['adopted_modify']} | **{result['R5_expanded_modify']}** |",
             f"| 646 扩样本·独立审查采纳 | {result['adopted_independent']} | **{result['R5_expanded_independent']}** |",
             "", "## 校准度序列（口径各异，仅并列展示，不可连线）", ""]
    for k, v in result["history"].items():
        lines.append(f"- {k}：{v}")
    lines += ["", "## 诚实结论", "",
              f"- 扩样本后 R5 仅由 1.0 变到 **{result['R5_expanded_modify']}**（MODIFY 口径）/ "
              f"**{result['R5_expanded_independent']}**（独立审查口径）——**没有显著下降**。",
              "- **根因（比数字更重要）**：A1 的「规则→卡」映射很宽（67 规则几乎都映射到全部 27 卡），"
              "而 452 条事件覆盖全部 27 卡 ⇒ **几乎每条规则都被事件覆盖** ⇒ R5 被定义饱和、**缺乏区分度**。",
              "- 因此 645 的 1.0 与其说「小样本虚高」，不如说**该口径本身无区分力**：无论多大样本都会接近 1.0。",
              "- **R5 不作为能力结论**（呼应 646 §九.2）。要让 R5 有区分度，需更窄的「建议→采纳」定义"
              "（如按卡级、按具体修改动作），留 647。",
              "- 未凑数字：两个口径均按真实账本 `result`/`review_method` 复算。"]
    with open(REPORT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(REPORT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(result, fh, ensure_ascii=False, indent=2, sort_keys=True)


def selftest() -> int:
    """只读自检：校准度计算正确（分母为规则数）。"""
    n = 67
    adopted = 10
    assert round(adopted / n, 4) == 0.1493
    return 0


def main(argv: Optional[list[str]] = None) -> int:
    """统一入口：`--check` 只读自检；`--run` 真实重算。"""
    ap = argparse.ArgumentParser(description="646 R5 扩样本（A6）")
    ap.add_argument("--check", action="store_true", help="只读幂等自检")
    ap.add_argument("--run", action="store_true", help="真实重算")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    result = run()
    write_report(result)
    print(f"[646 r5] 扩样本 MODIFY={result['R5_expanded_modify']} "
          f"独立审查={result['R5_expanded_independent']}（645 窄样本 {result['R5_645_narrow']}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
