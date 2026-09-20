#!/usr/bin/env python3
"""D2 回归测试：argument_fragmentation_613（碎片化：现状/投影/已生效 三态）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import argument_fragmentation_613 as d2  # noqa: E402


def test_projection_numbers():
    p = d2.projection()
    assert p["components_before"] == 11 and p["components_after"] == 7
    assert p["candidates_added"] == 98
    assert 0.66 < p["coverage_before"] < 0.67
    assert 0.80 < p["coverage_after"] < 0.81


def test_effective_is_zero_because_no_human_review():
    n_rev, _n_app = d2.effective_edges()
    assert n_rev == 0, "本批未做人审 ⇒ 已生效必须为 0"


def test_no_verdict_change_in_projection():
    p = d2.projection()
    assert p["verdict_changed"] == 0


def test_report_distinguishes_real_from_projection():
    p = d2.projection()
    n_rev, n_app = d2.effective_edges()
    page = d2.render(p, n_rev, n_app)
    assert "现状（真实）" in page and "投影" in page and "已生效" in page
    assert "并未真正改善" in page


def test_check_passes():
    assert d2.main(["--check"]) == 0
