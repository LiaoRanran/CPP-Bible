#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""weighted_af_solver.py — W2 可信度加权 AF 求解器（596 任务2；594 唯一解除退化的模型）。

背景（593/594 实证，先核实再用）：本仓 79 命题 + 误区库的自然攻击关系有三种构造，全部退化：
  * 无攻击边 ⇒ 全部 IN（零信息）；
  * 只有 MIS→命题 单向边 ⇒ **语义倒置**（误解无入边 ⇒ 永远 IN，命题反被压成 UNDEC）；
  * 对称但无权重 ⇒ 全部 UNDEC（互攻无胜负）。
594 找到的解 **W2**：① 每条 MIS→命题边配一条**对称**的命题→MIS 边；② **可信度加权击败**——
`A→B` 只有 `cred(A) > cred(B)`（**严格大于**）时才构成"击败"；③ 在**击败关系**上求 grounded
最小不动点。实测结果 IN=79（命题全 IN）/ OUT=42（误解全 OUT）/ UNDEC=0，非退化且语义正确。

可信度取值（任务书 596 任务2）：`high=3 / medium=2 / low=1`，无字段按 `low` 计。
  * 命题节点：命题级 `signed_by` 非空 ⇒ high；卡级 `verified_by` 非空（card_signed）或
    `machine_verified` ⇒ medium；否则 low；
  * 误解节点：取其在候选边上的 `confidence`（同一个 MIS 的所有边同值，由任务1 的分级决定）。
  * 实测：79 命题全 medium、42（带关联的）误解全 low ⇒ 命题"击败"误解 ⇒ 非退化。
    **若哪天误解卡补上人签（high），该误解就会反过来把命题击败 —— 这正是权重该有的后果。**

grounded 不动点（任务书 596 任务2.3）：
  * 初始全 UNDEC；
  * `IN` ⇔ 它的**全部**攻击者都 `OUT`；`OUT` ⇔ 存在 `IN` 的攻击者且该边构成击败；
  * 迭代到不动点（**最多 100 轮**，超限 ⇒ fail-loud，绝不静默返回半成品）。

只读纪律：不写卡、不改候选边、不改命题库；唯一写动作是 `solve` 覆盖写**派生数据**
`data/grounded_labels_w2.json`（入库）。

用法：
    python tools/weighted_af_solver.py solve [--edges PATH] [--out PATH]
                                             [--include-human-reviewed|--no-human-reviewed]
    python tools/weighted_af_solver.py stats [--json]
    python tools/weighted_af_solver.py --check        # 与 594 实证对账（失败 exit 2）

596 任务4 集成：`--include-human-reviewed`（**默认开启**）会把 `data/human_attack_edge_annotations.jsonl`
的人审结果应用到攻击图上（approve 升一级 / reject 剔除 / modify 指定档）。一旦人审真的介入，
594 的"未审候选图"基线（IN=79/OUT=42/UNDEC=0）**不再是权威**，`--check` 自动退化为只查结构不变量。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import attack_edge_generator as aeg  # noqa: E402
import attack_edge_review as aer  # noqa: E402
import human_review_cli as hrc  # noqa: E402   # 609 A3：人审标注的 `kind` 归一化
import prop_graph as pg  # noqa: E402

VERSION = "1.1"
DEFAULT_EDGES = aeg.DEFAULT_OUT
DEFAULT_ANNOTATIONS = aer.DEFAULT_ANN
DEFAULT_OUT = ROOT / "data" / "grounded_labels_w2.json"
#: 命题 id 在**本批数据文件**里的写法（与 attack_edge_generator 一致：`卡id::prop-N`）。
PROP_SEP = aeg.PROP_SEP
MAX_ROUNDS = 100                      # 不动点保护（任务书 596 任务2 硬要求）
#: 594 实证对账基线（`--check` 用；若实跑不符 ⇒ exit 2，不许改测试凑数）。
W2_EXPECTED = {"IN": 79, "OUT": 42, "UNDEC": 0}
WEIGHT = aeg.CONFIDENCE_WEIGHT


