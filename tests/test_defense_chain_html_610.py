"""610 B3 · 辩护链可视化回归锁（自包含 HTML/SVG，无外部依赖）。

**640c A1/A2 重写**：原版把渲染结果写死（节点 121 / 命题 79 / 误解 42、
击败边 17 / 非击败边 371 / OUT 静态表 7 行），人签重算后批量过期（640c 的 2 项）。

现在断言的是**渲染 == 现算**：期望值由 `defense_chain` 的判定现算给出
（击败边由 `dc.is_defeating` 逐边判定），不出现任何"当前数字"的字面量 ——
仓库正常演进（加边/人签）时自动跟随，渲染逻辑坏了才红。
"""
from __future__ import annotations

from pathlib import Path

import defense_chain as dc

EDGES, VERDICTS, CRED = dc.load_data()
N_PROP = sum(1 for n in VERDICTS if dc.node_type_of(n, EDGES) == "proposition")
N_MIS = len(VERDICTS) - N_PROP
N_DEFEATING = sum(1 for e in EDGES if dc.is_defeating(e, CRED))
N_PLAIN = len(EDGES) - N_DEFEATING
N_OUT = sum(1 for v in VERDICTS.values() if v == "OUT")


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
    assert html.count('class="node"') == len(VERDICTS)
    assert html.count("<circle class=\"node\"") == N_PROP, "外圈为命题（圆）"
    assert html.count("<rect class=\"node\"") == N_MIS, "内圈为误解（方）"


def test_html_has_legend(tmp_path: Path):
    html = _html(tmp_path)
    for item in ("IN", "OUT", "UNDEC", "击败边（可信度严格大于）", "非击败边",
                 f"命题（外圈 {N_PROP}）", f"误解（内圈 {N_MIS}）"):
        assert item in html, f"图例缺 {item}"


def test_html_self_contained(tmp_path: Path):
    html = _html(tmp_path)
    for bad in ('src="http', "src='http", 'href="http', "href='http", "cdn."):
        assert bad not in html, f"引用了外部资源：{bad}"
    assert "w3.org/2000/svg" in html, "SVG 命名空间是必需的（不是资源拉取）"


def test_edges_are_rendered_with_correct_weights(tmp_path: Path):
    """渲染出的边权重必须等于现算的击败/非击败划分（真验证：渲染 vs 判定）。"""
    html = _html(tmp_path)
    assert html.count('stroke="#A14E50" stroke-width="1.8"') == N_DEFEATING, "击败边红粗线数不符"
    assert html.count('stroke="#9E9E9E" stroke-width="0.6"') == N_PLAIN, "非击败边灰细线数不符"
    assert html.count("<line ") == len(EDGES), "边总数不符"


def test_interaction_and_static_fallback(tmp_path: Path):
    html = _html(tmp_path)
    assert 'onclick="show(' in html and "function show(id)" in html
    assert "节点详情" in html and "静态兜底" in html
    table = html.split("静态兜底")[1].split("</table>")[0]     # 只看静态兜底表（脚本里的模板行不算）
    assert table.count("<tr><td><code>") == N_OUT, "OUT 节点静态表行数应等于 OUT 节点数"
    assert "#35705A" in html and "#A14E50" in html


def test_generation_is_idempotent(tmp_path: Path):
    assert _html(tmp_path) == _html(tmp_path)


def test_cli_html(tmp_path: Path, capsys):
    out = tmp_path / "cli.html"
    assert dc.main(["html", "--out", str(out)]) == 0
    assert "自包含 HTML" in capsys.readouterr().out
    assert out.read_text(encoding="utf-8").count('class="node"') == len(VERDICTS)
