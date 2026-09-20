"""610 B3 · 辩护链可视化回归锁（自包含 HTML/SVG，无外部依赖）。

锁四件事（任务书 4 例 + 4 例自加）：
  1. 生成 HTML 非空且含 `<svg>` 与 `<script>`（静态图 + 点击交互）；
  2. 图里正好 **121** 个节点（79 命题 ◯ 外圈 + 42 误解 ◻ 内圈）；
  3. 图例齐全（IN/OUT/UNDEC + 击败边/非击败边 + ◯/◻ 含义）；
  4. **自包含**：不引用任何外部资源（无 `src="http`/`href="http`/CDN；`xmlns` 是命名空间不算拉取）；
  +. 击败边画红粗线 = **17** 条（与非击败边共 388 条）；
  +. 点击 handler + OUT 节点静态兜底表（7 行）；
  +. 判决颜色语义：#35705A(IN) / #A14E50(OUT)；
  +. 两次生成逐字一致（幂等，便于入库 diff）。
"""
from __future__ import annotations

from pathlib import Path

import defense_chain as dc

EDGES, VERDICTS, CRED = dc.load_data()


def _html(tmp_path: Path) -> str:
    p = dc.generate_defense_chain_html(EDGES, VERDICTS, CRED, tmp_path / "d.html")
    return p.read_text(encoding="utf-8")


def test_generate_html(tmp_path: Path):
    html = _html(tmp_path)
    assert len(html) > 10_000
    assert "<svg" in html and "</svg>" in html and "<script>" in html
    assert "<!DOCTYPE html>" in html and "<style>" in html


def test_html_has_all_nodes(tmp_path: Path):
    html = _html(tmp_path)
    total = html.count('class="node"')
    assert total == 121, f"节点数应为 121（实测 {total}）"
    assert html.count("<circle class=\"node\"") == 79, "外圈应为 79 个命题（圆）"
    assert html.count("<rect class=\"node\"") == 42, "内圈应为 42 个误解（方）"


def test_html_has_legend(tmp_path: Path):
    html = _html(tmp_path)
    for item in ("IN", "OUT", "UNDEC", "击败边（可信度严格大于）", "非击败边",
                 "命题（外圈 79）", "误解（内圈 42）"):
        assert item in html, f"图例缺 {item}"


def test_html_self_contained(tmp_path: Path):
    html = _html(tmp_path)
    for bad in ('src="http', "src='http", 'href="http', "href='http", "cdn."):
        assert bad not in html, f"引用了外部资源：{bad}"
    assert "w3.org/2000/svg" in html, "SVG 命名空间是必需的（不是资源拉取）"


def test_edges_are_rendered_with_correct_weights(tmp_path: Path):
    html = _html(tmp_path)
    assert html.count('stroke="#A14E50" stroke-width="1.8"') == 17, "击败边应 17 条红粗线"
    assert html.count('stroke="#9E9E9E" stroke-width="0.6"') == 371, "非击败边应 371 条灰细线"


def test_interaction_and_static_fallback(tmp_path: Path):
    html = _html(tmp_path)
    assert 'onclick="show(' in html and "function show(id)" in html
    assert "节点详情" in html and "静态兜底" in html
    assert html.count("<tr><td><code>MIS-") == 7, "OUT 节点静态表应 7 行"
    assert "#35705A" in html and "#A14E50" in html


def test_generation_is_idempotent(tmp_path: Path):
    assert _html(tmp_path) == _html(tmp_path)


def test_cli_html(tmp_path: Path, capsys):
    out = tmp_path / "cli.html"
    assert dc.main(["html", "--out", str(out)]) == 0
    assert "自包含 HTML" in capsys.readouterr().out
    assert out.read_text(encoding="utf-8").count('class="node"') == 121
