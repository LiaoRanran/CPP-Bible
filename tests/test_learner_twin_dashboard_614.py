#!/usr/bin/env python3
"""614 B2 回归测试：learner_twin_dashboard_614（真实数据版）。"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import learner_behavior_logger as b1  # noqa: E402
import learner_twin_dashboard_614 as b2  # noqa: E402


def _seed(tmp_path: Path) -> Path:
    store = tmp_path / "beh.jsonl"
    b1.simulate(store, kcs_n=10, rounds=5, seed=7)
    return store


def test_data_reading(tmp_path: Path) -> None:
    store = _seed(tmp_path)
    d = b2.build(store)
    assert len(d["kcs"]) == 27
    # 至少被学习的 10 个 KC 掌握度应 > 初始 0.1
    learned = [k for k in d["kcs"] if d["mastery"].get(k["id"], 0.1) > 0.1]
    assert len(learned) >= 5
    assert d["stats"]["total_events"] == 50
    assert 0.0 <= d["stats"]["avg_mastery"] <= 1.0


def test_html_generation(tmp_path: Path) -> None:
    store = _seed(tmp_path)
    d = b2.build(store)
    html = b2.render_html(d)
    assert "学习者镜像仪表盘" in html
    assert html.count('class="cell"') == 27
    assert "掌握度热力图" in html and "推荐学习路径" in html and "统计" in html


def test_key_elements_present(tmp_path: Path) -> None:
    store = _seed(tmp_path)
    d = b2.build(store)
    html = b2.render_html(d)
    # 进度曲线 SVG 存在（有事件即有 polyline）
    assert "<polyline" in html
    # 推荐路径随掌握度变化：被学习的 10 个 KC 不应出现在推荐列表
    recommended = set(d["recommended"])
    learned_ids = set(b1._kc_ids()[:10])
    assert learned_ids.isdisjoint(recommended)
    assert len(recommended) < 27  # 推荐集合随掌握度变化（非全量）
