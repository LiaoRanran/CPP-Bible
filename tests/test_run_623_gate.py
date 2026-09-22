"""623 C1 · 收工门禁（整目录 ruff）单元测试（≥3 例）

覆盖：整目录 ruff 绿 / 只跑本批 ruff 红（存量债漏检陷阱）/ 跳过非 .py 文件。
"""
from __future__ import annotations

import importlib.util
import os
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(ROOT, "tools", "run_623_gate.py")


def _load():
    spec = importlib.util.spec_from_file_location("run_623_gate_623", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _write(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(content)


def test_whole_dir_green_on_clean_tree():
    mod = _load()
    with tempfile.TemporaryDirectory() as td:
        _write(os.path.join(td, "a.py"), "def f():\n    return 1\n")
        targets = mod.collect_py_files([td])
        assert targets and targets[0].endswith("a.py")
        rc, _ = mod.run_ruff(targets)
        assert rc == 0, "干净树整目录 ruff 应全绿"


def test_only_batch_misses_stock_debt():
    """反模式演示：只检查本批新文件会漏掉存量债（存量债在旧文件里）。"""
    mod = _load()
    with tempfile.TemporaryDirectory() as td:
        # 旧文件含存量债（未用 import → F401）
        _write(os.path.join(td, "old_tool.py"), "import os\n\ndef g():\n    return 2\n")
        # 本批新文件（干净）
        _write(os.path.join(td, "new_623.py"), "def h():\n    return 3\n")
        # 整目录门禁：应抓到 old_tool.py 的债 → 红
        whole = mod.collect_py_files([td])
        rc_whole, _ = mod.run_ruff(whole)
        assert rc_whole != 0, "整目录门禁应抓到存量债"
        # 只跑本批（*623*）门禁：漏掉 old_tool.py → 绿（陷阱）
        batch = mod.collect_batch_files([td], ["*623*"])
        assert batch and all("623" in os.path.basename(b) for b in batch)
        rc_batch, _ = mod.run_ruff(batch)
        assert rc_batch == 0, "只跑本批会漏检存量债（正是 622 的口径陷阱）"


def test_skip_non_py_files():
    mod = _load()
    with tempfile.TemporaryDirectory() as td:
        _write(os.path.join(td, "a.py"), "def f():\n    return 1\n")
        _write(os.path.join(td, "notes.md"), "# 非 py 文件\n")  # 不应被 ruff 处理
        targets = mod.collect_py_files([td])
        assert targets == [os.path.join(td, "a.py")], "应跳过非 .py 文件"
        rc, _ = mod.run_ruff(targets)
        assert rc == 0


def test_real_tools_dir_green_after_b2():
    """验证 623 B2 修复后，真实 tools/ 整目录 ruff 全绿（门禁真实口径）。"""
    mod = _load()
    whole = mod.collect_py_files([os.path.join(ROOT, "tools")])
    assert whole, "tools/ 应含 .py 文件"
    rc, out = mod.run_ruff(whole)
    assert rc == 0, f"tools/ 整目录应全绿，实际:\n{out}"
