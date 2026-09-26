"""643 D2 · rule_drafter_643 单测（MDL 式/草案字段/排序/上限/不写库）。
编号 D2-1..D2-8。
"""
from __future__ import annotations

import rule_drafter_643 as D2


# D2-1：MDL 编码长度与 642/636 同式
def test_mdl_formula_matches_642():
    assert D2.mdl_bits("ABCD", "TITLE") == 8 * 4 + 8 * 5 + 32
    assert D2.mdl_bits("", "") == 32


# D2-2：草案字段齐备
def test_draft_fields():
    d = D2.make_draft("X-1", "T", "trig", "dec", {"kind": "NEW"}, "反例", 2)
    need = {"draft_id", "kind", "proposed_rule_id", "title", "trigger", "decision",
            "severity", "expected_block_rate", "mdl_bits", "blast_radius", "provenance",
            "evidence", "priority"}
    assert need <= set(d)


# D2-3：默认 severity 从宽（advice）+ expected_block_rate 不编造
def test_defaults_are_honest():
    d = D2.make_draft("X-1", "T", "t", "d", {}, "反例", 1)
    assert d["severity"] == "advice"
    assert d["expected_block_rate"] is None


# D2-4：证据强度进公式（反例 > 静态盲点，同规模）
def test_evidence_weight_in_formula():
    hi = D2.make_draft("X-1", "T", "t", "d", {}, "反例", 2)
    lo = D2.make_draft("X-1", "T", "t", "d", {}, "静态盲点", 2)
    assert hi["priority"] > lo["priority"]


# D2-5：draft_id 稳定（同输入同 id）
def test_draft_id_stable():
    a = D2.make_draft("X-1", "T", "t", "d", {}, "反例", 1)
    b = D2.make_draft("X-1", "T", "t", "d", {}, "反例", 1)
    assert a["draft_id"] == b["draft_id"] and len(a["draft_id"]) == 12


# D2-6：≥10 条候选 ⇒ 截断到上限且按 priority 降序
def test_cap_and_order():
    d = D2.drafts()
    assert d["n"] <= D2.MAX_DRAFTS, d["n"]
    pr = [x["priority"] for x in d["drafts"]]
    assert pr == sorted(pr, reverse=True)


# D2-7：**未写规则库**（铁律）+ 每条都有 provenance
def test_not_written_to_rule_db():
    d = D2.drafts()
    assert d["written_to_rule_db"] is False
    assert all(x["provenance"] for x in d["drafts"])


# D2-8：形态与证据分类自洽 + 只读自检
def test_kind_and_evidence_counts():
    d = D2.drafts()
    assert sum(d["by_kind"].values()) == d["n"]
    assert sum(d["by_evidence"].values()) == d["n"]
    assert all(x["kind"] in ("NEW", "MODIFY") for x in d["drafts"])
    assert D2.selftest() == 0
