"""629 A3 · 自身免疫率仪表盘 单测（7 例）。"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import autoimmune_dashboard_629 as D


def _html() -> str:
    return open(D.OUT_HTML, encoding="utf-8").read()


def test_html_is_self_contained():
    html = _html()
    assert len(html) > 6000
    assert not re.search(r'(src|href)\s*=\s*["\']https?://', html), "不得含外部资源"
    assert "<style>" in html and "backdrop-filter" in html
    assert "--bg:#0a0e1a" in html, "深色底必须内联"


def test_all_five_modules_present():
    html = _html()
    for m in D.MODULES:
        assert m in html, f"缺模块：{m}"


def test_escape_side_numbers():
    html = _html()
    assert (D.ESCAPE["hits"], D.ESCAPE["total"]) == (1, 1406)
    assert "1/1406" in html and "0.9062%" in html and "124/124" in html
    assert "0.071%" in html, "逃逸率应格式化到 3 位小数"


def test_autoimmune_side_matches_live_measurement():
    import autoimmune_rate_framework as A

    live = A.measure()
    html = _html()
    assert f"{live['rate'] * 100:.1f}%" in html
    assert f"（{live['warned_count']}/{live['total']}）" in html
    assert f"{len(live['hard_defect_cards'])} 张" in html
    assert f"{len(live['caliber_only_cards'])} 张" in html


def test_confusion_matrix_four_cells():
    html = _html()
    for kw in ("真阳性", "假阴性", "假阳性", "真阴性"):
        assert kw in html
    assert "格式过敏率" in html
    assert "中枢耐受" in html and "外周耐受" in html


def test_generate_is_deterministic():
    a = D.generate()
    b = D.generate()
    assert a == b, "生成必须是确定性的（同一数据 → 同一页面）"


def test_check_is_read_only_and_passes():
    before = os.stat(D.OUT_HTML)
    assert D.selftest() == 0
    after = os.stat(D.OUT_HTML)
    assert (before.st_size, before.st_mtime_ns) == (after.st_size, after.st_mtime_ns), \
        "--check 不得写盘"
