"""644 C2 证据-卡片关联层单测（L2-1..L2-5）。"""
from __future__ import annotations

import evidence_card_link_644 as c2


# L2-1：关联建立正确（多对多）
def test_link_many_to_many():
    idx = c2.new_index()
    c2.link(idx, "E1", "C1", "support", "t", "tester")
    c2.link(idx, "E1", "C2", "refute", "t", "tester")
    c2.link(idx, "E2", "C1", "background", "t", "tester")
    assert sorted(c2.query_card(idx, "C1")) == ["E1", "E2"]
    assert sorted(c2.query_evidence(idx, "E1")) == ["C1", "C2"]


# L2-2：引用方式分类合理
def test_relation_classification():
    idx = c2.new_index()
    c2.link(idx, "E1", "C2", "refute", "t", "tester")
    rel = [l for l in idx["links"] if l["evidence_id"] == "E1" and l["card_id"] == "C2"]
    assert rel and rel[0]["relation"] == "refute"


# L2-3：幂等（重复 link 不增加条目）
def test_idempotent():
    idx = c2.new_index()
    c2.link(idx, "E1", "C1", "support", "t", "tester")
    n0 = len(idx["links"])
    c2.link(idx, "E1", "C1", "support", "t", "tester")
    assert len(idx["links"]) == n0


# L2-4：从现有证据构建索引非空
def test_build_from_existing():
    idx = c2.build_index_from_existing()
    assert len(idx["links"]) > 0


# L2-5：selftest 通过
def test_selftest():
    assert c2.selftest() == 0
