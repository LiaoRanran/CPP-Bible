"""637 B · error_detector_637 单测（纯标准库，≥5 例）。编号 TB-1..TB-6。"""
from __future__ import annotations

import error_detector_637 as E


def _bad():
    return E._bad_obs()


def _good():
    return E._good_obs()


# TB-1：坏样本检出并被截断为 top 5
def test_top5():
    assert len(E.detect(_bad())) == 5


# TB-2：P0 优先排第一
def test_p0_first():
    assert E.detect(_bad())[0]["severity"] == "P0"


# TB-3：好样本零异常
def test_good_empty():
    assert E.detect(_good()) == []


# TB-4：接地率阈值边界（<50 命中，=50 不命中）
def test_grounding_boundary():
    assert len(E.detect({"metrics": {"grounding_pct": 49.9}})) == 1
    assert len(E.detect({"metrics": {"grounding_pct": 50.0}})) == 0


# TB-5：重指标缺失（None）不误报
def test_none_no_false_positive():
    obs = {"metrics": {"ruff_errors": None, "mypy_errors": None, "pytest_failures": None,
                       "grounding_pct": 90.0, "observation_pct": 1.0, "taint_cards": 0,
                       "exception_clauses": 1, "ahead": 1}}
    assert E.detect(obs) == []


# TB-6：--check 自检通过
def test_selftest():
    assert E.selftest() == 0
