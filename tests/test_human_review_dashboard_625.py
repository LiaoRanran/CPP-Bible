"""625 D2 · 人审深色科技风可视化回归测试（≥4 例）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import human_review_dashboard_625 as D  # noqa: E402

HTML = os.path.join(ROOT, "data", "human_review_dashboard_625.html")


def test_selftest_passes():
    assert D.selftest() == 0


def test_dashboard_html_generated():
    assert os.path.exists(HTML) and os.path.getsize(HTML) > 5000


def test_html_is_dark_tech_theme():
    txt = open(HTML, encoding="utf-8").read()
    assert "<!doctype html>" in txt
    assert "#0a0e1a" in txt                 # 深色背景
    assert "radial-gradient" in txt         # 科技光晕
    assert "function f(" in txt             # 筛选交互


def test_ambiguity_distribution_present():
    txt = open(HTML, encoding="utf-8").read()
    for amb in ("high", "medium", "low"):
        assert f"amb-{amb}" in txt


def test_readonly_no_authority_mutation():
    before = os.path.getsize(os.path.join(ROOT, "data", "authority", "authority_log.jsonl"))
    D.selftest()
    after = os.path.getsize(os.path.join(ROOT, "data", "authority", "authority_log.jsonl"))
    assert before == after
