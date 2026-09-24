"""633 任务0 · debt_inventory 单测（纯标准库，≥5 例）。

编号 T0-1..T0-7。
"""
from __future__ import annotations

import os

import tools.debt_inventory_633 as d


# T0-1：ID 自增唯一
def test_id_increments():
    d._reset_ids()
    a = d.item("X", "CI", "P1", "d", "l", "r", "a", "S")
    b = d.item("X", "CI", "P1", "d", "l", "r", "a", "S")
    assert a["id"] == "CI-001" and b["id"] == "CI-002"


# T0-2：严重度字段合法
def test_severity_values():
    d._reset_ids()
    it = d.item("X", "TOOL", "P3", "d", "l", "r", "a", "L")
    assert it["severity"] in ("P0", "P1", "P2", "P3")


# T0-3：CLI 判定（有主入口/argparse 才算工具债候选）
def test_is_cli():
    assert d._is_cli('if __name__ == "__main__":\n    pass\n') is True
    assert d._is_cli("import argparse\nargparse.ArgumentParser()\n") is True
    assert d._is_cli("def helper():\n    return 1\n") is False


# T0-4：本地缺失 import 检测
def test_missing_local_imports(tmp_path):
    p = tmp_path / "t.py"
    p.write_text("import tools.__no_such_mod_633__\nimport os\n", encoding="utf-8")
    miss = d._missing_local_imports(str(p))
    assert "tools.__no_such_mod_633__" in miss
    assert "os" not in miss


# T0-5：快照含全部指标且工具数为正
def test_snapshot():
    s = d.snapshot()
    assert set(s) >= {"dirty_files", "tools_total", "tools_no_check", "todo_count",
                      "key_files", "dead_links", "pending_push"}
    assert s["tools_total"] > 0


# T0-6：7 维度齐全且分级不越界
def test_scan_all_dimensions():
    data = d.scan_all()
    assert set(data["sections"]) == {"CI/测试债", "工具债", "数据债", "安全债",
                                     "文档债", "git债", "协议债"}
    for v in data["sections"].values():
        for it in v:
            assert it["severity"] in ("P0", "P1", "P2", "P3")


# T0-7：--check 自检通过（只读，exit 0）
def test_selftest_passes():
    assert d.selftest() == 0
    assert os.path.isabs(d.OUT_MD)
