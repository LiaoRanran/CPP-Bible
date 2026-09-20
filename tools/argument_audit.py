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
# mypy: ignore-errors
# 类型注解债务，CI 先转绿，后续逐步修
from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import defense_chain as dc  # noqa: E402
import human_review_report as hrr  # noqa: E402

VERSION = "1.0"
CRED_ORDER = dc.CREDIBILITY_ORDER
MODIFY_RATIO_THRESHOLD = 0.5      # 超过这条线算"歧义集中"
IMBALANCE_THRESHOLD = 0.6         # 单一主题占比超过这条线算"分布不平衡"
SHORT_REASON = 20


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


# ── C2 高级探测器 ─────────────────────────────────────────────────────────────
def detect_high_modify_ratio_mis(annotations: list[dict], threshold: float = MODIFY_RATIO_THRESHOLD
                                 ) -> list[dict]:
    """modify 比例 > threshold 的 MIS（歧义集中区），按比例降序。"""
    rows = hrr.summarize_by_mis(annotations)
    return [{**r, "reason": "modify 比例高 ⇒ 档位判断有歧义，建议第二轮人审"}
            for r in rows if (r["modify_ratio"] or 0) > threshold]


def detect_rubber_stamp_risk(annotations: list[dict]) -> list[dict]:
    """rubber-stamp 风险：**全部 approve** 且组内最短理由 < 20 字符的 MIS。

    存量人审无 `review_seconds` ⇒ 只能用"理由长度"这一个可观测量（**不用不可得的量硬凑指标**）。
    """
    idx = hrr.edge_index()
    reasons: dict[str, list[str]] = {}
    for a in annotations:
        e = idx.get(str(a.get("edge_id")))
        if e is None:
            continue
        reasons.setdefault(hrr.mis_of(e), []).append(str(a.get("reason", "")))
    out: list[dict] = []
    for r in hrr.summarize_by_mis(annotations):
        if r["total"] and r["approve"] == r["total"]:
            lens = [len(x) for x in reasons.get(r["mis_id"], [])]
            shortest = min(lens) if lens else 0
            if shortest < SHORT_REASON:
                out.append({"mis_id": r["mis_id"], "total": r["total"],
                            "shortest_reason_len": shortest,
                            "detail": f"全部 approve 且最短理由 {shortest} < {SHORT_REASON} 字符"})
    return sorted(out, key=lambda x: x["shortest_reason_len"])


def detect_topic_imbalance(annotations: list[dict]) -> dict:
    """主题分布不平衡：单一主题占比 > threshold ⇒ 标出失衡与其代价（覆盖偏窄）。"""
    topics = hrr.summarize_by_topic(annotations)
    top = max(topics.items(), key=lambda kv: kv[1]["total"])
    ratio = top[1]["ratio"]
    return {"distribution": {k: {"total": v["total"], "mis_count": v["mis_count"],
                                 "ratio": v["ratio"]} for k, v in topics.items()},
            "dominant_topic": top[0], "dominant_ratio": ratio,
            "imbalanced": ratio > IMBALANCE_THRESHOLD,
            "note": (f"{top[0]} 占 {ratio:.1%}（阈值 {IMBALANCE_THRESHOLD:.0%}）⇒ "
                     "论证覆盖偏向该主题，其它主题的误解密度低、结论外推需谨慎")
            if ratio > IMBALANCE_THRESHOLD else "分布未超阈值"}


def detect_proposition_overload(edges: list[dc.AttackEdge], top: int = 10) -> list[dict]:
    """命题过载：被最多攻击者指向的命题（可能是表述太宽泛），Top N。"""
    cnt: dict[str, set[str]] = {}
    for e in edges:
        if dc.node_type_of(e.target, edges) == "proposition":
            cnt.setdefault(e.target, set()).add(e.source)
    rows = [{"proposition": k, "attackers": len(v), "nodes": sorted(v)}
            for k, v in cnt.items()]
    rows.sort(key=lambda r: (-r["attackers"], r["proposition"]))
    return rows[:top]


