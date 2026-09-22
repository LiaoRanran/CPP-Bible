#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""human_review_queue.py — 候选攻击边的 **MIS 群组级人审队列**（608 线A 任务1）。

为什么：596 生成了 388 条候选攻击边（388 条边级人审 ≈ 1.89h，见 595），但人审是**群组级**更划算
（42 个 MIS 组 × 35s ≈ 24.5min，降 4.6 倍）。本工具把 388 边按 MIS 聚合为 42 个群组，按**歧义度**
主动学习式排序，给出待审队列、群组详情、进度统计，并提供 `--check` 与 `attack_edge_review` 数据一致性校验。

硬纪律（与 `attack_edge_review.py` 同款）：
  * **只读**：绝不写 `data/human_attack_edge_annotations.jsonl`（人审结果文件）——那是人审权力；
    本工具只读取、聚合、呈现。
  * **fail-closed**：`--check` 发现聚合与权威数据不一致 ⇒ exit 2，绝不静默通过。
  * 建议 verdict 只是**呈现辅助**（取自 W2 求解结果 `data/grounded_labels_w2.json`），不是自动判决；
    真判决只能由人执行 `attack_edge_review.py approve/reject/modify`。

用法：
    python tools/human_review_queue.py --list [--output FILE]
    python tools/human_review_queue.py --show <MIS-ID>
    python tools/human_review_queue.py --stats
    python tools/human_review_queue.py --check
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any

from path_config_625 import root as _queyi_root  # noqa: E402  (625 C1 路径解耦)

ROOT = _queyi_root()
sys.path.insert(0, str(Path(__file__).resolve().parent))

import attack_edge_generator as aeg  # noqa: E402
import attack_edge_review as aer  # noqa: E402
import gate_engine as ge  # noqa: E402

VERSION = "1.0"
DEFAULT_EDGES = aeg.DEFAULT_OUT
DEFAULT_W2 = ROOT / "data" / "grounded_labels_w2.json"
DEFAULT_MIS_DIR = aeg.DEFAULT_MIS_DIR
PROP_SEP = aeg.PROP_SEP

ACTIONS = ("approve", "reject", "modify")  # attack_edge_review 的人审动作


# ── 读取面（只读）────────────────────────────────────────────────────────────────
def _mis_name_map(mis_dir: Path | str = DEFAULT_MIS_DIR) -> dict[str, str]:
    """MIS id → 标题（`name` 字段，回退 `id`）。"""
    out: dict[str, str] = {}
    for f in sorted(Path(mis_dir).rglob("MIS-*.md")):
        if "README" in f.name:
            continue
        m = ge._meta(f)
        mid = str(m.get("id") or f.stem)
        out[mid] = str(m.get("name") or mid)
    return out


def _w2_labels(w2_path: Path | str = DEFAULT_W2) -> Any:
    """W2 求解结果：节点 id → {label, credibility, type}。"""
    data = json.loads(Path(w2_path).read_text(encoding="utf-8"))
    return data.get("nodes", {})


def _mis_of(edge: dict) -> Any:
    """一条边的 MIS 端点（无论方向）。"""
    return edge["source"] if edge["direction"] == "mis_to_prop" else edge["target"]


def _prop_of(edge: dict) -> Any:
    """一条边的命题端点（`卡id::prop-N`）。"""
    return edge["target"] if edge["direction"] == "mis_to_prop" else edge["source"]


def _card_of(prop_key: str) -> str:
    return prop_key.split(PROP_SEP, 1)[0]


def _variance(xs: list[float]) -> float:
    """总体方差（population variance）。"""
    n = len(xs)
    if n == 0:
        return 0.0
    mean = sum(xs) / n
    return sum((x - mean) ** 2 for x in xs) / n


