"""628 C1 · 人审仪表盘 v2 单测（8 例）。

断言 HTML 里**真实存在**的模块与样式（不测"应该好看"），并校验数据与当前状态一致。
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import human_review_dashboard_v2_628 as D


@pytest.fixture(scope="module")
def html():
    return D.generate()


@pytest.fixture(scope="module")
def data():
    return D.build()


def test_html_is_selfcontained_offline(html):
    assert html.startswith("<!doctype html>")
    assert "http://" not in html and "https://" not in html   # 无外部 CDN
    assert "<script" in html and "<style>" in html


def test_six_data_modules_present(html):
    for kw in ("① 人审进度", "② 歧义度热力图", "③ review_method",
               "④ W2 论证图 3D", "⑤ 独立人类确认强度", "⑥ 他验三件套状态"):
        assert kw in html


def test_dark_tech_style_present(html):
    for kw in ("#0a0e1a", "backdrop-filter:blur(10px)", "--cyan:#3ad6c5",
               "--violet:#8b6cff", "conic-gradient", "preserve-3d",
               "@keyframes float", "@keyframes spin"):
        assert kw in html


def test_data_matches_current_state(data):
    assert data["review"]["unique"] == 93
    assert data["w2"]["labels"] == {"IN": 114, "OUT": 7, "UNDEC": 0}
    assert len(data["w2"]["nodes"]) == 121
    assert data["blind_count"] == 0
    assert sum(data["methods"].values()) == data["events"] > 0


def test_ring_and_gauge_render_from_data(html, data):
    assert html.count("<circle") >= 4           # 底环 + 3 段进度
    assert "stroke-dasharray" in html
    assert f'>{data["review"]["unique"]}</text>' in html
    assert 'class="gnum"' in html and "目标 93" in html


def test_heatmap_has_one_cell_per_item(html, data):
    assert html.count('class="heat">') == 1
    assert html.count("</i>") >= len(data["items"])
    assert sum(1 for it in data["items"] if it["proof"]) > 0   # A3 写入的对称性证明 id
    assert data["items"] == sorted(data["items"], key=lambda i: -i["score"])


def test_3d_scene_uses_all_nodes(html):
    assert html.count('class="node ') == 121
    assert "translate3d(var(--x),var(--y),var(--z))" in html


def test_selftest_exit_zero():
    assert D.selftest() == 0