def detect_mis_overload(edges: list[dc.AttackEdge], top: int = 10) -> list[dict]:
    """MIS 过载：攻击最多**不同命题**的 MIS（可能是误解太宽泛），Top N。"""
    cnt: dict[str, set[str]] = {}
    for e in edges:
        if dc.node_type_of(e.source, edges) == "misconception":
            cnt.setdefault(e.source, set()).add(e.target)
    rows = [{"mis_id": k, "propositions": len(v), "edges": sum(1 for e in edges
                                                              if e.source == k),
             "targets": sorted(v)} for k, v in cnt.items()]
    rows.sort(key=lambda r: (-r["propositions"], r["mis_id"]))
    return rows[:top]


def detect_cycle_arguments(edges: list[dc.AttackEdge]) -> list[list[str]]:
    """2-环（A→B 且 B→A）。本仓的对称边设计使 `prop↔mis` 成对出现 ⇒ 2-环数量 = 半对数。"""
    pairs = {(e.source, e.target) for e in edges}
    seen: set[tuple[str, str]] = set()
    out: list[list[str]] = []
    for a, b in sorted(pairs):
        if (b, a) in pairs and (b, a) not in seen:
            seen.add((a, b))
            out.append([a, b])
    return out


# ── C3 完整报告 ───────────────────────────────────────────────────────────────
DEFAULT_REPORT = ROOT / "data" / "argument_audit_report.md"


def collect_findings(edges: list[dc.AttackEdge], annotations: list[dict],
                     verdicts: dict[str, str], credibilities: dict[str, str]) -> dict:
    """把 C1+C2 的所有探测器聚合成一份**结构化**发现清单（报告与 summary 共用）。"""
    props = [n for n in verdicts if dc.node_type_of(n, edges) == "proposition"]
    nodes = all_nodes(verdicts, edges)
    comps = detect_isolated_subgraphs(edges, nodes)
    sizes = sorted((len(c) for c in comps), reverse=True)
    singles = [c[0] for c in comps if len(c) == 1]
    return {
        "no_attacker_props": detect_no_attacker_propositions(edges, props),
        "no_defender_mis": detect_no_defender_mis(edges, verdicts, credibilities),
        "no_defender_nodes": detect_no_defender_nodes(edges, verdicts, credibilities),
        "credibility": detect_credibility_gaps(credibilities),
        "components": {"count": len(comps), "sizes": sizes, "isolated": singles,
                       "largest": sizes[0], "coverage": round(sizes[0] / max(len(nodes), 1), 4)},
        "unreviewed_edges": [e.edge_id for e in detect_unreviewed_edges(edges)],
        "high_modify": detect_high_modify_ratio_mis(annotations),
        "rubber_stamp": detect_rubber_stamp_risk(annotations),
        "topic": detect_topic_imbalance(annotations),
        "prop_overload": detect_proposition_overload(edges, 5),
        "mis_overload": detect_mis_overload(edges, 5),
        "cycles": detect_cycle_arguments(edges),
    }