# ── 聚合（核心）────────────────────────────────────────────────────────────────
def build_groups(edges: list[dict] | None = None,
                 w2: dict[str, dict] | None = None,
                 mis_dir: Path | str = DEFAULT_MIS_DIR) -> list[dict]:
    """把候选边按 MIS 聚合为群组，按歧义度降序。

    歧义度 = 群组内**目标命题数** × **目标命题可信度方差**（命题越分散、可信度越参差，歧义度越高）。
    建议 verdict 取自 W2：MIS 节点 OUT ⇒「reject 误解得以支持」；IN ⇒「approve」。
    ⚠️ 歧义度退化说明：本仓 79 命题 credibility **全 = 2（medium）**、42 MIS **全 = 1（low）**
    （596 实测），导致「可信度方差」项恒为 0 ⇒ 歧义度全 0，排序退化为按 `(-edge_count, mis_id)`
    保底（仍把边数多的组排前面，便于人审先啃大块）。待命题/误信号补可信度分级后，方差项才会激活。
    """
    if edges is None:
        edges = aeg.load_edges()
    if w2 is None:
        w2 = _w2_labels()
    names = _mis_name_map(mis_dir)

    by_mis: dict[str, list[dict]] = defaultdict(list)
    for e in edges:
        by_mis[_mis_of(e)].append(e)

    groups: list[dict] = []
    for mid, es in by_mis.items():
        props = {_prop_of(e) for e in es}
        cards = {_card_of(p) for p in props}
        creds = [float(w2.get(p, {}).get("credibility", 0)) for p in props]
        ambiguity = len(props) * _variance(creds)
        w2_label = w2.get(mid, {}).get("label", "—")
        suggested = {"OUT": "reject（命题成立，误解出局）",
                     "IN": "approve（误解得以支持）"}.get(w2_label, "—")
        groups.append({
            "mis_id": mid,
            "title": names.get(mid, mid),
            "edge_count": len(es),
            "cards": sorted(cards),
            "propositions": sorted(props),
            "n_props": len(props),
            "n_cards": len(cards),
            "ambiguity": ambiguity,
            "w2_label": w2_label,
            "suggested_verdict": suggested,
            "edges": es,
        })
    # 歧义度全 0（见 docstring 退化说明）时，靠 -edge_count 保底把大组排前面
    groups.sort(key=lambda g: (-g["ambiguity"], -g["edge_count"], g["mis_id"]))
    return groups


def _effective_annotations(annotations: list[dict]) -> dict[str, str]:
    """每条 edge_id 的生效人审动作（最后一条为准）。"""
    eff: dict[str, str] = {}
    for a in annotations:
        eid = str(a.get("edge_id") or "").strip()
        act = str(a.get("action") or "").strip()
        if eid and act in ACTIONS:
            eff[eid] = act
    return eff


# ── 输出 ───────────────────────────────────────────────────────────────────────
def cmd_list(groups: list[dict], output: str | None = None) -> int:
    lines = ["# 人审待审队列（按歧义度降序）\n",
             f"共 {len(groups)} 个 MIS 群组（源自 {sum(g['edge_count'] for g in groups)} 条候选边）。\n",
             "| 排序 | MIS 组 | 歧义度 | 边数 | 涉及卡 | 涉及命题 | W2 | 建议 verdict |",
             "|-----:|--------|-------:|-----:|-------:|---------:|----|--------------|"]
    for i, g in enumerate(groups, 1):
        lines.append(f"| {i} | `{g['mis_id']}` | {g['ambiguity']:.4f} | {g['edge_count']} "
                     f"| {g['n_cards']} | {g['n_props']} | {g['w2_label']} | {g['suggested_verdict']} |")
    lines.append("\n> 歧义度 = 群组内目标命题数 × 目标命题可信度方差（命题越分散、可信度越参差越高）。\n")
    text = "\n".join(lines) + "\n"
    if output:
        Path(output).write_text(text, encoding="utf-8")
        print(f"已写入队列报告：{output}（{len(groups)} 组）")
    else:
        print(text)
    return 0