# ── 节点与可信度（只读）────────────────────────────────────────────────────────
def proposition_nodes() -> dict[str, dict]:
    """79 命题节点（id 用 `卡id::prop-N`）+ 可信度分级（见模块 docstring）。"""
    out: dict[str, dict] = {}
    for p in pg.extract():
        key = str(p["prop_key"]).replace("/", PROP_SEP, 1)
        if str(p.get("signed_by") or "").strip():
            conf = "high"                              # 命题级人签
        elif str(p.get("signoff_state") or "") == "card_signed" or p.get("machine_verified"):
            conf = "medium"                            # 卡级人签 或 有机器锚
        else:
            conf = "low"
        out[key] = {"id": key, "type": "proposition", "confidence": conf,
                    "credibility": WEIGHT[conf], "card": p["card"],
                    "claim_type": p["claim_type"],
                    "signoff_state": p["signoff_state"],
                    "machine_verified": int(p.get("machine_verified") or 0)}
    return out


def _edge_lists(edges: list[dict]) -> tuple[dict[str, set[str]], dict[str, set[str]]]:
    """⇒ (attacks: A→{B}, attackers: B→{A})（有向攻击关系）。"""
    attacks: dict[str, set[str]] = {}
    attackers: dict[str, set[str]] = {}
    for e in edges:
        s, t = str(e["source"]), str(e["target"])
        attacks.setdefault(s, set()).add(t)
        attackers.setdefault(t, set()).add(s)
    return attacks, attackers


def build_graph(edges: list[dict]) -> dict[str, dict]:
    """节点全集 = 79 命题 ∪ 边里出现的所有误解节点（`mis_to_prop` 的 source / `prop_to_mis` 的 target）。"""
    nodes = proposition_nodes()
    mis_conf: dict[str, str] = {}
    for e in edges:
        for node, is_mis in ((str(e["source"]), e["direction"] == "mis_to_prop"),
                             (str(e["target"]), e["direction"] == "prop_to_mis")):
            if is_mis:
                cur = mis_conf.get(node)
                if cur is None or WEIGHT[str(e.get("confidence"))] > WEIGHT[cur]:
                    mis_conf[node] = str(e.get("confidence"))
    for mid, conf in sorted(mis_conf.items()):
        nodes[mid] = {"id": mid, "type": "misconception", "confidence": conf,
                      "credibility": WEIGHT[conf]}
    return nodes


def defeats_of(edges: list[dict], nodes: dict[str, dict]) -> set[tuple[str, str]]:
    """W2 击败关系：`(A,B)` 当 `cred(A) > cred(B)`（**严格大于**）。"""
    out: set[tuple[str, str]] = set()
    for e in edges:
        a, b = str(e["source"]), str(e["target"])
        if a in nodes and b in nodes and nodes[a]["credibility"] > nodes[b]["credibility"]:
            out.add((a, b))
    return out


# ── 求解 ───────────────────────────────────────────────────────────────────────
def _defeat_attackers(nodes: dict[str, dict],
                      defeats: set[tuple[str, str]]) -> dict[str, set[str]]:
    """击败关系**即**攻击关系（W2 的核心）：`defeat_attackers[b] = {a : (a,b) 构成击败}`。

    ⚠️ 这里踩过一次坑（596 实测）：若 IN 判定用**全部**攻击边、OUT 判定只用**击败边**，
    两个关系不一致 ⇒ 迭代互相卡死（实测 IN=4 / OUT=0 / UNDEC=117，全部误解 UNDEC）。
    W2 的语义是"不构成击败的攻击**不算攻击**"，所以两个判定必须用**同一个**关系。
    """
    out: dict[str, set[str]] = {n: set() for n in nodes}
    for a, b in defeats:
        if a in out and b in out:
            out[b].add(a)
    return out


