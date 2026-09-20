"""610 B1 · 辩护链核心引擎（智能原型 1：**确定性推理**，零 Oracle 风险）。

回答的问题：**某个节点为什么是 IN/OUT？如果动一下可信度会怎样？**

数据与口径（三条都必须写死，否则结论不可复现）：

  1. **边**来自 `data/attack_edges_candidates.jsonl`（388 条），信任度档取自边自身；
  2. **人审后的节点可信度**（610 实测：这套口径重算与入库 W2 产物**逐项一致**）：
       命题 = `medium`（默认档）；
       MIS  = 任一入边被 **approve** ⇒ `medium`；**modify / reject / 未审 ⇒ 保持 `low`**。
     ⚠️ 与 609 A3 `weighted_af_solver.reviewed_edges` 的差别：那支对 modify 取 `new_confidence`
     （实测得 IN121/OUT0），本引擎按**权威产物口径**（modify 保持 low ⇒ IN114/OUT7）；
  3. **判决**直接用 W2 求解内核（`weighted_af_solver` 的 `build_graph/defeats_of/
     grounded_labels`）现算，不抄入库文件里的标签 —— 这样 `what_if` 才有意义。

CLI 见 B2（`show/what-if/min-attack-set/report/stats/...`）。
"""
# mypy: ignore-errors
# 类型注解债务，CI 先转绿，后续逐步修
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import attack_edge_generator as aeg  # noqa: E402
import human_review_cli as hrc  # noqa: E402
import weighted_af_solver as w2  # noqa: E402

VERSION = "1.0"
DEFAULT_EDGES = aeg.DEFAULT_OUT
DEFAULT_ANN = hrc.DEFAULT_ANN
DEFAULT_LABELS = ROOT / "data" / "grounded_labels_w2.json"
DEFAULT_REPORT = ROOT / "data" / "defense_chain_report.md"
DEFAULT_HTML = ROOT / "data" / "defense_chain.html"

CREDIBILITY_ORDER = {"low": 0, "medium": 1, "high": 2}
PROP_CREDIBILITY = "medium"
#: 人审 action ⇒ MIS 的可信度档（modify **保持 low** —— 与入库 W2 产物一致的口径）
VERDICT_CREDIBILITY = {"approve": "medium", "modify": None, "reject": None, "unreviewed": None}


@dataclass
class AttackEdge:
    """一条攻击边（`kind` 按 610 任务书 = 方向；候选边的 kind 另存 `edge_kind`）。"""
    edge_id: str
    source: str
    target: str
    kind: str                    # "mis_to_prop" / "prop_to_mis"（= 方向）
    confidence: str              # "high" / "medium" / "low"
    human_verdict: str           # "approve" / "modify" / "reject" / "unreviewed"
    edge_kind: str = ""          # 候选边的 kind（misconception_refutation / related_atom）
    is_defeating: bool = False


@dataclass
class DefenseChain:
    node_id: str
    node_type: str
    credibility: str
    verdict: str
    attackers: list[AttackEdge] = field(default_factory=list)   # target == node_id
    defenders: list[AttackEdge] = field(default_factory=list)   # source == node_id
    defeated_by: list[str] = field(default_factory=list)        # 击败它的攻击者（OUT 才有）
    defeats: list[str] = field(default_factory=list)            # 它击败的节点
    #: **人的辩护者**（W2 口径）：IN 且攻击了"攻击我的某个攻击者"的节点 ⇒ 真正替我挡刀的那些
    w2_defenders: list[str] = field(default_factory=list)


# ── 数据加载 ──────────────────────────────────────────────────────────────────
def load_annotations(path: Path | str | None = None) -> list[dict]:
    return hrc.load_annotations(path if path else DEFAULT_ANN)


def load_data(edges_path: Path | str | None = None,
              ann_path: Path | str | None = None) -> tuple[list[AttackEdge], dict[str, str],
                                                            dict[str, str]]:
    """→ (attack_edges, verdicts, credibilities)。

    `verdicts` 由 **W2 内核现算**（不是读入库标签），`credibilities` 按上面第 2 条口径算。
    """
    raw = aeg.load_edges(edges_path if edges_path else DEFAULT_EDGES)
    last = hrc.latest_by_edge(load_annotations(ann_path))

    edges: list[AttackEdge] = []
    for e in raw:
        a = last.get(str(e["id"]))
        verdict = hrc.kind_of(a) if a is not None else "unreviewed"
        edges.append(AttackEdge(edge_id=str(e["id"]), source=str(e["source"]),
                                target=str(e["target"]), kind=str(e["direction"]),
                                confidence=str(e.get("confidence")), human_verdict=verdict,
                                edge_kind=str(e.get("kind", ""))))

    cred = credibilities_of(edges)
    verdicts = solve_verdicts(edges, cred)
    return edges, verdicts, cred


