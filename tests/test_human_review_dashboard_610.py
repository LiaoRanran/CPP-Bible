"""610 E2 · 人审进度仪表盘回归锁（自包含 HTML：总览 + 分组 + 主题 + 方向 + OUT 列表）。

锁三件事（任务书 E2 的 3 例 + 4 例自加）：
  1. `generate` 出非空 HTML 且含 `<svg>`（柱状图 + 饼图）；
  2. 总览卡片含 **388 / 100% / 354 / 34 / 0**（approve/modify/reject）；
  3. 含 **OUT 的 7 个 MIS** 清单（红色高亮类 `out`）；
  +. 自包含（无外部资源）；
  +. 饼图弧段数 == 主题数（5）；柱状图行数 ≤ 10；
  +. `--check` exit 0；篡改 HTML ⇒ exit 1；
  +. 缺 timestamp ⇒ 明说"无时间线数据"（不伪造时间线）。
"""
from __future__ import annotations

import json
from pathlib import Path

import human_review_dashboard as hd

ANNS = hd.hrr.load_annotations()


def test_generate_dashboard(tmp_path: Path):
    html = hd.render(ANNS)
    assert len(html) > 5_000
    assert "<!DOCTYPE html>" in html and html.count("<svg") == 2
    out = tmp_path / "d.html"
    assert hd.main(["generate", "--out", str(out)]) == 0
    assert out.read_text(encoding="utf-8") == html


def test_dashboard_has_overview():
    html = hd.render(ANNS)
    for want in (">388<", ">100%<", ">354<", ">34<", ">0<"):
        assert want in html, f"总览卡片缺 {want}"
    assert '<div class="k">记录数</div>' in html
    assert "完成度" in html and '<div class="k">approve</div>' in html


def test_dashboard_has_out_mis():
    html = hd.render(ANNS)
    assert "OUT 的 MIS（7 个" in html
    for mis in ("MIS-LANG-001", "MIS-MEM-001", "MIS-MEM-003", "MIS-UB-001",
                "MIS-UB-004", "MIS-UB-008", "MIS-UB-014"):
        assert f"class='out'>{mis}<" in html, f"缺 OUT MIS：{mis}"
    assert len(hd.out_mis_list()) == 7


def test_self_contained_and_chart_counts():
    html = hd.render(ANNS)
    for bad in ('src="http', 'href="http', "cdn."):
        assert bad not in html, f"必须自包含（发现 {bad}）"
    assert html.count("<path d=") == 5, "饼图弧段应等于主题数（5）"
    top10 = hd.hrr.summarize_by_mis(ANNS)[:10]
    assert hd._bars(top10).count('fill="#ef6c00"') == len(top10) == 10, "柱状图应有 10 行"


def test_check_consistency(tmp_path: Path, monkeypatch):
    hd.generate(out=tmp_path / "d.html")
    monkeypatch.setattr(hd, "DEFAULT_HTML", tmp_path / "d.html")
    assert hd.check() == []
    assert hd.main(["--check"]) == 0
    (tmp_path / "d.html").write_text("stale", encoding="utf-8")
    assert hd.main(["--check"]) == 1


def test_timeline_missing_is_explicit():
    tl = hd.timeline([])
    assert tl == {"days": {}, "missing": 0, "has_data": False}
    html = hd.render([])
    assert "无时间线数据" in html
    tl2 = hd.timeline([{"reason": "x"}])
    assert tl2["missing"] == 1 and tl2["has_data"] is False


def test_timeline_aggregates_by_day():
    tl = hd.timeline(ANNS)
    assert tl["has_data"] is True
    assert sum(tl["days"].values()) + tl["missing"] == len(ANNS)
    assert all(len(d) == 10 for d in tl["days"]), "日期应按 ISO YYYY-MM-DD 聚合"
    for d, n in tl["days"].items():
        assert isinstance(json.loads(json.dumps({d: n})), dict)
