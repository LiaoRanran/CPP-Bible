#!/usr/bin/env python3
"""613 任务C3 · 推荐路径图（拓扑排序 + 掌握度过滤）。

输入：`data/kc_inventory_612.json`（KC / 前置 / 后继 / 难度）+ `data/learner_state_612.jsonl`（掌握度）。
处理：
  1. 由 `prerequisites` 建 DAG（前置 → 本 KC）；`successors` 仅作交叉核对，不重复建边。
  2. **Kahn 拓扑排序**；同层内按 (难度, KC id) 升序确定性定序（避免每次跑出不同路径）。
  3. 环检测：若存在环 ⇒ 报告出来并**把环内节点整体后置于末尾**（fail-safe，绝不死循环、绝不丢节点）。
  4. 掌握度 ≥ 阈值（默认 0.5）标记「已掌握」，在推荐路径中折叠但**不删除**（保留全图可追溯）。
输出：`data/learning_path_613.md`（有序路径 + Mermaid 依赖图 + 下一步建议）。

CLI：
  python tools/learner_path_graph_613.py                 # 生成报告
  python tools/learner_path_graph_613.py --threshold 0.8 # 自定义掌握阈值
  python tools/learner_path_graph_613.py --check         # 自验证（exit 0=通过）
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import deque
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

KC_JSON = ROOT / "data" / "kc_inventory_612.json"
STATE = ROOT / "data" / "learner_state_612.jsonl"
OUT = ROOT / "data" / "learning_path_613.md"
USER = "default"
DEFAULT_THRESHOLD = 0.5


def load_kcs() -> list[dict]:
    d = json.loads(KC_JSON.read_text(encoding="utf-8"))
    return d.get("kcs", [])


def load_mastery() -> dict[str, float]:
    import learner_state as ls  # noqa: E402
    if not STATE.is_file():
        return {}
    return {kc: float(r.get("mastery_prob", 0.0))
            for (u, kc), r in ls.latest_by(STATE).items() if u == USER}


def build_graph(kcs: list[dict]) -> tuple[dict[str, set[str]], dict[str, int]]:
    """返回 (adj: 前置 -> {后继KC}, indeg: KC -> 前置数)。只按 prerequisites 建边。"""
    ids = {k["id"] for k in kcs}
    adj: dict[str, set[str]] = {i: set() for i in ids}
    indeg: dict[str, int] = {i: 0 for i in ids}
    for k in kcs:
        for p in (k.get("prerequisites") or []):
            pid = p if isinstance(p, str) else str(p.get("id", ""))
            if not pid or pid not in ids or pid == k["id"]:
                continue  # 悬空/自环前置：忽略（不建边，避免污染拓扑）
            adj[pid].add(k["id"])
    for src, dsts in adj.items():
        for d in dsts:
            indeg[d] += 1
    return adj, indeg


def topo_sort(kcs: list[dict], adj: dict[str, set[str]],
              indeg: dict[str, int]) -> tuple[list[str], list[str]]:
    """Kahn + 确定性定序。返回 (有序 id 列表, 环内 id 列表)。"""
    diff = {k["id"]: int(k.get("difficulty", 1) or 1) for k in kcs}
    indeg = dict(indeg)
    ready = sorted([i for i, d in indeg.items() if d == 0], key=lambda i: (diff.get(i, 1), i))
    q = deque(ready)
    order: list[str] = []
    while q:
        cur = q.popleft()
        order.append(cur)
        newly = []
        for nxt in sorted(adj.get(cur, ()), key=lambda i: (diff.get(i, 1), i)):
            indeg[nxt] -= 1
            if indeg[nxt] == 0:
                newly.append(nxt)
        for n in sorted(newly, key=lambda i: (diff.get(i, 1), i)):
            q.append(n)
    cyc = [i for i in indeg if i not in set(order)]
    # 环内节点按 (难度,id) 追加到末尾 ⇒ 不丢节点、不死循环
    order += sorted(cyc, key=lambda i: (diff.get(i, 1), i))
    return order, cyc


def render(kcs: list[dict], order: list[str], cyc: list[str], mastery: dict[str, float],
           adj: dict[str, set[str]], threshold: float) -> str:
    meta = {k["id"]: k for k in kcs}
    mastered = [i for i in order if mastery.get(i, 0.0) >= threshold]
    todo = [i for i in order if mastery.get(i, 0.0) < threshold]
    L = ["# 613 · 推荐学习路径图（C3）", "",
         f"> 生成：`python tools/learner_path_graph_613.py` ｜ 时间：{datetime.now().isoformat(timespec='seconds')}",
         f"> 算法：Kahn 拓扑排序（同层按 难度→KC id 确定性定序）；掌握阈值 = **{threshold}**。",
         "> 依赖边只取自 `prerequisites`；`successors` 仅交叉核对。", "",
         "## 一、规模", "",
         "| 项 | 值 |", "|---|---|",
         f"| KC 总数 | {len(kcs)} |",
         f"| 拓扑有序 | **{len(order)}** |",
         f"| 环内节点（后置到末尾） | {len(cyc)} |",
         f"| 已掌握（≥{threshold}） | {len(mastered)} |",
         f"| 待学习 | {len(todo)} |", ""]
    if cyc:
        L += [f"> ⚠ 检测到依赖环（{len(cyc)} 个节点）：{'、'.join(cyc[:10])}"
              f"{'…' if len(cyc) > 10 else ''} ⇒ 已后置，未丢弃。", ""]
    L += ["## 二、推荐路径（有序）", "",
          "| # | KC | 难度 | 掌握度 | 状态 | 前置 |", "|---|---|---|---|---|---|"]
    for i, kid in enumerate(order, 1):
        m = meta.get(kid, {})
        mv = mastery.get(kid, 0.0)
        st = "✅ 已掌握" if mv >= threshold else "⬜ 待学习"
        pre = m.get("prerequisites") or []
        L.append(f"| {i} | {kid} | {m.get('difficulty', '?')} | {mv:.4f} | {st} "
                 f"| {'、'.join(map(str, pre)) or '—'} |")
    L += ["", "## 三、下一步建议（前 5 个可学 KC）", ""]
    nxt = []
    for kid in todo:
        pre = meta.get(kid, {}).get("prerequisites") or []
        if all(mastery.get(p, 0.0) >= threshold for p in pre):
            nxt.append(kid)
    if nxt:
        for kid in nxt[:5]:
            L.append(f"- **{kid}**（难度 {meta.get(kid, {}).get('difficulty', '?')}，"
                     f"掌握度 {mastery.get(kid, 0.0):.4f}）— 前置已满足")
    else:
        L.append("- 当前无「前置已满足且未掌握」的 KC（或尚未接入真实掌握度）。")
    L += ["", "## 四、依赖图（Mermaid）", "", "```mermaid", "flowchart LR"]
    for kid in order:
        label = kid.replace("ATOM-", "").replace("-", "_")
        L.append(f"    {label}[{kid}]")
    for src, dsts in sorted(adj.items()):
        for d in sorted(dsts):
            L.append(f"    {src.replace('ATOM-', '').replace('-', '_')} --> "
                     f"{d.replace('ATOM-', '').replace('-', '_')}")
    L += ["```", "", "> 掌握度来源：`data/learner_state_612.jsonl`（612 为 simulate 模拟值；",
          "> 613 C2 接入真实行为后本图自动反映真实掌握度）。"]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="613 C3 · 推荐学习路径图（拓扑排序）")
    ap.add_argument("--threshold", type=float, default=DEFAULT_THRESHOLD)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)

    kcs = load_kcs()
    adj, indeg = build_graph(kcs)
    order, cyc = topo_sort(kcs, adj, indeg)

    if a.check:
        errs = []
        if len(kcs) != 27:
            errs.append(f"KC 数应为 27，实测 {len(kcs)}")
        if len(order) != len(kcs):
            errs.append(f"拓扑结果 {len(order)} ≠ KC 数 {len(kcs)}（不得丢节点）")
        if len(set(order)) != len(order):
            errs.append("拓扑结果含重复节点")
        # 依赖不倒置：每个 KC 必须排在其所有前置之后
        pos = {k: i for i, k in enumerate(order)}
        for k in kcs:
            for p in (k.get("prerequisites") or []):
                pid = p if isinstance(p, str) else str(p.get("id", ""))
                if pid in pos and pid != k["id"] and pos[pid] > pos.get(k["id"], -1) and pid not in cyc:
                    errs.append(f"依赖倒置：{pid} 排在 {k['id']} 之后")
        # 确定性
        if order != topo_sort(kcs, adj, indeg)[0]:
            errs.append("拓扑结果非确定性")
        for e in errs:
            print(f"[C3] ✗ {e}")
        print("[C3] " + ("✅ 自验证通过" if not errs else f"❌ {len(errs)} 项失败"))
        return 0 if not errs else 1

    mastery = load_mastery()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(render(kcs, order, cyc, mastery, adj, a.threshold),
                   encoding="utf-8", newline="\n")
    print(f"[C3] 写入 {OUT.relative_to(ROOT).as_posix()}（KC {len(kcs)} / 有序 {len(order)} "
          f"/ 环 {len(cyc)} / 阈值 {a.threshold}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
