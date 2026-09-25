"""636 2.3 · blind_protocol_636 单测（纯标准库，≥5 例）。编号 2.3-1..2.3-6。"""
from __future__ import annotations

import blind_protocol_636 as B


# 2.3-1：五步流程
def test_steps():
    assert len(B.STEPS) == 5


# 2.3-2：注入改变值
def test_inject():
    m = B.inject(10.0)
    assert m["masked"] != m["value"]
    assert m["sign"] in (-1, 1)
    assert m["offset"] > 0


# 2.3-3：揭盲还原
def test_reveal():
    for v in (0.0, 5.0, -3.0, 35.8):
        assert B.reveal(B.inject(v)) == v


# 2.3-4：违规统计
def test_violations():
    v = B.violations()
    assert v["decisions"] >= 1
    assert v["violations"] >= 0


# 2.3-5：分歧率如实登记 None
def test_disagreement():
    d = B.disagreement()
    assert d["rate"] is None and "无法计算" in d["note"]


# 2.3-6：--check 自检通过
def test_selftest():
    assert B.selftest() == 0
