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
    python tools/weighted_af_solver.py stats [--json]
    python tools/weighted_af_solver.py --check        # 与 594 实证对账（失败 exit 2）
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import attack_edge_generator as aeg  # noqa: E402
import prop_graph as pg  # noqa: E402

VERSION = "1.0"
DEFAULT_EDGES = aeg.DEFAULT_OUT
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


def check(doc: dict) -> list[str]:
    problems: list[str] = []
    s = doc["summary"]
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
    for name in ("solve", "stats"):
        sp = sub.add_parser(name)
        sp.add_argument("--edges", default=str(DEFAULT_EDGES))
        sp.add_argument("--out", default=str(DEFAULT_OUT))
        sp.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true", help="与 594 实证对账（失败 exit 2）")
    ap.add_argument("--out", default=str(DEFAULT_OUT))
    ap.add_argument("--edges", default=str(DEFAULT_EDGES))
    a = ap.parse_args(argv)

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
        problems = check(doc)
        if problems:
            print(f"[w2] ❌ 对账失败（{len(problems)} 项）：", file=sys.stderr)
            for x in problems[:10]:
                print(f"  - {x}", file=sys.stderr)
            return 2
        print(f"[w2] ✓ 与 594 实证一致：IN={doc['summary']['IN']} / OUT={doc['summary']['OUT']} / "
              f"UNDEC={doc['summary']['UNDEC']}（{doc['rounds']} 轮收敛）")
        return 0

    edges = load_edges(a.edges)
    if not edges:
        print(f"[w2] ❌ 候选边为空：{a.edges}（先跑 attack_edge_generator.py generate）", file=sys.stderr)
        return 2
    doc = solve(edges)
    if a.cmd == "stats":
        st = stats(doc)
        if a.json:
            print(json.dumps(st, ensure_ascii=False, indent=1))
            return 0
        print(f"[w2] 节点 {st['total']}（命题 {st['propositions']} / 误解 {st['misconceptions']}）"
              f" · IN {st['by_label']['IN']} / OUT {st['by_label']['OUT']} / UNDEC {st['by_label']['UNDEC']}")
        print(f"[w2] 命题标签 {st['prop_labels']} · 误解标签 {st['mis_labels']}")
        print(f"[w2] 平均攻击者 {st['avg_attackers']}（命题 {st['avg_attackers_prop']} / "
              f"误解 {st['avg_attackers_mis']}）· 平均辩护者 {st['avg_defenders']}")
        print(f"[w2] 击败边 {st['defeating_edges']}/{st['edges']} · {st['rounds']} 轮收敛")
        return 0

    p = write_labels(doc, a.out)
    s = doc["summary"]
    print(f"[w2] 已写 {p.relative_to(ROOT).as_posix() if str(p).startswith(str(ROOT)) else p}："
          f"节点 {s['nodes']} · IN {s['IN']} / OUT {s['OUT']} / UNDEC {s['UNDEC']}"
          f"（{doc['rounds']} 轮 · 击败边 {doc['defeating_edges']}/{doc['edges']}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
