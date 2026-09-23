"""627 E1 · 收工门禁 单测（≥4 例）。"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import run_627_gate as G


def test_new_tools_complete():
    assert len(G.NEW_TOOLS) == 11
    assert "pre_push_checklist_627" in G.NEW_TOOLS
    assert all(t.endswith("_627") for t in G.NEW_TOOLS)


def test_no_git_push_in_gate():
    src = open(G.__file__, encoding="utf-8").read()
    cmds = re.findall(r'\["git",\s*"([^"]+)"', src)
    assert "push" not in cmds


def test_core_tools_protected():
    assert "gate_engine.py" in G.CORE_TOOLS
    assert len(G.CORE_TOOLS) == 5


def test_batch_base_is_626_f1():
    assert G.BATCH_BASE == "4f2c976c"


def test_controlled_dirs_listed():
    assert G.CONTROLLED == ["atoms", "evidence", "Examples", "Book"]
