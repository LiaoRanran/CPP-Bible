"""635 1.5 · defeater_ledger_635 单测（纯标准库，≥5 例）。编号 1.5-1..1.5-6。"""
from __future__ import annotations

import defeater_ledger_635 as D


# 1.5-1：verified 卡 ≥1
def test_verified_cards():
    assert len(D.verified_cards()) >= 1


# 1.5-2：覆盖率 100%
def test_coverage():
    assert len(D.ledger()) == len(D.verified_cards())
    assert D.stats()["coverage_pct"] == 100.0


# 1.5-3：击败器条目结构
def test_entry_shape():
    r = D.ledger()[0]
    assert set(r) >= {"card", "type", "content", "taint_propagation"}
    assert r["type"] in ("rebutting", "undercutting")


# 1.5-4：taint 判定逻辑
def test_taint_logic():
    c = {"id": "X", "rel": "r", "text": ""}
    assert D.defeater_for(c, 3)["taint_propagation"] is True
    assert D.defeater_for(c, 2)["taint_propagation"] is False


# 1.5-5：first_prop 提取
def test_first_prop():
    assert D.first_prop("- id: prop-1\n    statement: 这是一条命题\n") == "这是一条命题"


# 1.5-6：--check 自检通过
def test_selftest():
    assert D.selftest() == 0