def cmd_show(groups: list[dict], mis_id: str) -> int:
    g = next((x for x in groups if x["mis_id"] == mis_id), None)
    if g is None:
        print(f"[FAIL] 未找到 MIS 组：{mis_id}", file=sys.stderr)
        return 2
    print(f"# {g['mis_id']} · {g['title']}\n")
    print(f"- W2 标签：{g['w2_label']} ⇒ 建议 verdict：{g['suggested_verdict']}")
    print(f"- 歧义度：{g['ambiguity']:.4f}（命题数 {g['n_props']} × 方差）")
    print(f"- 边数：{g['edge_count']}；涉及卡：{', '.join('`'+c+'`' for c in g['cards'])}")
    print(f"- 目标命题：{', '.join('`'+p+'`' for p in g['propositions'])}\n")
    print("## 边明细\n")
    print("| edge id | 方向 | confidence | 证据（截断） |")
    print("|---------|------|------------|--------------|")
    for e in g["edges"]:
        ev = str(e.get("evidence") or "")[:80].replace("\n", " ")
        print(f"| `{e['id']}` | {e['direction']} | {e['confidence']} | {ev} |")
    print("\n## W2 判决理由\n")
    print(f"- 该 MIS 节点在 W2 下被判 `{g['w2_label']}`：79 命题全 IN / 42 误解全 OUT，"
          "攻击图在 W2 下一边倒；群组级人审主要价值在**复核 W2 是否正确**而非发现新结论。\n")
    return 0


def cmd_stats(groups: list[dict], edges: list[dict] | None = None) -> int:
    if edges is None:
        edges = aeg.load_edges()
    ann = aer.load_annotations()
    eff = _effective_annotations(ann)
    reviewed = sum(1 for e in edges if eff.get(e["id"]) in ACTIONS)
    pending = len(edges) - reviewed
    cnt_by_action = {a: 0 for a in ACTIONS}
    for a in eff.values():
        cnt_by_action[a] = cnt_by_action.get(a, 0) + 1

    print("# 人审进度统计\n")
    print(f"- 候选边总数：{len(edges)}；已审（生效）：{reviewed}；待审：{pending}")
    print(f"- 生效动作分布：approve={cnt_by_action['approve']} "
          f"reject={cnt_by_action['reject']} modify={cnt_by_action['modify']}\n")

    # 按 MIS 组
    by_mis_total: dict[str, int] = defaultdict(int)
    by_mis_reviewed: dict[str, int] = defaultdict(int)
    by_prop_total: dict[str, int] = defaultdict(int)
    by_prop_reviewed: dict[str, int] = defaultdict(int)
    for e in edges:
        mid = _mis_of(e)
        pid = _prop_of(e)
        by_mis_total[mid] += 1
        by_prop_total[pid] += 1
        if eff.get(e["id"]) in ACTIONS:
            by_mis_reviewed[mid] += 1
            by_prop_reviewed[pid] += 1

    print("## 按 MIS 组\n")
    print("| MIS 组 | 已审 | 待审 | 总数 |")
    print("|--------|-----:|-----:|-----:|")
    for g in groups:
        mid = g["mis_id"]
        tot = by_mis_total.get(mid, 0)
        rev = by_mis_reviewed.get(mid, 0)
        print(f"| `{mid}` | {rev} | {tot - rev} | {tot} |")

    print("\n## 按目标命题\n")
    print("| 命题 | 已审 | 待审 | 总数 |")
    print("|------|-----:|-----:|-----:|")
    for pid in sorted(by_prop_total):
        tot = by_prop_total[pid]
        rev = by_prop_reviewed.get(pid, 0)
        print(f"| `{pid}` | {rev} | {tot - rev} | {tot} |")
    return 0


