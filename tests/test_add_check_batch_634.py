"""634 A2 · 79 个老工具 --check 批补 单测（纯标准库，≥5 例）。编号 A2-1..A2-4。

对冻结清单 `data/add_check_targets_634.json` 逐工具参数化验证 `--check` exit 0。
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
_TARGETS_FILE = os.path.join(ROOT, "data", "add_check_targets_634.json")
with open(_TARGETS_FILE, encoding="utf-8") as _fh:
    TARGETS = json.load(_fh)["targets"]


# A2-1：清单非空（冻结 79 个）
def test_targets_frozen():
    assert len(TARGETS) >= 70
    assert all(t.endswith(".py") for t in TARGETS)


# A2-2：每个目标都含 --check 守卫
def test_all_have_check_guard():
    missing = [t for t in TARGETS
               if '"--check"' not in open(os.path.join(ROOT, "tools", t), encoding="utf-8",
                                          errors="replace").read()]
    assert not missing, missing


# A2-3：每个目标 --check exit 0（参数化，逐工具）
@pytest.mark.parametrize("tool", TARGETS)
def test_check_exit0(tool):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", tool), "--check"],
                       cwd=ROOT, capture_output=True, text=True, timeout=120)
    assert r.returncode == 0, f"{tool}: {r.stderr[-200:]}"


# A2-4：--check 不写盘（抽查 5 个，跑前后 data/ 文件集合不变）
def test_check_does_not_write():
    import glob
    before = set(glob.glob(os.path.join(ROOT, "data", "**", "*"), recursive=True))
    for tool in TARGETS[:5]:
        subprocess.run([sys.executable, os.path.join(ROOT, "tools", tool), "--check"],
                       cwd=ROOT, capture_output=True, text=True, timeout=120)
    after = set(glob.glob(os.path.join(ROOT, "data", "**", "*"), recursive=True))
    assert before == after
