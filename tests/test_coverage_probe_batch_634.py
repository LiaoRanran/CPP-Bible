"""634 B1 · coverage 批探针单测（纯标准库，≥5 例 + 14 参数化）。编号 B1-1..B1-5。"""
from __future__ import annotations

import os
import subprocess
import sys

import coverage_probe_batch_634 as B
import pytest

ROOT = B.ROOT


# B1-1：14 个新向量
def test_14_new_vectors():
    assert len(B.NEW_VECTORS) == 14
    assert all(k.startswith("L") for k in B.NEW_VECTORS)


# B1-2：probe 结构
def test_probe_structure():
    r = B.probe("L1.1")
    assert set(r) >= {"id", "name", "risk", "mechanism_present"}
    assert r["id"] == "L1.1"


# B1-3：矩阵覆盖 ≥85%
def test_matrix_coverage():
    mx = B.matrix()
    assert mx["total"] == 35
    assert mx["coverage_pct"] >= 85.0


# B1-4：至少一个机制存在
def test_some_mechanism_present():
    assert any(r["mechanism_present"] for r in B.probe_all())


# B1-5：--check 自检通过
def test_selftest():
    assert B.selftest() == 0


# B1-6..：14 个薄包装各自 --check exit 0（参数化）
_WRAPPERS = [f"coverage_probe_{v.replace('.', '_')}_634.py" for v in B.NEW_VECTORS]


@pytest.mark.parametrize("wrapper", _WRAPPERS)
def test_wrapper_check_exit0(wrapper):
    r = subprocess.run([sys.executable, os.path.join(ROOT, "tools", wrapper), "--check"],
                       cwd=ROOT, capture_output=True, text=True, timeout=60)
    assert r.returncode == 0, f"{wrapper}: {r.stderr[-200:]}"
