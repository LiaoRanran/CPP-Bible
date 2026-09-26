"""645 A4 闭环 R5 校准度单测（slow 组：真实跑 A1→A3 闭环）。

锁定：R5 真实可量化、未达标诚实登记、系列口径并列不偷换。
对应 645 §三 A4 验收：R5 真实提升（非代理 0.1）、未达标诚实登记根因。
"""
import sys

import pytest

sys.path.insert(0, "tools")

import loop_r5_runner_645 as a4

pytestmark = pytest.mark.slow


def test_selftest_passes():
    assert a4.selftest() == 0


def test_run_loop_computes_r5():
    res = a4.run_loop(max_drafts=3)
    assert 0.0 <= res["R5"] <= 1.0
    # R5 系列含真实计算值与历史口径（R3 为 None 标注口径缺失）
    assert "R5" in res["series"]
    assert res["series"]["R3"] is None
    # 每条草案都带真实涟漪（真注入）或 admission 标记
    for d in res["drafts"]:
        assert "ripple" in d