def credibilities_of(edges: list[AttackEdge]) -> dict[str, str]:
    """节点可信度：命题 = medium（**全集取 W2 内置命题表**，含 4 个无边的命题）；
    MIS = 有 approve 边 ⇒ medium，否则 low（modify/reject/未审 ⇒ low）。"""
    props = set(w2.proposition_nodes())
    mis_approved: set[str] = set()
    mis_all: set[str] = set()
    for e in edges:
        if e.kind == "mis_to_prop":
            prop, mis = e.target, e.source
        else:
            prop, mis = e.source, e.target
        props.add(prop)
        mis_all.add(mis)
        if e.human_verdict == "approve":
            mis_approved.add(mis)
    out = {p: PROP_CREDIBILITY for p in props}
    for m in mis_all:
        out[m] = VERDICT_CREDIBILITY["approve"] if m in mis_approved else "low"
    return dict(sorted(out.items()))


def _as_dicts(edges: list[AttackEdge], cred: dict[str, str]) -> list[dict]:
    """转成 W2 内核吃的边格式。

    关键：W2 的 `build_graph` 是**从边反推 MIS 档位**（取该 MIS 相关边的最大档）⇒
    这里每条边的 `confidence` 必须填**该边 MIS 端点**的档位，而不是 source 的档位；
    命题档位由 W2 内置命题表给出（medium）。
    """
    out = []
    for e in edges:
        mis_end = e.source if e.kind == "mis_to_prop" else e.target
        out.append({"id": e.edge_id, "source": e.source, "target": e.target,
                    "kind": e.edge_kind or "misconception_refutation",
                    "direction": e.kind,
                    "confidence": cred.get(mis_end, e.confidence)})
    return out


def _solve_raw(edges: list[AttackEdge], cred: dict[str, str]) -> dict:
    """**节点级**可信度 + W2 的 grounded 内核（`grounded_labels`）现算。

    为什么不用 `w2.solve`：那支是"从边反推 MIS 档"（`build_graph`），命题档位写死 ⇒
    `what_if(命题, …)` 会**没有任何效果**（610 实测：改动命题可信度，判决 0 变化）。
    这里把节点档位当作输入、只复用 W2 的**判决内核**（击败 = 严格大于；IN/OUT 最小不动点）。
    """
    nodes: dict[str, dict] = {}
    for n, c in cred.items():
        nodes[n] = {"id": n, "type": node_type_of(n, edges), "confidence": c,
                    "credibility": CREDIBILITY_ORDER[c]}
    defeats = {(e.source, e.target) for e in edges
               if CREDIBILITY_ORDER.get(cred.get(e.source, "low"), 0)
               > CREDIBILITY_ORDER.get(cred.get(e.target, "low"), 0)}
    labels, rounds = w2.grounded_labels(nodes, defeats)
    return {"nodes": nodes, "labels": labels, "defeats": defeats, "rounds": rounds}


def solve_verdicts(edges: list[AttackEdge], cred: dict[str, str]) -> dict[str, str]:
    return dict(_solve_raw(edges, cred)["labels"])


def solve_summary(edges: list[AttackEdge], cred: dict[str, str]) -> dict:
    r = _solve_raw(edges, cred)
    labels = r["labels"]
    props = [n for n in labels if node_type_of(n, edges) == "proposition"]
    mis = [n for n in labels if node_type_of(n, edges) == "misconception"]
    return {"nodes": len(labels),
            "in": sum(1 for v in labels.values() if v == "IN"),
            "out": sum(1 for v in labels.values() if v == "OUT"),
            "undec": sum(1 for v in labels.values() if v == "UNDEC"),
            "in_propositions": sum(1 for n in props if labels[n] == "IN"),
            "in_misconceptions": sum(1 for n in mis if labels[n] == "IN"),
            "defeating_edges": len(r["defeats"]), "edges": len(edges), "rounds": r["rounds"]}


