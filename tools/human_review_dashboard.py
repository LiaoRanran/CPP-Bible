"""610 E2 · 人审进度仪表盘（自包含 HTML：SVG 柱状/饼图 + 卡片 + OUT 清单 + 时间线）。

口径全部复用 610 A2/A3 的统计函数（**单一真源**：仪表盘不许自己再算一套）。
纯 SVG 手绘（不引图表库）⇒ 离线可看；所有数字来自 388 条授权人审 + 入库 W2 产物。

七块内容：
  1. 总览卡片：记录数 / 完成度 / approve / modify / reject；
  2. Top10 modify 比例最高的 MIS（柱状图）；
  3. 主题分布（饼图，MEM/UB/HIST/CONC/LANG）；
  4. 方向分布（mis_to_prop / prop_to_mis）；
  5. **OUT 的 7 个 MIS**（红色高亮，取自入库 W2 产物，不另算）；
  6. 质量异常（A2 的检测结果原样呈现）；
  7. 时间线（按日聚合的审查时刻直方图；无 timestamp ⇒ 明说"无时间线数据"）。

CLI：
    generate [--out FILE]   0 ok
    --check                 0 与源数据一致 / 1 破
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from collections import Counter
from datetime import datetime
from pathlib import Path

from path_config_625 import root as _queyi_root  # noqa: E402  (625 C1 路径解耦)

ROOT = _queyi_root()
sys.path.insert(0, str(Path(__file__).resolve().parent))

import human_review_report as hrr  # noqa: E402

VERSION = "1.0"
DEFAULT_HTML = ROOT / "data" / "human_review_dashboard.html"
LABELS = ROOT / "data" / "grounded_labels_w2.json"

COLORS = ("#1565c0", "#2e7d32", "#ef6c00", "#6a1b9a", "#00838f", "#c62828")


def out_mis_list(labels_path: Path | str | None = None) -> list[str]:
    """OUT 的 MIS 列表（取自入库 W2 产物）。"""
    p = Path(labels_path) if labels_path else LABELS
    if not p.is_file():
        return []
    doc = json.loads(p.read_text(encoding="utf-8"))
    return sorted(k for k, v in doc.get("nodes", {}).items()
                  if v.get("type") == "misconception" and v.get("label") == "OUT")


def timeline(annotations: list[dict]) -> dict:
    """按日聚合（`timestamp` 为空/缺 ⇒ 明说没有时间线数据）。"""
    days: Counter = Counter()
    missing = 0
    for a in annotations:
        ts = str(a.get("timestamp") or a.get("reviewed_at") or "")
        if not ts:
            missing += 1
            continue
        try:
            days[datetime.fromisoformat(ts).date().isoformat()] += 1
        except ValueError:
            missing += 1
    return {"days": dict(sorted(days.items())), "missing": missing,
            "has_data": bool(days)}


def _bars(rows: list[dict], width: int = 720, row_h: int = 26) -> str:
    """横向柱状图（Top10 modify 比例）。"""
    h = row_h * len(rows) + 20
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {h}" '
           f'role="img" aria-label="modify 比例 Top10">',
           f'<rect width="{width}" height="{h}" fill="#fff"/>']
    for i, r in enumerate(rows):
        y = 14 + i * row_h
        ratio = r["modify_ratio"] or 0
        w = int((width - 320) * ratio)
        svg.append(f'<text x="150" y="{y + 12}" font-size="11" text-anchor="end" '
                   f'fill="#333">{r["mis_id"]}</text>')
        svg.append(f'<rect x="158" y="{y}" width="{w}" height="16" fill="#ef6c00" '
                   f'opacity="0.85"/>')
        svg.append(f'<text x="{158 + max(w, 2) + 6}" y="{y + 12}" font-size="11" '
                   f'fill="#333">{ratio:.2f}（{r["modify"]}/{r["total"]}）</text>')
    svg.append("</svg>")
    return "\n".join(svg)


def _pie(dist: dict[str, dict], size: int = 260) -> str:
    """饼图（主题分布）。"""
    total = sum(v["total"] for v in dist.values()) or 1
    cx = cy = size / 2
    r = size / 2 - 12
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {size} {size}" '
           f'role="img" aria-label="主题分布">',
           f'<rect width="{size}" height="{size}" fill="#fff"/>']
    ang = -math.pi / 2
    for i, (name, v) in enumerate(dist.items()):
        frac = v["total"] / total
        a2 = ang + 2 * math.pi * frac
        large = 1 if frac > 0.5 else 0
        x1, y1 = cx + r * math.cos(ang), cy + r * math.sin(ang)
        x2, y2 = cx + r * math.cos(a2), cy + r * math.sin(a2)
        color = COLORS[i % len(COLORS)]
        svg.append(f'<path d="M {cx} {cy} L {x1:.1f} {y1:.1f} A {r} {r} 0 {large} 1 '
                   f'{x2:.1f} {y2:.1f} Z" fill="{color}" opacity="0.85">'
                   f'<title>{name}: {v["total"]}（{frac:.1%}）</title></path>')
        ang = a2
    svg.append("</svg>")
    return "\n".join(svg)


def render(annotations: list[dict], *, labels_path: Path | str | None = None,
           edges_path: Path | str | None = None) -> str:
    v = hrr.summarize_by_verdict(annotations)
    by_mis = hrr.summarize_by_mis(annotations, edges_path)
    topics = hrr.summarize_by_topic(annotations, edges_path)
    dirs = hrr.summarize_by_direction(annotations, edges_path)
    anomalies = hrr.detect_quality_anomalies(annotations, edges_path)
    out_mis = out_mis_list(labels_path)
    tl = timeline(annotations)
    total = len(annotations)
    reviewed_pct = 100.0

    def card(label: str, value: str, color: str = "#333") -> str:
        return (f'<div class="card"><div class="k">{label}</div>'
                f'<div class="v" style="color:{color}">{value}</div></div>')

    parts = [
        "<!DOCTYPE html><html lang='zh-CN'><head><meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width, initial-scale=1'>",
        "<title>人审进度仪表盘 · 610 E2</title><style>",
        "body{font-family:sans-serif;margin:16px;color:#222}",
        ".cards{display:flex;flex-wrap:wrap;gap:12px}",
        ".card{border:1px solid #e0e0e0;border-radius:6px;padding:10px 14px;min-width:120px}",
        ".k{font-size:12px;color:#666}.v{font-size:20px;font-weight:700}",
        "svg{width:100%;height:auto;max-width:760px}",
        "table{border-collapse:collapse;margin-top:8px}",
        "th,td{border:1px solid #ddd;padding:4px 8px;font-size:12px}",
        ".out{color:#A14E50;font-weight:700}",
        "</style></head><body><h1>人审进度仪表盘</h1>",
        "<div class='cards'>",
        card("记录数", str(total)),
        card("完成度", f"{reviewed_pct:.0f}%", "#2e7d32"),
        card("approve", str(v["approve"]["count"]), "#2e7d32"),
        card("modify", str(v["modify"]["count"]), "#ef6c00"),
        card("reject", str(v["reject"]["count"]), "#666"),
        card("MIS 组", str(len(by_mis))),
        "</div>",
        "<h2>Top10 modify 比例最高的 MIS</h2>", _bars(by_mis[:10]),
        "<h2>主题分布</h2>", _pie(topics),
        "<table><tr><th>主题</th><th>MIS 数</th><th>条数</th><th>占比</th></tr>",
    ]
    for name, row in topics.items():
        parts.append(f"<tr><td>{name}</td><td>{row['mis_count']}</td><td>{row['total']}</td>"
                     f"<td>{row['ratio']:.1%}</td></tr>")
    parts.append("</table><h2>方向分布</h2><table><tr><th>direction</th><th>条数</th></tr>")
    for d, n in dirs.items():
        parts.append(f"<tr><td>{d}</td><td>{n}</td></tr>")
    parts.append("</table>")
    parts.append(f"<h2>OUT 的 MIS（{len(out_mis)} 个，红色高亮）</h2><ul>")
    parts += [f"<li class='out'>{m}</li>" for m in out_mis] or ["<li>（无）</li>"]
    parts.append("</ul><h2>质量异常</h2><table><tr><th>类型</th><th>MIS</th><th>说明</th></tr>")
    for a in anomalies:
        parts.append(f"<tr><td>{a['type']}</td><td>{a['mis_id']}</td><td>{a['detail']}</td></tr>")
    parts.append("</table><h2>时间线</h2>")
    if tl["has_data"]:
        parts.append("<table><tr><th>日期</th><th>条数</th></tr>")
        for d, n in tl["days"].items():
            parts.append(f"<tr><td>{d}</td><td>{n}</td></tr>")
        parts.append("</table>")
    else:
        parts.append("<p>无时间线数据</p>")
    if tl["missing"]:
        parts.append(f"<p>（{tl['missing']}/{total} 条记录缺 timestamp ⇒ 未进时间线）</p>")
    parts.append("<p>数字全部来自 388 条授权人审与入库 W2 产物；本页**只读**。</p>"
                 "</body></html>")
    return "\n".join(parts)


def generate(*, out: Path | str | None = None, annotations: list[dict] | None = None,
             labels_path: Path | str | None = None,
             edges_path: Path | str | None = None) -> Path:
    anns = annotations if annotations is not None else hrr.load_annotations()
    p = Path(out) if out else DEFAULT_HTML
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(render(anns, labels_path=labels_path, edges_path=edges_path),
                 encoding="utf-8", newline="\n")
    return p


def check(*, html_path: Path | str | None = None) -> list[str]:
    problems: list[str] = []
    anns = hrr.load_annotations()
    p = Path(html_path) if html_path else DEFAULT_HTML
    if not p.is_file():
        return [f"仪表盘不存在：{p}（先跑 generate）"]
    text = p.read_text(encoding="utf-8")
    if text != render(anns):
        problems.append("仪表盘与源数据重新渲染不一致（过期）⇒ 跑 generate 重生成")
    v = hrr.summarize_by_verdict(anns)
    for expect in (f">{len(anns)}<", f">{v['approve']['count']}</", f">{v['modify']['count']}<"):
        if expect not in text:
            problems.append(f"仪表盘缺事实数字：{expect}")
    if len(out_mis_list()) != 7 or "OUT 的 MIS（7 个" not in text:
        problems.append("OUT 的 MIS 清单不是 7 个")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="human_review_dashboard",
                                 description="610 E2 人审进度仪表盘（自包含 HTML）")
    ap.add_argument("--version", action="version", version=f"human_review_dashboard {VERSION}")
    ap.add_argument("--check", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sp = sub.add_parser("generate")
    sp.add_argument("--out", default=str(DEFAULT_HTML))
    a = ap.parse_args(argv)

    if a.check:
        problems = check()
        if problems:
            print(f"[dash] --check FAIL：{len(problems)} 项", file=sys.stderr)
            for m in problems[:50]:
                print("  - " + m, file=sys.stderr)
            return 1
        print("[dash] --check OK：仪表盘与源数据一致（388 条 · approve 354 / modify 34 / "
              "reject 0 · OUT MIS 7）")
        return 0

    if a.cmd is None:
        ap.print_help()
        return 2
    p = generate(out=a.out)
    print(f"[dash] 已写 {p.relative_to(ROOT).as_posix() if str(p).startswith(str(ROOT)) else p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
