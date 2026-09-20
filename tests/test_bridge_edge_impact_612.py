"""612 A3 回归测试：加桥后 W2 重算 + 判决变化（锁基线不变量）。"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import bridge_edge_impact as a3  # noqa: E402


def test_impact_generates():
    r = a3.impact("keep-low", "approved-only")
    assert {"base_summary", "new_summary", "flipped", "flips",
            "components_before", "components_after"} <= set(r)


def test_zero_approved_matches_baseline_keep_low():
    r = a3.impact("keep-low", "approved-only")
    assert r["bridges_applied"] == 0
    assert r["base_summary"]["IN"] == 114 and r["base_summary"]["OUT"] == 7


def test_zero_approved_matches_baseline_upgrade_medium():
    r = a3.impact("upgrade-medium", "approved-only")
    assert r["base_summary"]["IN"] == 121 and r["base_summary"]["OUT"] == 0


def test_whatif_all_medium_runs_and_improves_components():
    r = a3.impact("keep-low", "all-medium")
    assert r["bridges_applied"] == 98
    assert r["components_before"] == 11 and r["components_after"] == 7
    assert r["flipped"] == 0            # 与 C3 一致：加桥判决变化 0


def test_flips_format():
    for m in a3.MODES:
        for w in a3.WHATIFS:
            r = a3.impact(m, w)
            for f in r["flips"]:
                assert {"node_id", "old", "new", "node_type"} <= set(f)


def test_check_passes():
    assert a3.main(["--check"]) == 0
