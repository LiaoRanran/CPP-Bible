"""609 C1 · 论证落地可视化：单文件自包含 HTML（**零外部依赖、离线可双击打开**）。

为什么必须自包含：论证图是给**人**看的；一张要联网取 CDN 的图，在 evidence 评审现场
打不开就等于没有。故 SVG 手绘、CSS 内联、数据随 HTML 内联落盘（不引外部字体/JS 库）。

版式：
  * **SVG 圆形布局**：节点等分圆周，命题画圆、误解画方；
    攻击边（真实构成击败的，即 `defeated_attackers`）红细实线；
    支持边（`defenders` 派生的"为它辩护"关系）绿虚线；
    悬停 `<title>` 给节点摘要（不必开控制台）。
  * **仪表盘**：IN/OUT/UNDEC 三条横条 + 各自占比。
  * **Top10 表**：被攻击最多的节点 + 攻击者数 + 辩护者数。

CLI：
    render [--labels DOC] [--out FILE]     0 ok / 2 文档不存在
    --check                                0 合法 / 1 文档结构破
"""
# mypy: ignore-errors
from __future__ import annotations

import argparse
import html
import json
import math
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VERSION = "1.0"
DEFAULT_LABELS = ROOT / "data" / "grounded_labels_w2.json"
DEFAULT_OUT = ROOT / "data" / "argument_net.html"

TOP_N = 10
COLOR = {"IN": "#2e7d32", "OUT": "#c62828", "UNDEC": "#9e9e9e",
         "proposition": "#1565c0", "misconception": "#ef6c00"}


def load_doc(path: Path | str = DEFAULT_LABELS) -> dict:
    p = Path(path)
    if not p.is_file():
        raise SystemExit(f"[visualizer] 标注文档不存在：{p}（先跑 weighted_af_solver.py solve）")
    try:
        doc = json.loads(p.read_text(encoding="utf-8"))
    except ValueError as exc:
        raise SystemExit(f"[visualizer] 标注文档不是合法 JSON：{exc}") from exc
    if not isinstance(doc, dict) or "nodes" not in doc or "summary" not in doc:
        raise SystemExit("[visualizer] 标注文档结构不完整（缺 nodes/summary）⇒ 拒绝出图")
    return doc


def support_edges(nodes: dict[str, dict]) -> list[tuple[str, str]]:
    """支持边 = `defenders` 的反向展开：`d` 为 `n` 辩护 ⇒ (d, n) 是支持边（去重排序）。"""
    out: set[tuple[str, str]] = set()
    for nid, v in nodes.items():
        for d in v.get("defenders", ()):
            if d in nodes:
                out.add((str(d), str(nid)))
    return sorted(out)


def attack_edges(nodes: dict[str, dict]) -> list[tuple[str, str]]:
    """攻击边 = 真实构成击败的入边（`defeated_attackers`），避开"有边无击败"的假攻击。"""
    return sorted({(str(a), str(nid)) for nid, v in nodes.items()
                   for a in v.get("defeated_attackers", ()) if a in nodes})


def _pos(seq: dict[str, str], r: float, cx: float, cy: float) -> dict[str, tuple[float, float]]:
    ids = sorted(seq)
    n = max(len(ids), 1)
    out: dict[str, tuple[float, float]] = {}
    for i, nid in enumerate(ids):
        ang = 2 * math.pi * i / n - math.pi / 2
        out[nid] = (cx + r * math.cos(ang), cy + r * math.sin(ang))
    return out


def build_svg(nodes: dict[str, dict], *, w: int = 900, h: int = 620) -> str:
    seq = {k: v["type"] for k, v in nodes.items()}
    cx, cy, r = w / 2, h / 2, min(w, h) * 0.40
    pos = _pos(seq, r, cx, cy)
    lines: list[str] = [f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" '
                        f'font-family="sans-serif" font-size="11">',
                        f'<rect width="{w}" height="{h}" fill="#ffffff"/>']
    for a, b in support_edges(nodes):
        x1, y1 = pos[a]
        x2, y2 = pos[b]
        lines.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                     f'stroke="{COLOR["IN"]}" stroke-width="1" stroke-dasharray="4 3" opacity="0.45"/>')
    for a, b in attack_edges(nodes):
        x1, y1 = pos[a]
        x2, y2 = pos[b]
        lines.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
                     f'stroke="{COLOR["OUT"]}" stroke-width="1.2" opacity="0.7"/>')
    for nid in sorted(nodes):
        v = nodes[nid]
        x, y = pos[nid]
        label = html.escape(str(nid))
        fill = COLOR.get(str(v.get("label")), "#9e9e9e")
        tip = html.escape(f'{nid} [{v.get("type")}] {v.get("label")} '
                          f'cred={v.get("credibility")} attackers={len(v.get("attackers", ()))}')
        if v.get("type") == "proposition":
            lines.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="{fill}" '
                         f'stroke="#1565c0" stroke-width="1"><title>{tip}</title></circle>')
        else:
            lines.append(f'<rect x="{x - 8:.1f}" y="{y - 8:.1f}" width="16" height="16" fill="{fill}" '
                         f'stroke="#e65100" stroke-width="1"><title>{tip}</title></rect>')
        if len(label) <= 22:
            lines.append(f'<text x="{x + 12:.1f}" y="{y + 4:.1f}" fill="#333">{label}</text>')
    lines.append("</svg>")
    return "\n".join(lines)


