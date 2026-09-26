"""643 B4 · escape_hotspot_scanner_643 单测（归因/两口径/N-A 拆分/只读）。
编号 B4-1..B4-8。
"""
from __future__ import annotations

import escape_hotspot_scanner_643 as B4


# B4-1：四类归因各自触发
def test_attributions():
    assert B4.attribute({"new_block": [], "new_warn": []})[0] == "规则缺失"
    assert B4.attribute({"new_block": [], "new_warn": ["W"]})[0] == "规则太弱"
    assert B4.attribute({"equivalent": True})[0] == "验证器能力天花板"
    assert B4.attribute({"new_block": ["B"], "new_warn": []})[0] == "规则冲突"


# B4-2：归因互斥（每条只落一类）
def test_attribution_mutually_exclusive():
    rows = [{"new_block": [], "new_warn": []}, {"new_block": [], "new_warn": ["W"]},
            {"equivalent": True}, {"new_block": ["B"]}]
    got = [B4.attribute(r)[0] for r in rows]
    assert len(set(got)) == 4, str(got)


# B4-3：能力天花板优先于规则缺失（equivalent 先判）
def test_capability_takes_precedence():
    assert B4.attribute({"equivalent": True, "new_block": [], "new_warn": []})[0] \
        == "验证器能力天花板"


# B4-4：两口径并列（counted 1 vs raw 9），不合并
def test_two_calibers_reported():
    e = B4.assess()["escaped"]
    assert e["counted_escaped"] == 1 and e["raw_escaped"] == 9
    assert e["equivalent_invalid"] == e["raw_escaped"] - e["counted_escaped"]


# B4-5：已知逃逸案例必归入（合计 = 原始条数）
def test_all_escapes_attributed():
    e = B4.assess()["escaped"]
    assert sum(e["by_attribution"].values()) == e["raw_escaped"] == 9


# B4-6：算子 7 个且带 CP 区间
def test_operators():
    rows = B4.assess()["operators"]["rows"]
    assert len(rows) == 7
    assert all("cp_low" in r and "cp_high" in r for r in rows)


# B4-7：N/A 拆分自洽 + 必须标 inferred（v7 无原因字段）
def test_na_split_and_inferred_flag():
    na = B4.assess()["na"]
    assert na["semantic_na"] + na["capability_na_hint"] == na["total_n_a"] == 179
    assert na["inferred"] is True and na["reason_available"] is False


# B4-8：卡片域分组 + 只读自检
def test_card_groups_and_selftest():
    rows = B4.assess()["card_groups"]["rows"]
    assert len(rows) > 0
    assert all("escape_rate" in r and "na_rate" in r for r in rows)
    assert B4.selftest() == 0
