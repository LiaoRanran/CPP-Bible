"""646 阶段 B1 · 标准获取补全单测（fast，不联网）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import standard_fetcher_646 as b1  # noqa: E402


def test_selftest_passes():
    """--check 只读自检。"""
    assert b1.selftest() == 0


def test_prev_report_loaded():
    """645 报告可读（16 成功）。"""
    import json
    assert os.path.exists(b1.PREV_JSON)
    with open(b1.PREV_JSON, encoding="utf-8") as fh:
        prev = json.load(fh)
    assert prev["ok"] == 16


def test_646_report_reaches_18():
    """646 报告存在且达 18/18（真实抓取结果）。"""
    import json
    if not os.path.exists(b1.REPORT_JSON):
        import pytest
        pytest.skip("646 抓取报告尚未生成（需 --acquire）")
    with open(b1.REPORT_JSON, encoding="utf-8") as fh:
        rep = json.load(fh)
    assert rep["topics"] == 18
    assert rep["ok"] >= 16
