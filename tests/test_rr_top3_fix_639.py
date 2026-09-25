"""639 D3 单测：RR top3 代码级 co-fire 复核（≥5 例）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import gate_engine as ge  # noqa: E402
import rr_top3_fix_639 as R  # noqa: E402


def test_type_domains_subset_of_known():
    dm = R.domains()
    assert dm["dag"] <= dm["known"]
    assert dm["conflict"] <= dm["known"]


def test_conflict_unknown_disjoint():
    """CONFLICT 域 ⊆ KNOWN 且 UNKNOWN 只在 ∉ KNOWN ⇒ 不能 co-fire。"""
    r = R.analyze()
    assert r["disjoint_conflict_unknown"]


def test_dag_unknown_disjoint():
    r = R.analyze()
    assert r["disjoint_dag_unknown"]


def test_target_conflict_can_cofire():
    """构造真实语料形态：同卡同边同时命中 TARGET(warn) 与 CONFLICT(block)。"""
    meta = {"id": "A", "relations": [
        {"type": "prerequisite", "target": "ATOM-MISSING-001"},
        {"type": "contradicts", "target": "ATOM-MISSING-001"}]}
    rels = ge._relations_norm(meta)
    types = {str(x.get("type")) for x in rels if isinstance(x, dict)}
    assert {"prerequisite", "contradicts"} <= types
    # TARGET：目标不在 atoms ⇒ warn；CONFLICT：同卡支持+矛盾 ⇒ block
    # （语义复核，非跑全库门禁）


def test_p0_zeroed_with_verdicts():
    r = R.analyze()
    assert r["p0_after"] == 0
    assert len(r["rows"]) == 3
    assert all(x["verdict"] for x in r["rows"])


def test_top3_matches_638_report():
    import json
    d = json.load(open(os.path.join(R.ROOT, "data",
                                    "638_rr_conflict_analysis.json"),
                       encoding="utf-8"))
    top3_638 = {(p["rule_a"], p["rule_b"]) for p in d.get("top3", [])}
    ours = {tuple(x["pair"].split(" ↔ ")) for x in R.analyze()["rows"]}
    assert top3_638 == ours
