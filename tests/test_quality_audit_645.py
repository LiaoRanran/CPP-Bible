"""645 阶段 F1/F2 · 优雅代码审计单测（fast）。"""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import quality_audit_645 as f  # noqa: E402


def test_selftest_passes():
    """--check 只读自检（AST 行为正确）。"""
    assert f.selftest() == 0


def test_audit_file_detects_missing_doc(tmp_path):
    """缺 docstring 的公开函数应被检出。"""
    p = tmp_path / "m.py"
    p.write_text("import json\n\n\ndef nodoc():\n    return json.dumps({})\n", encoding="utf-8")
    r = f.audit_file(str(p))
    assert "<module>" in r["missing_docstrings"]
    assert "nodoc" in r["missing_docstrings"]
    assert r["unused_import_candidates"] == []


def test_audit_file_private_skipped(tmp_path):
    """以下划线开头的私有函数不计入覆盖率。"""
    p = tmp_path / 'm.py'
    p.write_text('"""d"""\n\n\ndef _priv():\n    return 1\n', encoding="utf-8")
    r = f.audit_file(str(p))
    assert r["missing_docstrings"] == []


def test_audit_real_runs():
    """真实审计 645 工具，覆盖率应为 1.0（本批工具均有 docstring）。"""
    res = f.audit()
    assert res["tool_count"] >= 10
    assert res["docstring_coverage"] == pytest.approx(1.0)