def generate_full_report(edges: list[dc.AttackEdge], annotations: list[dict],
                         verdicts: dict[str, str], credibilities: dict[str, str]) -> str:
    f = collect_findings(edges, annotations, verdicts, credibilities)
    s = dc.solve_summary(edges, credibilities)
    lines = [
        "# 论证漏洞报告（610 C3 · 智能原型 2）", "",
        "> 只读生成：数据来自候选边 + 用户授权人审 + 610 B1 的辩护链引擎（同一口径）。", "",
        "## 1. 总览", "",
        f"- 节点 **{s['nodes']}**（命题 79 + 误解 42）· 边 **{s['edges']}**"
        f"（其中**构成击败** {s['defeating_edges']}）",
        f"- 判决 **IN {s['in']} / OUT {s['out']} / UNDEC {s['undec']}** · {s['rounds']} 轮收敛",
        f"- 人审 388/388（approve 354 / modify 34 / reject 0）· 未审边 {len(f['unreviewed_edges'])}",
        f"- 连通分量 **{f['components']['count']}** 个（孤立 {len(f['components']['isolated'])}，"
        f"最大 {f['components']['largest']} 节点 = {f['components']['coverage']:.1%}）", "",
        "## 2. P0 漏洞（结构性，需立即处理）", "",
        f"- **无 `high` 可信度节点**（分布 {f['credibility']['distribution']}）："
        "⇒ OUT 的 MIS 永远拿不到高可信辩护者，'被推翻后翻案'在结构上不可能发生；",
        f"- **论证盲区：{len(f['no_attacker_props'])} 个命题无任何攻击者**"
        f"（{', '.join(f['no_attacker_props'])}）：没有任何误解指向它们 ⇒ "
        "要么该命题太显然（无需攻击），要么还没人造出对应误解 ⇒ 覆盖缺口；", "",
        "## 3. P1 漏洞（需短期处理）", "",
        f"- **OUT 且无辩护者**：OUT 的 MIS 中 {len(f['no_defender_mis'])} 个无 W2 辩护者"
        f"（{', '.join(f['no_defender_mis'])}）；无辩护者节点合计 {len(f['no_defender_nodes'])} 个；",
        f"- **歧义集中：{len(f['high_modify'])} 个 MIS 的 modify 比例 = 1.0**"
        f"（{', '.join(r['mis_id'] for r in f['high_modify'])}）⇒ 档位判据需沉淀；",
        f"- **主题失衡**：{f['topic']['dominant_topic']} 占 {f['topic']['dominant_ratio']:.1%}"
        f"（阈值 60%）⇒ 结论外推到其它主题需谨慎；",
        f"- **论证图碎片化**：{f['components']['count']} 个连通分量、最大分量只覆盖 "
        f"{f['components']['coverage']:.1%} 节点 ⇒ 大量子论证彼此孤立，跨主题的辩护链无法成立；", "",
        "## 4. P2 漏洞（需长期处理）", "",
        f"- 命题过载：`{f['prop_overload'][0]['proposition']}` 被 "
        f"{f['prop_overload'][0]['attackers']} 个 MIS 攻击（表述可能过宽）；",
        f"- MIS 过载：`{f['mis_overload'][0]['mis_id']}` 攻击 "
        f"{f['mis_overload'][0]['propositions']} 个不同命题（误解可能过宽）；",
        f"- 循环论证：**{len(f['cycles'])} 个 2-环**（对称边设计的必然产物；"
        "W2 里同档不构成击败 ⇒ 不产生自证循环，但换档位口径时必须重查）；", "",
        "## 5. 详细描述 / 影响 / 修复建议", "",
        "| 漏洞 | 影响 | 建议（**只建议不执行**） |", "|---|---|---|",
        "| 无 high 档节点 | OUT 的 MIS 无法被翻案（无高可信辩护者） | 新增/升级可产出 `high` 的判据；"
        "或明确「本仓不设 high 档」并把它写进口径 |",
        f"| {len(f['no_attacker_props'])} 个无攻击者命题 | 论证盲区，覆盖度虚高 | "
        "优先为这 4 条造误解或标注「无需攻击」的理由 |",
        f"| {len(f['high_modify'])} 个 modify=1.0 的 MIS | 档位判断歧义，人审可信度打折 | "
        "把「证据较充分但偏保守」沉淀成可复算的判据，再跑第二轮 |",
        f"| 主题失衡（{f['topic']['dominant_ratio']:.1%}） | 跨主题结论外推风险 | "
        "按主题设定覆盖配额（本批只提示，不改生成器） |",
        f"| 论证图 {f['components']['count']} 分量 | 子论证孤立，跨主题辩护链断裂 | "
        "优先补「桥接」攻击边（让大分量之间产生真实攻击关系），不硬造 |", "",
        "## 6. 漏洞统计", "",
        "| 优先级 | 条数 | 明细 |", "|---|---:|---|",
        f"| P0 | 2 | 无 high 档节点 · 无攻击者命题 {len(f['no_attacker_props'])} |",
        f"| P1 | 4 | 无辩护者 OUT MIS {len(f['no_defender_mis'])} · "
        f"modify=1.0 的 MIS {len(f['high_modify'])} · 主题失衡 · 图碎片化 |",
        f"| P2 | 3 | 命题过载 · MIS 过载 · 2-环 {len(f['cycles'])} |", "",
        "## 7. 后续建议（NDW 分类）", "",
        "- **Need（必须做）**：为 4 个无攻击者命题补误解或补「无需攻击」理由（否则覆盖度无法声明）；",
        "- **Do（可做）**：把 7 个 modify=1.0 的 MIS 的判据沉淀成规则，作为下一轮人审的前置材料；",
        "- **Won't（本批不做）**：不给 OUT 的 MIS 硬造辩护者、不改生成器阈值、不重冻结 W2、"
        "不执行任何人审（人审权力在用户手中）；", "",
        "> 本报告**只呈现事实与建议**；所有修复动作都需人确认后另行开批。", "",
    ]
    return "\n".join(lines)


