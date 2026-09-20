"""610 C1 · 论证漏洞检测（智能原型 2：**结构级**自检，纯标准库 · 只读 · 零 Oracle 风险）。

从"验证单条内容"升到"验证整个论证结构"：从辩护链（610 B1）出发找**结构性漏洞**。

C1 的五个基础探测器：
  * `detect_no_attacker_propositions`：没有任何误解攻击它的命题（论证盲区）；
  * `detect_no_defender_mis`：**OUT 且无辩护者**的 MIS（被判错却没人替它挡）；
  * `detect_isolated_subgraphs`：连通分量（含只由 1 个节点组成的孤立子图）；
  * `detect_unreviewed_edges`：尚未人审的边（人审全量后应为 0）；
  * `detect_credibility_gaps`：可信度档位分布缺口（最大档 `high` 为空 ⇒ OUT 的 MIS 无高可信辩护者可用）。

⚠️ 口径（610 实测）：**辩护者 = W2 意义的辩护者**（IN 且攻击了"攻击我的攻击者"）。
任务书写"7 个无辩护者 MIS"，实测是 **1 个**（`MIS-LANG-001`；另 2 个空辩护者是**未 OUT** 的 MIS，
4 个是命题）⇒ 本工具按实测给数，并在报告里登记该偏差。

CLI：no-attackers / no-defenders / isolated / unreviewed / credibility-gaps / --check
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import defense_chain as dc  # noqa: E402

VERSION = "1.0"
CRED_ORDER = dc.CREDIBILITY_ORDER


# ── 数据 ──────────────────────────────────────────────────────────────────────
def load_state(edges_path: Path | str | None = None,
               ann_path: Path | str | None = None):
    """→ (edges, verdicts, credibilities)；全部走 610 B1 的同一口径（单一真源）。"""
    return dc.load_data(edges_path, ann_path)


def all_nodes(verdicts: dict[str, str], edges: list[dc.AttackEdge]) -> list[str]:
    """图里的节点全集 = 出现过边的节点 ∪ 判决表里的节点（**含 4 个无边的命题**）。"""
    nodes = set(verdicts)
    for e in edges:
        nodes.add(e.source)
        nodes.add(e.target)
    return sorted(nodes)


# ── 五个基础探测器 ────────────────────────────────────────────────────────────
def detect_no_attacker_propositions(edges: list[dc.AttackEdge],
                                    all_propositions: list[str]) -> list[str]:
    """无任何入边的命题（＝没有任何误解攻击它）。"""
    attacked = {e.target for e in edges}
    return sorted(p for p in all_propositions if p not in attacked)


def detect_no_defender_mis(edges: list[dc.AttackEdge], verdicts: dict[str, str],
                           credibilities: dict[str, str]) -> list[str]:
    """**OUT 且 W2 辩护者为空**的 MIS（被判错且无人替它挡刀）。"""
    out_mis = [n for n in sorted(verdicts)
               if verdicts[n] == "OUT" and dc.node_type_of(n, edges) == "misconception"]
    return [n for n in out_mis
            if not dc.get_defense_chain(n, edges, verdicts, credibilities).w2_defenders]


def detect_no_defender_nodes(edges: list[dc.AttackEdge], verdicts: dict[str, str],
                             credibilities: dict[str, str]) -> list[str]:
    """**任意类型**的无辩护者节点（含 4 个孤立命题）⇒ 610 实测 7 个。"""
    return sorted(n for n in verdicts
                  if not dc.get_defense_chain(n, edges, verdicts, credibilities).w2_defenders)


def detect_isolated_subgraphs(edges: list[dc.AttackEdge], nodes: list[str]) -> list[list[str]]:
    """连通分量（忽略方向）。只由 1 个节点组成的分量 = 孤立子图。"""
    adj: dict[str, set[str]] = {n: set() for n in nodes}
    for e in edges:
        if e.source in adj and e.target in adj:
            adj[e.source].add(e.target)
            adj[e.target].add(e.source)
    seen: set[str] = set()
    comps: list[list[str]] = []
    for n in nodes:
        if n in seen:
            continue
        q = deque([n])
        seen.add(n)
        comp: list[str] = []
        while q:
            cur = q.popleft()
            comp.append(cur)
            for nxt in sorted(adj.get(cur, ())):
                if nxt not in seen:
                    seen.add(nxt)
                    q.append(nxt)
        comps.append(sorted(comp))
    comps.sort(key=lambda c: (len(c), c[0]))
    return comps


def detect_unreviewed_edges(edges: list[dc.AttackEdge]) -> list[dc.AttackEdge]:
    """未人审的边（`human_verdict == "unreviewed"`）。"""
    return [e for e in edges if e.human_verdict == "unreviewed"]


def detect_credibility_gaps(credibilities: dict[str, str]) -> dict:
    """可信度档位分布 + 缺口（`high` 为空 ⇒ 无法用高可信节点为 OUT 的 MIS 提供辩护）。"""
    dist = {k: sum(1 for v in credibilities.values() if v == k) for k in ("high", "medium", "low")}
    gaps: list[str] = []
    if dist["high"] == 0:
        gaps.append("无 `high` 可信度节点 ⇒ 结构性缺口：任何 OUT 的 MIS 都拿不到高可信辩护者")
    return {"distribution": dist, "gaps": gaps, "total": len(credibilities)}


# ── CLI ───────────────────────────────────────────────────────────────────────
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="argument_audit",
                                 description="610 论证漏洞检测（只读 · 纯标准库）")
    ap.add_argument("--version", action="version", version=f"argument_audit {VERSION}")
    ap.add_argument("--edges", default=None)
    ap.add_argument("--annotations", default=None)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd")
    for name in ("no-attackers", "no-defenders", "isolated", "unreviewed",
                 "credibility-gaps"):
        sp = sub.add_parser(name)
        sp.add_argument("--json", action="store_true", dest="json_sub")
    a = ap.parse_args(argv)
    if getattr(a, "json_sub", False):
        a.json = True

    edges, verdicts, cred = load_state(a.edges, a.annotations)
    nodes = all_nodes(verdicts, edges)

    if a.check:
        problems = check(a.edges, a.annotations)
        if problems:
            print(f"[audit] --check FAIL：{len(problems)} 项", file=sys.stderr)
            for m in problems[:50]:
                print("  - " + m, file=sys.stderr)
            return 2
        print("[audit] --check OK：五个基础探测器与 W2 产物自洽（无攻击者 4 · OUT 无辩护者 1 · "
              "无辩护者合计 7 · 未审边 0 · 分量 11（孤立 4，最大 80）· "
              "可信度 high 0/medium 114/low 7）")
        return 0

    if a.cmd is None:
        ap.print_help()
        return 2

    if a.cmd == "no-attackers":
        props = [n for n in verdicts if dc.node_type_of(n, edges) == "proposition"]
        res = detect_no_attacker_propositions(edges, props)
    elif a.cmd == "no-defenders":
        res = detect_no_defender_mis(edges, verdicts, cred)
    elif a.cmd == "isolated":
        comps = detect_isolated_subgraphs(edges, nodes)
        res = [c for c in comps if len(c) == 1]
    elif a.cmd == "unreviewed":
        res = [e.edge_id for e in detect_unreviewed_edges(edges)]
    else:
        res = detect_credibility_gaps(cred)
    print(json.dumps(res, ensure_ascii=False, indent=1) if a.json
          else ("\n".join(map(str, res)) if isinstance(res, list) else json.dumps(
              res, ensure_ascii=False, indent=1)))
    return 0


def check(edges_path: Path | str | None = None,
          ann_path: Path | str | None = None) -> list[str]:
    problems: list[str] = []
    edges, verdicts, cred = load_state(edges_path, ann_path)
    nodes = all_nodes(verdicts, edges)
    props = [n for n in verdicts if dc.node_type_of(n, edges) == "proposition"]
    na = detect_no_attacker_propositions(edges, props)
    if len(na) != 4:
        problems.append(f"无攻击者命题应为 4（实测 {len(na)}）")
    nd_mis = detect_no_defender_mis(edges, verdicts, cred)
    if nd_mis != ["MIS-LANG-001"]:
        problems.append(f"OUT 且无辩护者的 MIS 应为 ['MIS-LANG-001']（实测 {nd_mis}）")
    nd_all = detect_no_defender_nodes(edges, verdicts, cred)
    if len(nd_all) != 7:
        problems.append(f"无辩护者节点总数应为 7（实测 {len(nd_all)}）")
    un = detect_unreviewed_edges(edges)
    if un:
        problems.append(f"存在未人审边 {len(un)} 条（人审全量后应为 0）")
    gaps = detect_credibility_gaps(cred)
    if gaps["distribution"] != {"high": 0, "medium": 114, "low": 7}:
        problems.append(f"可信度分布非 {({'high': 0, 'medium': 114, 'low': 7})}："
                        f"{gaps['distribution']}")
    comps = detect_isolated_subgraphs(edges, nodes)
    singles = [c for c in comps if len(c) == 1]
    sizes = sorted((len(c) for c in comps), reverse=True)
    if len(singles) != 4 or len(comps) != 11:
        problems.append(f"连通分量应为 11（其中孤立 4）（实测 分量 {len(comps)} / 孤立 {len(singles)}）")
    if sizes[0] != 80:
        problems.append(f"最大连通分量应为 80 节点（实测 {sizes[0]}）⇒ 论证图碎片化程度变了")
    if len(nodes) != 121:
        problems.append(f"节点全集应为 121（实测 {len(nodes)}）")
    return problems


if __name__ == "__main__":
    sys.exit(main())
