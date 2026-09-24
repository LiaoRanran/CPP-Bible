"""634 E1 · run_634_gate 单测（纯标准库，≥5 例）。编号 E1-1..E1-6。"""
from __future__ import annotations

import os

import run_634_gate as G


# E1-1：新工具清单存在
def test_new_tools_exist():
    assert len(G.NEW_TOOLS) >= 6
    for t in G.NEW_TOOLS:
        assert os.path.exists(os.path.join(G.ROOT, "tools", f"{t}.py")), t


# E1-2：79 工具清单文件存在
def test_targets_file():
    assert os.path.exists(G.TARGETS_FILE)


# E1-3：coverage 复算 ≥85
def test_coverage():
    c = G.check_coverage()
    assert c["ok"] and c["pct"] >= 85.0


# E1-4：自身免疫率 = 0
def test_autoimmune_zero():
    a = G.check_autoimmune()
    assert a["ok"] and a["missing"] == 0 and a["cards"] >= 1


# E1-5：受控目录检查可调用
def test_controlled_callable():
    assert isinstance(G.check_controlled(), dict)


# E1-6：--check 自检通过
def test_selftest():
    assert G.selftest() == 0