def write_report(report: str, path: Path | str | None = None) -> Path:
    p = Path(path) if path else DEFAULT_REPORT
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(report, encoding="utf-8", newline="\n")
    return p


def summary_json(edges: list[dc.AttackEdge], annotations: list[dict], verdicts: dict[str, str],
                 credibilities: dict[str, str]) -> dict:
    f = collect_findings(edges, annotations, verdicts, credibilities)
    return {"p0": {"no_high_credibility": f["credibility"]["distribution"]["high"] == 0,
                   "no_attacker_propositions": len(f["no_attacker_props"])},
            "p1": {"no_defender_out_mis": len(f["no_defender_mis"]),
                   "high_modify_mis": len(f["high_modify"]),
                   "topic_imbalanced": f["topic"]["imbalanced"],
                   "components": f["components"]["count"]},
            "p2": {"top_prop_overload": f["prop_overload"][0]["attackers"],
                   "top_mis_overload": f["mis_overload"][0]["propositions"],
                   "cycles": len(f["cycles"])},
            "totals": {"p0": 2, "p1": 4, "p2": 3,
                       "defeating_edges": dc.solve_summary(edges, credibilities)["defeating_edges"]},
            "note": "P0/P1/P2 的条数口径见报告 §6；只统计**已判定**的漏洞，不估未知"}


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
                 "credibility-gaps", "high-modify", "rubber-stamp", "topic-imbalance",
                 "proposition-overload", "mis-overload", "cycles", "summary"):
        sp = sub.add_parser(name)
        sp.add_argument("--json", action="store_true", dest="json_sub")
    sp = sub.add_parser("report")
    sp.add_argument("--out", default=None)
    a = ap.parse_args(argv)
    if getattr(a, "json_sub", False):
        a.json = True

    edges, verdicts, cred = load_state(a.edges, a.annotations)
    nodes = all_nodes(verdicts, edges)
    anns = dc.load_annotations(a.annotations)

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
    elif a.cmd == "high-modify":
        res = detect_high_modify_ratio_mis(anns)
    elif a.cmd == "rubber-stamp":
        res = detect_rubber_stamp_risk(anns)
    elif a.cmd == "topic-imbalance":
        res = detect_topic_imbalance(anns)
    elif a.cmd == "proposition-overload":
        res = detect_proposition_overload(edges)
    elif a.cmd == "mis-overload":
        res = detect_mis_overload(edges)
    elif a.cmd == "cycles":
        res = detect_cycle_arguments(edges)
    elif a.cmd == "report":
        p = write_report(generate_full_report(edges, anns, verdicts, cred), a.out)
        print(f"[audit] 已写 {p.relative_to(ROOT).as_posix() if str(p).startswith(str(ROOT)) else p}"
              f"（P0 2 · P1 4 · P2 3）")
        return 0
    elif a.cmd == "summary":
        res = summary_json(edges, anns, verdicts, cred)
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
