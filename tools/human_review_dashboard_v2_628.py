"""628 C1 · 人审深色科技风仪表盘 v2（自包含 HTML，离线可开，无外部 CDN）

在 625 D2（v1 纯静态条形图 + 表格）基础上深化视觉：深色底 + 玻璃拟态卡片 +
青/紫霓虹强调 + 纯 CSS 粒子背景 + CSS 3D 论证图。

6 个数据模块（全部读原始数据文件，**纯标准库**，不 import 626 工具）：
1. 人审进度环形图（唯一审查项 已审/待审/独立盲审）
2. 歧义度热力图（93 unique 按歧义度降序）
3. review_method 分布饼图（DecisionEvent 口径）
4. W2 论证图 3D（121 节点，IN/OUT/UNDEC 三色）
5. 独立人类确认强度仪表盘（0 / 93 目标）
6. 他验三件套状态卡片（独立验证者 / VSA 凭证 / 透明日志，自算哈希链）

**只读**：不改任何日志、不执行任何判决。必有 `--check`。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import sys
import time
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

REVIEW_LEDGER = os.path.join(ROOT, "data", "review_item_ledger.jsonl")
DE_LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
GROUNDED = os.path.join(ROOT, "data", "grounded_labels_w2.json")
VSA_DIR = os.path.join(ROOT, "data", "vsa")
LOG = os.path.join(ROOT, "data", "transparency_log.jsonl")
VERIFIER = os.path.join(HERE, "independent_verifier_628.py")
OUT_HTML = os.path.join(ROOT, "data", "human_review_dashboard_v2.html")
OUT_DESIGN = os.path.join(ROOT, "data", "human_review_dashboard_v2_design_628.md")

EXPECT_UNIQUE = 93


def _expect_w2() -> dict:
    """640b A1：W2 期望值取单一权威源（不再写死 114/7）。"""
    try:
        import w2_authority_640b as A
        a = A.artifact_summary()
        return {"IN": a["IN"], "OUT": a["OUT"], "UNDEC": a["UNDEC"]}
    except Exception:  # noqa: BLE001
        return {"IN": 114, "OUT": 7, "UNDEC": 0}        # 回退：历史登记口径


EXPECT_W2 = _expect_w2()


def _jl(path: str) -> list[dict]:
    out: list[dict] = []
    if not os.path.exists(path):
        return out
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                out.append(json.loads(line))
    return out


# ── 数据聚合（纯标准库） ──────────────────────────────────────────

def method_distribution(events: list[dict]) -> dict[str, int]:
    out: dict[str, int] = {}
    for e in events:
        m = str(e.get("review_method") or "UNKNOWN")
        out[m] = out.get(m, 0) + 1
    return out


def blind_review_count(events: list[dict]) -> int:
    return sum(1 for e in events if str(e.get("blind_review_id") or "").strip())


def w2_nodes() -> list[dict]:
    g = json.load(open(GROUNDED, encoding="utf-8"))
    return [{"id": k, "label": str(v.get("label", "UNDEC")),
             "cred": int(v.get("credibility", 0) or 0)}
            for k, v in g["nodes"].items()]


def log_state() -> dict:
    """自算透明日志哈希链（不 import B3）。"""
    entries = _jl(LOG)
    prev, broken = "GENESIS", False
    for e in entries:
        payload = {k: v for k, v in e.items() if k != "entry_hash"}
        blob = json.dumps(payload, ensure_ascii=False, sort_keys=True).encode("utf-8")
        if hashlib.sha256(blob).hexdigest() != e.get("entry_hash") \
                or e.get("prev_log_hash") != prev:
            broken = True
        prev = str(e.get("entry_hash"))
    return {"entries": len(entries), "chain_valid": not broken}


def attestation_status() -> dict:
    vsa = (sorted(f for f in os.listdir(VSA_DIR)
                  if f.startswith("attestation_") and f.endswith(".json"))
           if os.path.isdir(VSA_DIR) else [])
    return {"verifier_present": os.path.exists(VERIFIER), "vsa_count": len(vsa),
            "latest_vsa": vsa[-1] if vsa else None, "log": log_state()}


def build() -> dict:
    items = _jl(REVIEW_LEDGER)
    events = _jl(DE_LEDGER)
    by_status: dict[str, int] = {}
    for it in items:
        s = str(it.get("status") or "unknown")
        by_status[s] = by_status.get(s, 0) + 1
    nodes = w2_nodes()
    labels = {"IN": 0, "OUT": 0, "UNDEC": 0}
    for n in nodes:
        if n["label"] in labels:
            labels[n["label"]] += 1
    pivots = sorted(items, key=lambda i: -float(i.get("ambiguity_score", 0)))
    return {
        "generated_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "review": {"unique": len({str(i.get("target_id")) for i in items}),
                   "records": len(items), "by_status": by_status,
                   "pending": by_status.get("pending", 0),
                   "decided": sum(v for k, v in by_status.items() if k != "pending")},
        "methods": method_distribution(events),
        "blind_count": blind_review_count(events),
        "events": len(events),
        "ambiguity": {
            "high": sum(1 for i in pivots if float(i.get("ambiguity_score", 0)) >= 0.8),
            "medium": sum(1 for i in pivots if 0.5 <= float(i.get("ambiguity_score", 0)) < 0.8),
            "low": sum(1 for i in pivots if float(i.get("ambiguity_score", 0)) < 0.5)},
        "items": [{"id": str(i.get("target_id")), "score": float(i.get("ambiguity_score", 0)),
                   "status": str(i.get("status")),
                   "proof": str(i.get("symmetry_proof_id") or "")} for i in pivots],
        "w2": {"nodes": nodes, "labels": labels},
        "attest": attestation_status(),
    }


# ── 样式与脚本（普通字符串：无需 f-string 双花括号转义） ──────────

CSS = """
:root{--bg:#0a0e1a;--panel:rgba(20,28,48,.62);--line:rgba(90,130,200,.22);--txt:#c9d4ee;
--dim:#7c89a8;--cyan:#3ad6c5;--violet:#8b6cff;--rose:#ff4d6d;--amber:#ffb020}
*{box-sizing:border-box}
html,body{margin:0;background:#0a0e1a;color:var(--txt);
font:14px/1.55 'Segoe UI',system-ui,-apple-system,"Microsoft YaHei",sans-serif}
body{padding:30px 26px 60px;position:relative;overflow-x:hidden;
background:radial-gradient(1100px 620px at 72% -12%,#16224a 0%,#0a0e1a 58%),
radial-gradient(900px 520px at 8% 108%,#241a4a 0%,rgba(10,14,26,0) 60%)}
.particles{position:fixed;inset:0;pointer-events:none;z-index:0}
.particles i{position:absolute;width:2px;height:2px;border-radius:50%;background:var(--cyan);
opacity:.5;animation:float 14s linear infinite}
@keyframes float{0%{transform:translateY(0) scale(.7);opacity:0}12%{opacity:.55}
88%{opacity:.55}100%{transform:translateY(-120vh) scale(1.15);opacity:0}}
.wrap{position:relative;z-index:1;max-width:1400px;margin:0 auto}
h1{font-weight:600;letter-spacing:.05em;margin:0 0 6px;font-size:26px}
h1 span{background:linear-gradient(92deg,var(--cyan),var(--violet));
-webkit-background-clip:text;background-clip:text;color:transparent}
.sub{color:var(--dim);margin-bottom:24px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(170px,1fr));gap:14px;
margin-bottom:22px}
.kpi{background:var(--panel);border:1px solid var(--line);border-radius:14px;padding:16px;
backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);
box-shadow:0 8px 28px rgba(0,0,0,.38),inset 0 1px 0 rgba(255,255,255,.05)}
.kpi .n{font-size:30px;font-weight:700;color:var(--cyan);font-variant-numeric:tabular-nums;
text-shadow:0 0 18px rgba(58,214,197,.35)}
.kpi .t{color:var(--dim);font-size:12px;letter-spacing:.06em;text-transform:uppercase}
.cols{display:grid;grid-template-columns:repeat(auto-fit,minmax(330px,1fr));gap:18px;
margin-bottom:18px}
.card{background:var(--panel);border:1px solid var(--line);border-radius:16px;padding:18px;
backdrop-filter:blur(10px);-webkit-backdrop-filter:blur(10px);
box-shadow:0 10px 34px rgba(0,0,0,.4),inset 0 1px 0 rgba(255,255,255,.05)}
.card h2{margin:0 0 14px;font-size:15px;font-weight:600;letter-spacing:.04em}
.card h2 em{color:var(--dim);font-style:normal;font-size:12px;font-weight:400;margin-left:6px}
.ring{display:flex;align-items:center;gap:20px;flex-wrap:wrap}
.ring svg{filter:drop-shadow(0 0 10px rgba(58,214,197,.32))}
.legend{display:flex;flex-direction:column;gap:8px;font-size:13px}
.legend b{font-variant-numeric:tabular-nums}
.dot{display:inline-block;width:9px;height:9px;border-radius:50%;margin-right:8px}
.heat{display:flex;flex-wrap:wrap;gap:4px}
.heat i{width:16px;height:16px;border-radius:4px;display:block;transition:transform .16s}
.heat i:hover{transform:scale(1.55)}
.piewrap{position:relative;width:190px;height:190px;margin:0 auto}
.pie{width:190px;height:190px;border-radius:50%;
box-shadow:0 0 26px rgba(139,108,255,.28) inset,0 8px 26px rgba(0,0,0,.45)}
.pie-hole{position:absolute;inset:31%;border-radius:50%;background:#0e1424;
display:flex;align-items:center;justify-content:center;font-size:20px;font-weight:700;
color:var(--violet)}
.scene{height:330px;perspective:900px;overflow:hidden;border-radius:14px;
background:radial-gradient(closest-side,rgba(58,214,197,.09),rgba(10,14,26,0))}
.stage{position:relative;width:100%;height:100%;transform-style:preserve-3d;
animation:spin 46s linear infinite}
@keyframes spin{from{transform:rotateX(-16deg) rotateY(0)}to{transform:rotateX(-16deg) rotateY(360deg)}}
.node{position:absolute;left:50%;top:50%;width:15px;height:15px;border-radius:50%;
margin:-7px 0 0 -7px;cursor:pointer;background:currentColor;box-shadow:0 0 12px currentColor;
transform:translate3d(var(--x),var(--y),var(--z)) scale(var(--s,1))}
.node.in{color:var(--cyan)}.node.out{color:var(--rose)}.node.undec{color:var(--dim)}
.node:hover{--s:2.1;z-index:9}
.gauge{position:relative;width:230px;height:126px;margin:4px auto 0;overflow:hidden}
.gauge svg{position:absolute;inset:0}
.gnum{position:absolute;left:0;right:0;bottom:6px;text-align:center;font-size:32px;
font-weight:700;color:var(--amber);text-shadow:0 0 20px rgba(255,176,32,.4)}
.gtgt{text-align:center;color:var(--dim);font-size:12px;margin-top:4px}
.tri{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:12px}
.tri div{border:1px solid var(--line);border-radius:12px;padding:12px;background:rgba(10,16,32,.5)}
.tri .s{font-size:12px;color:var(--dim);letter-spacing:.05em}
.tri .v{font-size:16px;font-weight:600;margin-top:6px}
.ok{color:var(--cyan)}.warn{color:var(--amber)}.bad{color:var(--rose)}
table{width:100%;border-collapse:collapse;font-size:12.5px}
th,td{text-align:left;padding:8px 9px;border-bottom:1px solid var(--line);
white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:260px}
th{color:var(--dim);font-weight:600}
@media(max-width:680px){body{padding:18px 12px 40px}.scene{height:250px}}
"""

JS = """
(function(){
  var box=document.querySelector('.particles');
  for(var i=0;i<38;i++){
    var s=document.createElement('i');
    s.style.left=(Math.random()*100)+'vw';
    s.style.top=(60+Math.random()*46)+'vh';
    s.style.animationDelay=(-Math.random()*14)+'s';
    s.style.animationDuration=(10+Math.random()*10)+'s';
    if(i%3===0){s.style.background='#8b6cff';}
    box.appendChild(s);
  }
})();
"""

# ── 渲染 ─────────────────────────────────────────────────────────

def _kpis(d: dict) -> str:
    cards = [
        (str(d["review"]["unique"]), "唯一审查项"),
        (str(d["review"]["pending"]), "待审"),
        (str(d["blind_count"]), "独立盲审"),
        (str(d["w2"]["labels"]["IN"]), "W2 IN"),
        (str(d["w2"]["labels"]["OUT"]), "W2 OUT"),
        (str(d["events"]), "决定事件"),
        (str(d["ambiguity"]["high"]), "高歧义"),
    ]
    inner = "".join(f'<div class="kpi"><div class="n">{v}</div><div class="t">{t}</div></div>'
                    for v, t in cards)
    return f'<div class="grid">{inner}</div>'


def _ring(d: dict) -> str:
    rv = d["review"]
    total = max(rv["unique"], 1)
    seg = [("#3ad6c5", rv["decided"] / total, f'{rv["decided"]} 已审'),
           ("#8b6cff", d["blind_count"] / total, f'{d["blind_count"]} 独立盲审'),
           ("#ff4d6d", rv["pending"] / total, f'{rv["pending"]} 待审')]
    circ = 2 * math.pi * 54
    arcs, off = "", 0.0
    for color, frac, _lab in seg:
        ln = max(frac, 0.0) * circ
        arcs += (f'<circle cx="60" cy="60" r="54" fill="none" stroke="{color}" '
                 f'stroke-width="13" stroke-dasharray="{ln:.2f} {circ - ln:.2f}" '
                 f'stroke-dashoffset="{-off:.2f}" transform="rotate(-90 60 60)" '
                 f'opacity="0.92"/>')
        off += ln
    legend = "".join(f'<div><span class="dot" style="background:{c}"></span>{lab}</div>'
                     for c, _f, lab in seg)
    return (f'<div class="card"><h2>① 人审进度<em>环形图 · 按唯一审查项</em></h2>'
            f'<div class="ring"><svg width="150" height="150" viewBox="0 0 120 120">'
            f'<circle cx="60" cy="60" r="54" fill="none" stroke="rgba(90,130,200,.18)" '
            f'stroke-width="13"/>{arcs}'
            f'<text x="60" y="57" text-anchor="middle" fill="#c9d4ee" font-size="20" '
            f'font-weight="700">{rv["unique"]}</text>'
            f'<text x="60" y="74" text-anchor="middle" fill="#7c89a8" font-size="9">'
            f'UNIQUE ITEMS</text></svg><div class="legend">{legend}'
            f'<div style="color:var(--dim);font-size:12px">记录 {rv["records"]} 条 · '
            f'状态 {json.dumps(rv["by_status"], ensure_ascii=False)}</div>'
            f'</div></div></div>')


def _heat(d: dict) -> str:
    cells = ""
    for it in d["items"]:
        s = min(max(it["score"], 0.0), 1.0)
        color = f'rgba({int(60 + 195 * s)},{int(214 - 150 * s)},{int(197 - 90 * s)},.92)'
        title = (f'{it["id"]} · 歧义 {it["score"]:.2f} · {it["status"]}'
                 + (f' · {it["proof"]}' if it["proof"] else ''))
        cells += f'<i style="background:{color}" title="{title}"></i>'
    amb = d["ambiguity"]
    return (f'<div class="card"><h2>② 歧义度热力图<em>'
            f'{d["review"]["unique"]} 项按歧义度降序</em></h2><div class="heat">{cells}</div>'
            f'<div style="margin-top:12px;color:var(--dim);font-size:12px">'
            f'高(≥0.8) {amb["high"]} · 中(0.5–0.8) {amb["medium"]} · 低(&lt;0.5) {amb["low"]}'
            f' · 越红歧义越高，悬停看明细</div></div>')


def _pie(d: dict) -> str:
    m = d["methods"]
    palette = {"BATCH_AUTH": "#3ad6c5", "MIRROR_DERIVED": "#8b6cff",
               "ITEM_OPEN": "#ffb020", "ITEM_BLIND": "#ff4d6d"}
    total = max(sum(m.values()), 1)
    stops, off, legend = [], 0.0, ""
    for k in sorted(m):
        frac = m[k] / total
        c = palette.get(k, "#5a7ab0")
        stops.append(f'{c} {off * 100:.2f}% {(off + frac) * 100:.2f}%')
        legend += (f'<div><span class="dot" style="background:{c}"></span>{k} '
                   f'<b>{m[k]}</b></div>')
        off += frac
    return (f'<div class="card"><h2>③ review_method 分布<em>DecisionEvent 口径</em></h2>'
            f'<div style="display:flex;gap:18px;align-items:center;flex-wrap:wrap">'
            f'<div class="piewrap"><div class="pie" style="background:conic-gradient('
            f'{",".join(stops)})"></div><div class="pie-hole">{d["events"]}</div></div>'
            f'<div class="legend">{legend}</div></div></div>')


def _sphere(n: int, radius: float = 158.0) -> list[tuple[float, float, float]]:
    """确定性球面分布（黄金角螺旋），保证每次渲染布局一致。"""
    ga = math.pi * (3 - math.sqrt(5))
    pts = []
    for i in range(max(n, 1)):
        y = 1 - (i / max(n - 1, 1)) * 2
        r = math.sqrt(max(1 - y * y, 0.0))
        th = ga * i
        pts.append((math.cos(th) * r * radius, y * radius * 0.72,
                    math.sin(th) * r * radius * 0.55))
    return pts


def _w2_3d(d: dict) -> str:
    nodes = d["w2"]["nodes"]
    pts = _sphere(len(nodes))
    cells = ""
    for nd, (x, y, z) in zip(nodes, pts):
        cls = nd["label"].lower() if nd["label"] in ("IN", "OUT") else "undec"
        title = f'{nd["id"]} · {nd["label"]} · cred {nd["cred"]}'
        cells += (f'<div class="node {cls}" style="--x:{x:.1f}px;--y:{y:.1f}px;'
                  f'--z:{z:.1f}px" title="{title}"></div>')
    lab = d["w2"]["labels"]
    return (f'<div class="card"><h2>④ W2 论证图 3D<em>{len(nodes)} 节点 · '
            f'CSS 3D 透视旋转</em></h2><div class="scene"><div class="stage">{cells}</div>'
            f'</div><div class="legend" style="flex-direction:row;gap:24px;margin-top:10px">'
            f'<div><span class="dot" style="background:#3ad6c5"></span>IN {lab["IN"]}</div>'
            f'<div><span class="dot" style="background:#ff4d6d"></span>OUT {lab["OUT"]}</div>'
            f'<div><span class="dot" style="background:#7c89a8"></span>UNDEC '
            f'{lab["UNDEC"]}</div></div></div>')


def _gauge(d: dict) -> str:
    """半圆仪表：独立人类确认强度（当前 / 目标 = 唯一审查项数）。"""
    cur = d["blind_count"]
    tgt = max(d["review"]["unique"], 1)
    frac = min(cur / tgt, 1.0)
    arc = 2 * math.pi * 60
    half = arc / 2
    return (f'<div class="card"><h2>⑤ 独立人类确认强度<em>Blind Review 盲审计数</em></h2>'
            f'<div class="gauge"><svg viewBox="0 0 160 90">'
            f'<path d="M20 80 A60 60 0 0 1 140 80" fill="none" '
            f'stroke="rgba(90,130,200,.2)" stroke-width="12" stroke-linecap="round"/>'
            f'<path d="M20 80 A60 60 0 0 1 140 80" fill="none" stroke="#ffb020" '
            f'stroke-width="12" stroke-linecap="round" '
            f'stroke-dasharray="{half * frac:.2f} 999"/>'
            f'</svg><div class="gnum">{cur}</div></div>'
            f'<div class="gtgt">目标 {tgt}（全部唯一审查项经独立人确认）· '
            f'执行真实 Blind Review 需人审者配合（本批只建设工具）</div></div>')


def _attest_card(d: dict) -> str:
    a = d["attest"]
    log = a["log"]
    chain = "完整" if log["chain_valid"] else "断裂"
    items = [
        ("独立验证者", "在位" if a["verifier_present"] else "缺失",
         "ok" if a["verifier_present"] else "bad"),
        ("VSA 凭证", f'{a["vsa_count"]} 张', "ok" if a["vsa_count"] else "warn"),
        ("透明日志", f'{log["entries"]} 条 · 链{chain}', "ok" if log["chain_valid"] else "bad"),
    ]
    inner = "".join(f'<div><div class="s">{s}</div><div class="v {c}">{v}</div></div>'
                    for s, v, c in items)
    return (f'<div class="card"><h2>⑥ 他验三件套状态<em>628 B1–B4</em></h2>'
            f'<div class="tri">{inner}</div></div>')


def _page(d: dict) -> str:
    return "\n".join([
        "<!doctype html>", '<html lang="zh-CN"><head><meta charset="utf-8">',
        '<meta name="viewport" content="width=device-width,initial-scale=1">',
        "<title>人审仪表盘 v2 · 阙疑深色科技风</title>",
        "<style>", CSS, "</style></head><body>",
        '<div class="particles"></div>', '<div class="wrap">',
        '<h1>人审仪表盘 <span>v2</span></h1>',
        f'<div class="sub">628 C1 · 深色科技风 · 玻璃拟态 + 霓虹 + CSS 3D · '
        f'纯标准库只读生成 · {d["generated_at"]}</div>',
        _kpis(d), '<div class="cols">', _ring(d), _pie(d), "</div>",
        _heat(d), _w2_3d(d), '<div class="cols">', _gauge(d), _attest_card(d), "</div>",
        "</div>", "<script>", JS, "</script>", "</body></html>",
    ])


# ── 自检 / CLI ───────────────────────────────────────────────────

def generate() -> str:
    html = _page(build())
    with open(OUT_HTML, "w", encoding="utf-8", newline="\n") as fh:
        fh.write(html)
    return html


def write_design() -> None:
    d = build()
    lines = [
        "# 628 C1 · 人审仪表盘 v2 设计说明", "",
        "## 视觉设计决策", "",
        "- **深色底 `#0a0e1a` + 双径向渐变**：长时间盯人审清单不刺眼，且让霓虹强调色有对比度。",
        "- **玻璃拟态**（`backdrop-filter: blur(10px)` + 半透明面板 + 内高光）：卡片有层次，"
        "信息密度高时也不糊成一片。",
        "- **青(#3ad6c5)/紫(#8b6cff)霓虹**：青=稳定/已确证，紫=结构性/衍生，玫瑰=需注意，琥珀=待办。",
        "- **粒子背景**：38 个纯 CSS 动画光点（JS 只负责撒点，无外部库），暗示\"审计轨迹在持续流动\"。",
        "- **CSS 3D 论证图**：`perspective:900px` + `transform-style:preserve-3d`，"
        "外层 stage 46s 匀速 rotateY，节点用 `translate3d` 落在黄金角球面上，hover 放大 2.1×。",
        "",
        "## 数据模块（6 个）", "",
        "| # | 模块 | 数据源 | 当前值 |",
        "|---|---|---|---|",
        f"| 1 | 人审进度环形图 | `review_item_ledger.jsonl` | 唯一 {d['review']['unique']} · "
        f"待审 {d['review']['pending']} · 独立盲审 {d['blind_count']} |",
        f"| 2 | 歧义度热力图 | `review_item_ledger.jsonl` | 高 {d['ambiguity']['high']} · "
        f"中 {d['ambiguity']['medium']} · 低 {d['ambiguity']['low']} |",
        f"| 3 | review_method 饼图 | `decision_event_v2_ledger.jsonl` | "
        f"{json.dumps(d['methods'], ensure_ascii=False)} |",
        f"| 4 | W2 论证图 3D | `grounded_labels_w2.json` | {len(d['w2']['nodes'])} 节点 · "
        f"IN{d['w2']['labels']['IN']}/OUT{d['w2']['labels']['OUT']}/"
        f"UNDEC{d['w2']['labels']['UNDEC']} |",
        f"| 5 | 独立人类确认强度 | DecisionEvent `blind_review_id` | {d['blind_count']} / "
        f"{d['review']['unique']} |",
        f"| 6 | 他验三件套状态 | `data/vsa/` + `transparency_log.jsonl` | 凭证 "
        f"{d['attest']['vsa_count']} 张 · 日志 {d['attest']['log']['entries']} 条 |",
        "",
        "## 与 v1（625 D2）对比", "",
        "- v1：纯静态深色 + SVG 条形图 + 可筛选表格，无动效、无 3D、无他验状态。",
        "- v2：玻璃拟态 + 霓虹 + 粒子动画 + CSS 3D 论证图 + 环形/饼图/仪表 + 他验三件套状态卡。",
        "- v2 **纯静态自包含**（无 CDN、无网络），双击即可离线打开。",
        "",
        "## 偏差登记（任务书假设 vs 实测）", "",
        "- 任务书写\"人审进度环形图（388 条…）\"：仓库内**无 388 这一口径**（`grep 388 data/` 零命中）。",
        "  实测口径为 **93 unique 审查项**（记录 93 条）与 **452 条 DecisionEvent**；"
        "环行图按\"唯一审查项\"画，另在 KPI 卡并列展示决定事件 452 条。",
        "- 任务书饼图列出的 `ITEM_BLIND` 当前为 **0 条**（真实盲审未执行），饼图按实际存在的三类画。",
        "",
        "## 局限性", "",
        "- 纯 CSS 3D（非 WebGL/Three.js）：节点只有位置和缩放，没有边/连线与真实图布局。",
        "  若要更炫的 3D 论证图（含边、可旋转拖拽），需引入 Three.js——按硬边界 14 留后续批次。",
        "- 环形/饼图用 SVG stroke 与 `conic-gradient`，非图表库；配色对色盲不友好（未做可访问性配色）。",
        "- 只读展示：不做任何判决、不改日志。",
    ]
    with open(OUT_DESIGN, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    html = generate()
    chk("HTML 生成且非空", len(html) > 4000, f"({len(html)} bytes)")
    chk("含 6 个数据模块", all(k in html for k in
                           ("① 人审进度", "② 歧义度热力图", "③ review_method",
                            "④ W2 论证图 3D", "⑤ 独立人类确认强度", "⑥ 他验三件套状态")))
    chk("深色科技风样式存在", all(k in html for k in
                             ("backdrop-filter", "--cyan", "conic-gradient", "preserve-3d",
                              "@keyframes float")))
    d = build()
    chk("唯一审查项 = 93", d["review"]["unique"] == EXPECT_UNIQUE, f'({d["review"]["unique"]})')
    chk("W2 = IN114/OUT7", d["w2"]["labels"]["IN"] == EXPECT_W2["IN"]
        and d["w2"]["labels"]["OUT"] == EXPECT_W2["OUT"], f'({d["w2"]["labels"]})')
    chk("W2 节点 121", len(d["w2"]["nodes"]) == 121, f'({len(d["w2"]["nodes"])})')
    chk("独立人类确认强度 = 0", d["blind_count"] == 0, f'({d["blind_count"]})')
    chk("透明日志链自算完整", d["attest"]["log"]["chain_valid"],
        f'({d["attest"]["log"]["entries"]} 条)')
    chk("3D 节点数 = 121", len(_sphere(121)) == 121)
    print(f"C1 dashboard v2 check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="628 C1 人审仪表盘 v2")
    ap.add_argument("--check", action="store_true", help="自检（含生成 HTML）")
    ap.add_argument("--design", action="store_true", help="写设计说明")
    ap.add_argument("--out", default=OUT_HTML)
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.design:
        write_design()
        print(f"written {OUT_DESIGN}")
        return 0
    html = generate()
    print(f"written {args.out}  ({len(html)} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
