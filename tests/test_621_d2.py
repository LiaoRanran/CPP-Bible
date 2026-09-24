"""621 D2 · 人审质量评估 单测"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import human_review_quality_compare_621 as Q  # noqa: E402
import soft_baseline_634 as SB  # 634 A3  # noqa: E402


def test_reason_stats_basic():
    rows = [{"reason": "a" * 10}, {"reason": "a" * 10}, {"reason": "b" * 20}]
    st = Q.reason_stats(rows, "reason")
    assert st["length"]["n"] == 3
    assert st["length"]["max"] == 20
    assert st["unique_reasons"] == 2
    assert st["diversity"] == round(2 / 3, 4)


def test_reason_stats_empty():
    st = Q.reason_stats([], "reason")
    assert st["length"]["n"] == 0
    assert st["diversity"] is None


def test_edge_direction_parsing():
    d = Q.edge_direction("ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-1")
    assert d == {"src": "MIS-LANG-001", "dst": "ATOM-LANG-INLINE-001", "prop": "prop-1"}
    assert Q.edge_direction("bad-id") is None


def test_consistency_literal_vs_normalized():
    """MODIFY(建议) vs OVERRIDE(批量) 字面不一致，但语义族一致。"""
    batch = [{"target": {"id": "ae-A->B::prop-1"}, "power": "OVERRIDE"},
             {"target": {"id": "ae-C->D::prop-1"}, "power": "ACCEPT"},
             {"target": {"id": "ae-E->F::prop-1"}, "power": "ACCEPT"}]
    props = [{"target": {"id": "ae-A->B::prop-1"}, "suggested_decision": "MODIFY"},
             {"target": {"id": "ae-C->D::prop-1"}, "suggested_decision": "ACCEPT"},
             {"target": {"id": "ae-E->F::prop-1"}, "suggested_decision": "REJECT"}]
    c = Q.decision_consistency(batch, props)
    # 字面：仅 C->D 字面相同 ⇒ same=1；A->B(MODIFY vs OVERRIDE) 与 E->F(REJECT vs ACCEPT) 不同 ⇒ diff=2
    assert c["same"] == 1 and c["diff"] == 2
    # 语义族：A->B 归一后相同 ⇒ norm_same=2；E->F 是 accept vs reject ⇒ norm_diff=1
    assert c["norm_same"] == 2 and c["norm_diff"] == 1
    # E->F 是真正的语义分歧（不是词汇映射噪音）
    assert len(c["semantic_disagreements"]) == 1
    assert c["semantic_disagreements"][0]["edge"] == "ae-E->F::prop-1"


def test_consistency_detects_real_semantic_disagreement():
    batch = [{"target": {"id": "ae-A->B::prop-1"}, "power": "ACCEPT"}]
    props = [{"target": {"id": "ae-A->B::prop-1"}, "suggested_decision": "REJECT"}]
    c = Q.decision_consistency(batch, props)
    assert c["norm_diff"] == 1
    assert len(c["semantic_disagreements"]) == 1


def test_consistency_unknown_when_missing_in_batch():
    c = Q.decision_consistency([], [{"target": {"id": "ae-A->B::prop-1"},
                                     "suggested_decision": "ACCEPT"}])
    assert c["unknown"] == 1


def test_mirror_handling_reversed_pair():
    mh = Q.mirror_handling([{"target": {"id": "ae-A->B::prop-1"}},
                            {"target": {"id": "ae-B->A::prop-1"}},
                            {"target": {"id": "bad-id"}}])
    assert mh["with_direction"] == 2
    assert mh["reversed_pairs_found"] == 1


def test_real_artifacts_analyze():
    if not os.path.exists(Q.DECISION_LOG) or not os.path.exists(Q.PROPOSALS):
        return
    res = Q.analyze()
    # 634 A3：全局计数，读单一基线
    assert res["batch"]["count"] == SB.soft("authority_batch_count", res["batch"]["count"])
    assert res["item"]["count"] == 30
    assert res["mirror"]["with_direction"] == 30
    assert res["consistency"]["norm_rate"] == 1.0


def test_report_renders():
    res = Q.analyze()
    md = Q.render_report(res)
    assert "人审质量评估" in md
    assert "语义族比较" in md


def test_selftest_passes():
    assert Q.selftest() == 0
