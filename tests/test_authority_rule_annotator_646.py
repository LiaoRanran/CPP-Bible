"""646 阶段 A5 · 账本规则注释单测（fast）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import authority_rule_annotator_646 as a5  # noqa: E402


def test_selftest_passes():
    """--check 只读自检（解析/反表）。"""
    assert a5.selftest() == 0


def test_atom_extraction():
    """从 edge target_id 正确抽出原子卡 id。"""
    assert a5._atom_of("ae-MIS-LANG-001->ATOM-LANG-INLINE-001::prop-1") == "ATOM-LANG-INLINE-001"
    assert a5._atom_of("no-atom-here") is None


def test_annotate_covers_rules():
    """452 事件全部注释，67 规则全覆盖。"""
    res = a5.annotate()
    assert res["events"] == 452
    assert res["rules_with_events"] == 67


def test_ledger_unchanged():
    """注释不修改原账本（sha256 前后一致）。"""
    before = a5._ledger_sha256()
    res = a5.annotate()
    after = a5._ledger_sha256()
    assert before == after == res["ledger_sha256"]
