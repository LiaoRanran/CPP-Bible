# -*- coding: utf-8 -*-
"""
p01_arggraph_robustness.py  — _arch_v20 只读探针
方向 11（复杂系统/网络科学）+ 方向 12（信息论）实证：
  在阙疑真实攻击边数据上，把论证图当作有向网络测量：
    1) 规模/度数分布/Shannon 熵（方向12：熵作为结构度量）
    2) 关键节点：in/out 度 + 介数中心性（方向11：critical node identification）
    3) 级联失效：按度排序定点移除 vs 随机移除，观察最大连通分量 LCC（方向11）
    4) 镜像边统计（前序 v19 G9：同一 ATOM 的多条 prop 扇向同一 MIS）
    5) 批准边子图 vs 全部候选边对比（人审过滤改变了什么结构）
纯标准库，只读，不写任何仓内正式文件。
"""
import json, math, random, collections, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EDGES_609 = os.path.join(ROOT, "data", "attack_edges_609.json")
CAND = os.path.join(ROOT, "data", "attack_edges_candidates.jsonl")
ANNO = os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl")


def load_jsonl(p):
    out = []
    with open(p, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                out.append(json.loads(line))
    return out


def shannon_entropy(counts):
    n = sum(counts)
    if n == 0:
        return 0.0
    return -sum((c / n) * math.log2(c / n) for c in counts if c)


def lcc_size(nodes, adj):
    """无向最大连通分量（忽略方向，鲁棒性惯例）"""
    seen = set()
    best = 0
    for s in nodes:
        if s in seen:
            continue
        stack, comp = [s], {s}
        seen.add(s)
        while stack:
            u = stack.pop()
            for v in adj.get(u, ()):
                if v in nodes and v not in comp:
                    comp.add(v); seen.add(v); stack.append(v)
        best = max(best, len(comp))
    return best


def betweenness(nodes, adj, cap=400):
    """无向无权 Brandes 介数（节点少时全量）"""
    cb = collections.defaultdict(float)
    for s in nodes:
        S, P, sigma, D = [], {v: [] for v in nodes}, {v: 0 for v in nodes}, {v: -1 for v in nodes}
        sigma[s], D[s] = 1, 0
        Q = [s]
        for v in Q:
            for w in adj.get(v, ()):
                if w not in D:
                    continue
                if D[w] < 0:
                    Q.append(w); D[w] = D[v] + 1
                if D[w] == D[v] + 1:
                    sigma[w] += sigma[v]; P[w].append(v)
        delta = {v: 0.0 for v in nodes}
        for w in reversed(Q):
            for v in P[w]:
                delta[v] += (sigma[v] / sigma[w]) * (1 + delta[w])
            if w != s:
                cb[w] += delta[w]
    return cb


def analyze(edges, title):
    print("=" * 78)
    print(f"## {title}  边数={len(edges)}")
    nodes = set()
    adj = collections.defaultdict(set)   # 无向邻接（LCC/介数用）
    outd = collections.Counter()
    ind = collections.Counter()
    kinds = collections.Counter()
    atom_target = collections.Counter()  # (atom,target) 组规模（镜像边）
    for e in edges:
        s, t = e["source"], e["target"]
        nodes |= {s, t}
        adj[s].add(t); adj[t].add(s)
        outd[s] += 1; ind[t] += 1
        kinds[e.get("kind", "?")] += 1
        atom = s.split("::")[0]
        atom_target[(atom, t)] += 1
    print(f"节点={len(nodes)}  有向边={len(edges)}  平均度(无向)={2*sum(len(v) for v in adj.values())/max(1,len(nodes)):.2f}")
    print("边类型分布:", dict(kinds))

    degs = [len(v) for v in adj.values()]
    deg_hist = collections.Counter(degs)
    print(f"无向度: min={min(degs)} max={max(degs)} 度Shannon熵={shannon_entropy(deg_hist.values()):.3f} bit "
          f"(理论最大 {math.log2(len(deg_hist)):.3f})")

    # 节点类别
    mis = [n for n in nodes if n.startswith("MIS-")]
    prop = [n for n in nodes if "::prop-" in n]
    other = nodes - set(mis) - set(prop)
    print(f"节点类别: MIS={len(mis)}  命题节点={len(prop)}  其他={len(other)} {sorted(other)[:6]}")

    # 关键节点：入度 top（被最多命题攻击的 MIS = 论证依赖集中点）
    print("\n-- 被最多命题指向的节点（入度 top8，论证依赖集中度）--")
    for n, c in ind.most_common(8):
        print(f"  {c:3d}  {n}")
    print("-- 扇出最大的命题节点（out度 top8）--")
    for n, c in outd.most_common(8):
        print(f"  {c:3d}  {n}")

    # 介数
    cb = betweenness(nodes, adj)
    topb = sorted(cb.items(), key=lambda kv: (-kv[1], kv[0]))[:8]
    print("-- 介数中心性 top8（信息流咽喉）--")
    for n, c in topb:
        # 取整显示：不同 str hash 进程下浮点求和末位有 ±0.1 抖动，不影响排序
        print(f"  {round(c):8d}  {n}")

    # 镜像边
    groups = collections.Counter(atom_target.values())
    mirror_edges = sum((g - 1) * cnt for g, cnt in groups.items() if g >= 2)
    multi = [(k, g) for k, g in atom_target.items() if g >= 2]
    multi.sort(key=lambda kv: -kv[1])
    print(f"\n-- 镜像边（同 ATOM 多 prop → 同 MIS）--")
    print(f"  存在多打一的(atom,MIS)组={len(multi)}  冗余镜像边(组规模-1之和)={mirror_edges} "
          f"占总边 {100*mirror_edges/max(1,len(edges)):.1f}%")
    for (atom, t), g in multi[:6]:
        print(f"   x{g}  {atom} -> {t}")

    # 级联失效：LCC 对定点移除的脆弱性
    # 名次确定性：按(度降序, 节点名升序)，避免 str hash 随机化下同度节点跨进程波动
    N0 = lcc_size(nodes, adj)
    ranked = [n for n, _ in sorted(
        ((n, len(adj[n])) for n in nodes), key=lambda kv: (-kv[1], kv[0]))]
    rnd = random.Random(20260921)
    print(f"\n-- 级联失效模拟（初始 LCC={N0}）--")
    print("  移除数  定点(按度)LCC   随机LCC(100次均值)   定点/初始")
    for k in (3, 5, 8, 12):
        alive_t = nodes - set(ranked[:k])
        t = lcc_size(alive_t, adj)
        rs = []
        nl = sorted(nodes)  # 固定初始序，避免 hash 随机化影响 shuffle 序列
        for _ in range(100):
            rnd.shuffle(nl)
            rs.append(lcc_size(nodes - set(nl[:k]), adj))
        print(f"   {k:3d}     {t:6d}        {sum(rs)/len(rs):7.1f}          {t/N0:.3f}")
    return nodes, edges


def main():
    random.seed(20260921)
    # 609 冻结边
    e609 = [json.loads(l) for l in open(EDGES_609, encoding="utf-8") if l.strip()]
    nodes609, _ = analyze(e609, "attack_edges_609.json（冻结/权威边集）")

    # 候选全集
    cand = load_jsonl(CAND)
    cids = {e["id"] for e in cand}
    print(f"\n候选文件总边={len(cand)}  与609边id重合={len(cids & {e['id'] for e in e609})}")

    # 人审标注
    anno = load_jsonl(ANNO)
    acts = collections.Counter(a["action"] for a in anno)
    print(f"人审标注记录={len(anno)}  动作分布={dict(acts)}")
    approved = {a["edge_id"] for a in anno if a["action"] in ("approve", "modify")}
    rejected = {a["edge_id"] for a in anno if a["action"] == "reject"}
    print(f"approve+modify={len(approved)}  reject={len(rejected)}")
    # 人审批准边在候选集合上构成的子图
    esub = [e for e in cand if e["id"] in approved]
    analyze(esub, "人审 approve/modify 边子图（候选文件∩人审通过）")


if __name__ == "__main__":
    main()
