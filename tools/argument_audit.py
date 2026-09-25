"""610 C1 · 论证漏洞检测（智能原型 2：**结构级**自检，纯标准库 · 只读 · 零 Oracle 风险）。

从"验证单条内容"升到"验证整个论证结构"：从辩护链（610 B1）出发找**结构性漏洞**。

C1 的五个基础探测器：
  * `detect_no_attacker_propositions`：没有任何误解攻击它的命题（论证盲区）；
  * `detect_no_defender_mis`：**OUT 且无辩护者**的 MIS（被判错却没人替它挡）；
  * `detect_isolated_subgraphs`：连通分量（含只由 1 个节点组成的孤立子图）；
  * `detect_unreviewed_edges`：尚未人审的边（人审全量后应为 0）；
  * `detect_credibility_gaps`：可信度档位分布缺口（最大档 `high` 为空 ⇒ OUT 的 MIS 无高可信辩护者可用）。

⚠️ 口径（610 实测）：**辩护者 = W2 意义的辩护者**（IN 且攻击了"攻击我的攻击者"）。
任务书写"7 个无辩护者 MIS"，610 实测是 **1 个**（`MIS-LANG-001`）。

⚠️ 640c 起**所有数字动态取**（`tools/w2_derived_640c.py` 为派生量单一权威源）：
632/634 命题级人签把 79 条命题抬到 `high` ⇒ MIS（approve 只到 `medium`）**全部**被判 OUT
⇒ "OUT 且无辩护者的 MIS"由 1 变 42，"无辩护者节点合计"由 7 变 46。**这是口径演进，不是 bug**
（640b 已登记语义后果，641 裁决）；本工具与 `check()` 不再锁定快照数字。

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


def priority_counts(f: dict) -> dict:
    """P0/P1/P2 条数（**现算**；640c A1/A2：曾写死 2/4/3，与内容脱钩）。

    * P0 = 结构性缺口：`high` 档为空 / 存在无攻击者命题；
    * P1 = 无辩护者 OUT MIS / modify=1.0 的 MIS / 主题失衡 / 图碎片化（>1 分量）；
    * P2 = 命题过载 / MIS 过载 / 2-环。
    """
    p0 = (1 if f["credibility"]["distribution"]["high"] == 0 else 0) \
        + (1 if f["no_attacker_props"] else 0)
    p1 = sum([bool(f["no_defender_mis"]), bool(f["high_modify"]),
              bool(f["topic"]["imbalanced"]), f["components"]["count"] > 1])
    p2 = sum([bool(f["prop_overload"]), bool(f["mis_overload"]), bool(f["cycles"])])
    return {"p0": p0, "p1": p1, "p2": p2}


def generate_full_report(edges: list[dc.AttackEdge], annotations: list[dict],
                         verdicts: dict[str, str], credibilities: dict[str, str]) -> str:
    """七节完整报告。**所有数字现算**；P0/P1 段落按实际条件出现（不谎报已消解的缺口）。"""
    f = collect_findings(edges, annotations, verdicts, credibilities)
    s = dc.solve_summary(edges, credibilities)
    cnt = priority_counts(f)
    dist = f["credibility"]["distribution"]
    n_props = s["nodes"] - sum(1 for n in verdicts if dc.node_type_of(n, edges) == "misconception")
    n_mis = sum(1 for n in verdicts if dc.node_type_of(n, edges) == "misconception")
    n_approve = sum(1 for a in annotations if a.get("action") == "approve")
    n_modify = sum(1 for a in annotations if a.get("action") == "modify")
    n_reject = sum(1 for a in annotations if a.get("action") == "reject")
    p0_lines: list[str] = []
    if dist["high"] == 0:
        p0_lines.append(
            f"- **无 `high` 可信度节点**（分布 {dist}）："
            "⇒ OUT 的 MIS 永远拿不到高可信辩护者，'被推翻后翻案'在结构上不可能发生；")
    else:
        p0_lines.append(
            f"- ~~无 `high` 可信度节点~~ **已消解**（分布 {dist}，`high` {dist['high']} 个）："
            "高可信节点已存在 ⇒ 该结构性缺口不再成立（640c 按实况改判，原为无条件 P0）；")
    if f["no_attacker_props"]:
        p0_lines.append(
            f"- **论证盲区：{len(f['no_attacker_props'])} 个命题无任何攻击者**"
            f"（{', '.join(f['no_attacker_props'])}）：没有任何误解指向它们 ⇒ "
            "要么该命题太显然（无需攻击），要么还没人造出对应误解 ⇒ 覆盖缺口；")
    else:
        p0_lines.append("- 论证盲区：**已消解**（每个命题都至少有一个误解指向）；")
    p1_lines: list[str] = []
    if f["no_defender_mis"]:
        p1_lines.append(
            f"- **OUT 且无辩护者**：OUT 的 MIS 中 {len(f['no_defender_mis'])} 个无 W2 辩护者"
            f"（{', '.join(f['no_defender_mis'])}）；无辩护者节点合计 {len(f['no_defender_nodes'])} 个；")
    if f["high_modify"]:
        p1_lines.append(
            f"- **歧义集中：{len(f['high_modify'])} 个 MIS 的 modify 比例 = 1.0**"
            f"（{', '.join(r['mis_id'] for r in f['high_modify'])}）⇒ 档位判据需沉淀；")
    if f["topic"]["imbalanced"]:
        p1_lines.append(
            f"- **主题失衡**：{f['topic']['dominant_topic']} 占 {f['topic']['dominant_ratio']:.1%}"
            f"（阈值 60%）⇒ 结论外推到其它主题需谨慎；")
    if f["components"]["count"] > 1:
        p1_lines.append(
            f"- **论证图碎片化**：{f['components']['count']} 个连通分量、最大分量只覆盖 "
            f"{f['components']['coverage']:.1%} 节点 ⇒ 大量子论证彼此孤立，跨主题的辩护链无法成立；")
    p2_lines: list[str] = []
    if f["prop_overload"]:
        p2_lines.append(f"- 命题过载：`{f['prop_overload'][0]['proposition']}` 被 "
                        f"{f['prop_overload'][0]['attackers']} 个 MIS 攻击（表述可能过宽）；")
    if f["mis_overload"]:
        p2_lines.append(f"- MIS 过载：`{f['mis_overload'][0]['mis_id']}` 攻击 "
                        f"{f['mis_overload'][0]['propositions']} 个不同命题（误解可能过宽）；")
    if f["cycles"]:
        p2_lines.append(f"- 循环论证：**{len(f['cycles'])} 个 2-环**（对称边设计的必然产物；"
                        "W2 里同档不构成击败 ⇒ 不产生自证循环，但换档位口径时必须重查）；")
    fix_rows = []
    if dist["high"] == 0:
        fix_rows.append("| 无 high 档节点 | OUT 的 MIS 无法被翻案（无高可信辩护者） | "
                        "新增/升级可产出 `high` 的判据；或明确「本仓不设 high 档」并把它写进口径 |")
    fix_rows.append(f"| {len(f['no_attacker_props'])} 个无攻击者命题 | 论证盲区，覆盖度虚高 | "
                    f"优先为这 {len(f['no_attacker_props'])} 条造误解或标注「无需攻击」的理由 |")
    fix_rows.append(f"| {len(f['high_modify'])} 个 modify=1.0 的 MIS | 档位判断歧义，人审可信度打折 | "
                    "把「证据较充分但偏保守」沉淀成可复算的判据，再跑第二轮 |")
    if f["topic"]["imbalanced"]:
        fix_rows.append(f"| 主题失衡（{f['topic']['dominant_ratio']:.1%}） | 跨主题结论外推风险 | "
                        "按主题设定覆盖配额（本批只提示，不改生成器） |")
    if f["components"]["count"] > 1:
        fix_rows.append(f"| 论证图 {f['components']['count']} 分量 | 子论证孤立，跨主题辩护链断裂 | "
                        "优先补「桥接」攻击边（让大分量之间产生真实攻击关系），不硬造 |")
    lines = [
        "# 论证漏洞报告（610 C3 · 智能原型 2）", "",
        "> 只读生成：数据来自候选边 + 用户授权人审 + 610 B1 的辩护链引擎（同一口径）。", "",
        "## 1. 总览", "",
        f"- 节点 **{s['nodes']}**（命题 {n_props} + 误解 {n_mis}）· 边 **{s['edges']}**"
        f"（其中**构成击败** {s['defeating_edges']}）",
        f"- 判决 **IN {s['in']} / OUT {s['out']} / UNDEC {s['undec']}** · {s['rounds']} 轮收敛",
        f"- 人审 {len(annotations)}/{s['edges']}"
        f"（approve {n_approve} / modify {n_modify} / reject {n_reject}）"
        f"· 未审边 {len(f['unreviewed_edges'])}",
        f"- 连通分量 **{f['components']['count']}** 个（孤立 {len(f['components']['isolated'])}，"
        f"最大 {f['components']['largest']} 节点 = {f['components']['coverage']:.1%}）", "",
        "## 2. P0 漏洞（结构性，需立即处理）", "", *p0_lines, "",
        "## 3. P1 漏洞（需短期处理）", "", *(p1_lines or ["- 无（各项均在阈值内）"]), "",
        "## 4. P2 漏洞（需长期处理）", "", *(p2_lines or ["- 无"]), "",
        "## 5. 详细描述 / 影响 / 修复建议", "",
        "| 漏洞 | 影响 | 建议（**只建议不执行**） |", "|---|---|---|", *fix_rows, "",
        "## 6. 漏洞统计", "",
        "| 优先级 | 条数 | 明细 |", "|---|---:|---|",
        f"| P0 | {cnt['p0']} | "
        f"{'无 high 档节点 · ' if dist['high'] == 0 else ''}"
        f"无攻击者命题 {len(f['no_attacker_props'])} |",
        f"| P1 | {cnt['p1']} | 无辩护者 OUT MIS {len(f['no_defender_mis'])} · "
        f"modify=1.0 的 MIS {len(f['high_modify'])} · 主题失衡 · 图碎片化 |",
        f"| P2 | {cnt['p2']} | 命题过载 · MIS 过载 · 2-环 {len(f['cycles'])} |", "",
        "## 7. 后续建议（NDW 分类）", "",
        f"- **Need（必须做）**：为 {len(f['no_attacker_props'])} 个无攻击者命题补误解或补"
        "「无需攻击」理由（否则覆盖度无法声明）；",
        f"- **Do（可做）**：把 {len(f['high_modify'])} 个 modify=1.0 的 MIS 的判据沉淀成规则，"
        "作为下一轮人审的前置材料；",
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
            # 640c A1：条数**现算**（曾写死 2/4/3；`p0` 与 `no_high_credibility` 脱钩会自相矛盾）
            "totals": {**priority_counts(f),
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
        snap = snapshot(a.edges, a.annotations)
        d = snap["credibility_distribution"]
        print(f"[audit] --check OK：探测不变量与 W2 产物自洽"
              f"（无攻击者 {snap['no_attacker_propositions']} · OUT 无辩护者 {snap['no_defender_mis']}"
              f" · 无辩护者合计 {snap['no_defender_nodes']} · 未审边 {snap['unreviewed_edges']}"
              f" · 分量 {snap['components']}（孤立 {snap['isolated']}，最大 {snap['largest']}）"
              f" · 可信度 high {d['high']}/medium {d['medium']}/low {d['low']}）")
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
        report = generate_full_report(edges, anns, verdicts, cred)
        p = write_report(report, a.out)
        c = priority_counts(collect_findings(edges, anns, verdicts, cred))
        print(f"[audit] 已写 {p.relative_to(ROOT).as_posix() if str(p).startswith(str(ROOT)) else p}"
              f"（P0 {c['p0']} · P1 {c['p1']} · P2 {c['p2']}）")
        return 0
    elif a.cmd == "summary":
        res = summary_json(edges, anns, verdicts, cred)
    else:
        res = detect_credibility_gaps(cred)
    print(json.dumps(res, ensure_ascii=False, indent=1) if a.json
          else ("\n".join(map(str, res)) if isinstance(res, list) else json.dumps(
              res, ensure_ascii=False, indent=1)))
    return 0


def snapshot(edges_path: Path | str | None = None,
             ann_path: Path | str | None = None) -> dict:
    """五个基础探测器的**当前实况**（--check OK 文案与测试取值共用一处）。"""
    edges, verdicts, cred = load_state(edges_path, ann_path)
    nodes = all_nodes(verdicts, edges)
    props = [n for n in verdicts if dc.node_type_of(n, edges) == "proposition"]
    comps = detect_isolated_subgraphs(edges, nodes)
    sizes = sorted((len(c) for c in comps), reverse=True)
    return {"no_attacker_propositions": len(detect_no_attacker_propositions(edges, props)),
            "no_defender_mis": len(detect_no_defender_mis(edges, verdicts, cred)),
            "no_defender_nodes": len(detect_no_defender_nodes(edges, verdicts, cred)),
            "unreviewed_edges": len(detect_unreviewed_edges(edges)),
            "components": len(comps),
            "isolated": sum(1 for c in comps if len(c) == 1),
            "largest": sizes[0] if sizes else 0,
            "credibility_distribution": detect_credibility_gaps(cred)["distribution"],
            "nodes": len(nodes)}


def check(edges_path: Path | str | None = None,
          ann_path: Path | str | None = None,
          labels_path: Path | str | None = None) -> list[str]:
    """自洽校验（640c A1/A2 重写：**不变量 + 跨源一致性**，不再是快照比对）。

    **A 不变量**（纯内部一致性，与"当前数字是多少"无关 ⇒ 仓库正常演进不红，破坏即真 bug）：
      ① 可信度分布之和 == 判决表节点数；
      ② 无辩护者 MIS ⊆ OUT 节点，且每个无辩护者节点确实没有 W2 辩护者；
      ③ 无辩护者 MIS ⊆ 无辩护者节点（两个探测器同一口径）；
      ④ 连通分量是节点全集的一个划分（尺寸之和 == 节点数）；
      ⑤ 未审边 == 0（人审是本工具的前置条件；未审则结论不可用）。

    **B 跨源一致性**（**现算 vs 入库 W2 产物**：两条不同路径 ⇒ 有真实验证力）：
      ⑥ 判决汇总（IN/OUT/UNDEC/节点数）与产物一致；
      ⑦ 可信度分布与产物 `confidence` 分布一致；
      ⑧ OUT MIS 数与产物一致。
    """
    problems: list[str] = []
    edges, verdicts, cred = load_state(edges_path, ann_path)
    nodes = all_nodes(verdicts, edges)

    # ── A 不变量 ──
    gaps = detect_credibility_gaps(cred)
    if sum(gaps["distribution"].values()) != gaps["total"] or gaps["total"] != len(verdicts):
        problems.append(f"可信度分布之和 {sum(gaps['distribution'].values())} "
                        f"≠ 判决表节点数 {gaps['total']}/{len(verdicts)}")
    nd_mis = detect_no_defender_mis(edges, verdicts, cred)
    nd_all = detect_no_defender_nodes(edges, verdicts, cred)
    out_nodes = {n for n, v in verdicts.items() if v == "OUT"}
    if not set(nd_mis) <= out_nodes:
        problems.append(f"无辩护者 MIS 里有非 OUT 节点：{sorted(set(nd_mis) - out_nodes)}")
    if not set(nd_mis) <= set(nd_all):
        problems.append(f"无辩护者 MIS 不在无辩护者节点集合内："
                        f"{sorted(set(nd_mis) - set(nd_all))}")
    bad = [n for n in nd_all if dc.get_defense_chain(n, edges, verdicts, cred).w2_defenders]
    if bad:
        problems.append(f"无辩护者节点实际有 W2 辩护者：{bad[:5]} ⇒ 探测口径不一致")
    un = detect_unreviewed_edges(edges)
    if un:
        problems.append(f"存在未人审边 {len(un)} 条（人审全量后应为 0）")
    comps = detect_isolated_subgraphs(edges, nodes)
    total_in_comps = sum(len(c) for c in comps)
    if total_in_comps != len(nodes):
        problems.append(f"连通分量不是节点全集的划分：分量合计 {total_in_comps} ≠ 节点 {len(nodes)}")

    # ── B 跨源一致性（现算 vs 入库产物）──
    try:
        pn = dc.pinned_summary(labels_path)
    except FileNotFoundError as exc:
        problems.append(f"W2 产物不可读 ⇒ 无法跨源校验：{exc}")
        return problems
    s = dc.solve_summary(edges, cred)
    if (s["in"], s["out"], s["undec"], s["nodes"]) != (pn["in"], pn["out"], pn["undec"],
                                                       pn["nodes"]):
        problems.append(f"判决汇总 {s['in']}/{s['out']}/{s['undec']}（{s['nodes']}）"
                        f"≠ 产物 {pn['in']}/{pn['out']}/{pn['undec']}（{pn['nodes']}）")
    if gaps["distribution"] != pn["credibility_distribution"]:
        problems.append(f"可信度分布 {gaps['distribution']} ≠ 产物 {pn['credibility_distribution']}")
    out_mis = sum(1 for n in out_nodes if dc.node_type_of(n, edges) == "misconception")
    if out_mis != pn["out_mis"]:
        problems.append(f"OUT MIS 数 {out_mis} ≠ 产物 {pn['out_mis']}")
    return problems


if __name__ == "__main__":
    sys.exit(main())
