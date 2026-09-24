"""632 H1 · run_632_gate 单测（纯标准库，≥5 例）。

聚焦门禁的构件：工具清单 / 产物清单 / check_tool / gather_deliverables。
不在此调用 run_gate()/main()（否则会触发全量 pytest）；全量门禁由手动 `--check` 验证。
编号 H1-1..H1-6。
"""
from __future__ import annotations

import os

import tools.run_632_gate as m

ROOT = m.ROOT


# H1-1：工具清单里的文件都存在
def test_tools_manifest_exist():
    assert len(m.TOOLS) > 0
    for n in m.TOOLS:
        assert os.path.exists(m._tool_path(n)), n


# H1-2：产物清单里的文件都存在
def test_deliverables_manifest_exist():
    assert len(m.DELIVERABLES) > 0
    for rel in m.DELIVERABLES:
        assert os.path.exists(os.path.join(ROOT, rel)), rel


# H1-3：check_tool 对真实工具返回规范结构且通过
def test_check_tool_real():
    r = m.check_tool("baseline_632")
    assert set(r) >= {"name", "ok", "exit", "detail"}
    assert r["ok"] is True
    assert r["exit"] == 0


# H1-4：check_tool 对不存在的工具有序失败（不抛异常）
def test_check_tool_missing():
    r = m.check_tool("__no_such_632_tool__")
    assert r["ok"] is False
    assert r["detail"] == "工具文件不存在"


# H1-5：gather_deliverables 返回结构且当前无缺失
def test_gather_deliverables():
    d = m.gather_deliverables()
    assert "rows" in d and "missing" in d
    assert d["missing"] == [], d["missing"]


# H1-6：清单覆盖全部子任务工具（B1..G1 + task0）
def test_manifest_covers_subtasks():
    names = set(m.TOOLS)
    expected = [
        "transparency_anchor_632", "transparency_verify_632",
        "autoimmune_human_fill_helper_632", "autoimmune_human_fill_apply_632",
        "pollution_guard_session_632", "sandbox_apply_622",
        "coverage_probe_l2_3_632", "coverage_probe_l4_2_632", "coverage_probe_l4_4_632",
        "queyi_core_interface_v03_632", "baseline_632", "ci_pytest_final_clear_632",
    ]
    for n in expected:
        assert n in names, n
