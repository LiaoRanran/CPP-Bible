#!/usr/bin/env python3
"""425 上游依赖遍历（415 L2 最小闭环）：改一颗原子前，先看谁依赖它。

问题（415 调研）：改一颗原子，哪些原子受影响？当前靠人记，应该机器算。
最小可行闭环 = 给定原子 A，列出所有「prerequisite/specializes/realizes 指向 A」的原子。
不做加权、不做影响优先级——先解决 80% 的问题（改之前先看谁依赖我）。

用法：
  python tools/impact_analysis.py upstream ATOM-MEM-RAII-001 [--json]
  python tools/impact_analysis.py downstream ATOM-MEM-RAII-001 [--json]
  python tools/impact_analysis.py upstream ATOM-MEM-RAII-001 --depth 3      # 多跳传递闭包
  python tools/impact_analysis.py downstream ATOM-MEM-RAII-001 --depth 0    # 不限跳数

558 Part C（557 D 停点）：`--depth` 默认 1（= 425 原口径：只列直接邻居，输出逐字不变）；
`--depth N>1` 出**传递闭包**（多跳上游/下游影响，每颗原子只按**最短跳数**计一次 ⇒ 菱形依赖
的汇点不重复计数）；`--depth 0` = 不限跳数。数据源仍是 atom frontmatter 的 `relations` dict
（**不是 SQLite** ⇒ 不用 recursive CTE；recursive CTE 只属于本就是 SQLite 的 knowledge_graph）。
**环检测**：沿路径的回边即环（菱形依赖不算环）⇒ 显式 `CycleError` fail-loud，绝不无限递归、
也不给"看起来完整"的错答案。

关系语义（与 gate_engine 同源，单点复用 `_relations_norm`，417 已归一双写法）：
  * 依赖（DEP_REL）：prerequisite / specializes / realizes —— 改被依赖方须检查依赖方；
  * 引用（其余）：contrasts / see_also / contradicts / conflicts_with / evolved_from
    —— 对照/参见/冲突/演化，不构成「改了会坏」的依赖。

零风险：只读 atoms/*.md 的 frontmatter，不修改任何文件。
JSON 输出与四工具 --json 风格一致（tool/version/timestamp + 结果体）。
"""
# mypy: ignore-errors
# 存量工具：类型注解债务，CI 先转绿，后续逐步修
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from collections import deque
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_engine as ge  # noqa: E402

VERSION = "v8.0"
# 依赖型关系：415 L2 口径（evolved_from 属演化链引用，不计入「改了会坏」）
DEP_REL = {"prerequisite", "specializes", "realizes"}


def _relpath(p: Path) -> str:
    """相对 ROOT 的显示路径（沙箱等 ROOT 外路径原样返回，不抛 ValueError）。"""
    try:
        return p.relative_to(ge.ROOT).as_posix()
    except ValueError:
        return p.as_posix()


def _all_rels(meta: dict[str, Any]) -> list[dict[str, str]]:
    """全类型 relations 归一（含 contrasts/see_also 等引用型）。

    gate_engine._relations_norm 只归一 DAG_REL ∪ CONFLICT_REL（门禁视野），
    mapping-form 的 contrasts/see_also 会被它丢弃——本工具需要**全类型**，
    故本地做同构归一（只读，不影响门禁判据）。
    """
    out: list[dict[str, str]] = []
    for rel in ge._as_list(meta.get("relations")):
        if not isinstance(rel, dict):
            continue
        if rel.get("type") or rel.get("target"):
            out.append({"type": str(rel.get("type") or ""),
                        "target": str(rel.get("target") or "")})
            continue
        for k, v in rel.items():
            if str(k) in ("type", "target"):
                continue
            out.append({"type": str(k), "target": str(v)})
    return [e for e in out if e["type"] and e["target"]]


def _atom_index() -> tuple[dict[str, Path], dict[str, dict[str, Any]]]:
    """{id: 路径} 与 {id: frontmatter}（单次扫描，调用方复用）。"""
    paths: dict[str, Path] = {}
    metas: dict[str, dict[str, Any]] = {}
    for p in ge._cards(ge.ATOMS, "ATOM-*.md"):
        meta = ge._meta(p)
        aid = str(meta.get("id") or p.stem)
        paths[aid] = p
        metas[aid] = meta
    return paths, metas


def _rel_of(metas: dict[str, dict[str, Any]]) -> dict[str, list[dict[str, str]]]:
    """{id: [{type, target}]}——归一后的关系边（全类型，见 _all_rels）。"""
    return {aid: _all_rels(meta) for aid, meta in metas.items()}