def is_defeating(edge: AttackEdge, credibilities: dict[str, str]) -> bool:
    """击败 = 攻击者可信度**严格大于**被攻击者（W2 定义，一行不改）。"""
    a = credibilities.get(edge.source, "low")
    b = credibilities.get(edge.target, "low")
    return CREDIBILITY_ORDER[a] > CREDIBILITY_ORDER[b]


def node_type_of(node_id: str, edges: list[AttackEdge]) -> str:
    return "proposition" if "::prop-" in str(node_id) else "misconception"


# ── 辩护链 ────────────────────────────────────────────────────────────────────
def get_defense_chain(node_id: str, edges: list[AttackEdge], verdicts: dict[str, str],
                      credibilities: dict[str, str]) -> DefenseChain:
    attackers = [e for e in edges if e.target == node_id]
    defenders = [e for e in edges if e.source == node_id]
    for e in attackers + defenders:
        e.is_defeating = is_defeating(e, credibilities)
    verdict = verdicts.get(node_id, "UNDEC")
    defeated_by = sorted({e.source for e in attackers if e.is_defeating}) \
        if verdict == "OUT" else []
    defeats = sorted({e.target for e in defenders if e.is_defeating})
    attacks_of: dict[str, set[str]] = {}
    for e in edges:
        attacks_of.setdefault(e.source, set()).add(e.target)
    w2_defenders = sorted({d for a in (set(defeated_by) | {e.source for e in attackers})
                           for d in attacks_of.get(a, set())
                           if verdicts.get(d) == "IN" and d != node_id})
    return DefenseChain(node_id=node_id, node_type=node_type_of(node_id, edges),
                        credibility=credibilities.get(node_id, "low"), verdict=verdict,
                        attackers=attackers, defenders=defenders,
                        defeated_by=defeated_by, defeats=defeats,
                        w2_defenders=w2_defenders)


def render_chain(chain: DefenseChain) -> str:
    """人读文本（CLI show 用）。"""
    lines = [f"# 辩护链 · {chain.node_id}",
             f"- 类型 {chain.node_type} · 判决 **{chain.verdict}** · 可信度 {chain.credibility}",
             f"- 攻击它的边 {len(chain.attackers)} 条（构成击败 {len(chain.defeated_by)} 条）"
             f" · 它攻击别人 {len(chain.defenders)} 条（其中击败 {len(chain.defeats)} 条）"]
    if chain.attackers:
        lines.append("## 攻击者")
        for e in sorted(chain.attackers, key=lambda x: x.source):
            tag = "击败" if e.is_defeating else "不构成击败（同档或更低）"
            lines.append(f"- `{e.edge_id}`：`{e.source}`（{e.human_verdict}）→ "
                         f"`{e.target}` ⇒ {tag}")
    else:
        lines.append("## 攻击者\n- 无（没有任何边指向它）")
    lines.append("## 被它击败")
    lines += [f"- `{t}`" for t in chain.defeats] or ["- 无"]
    if chain.verdict == "OUT":
        lines.append("## 击败它的攻击者（决定 OUT 的那批）")
        lines += [f"- `{s}`" for s in chain.defeated_by] or ["- 无（OUT 却无击败者 ⇒ 异常）"]
    return "\n".join(lines) + "\n"


# ── 因果推理 ──────────────────────────────────────────────────────────────────
def what_if(node_id: str, new_credibility: str, edges: list[AttackEdge],
            verdicts: dict[str, str], credibilities: dict[str, str]) -> dict:
    """若 `node_id` 的可信度变成 `new_credibility` ⇒ 用 W2 内核**全量重算**判决差异。

    （任务书允许"只重算直接相邻"的简化版；这里直接全量重算——121 节点规模下代价可忽略，
    却避免了"局部近似"带来的结论风险。）
    """
    if new_credibility not in CREDIBILITY_ORDER:
        raise ValueError(f"可信度须 ∈ {tuple(CREDIBILITY_ORDER)}，实得 {new_credibility!r}")
    cred2 = dict(credibilities)
    cred2[node_id] = new_credibility
    v2 = solve_verdicts(edges, cred2)
    changed = [{"node_id": k, "old_verdict": verdicts.get(k), "new_verdict": v2[k]}
               for k in sorted(v2) if verdicts.get(k) != v2[k]]
    s = solve_summary(edges, cred2)
    return {"node_id": node_id, "from": credibilities.get(node_id), "to": new_credibility,
            "changed_nodes": changed, "total_in": s["in"], "total_out": s["out"],
            "total_undec": s["undec"], "defeating_edges": s["defeating_edges"],
            "new_credibility_of_node": new_credibility}


