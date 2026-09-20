"""610 E1 · 逃逸率收敛曲线回归锁（v1→v7 + C-P95 + 尺子变更史 + 自包含 HTML）。

锁四件事（任务书 E1 的 4 例 + 3 例自加）：
  1. `load_baselines`：**7** 个版本齐备（v1…v7），v7 = **1/1406**；
     v1–v4 **无** `equivalent` 字段 ⇒ 记 None（不是 0！"没这个字段"≠"0 条"）；
  2. `compute_cp95(1, 1406)` = **[0.0018%, 0.3956%]**（与冻结值 1e-9 一致，复用 609 E1 的实现）；
  3. `detect_ruler_changes`：≥3 处（实测 **6** 处），每处给出可测原因 + 权威 note；
  4. `generate` 出**自包含** HTML：含 `<svg>`、误差带、尺子变更竖线，且**无外部资源**；
  +. `--check` exit 0；
  +. 图注必须含"不是同一量的时间序列"（防止被读成进步曲线）；
  +. 缺版本 ⇒ 标"数据缺失"而不是画 0。
"""
from __future__ import annotations

import json
from pathlib import Path

import escape_rate_trend as ert


def test_load_baselines():
    rows = ert.load_baselines()
    assert [r["version"] for r in rows] == [f"v{i}" for i in range(1, 8)]
    assert not any(r.get("missing") for r in rows), "v1…v7 基线文件应齐备"
    v7 = rows[6]
    assert (v7["escaped"], v7["judgeable"]) == (1, 1406)
    assert v7["n_a"] == 179 and v7["equivalent"] == 8
    v1 = rows[0]
    assert v1["equivalent"] is None, "v1 没有 equivalent 字段 ⇒ 必须是 None（不是 0）"
    assert (v1["escaped"], v1["judgeable"]) == (227, 956)


def test_compute_cp95():
    lo, up = ert.compute_cp95(1, 1406)
    assert abs(lo - 1.8006813682120512e-05) < 1e-9
    assert abs(up - 0.003956325504751501) < 1e-9
    assert round(lo * 100, 4) == 0.0018 and round(up * 100, 4) == 0.3956
    lo0, up0 = ert.compute_cp95(0, 1406)
    assert lo0 == 0.0 and up0 > 0.0, "零失效上界不许是 0"


def test_detect_ruler_changes():
    t = ert.trend()
    ch = t["ruler_changes"]
    assert len(ch) >= 3, f"尺子变更点应 ≥3（实测 {len(ch)}）"
    pairs = [(c["from"], c["to"]) for c in ch]
    assert ("v1", "v2") in pairs and ("v6", "v7") in pairs
    v45 = [c for c in ch if c["from"] == "v4" and c["to"] == "v5"][0]
    assert any("equivalent" in r for r in v45["reasons"]), "v4→v5 应识别出 equivalent 字段引入"
    assert all(c["reasons"] and c["note"] for c in ch), "每处变更都要有原因与 note"
    assert "不得声称单调收敛" in t["note"]


def test_generate_trend_html(tmp_path: Path):
    t = ert.trend()
    html = ert.render_html(t["baselines"], t["ruler_changes"])
    assert "<svg" in html and "</svg>" in html
    assert html.count("尺子变更") >= 6
    assert "C-P95" in html and "0.3956%" in html
    assert "不是同一量的时间序列" in html
    for bad in ('src="http', 'href="http', "cdn."):
        assert bad not in html, f"必须自包含（发现外部资源 {bad}）"
    out = tmp_path / "t.html"
    assert ert.main(["generate", "--out", str(out)]) == 0
    assert out.read_text(encoding="utf-8") == html


def test_check_is_green():
    assert ert.check() == []
    assert ert.main(["--check"]) == 0


def test_missing_version_marked_not_zeroed(tmp_path: Path):
    """把 v5 藏起来 ⇒ 必须标"数据缺失"，**不许**当成 0 逃逸率画点。"""
    d = tmp_path / "mutation"
    d.mkdir()
    for f in ert.BASELINE_DIR.glob("full_baseline_v*.json"):
        if f.name != "full_baseline_v5.json":
            (d / f.name).write_text(f.read_text(encoding="utf-8"), encoding="utf-8")
    rows = ert.enrich_with_intervals(ert.load_baselines(d))
    v5 = [r for r in rows if r["version"] == "v5"][0]
    assert v5["missing"] is True
    assert v5["escape_rate"] is None, "缺失版本不得被当成 0"
    html = ert.render_html(rows, ert.detect_ruler_changes(rows))
    assert "数据缺失" in html


def test_cli_stats_json(capsys):
    assert ert.main(["stats", "--json"]) == 0
    t = json.loads(capsys.readouterr().out)
    assert len(t["baselines"]) == 7
    assert t["baselines"][6]["cp95_upper"] < 0.004
