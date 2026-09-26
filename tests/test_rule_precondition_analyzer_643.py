"""643 C1 · rule_precondition_analyzer_643 单测（AST 解析/信号/盲点/规模/只读）。
编号 C1-1..C1-8。
"""
from __future__ import annotations

import rule_precondition_analyzer_643 as C1

SRC = ('register(Rule("R-A", "t", "fact", "programmatic", "block", "atom", '
       'check=check_a))\n'
       'rows = [("R-B", "t2", "atom", check_b)]\n'
       'def check_a():\n'
       '    if card.get("status") and re.match("x", s):\n'
       '        return []\n'
       '    for c in _cards(ATOMS, "*.md"):\n'
       '        if len(c) > 60:\n'
       '            return []\n'
       'def check_b():\n'
       '    return []\n')


# C1-1：两种注册形态都能映射到 check 函数
def test_registration_forms_mapped():
    cm = C1.rule_check_map(SRC)
    assert cm["R-A"] == "check_a"
    assert cm["R-B"] == "check_b"


# C1-2：函数体信号（字段 / 正则 / 数值 / 循环）
def test_signals_fields_regex_numeric_loops():
    fn = C1.function_index(SRC)["check_a"]
    sg = C1.signals(fn)
    assert "status" in sg["fields"]
    assert sg["regex_calls"] >= 1
    assert 60.0 in sg["numeric_consts"]
    assert sg["loops"] >= 1


# C1-3：空输入不炸（未映射规则的兜底）
def test_signals_none_is_empty():
    sg = C1.signals(None)
    assert sg["fields"] == [] and sg["regex_calls"] == 0 and sg["loops"] == 0


# C1-4：盲点判据齐备（四类）
def test_blind_spots_kinds():
    sg = {"fields": ["status"], "regex_calls": 1, "numeric_consts": [60.0], "loops": 1,
          "iterdir_calls": 0, "lines": 10}
    kinds = {b["kind"] for b in C1.blind_spots(sg, "atom")}
    assert {"field_missing_silent", "regex_fragile", "numeric_threshold",
            "cross_card_dependency"} <= kinds


# C1-5：repo scope 追加 path_scope_only；atom 不追加
def test_scope_dependent_blind_spot():
    sg = {"fields": [], "regex_calls": 0, "numeric_consts": [], "loops": 0,
          "iterdir_calls": 0, "lines": 1}
    assert any(b["kind"] == "path_scope_only" for b in C1.blind_spots(sg, "repo"))
    assert not any(b["kind"] == "path_scope_only" for b in C1.blind_spots(sg, "atom"))


# C1-6：真实规模与映射率
def test_real_scale():
    a = C1.analyze()
    assert a["n_rules"] == 67
    assert a["n_mapped"] >= 34, a["n_mapped"]
    assert a["n_mapped"] + a["n_unmapped"] == 67


# C1-7：盲点统计自洽 + 每条盲点都有 why
def test_blind_spot_stats_consistent():
    a = C1.analyze()
    assert sum(a["blind_by_kind"].values()) == sum(len(r["blind_spots"]) for r in a["rows"])
    assert all(b["why"] for r in a["rows"] for b in r["blind_spots"])


# C1-8：字段直方图非空 + 只读自检
def test_histogram_and_selftest():
    a = C1.analyze()
    assert len(a["fields_histogram"]) > 0
    assert all(isinstance(v, int) and v > 0 for v in a["fields_histogram"].values())
    assert C1.selftest() == 0