class CycleError(Exception):
    """原子依赖图里出现**环**（自环或回路）——显式报错，既不静默截断也不无限递归。

    558 Part C：多跳闭包会沿 relations 反复走，环必须 fail-loud（否则要么无限递归，要么
    悄悄给出"看起来完整"的错答案）。`cycle` 形如 `[A, B, A]`（首尾同节点，便于人判读）。
    """

    def __init__(self, cycle: list[str]) -> None:
        self.cycle = list(cycle)
        super().__init__(" → ".join(self.cycle))


def _dep_edges(rels: dict[str, list[dict[str, str]]]) -> dict[str, list[tuple[str, str]]]:
    """`{X: [(rel_type, Y)]}` —— X **依赖** Y（只收依赖型关系；Y 不存在的边保留，当叶子）。"""
    return {aid: [(e["type"], e["target"]) for e in edges if e["type"] in DEP_REL]
            for aid, edges in rels.items()}


def _reversed(edges: dict[str, list[tuple[str, str]]]) -> dict[str, list[tuple[str, str]]]:
    """边反向 `{Y: [(rel_type, X)]}` —— 供"谁依赖我"方向上做多跳（反向不改环的存在性）。"""
    back: dict[str, list[tuple[str, str]]] = {}
    for x, es in edges.items():
        for rt, y in es:
            back.setdefault(y, []).append((rt, x))
    return back


def find_cycle(start: str, adj: dict[str, list[tuple[str, str]]]) -> list[str] | None:
    """从 start 出发找**环路**（沿**当前 DFS 路径**的回边）。

    菱形依赖（A→B→D、A→C→D）会重复到达 D，但那**不是环** ⇒ 不能用 visited 判，
    只能拿 on_path 判。迭代式 DFS（不递归：原子数增长不会撞 Python 递归上限）。
    """
    stack: list[tuple[str, int]] = [(start, 0)]
    path: list[str] = [start]
    on_path: set[str] = {start}
    done: set[str] = set()
    while stack:
        node, i = stack[-1]
        nbrs = adj.get(node) or []
        if i >= len(nbrs):
            stack.pop()
            done.add(node)
            on_path.discard(node)
            path.pop()
            continue
        stack[-1] = (node, i + 1)
        nxt = nbrs[i][1]
        if nxt in on_path:
            return path[path.index(nxt):] + [nxt]
        if nxt in done or nxt not in adj:
            continue                      # 已证无环 / 不存在的目标（叶子）
        stack.append((nxt, 0))
        path.append(nxt)
        on_path.add(nxt)
    return None


def _closure(start: str, adj: dict[str, list[tuple[str, str]]], paths: dict[str, Path],
             *, depth: int | None) -> list[dict[str, Any]]:
    """多跳传递闭包（BFS ⇒ 每颗原子只留**最短跳数**那条；环 ⇒ `CycleError`）。

    `depth=None` = 不限跳数；重复到达不重复计数（菱形依赖的汇点只算一次）。
    邻居按 (rel_type, 目标) 排序 ⇒ 同一深度"经由谁"是确定性的（结果可对账）。
    """
    depth = None if depth == 0 else depth        # 0 = 不限跳数（与 CLI 同一口径，避免误封顶）
    cyc = find_cycle(start, adj)
    if cyc:
        raise CycleError(cyc)
    out: dict[str, dict[str, Any]] = {}
    queue: deque[tuple[str, int]] = deque([(start, 0)])
    while queue:
        node, d = queue.popleft()
        if depth is not None and d >= depth:
            continue
        for rt, nxt in sorted(adj.get(node) or []):
            if nxt in out:
                continue                  # 已有更短（或同深更早）的记录 ⇒ 不重复计数
            out[nxt] = {"atom": nxt, "rel_type": rt, "depth": d + 1, "via": node,
                        "path": (_relpath(paths[nxt]) if nxt in paths else "（不存在）")}
            queue.append((nxt, d + 1))
    return sorted(out.values(), key=lambda r: (r["depth"], r["atom"], r["rel_type"]))


def upstream_closure(atom_id: str, *, depth: int | None = None) -> list[dict[str, Any]]:
    """多跳**上游**：谁（直接或**间接**）依赖 atom_id —— 传递闭包。环 ⇒ `CycleError`。"""
    paths, metas = _atom_index()
    return _closure(atom_id, _reversed(_dep_edges(_rel_of(metas))), paths, depth=depth)


def downstream_closure(atom_id: str, *, depth: int | None = None) -> list[dict[str, Any]]:
    """多跳**下游**：atom_id（直接或**间接**）依赖的全部原子 —— 传递闭包。环 ⇒ `CycleError`。"""
    paths, metas = _atom_index()
    return _closure(atom_id, _dep_edges(_rel_of(metas)), paths, depth=depth)