def top_targets(nodes: dict[str, dict], n: int = TOP_N) -> list[dict]:
    rows = [{"node": k, "type": v.get("type"), "label": v.get("label"),
             "attackers": len(v.get("attackers", ())),
             "defenders": len(v.get("defenders", ()))}
            for k, v in nodes.items()]
    rows.sort(key=lambda r: (-r["attackers"], r["node"]))
    return rows[:n]


def render_html(doc: dict) -> str:
    nodes = doc["nodes"]
    s = doc["summary"]
    total = max(s.get("nodes", len(nodes)), 1)

    def bar(label: str, cnt: int, color: str) -> str:
        pct = cnt / total * 100
        return (f'<tr><td class="k">{label}</td><td class="v">{cnt}</td>'
                f'<td><div class="bar" style="width:{pct:.1f}%;background:{color}"></div>'
                f'<span class="pct">{pct:.1f}%</span></td></tr>')

    rows = "".join(bar(k, int(s.get(k, 0)), COLOR.get(k, "#9e9e9e"))
                   for k in ("IN", "OUT", "UNDEC"))
    top = "".join(
        f'<tr><td>{html.escape(str(r["node"]))}</td><td>{html.escape(str(r["type"]))}</td>'
        f'<td>{html.escape(str(r["label"]))}</td><td>{r["attackers"]}</td><td>{r["defenders"]}</td></tr>'
        for r in top_targets(nodes))
    return f"""<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<title>论证落地图 · W2 grounded</title>
<style>
body{{font-family:sans-serif;margin:24px;color:#222}}
table{{border-collapse:collapse;margin-top:8px}}
th,td{{border:1px solid #ddd;padding:4px 8px;text-align:left;font-size:12px}}
.k{{font-weight:700}} .v{{text-align:right}}
.bar{{height:10px;display:inline-block;vertical-align:middle}}
.pct{{font-size:11px;margin-left:6px;color:#666}}
.card{{border:1px solid #e0e0e0;border-radius:6px;padding:12px;margin-bottom:16px}}
svg text{{font-size:9px}}
</style></head><body>
<h1>论证落地图 · W2 可信度加权 grounded</h1>
<p class="note">节点 {s.get('nodes')} · 轮数 {doc.get('rounds')} ·
击败边 {doc.get('defeating_edges')}/{doc.get('edges')} ·
攻击边 {len(attack_edges(nodes))} · 支持边 {len(support_edges(nodes))}</p>
<div class="card"><h2>判决仪表盘</h2><table>{rows}</table></div>
<div class="card"><h2>论据拓扑</h2>{build_svg(nodes)}
<p class="note">红实线=攻击（构成击败）；绿虚线=支持；圆=命题；方=误解；悬停看摘要。</p></div>
<div class="card"><h2>Top{TOP_N} 被攻击节点</h2>
<table><tr><th>节点</th><th>类型</th><th>判决</th><th>攻击数</th><th>辩护数</th></tr>{top}</table></div>
</body></html>
"""


def render(*, labels: Path | str = DEFAULT_LABELS, out: Path | str = DEFAULT_OUT) -> Path:
    doc = load_doc(labels)
    p = Path(out)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(render_html(doc), encoding="utf-8", newline="\n")
    return p


def check(path: Path | str = DEFAULT_LABELS) -> list[str]:
    problems: list[str] = []
    if not Path(path).is_file():
        return [f"标注文档不存在：{path}"]
    doc = load_doc(path)
    nodes = doc.get("nodes")
    if not isinstance(nodes, dict) or not nodes:
        return ["nodes 为空或不是对象"]
    for nid, v in nodes.items():
        if str(v.get("label")) not in ("IN", "OUT", "UNDEC"):
            problems.append(f"{nid} 判决非 IN/OUT/UNDEC：{v.get('label')!r}")
        if str(v.get("type")) not in ("proposition", "misconception"):
            problems.append(f"{nid} 类型非法：{v.get('type')!r}")
    s = doc.get("summary", {})
    if int(s.get("nodes", -1)) != len(nodes):
        problems.append("summary.nodes 与 nodes 实际数量不一致")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="grounded_visualizer",
                                 description="609 C1 论证落地可视化（单文件自包含 HTML）")
    ap.add_argument("--version", action="version", version=f"grounded_visualizer {VERSION}")
    ap.add_argument("--labels", default=str(DEFAULT_LABELS))
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--check", action="store_true", help="校验标注文档结构")
    a = ap.parse_args(argv)

    if a.check:
        problems = check(a.labels)
        if problems:
            print(f"[visualizer] --check FAIL：{len(problems)} 项", file=sys.stderr)
            for m in problems[:50]:
                print("  - " + m, file=sys.stderr)
            return 1
        print(f"[visualizer] --check OK：{a.labels} 结构合法（节点 "
              f"{len(load_doc(a.labels)['nodes'])}）")
        return 0

    p = render(labels=a.labels, out=a.out)
    doc = load_doc(a.labels)
    nodes = doc["nodes"]
    print(f"[visualizer] 已写 {p.relative_to(ROOT).as_posix() if str(p).startswith(str(ROOT)) else p}"
          f"：节点 {len(nodes)} · 攻击边 {len(attack_edges(nodes))} · "
          f"支持边 {len(support_edges(nodes))} · Top{TOP_N} 已附")
    return 0


if __name__ == "__main__":
    sys.exit(main())