def grounded_labels(nodes: dict[str, dict], defeats: set[tuple[str, str]], *,
                    max_rounds: int = MAX_ROUNDS) -> tuple[dict[str, str], int]:
    """在**击败关系**上求 grounded 标签（最小不动点）；返回 (labels, 轮数)。

    * `IN` ⇔ 它的**全部**（击败意义下的）攻击者都 `OUT`（无攻击者 ⇒ 立即 IN）；
    * `OUT` ⇔ 存在 `IN` 的攻击者（该边已构成击败）；
    * 其余 `UNDEC`（互攻无胜负）。
    超 `max_rounds` 未收敛 ⇒ `RuntimeError`（fail-loud：半成品标注比没有标注更危险）。
    """
    ids = sorted(nodes)
    d_atk = _defeat_attackers(nodes, defeats)
    label = dict.fromkeys(ids, "UNDEC")
    for rnd in range(1, max_rounds + 1):
        new: dict[str, str] = {}
        for n in ids:
            atk = sorted(d_atk[n])
            if all(label[a] == "OUT" for a in atk):
                new[n] = "IN"
            elif any(label[a] == "IN" for a in atk):
                new[n] = "OUT"
            else:
                new[n] = "UNDEC"
        if new == label:
            return label, rnd
        label = new
    raise RuntimeError(f"grounded 不动点在 {max_rounds} 轮内未收敛（攻击关系可能被污染）")


def solve(edges: list[dict], *, max_rounds: int = MAX_ROUNDS) -> dict:
    """端到端：候选边 ⇒ 节点 ∪ 攻击关系 ⇒ W2 grounded 标注。"""
    nodes = build_graph(edges)
    attacks, attackers = _edge_lists(edges)
    defeats = defeats_of(edges, nodes)
    labels, rounds = grounded_labels(nodes, defeats, max_rounds=max_rounds)
    out_nodes: dict[str, dict] = {}
    for n in sorted(nodes):
        atk = sorted(attackers.get(n, ()))
        out_nodes[n] = {
            "id": n, "type": nodes[n]["type"], "label": labels[n],
            "confidence": nodes[n]["confidence"], "credibility": nodes[n]["credibility"],
            # `attackers` 记**全部**攻击边（含不构成击败的），用于人读辩护链
            "attackers": atk,
            # 被它击败的攻击者（W2 的可信度加权击败：只对**真的**攻击者成立）
            "defeated_attackers": sorted(a for a in atk if (n, a) in defeats),
            # 为它辩护：IN 且攻击它的某个攻击者（即把攻击者打 OUT 的一方；不算自己）
            "defenders": sorted({d for a in atk for d in attacks.get(a, ())
                                 if labels.get(d) == "IN" and d != n}),
        }
        if nodes[n]["type"] == "proposition":
            out_nodes[n]["card"] = nodes[n]["card"]
            out_nodes[n]["claim_type"] = nodes[n]["claim_type"]
            out_nodes[n]["signoff_state"] = nodes[n]["signoff_state"]
    summary = {"IN": sum(1 for v in out_nodes.values() if v["label"] == "IN"),
               "OUT": sum(1 for v in out_nodes.values() if v["label"] == "OUT"),
               "UNDEC": sum(1 for v in out_nodes.values() if v["label"] == "UNDEC"),
               "nodes": len(out_nodes),
               "IN_propositions": sum(1 for v in out_nodes.values()
                                      if v["label"] == "IN" and v["type"] == "proposition"),
               "IN_misconceptions": sum(1 for v in out_nodes.values()
                                        if v["label"] == "IN" and v["type"] == "misconception")}
    return {"tool": "weighted_af_solver", "version": VERSION,
            "model": "W2_credibility_weighted_grounded",
            "credibility_levels": WEIGHT, "rounds": rounds,
            "edges": len(edges), "defeating_edges": len(defeats),
            "summary": summary, "nodes": out_nodes}


# ── 对照实现（**已知失败**，保留是为了让"为什么选 W2"可复现）────────────────────
NEG_MARKERS = ("错误", "不对", "实际上", "并非", "不是", "误", "错", "无", "否",
               "反例", "不成立", "不能", "不应", "没有", "不可", "无法", "违背", "相反", "忽略")


def w1_weight(refutations: list[str]) -> float:
    """W1 的边权：反驳文本里的否定标记密度（594 手搓口径，纯标准库）。"""
    text = " ".join(refutations)
    if not text:
        return 0.0
    return sum(text.count(w) for w in NEG_MARKERS) / max(len(text), 1)


