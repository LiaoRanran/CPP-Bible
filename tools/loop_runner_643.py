"""643 E3 · **闭环第 4 次运行（R4）**（抗 Goodhart #3）。

**定位**：跑闭环第 4 轮（637 R1 / 638 R2 / 642 R3 / **643 R4**），
按 inbox 要求**用 B5 的问题发现器替代 637 的静态指标采集**、**用 C2 的攻击生成器替代 637 的方案库**，
并记录**候选数 / 采纳数 / 事后验证结果**与**校准度**。

**R4 的三个数字（口径必须看清）**：
| 项 | 值 | 口径 |
|---|---|---|
| 候选数 | B5 问题清单 + D2 草案 | 智能层本批产出的**可采纳项** |
| 采纳数 | **0** | **人审未批**（机器不代签，本批不代决） |
| 事后验证 | **20 条**（C4 已实测的子集） | C4 的等预算对比里**已有实测结论**的那部分 |
| 校准度 | **预期兑现率 2/20 = 10.0%** | **可验证子集口径**（≠ R1 的"建议靠谱率"、R1/R2/R3 口径各不相同） |

**为什么 R4 有数字而 R3 是 `None`**：R3 时没有任何可验证子集（全部待人审）；
本批 C4 实测了 20 条候选的"预期是否兑现" ⇒ 出现了一个**可验证子集**。
但**口径与 R1/R2/R3 都不同** ⇒ **不可直接连成趋势**（如实登记）。

**不写 642 的台账**：`data/642_loop_calibration.json` 属 642 批产物；
R4 写 `data/643_loop_r4.json`，**是否并入 642 台账交人裁决**。

只读契约：`--check` 只读、exit 0；`--report` 写 `data/643_loop_r4.md` + `.json`。纯标准库；≥6 例单测。
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

import cost_benefit_637 as cb637  # noqa: E402
import issue_dispatcher_643 as B5  # noqa: E402
import rule_drafter_643 as D2  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "643_loop_r4.md")
OUT_JSON = os.path.join(ROOT, "data", "643_loop_r4.json")
QUALITY_JSON = os.path.join(ROOT, "data", "643_attack_quality.json")
EXPANSION_THRESHOLD = 0.60
RISK_CLASS = {"missing_dimension": "report", "rule_single_card": "report",
              "rule_should_hold": "report"}


def risk_class_of(kind: str) -> str:
    return RISK_CLASS.get(kind, "tool" if "rule" in kind else "report")


def calibrate() -> dict[str, Any]:
    """R4 校准度（可验证子集口径）：取 C4 实测的预期兑现率。"""
    if not os.path.exists(QUALITY_JSON):
        return {"calibration": None, "verified_subset": 0, "realized": 0,
                "why": "C4 未跑 ⇒ 无可验证子集（R4 校准度 = None）"}
    try:
        q = json.loads(open(QUALITY_JSON, encoding="utf-8").read())
    except (OSError, json.JSONDecodeError) as exc:
        return {"calibration": None, "verified_subset": 0, "realized": 0,
                "why": f"C4 结果不可读（{type(exc).__name__}）"}
    t = q.get("targeted", {})
    eff = int(t.get("effective") or 0)
    rate = t.get("oracle_hit_rate")
    realized = round((rate or 0) * eff)
    return {"calibration": rate, "verified_subset": eff, "realized": realized,
            "why": f"C4 的定向组 {eff} 条有效候选里，**预期兑现 {realized} 条**"
                   f"（`oracle_hit_rate={rate}`）",
            "caliber": "**可验证子集口径**（预期兑现率）≠ R1/R2/R3 的口径"}


def run() -> dict[str, Any]:
    d5 = B5.dispatch()
    d2 = D2.drafts()
    cands = []
    for it in d5["top"]:
        cands.append({"candidate_id": it["issue_id"], "source": "B5",
                      "kind": it["kind"], "target": it["target"],
                      "cost": it["cost"], "benefit": it["impact"],
                      "risk_class": risk_class_of(it["kind"]),
                      "score_643": it["score"]})
    for dr in d2["drafts"]:
        cands.append({"candidate_id": dr["draft_id"], "source": "D2",
                      "kind": dr["kind"], "target": dr["proposed_rule_id"],
                      "cost": 2, "benefit": dr["blast_radius"]["cards"],
                      "risk_class": "core" if dr["kind"] == "MODIFY" else "tool",
                      "score_643": dr["priority"]})
    # 复用 637 的 cost/benefit 打分（**只调纯函数**，不跑它的 IO）
    for c in cands:
        try:
            c["score_637"] = round(cb637.score_one(c["cost"] * 10, c["benefit"] * 10,
                                                   c["risk_class"]), 4)
        except Exception as exc:  # noqa: BLE001
            c["score_637"] = None
            c["score_637_error"] = f"{type(exc).__name__}: {exc}"
    cal = calibrate()
    return {"round": "R4", "batch": 643, "at": "2026-09-26",
            "candidates": len(cands), "adopted": 0,
            "verified_subset": cal["verified_subset"], "realized": cal["realized"],
            "calibration": cal["calibration"], "calibration_why": cal["why"],
            "caliber": cal.get("caliber", ""),
            "by_source": {"B5": sum(1 for c in cands if c["source"] == "B5"),
                          "D2": sum(1 for c in cands if c["source"] == "D2")},
            "candidate_rows": cands,
            "replaces": {"observer": "B5 issue_dispatcher_643（问题发现器替代静态指标）",
                         "generator": "C2 targeted_mutator_643（攻击生成器替代方案库）"},
            "merged_into_642_ledger": False,
            "threshold": EXPANSION_THRESHOLD,
            "meets_threshold": bool(cal["calibration"] is not None
                                    and cal["calibration"] >= EXPANSION_THRESHOLD)}


def write_report() -> str:
    r = run()
    lines = [
        "# 643 E3 · 闭环第 4 次运行（R4）", "",
        f"> 候选 **{r['candidates']}**（B5 {r['by_source']['B5']} + D2 {r['by_source']['D2']}）、"
        f"采纳 **{r['adopted']}**（人审未批）、事后验证子集 **{r['verified_subset']}**、"
        f"兑现 **{r['realized']}** ⇒ **校准度 {r['calibration']}**。",
        f"> 门槛 **{r['threshold']:.0%}** ⇒ **{'达标' if r['meets_threshold'] else '未达标'}**。",
        f"> 校准度依据：{r['calibration_why']}",
        f"> 口径：{r['caliber']}", "",
        "## 一、R1→R4 四点（**口径各不相同，不可直接连线**）", "",
        "| 轮次 | 批次 | 候选 | 采纳 | 事后验证 | 校准度 | 口径 |",
        "|---|---|---|---|---|---|---|",
        "| R1 | 637 | 8 | 3 | 8 | **37.5%** | 建议靠谱率（人工逐条打分） |",
        "| R2 | 638 | 4 | 3 | 4 | **50.0%** | 1 − 误报率（异常检出准确率，派生） |",
        "| R3 | 642 | 157 | 0 | 0 | **None** | 未代决 ⇒ 无从验证（**不是 0**） |",
        f"| **R4** | **643** | {r['candidates']} | {r['adopted']} | "
        f"{r['verified_subset']} | **{r['calibration']}** | "
        "可验证子集：预期兑现率 |", "",
        "## 二、本轮替代了什么（inbox 要求）", "",
        f"- 观测器：**{r['replaces']['observer']}**；",
        f"- 生成器：**{r['replaces']['generator']}**。", "",
        "## 三、候选明细（含 637 打分对照）", "",
        "| 候选 | 来源 | 类别 | 目标 | cost | benefit | 643 score | 637 score |",
        "|---|---|---|---|---|---|---|---|"]
    for c in r["candidate_rows"]:
        lines.append(f"| `{c['candidate_id']}` | {c['source']} | `{c['kind']}` | "
                     f"{c['target']} | {c['cost']} | {c['benefit']} | {c['score_643']} | "
                     f"{c['score_637']} |")
    lines += ["", "## 诚实登记", "",
              "1. **R4 的校准度口径与 R1/R2/R3 都不同** ⇒ **不能连成趋势**"
              "（642 C2 已登记「口径不同」的坑，本批继续显式标注）；",
              "2. **采纳数 0 是实情**：机器**不代签**，草案与人审项都未获批准 ⇒ "
              "「采纳」一栏为 0 不是失败；",
              "3. **事后验证的是「可验证子集」**（C4 的 20 条）**不是候选全集**"
              f"（{r['candidates']} 条）⇒ 校准度是**子集指标**；",
              "4. **未并入 642 的台账**（`data/642_loop_calibration.json` 属 642 批产物）"
              "⇒ R4 写 643 自己的文件，**是否并入交人裁决**；",
              "5. **复用 637 只是纯函数**（`score_one`）：未跑 637 的 observer/detector/memo IO，"
              "避免跨批污染与重跑成本；",
              "6. 门槛 60% 是 642 定下的经验值，本工具**不改**它。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(r, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("风险档映射（默认 report，规则类 tool，MODIFY=core 由调用方给）",
        risk_class_of("missing_dimension") == "report"
        and risk_class_of("rule_too_hot") == "tool")

    r = run()
    chk("候选 = B5 前 10 + D2 草案", r["candidates"] == r["by_source"]["B5"]
        + r["by_source"]["D2"] and r["candidates"] > 0, str(r["by_source"]))
    chk("采纳数恒为 0（不代签）", r["adopted"] == 0)
    chk("校准度 = 兑现/子集（可复算）",
        r["calibration"] is None
        or abs(r["calibration"] - r["realized"] / r["verified_subset"]) < 0.02,
        f"{r['realized']}/{r['verified_subset']}={r['calibration']}")
    chk("门槛判定一致（>= 60%）",
        r["meets_threshold"] == (r["calibration"] is not None
                                 and r["calibration"] >= EXPANSION_THRESHOLD))
    chk("未并入 642 台账", r["merged_into_642_ledger"] is False)
    chk("637 打分已复用（或明确报错）",
        all(("score_637" in c) for c in r["candidate_rows"]))
    chk("替代项写实", "issue_dispatcher" in r["replaces"]["observer"]
        and "targeted_mutator" in r["replaces"]["generator"])
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="643 E3 闭环 R4")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写 R4 报告")
    ap.add_argument("--json", action="store_true", help="打印 R4（JSON）")
    x = ap.parse_args(argv)
    if x.check:
        return selftest()
    if x.report:
        print(f"written {write_report()}")
        return 0
    r = run()
    if x.json:
        print(json.dumps({k: v for k, v in r.items() if k != "candidate_rows"},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"[loop-R4] 候选 {r['candidates']} / 采纳 {r['adopted']} / "
          f"校准度 {r['calibration']}（门槛 {r['threshold']:.0%} "
          f"{'达标' if r['meets_threshold'] else '未达标'}）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
