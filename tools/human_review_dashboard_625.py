"""625 D2 · 人审可视化（深色科技风，纯静态 HTML/CSS/JS，无外部依赖）

复用 624 E2 的逐条复核清单模型（`human_review_item_by_item_generator_624.generate`），
渲染一个**深色科技风**仪表盘：覆盖统计 + 歧义度分布（SVG 条形图）+ 可筛选的逐条清单表。

**只读**：读取 annotations/Authority 与 624 E2 生成器模型；**不改任何日志、不执行判决**。
铁律：必有 `--check`。
"""
from __future__ import annotations

import argparse
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

import human_review_item_by_item_generator_624 as HG  # noqa: E402

AUTH = os.path.join(ROOT, "data", "authority", "authority_log.jsonl")


def load_jsonl(path: str) -> list[dict]:
    out: list[dict] = []
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def authority_stats() -> dict:
    log = load_jsonl(AUTH)
    by_power: dict[str, int] = {}
    for d in log:
        p = str((d.get("power") or d.get("decided_power") or "UNKNOWN")).upper()
        by_power[p] = by_power.get(p, 0) + 1
    return {"entries": len(log), "by_power": by_power}


def build(items: list[dict]) -> dict:
    amb = {"high": 0, "medium": 0, "low": 0}
    rec: dict[str, int] = {}
    for it in items:
        amb[it["ambiguity"]] = amb.get(it["ambiguity"], 0) + 1
        r = it.get("recommended", "")
        rec[r] = rec.get(r, 0) + 1
    return {"items": items, "ambiguity": amb, "recommend": rec,
            "total": len(items), "auth": authority_stats()}


def _bar(label: str, value: int, maximum: int, color: str) -> str:
    pct = (value / maximum * 100) if maximum else 0
    return (f'<div class="row"><span class="lab">{label}</span>'
            f'<div class="track"><div class="fill" style="width:{pct:.1f}%;background:{color}"></div>'
            f'</div><span class="val">{value}</span></div>')


def render(d: dict) -> str:
    maxv = max(list(d["ambiguity"].values()) + [1])
    colors = {"high": "#ff4d6d", "medium": "#ffb020", "low": "#3ad6c5"}
    bars = "".join(_bar(k, d["ambiguity"][k], maxv, colors[k]) for k in ("high", "medium", "low"))
    rows = ""
    for it in d["items"]:
        rows += (f'<tr data-amb="{it["ambiguity"]}">'
                 f'<td>{it["edge_id"]}</td><td>{it["atom"]}</td>'
                 f'<td><span class="pill amb-{it["ambiguity"]}">{it["ambiguity"]}</span></td>'
                 f'<td>{it.get("recommended", "")}</td>'
                 f'<td class="reason">{it.get("reason", "")}</td></tr>')
    return f"""<!doctype html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>人审可视化 · 阙疑深色科技风</title>
<style>
:root{{--bg:#0a0e1a;--panel:#121a2e;--line:#1f2b45;--txt:#c9d4ee;--dim:#7c89a8;--accent:#3ad6c5}}
*{{box-sizing:border-box}}
body{{margin:0;background:radial-gradient(1200px 600px at 70% -10%,#142042,#0a0e1a);
color:var(--txt);font:14px/1.5 'Segoe UI',system-ui,sans-serif;padding:28px}}
h1{{font-weight:600;letter-spacing:.04em;margin:0 0 4px}}
.sub{{color:var(--dim);margin-bottom:22px}}
.grid{{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:14px;margin-bottom:26px}}
.kpi{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:16px}}
.kpi .n{{font-size:30px;font-weight:700;color:var(--accent)}}
.kpi .t{{color:var(--dim);font-size:12px;letter-spacing:.05em}}
.card{{background:var(--panel);border:1px solid var(--line);border-radius:12px;padding:18px;margin-bottom:22px}}
.card h2{{margin:0 0 14px;font-size:15px;font-weight:600}}
.row{{display:flex;align-items:center;gap:10px;margin:8px 0}}
.lab{{width:64px;color:var(--dim)}}
.track{{flex:1;height:14px;background:#0c1322;border:1px solid var(--line);border-radius:8px;overflow:hidden}}
.fill{{height:100%;border-radius:8px;box-shadow:0 0 12px currentColor}}
.val{{width:40px;text-align:right;font-variant-numeric:tabular-nums}}
table{{width:100%;border-collapse:collapse;font-size:13px}}
th,td{{text-align:left;padding:9px 10px;border-bottom:1px solid var(--line)}}
th{{color:var(--dim);font-weight:600;position:sticky;top:0;background:var(--panel)}}
.reason{{color:var(--dim)}}
.pill{{padding:2px 9px;border-radius:999px;font-size:11px;border:1px solid var(--line)}}
.amb-high{{color:#ff4d6d;border-color:#ff4d6d}}
.amb-medium{{color:#ffb020;border-color:#ffb020}}
.amb-low{{color:#3ad6c5;border-color:#3ad6c5}}
.filters{{margin-bottom:12px}}
.filters button{{background:#0c1322;color:var(--txt);border:1px solid var(--line);
border-radius:8px;padding:5px 12px;margin-right:8px;cursor:pointer}}
.filters button:hover{{border-color:var(--accent)}}
</style></head><body>
<h1>人审可视化仪表盘</h1>
<div class="sub">625 D2 · 深色科技风 · 复用 624 E2 逐条复核模型 · 只读不判决</div>
<div class="grid">
<div class="kpi"><div class="n">{d['total']}</div><div class="t">复核清单总数</div></div>
<div class="kpi"><div class="n">{d['ambiguity']['high']}</div><div class="t">高歧义</div></div>
<div class="kpi"><div class="n">{d['ambiguity']['medium']}</div><div class="t">中歧义</div></div>
<div class="kpi"><div class="n">{d['ambiguity']['low']}</div><div class="t">低歧义</div></div>
<div class="kpi"><div class="n">{d['auth']['entries']}</div><div class="t">Authority 日志条数</div></div>
</div>
<div class="card"><h2>歧义度分布</h2>{bars}</div>
<div class="card"><h2>逐条清单（可筛选）</h2>
<div class="filters"><button onclick="f('all')">全部</button>
<button onclick="f('high')">高</button><button onclick="f('medium')">中</button>
<button onclick="f('low')">低</button></div>
<table id="t"><thead><tr><th>边ID</th><th>原子</th><th>歧义度</th><th>推荐判决</th><th>理由</th></tr></thead>
<tbody>{rows}</tbody></table></div>
<script>
function f(a){{const r=document.querySelectorAll('#t tbody tr');
r.forEach(tr=>{{tr.style.display=(a==='all'||tr.dataset.amb===a)?'':'none'}})}}
</script>
</body></html>"""


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    edges = HG.load_edges(HG.SYNCED)
    chk("synced annotations 可读", isinstance(edges, list))
    items = HG.generate(edges)
    chk("生成 ≥80 条复核项（624 E2 上限）", len(items) >= 80)
    d = build(items)
    html = render(d)
    chk("HTML 含关键元素", "<!doctype html>" in html and "人审可视化" in html)
    chk("含筛选脚本", "function f(" in html)
    chk("权威日志可读", d["auth"]["entries"] > 0)
    print(f"D2 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="625 D2 人审深色科技风可视化")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--out", default=os.path.join(ROOT, "data", "human_review_dashboard_625.html"))
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    edges = HG.load_edges(HG.SYNCED)
    items = HG.generate(edges)
    html = render(build(items))
    with open(args.out, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    print(f"written {args.out}  (items={len(items)})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
