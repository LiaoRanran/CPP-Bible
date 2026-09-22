"""626 A3 · Authority Schema v2 回归测试（≥5 例）。"""
import sys

ROOT = __import__("os").path.dirname(__import__("os").path.dirname(
    __import__("os").path.abspath(__file__)))
sys.path.insert(0, ROOT + "/tools")
import authority_schema_v2_626 as A  # noqa: E402


def test_five_review_methods():
    assert len(A.REVIEW_METHODS) == 5
    for m in ("BATCH_AUTH", "MIRROR_DERIVED", "ITEM_OPEN", "ITEM_BLIND",
              "ITEM_SECOND_REVIEW"):
        assert A.is_valid_review_method(m)


def test_four_decision_origins():
    assert len(A.DECISION_ORIGINS) == 4
    for o in ("human_observed", "user_authorized_execution",
              "machine_projection", "mirror_projection"):
        assert A.is_valid_decision_origin(o)


def test_622_thirty_items_not_independent():
    """判据 1：622 的 30 条 user_authorized_execution 不得计为独立人审。"""
    assert not A.is_independent_human_review("ITEM_OPEN", "user_authorized_execution")
    assert not A.is_independent_human_review("BATCH_AUTH", "human_observed")


def test_only_blind_or_second_review_counts():
    assert A.is_independent_human_review("ITEM_BLIND", "human_observed")
    assert A.is_independent_human_review("ITEM_SECOND_REVIEW", "human_observed")
    assert not A.is_independent_human_review("ITEM_BLIND", "machine_projection")


def test_legacy_mapping():
    assert A.normalize_legacy_method("batch_authorization") == "BATCH_AUTH"
    assert A.normalize_legacy_method("item_by_item_executed") == "ITEM_OPEN"
    assert A.normalize_legacy_power("OVERRIDE") == "REPLACE"
    assert A.normalize_legacy_power("ACCEPT") == "CREATE"


def test_validate_event():
    assert A.validate_event("ITEM_BLIND", "human_observed", "CREATE", "APPROVE") == []
    assert A.validate_event("BOGUS", "human_observed", "CREATE", "APPROVE")
    assert A.validate_event("ITEM_BLIND", "bogus_origin", "CREATE", "APPROVE")


def test_selftest_passes():
    assert A.selftest() == 0
