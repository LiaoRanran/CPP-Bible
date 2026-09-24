"""634 B3 · na_rate_634 单测（纯标准库，≥5 例）。编号 B3-1..B3-6。"""
from __future__ import annotations

import na_rate_634 as N


# B3-1：judged 分类
def test_classify_judged():
    assert N.classify_row({"verdict": "blocked"}) == "judged"
    assert N.classify_row({"verdict": "escaped"}) == "judged"


# B3-2：载体型（无法施加）
def test_classify_carrier():
    assert N.classify_row({"verdict": "infra_error", "reason": "无法施加 op=M7 field=id"}) == "unjudgeable(载体)"


# B3-3：timeout
def test_classify_timeout():
    assert N.classify_row({"verdict": "n_a", "reason": "timeout 超时"}) == "timeout"


# B3-4：样本行数 130
def test_rows_total():
    assert N.breakdown()["rows_total"] == 130


# B3-5：v7 聚合 n_a = 179
def test_v7_na():
    assert N.breakdown()["v7"]["n_a"] == 179


# B3-6：--check 自检通过
def test_selftest():
    assert N.selftest() == 0
