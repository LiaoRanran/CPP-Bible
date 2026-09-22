"""623 C2 · 尺子覆盖率审计 单元测试（≥3 例）"""
from __future__ import annotations

import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(ROOT, "tools", "ruler_coverage_audit_623.py")


def _load():
    spec = importlib.util.spec_from_file_location("ruler_audit_623", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_critical_rulers_count():
    mod = _load()
    assert len(mod.CRITICAL_RULERS) == 11


def test_no_exposed():
    mod = _load()
    r = mod.audit()
    assert r["exposed"] == [], f"应有 0 裸露，实际 {r['exposed']}"
    assert r["protected_count"] == 11


def test_check_exits_zero():
    mod = _load()
    assert mod.main(["--check"]) == 0
