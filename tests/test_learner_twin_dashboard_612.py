#!/usr/bin/env python3
"""D5 回归测试：学习者镜像仪表盘（自包含 HTML）。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "tools"))

import learner_twin_dashboard as d5  # noqa: E402


def test_render_has_four_modules():
    d = d5._simulated_data()
    page = d5.render(d, d["kc_inv"], d["by_id"], d["mastery"])
    for marker in ("学习统计面板", "KC 掌握度热力图", "学习进度曲线", "推荐学习路径"):
        assert marker in page, marker
    assert "模拟数据" in page
    assert "<!DOCTYPE html>" in page


def test_html_self_contained():
    d = d5._simulated_data()
    page = d5.render(d, d["kc_inv"], d["by_id"], d["mastery"])
    # 无外部依赖（无 http 外链 / 无 CDN script src / 无 link href 外链）
    assert "src=\"http" not in page
    assert "cdn" not in page.lower()
    assert "<link" not in page


def test_color_contrast_pairs():
    low_bg, low_fg = d5._color(0.1)
    mid_bg, mid_fg = d5._color(0.5)
    high_bg, high_fg = d5._color(0.9)
    assert low_bg == "#b71c1c" and low_fg == "#ffffff"
    assert mid_bg == "#f9a825" and mid_fg == "#1a1a1a"
    assert high_bg == "#1b5e20" and high_fg == "#ffffff"


def test_check_passes():
    assert d5.main(["--check"]) == 0


def test_file_generated():
    # 默认命令应写出 HTML 文件且非空
    rc = d5.main([])
    assert rc == 0
    p = Path(__file__).resolve().parents[1] / "data" / "learner_twin_dashboard_612.html"
    assert p.is_file() and p.stat().st_size > 2000
