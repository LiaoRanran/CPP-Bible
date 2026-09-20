#!/usr/bin/env python3
"""C4 回归测试：learner_twin_dashboard_613（仪表盘升级版 · 自包含 HTML）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import learner_twin_dashboard_613 as c4  # noqa: E402


def test_self_contained_html():
    html = c4.render()
    assert "<script" not in html
    assert "https://" not in html and "http://" not in html.replace("http://www.w3.org", "")


def test_four_modules_present():
    html = c4.render()
    for sec in ("掌握度热力图", "域级汇总", "推荐学习路径", "真实行为统计"):
        assert sec in html


def test_banner_marks_simulated_when_no_real_updates():
    rows = [{"kind": "init", "simulated": False},
            {"kind": "update", "simulated": True}]
    assert c4.is_real(rows) is False, "只有 simulated 的 update 不算真实递推"
    assert c4.is_real([{"kind": "update", "simulated": False}]) is True


def test_behavior_stats_empty_and_scored():
    assert c4.behavior_stats([])["n"] == 0
    assert c4.behavior_stats([])["accuracy"] is None
    rows = [{"action_type": "answer", "correct": True, "kc_id": "A"},
            {"action_type": "test", "correct": False, "kc_id": "B"},
            {"action_type": "review", "correct": None, "kc_id": "A"}]
    s = c4.behavior_stats(rows)
    assert s["n"] == 3 and s["n_scored"] == 2
    assert abs(s["accuracy"] - 0.5) < 1e-9
    assert s["by_action"]["review"] == 1 and s["distinct_kc"] == 2


def test_mastery_map_reads_mastery_prob():
    # 字段名必须是 mastery_prob（612 实踩：写成 mastery 会恒 0）
    c4._state_rows = lambda: [{"user_id": "default", "kc_id": "K1", "mastery_prob": 0.7}]
    assert abs(c4.mastery_map()["K1"] - 0.7) < 1e-9
    c4._state_rows = _orig_state_rows


_orig_state_rows = c4._state_rows


def test_recommended_path_covers_all_kc():
    path = c4.recommended_path()
    assert len(path) == 27 and len(set(path)) == 27


def test_bar_and_color():
    assert len(c4._bar(1.0)) == 20 and len(c4._bar(0.0)) == 20
    assert c4._color(0.9) != c4._color(0.1)


def test_check_passes():
    assert c4.main(["--check"]) == 0