def cmd_check(groups: list[dict], edges: list[dict] | None = None,
              w2: dict[str, dict] | None = None) -> int:
    """fail-loud：聚合结果必须与权威数据一致。"""
    if edges is None:
        edges = aeg.load_edges()
    if w2 is None:
        w2 = _w2_labels()
    errors: list[str] = []

    # 1) 边总数一致
    grouped_edges = [e for g in groups for e in g["edges"]]
    if len(grouped_edges) != len(edges):
        errors.append(f"聚合边总数 {len(grouped_edges)} ≠ 权威边总数 {len(edges)}")
    # 2) 每条边恰好归属一个 MIS 组（无重复、无遗漏）
    seen: dict[str, int] = defaultdict(int)
    for e in grouped_edges:
        seen[e["id"]] += 1
    dup = [k for k, v in seen.items() if v != 1]
    if dup:
        errors.append(f"{len(dup)} 条边被重复/遗漏聚合（应按 1 次出现）：{dup[:5]}…")
    # 3) 每个 MIS 组都能在 W2 找到标签
    for g in groups:
        if g["mis_id"] not in w2:
            errors.append(f"MIS 组 {g['mis_id']} 在 W2 节点里缺失（建议 verdict 无法判定）")
    # 4) 人审标注引用的 edge_id 必须存在
    ann = aer.load_annotations()
    valid_ids = {e["id"] for e in edges}
    bad = [a.get("edge_id") for a in ann if a.get("edge_id") not in valid_ids]
    if bad:
        errors.append(f"{len(bad)} 条人审标注引用了不存在的 edge_id：{bad[:5]}…")
    # 5) 群组数应为去重 MIS 数（= W2 OUT 数 42）
    if {g["mis_id"] for g in groups} != set(w2) - {k for k in w2 if k.startswith("ATOM-")}:
        # 仅软提示：W2 节点含命题与 MIS，群组应恰好覆盖所有 MIS 节点
        mis_nodes = {k for k in w2 if k.startswith("MIS-")}
        if {g["mis_id"] for g in groups} != mis_nodes:
            errors.append(f"群组 MIS 集合 ≠ W2 的 MIS 节点集合"
                          f"（差 {sorted(mis_nodes ^ {g['mis_id'] for g in groups})[:5]}）")

    if errors:
        print("[FAIL] 一致性校验未通过：", file=sys.stderr)
        for er in errors:
            print(f"  - {er}", file=sys.stderr)
        return 2
    print(f"[OK] 一致性校验通过：{len(edges)} 边 → {len(groups)} MIS 组，"
          f"W2 标签齐全，人审标注引用合法。")
    return 0


