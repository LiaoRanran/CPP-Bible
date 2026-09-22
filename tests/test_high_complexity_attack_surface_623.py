"""623 E1 · 高复杂度带攻击面分析 单元测试（≥4 例）"""
from __future__ import annotations

import importlib.util
import os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOL = os.path.join(ROOT, "tools", "high_complexity_attack_surface_623.py")


def _load():
    spec = importlib.util.spec_from_file_location("hc_as_623", TOOL)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_load_rules_count():
    mod = _load()
    rules = mod.load_rules()
    assert len(rules) == 63


def test_reproduces_622_e2_finding():
    mod = _load()
    r = mod.analyze()
    # 622 E2 核心结论：高复杂度带 warn-only，EV-SERVES-EXIST 是代表
    assert "EV-SERVES-EXIST" in r["reproduced_622_e2"]


def test_hc_warn_are_warn_severity():
    mod = _load()
    rules = {x["rule"]: x["severity"] for x in mod.load_rules()}
    r = mod.analyze()
    for rid in r["hc_warn_touched"]:
        assert rules.get(rid) == "warn", f"{rid} 应为 warn 级"


def test_attack_surface_score_range():
    mod = _load()
    r = mod.analyze()
    s = r["attack_surface_score"]
    assert 0 <= s <= 100
    assert s > 0