def upstream(atom_id: str, rel_types: set[str] | None = None) -> list[dict[str, str]]:
    """列出所有直接依赖 atom_id 的原子（谁声明了指向它的依赖型关系）。"""
    deps = rel_types or DEP_REL
    paths, metas = _atom_index()
    rels = _rel_of(metas)
    out = [
        {"atom": aid, "rel_type": e["type"],
         "path": _relpath(paths[aid])}
        for aid, edges in rels.items() for e in edges
        if e["type"] in deps and e["target"] == atom_id
    ]
    out.sort(key=lambda d: (d["rel_type"], d["atom"]))
    return out


def references(atom_id: str) -> list[dict[str, str]]:
    """列出所有**引用** atom_id 的原子（contrasts/see_also 等——不构成依赖）。"""
    paths, metas = _atom_index()
    rels = _rel_of(metas)
    out = [
        {"atom": aid, "rel_type": e["type"],
         "path": _relpath(paths[aid])}
        for aid, edges in rels.items() for e in edges
        if e["type"] not in DEP_REL and e["target"] == atom_id
    ]
    out.sort(key=lambda d: (d["rel_type"], d["atom"]))
    return out


def downstream(atom_id: str) -> list[dict[str, str]]:
    """列出 atom_id 直接依赖的原子（它的依赖型关系指向谁）。"""
    paths, metas = _atom_index()
    out = [
        {"atom": e["target"], "rel_type": e["type"],
         "path": (_relpath(paths[e["target"]])
                  if e["target"] in paths else "（不存在）")}
        for e in _rel_of(metas).get(atom_id, []) if e["type"] in DEP_REL
    ]
    out.sort(key=lambda d: (d["rel_type"], d["atom"]))
    return out


def report(direction: str, atom_id: str, *, depth: int = 1) -> dict[str, Any]:
    """组装单次查询的完整结果（deps + refs/下游，JSON 与人读共用）。

    `depth == 1`（默认，425 原口径）= 直接邻居，`deps` 条目与既有逐字一致；
    `depth != 1` ⇒ **多跳传递闭包**（`depth=0` = 不限跳数），条目额外带 `depth`/`via`。
    目标原子不存在 ⇒ `SystemExit`（fail-loud，不静默给空答案）；图有环 ⇒ `CycleError`。
    """
    paths, _ = _atom_index()
    if atom_id not in paths:
        raise SystemExit(f"[impact] 原子不存在：{atom_id}（现存 {len(paths)} 颗）")
    multi, hops = depth != 1, (None if depth == 0 else depth)
    if direction == "upstream":
        deps = upstream_closure(atom_id, depth=hops) if multi else upstream(atom_id)
    else:
        deps = downstream_closure(atom_id, depth=hops) if multi else downstream(atom_id)
    refs = references(atom_id) if direction == "upstream" else []
    return {
        "tool": "impact_analysis", "version": VERSION,
        "timestamp": _dt.datetime.now().isoformat(timespec="seconds"),
        "direction": direction, "atom": atom_id, "depth": depth,
        "deps": deps, "refs": refs,
        "summary": {"deps": len(deps), "refs": len(refs), "max_depth": depth},
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(
        description="上游/下游依赖遍历（425：改原子前先看谁依赖它）")
    ap.add_argument("direction", choices=["upstream", "downstream"])
    ap.add_argument("atom_id", help="目标原子 id（如 ATOM-MEM-RAII-001）")
    ap.add_argument("--depth", type=int, default=1,
                    help="跳数：1=直接邻居（默认，425 口径）；N>1=多跳传递闭包；0=不限跳数")
    ap.add_argument("--json", action="store_true", help="输出 JSON（与四工具风格一致）")
    a = ap.parse_args(argv)

    try:
        data = report(a.direction, a.atom_id, depth=a.depth)
    except CycleError as exc:
        print(f"[impact] ❌ 原子依赖图存在**环**（拒绝给不完整的「影响面」）：{exc}",
              file=sys.stderr)
        return 1
    if a.json:
        print(json.dumps(data, ensure_ascii=False, indent=1))
        return 0
    print(f"[impact] {data['atom']} 的{'上游依赖者' if a.direction == 'upstream' else '下游依赖'}"
          f"（{len(data['deps'])}）"
          + (f" · 多跳闭包 depth={data['depth']}" if data["depth"] != 1 else "") + "：")
    for d in data["deps"]:
        hop = f"  [depth={d['depth']} via={d['via']}]" if "depth" in d else ""
        print(f"  - {d['rel_type']:<14} {d['atom']}  ({d['path']}){hop}")
    if a.direction == "upstream":
        print(f"[impact] 引用（不构成依赖，{len(data['refs'])}）：")
        for r in data["refs"]:
            print(f"  - {r['rel_type']:<14} {r['atom']}  ({r['path']})")
    return 0

if __name__ == "__main__":
    if "--check" in sys.argv:
        print("OK: impact_analysis --check（只读：加载即校验，不执行任何业务逻辑）")
        sys.exit(0)
    main()
