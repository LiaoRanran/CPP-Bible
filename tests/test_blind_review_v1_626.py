"""626 C1 · Blind Review v1 回归测试（≥10 例）。"""
import os
import sys
import tempfile

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import blind_review_v1_626 as B  # noqa: E402

EXAMPLE = os.path.join(ROOT, "data", "blind_review_example_626.jsonl")


def _done_session():
    m = B.BlindReviewManager()
    s = m.start_session("RI-edge-ae-x", ["ev"])
    m.submit_pass_a(s.blind_review_id, "APPROVE", "ok")
    m.reveal_ai_recommendation(s.blind_review_id, "APPROVE", "ai")
    m.submit_pass_b(s.blind_review_id, "APPROVE", changed=False)
    return m, s


def test_selftest_passes():
    assert B.selftest() == 0


def test_start_session_and_pass_a():
    m = B.BlindReviewManager()
    s = m.start_session("RI-edge-ae-1", ["ev1"])
    assert s.status == "pass_a_pending"
    m.submit_pass_a(s.blind_review_id, "APPROVE", "证据充分")
    assert s.status == "pass_a_done"
    assert s.pass_a.ai_recommendation_shown is False


def test_pass_a_forbids_ai_recommendation():
    """判据核心：Pass A 禁止展示 AI 推荐。"""
    m = B.BlindReviewManager()
    s = m.start_session("RI-edge-ae-2", ["ev"])
    with pytest.raises(ValueError, match="Pass A 禁止展示 AI 推荐"):
        m.submit_pass_a(s.blind_review_id, "APPROVE", "r",
                        ai_recommendation_shown=True)


def test_reveal_and_pass_b():
    m, s = _done_session()
    assert s.status == "pass_b_done"
    assert s.pass_b.consistency == "agree"
    assert s.pass_b.automation_bias_risk == "low"


def test_changed_after_reveal():
    m = B.BlindReviewManager()
    s = m.start_session("RI-edge-ae-3", ["ev"])
    m.submit_pass_a(s.blind_review_id, "REJECT", "不足")
    m.reveal_ai_recommendation(s.blind_review_id, "APPROVE", "ai")
    m.submit_pass_b(s.blind_review_id, "APPROVE", changed=True, change_reason="被说服")
    assert s.pass_b.changed_after_reveal is True
    assert s.pass_b.consistency == "changed"
    assert s.pass_b.automation_bias_risk == "high"


def test_consistency_stats():
    m, _s = _done_session()
    st = m.get_consistency_stats()
    assert st["agree"] == 1
    assert sum(st.values()) == 1


def test_view_digest_stable_and_distinct():
    m1 = B.BlindReviewManager()
    s1 = m1.start_session("RI-edge-ae-4", ["evA", "evB"])
    m1.submit_pass_a(s1.blind_review_id, "APPROVE", "r")
    m2 = B.BlindReviewManager()
    s2 = m2.start_session("RI-edge-ae-5", ["evC"])
    m2.submit_pass_a(s2.blind_review_id, "APPROVE", "r")
    assert s1.pass_a.view_digest != s2.pass_a.view_digest
    assert len(s1.pass_a.view_digest) == 64


def test_export_import_roundtrip():
    m, _s = _done_session()
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "b.jsonl")
        m.export_jsonl(p)
        m2 = B.BlindReviewManager.import_jsonl(p)
    assert len(m2.get_all_sessions()) == 1
    assert m2.get_all_sessions()[0].pass_a.decision == "APPROVE"


def test_authority_integration_interface():
    m, s = _done_session()
    kw = m.to_authority_event_kwargs(s.blind_review_id)
    assert kw["review_method"] == "ITEM_BLIND"
    assert kw["decision_origin"] == "human_observed"
    assert kw["blind_review_id"] == s.blind_review_id


def test_example_data_generated_and_marked():
    assert os.path.exists(EXAMPLE)
    m = B.BlindReviewManager.import_jsonl(EXAMPLE)
    assert len(m.get_all_sessions()) >= 3
    # 示例为模拟数据，不得混入真实人审统计
    assert all(s.pass_a.ai_recommendation_shown is False
               for s in m.get_all_sessions() if s.pass_a)


def test_illegal_decision_rejected():
    m = B.BlindReviewManager()
    s = m.start_session("RI-edge-ae-6", ["ev"])
    with pytest.raises(ValueError):
        m.submit_pass_a(s.blind_review_id, "BOGUS", "r")
