#!/usr/bin/env python3
"""616 A1 回归测试：confidence_sequence（置信序列/e-process，修复统计偷看）。"""
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import confidence_sequence as cs  # noqa: E402


def test_init_defaults() -> None:
    c = cs.ConfidenceSequence()
    assert c.alpha == 0.05 and c.a == 1.0 and c.b == 1.0
    assert c.n == 0 and c.x == 0


def test_update_accumulates() -> None:
    c = cs.ConfidenceSequence()
    c.update(10, 0)
    c.update(5, 1)
    assert c.n == 16 and c.x == 1
    assert c.point_estimate() == 1 / 16


def test_ci_ordering() -> None:
    c = cs.ConfidenceSequence()
    c.update(100, 3)
    lo, hi = c.get_ci()
    assert 0.0 <= lo <= c.point_estimate() <= hi <= 1.0
    assert c.get_lower_bound() == lo and c.get_upper_bound() == hi


def test_upper_bound_matches_reference() -> None:
    # n=1406, x=1：CS ≈ 0.9062%，CP 单侧 ≈ 0.3370%（_arch_v20 p02 历史参考）
    up = cs.cs_upper(1406, 1)
    cp = cs.cp_upper(1406, 1)
    assert abs(up - 0.009062) < 5e-5
    assert abs(cp - 0.003370) < 5e-5
    assert up > cp                                   # anytime 更保守
    # 上界定义自洽：E_n(上界) ≈ 1/alpha
    assert abs(cs.log_eprocess(up, 1, 1406) - math.log(1 / 0.05)) < 1e-3


def test_check_consistency() -> None:
    assert cs.check() == []
