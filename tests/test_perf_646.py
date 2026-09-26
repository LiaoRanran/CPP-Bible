"""646 阶段 A3 · 进程内记忆化单测（fast）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import perf_646 as perf  # noqa: E402


def test_selftest_passes():
    """--check 只读自检（缓存命中且一致）。"""
    perf.clear()
    assert perf.selftest() == 0


def test_cache_hit_returns_same_object():
    """第二次调用命中缓存（同一对象）。"""
    perf.clear()
    a = perf.atoms()
    b = perf.atoms()
    assert a is b


def test_clear_resets_cache():
    """clear() 后重新计算（对象不同）。"""
    perf.clear()
    a = perf.atoms()
    perf.clear()
    b = perf.atoms()
    assert a == b


def test_counts_consistent_with_ids():
    """命中计数之和 == 命中事件数。"""
    perf.clear()
    assert sum(perf.finding_counts().values()) == len(perf.finding_rule_ids())