def cmd_feedback(groups: list[dict], edges: list[dict] | None = None) -> int:
    """人审反馈闭环（**只建议不执行**）：基于已审边生成生成器改进 / W2 校准建议，
    并做 automation-bias 检测（595：agree_rate==1.0 且理由过短 ⇒ 疑似 rubber-stamp）。
    """
    if edges is None:
        edges = aeg.load_edges()
    ann = aer.load_annotations()
    eff = _effective_annotations(ann)
    if not eff:
        print("无反馈数据（当前 0 条已审；人审结果文件 "
              "`data/human_attack_edge_annotations.jsonl` 尚不存在或为空）。")
        return 0

    edge_by_id = {e["id"]: e for e in edges}
    group_by_mis = {g["mis_id"]: g for g in groups}
    # 建议 verdict：W2 节点 OUT ⇒ reject；IN ⇒ approve
    def sugg_of(mid: str) -> str:
        return "reject" if group_by_mis.get(mid, {}).get("w2_label") == "OUT" else "approve"

    cnt = {"approve": 0, "reject": 0, "modify": 0}
    gen_sugg: list[str] = []      # 生成器改进（来自 reject）
    w2_sugg: list[str] = []       # W2 校准（来自 modify）
    aligned = 0
    short_reason = False
    reviewed = 0

    for eid, action in eff.items():
        e = edge_by_id.get(eid)
        if e is None or action not in ACTIONS:
            continue
        reviewed += 1
        cnt[action] += 1
        mid = _mis_of(e)
        prop = _prop_of(e)
        direction = e["direction"]
        kind = e.get("kind")
        orig_conf = e.get("confidence")
        # 该条人审的 reason（从 annotations 取最后一条有效 reason）
        reason = ""
        for a in ann:
            if a.get("edge_id") == eid and a.get("action") == action:
                reason = str(a.get("reason") or "")
        if len(reason) < 20:
            short_reason = True
        # 与建议 verdict 是否一致（建议统一为 reject，因 W2 全 OUT）
        if action == sugg_of(mid):
            aligned += 1

        if action == "reject":
            assoc = ("related_atoms" if kind == "related_atom"
                     else "refutations/misconceptions" if kind in ("misconception", "misconception_refutation")
                     else "关联字段")
            gen_sugg.append(
                f"- 边 `{eid}`（{mid} → `{prop}`，方向 {direction}，kind {kind}）：人工 **reject** "
                f"⇒ 建议复核生成器对 `{mid}` 的 `{assoc}` 关联是否过宽 / 命题映射是否不准确"
                f"（只建议，不改 `attack_edge_generator.py`）。")
        elif action == "modify":
            new_conf = None
            for a in ann:
                if a.get("edge_id") == eid and a.get("action") == "modify":
                    new_conf = a.get("confidence")
            w2_sugg.append(
                f"- 边 `{eid}`（{mid} → `{prop}`）：人工将可信度 `{orig_conf}` → `{new_conf}` "
                f"⇒ 建议 `weighted_af_solver` 对该 MIS 可信度档同步调整（只建议，不执行）。")

    agree_rate = (aligned / reviewed) if reviewed else 0.0
    L = ["# 人审反馈闭环建议（只建议不执行）\n",
         "## 概况\n",
         f"- 已审生效：{reviewed}（approve={cnt['approve']} / reject={cnt['reject']} "
         f"/ modify={cnt['modify']}）",
         f"- 与建议 verdict 一致率：{agree_rate * 100:.1f}%（建议 verdict 来自 W2：全 OUT ⇒ reject）\n"]

    # automation-bias 预警（595）
    if reviewed and agree_rate == 1.0 and short_reason:
        L.append("## ⚠️ automation-bias 预警\n")
        L.append("- 一致率 = 100% 且存在理由过短（<20 字符）的审查 ⇒ **疑似 rubber-stamp，建议复核**"
                 "（595 调研：人审在工具给出强建议时易不假思索地同意）。\n")
    elif reviewed and agree_rate == 1.0:
        L.append("## ⚠️ automation-bias 提示\n")
        L.append("- 一致率 = 100%（全与建议 reject 一致）；理由均充分，但仍建议抽样复核确认非 rubber-stamp。\n")

    L.append("## 生成器改进建议（来自 reject 边）\n")
    if gen_sugg:
        L.extend(gen_sugg)
    else:
        L.append("- 暂无（当前 0 条 reject）。\n")

    L.append("\n## W2 权重校准建议（来自 modify 边）\n")
    if w2_sugg:
        L.extend(w2_sugg)
    else:
        L.append("- 暂无（当前 0 条 modify）。\n")
    L.append("\n> 所有条目均为**建议**，本工具绝不自动修改 `attack_edge_generator.py` / "
             "`weighted_af_solver.py`（人审权力）。\n")
    print("\n".join(L))
    return 0


# ── CLI ───────────────────────────────────────────────────────────────────────
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="候选攻击边 MIS 群组级人审队列（只读）")
    ap.add_argument("--list", action="store_true", help="待审队列（歧义度排序）")
    ap.add_argument("--output", default=None, help="--list 写入报告文件而非 stdout")
    ap.add_argument("--show", metavar="MIS-ID", default=None,
                    help="群组详情，如 MIS-CONC-001")
    ap.add_argument("--stats", action="store_true",
                    help="人审进度统计（按 MIS 组 + 命题）")
    ap.add_argument("--check", action="store_true",
                    help="与 attack_edge_review 数据一致性校验（fail-loud）")
    ap.add_argument("--feedback", action="store_true",
                    help="人审反馈闭环：基于已审边生成生成器改进/W2校准建议（只建议不执行）")

    args = ap.parse_args(argv)

    if not (args.list or args.stats or args.check or args.feedback or args.show is not None):
        ap.error("必须指定一个动作：--list / --show / --stats / --check / --feedback")

    # 懒加载（四个动作都需要聚合）
    edges = aeg.load_edges()
    w2 = _w2_labels()
    groups = build_groups(edges, w2)

    if args.check:
        return cmd_check(groups, edges, w2)
    if args.feedback:
        return cmd_feedback(groups, edges)
    if args.show is not None:
        return cmd_show(groups, args.show)
    if args.list:
        return cmd_list(groups, args.output)
    if args.stats:
        return cmd_stats(groups, edges)
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
