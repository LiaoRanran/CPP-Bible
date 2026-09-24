"""633 B2 · tool_debt_audit 单测（纯标准库，≥5 例）。编号 B2-1..B2-6。"""
from __future__ import annotations

import os

import tools.debt_inventory_633 as di
import tools.tool_debt_audit_633 as m


# B2-1：严格 TODO 口径排除占位符 XXX
def test_todo_regex_excludes_placeholder():
    assert m._REAL_TODO_RE.search("MIS-XXX 用法") is None
    assert m._REAL_TODO_RE.search("TODO: 待修") is not None
    # 命中的真 TODO 行不含占位提示词
    for _f, _i, tx in m.real_todo_hits():
        assert not any(h in tx for h in m._PLACEHOLDER_HINT)


# B2-2：占位符 XXX 计数 > 0（解释任务0 的 35 误报）
def test_placeholder_xxx_positive():
    assert m.placeholder_xxx_count() > 0


# B2-3：分类含 5 键且无 import 真债
def test_categorize():
    c = m.categorize()
    assert set(c) == {"no_check_cli", "broken_import", "todo", "big_file", "naming"}
    assert len(c["broken_import"]) == 0


# B2-4：补 --check 范式含关键要素
def test_check_gap_pattern():
    p = m.check_gap_pattern()
    assert "--check" in p and "只读" in p


# B2-5：本批实加 --check 的 3 个工具确实有了 --check
def test_added_check_tools_have_check():
    assert len(m.ADDED_CHECK) >= 3
    for f in m.ADDED_CHECK:
        src = di._read(os.path.join(di.ROOT, f))
        assert "--check" in src, f


# B2-6：--check 自检通过
def test_selftest_passes():
    assert m.selftest() == 0
