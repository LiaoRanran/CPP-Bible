"""646 阶段 A1 · 规则→卡映射单测（fast）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import rule_card_mapper_646 as a1  # noqa: E402


def test_selftest_passes():
    """--check 只读自检（已知关联必命中）。"""
    assert a1.selftest() == 0


def test_rule_tokens_drop_generic():
    """通用词/数字被剔除。"""
    t = a1._rule_tokens("ATOM-CLAIM-CONCEPT-NORMALIZED")
    assert "atom" not in t and "claim" in t and "normalized" in t


def test_gray_zone_maps_only_ub_card():
    """已知关联：GRAY 规则 → 唯一 UB 卡 high。"""
    m = a1.build_mapping()
    gray = m["rules"]["ATOM-GRAY-ZONE"]["cards"]
    assert len(gray) == 1
    assert gray[0]["card"] == "ATOM-UB-GRAY-001" and gray[0]["strength"] == "high"


def test_every_rule_has_mapping():
    """无孤儿规则：67 规则全部有映射。"""
    m = a1.build_mapping()
    assert m["rules_with_mapping"] == m["rule_count"] == 67
    assert all(info["cards"] for info in m["rules"].values())


def test_card_count_is_27():
    """卡片域 = 真实 27 卡（不是 28，见 646 §三.1）。"""
    m = a1.build_mapping()
    assert m["card_count"] == 27
