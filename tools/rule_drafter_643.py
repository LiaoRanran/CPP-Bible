"""643 D2 · **规则草案生成器**（智能层：自动提案规则 #2）。

**定位**：基于 D1 的归因（**反例驱动**，A4-D-1），生成 **≤10 条规则草案**，
每条带：名称 / 触发条件 / 判定逻辑 / 预期效果 / **理由（可追溯到具体案例）** /
**MDL 编码长度** / **blast radius 估算**。**只出草案，不写生产规则库。**

**草案的两个来源（都带 provenance，且都标"近似"程度）**：

| 来源 | 触发 | 草案形态 |
|---|---|---|
| **反例（硬证据）** | D1 的 `规则缺失` 案例 | **新规则**草案（`NEW`） |
| **静态盲点（软线索）** | C1 的 `field_missing_silent` 盲点 | **修改**草案（`MODIFY`：为该规则补「字段缺失即报」分支） |

**排序**：`priority = 证据强度 × 影响面 / MDL 成本`（证据强度：反例=3、静态盲点=1；
影响面 = 涉及卡/规则数；成本 = MDL bits 归一化）。**与 637 的倒挂缺陷相反**：证据强度进公式。

**铁律**：草案写 `data/643_rule_drafts.json`（**侧车**），
**绝不写入 `gate_engine.py`**、**不改现有 67 条规则**、**severity 默认 `advice`**（从宽起步，A1-C4）。

只读契约：`--check` 只读、exit 0；`--report` 写 `data/643_rule_drafts.md` + `.json`。
纯标准库；≥6 例单测。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import coverage_gap_scanner_643 as B1  # noqa: E402
import escape_root_cause_643 as D1  # noqa: E402
import rule_precondition_analyzer_643 as C1  # noqa: E402

OUT_MD = os.path.join(ROOT, "data", "643_rule_drafts.md")
OUT_JSON = os.path.join(ROOT, "data", "643_rule_drafts.json")
MAX_DRAFTS = 10
EVIDENCE_WEIGHT = {"反例": 3, "静态盲点": 1}
DEFAULT_SEVERITY = "advice"          # 从宽起步（A1-C4）
BASE_COST_BITS = 64                  # 与 636/642 同源的编码长度式：8*len(id)+8*len(title)+32


def mdl_bits(rule_id: str, title: str) -> int:
    """MDL 编码长度（**与 642/636 同式**：`8*len(id) + 8*len(title) + 32`）。"""
    return 8 * len(rule_id) + 8 * len(title) + 32


def make_draft(rule_id: str, title: str, trigger: str, decision: str,
               provenance: dict[str, Any], evidence: str,
               blast_cards: int, blast_rules: int = 0) -> dict[str, Any]:
    bits = mdl_bits(rule_id, title)
    impact = max(1, blast_cards) + blast_rules
    prio = round(EVIDENCE_WEIGHT.get(evidence, 1) * impact / (bits / BASE_COST_BITS), 3)
    return {"draft_id": hashlib.sha256(f"{rule_id}|{title}".encode()).hexdigest()[:12],
            "kind": provenance.get("kind", "NEW"),
            "proposed_rule_id": rule_id, "title": title,
            "trigger": trigger, "decision": decision,
            "severity": DEFAULT_SEVERITY,
            "expected_block_rate": None,
            "mdl_bits": bits,
            "blast_radius": {"cards": blast_cards, "rules": blast_rules},
            "provenance": provenance,
            "evidence": evidence, "priority": prio,
            "generated_by": "rule_drafter_643", "version": "643.1"}


def drafts() -> dict[str, Any]:
    cov = B1.report()
    card_hits = cov["analysis"]["card_hit_counts"]
    out: list[dict[str, Any]] = []

    # 来源 1：D1 的可行动反例（规则缺失 → 新规则草案）
    d1 = D1.attributable()
    for i, case in enumerate(d1["actionable"]):
        if case["cause"] != "规则缺失":
            continue
        out.append(make_draft(
            f"ATOM-DRAFT-{i + 1:03d}",
            f"补：{case['card']} 上的逃逸面（{case['op']}）",
            f"卡 `{case['card']}`；缺失面 = {case['op']}",
            "命中即报（建议先 advice）",
            {"kind": "NEW", "case_id": case["case_id"], "source": case["source"],
             "card": case["card"], "op": case["op"]},
            "反例", 1))

    # 来源 2：C1 的 field_missing_silent 盲点（软线索 ⇒ 修改草案）
    pre = C1.analyze()
    soft = [r for r in pre["rows"]
            if any(b["kind"] == "field_missing_silent" for b in r["blind_spots"])]
    soft.sort(key=lambda r: (-card_hits.get(r["rule_id"], 0), r["rule_id"]))
    for r in soft[:MAX_DRAFTS]:
        hits = card_hits.get(r["rule_id"], 0)
        out.append(make_draft(
            f"MOD-{r['rule_id']}",
            f"为 `{r['rule_id']}` 补「必备字段缺失即报」分支",
            f"scope={r['scope']}；引用字段 {', '.join(r['precondition']['fields'][:4]) or '（未识别）'}",
            "字段缺失时**显式报告**（当前可能静默跳过）",
            {"kind": "MODIFY", "target_rule": r["rule_id"],
             "check_fn": r["check_fn"], "fields": r["precondition"]["fields"]},
            "静态盲点", max(1, hits), 1))

    out.sort(key=lambda d: (-d["priority"], d["proposed_rule_id"]))
    out = out[:MAX_DRAFTS]
    by_kind: dict[str, int] = {}
    by_ev: dict[str, int] = {}
    for d in out:
        by_kind[d["kind"]] = by_kind.get(d["kind"], 0) + 1
        by_ev[d["evidence"]] = by_ev.get(d["evidence"], 0) + 1
    return {"drafts": out, "n": len(out), "by_kind": by_kind, "by_evidence": by_ev,
            "max_drafts": MAX_DRAFTS,
            "n_actionable_cases": len(d1["actionable"]),
            "n_soft_blind_spots": len(soft),
            "severity_default": DEFAULT_SEVERITY, "written_to_rule_db": False}


def write_report() -> str:
    d = drafts()
    lines = [
        "# 643 D2 · 规则草案（智能层：自动提案规则 #2；**只出草案**）", "",
        f"> 草案 **{d['n']}** 条（上限 {d['max_drafts']}）；形态 `{d['by_kind']}`；"
        f"证据类型 `{d['by_evidence']}`。",
        f"> 来源：反例（可行动案例 **{d['n_actionable_cases']}** 条）+ "
        f"静态盲点（**{d['n_soft_blind_spots']}** 条候选，取前 {MAX_DRAFTS}）。",
        f"> **默认 severity = `{d['severity_default']}`**（从宽起步，A1-C4）；"
        f"**未写入规则库**（`written_to_rule_db={d['written_to_rule_db']}`）。", "",
        "## 一、草案清单（按 priority 降序）", "",
        "| # | 形态 | 拟用 id | 标题 | 触发条件 | 判定 | MDL bits | blast | 证据 | priority |",
        "|---|---|---|---|---|---|---|---|---|---|"]
    for i, x in enumerate(d["drafts"], 1):
        br = x["blast_radius"]
        lines.append(f"| {i} | `{x['kind']}` | `{x['proposed_rule_id']}` | {x['title']} | "
                     f"{x['trigger']} | {x['decision']} | {x['mdl_bits']} | "
                     f"卡{br['cards']}/规则{br['rules']} | {x['evidence']} | {x['priority']} |")
    if not d["drafts"]:
        lines.append("| — | — | — | **零草案** | — | — | — | — | — | — |")
    lines += ["", "## 二、逐条理由（可追溯）", ""]
    for i, x in enumerate(d["drafts"], 1):
        lines.append(f"{i}. `{x['proposed_rule_id']}`（{x['kind']}）：provenance = "
                     f"`{json.dumps(x['provenance'], ensure_ascii=False)}`")
    lines += ["", "## 诚实登记", "",
              "1. **自动提案 ≠ 规则真的好**（§十二.3）：MDL/反涟漪通过**不代表规则正确**，"
              "必须人审；",
              "2. **`expected_block_rate` 一律为 `None`**（本工具**不估**）："
              "没有实测就没有数字，估了就是编（估计留 D4/E1 用实测填）；",
              "3. **静态盲点类草案（MODIFY）是「软线索」**：C1 只证明「该规则引用了字段」，"
              "**没有**证明它缺「缺失即报」分支 ⇒ 证据权重只有反例的 1/3，"
              "且**必须逐条人读代码**后才能立项；",
              "4. **反例类草案只有"
              f"{d['n_actionable_cases']} 条**：因为 v7 的 9 条逃逸里 8 条是语义等价"
              "（能力天花板，不该自动化）⇒ 反例供给**天然稀薄**，这是实情不是漏做；",
              "5. **排序公式含证据强度**（反例 3 / 静态 1）：刻意修掉 637 的"
              "「公式不含严重度/证据强度」型倒挂；",
              "6. 本工具**只写侧车 JSON**：不动 `gate_engine.py`、不动现有 67 条规则。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(d, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("MDL 式与 642/636 同形", mdl_bits("ABC", "T") == 8 * 3 + 8 * 1 + 32,
        str(mdl_bits("ABC", "T")))
    a = make_draft("X-1", "T", "trig", "dec", {"kind": "NEW"}, "反例", 2)
    chk("草案字段齐备",
        {"draft_id", "kind", "proposed_rule_id", "title", "trigger", "decision",
         "severity", "expected_block_rate", "mdl_bits", "blast_radius", "provenance",
         "evidence", "priority"} <= set(a))
    chk("默认 severity 从宽（advice）", a["severity"] == "advice")
    chk("expected_block_rate 不编造（None）", a["expected_block_rate"] is None)
    chk("证据强度进公式（反例 > 静态，同规模）",
        make_draft("X-1", "T", "t", "d", {}, "反例", 2)["priority"]
        > make_draft("X-1", "T", "t", "d", {}, "静态盲点", 2)["priority"])
    chk("id 稳定（同题目 ⇒ 同 draft_id）",
        make_draft("X-1", "T", "t", "d", {}, "反例", 2)["draft_id"]
        == make_draft("X-1", "T", "t", "d", {}, "反例", 2)["draft_id"])

    d = drafts()
    chk("草案数 ≤ 上限", d["n"] <= MAX_DRAFTS, str(d["n"]))
    chk("未写规则库", d["written_to_rule_db"] is False)
    chk("每条草案都有可追溯 provenance",
        all(x["provenance"] for x in d["drafts"]))
    chk("按 priority 降序",
        all(d["drafts"][i]["priority"] >= d["drafts"][i + 1]["priority"]
            for i in range(len(d["drafts"]) - 1)))
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="643 D2 规则草案生成")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写草案（侧车）")
    ap.add_argument("--json", action="store_true", help="打印草案（JSON）")
    x = ap.parse_args(argv)
    if x.check:
        return selftest()
    if x.report:
        print(f"written {write_report()}")
        return 0
    d = drafts()
    if x.json:
        print(json.dumps(d, ensure_ascii=False, indent=2))
        return 0
    print(f"[rule-drafter] 草案 {d['n']} 条 ⇒ 形态 {d['by_kind']}；证据 {d['by_evidence']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
