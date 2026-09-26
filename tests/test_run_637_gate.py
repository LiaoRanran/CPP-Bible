"""637 H · run_637_gate 单测（纯标准库，≥5 例）。编号 TH-1..TH-5。"""
from __future__ import annotations

import os

import run_637_gate as G


# TH-1：6 个新工具，且文件都在
def test_new_tools():
    assert len(G.NEW_TOOLS) == 6
    assert all(os.path.exists(os.path.join(G.ROOT, "tools", f"{t}.py")) for t in G.NEW_TOOLS)


# TH-2：闭环 5 段
def test_loop_tools():
    assert len(G.LOOP_TOOLS) == 5
    assert G.LOOP_TOOLS[0] == "self_observer_637"
    assert G.LOOP_TOOLS[-1] == "evolution_memo_637"


# TH-3：8 个交付文件
def test_deliverables():
    assert len(G.DELIVERABLES) == 8


# TH-4：受控目录零污染
def test_controlled():
    assert G.check_controlled()["ok"] is True


# TH-5：--check 自检通过
def test_selftest():
    assert G.selftest() == 0