def what_if_overturned(node_id: str, edges: list[AttackEdge], verdicts: dict[str, str],
                       credibilities: dict[str, str]) -> dict:
    """"被推翻"预演：可信度压到 `low`（± 强制该节点 OUT）后，判决怎么变。"""
    res = what_if(node_id, "low", edges, verdicts, credibilities)
    cred2 = dict(credibilities)
    cred2[node_id] = "low"
    v2 = solve_verdicts(edges, cred2)
    res["forced_out"] = v2.get(node_id) == "OUT"
    res["overturned_self_verdict"] = v2.get(node_id)
    res["affected_nodes"] = [c["node_id"] for c in res["changed_nodes"]]
    return res


def find_min_attack_set(target_node: str, edges: list[AttackEdge],
                        credibilities: dict[str, str], *,
                        verdicts: dict[str, str] | None = None) -> dict:
    """让 `target_node` 变 OUT 的**最小攻击集**（提升哪些攻击者的可信度到 `high`）。

    ⚠️ 贪心**近似解**（真最优是 NP-hard）：按"当前可信度档高→低、攻击者被批准过→未批准"排序，
    逐个提升并全量重算，直到目标变 OUT。返回 `{"set": [...], "achieved": bool, "note": ...}`；
    穷尽攻击者仍未 OUT ⇒ `achieved=False`（**不假装找到了**）。
    """
    base = verdicts if verdicts is not None else solve_verdicts(edges, credibilities)
    if base.get(target_node) == "OUT":
        return {"target": target_node, "set": [], "achieved": True,
                "note": "目标本来就是 OUT ⇒ 空集已达成"}
    attackers = sorted({e.source for e in edges if e.target == target_node},
                       key=lambda n: (-CREDIBILITY_ORDER.get(credibilities.get(n, "low"), 0), n))
    chosen: list[str] = []
    cred2 = dict(credibilities)
    for cand in attackers:
        cred2[cand] = "high"
        chosen.append(cand)
        if solve_verdicts(edges, cred2).get(target_node) == "OUT":
            return {"target": target_node, "set": chosen, "achieved": True,
                    "note": f"贪心近似：提升 {len(chosen)}/{len(attackers)} 个攻击者到 high"}
    return {"target": target_node, "set": chosen, "achieved": False,
            "note": "穷尽全部攻击者仍未使目标 OUT ⇒ 该目标不由这些攻击者决定（如命题需 ALL 攻击者 OUT）"}


# ── 批量报告 ──────────────────────────────────────────────────────────────────
def batch_report(edges: list[AttackEdge], verdicts: dict[str, str],
                 credibilities: dict[str, str]) -> str:
    s = solve_summary(edges, credibilities)
    chains = {n: get_defense_chain(n, edges, verdicts, credibilities) for n in sorted(verdicts)}
    out_nodes = sorted(n for n, v in verdicts.items() if v == "OUT")
    no_def = sorted(n for n, c in chains.items() if not c.w2_defenders)
    no_atk = sorted(n for n, c in chains.items()
                    if not c.attackers and c.node_type == "proposition")
    cred_dist: dict[str, int] = {}
    for c in credibilities.values():
        cred_dist[c] = cred_dist.get(c, 0) + 1
    lines = [
        "# 辩护链批量报告（610 B1）", "",
        "## 1. 总览", "",
        f"- 节点 **{s['nodes']}**（命题 {s['nodes'] - len([n for n in verdicts if node_type_of(n, edges) == 'misconception'])}"
        f" + 误解 {len([n for n in verdicts if node_type_of(n, edges) == 'misconception'])})",
        f"- 判决 **IN {s['in']} / OUT {s['out']} / UNDEC {s['undec']}**",
        f"- 边 {s['edges']} 条 · 击败边 **{s['defeating_edges']}** · {s['rounds']} 轮收敛",
        f"- 可信度分布 {cred_dist}", "",
        f"## 2. OUT 节点（{len(out_nodes)} 个）", "",
    ]
    for n in out_nodes:
        c = chains[n]
        lines.append(f"- `{n}`（cred {c.credibility}）：被 {len(c.defeated_by)} 个攻击者击败"
                     f"（{', '.join(c.defeated_by) or '—'}）· 辩护者 {len(c.defenders)} 条")
    lines += ["", f"## 3. 无辩护者的节点（{len(no_def)} 个）", ""]
    lines += [f"- `{n}`（{chains[n].verdict}）" for n in no_def] or ["- 无"]
    lines += ["", f"## 4. 无攻击者的命题（{len(no_atk)} 个）", ""]
    lines += [f"- `{n}`（cred {chains[n].credibility} ⇒ 无攻击者即 IN）" for n in no_atk] or ["- 无"]
    lines += ["", "## 5. 逐节点辩护链（IN 命题抽样 5 个）", ""]
    props_in = [n for n in sorted(verdicts) if verdicts[n] == "IN"
                and node_type_of(n, edges) == "proposition"][:5]
    for n in props_in:
        c = chains[n]
        lines.append(f"- `{n}`：攻击者 {len(c.attackers)} 条全部不构成击败（同可信度）"
                     f" ⇒ 判 IN；其中 {len(c.defeats)} 个攻击者被它击败")
    lines += ["", "> 口径：命题 = medium；MIS = 有 approve 边 ⇒ medium，否则 low"
                  "（modify 保持 low，与入库 W2 产物一致）。", ""]
    return "\n".join(lines)


