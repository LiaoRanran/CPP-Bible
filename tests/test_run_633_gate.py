"""633 F1 · run_633_gate 单测（纯标准库，≥5 例）。编号 F1-1..F1-6。"""
from __future__ import annotations

import os

import tools.run_633_gate as m


# F1-1：5 个新工具都存在
def test_new_tools_exist():
    assert len(m.NEW_TOOLS) == 5
    for t in m.NEW_TOOLS:
        assert os.path.exists(os.path.join(m.ROOT, "tools", f"{t}.py")), t


# F1-2：盘点文件清单齐备性检查可用
def test_inventory_check():
    inv = m.check_inventory()
    assert set(inv) >= {"ok", "missing", "n"}
    assert inv["n"] >= 8


# F1-3：快照比较结构
def test_compare_snapshots():
    c = m.compare_snapshots({"dirty_files": 10, "todo_count": 1},
                            {"dirty_files": 7, "todo_count": 2})
    assert "rows" in c
    d = {r["metric"]: r["delta"] for r in c["rows"]}
    assert d["dirty_files"] == -3 and d["todo_count"] == 1


# F1-4：化债前快照可读
def test_pre_snapshot():
    s = m.pre_snapshot()
    assert isinstance(s, dict)
    assert "dirty_files" in s


# F1-5：current snapshot 含 7 指标
def test_snapshot_now():
    s = m.snapshot_now()
    assert set(s) >= {"dirty_files", "tools_total", "tools_no_check", "todo_count",
                      "key_files", "dead_links", "pending_push"}


# F1-6：--check 自检通过
def test_selftest_passes():
    assert m.selftest() == 0
