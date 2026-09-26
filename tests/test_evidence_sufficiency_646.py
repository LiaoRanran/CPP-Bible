"""646 阶段 B3 · 充分性重判单测（fast）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import evidence_sufficiency_646 as b3  # noqa: E402


def test_selftest_passes():
    """--check 只读自检。"""
    assert b3.selftest() == 0


def test_real_27_cards_all_sufficient():
    """真实 27 卡全部充分，幻影卡被排除。"""
    res = b3.judge()
    assert res["cards_total"] == 27
    assert res["sufficient"] == 27
    assert res["insufficient"] == 0
    assert res["phantom_excluded"] == "ATOM-MEM-MOVE-001"
    assert "ATOM-MEM-MOVE-001" not in res["per_card"]