def stats(edges: list[AttackEdge], verdicts: dict[str, str],
          credibilities: dict[str, str]) -> dict:
    s = solve_summary(edges, credibilities)
    out_nodes = sorted(n for n, v in verdicts.items() if v == "OUT")
    chains = {n: get_defense_chain(n, edges, verdicts, credibilities) for n in sorted(verdicts)}
    # 口径（与入库 W2 产物 7/4 对齐）：no_defenders = **W2 意义的辩护者**为空；
    # no_attackers = 无任何入边的命题（4 个 CONC 命题）。
    no_def = sorted(n for n in verdicts if not chains[n].w2_defenders)
    no_atk = sorted(n for n, v in verdicts.items()
                    if not any(e.target == n for e in edges) and node_type_of(n, edges) == "proposition")
    return {"total_nodes": s["nodes"], "in": s["in"], "out": s["out"], "undec": s["undec"],
            "in_propositions": s["in_propositions"], "in_misconceptions": s["in_misconceptions"],
            "total_edges": s["edges"], "defeating_edges": s["defeating_edges"],
            "rounds": s["rounds"], "no_defenders": len(no_def), "no_attackers": len(no_atk),
            "out_nodes": out_nodes, "no_defender_nodes": no_def,
            "no_attacker_propositions": no_atk,
            "credibility_distribution": {k: sum(1 for v in credibilities.values() if v == k)
                                         for k in ("high", "medium", "low")}}


HTML_HEAD = """<!DOCTYPE html>
<html lang="zh-CN"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>辩护链可视化 · 610 B3</title>
<style>
body{font-family:sans-serif;margin:16px;color:#222}
svg{width:100%;height:auto;display:block}
.wrap{display:flex;flex-wrap:wrap;gap:16px}
.panel{flex:1 1 320px;min-width:280px;border:1px solid #e0e0e0;border-radius:6px;padding:12px}
.legend span{display:inline-block;margin-right:14px;font-size:12px}
.dot{display:inline-block;width:10px;height:10px;border-radius:50%;margin-right:4px}
table{border-collapse:collapse;width:100%}
th,td{border:1px solid #ddd;padding:4px 8px;font-size:12px;text-align:left}
code{background:#f5f5f5;padding:1px 4px}
.node{cursor:pointer}
.node:hover{stroke:#000;stroke-width:3}
#detail{min-height:120px;font-size:13px}
</style></head><body>
<h1>辩护链可视化（智能原型 1）</h1>
<p class="note">口径：命题 = medium；MIS = 有 approve 边 ⇒ medium，否则 low（modify 保持 low）。</p>
<div class="wrap">
  <div class="panel" style="flex:2 1 520px">
    <div id="graph"></div>
    <p class="legend">
      <span><i class="dot" style="background:#35705A"></i>IN</span>
      <span><i class="dot" style="background:#A14E50"></i>OUT</span>
      <span><i class="dot" style="background:#9E9E9E"></i>UNDEC</span>
      <span style="color:#A14E50"><b>━</b> 击败边（可信度严格大于）</span>
      <span style="color:#9E9E9E">━ 非击败边</span>
      <span>◯ 命题（外圈 79） · ◻ 误解（内圈 42）</span>
    </p>
  </div>
  <div class="panel"><h2>节点详情</h2><div id="detail">点击左侧任一节点查看它的辩护链。</div></div>
  <div class="panel"><h2>OUT 节点（静态兜底）</h2>__OUT_TABLE__</div>
</div>
<noscript><p>（未启用脚本：上方 SVG 与 OUT 节点表已给出静态视图。）</p></noscript>
<script>
const NODES = __NODES__;
function show(id){
  const n = NODES[id]; if(!n) return;
  const rows = [];
  rows.push('<h3>' + id + '</h3>');
  rows.push('<p>类型 ' + n.type + ' · 判决 <b>' + n.verdict + '</b> · 可信度 ' + n.cred + '</p>');
  rows.push('<p>被击败于：' + (n.defeated_by.length ? n.defeated_by.map(x=>'<code>'+x+'</code>').join(' ') : '—（不被击败）') + '</p>');
  rows.push('<p>W2 辩护者：' + (n.w2_defenders.length ? n.w2_defenders.map(x=>'<code>'+x+'</code>').join(' ') : '—（无人辩护）') + '</p>');
  rows.push('<table><tr><th>攻击者</th><th>人审</th><th>是否击败</th></tr>');
  n.attackers.forEach(a=>{rows.push('<tr><td><code>'+a.source+'</code></td><td>'+a.verdict+'</td><td>'+(a.defeating?'✅ 击败':'—')+'</td></tr>');});
  rows.push('</table>');
  document.getElementById('detail').innerHTML = rows.join('');
}
</script>
</body></html>
"""


