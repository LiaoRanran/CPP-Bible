"""635 E1 · run_635_gate 单测（纯标准库，≥5 例）。编号 E1-1..E1-6。"""
from __future__ import annotations

import os

import run_635_gate as G


# E1-1：11 新工具存在
def test_new_tools():
    assert len(G.NEW_TOOLS) == 11
    for t in G.NEW_TOOLS:
        assert os.path.exists(os.path.join(G.ROOT, "tools", f"{t}.py")), t


# E1-2：11 交付文件
def test_deliverables_list():
    assert len(G.DELIVERABLES) == 11


# E1-3：交付齐备
def test_deliverables_exist():
    d = G.check_deliverables()
    assert d["ok"] and not d["missing"]


# E1-4：受控目录干净
def test_controlled():
    assert G.check_controlled()["ok"] is True


# E1-5：报告结构
def test_reports_keys():
    assert set(G.REPORTS) == {"acceptance", "visibility", "next_steps"}


# E1-6：--check 自检通过
def test_selftest():
    assert G.selftest() == 0
