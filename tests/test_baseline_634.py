"""634 任务0 · baseline_634 单测（纯标准库，≥5 例）。编号 T0-1..T0-6。"""
from __future__ import annotations

import tools.baseline_634 as B


# T0-1：Standing Baseline 8 维
def test_standing_8_dims():
    assert len(B.STANDING) == 8
    assert "coverage" in B.STANDING and "pytest_side_effect" in B.STANDING


# T0-2：git_status 可读
def test_git_status():
    assert isinstance(B.git_status(), list)


# T0-3：计数为正
def test_counts():
    c = B.counts()
    assert c["tools_py"] > 0 and c["tests_py"] > 0 and c["commits"] > 0


# T0-4：无 --check 工具数为整数
def test_no_check_tools():
    assert isinstance(B.no_check_tools(), int)


# T0-5：副作用扫描结构 + 命中
def test_audit_sites():
    a = B.audit_write_sites()
    assert set(a) == {"write_call", "prod_path_write"}
    assert len(a["write_call"]) >= 1


# T0-6：--check 自检通过
def test_selftest():
    assert B.selftest() == 0