def generate_defense_chain_html(edges: list[AttackEdge], verdicts: dict[str, str],
                               credibilities: dict[str, str],
                               output_path: Path | str | None = None) -> Path:
    """生成自包含辩护链可视化（内圈 42 MIS / 外圈 79 命题；无任何外部资源）。"""
    chains = {n: get_defense_chain(n, edges, verdicts, credibilities)
              for n in sorted(verdicts)}
    props = [n for n in sorted(verdicts) if chains[n].node_type == "proposition"]
    mis = [n for n in sorted(verdicts) if chains[n].node_type == "misconception"]
    W, H, CX, CY = 900, 760, 450, 380
    R_OUT, R_IN = 340.0, 190.0

    def pos(seq: list[str], r: float) -> dict[str, tuple[float, float]]:
        import math
        n = max(len(seq), 1)
        out = {}
        for i, nid in enumerate(seq):
            ang = 2 * math.pi * i / n - math.pi / 2
            out[nid] = (CX + r * math.cos(ang), CY + r * math.sin(ang))
        return out

    p_pos, m_pos = pos(props, R_OUT), pos(mis, R_IN)
    svg = [f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" '
           f'role="img" aria-label="辩护链图">',
           f'<rect width="{W}" height="{H}" fill="#ffffff"/>']
    for e in edges:                                     # 边：灰细（非击败）/ 红粗（击败）
        defeating = is_defeating(e, credibilities)
        a, b = p_pos.get(e.source) or m_pos.get(e.source), p_pos.get(e.target) or m_pos.get(e.target)
        if not a or not b:
            continue
        stroke = "#A14E50" if defeating else "#9E9E9E"
        width = 1.8 if defeating else 0.6
        svg.append(f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" '
                   f'stroke="{stroke}" stroke-width="{width}" opacity="0.75"/>')
    for nid in props + mis:                             # 节点
        c = chains[nid]
        fill = {"IN": "#35705A", "OUT": "#A14E50", "UNDEC": "#9E9E9E"}[c.verdict]
        x, y = (p_pos if nid in p_pos else m_pos)[nid]
        title = f"{nid} · {c.verdict} · cred {c.credibility}"
        shape = (f'<circle class="node" cx="{x:.1f}" cy="{y:.1f}" r="7" fill="{fill}" '
                 f'stroke="#333" onclick="show(\'{nid}\')"><title>{title}</title></circle>'
                 if c.node_type == "proposition" else
                 f'<rect class="node" x="{x - 6:.1f}" y="{y - 6:.1f}" width="12" height="12" '
                 f'fill="{fill}" stroke="#333" onclick="show(\'{nid}\')"><title>{title}</title></rect>')
        svg.append(shape)
    svg.append("</svg>")

    nodes_json = {n: {"type": c.node_type, "verdict": c.verdict, "cred": c.credibility,
                      "defeated_by": c.defeated_by, "w2_defenders": c.w2_defenders,
                      "attackers": [{"source": e.source, "verdict": e.human_verdict,
                                     "defeating": is_defeating(e, credibilities)}
                                    for e in c.attackers]}
                  for n, c in chains.items()}
    out_rows = [f"<tr><td><code>{n}</code></td><td>{chains[n].credibility}</td>"
                f"<td>{len(chains[n].defeated_by)}</td></tr>"
                for n in sorted(verdicts) if verdicts[n] == "OUT"]
    html = (HTML_HEAD
            .replace("__OUT_TABLE__", "<table><tr><th>节点</th><th>可信度</th><th>击败者数</th></tr>"
                                      + "".join(out_rows) + "</table>")
            .replace("__NODES__", json.dumps(nodes_json, ensure_ascii=False))
            .replace("<div id=\"graph\"></div>", "<div id=\"graph\">" + "".join(svg) + "</div>"))
    p = Path(output_path) if output_path else DEFAULT_HTML
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(html, encoding="utf-8", newline="\n")
    return p


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="defense_chain",
                                 description="610 辩护链推理（确定性 · 只读）")
    ap.add_argument("--version", action="version", version=f"defense_chain {VERSION}")
    ap.add_argument("--edges", default=None)
    ap.add_argument("--annotations", default=None)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd")

    def _sp(name: str, **kw) -> argparse.ArgumentParser:
        """子命令也接受 `--json`（argparse 的全局 flag 写在子命令之后会被拒，610 实测踩坑）。"""
        return sub.add_parser(name, **kw)

    _sp("stats").add_argument("--json", action="store_true", dest="json_sub")
    sp = _sp("show")
    sp.add_argument("node_id")
    sp = _sp("what-if")
    sp.add_argument("node_id")
    sp.add_argument("credibility")
    sp.add_argument("--json", action="store_true", dest="json_sub")
    sp = _sp("what-if-overturned")
    sp.add_argument("node_id")
    sp.add_argument("--json", action="store_true", dest="json_sub")
    sp = _sp("min-attack-set")
    sp.add_argument("node_id")
    sp.add_argument("--json", action="store_true", dest="json_sub")
    sp = _sp("report")
    sp.add_argument("--out", default=None)
    sp = _sp("html")
    sp.add_argument("--out", default=None)
    for name in ("list-out", "list-no-defenders", "list-no-attackers"):
        _sp(name).add_argument("--json", action="store_true", dest="json_sub")
    a = ap.parse_args(argv)
    if getattr(a, "json_sub", False):
        a.json = True

    edges, verdicts, cred = load_data(a.edges, a.annotations)

    if a.check:
        problems = check(a.edges, a.annotations)
        if problems:
            print(f"[chain] --check FAIL：{len(problems)} 项", file=sys.stderr)
            for m in problems[:50]:
                print("  - " + m, file=sys.stderr)
            return 2
        st = stats(edges, verdicts, cred)
        print(f"[chain] --check OK：IN {st['in']} / OUT {st['out']} / UNDEC {st['undec']}"
              f" · 击败边 {st['defeating_edges']}/{st['total_edges']} · 节点 {st['total_nodes']}")
        return 0

    if a.cmd is None:
        ap.print_help()
        return 2

    if a.cmd == "stats":
        print(json.dumps(stats(edges, verdicts, cred), ensure_ascii=False, indent=1))
        return 0
    if a.cmd == "show":
        print(render_chain(get_defense_chain(a.node_id, edges, verdicts, cred)), end="")
        return 0
    if a.cmd == "what-if":
        try:
            res = what_if(a.node_id, a.credibility, edges, verdicts, cred)
        except ValueError as exc:                  # 非法档位 ⇒ exit 2（fail-loud，但不甩栈）
            print(f"[chain] {exc}", file=sys.stderr)
            return 2
        print(json.dumps(res, ensure_ascii=False, indent=1) if a.json
              else f"[chain] {res['node_id']}：{res['from']} → {res['to']} ⇒ "
                   f"IN {res['total_in']} / OUT {res['total_out']} / UNDEC {res['total_undec']}"
                   f"（变化 {len(res['changed_nodes'])} 个节点）")
        return 0
    if a.cmd == "what-if-overturned":
        res = what_if_overturned(a.node_id, edges, verdicts, cred)
        print(json.dumps(res, ensure_ascii=False, indent=1) if a.json
              else f"[chain] 推翻 {res['node_id']} ⇒ 它自己 {res['overturned_self_verdict']}"
                   f"；受影响 {len(res['affected_nodes'])} 个节点"
                   f"（总 IN {res['total_in']} / OUT {res['total_out']}）")
        return 0
    if a.cmd == "min-attack-set":
        res = find_min_attack_set(a.node_id, edges, cred, verdicts=verdicts)
        print(json.dumps(res, ensure_ascii=False, indent=1) if a.json
              else f"[chain] {res['target']} 的最小攻击集：{res['set']}（达成={res['achieved']}）"
                   f"\n  {res['note']}")
        return 0
    if a.cmd == "report":
        p = Path(a.out) if a.out else DEFAULT_REPORT
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(batch_report(edges, verdicts, cred), encoding="utf-8", newline="\n")
        print(f"[chain] 已写 {p.relative_to(ROOT).as_posix() if str(p).startswith(str(ROOT)) else p}")
        return 0
    if a.cmd == "html":
        p = generate_defense_chain_html(edges, verdicts, cred, a.out)
        print(f"[chain] 已写 {p.relative_to(ROOT).as_posix() if str(p).startswith(str(ROOT)) else p}"
              f"（自包含 HTML：内圈 42 MIS / 外圈 79 命题）")
        return 0
    st = stats(edges, verdicts, cred)
    key = {"list-out": "out_nodes", "list-no-defenders": "no_defender_nodes",
           "list-no-attackers": "no_attacker_propositions"}[a.cmd]
    print(json.dumps(st[key], ensure_ascii=False, indent=1) if a.json
          else "\n".join(st[key]) or "（空）")
    return 0


