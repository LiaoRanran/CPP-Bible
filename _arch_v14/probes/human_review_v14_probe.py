#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
595 异族调研 · 探针（只读，纯标准库，不装 numpy/scipy/clingo/外部 JS 库）
=========================================================================
在 593/594 的 79 命题 + 42 MIS + 194 候选攻击边结构上，手搓：
  * 人审工作量模拟（排序/批量确认/主动学习，给出"小时级"的具体数字）
  * automation bias 防护模拟（陷阱题 + 机器可检测信号）
  * 可视化原型数据（节点/边/状态 -> graph.json + 自包含 index.html，纯标准库生成）
输出 JSON 到 stdout；并写 _arch_v14/visualization/ 下的原型文件（属本调研产出）。
"""
from __future__ import annotations
import sys, time, json, math, random
from pathlib import Path

ROOT = Path(r"C:\CodeLearnling\note\note\C++\CPP-Bible")
sys.path.insert(0, str(ROOT / "tools"))
import prop_graph as pg
import gate_engine as ge

t0 = time.perf_counter()
random.seed(595)

# ── 复用 594 的核心抽取 ───────────────────────────────────────────────────────
props = pg.extract()
by_card = {}
for p in props:
    by_card.setdefault(p["card"], []).append(p)

def cred(p):
    s = p.get("signoff_state", "")
    if s == "prop_signed":
        return 1.0
    if s == "card_signed":
        return 0.8
    if p.get("machine_verified"):
        return 0.6
    return 0.4
prop_cred = {p["prop_key"]: cred(p) for p in props}

mis_to_atoms = {}
mis_refs = {}
mis_dir = ROOT / "misconceptions"
for f in sorted(mis_dir.glob("MIS-*.md")):
    m = ge._meta(f)
    mis_refs[f.stem] = m.get("refutations") or []
    for a in (m.get("related_atoms") or []):
        mis_to_atoms.setdefault(f.stem, set()).add(a)

# 候选攻击边（单向 MIS->prop，来自 related_atoms）
edges = []
for mis, atoms in mis_to_atoms.items():
    for a in atoms:
        plist = by_card.get(a, [])
        for p in plist:
            edges.append({
                "mis": mis, "prop": p["prop_key"], "card": a,
                "prop_cred": prop_cred[p["prop_key"]], "mis_cred": 0.1,
                "n_props_on_card": len(plist),
                "has_text": bool(mis_refs.get(mis)),
            })
# 每张卡被多少 MIS 关联（歧义度之一）
card_mis_count = {}
for mis, atoms in mis_to_atoms.items():
    for a in atoms:
        card_mis_count[a] = card_mis_count.get(a, 0) + 1
for e in edges:
    e["n_mis_on_card"] = card_mis_count.get(e["card"], 1)
N_EDGES = len(edges)

# ── 1. 人审工作量模拟 ─────────────────────────────────────────────────────────
# 三套策略（明确声明标准）
def review_SA(e):   # 仅验证过的命题自动确认（忽略目标歧义）
    return e["prop_cred"] < 0.8
def review_SB(e):   # 验证过 且 单命题卡 才自动确认
    return e["prop_cred"] < 0.8 or e["n_props_on_card"] > 1
def review_SC(e):   # 主动学习：仅"未验证 或 目标歧义"进人审
    return review_SB(e)

def split(rev_pred):
    auto = [e for e in edges if not rev_pred(e)]
    rev = [e for e in edges if rev_pred(e)]
    return auto, rev

strategies = {}
T_AUTO, T_REVIEW = 3.0, 35.0
for name, pred in [("SA_verified_auto", review_SA), ("SB_verified_unambiguous", review_SB),
                   ("SC_active_learning", review_SC)]:
    auto, rev = split(pred)
    strategies[name] = {
        "auto": len(auto), "review": len(rev),
        "review_minutes": round(len(rev) * T_REVIEW / 60, 1),
        "review_hours": round(len(rev) * T_REVIEW / 3600, 2),
    }

# prop_cred 分布 + 卡命题数分布（解释瓶颈来源）
cred_hist = {}
for e in edges:
    cred_hist[e["prop_cred"]] = cred_hist.get(e["prop_cred"], 0) + 1
cardprop_hist = {}
for e in edges:
    cardprop_hist[e["n_props_on_card"]] = cardprop_hist.get(e["n_props_on_card"], 0) + 1

# 主动学习排序：人审队列按歧义度降序（多命题+多MIS卡的边优先）
def ambiguity(e):
    return e["n_props_on_card"] * 2 + e["n_mis_on_card"]
review_sorted = sorted([e for e in edges if review_SB(e)], key=ambiguity, reverse=True)

# 群组级人审：按 MIS 聚合（每条 MIS 只需一次"决定它驳斥哪些命题"的判断）
mis_groups = {}
for e in edges:
    mis_groups.setdefault(e["mis"], []).append(e)
mis_level = {"mis_groups": len(mis_groups),
             "review_minutes": round(len(mis_groups) * T_REVIEW / 60, 1),
             "review_hours": round(len(mis_groups) * T_REVIEW / 3600, 2),
             "note": "按 MIS 聚合人审 ≈ 42 次判断，远少于 194 条边级判断"}

workload = {
    "total_edges": N_EDGES,
    "strategies": strategies,
    "mis_group_level": mis_level,
    "prop_cred_hist": {str(k): v for k, v in sorted(cred_hist.items())},
    "card_props_hist": {str(k): v for k, v in sorted(cardprop_hist.items())},
    "assumptions_s": {"T_AUTO": T_AUTO, "T_REVIEW": T_REVIEW},
    "note": "瓶颈来自目标歧义（多命题卡），非可信度——191/194 边命题已验证(cred>=0.8)",
}

# ── 2. automation bias 防护模拟 ───────────────────────────────────────────────
TRAP_N = 10
true_invalid = [e for e in edges if e["prop_cred"] < 0.8]
traps = [{"prop_cred": 0.1, "is_trap": True} for _ in range(TRAP_N)]
def simulate(queue, mode):
    agree = caught = confirmed = 0
    for e in queue:
        machine_says = True
        if mode == "rubber":
            decision = True
        else:
            decision = e.get("prop_cred", 0) >= 0.8 and not e.get("is_trap", False)
        if decision:
            confirmed += 1
        if decision == machine_says:
            agree += 1
        if e.get("is_trap") and not decision:
            caught += 1
    return {"mode": mode, "agree_rate": round(agree / len(queue), 3),
            "confirmed": confirmed, "caught_traps": caught, "traps_total": TRAP_N}
queue = edges + traps
sim = {"trap_count": TRAP_N, "true_invalid_edges": len(true_invalid),
       "rubber_stamp": simulate(queue, "rubber"), "careful": simulate(queue, "careful"),
       "detect_signals": {"rubber_signature": "agree_rate==1.0 且 caught_traps==0",
                          "detectable_by_machine": True,
                          "note": "存 review_seconds+reason_len，agree==1.0 且 reason 过短即触发复核"}}

# ── 3. 可视化原型数据 ─────────────────────────────────────────────────────────
nodes = [{"id": p["prop_key"], "type": "prop", "status": "IN", "cred": prop_cred[p["prop_key"]]} for p in props]
nodes += [{"id": mis, "type": "mis", "status": "OUT", "cred": 0.1} for mis in mis_to_atoms]
viz_edges = [{"from": e["mis"], "to": e["prop"], "kind": "attack"} for e in edges]
for card, plist in by_card.items():
    pids = [p["prop_key"] for p in plist]
    for i in range(len(pids)):
        for j in range(i + 1, len(pids)):
            viz_edges.append({"from": pids[i], "to": pids[j], "kind": "support"})
graph = {"nodes": nodes, "edges": viz_edges,
         "meta": {"props": len(props), "mis": len(mis_to_atoms),
                  "attack_edges": sum(1 for x in viz_edges if x["kind"] == "attack"),
                  "support_edges": sum(1 for x in viz_edges if x["kind"] == "support")}}

# ── 4. 输出 ───────────────────────────────────────────────────────────────────
summary = {"tool": "human_review_v14_probe.py", "mode": "read-only",
           "workload": workload, "automation_bias_sim": sim,
           "viz_graph_meta": graph["meta"], "wall_s": round(time.perf_counter() - t0, 3)}
print(json.dumps(summary, ensure_ascii=False, indent=1))

def build_html(g):
    n_p = sum(1 for x in g["nodes"] if x["type"] == "prop")
    n_m = sum(1 for x in g["nodes"] if x["type"] == "mis")
    W, H, R1, R2 = 1000, 1000, 260, 430
    cx, cy = W // 2, H // 2
    pos = {}
    i = 0
    for x in g["nodes"]:
        if x["type"] == "mis":
            ang = 2 * math.pi * i / max(n_m, 1)
            pos[x["id"]] = (cx + R1 * math.cos(ang), cy + R1 * math.sin(ang)); i += 1
    i = 0
    for x in g["nodes"]:
        if x["type"] == "prop":
            ang = 2 * math.pi * i / max(n_p, 1)
            pos[x["id"]] = (cx + R2 * math.cos(ang), cy + R2 * math.sin(ang)); i += 1
    lines, circ = [], []
    for e in g["edges"]:
        a, b = pos.get(e["from"]), pos.get(e["to"])
        if not a or not b:
            continue
        col = "#d33" if e["kind"] == "attack" else "#3a3"
        w = 1.2 if e["kind"] == "attack" else 0.5
        lines.append(f'<line x1="{a[0]:.0f}" y1="{a[1]:.0f}" x2="{b[0]:.0f}" y2="{b[1]:.0f}" stroke="{col}" stroke-width="{w}" opacity="0.35"/>')
    for x in g["nodes"]:
        px, py = pos[x["id"]]
        fill = "#2a8" if x["status"] == "IN" else "#c44"
        rad = 7 if x["type"] == "prop" else 9
        circ.append(f'<circle cx="{px:.0f}" cy="{py:.0f}" r="{rad}" fill="{fill}"><title>{x["id"]} ({x["type"]}/{x["status"]})</title></circle>')
    return f"""<!doctype html><html lang="zh"><head><meta charset="utf-8">