def w1_threshold_labels(nodes: dict[str, dict], edges: list[dict], weights: dict[str, float],
                        theta: float) -> dict[str, str]:
    """**对照用（594 W1）**：把边权按阈值 θ 二值化成"攻击"，**不做可信度比较**。

    594 实证：在**单向**边上，误解没有任何入边 ⇒ 无论 θ 取何值，误解恒 IN、命题恒非 IN
    —— 语义倒置。保留这份实现是为了在仓内可复现"阈值加权救不了退化，对称边才能"。
    """
    bin_edges = [e for e in edges if weights.get(str(e["source"]), 0.0) >= theta]
    labels, _r = grounded_labels(nodes, {(str(e["source"]), str(e["target"]))
                                         for e in bin_edges})
    return labels


def load_edges(path: Path | str = DEFAULT_EDGES) -> list[dict]:
    return aeg.load_edges(path)


def write_labels(doc: dict, out: Path | str = DEFAULT_OUT) -> Path:
    p = Path(out)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(doc, ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                 encoding="utf-8", newline="\n")
    return p


def stats(doc: dict) -> dict:
    nodes = doc["nodes"]
    props = [v for v in nodes.values() if v["type"] == "proposition"]
    mis = [v for v in nodes.values() if v["type"] == "misconception"]

    def dist(rows: list[dict]) -> dict[str, int]:
        d: dict[str, int] = {}
        for r in rows:
            d[r["label"]] = d.get(r["label"], 0) + 1
        return dict(sorted(d.items()))
    return {"total": len(nodes), "by_label": doc["summary"], "propositions": len(props),
            "misconceptions": len(mis), "prop_labels": dist(props), "mis_labels": dist(mis),
            "avg_attackers": round(sum(len(v["attackers"]) for v in nodes.values()) / max(len(nodes), 1), 2),
            "avg_defenders": round(sum(len(v["defenders"]) for v in nodes.values()) / max(len(nodes), 1), 2),
            "avg_attackers_prop": round(sum(len(v["attackers"]) for v in props) / max(len(props), 1), 2),
            "avg_attackers_mis": round(sum(len(v["attackers"]) for v in mis) / max(len(mis), 1), 2),
            "rounds": doc["rounds"], "defeating_edges": doc["defeating_edges"],
            "edges": doc["edges"]}


# ── 609 A3：人审介入的权重规则（**只改权重输入，不改 W2 击败规则**）────────────────
# ⚠️ 与 596 `aer.effective_edges` 的差别：596 读 `action` 字段、无 trace；609 读任务书的
#   `kind` 字段（兼容 `action`），并把**人审来源**带在边上（`human_reviewed` / `review_reason`），
#   好让 `diff` 能把"哪条人审导致了这次翻转"追到边级。
REVIEW_RULES = {
    # kind      → (动作, 说明)
    "approve": ("promote", "人审确认攻击边成立 ⇒ 可信度升一级（low→medium→high→high，档位见 PROMOTE）"),
    "reject":  ("drop",    "人审拒绝攻击边 ⇒ 从攻击图中**移除**（不再参与击败）"),
    "modify":  ("set",     "人审改档 ⇒ **按 `--modify-mode` 决定是否采纳**（见 MODIFY_MODES）"),
}
PROMOTE = {"low": "medium", "medium": "high", "high": "high"}

# ── 611 B1：modify 口径**双模式**（口径冲突不裁决，两档都能跑，默认对齐入库权威）──────────
# 背景（610 交人项 ①）：388 条人审里 34 条 modify 的 `new_confidence` **全是 medium**。
#   * `keep-low`（**默认**）：modify **不改变生效权重**（保持该边原有的 low）——
#     这是 `data/grounded_labels_w2.json` 的实际生成口径 ⇒ IN114/OUT7/击败边 17；
#   * `upgrade-medium`：modify 采纳 `confidence`/`new_confidence`（609 A3 的口径）⇒ IN121/OUT0/击败边 0。
# 为什么默认取 `keep-low`：**默认值应该与入库权威产物一致**（否则"跑一遍默认"就得到与冻结产物
#   不同的图）。两档都在，谁对谁错**由人裁决**（611 只做工具支持，不统一口径）。
MODIFY_MODES = ("keep-low", "upgrade-medium")
DEFAULT_MODIFY_MODE = "keep-low"


