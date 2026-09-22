"""624 E2 人审逐条清单生成器 · 单元测试（≥4 例）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import human_review_item_by_item_generator_624 as m  # noqa: E402


def _items():
    return m.generate(m.load_edges(m.ANN), cap=80)


def test_generates_over_70_and_total_over_100():
    items = _items()
    assert len(items) > 70
    assert m.PRIOR_COUNT + len(items) > 100


def test_ambiguity_sorted_high_first():
    items = _items()
    order = {"high": 0, "medium": 1, "low": 2}
    keys = [order[x["ambiguity"]] for x in items]
    assert keys == sorted(keys)
    assert all(x["ambiguity"] in ("high", "medium", "low") for x in items)


def test_recommend_valid_and_summary():
    items = _items()
    assert all(x["recommend"] in ("approve", "modify", "reject") for x in items)
    s = m.summarize(items)
    assert s["total"] == len(items)
    assert s["total_after"] == m.PRIOR_COUNT + len(items)


def test_modify_edges_are_high_ambiguity():
    items = _items()
    for x in items:
        if x["action"] == "modify":
            assert x["ambiguity"] == "high"


def test_report_file_exists():
    p = os.path.join(ROOT, "data", "human_review_item_by_item_624.md")
    assert os.path.exists(p) and os.path.getsize(p) > 500


def test_selftest_passes():
    assert m.selftest() == 0