<title>grounded 可视化原型 (W2: 命题IN / 误解OUT)</title>
<style>body{{font-family:sans-serif;background:#111;color:#ddd}} .legend{{margin:8px}}</style></head><body>
<h3>grounded 标注可视化原型 — W2 模型（命题全 IN / 误解全 OUT）</h3>
<div class="legend">● 绿=IN(命题) ● 红=OUT(误解) | 红线=攻击边(MIS→命题) 绿细线=支持边代理(同卡命题)</div>
<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}">
{''.join(lines)}
{''.join(circ)}
</svg>
<p>节点数={len(g['nodes'])}，攻击边={g['meta']['attack_edges']}，支持边(代理)={g['meta']['support_edges']}。</p>
<p>纯标准库生成，无外部依赖。悬停圆点看 id。布局为圆形（内圈误解/外圈命题）。</p>
</body></html>"""

# ── 5. 写可视化原型（本调研产出，落 _arch_v14/）────────────────────────────────
out_dir = ROOT / "_arch_v14" / "visualization"
out_dir.mkdir(parents=True, exist_ok=True)
(out_dir / "graph.json").write_text(json.dumps(graph, ensure_ascii=False, indent=1), encoding="utf-8")
(out_dir / "index.html").write_text(build_html(graph), encoding="utf-8")
print(f"[probe] wrote {out_dir/'graph.json'} and {out_dir/'index.html'}")
