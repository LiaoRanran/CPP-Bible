"""612 B3 回归测试：活性锚补全 what-if（只读，锁 warn 消除预测）。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import liveness_impact as b3  # noqa: E402


def test_whatif_generates():
    r = b3.analyze(None)
    assert {"warn_before", "warn_after", "addressed", "by_class"} <= set(r)


def test_zero_completion_keeps_baseline():
    r = b3.analyze(0)
    assert r["addressed"] == 0
    assert r["warn_after"] == r["warn_before"] == 50


def test_full_completion_clears_all():
    r = b3.analyze(None)
    assert r["addressed"] == 50
    assert r["warn_after"] == 0


def test_check_passes():
    assert b3.main(["--check"]) == 0
