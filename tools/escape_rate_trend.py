"""610 E1 · 逃逸率收敛曲线（v1→v7 + C-P95 误差带 + **尺子变更史**标注）。

三条纪律（否则这张图会被读成"进步曲线"）：

  1. **数字全部读自基线文件** `data/mutation/full_baseline_v{1..7}.json`（谁的尺子谁自证）；
     区间用 **Clopper-Pearson 精确法**（复用 609 E1 的 `metrics_honesty`，**不引 scipy**）；
  2. **尺子变更史必须显形**：`judged` / `n_a` / `equivalent` 字段的出现与变化都是"尺子变了"的
     可测信号 ⇒ 图上画竖线 + 标注；旁注照抄 `data/metrics.jsonl` 里各版本的 `note`（权威叙述）；
  3. 图注必须写"**v1→v5 是尺子变更史，不是同一量的时间序列**"——不许把连点当成收敛证据。

纯 SVG 自包含 HTML（**不引 ECharts/CDN**：图要在离线评审现场能打开）。

CLI：
    generate [--out FILE]    0 ok
    stats [--json]           0 ok
    --check                  0 v7 数字与基线一致 / 1 破
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import metrics_honesty as mh  # noqa: E402  （C-P 精确区间：单一实现，别处不许重写）

VERSION = "1.0"
BASELINE_DIR = ROOT / "data" / "mutation"
DEFAULT_HTML = ROOT / "data" / "escape_rate_trend.html"
METRICS = ROOT / "data" / "metrics.jsonl"


def load_baselines(path_dir: Path | str | None = None) -> list[dict]:
    """加载 v1…v7；字段缺失（如 v1–v4 无 `equivalent`）⇒ 记 `None` 并**标注数据缺失**。"""
    d = Path(path_dir) if path_dir else BASELINE_DIR
    out: list[dict] = []
    for i in range(1, 8):
        f = d / f"full_baseline_v{i}.json"
        if not f.is_file():
            out.append({"version": f"v{i}", "missing": True,
                        "note": f"数据缺失：{f.name} 不存在"})
            continue
        doc = json.loads(f.read_text(encoding="utf-8"))
        escaped = doc.get("escaped")
        judged = (doc.get("rates") or {}).get("judged")
        if judged is None and isinstance(doc.get("blocked"), int) and isinstance(escaped, int):
            judged = doc["blocked"] + escaped
        out.append({"version": f"v{i}", "missing": False,
                    "variants": doc.get("variants"), "blocked": doc.get("blocked"),
                    "escaped": escaped, "n_a": doc.get("n_a"),
                    "equivalent": doc.get("equivalent"), "judgeable": judged,
                    "strict_blocked": doc.get("strict_blocked"),
                    "file": f.relative_to(ROOT).as_posix()})
    return out


def compute_cp95(escaped: int, judgeable: int, conf: float = 0.95) -> tuple[float, float]:
    """Clopper-Pearson 双侧 95% 区间（**复用 609 E1 的实现**）。"""
    return mh.cp_lower(judgeable, escaped, conf), mh.cp_upper(judgeable, escaped, conf)


def enrich_with_intervals(rows: list[dict]) -> list[dict]:
    for r in rows:
        if r.get("missing") or not r.get("judgeable"):
            r["escape_rate"] = None
            r["cp95_lower"] = r["cp95_upper"] = None
            continue
        r["escape_rate"] = r["escaped"] / r["judgeable"]
        r["cp95_lower"], r["cp95_upper"] = compute_cp95(r["escaped"], r["judgeable"])
    return rows


def history_notes() -> dict[str, str]:
    """从 metrics.jsonl 取各版本 note（权威叙述；取不到 ⇒ 空）。"""
    try:
        doc = mh.load_metrics(METRICS)
    except SystemExit:
        return {}
    return {str(h.get("version") or h.get("baseline_version")): str(h.get("note") or "")
            for h in mh.convergence_curve(doc)}


def detect_ruler_changes(rows: list[dict], *, notes: dict[str, str] | None = None) -> list[dict]:
    """**可测信号**判定尺子变更：`judged` / `n_a` / `equivalent` 出现或变化 ⇒ 记一条。

    叙述优先取 metrics.jsonl 的 note（权威），没有就按信号自动描述（不编故事）。
    """
    notes = notes if notes is not None else history_notes()
    out: list[dict] = []
    prev: dict | None = None
    for r in rows:
        if r.get("missing"):
            prev = None
            continue
        if prev is not None:
            reasons = []
            if r["judgeable"] != prev["judgeable"]:
                reasons.append(f"可判分母 {prev['judgeable']} → {r['judgeable']}")
            if r["n_a"] != prev["n_a"]:
                reasons.append(f"n_a {prev['n_a']} → {r['n_a']}")
            if prev.get("equivalent") is None and r.get("equivalent") is not None:
                reasons.append(f"引入 equivalent 字段（{r['equivalent']} 条）")
            elif r.get("equivalent") != prev.get("equivalent"):
                reasons.append(f"equivalent {prev.get('equivalent')} → {r.get('equivalent')}")
            if reasons:
                out.append({"from": prev["version"], "to": r["version"],
                            "reasons": reasons,
                            "note": notes.get(r["version"], "") or "（无权威 note，仅按可测信号描述）"})
        prev = r
    return out


def _svg(rows: list[dict], changes: list[dict]) -> str:
    W, H = 920, 420
    L, R, T, B = 70, 30, 30, 70
    pts = [r for r in rows if not r.get("missing")]
    rates = [(r["escape_rate"] or 0) for r in pts]
    ups = [(r["cp95_upper"] or 0) for r in pts]
    ymax = max(ups + rates + [1e-6]) * 1.15
    n = len(pts)

    def x(i: int) -> float:
        return L + (W - L - R) * (i / max(n - 1, 1))

    def y(v: float) -> float:
        return H - B - (H - T - B) * (v / ymax if ymax else 0)

    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" role="img" '
           f'aria-label="逃逸率收敛曲线">',
           f'<rect width="{W}" height="{H}" fill="#fff"/>']
    # 轴
    svg.append(f'<line x1="{L}" y1="{H - B}" x2="{W - R}" y2="{H - B}" stroke="#333"/>')
    svg.append(f'<line x1="{L}" y1="{T}" x2="{L}" y2="{H - B}" stroke="#333"/>')
    for frac in (0, 0.25, 0.5, 0.75, 1.0):
        yy = H - B - (H - T - B) * frac
        svg.append(f'<line x1="{L}" y1="{yy:.1f}" x2="{W - R}" y2="{yy:.1f}" '
                   f'stroke="#eee"/>')
        svg.append(f'<text x="{L - 8}" y="{yy + 4:.1f}" font-size="10" text-anchor="end" '
                   f'fill="#666">{ymax * frac * 100:.1f}%</text>')
    # 尺子变更竖线
    idx = {r["version"]: i for i, r in enumerate(pts)}
    for ch in changes:
        if ch["to"] in idx:
            xx = x(idx[ch["to"]])
            svg.append(f'<line x1="{xx:.1f}" y1="{T}" x2="{xx:.1f}" y2="{H - B}" '
                       f'stroke="#c62828" stroke-dasharray="4 3" opacity="0.6"/>')
            svg.append(f'<text x="{xx + 3:.1f}" y="{T + 12}" font-size="10" fill="#c62828">'
                       f'尺子变更 {ch["from"]}→{ch["to"]}</text>')
    # C-P 误差带（每点一根须）+ 折线 + 点
    for i, r in enumerate(pts):
        if r["cp95_upper"] is None:
            continue
        svg.append(f'<line x1="{x(i):.1f}" y1="{y(r["cp95_lower"]):.1f}" x2="{x(i):.1f}" '
                   f'y2="{y(r["cp95_upper"]):.1f}" stroke="#1565c0" stroke-width="1.2" '
                   f'opacity="0.55"/>')
        svg.append(f'<text x="{x(i):.1f}" y="{H - B + 16}" font-size="11" '
                   f'text-anchor="middle" fill="#333">{r["version"]}</text>')
        svg.append(f'<text x="{x(i):.1f}" y="{H - B + 30}" font-size="9" '
                   f'text-anchor="middle" fill="#888">{r["escaped"]}/{r["judgeable"]}</text>')
    poly = " ".join(f"{x(i):.1f},{y(r['escape_rate']):.1f}" for i, r in enumerate(pts)
                    if r["escape_rate"] is not None)
    svg.append(f'<polyline points="{poly}" fill="none" stroke="#2e7d32" stroke-width="1.6"/>')
    for i, r in enumerate(pts):
        if r["escape_rate"] is None:
            continue
        svg.append(f'<circle cx="{x(i):.1f}" cy="{y(r["escape_rate"]):.1f}" r="4" '
                   f'fill="#2e7d32"><title>{r["version"]} 逃逸率 '
                   f'{r["escape_rate"] * 100:.4f}%（C-P95 上界 {r["cp95_upper"] * 100:.4f}%）'
                   f'</title></circle>')
    svg.append("</svg>")
    return "\n".join(svg)


def render_html(rows: list[dict], changes: list[dict]) -> str:
    body = [
        "<!DOCTYPE html><html lang='zh-CN'><head><meta charset='utf-8'>",
        "<meta name='viewport' content='width=device-width, initial-scale=1'>",
        "<title>逃逸率收敛曲线 · 610 E1</title><style>",
        "body{font-family:sans-serif;margin:16px;color:#222}",
        "svg{width:100%;height:auto}table{border-collapse:collapse;margin-top:12px}",
        "th,td{border:1px solid #ddd;padding:4px 8px;font-size:12px}",
        ".warn{color:#c62828;font-weight:700}</style></head><body>",
        "<h1>逃逸率收敛曲线 v1→v7（C-P95 误差带）</h1>",
        "<p class='warn'>v1→v5 是**尺子变更史**，不是同一量的时间序列 ⇒ 不得据此宣称收敛。</p>",
        _svg(rows, changes),
        "<h2>逐版本</h2><table><tr><th>版本</th><th>escaped</th><th>可判</th><th>n_a</th>",
        "<th>equivalent</th><th>点估计</th><th>C-P95 上界</th></tr>",
    ]
    for r in rows:
        if r.get("missing"):
            body.append(f"<tr><td>{r['version']}</td><td colspan='6'>数据缺失</td></tr>")
            continue
        er = "—" if r["escape_rate"] is None else f"{r['escape_rate'] * 100:.4f}%"
        up = "—" if r["cp95_upper"] is None else f"{r['cp95_upper'] * 100:.4f}%"
        body.append(f"<tr><td>{r['version']}</td><td>{r['escaped']}</td><td>{r['judgeable']}</td>"
                    f"<td>{r['n_a']}</td><td>{r['equivalent']}</td><td>{er}</td><td>{up}</td></tr>")
    body.append("</table><h2>尺子变更点</h2><ul>")
    for ch in changes:
        body.append(f"<li><b>{ch['from']}→{ch['to']}</b>：{'；'.join(ch['reasons'])}"
                    f"<br><span style='color:#666'>{ch['note']}</span></li>")
    body.append("</ul><p>区间算法：Clopper-Pearson 精确双侧 95%（无 scipy）；"
                "数字全部读自 data/mutation/full_baseline_v*.json。</p></body></html>")
    return "\n".join(body)


def trend(*, baselines_dir: Path | str | None = None) -> dict:
    rows = enrich_with_intervals(load_baselines(baselines_dir))
    changes = detect_ruler_changes(rows)
    return {"baselines": rows, "ruler_changes": changes,
            "note": "v1→v5 为口径修正（尺子变更），不得声称单调收敛"}


def check(baselines_dir: Path | str | None = None) -> list[str]:
    problems: list[str] = []
    t = trend(baselines_dir=baselines_dir)
    rows = {r["version"]: r for r in t["baselines"]}
    if len(t["baselines"]) != 7:
        problems.append(f"应有 v1…v7 共 7 个版本（实测 {len(t['baselines'])}）")
    v7 = rows.get("v7", {})
    if v7.get("escaped") != 1 or v7.get("judgeable") != 1406:
        problems.append(f"v7 应为 1/1406（实测 {v7.get('escaped')}/{v7.get('judgeable')}）")
    up = v7.get("cp95_upper")
    if up is None or abs(up - 0.003956325504751501) > 1e-9:
        problems.append(f"v7 C-P95 上界与冻结值不符：{up}")
    if len(t["ruler_changes"]) < 3:
        problems.append(f"尺子变更点应 ≥3（实测 {len(t['ruler_changes'])}）")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="escape_rate_trend",
                                 description="610 E1 逃逸率收敛曲线（C-P95 + 尺子变更史）")
    ap.add_argument("--version", action="version", version=f"escape_rate_trend {VERSION}")
    ap.add_argument("--baselines", default=None)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    sp = sub.add_parser("generate")
    sp.add_argument("--out", default=str(DEFAULT_HTML))
    sp = sub.add_parser("stats")
    sp.add_argument("--json", action="store_true", dest="json_sub")
    a = ap.parse_args(argv)
    if getattr(a, "json_sub", False):
        a.json = True

    if a.check:
        problems = check(a.baselines)
        if problems:
            print(f"[trend] --check FAIL：{len(problems)} 项", file=sys.stderr)
            for m in problems[:50]:
                print("  - " + m, file=sys.stderr)
            return 1
        print("[trend] --check OK：v1…v7 齐备 · v7 = 1/1406 · C-P95 上界 0.3956% · "
              "尺子变更点 ≥3")
        return 0

    if a.cmd is None:
        ap.print_help()
        return 2

    t = trend(baselines_dir=a.baselines)
    if a.cmd == "stats":
        print(json.dumps(t, ensure_ascii=False, indent=1) if a.json else
              "\n".join(f"{r['version']}: {r.get('escaped')}/{r.get('judgeable')}"
                        f" cp95_upper={r.get('cp95_upper')}" for r in t["baselines"]))
        return 0
    p = Path(a.out)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(render_html(t["baselines"], t["ruler_changes"]), encoding="utf-8", newline="\n")
    print(f"[trend] 已写 {p.relative_to(ROOT).as_posix() if str(p).startswith(str(ROOT)) else p}"
          f"（{len(t['baselines'])} 个版本 · 尺子变更 {len(t['ruler_changes'])} 处）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
