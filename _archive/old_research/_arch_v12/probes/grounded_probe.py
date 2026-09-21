#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
593 异族调研 · 探针（只读）
================================
手搓纯标准库 grounded 求解器，在本仓 79 命题图上实跑，回答维度 2 的核心发现：
  * 攻击关系能否从现有数据构造？
  * 能构造的话，grounded 标注 in/out/undecided 各多少？
  * 当前数据下 grounded 是否退化成平凡解？

纪律：只读。本脚本不修改任何正式文件；只读取 atoms/、misconceptions/、tools/prop_graph.py。
输出 JSON 到 stdout；不写 data/、不 build propositions.db。
"""
from __future__ import annotations
import sys, time, json, itertools
from pathlib import Path

ROOT = Path(r"C:\CodeLearnling\note\note\C++\CPP-Bible")
sys.path.insert(0, str(ROOT / "tools"))
import prop_graph as pg  # 只读抽取 79 命题
import gate_engine as ge  # 读卡片 frontmatter（_meta）

t0 = time.perf_counter()

# ── 1. 抽取 79 命题（来自 27 张卡的 claim_structured）──────────────────────────
props = pg.extract()            # 列表，每项含 prop_key / card / claim_type / evidence 等
N = len(props)
prop_keys = [p["prop_key"] for p in props]
by_card = {}
for p in props:
    by_card.setdefault(p["card"], []).append(p)

# 命题类型分布
type_dist = {}
for p in props:
    type_dist[p["claim_type"]] = type_dist.get(p["claim_type"], 0) + 1

# 命题 → 证据卡 边（支持边，非攻击边）
support_edges = 0
for p in props:
    ev = p.get("_ev") or []
    support_edges += len(ev)

# ── 2. 扫描攻击关系候选：MIS 误解库 ──────────────────────────────────────────
# 每个 atom 卡的 frontmatter 含 `misconceptions: [MIS-xxx]`；
# 每个 MIS 文件含 `related_atoms: [ATOM-xxx]` 与 `refutations:`（反驳文本列表）。
mis_total = 0
mis_with_refutations = 0
mis_links = 0                 # (atom, mis) 关联对数
atoms_with_mis = set()
mis_to_atoms = {}             # MIS -> set(atoms)
atom_to_mis = {}              # atom -> set(MIS)
refutation_text_count = 0

mis_dir = ROOT / "misconceptions"
for f in sorted(mis_dir.glob("MIS-*.md")):
    mis_total += 1
    m = ge._meta(f)
    refs = m.get("refutations") or []
    if refs:
        mis_with_refutations += 1
        refutation_text_count += len(refs)
    rel = m.get("related_atoms") or []
    for a in rel:
        mis_links += 1
        mis_to_atoms.setdefault(f.stem, set()).add(a)
        atom_to_mis.setdefault(a, set()).add(f.stem)

# 从 atom 卡方向也收集一遍（双源交叉核对）
atoms_dir = ROOT / "atoms"
atom_mis_from_card = {}
for p in sorted(atoms_dir.rglob("ATOM-*.md")):
    if "README" in p.name:
        continue
    m = ge._meta(p)
    ml = m.get("misconceptions") or []
    if ml:
        atom_mis_from_card[p.stem] = set(ml)
        atoms_with_mis.add(p.stem)
        for x in ml:
            atom_to_mis.setdefault(p.stem, set()).add(x)
            mis_to_atoms.setdefault(x, set()).add(p.stem)

# 有多少命题被 MIS 关联牵扯（即所在卡有 misconceptions）
props_touched_by_mis = 0
for card, plist in by_card.items():
    if card in atom_to_mis:
        props_touched_by_mis += len(plist)

# ── 3. grounded 求解器（Dung 1995 最小不动点）────────────────────────────────
def grounded_extension(args, attacks):
    """attacks[x] = set(y) 表示 x 攻击 y。返回最小不动点 G（grounded 扩展）。"""
    attackers = {a: set() for a in args}
    for x, ys in attacks.items():
        for y in ys:
            if y in attackers:
                attackers[y].add(x)
    S = set()
    while True:
        nxt = set()
        for a in args:
            ok = True
            for b in attackers[a]:
                # b 是否被 S 击败：存在 c∈S 使 c 攻击 b
                defeated = any(b in (attacks.get(c, ())) for c in S)
                if not defeated:
                    ok = False
                    break
            if ok:
                nxt.add(a)
        if nxt == S:
            return S
        S = nxt

def tripartition(args, attacks, G):
    """IN=G; OUT=被 G 中节点攻击; UNDEC=其余。"""
    out = set()
    for g in G:
        for y in attacks.get(g, ()):
            out.add(y)
    undec = set(args) - G - out
    return G, out, undec

def measure(args, attacks, iters=200):
    best = 1e9
    G = set()
    for _ in range(iters):
        t = time.perf_counter()
        G = grounded_extension(args, attacks)
        dt = time.perf_counter() - t
        best = min(best, dt)
    return G, best

scenarios = {}

# 场景 S0：纯命题集，零攻击边 → 期望全 IN（平凡解）
args0 = set(prop_keys)
att0 = {}
G0, dt0 = measure(args0, att0)
in0, out0, und0 = tripartition(args0, att0, G0)
scenarios["S0_no_attacks"] = {
    "args": len(args0), "IN": len(in0), "OUT": len(out0), "UNDEC": len(und0),
    "time_s": dt0, "note": "零攻击边：grounded = 全集（全接受，平凡解）"
}

# 场景 S1：MIS 作为攻击者节点，MIS -> prop（方向单向，prop 不反击 MIS）
#   语义：误解是错误声称，它攻击了被它误导的命题。prop 不反攻 MIS。
args1 = set(prop_keys) | set(mis_to_atoms.keys())
att1 = {}
for mis, atoms in mis_to_atoms.items():
    for a in atoms:
        for p in by_card.get(a, []):
            att1.setdefault(mis, set()).add(p["prop_key"])
G1, dt1 = measure(args1, att1)
in1, out1, und1 = tripartition(args1, att1, G1)
scenarios["S1_mis_attacks_prop_oneway"] = {
    "args": len(args1), "IN_mis": len(in1 & set(mis_to_atoms.keys())),
    "IN_prop": len(in1 & set(prop_keys)),
    "OUT": len(out1), "UNDEC": len(und1),
    "time_s": dt1,
    "note": "MIS单向攻命题：MIS无入边→全IN(被当真！语义倒置)；其攻击的命题被OUT"
}

# 场景 S2：对称冲突 MIS <-> prop（误解与被它误解的命题互相攻击）
args2 = set(prop_keys) | set(mis_to_atoms.keys())
att2 = {}
for mis, atoms in mis_to_atoms.items():
    for a in atoms:
        for p in by_card.get(a, []):
            att2.setdefault(mis, set()).add(p["prop_key"])
            att2.setdefault(p["prop_key"], set()).add(mis)
G2, dt2 = measure(args2, att2)
in2, out2, und2 = tripartition(args2, att2, G2)
scenarios["S2_mis_prop_symmetric"] = {
    "args": len(args2), "IN": len(in2), "OUT": len(out2), "UNDEC": len(und2),
    "time_s": dt2,
    "note": "对称2-环：grounded=∅，所有命题UNDECIDED（退化成全不确定）"
}

# ── 4. 输出 ──────────────────────────────────────────────────────────────────
result = {
    "tool": "grounded_probe.py",
    "mode": "read-only",
    "propositions": N,
    "cards": len(by_card),
    "proposition_type_dist": type_dist,
    "support_edges_evidence": support_edges,
    "mis_library": {
        "mis_total": mis_total,
        "mis_with_refutations_field": mis_with_refutations,
        "refutation_text_items": refutation_text_count,
        "mis_links_atom_mis": mis_links,
        "atoms_linked_to_mis": len(atom_to_mis),
        "props_touched_by_mis": props_touched_by_mis,
    },
    "scenarios": scenarios,
    "wall_build_s": time.perf_counter() - t0,
}
print(json.dumps(result, ensure_ascii=False, indent=1))