def reviewed_edges(edges: list[dict], annotations: list[dict], *,
                   latest: dict[str, dict] | None = None,
                   modify_mode: str = DEFAULT_MODIFY_MODE) -> tuple[list[dict], dict]:
    """按人审结果生成**生效边**；返回 (生效边, 变更明细{edge_id: {...}})。

    同一条边多次审查 ⇒ 取**最后一条**（`hrc.latest_by_edge`），历史仍留在文件里可追溯。

    `modify_mode`（611 B1）：
      * `keep-low` —— modify **不生效**（权重保持原值）；变更明细里记 `effective=False`，
        好让 `diff` **不把它算成"导致翻转的人审"**（它确实没改任何东西）；
      * `upgrade-medium` —— modify 采纳 `confidence`/`new_confidence`（609 A3 原语义）。
    """
    if modify_mode not in MODIFY_MODES:
        raise ValueError(f"modify_mode 须 ∈ {MODIFY_MODES}，实得 {modify_mode!r}")
    import human_review_cli as hrc  # 局部导入：596 的调用路径不该被迫加载 609 依赖

    last = latest if latest is not None else hrc.latest_by_edge(annotations)
    out: list[dict] = []
    changes: dict[str, dict] = {}
    for e in edges:
        eid = str(e["id"])
        a = last.get(eid)
        if a is None:
            out.append(e)
            continue
        kind = hrc.kind_of(a)
        rule, why = REVIEW_RULES.get(kind, (None, None))
        old_conf = str(e.get("confidence"))
        if rule == "drop":
            changes[eid] = {"action": "drop", "kind": kind, "old_confidence": old_conf,
                            "new_confidence": None, "why": why, "effective": True,
                            "review_reason": str(a.get("reason", ""))}
            continue
        if rule == "promote":
            new_conf = PROMOTE.get(old_conf, old_conf)
        elif rule == "set":
            if modify_mode == "keep-low":
                # 不生效：权重不动，但**留下痕迹**（人审过、理由是什么），便于复核
                ne = dict(e)
                ne["human_reviewed"] = kind
                ne["review_reason"] = str(a.get("reason", ""))
                ne["modify_ignored_by"] = modify_mode
                changes[eid] = {"action": "keep", "kind": kind, "old_confidence": old_conf,
                                "new_confidence": old_conf, "effective": False,
                                "why": "keep-low 口径：modify 不改变生效权重（与入库权威产物一致）",
                                "declared_confidence": str(a.get("confidence")
                                                           or a.get("new_confidence") or ""),
                                "review_reason": str(a.get("reason", ""))}
                out.append(ne)
                continue
            # 兼容 596 的 `new_confidence`（同 `attack_edge_review.py` 的写法）
            new_conf = str(a.get("confidence") or a.get("new_confidence") or old_conf)
        else:                                    # 未知 kind ⇒ fail-closed：保持原权重不动
            out.append(e)
            continue
        ne = dict(e)
        ne["confidence"] = new_conf
        ne["human_reviewed"] = kind
        ne["review_reason"] = str(a.get("reason", ""))
        changes[eid] = {"action": rule, "kind": kind, "old_confidence": old_conf,
                        "new_confidence": new_conf, "why": why, "effective": True,
                        "review_reason": str(a.get("reason", ""))}
        out.append(ne)
    return out, changes


def review_progress(edges: list[dict], annotations: list[dict]) -> dict:
    """人审进度：reviewed / pending / total（同边多次审只算一条）。"""
    last = hrc.latest_by_edge(annotations)
    done = sum(1 for e in edges if str(e["id"]) in last)
    return {"total": len(edges), "reviewed": done, "pending": len(edges) - done,
            "annotations": len(annotations),
            "reviewed_rate": round(done / len(edges), 4) if edges else None}


def solve_reviewed(edges: list[dict], annotations: list[dict], *,
                   modify_mode: str = DEFAULT_MODIFY_MODE) -> tuple[dict, dict]:
    """端到端：原始候选边 + 人审 ⇒ 新 W2 doc，连同变更明细。"""
    eff, changes = reviewed_edges(edges, annotations, modify_mode=modify_mode)
    return solve(eff), changes