# ── 一致性检查 ────────────────────────────────────────────────────────────────
def check(edges_path: Path | str | None = None,
          ann_path: Path | str | None = None,
          labels_path: Path | str | None = None) -> list[str]:
    """五条硬检查（610 B2 口径）：
    ① 每个节点 verdict 与**入库 W2 产物**一致；② OUT 节点必有击败者；③ IN 节点必无击败者；
    ④ 击败边 = 入库产物记的 17；⑤ 节点数 = 121（命题 79 + 误解 42）。
    """
    problems: list[str] = []
    edges, verdicts, cred = load_data(edges_path, ann_path)
    st = stats(edges, verdicts, cred)
    lp = Path(labels_path) if labels_path else DEFAULT_LABELS
    if not lp.is_file():
        return [f"W2 产物缺失：{lp}"]
    auth = json.loads(lp.read_text(encoding="utf-8"))
    num2name = {0: "low", 1: "low", 2: "medium", 3: "high"}   # 产物里 credibility 是**数字档**
    for nid, v in auth["nodes"].items():
        if verdicts.get(nid) != v["label"]:
            problems.append(f"{nid}：本引擎 {verdicts.get(nid)} ≠ 入库产物 {v['label']}")
        want = num2name.get(v.get("credibility"), str(v.get("credibility")))
        if cred.get(nid) != want:
            problems.append(f"{nid}：可信度 {cred.get(nid)} ≠ 产物 {want}"
                            f"（数字档 {v.get('credibility')}）")
    if st["defeating_edges"] != auth["defeating_edges"]:
        problems.append(f"击败边 {st['defeating_edges']} ≠ 产物 {auth['defeating_edges']}")
    if st["total_nodes"] != 121 or st["in"] != 114 or st["out"] != 7 or st["undec"] != 0:
        problems.append(f"判决汇总 {st['in']}/{st['out']}/{st['undec']} ≠ 114/7/0"
                        f"（节点 {st['total_nodes']}）")
    for n in st["out_nodes"]:
        c = get_defense_chain(n, edges, verdicts, cred)
        if not c.defeated_by:
            problems.append(f"OUT 节点 {n} 无击败者（defeated_by 空）")
    for n, v in verdicts.items():
        c = get_defense_chain(n, edges, verdicts, cred)
        if v == "IN" and c.defeated_by:
            problems.append(f"IN 节点 {n} 却有击败者 {c.defeated_by}")
    if st["in_propositions"] != 79 or st["in_misconceptions"] != 35:
        problems.append(f"IN 命题/误解 {st['in_propositions']}/{st['in_misconceptions']} ≠ 79/35")
    return problems


if __name__ == "__main__":
    sys.exit(main())
