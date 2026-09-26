"""643 B3 · autoimmune_hotspot_scanner_643 单测（分类/阈值边界/数据缺口/只读）。
编号 B3-1..B3-8。
"""
from __future__ import annotations

import autoimmune_hotspot_scanner_643 as B3


# B3-1：四类建议各自的触发
def test_four_verdicts():
    assert B3.classify("warn", 0, 0, 1.0, 6)[0] == "退役候选"
    assert B3.classify("warn", 1, 1, 0.50, 6)[0] == "不适用候选"
    assert B3.classify("advice", 12, 3, 0.10, 6)[0] == "收紧候选"
    assert B3.classify("block", 0, 5, 0.10, 6)[0] == "放宽候选"
    assert B3.classify("block", 2, 3, 0.10, 6)[0] == "观察"


# B3-2：阈值边界（恰好等于阈值即触发）
def test_threshold_edges():
    assert B3.classify("warn", 1, 1, B3.EXEMPT_THRESHOLD, 6)[0] == "不适用候选"
    assert B3.classify("advice", B3.LIVE_HOT, 1, 0.10, 6)[0] == "收紧候选"
    assert B3.classify("block", 0, B3.ACTIVE_ROUNDS, 0.10, 6)[0] == "放宽候选"


# B3-3：差一格就不触发（阈值不是摆设）
def test_below_threshold_not_triggered():
    assert B3.classify("advice", B3.LIVE_HOT - 1, 1, 0.10, 6)[0] == "观察"
    assert B3.classify("block", 0, B3.ACTIVE_ROUNDS - 1, 0.10, 6)[0] == "观察"
    assert B3.classify("warn", 1, 1, B3.EXEMPT_THRESHOLD - 0.01, 6)[0] == "观察"


# B3-4：判据顺序（退役优先于不适用；豁免率优先于收紧）
def test_priority_order():
    # 退役：touched=0 **且** live_hits=0（即使豁免率也越阈，仍先判退役）
    assert B3.classify("advice", 0, 0, 0.90, 6)[0] == "退役候选"
    # 有命中就不是退役 ⇒ 落到不适用（豁免率越阈），而不是收紧（命中越阈）
    assert B3.classify("advice", 20, 1, 0.90, 6)[0] == "不适用候选"


# B3-5：豁免率为 None 时不误判"不适用"
def test_exempt_none_not_inapplicable():
    assert B3.classify("warn", 3, 3, None, 6)[0] == "观察"


# B3-6：67 规则在册 + 分布自洽
def test_assess_shape():
    a = B3.assess()
    assert a["n_rules"] == 67
    assert sum(a["by_verdict"].values()) == 67


# B3-7：数据缺口登记（inbox 要的 warn/block 率无法算，必须显式登记而非编造）
def test_data_gap_registered():
    a = B3.assess()
    assert len(a["unavailable"]) >= 3
    assert any("warn 率" in u for u in a["unavailable"])
    assert a["proxied_rules"] == 67, "known_error_rate 全为代理 ⇒ 不据它下判"


# B3-8：只读自检
def test_selftest():
    assert B3.selftest() == 0