def _incident(node: str, changes: dict[str, dict], edges: list[dict]) -> list[str]:
    """某节点涉及的、**真正动了权重**的人审边 id（用于把翻转追到边级）。

    611 B1：`effective=False` 的变更（keep-low 下被忽略的 modify）**不算触发者** ——
    它没改任何权重，把它算进去会把反转归因到"其实什么都没做"的人审上。
    """
    out = []
    for e in edges:
        s, t = str(e["source"]), str(e["target"])
        eid = str(e["id"])
        if node in (s, t) and eid in changes and changes[eid].get("effective", True):
            out.append(eid)
    return sorted(out)


def diff_verdicts(base: dict, new: dict, *, edges: list[dict] | None = None,
                  changes: dict[str, dict] | None = None) -> dict:
    """对比两份 W2 doc 的判决差异；翻转精确到**节点 + 触发它的人审边**。

    `changes` 来自 `reviewed_edges`（含 drop / promote / set 明细）；没给 ⇒ 只报翻转不给归因。
    """
    flips: list[dict] = []
    for nid in sorted(set(base.get("nodes", {})) | set(new.get("nodes", {}))):
        b = base.get("nodes", {}).get(nid, {}).get("label", "∅")
        n = new.get("nodes", {}).get(nid, {}).get("label", "∅")
        if b == n:
            continue
        row = {"node_id": nid, "old": b, "new": n,
               "node_type": new.get("nodes", {}).get(nid, {}).get("type", "?")}
        if changes and edges is not None:
            hit = _incident(nid, changes, edges)
            kinds: dict[str, int] = {}
            for eid in hit:
                k = str(changes[eid]["kind"])
                kinds[k] = kinds.get(k, 0) + 1
            row["trigger_edge_ids"] = hit[:10]
            row["trigger_edge_count"] = len(hit)
            row["trigger_kinds"] = kinds
            row["reason"] = (f"人审对该节点的 {len(hit)} 条攻击边动了手"
                             f"（{kinds}）⇒ 可信度加权击败关系改变 ⇒ {b}→{n}")
        else:
            row["reason"] = "（未提供人审变更明细，无法归因）"
        flips.append(row)
    return {"flipped": len(flips), "flips": flips,
            "base_summary": base.get("summary", {}), "new_summary": new.get("summary", {}),
            "base_edges": base.get("edges"), "new_edges": new.get("edges")}


def check(doc: dict, *, expect_594: bool = True) -> list[str]:
    """校验标注文档。`expect_594=False` ⇒ 只查结构不变量（人审介入后 594 基线不再适用）。"""
    problems: list[str] = []
    s = doc["summary"]
    if expect_594:
        for k, want in W2_EXPECTED.items():
            if s.get(k) != want:
                problems.append(f"与 594 实证不符：{k} = {s.get(k)}（期望 {want}）")
    if doc["rounds"] >= MAX_ROUNDS:
        problems.append(f"轮数 {doc['rounds']} 已达上限 {MAX_ROUNDS}（未真正收敛）")
    unlabeled = [k for k, v in doc["nodes"].items() if v["label"] not in ("IN", "OUT", "UNDEC")]
    if unlabeled:
        problems.append(f"存在无标注节点：{unlabeled[:5]}")
    if len(doc["nodes"]) != s["nodes"]:
        problems.append("nodes 数与 summary.nodes 不一致")
    # 语义正确性硬检查：命题不得 OUT、误解不得 IN（数据有问题就要显形）
    bad_prop = sorted(k for k, v in doc["nodes"].items()
                      if v["type"] == "proposition" and v["label"] == "OUT")
    bad_mis = sorted(k for k, v in doc["nodes"].items()
                     if v["type"] == "misconception" and v["label"] == "IN")
    if bad_prop:
        problems.append(f"命题被判 OUT（数据异常）：{bad_prop[:5]}")
    if bad_mis:
        problems.append(f"误解被判 IN（数据异常）：{bad_mis[:5]}")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="W2 可信度加权 AF 求解器（只读求解；标注入库）")
    sub = ap.add_subparsers(dest="cmd")
    for name in ("solve", "stats", "diff"):
        sp = sub.add_parser(name)
        sp.add_argument("--edges", default=str(DEFAULT_EDGES))
        sp.add_argument("--annotations", default=str(DEFAULT_ANNOTATIONS))
        sp.add_argument("--out", default=str(DEFAULT_OUT))
        sp.add_argument("--json", action="store_true")
        sp.add_argument("--include-human-reviewed", dest="human", action="store_true", default=True,
                        help="启用**已审**攻击边：approve 升一级 / reject 剔除 / modify 指定档（默认开）")
        sp.add_argument("--no-human-reviewed", dest="human", action="store_false",
                        help="只用原始候选边（忽略人审标注）")
        sp.add_argument("--modify-mode", choices=MODIFY_MODES, default=DEFAULT_MODIFY_MODE,
                        help=f"modify 档位口径（默认 {DEFAULT_MODIFY_MODE} = 入库权威产物口径；"
                             f"{' / '.join(MODIFY_MODES)}）")
        if name == "diff":
            sp.add_argument("--baseline", required=True,
                            help="对比基线 W2 文档（通常是未人审的 grounded_labels_w2.json）")
    ap.add_argument("--check", action="store_true", help="与 594 实证对账（失败 exit 2）")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--edges", default=str(DEFAULT_EDGES))
    ap.add_argument("--annotations", default=str(DEFAULT_ANNOTATIONS))
    ap.add_argument("--include-human-reviewed", dest="human", action="store_true", default=True)
    ap.add_argument("--no-human-reviewed", dest="human", action="store_false")
    a = ap.parse_args(argv)

    anns = aer.load_annotations(a.annotations)
    if a.check:
        p = Path(a.out)
        if not p.is_file():
            print(f"[w2] ❌ 标注文件不存在：{p}（先跑 solve）", file=sys.stderr)
            return 2
        try:
            doc = json.loads(p.read_text(encoding="utf-8"))
        except ValueError as exc:
            print(f"[w2] ❌ 标注文件不是合法 JSON：{exc}", file=sys.stderr)
            return 2
        missing = [k for k in ("summary", "nodes", "rounds") if k not in doc] \
            if isinstance(doc, dict) else ["（不是 JSON 对象）"]
        if missing:
            print(f"[w2] ❌ 标注文件结构不完整（缺 {missing}）⇒ 拒绝判绿", file=sys.stderr)
            return 2
        # 人审一旦介入（有标注且启用），594 的"未审候选图"基线就不再是权威 ⇒ 只查结构不变量
        expect_594 = not (a.human and anns)
        problems = check(doc, expect_594=expect_594)
        if problems:
            print(f"[w2] ❌ 对账失败（{len(problems)} 项）：", file=sys.stderr)
            for x in problems[:10]:
                print(f"  - {x}", file=sys.stderr)
            return 2
        tail = "（人审已介入 ⇒ 只查结构不变量，594 基线不再适用）" if not expect_594 else ""
        print(f"[w2] ✓ IN={doc['summary']['IN']} / OUT={doc['summary']['OUT']} / "
              f"UNDEC={doc['summary']['UNDEC']}（{doc['rounds']} 轮收敛）{tail}")
        return 0

    raw_edges = load_edges(a.edges)
    if not raw_edges:
        print(f"[w2] ❌ 候选边为空：{a.edges}（先跑 attack_edge_generator.py generate）", file=sys.stderr)
        return 2
    changes: dict[str, dict] = {}
    edges = raw_edges
    if a.human and anns:
        mode = getattr(a, "modify_mode", DEFAULT_MODIFY_MODE)
        edges, changes = reviewed_edges(raw_edges, anns, modify_mode=mode)
        prog = review_progress(raw_edges, anns)
        noop = sum(1 for v in changes.values() if not v.get("effective", True))
        # 走 stderr：`--json` 时 stdout 必须是**纯 JSON**（可被 jq / json.loads 直接吃）
        print(f"[w2] 人审标注生效：历史 {prog['annotations']} 条 · 已审边 "
              f"{prog['reviewed']}/{prog['total']}（pending {prog['pending']}）"
              f" · 边 {len(raw_edges)} ⇒ {len(edges)}（剔除 "
              f"{len(raw_edges) - len(edges)} 条被拒边；approve 升一级 / "
              f"modify 口径 {mode}，其中 {noop} 条 modify 未生效）",
              file=sys.stderr)
    doc = solve(edges)

    if a.cmd == "diff":
        bp = Path(a.baseline)
        if not bp.is_file():
            print(f"[w2] ❌ 基线文件不存在：{bp}（先跑 solve 生成未人审的 W2 文档）", file=sys.stderr)
            return 2
        try:
            base = json.loads(bp.read_text(encoding="utf-8"))
        except ValueError as exc:
            print(f"[w2] ❌ 基线文件不是合法 JSON：{exc}", file=sys.stderr)
            return 2
        d = diff_verdicts(base, doc, edges=raw_edges, changes=changes)
        if a.json:
            print(json.dumps(d, ensure_ascii=False, indent=1))
            return 0
        print(f"[w2] diff vs {bp.name}：翻转 {d['flipped']} 个节点"
              f"（IN {d['base_summary'].get('IN')}→{d['new_summary'].get('IN')} · "
              f"OUT {d['base_summary'].get('OUT')}→{d['new_summary'].get('OUT')} · "
              f"UNDEC {d['base_summary'].get('UNDEC')}→{d['new_summary'].get('UNDEC')}）")
        for f in d["flips"][:50]:
            print(f"  - {f['node_id']}（{f['node_type']}）：{f['old']} → {f['new']}"
                  f" · 触发人审边 {f.get('trigger_edge_count', 0)} 条 {f.get('trigger_kinds', {})}")
            print(f"      {f['reason']}")
        return 0

    if a.cmd == "stats":
        st = stats(doc)
        extra = {}
        if changes:
            prog = review_progress(raw_edges, anns)
            base = solve(raw_edges)
            influence = diff_verdicts(base, doc, edges=raw_edges, changes=changes)
            ineff = [k for k, v in changes.items() if not v.get("effective", True)]
            extra = {"review_progress": prog, "review_changes": len(changes),
                     "ineffective_changes": len(ineff),
                     "modify_mode": getattr(a, "modify_mode", DEFAULT_MODIFY_MODE),
                     "flipped_nodes": influence["flipped"], "flips": influence["flips"]}
        payload = {**st, **extra}
        if a.json:
            print(json.dumps(payload, ensure_ascii=False, indent=1))
            return 0
        print(f"[w2] 节点 {st['total']}（命题 {st['propositions']} / 误解 {st['misconceptions']}）"
              f" · IN {st['by_label']['IN']} / OUT {st['by_label']['OUT']} / UNDEC {st['by_label']['UNDEC']}")
        print(f"[w2] 命题标签 {st['prop_labels']} · 误解标签 {st['mis_labels']}")
        print(f"[w2] 平均攻击者 {st['avg_attackers']}（命题 {st['avg_attackers_prop']} / "
              f"误解 {st['avg_attackers_mis']}）· 平均辩护者 {st['avg_defenders']}")
        print(f"[w2] 击败边 {st['defeating_edges']}/{st['edges']} · {st['rounds']} 轮收敛")
        if extra:
            p = extra["review_progress"]
            print(f"[w2] 人审进度 {p['reviewed']}/{p['total']}"
                  f"（pending {p['pending']} · 历史 {p['annotations']} 条）"
                  f" · 变更 {extra['review_changes']} 条边"
                  f"（其中未生效 {extra['ineffective_changes']} 条 · modify 口径 "
                  f"{extra['modify_mode']}）")
            print(f"[w2] 判决影响：{extra['flipped_nodes']} 个节点翻转")
            for f in extra["flips"][:20]:
                print(f"  - {f['node_id']}（{f['node_type']}）：{f['old']} → {f['new']}"
                      f" · 触发人审边 {f.get('trigger_edge_count', 0)} 条")
        return 0

    p = write_labels(doc, a.out)
    s = doc["summary"]
    print(f"[w2] 已写 {p.relative_to(ROOT).as_posix() if str(p).startswith(str(ROOT)) else p}："
          f"节点 {s['nodes']} · IN {s['IN']} / OUT {s['OUT']} / UNDEC {s['UNDEC']}"
          f"（{doc['rounds']} 轮 · 击败边 {doc['defeating_edges']}/{doc['edges']}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
