#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""prop_closure.py — 命题闭包（582 N2 落地的**只读**基础设施；592 任务3）。

为什么需要：R4 grounded 论证层要算"全局可接受集"，前置是**依赖闭包**——一条命题成立与否，
取决于它引用的卡/证据，以及那些卡自己声明的命题，递归展开。没有闭包就没法定义可接受集，
所以先把这个纯图算法做出来、并且**用两种独立实现互相对账**（图算法的错法很多，
单一实现对账等于自证）。

闭包定义（`evidence →` 边，双向覆盖"命题引用卡"与"卡引用命题"）：
  * `prop_key → card`          命题引用**本卡**
  * `prop_key → evidence_id`   命题引用**证据卡**
  * `card → prop_key`          卡引用**它声明的命题**
从起点命题出发按上述有向边 BFS/递归可达的全部节点 = 闭包（节点含命题与卡两类 id）。

双实现对账：
  * Python：`closure()` —— 显式 BFS + visited 去重（环不死循环）；
  * SQL：`closure_sql()` —— `WITH RECURSIVE`（`UNION` 天然去重）。
两者在**同一份边集**上必须**集合逐元素相等**，不等 ⇒ `cross_check()` 返回差异、CLI exit 2。

只读硬纪律（本文件**没有任何写调用**：无 open('w')/write_text/unlink/subprocess）：
  * 绝不改卡、绝不改 `data/propositions.db`（库是 `prop_graph.py build` 的派生视图）；
  * 纯读连接（`sqlite3.connect` 默认不写；不建临时表、不写任何文件）。

用法：
    python tools/prop_closure.py stats [--json]            # 全库闭包统计（平均/最大/孤立）
    python tools/prop_closure.py from --id prop-1 [--json]  # 从指定命题出发的闭包
    python tools/prop_closure.py cross-check [--json]       # 双实现全量对账（79 命题逐个）
"""
# mypy: ignore-errors
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DB = ROOT / "data" / "propositions.db"
VERSION = "v1"

#: 边定义 —— **双实现共用的唯一真源**（改这里两边同时改，不会分叉）。
EDGE_UNION_SQL = (
    "SELECT card AS src, prop_key AS dst FROM props "
    "UNION ALL SELECT prop_key, card FROM props "
    "UNION ALL SELECT prop_key, evidence_id FROM prop_evidence"
)
#: 只读所需的最小列面（本工具不校验全 schema —— 那是 prop_graph 的职责）。
REQUIRED_COLUMNS = {"props": ("prop_key", "card"),
                    "prop_evidence": ("prop_key", "evidence_id")}
REBUILD_HINT = r"`.venv\Scripts\python.exe tools/prop_graph.py build`（纯派生视图，重建无损）"


def _connect(db: Path | str = DEFAULT_DB) -> sqlite3.Connection:
    """打开库并**先体检**（缺库/缺表/缺列 ⇒ fail-loud + 给出重建命令，不抛裸 OperationalError）。"""
    p = Path(db)
    if not p.is_file():
        raise SystemExit(f"[closure] 库不存在：{p}（先跑 {REBUILD_HINT}）")
    conn = sqlite3.connect(str(p))
    try:
        for table, cols in REQUIRED_COLUMNS.items():
            have = {r[1] for r in conn.execute(f"PRAGMA table_info({table})")}
            if not have:
                raise SystemExit(f"[closure] 库缺表 {table}（{p}）⇒ 先跑 {REBUILD_HINT}")
            missing = [c for c in cols if c not in have]
            if missing:
                raise SystemExit(f"[closure] 表 {table} 缺列 {missing} ⇒ 先跑 {REBUILD_HINT}")
    except BaseException:
        conn.close()
        raise
    return conn


# ── 边与邻接表 ──────────────────────────────────────────────────────────────────
def load_edges(db: Path | str = DEFAULT_DB) -> list[tuple[str, str]]:
    """读全量有向边（排序确定，便于对账/幂等）。"""
    conn = _connect(db)
    try:
        return [(str(s), str(t)) for s, t in conn.execute(
            f"SELECT src, dst FROM ({EDGE_UNION_SQL}) ORDER BY src, dst")]
    finally:
        conn.close()


def build_adjacency(edges) -> dict[str, set[str]]:
    adj: dict[str, set[str]] = {}
    for s, t in edges:
        adj.setdefault(str(s), set()).add(str(t))
    return adj


def prop_keys(db: Path | str = DEFAULT_DB) -> list[str]:
    conn = _connect(db)
    try:
        # prop_key = "<卡id>/<prop-id>" ⇒ 按 prop_key 排序等价于 (card, prop_id) 排序，
        # 且不依赖 prop_id 列存在（本工具只读最小列面）。
        return [str(r[0]) for r in conn.execute("SELECT prop_key FROM props ORDER BY prop_key")]
    finally:
        conn.close()


def resolve(db: Path | str, ident: str) -> list[str]:
    """把 CLI `--id` 解析成 prop_key 列表：**全名精确命中优先**；否则按卡内 prop_id 全量匹配。

    `prop-1` 这类卡内 id 跨卡重名（实测 27 条）⇒ 返回全部（排序确定），由调用方逐条展示。
    """
    keys = prop_keys(db)
    if ident in set(keys):
        return [ident]
    return sorted(k for k in keys if k.rsplit("/", 1)[-1] == ident)


# ── 实现一：Python BFS ─────────────────────────────────────────────────────────
def closure(start: str, adjacency: dict[str, set[str]]) -> set[str]:
    """从 `start` 出发的可达集合（含起点自身）。环由 visited 去重终止，不会无限递归。"""
    seen = {start}
    dq: deque[str] = deque([start])
    while dq:
        cur = dq.popleft()
        for nxt in adjacency.get(cur, ()):
            if nxt not in seen:
                seen.add(nxt)
                dq.append(nxt)
    return seen


# ── 实现二：SQLite WITH RECURSIVE ──────────────────────────────────────────────
def _edge_cte(edges: list[tuple[str, str]] | None) -> tuple[str, list[str]]:
    """边 CTE 的 SQL 体：`None` ⇒ 从库表推；给了边列表 ⇒ 用 `VALUES` 内联（**不建临时表**）。"""
    if edges is None:
        return EDGE_UNION_SQL, []
    if not edges:
        return "SELECT NULL AS src, NULL AS dst WHERE 0", []
    body = "VALUES " + ", ".join("(?,?)" for _ in edges)
    return body, [x for e in edges for x in e]


def closure_sql(conn: sqlite3.Connection, start: str,
                edges: list[tuple[str, str]] | None = None) -> set[str]:
    """SQL 递归实现（与 `closure()` 必须逐元素相同）。

    `edges=None` ⇒ 边取库表（`EDGE_UNION_SQL`）；否则用内联 `VALUES`（合成图对账用，
    仍然**只读**：不建临时表、不写库文件）。
    """
    body, params = _edge_cte(edges)
    sql = (f"WITH edges(src, dst) AS ({body}),\n"
           "recursive_closure(id) AS (\n"
           "  SELECT ?\n"
           "  UNION\n"
           "  SELECT e.dst FROM edges e JOIN recursive_closure c ON e.src = c.id\n"
           ")\n"
           "SELECT id FROM recursive_closure")
    return {str(r[0]) for r in conn.execute(sql, [*params, start])}


# ── 对账 ───────────────────────────────────────────────────────────────────────
def cross_check(db: Path | str = DEFAULT_DB) -> list[dict]:
    """双实现全量对账：逐命题比对集合。返回不一致清单（空 = 全一致）。"""
    conn = _connect(db)
    try:
        edges = [(str(s), str(t)) for s, t in conn.execute(
            f"SELECT src, dst FROM ({EDGE_UNION_SQL})")]
        adj = build_adjacency(edges)
        mismatches = []
        for key in prop_keys(db):
            py = closure(key, adj)
            sq = closure_sql(conn, key)          # 走库表边，独立于上面的内存邻接表
            if py != sq:
                mismatches.append({"prop_key": key, "only_python": sorted(py - sq),
                                   "only_sql": sorted(sq - py)})
        return mismatches
    finally:
        conn.close()


# ── 统计 ───────────────────────────────────────────────────────────────────────
def stats(db: Path | str = DEFAULT_DB) -> dict:
    """全库闭包统计：命题/卡/边数、闭包大小分布、平均/最大、孤立命题、连通分量数。

    节点 id 含两类（命题 + 卡）⇒ `avg_closure_size` 是"全体节点"口径；另给 `avg_closure_props`
    只数可达**命题**（给人读时更直观）。
    """
    conn = _connect(db)
    try:
        props = prop_keys(db)
        all_props = set(props)
        rows = [(str(s), str(t)) for s, t in conn.execute(
            f"SELECT src, dst FROM ({EDGE_UNION_SQL})")]
        adj = build_adjacency(rows)
        nodes_all = {x for pair in rows for x in pair}
        sizes, psizes, isolated, seen = {}, {}, [], set()
        components = 0
        for k in props:
            c = closure(k, adj)
            sizes[k] = len(c)
            psizes[k] = len(c & all_props)
            if c == {k}:
                isolated.append(k)
            if not (c & seen):
                components += 1
            seen |= c
        vals = sorted(sizes.values())
        pvals = sorted(psizes.values())
        prop_cards = {r[0] for r in conn.execute("SELECT DISTINCT card FROM props")}
        card_nodes = nodes_all - all_props
        return {"tool": "prop_closure", "version": VERSION, "db": str(Path(db)),
                "propositions": len(props), "cards": len(prop_cards),
                "card_nodes": len(card_nodes),
                "evidence_cards": len(card_nodes - prop_cards),
                "edges": len(set(rows)), "edge_rows": len(rows),
                "components": components,
                "avg_closure_size": round(sum(vals) / len(vals), 3) if vals else None,
                "max_closure_size": vals[-1] if vals else None,
                "min_closure_size": vals[0] if vals else None,
                "avg_closure_props": round(sum(pvals) / len(pvals), 3) if pvals else None,
                "max_closure_props": pvals[-1] if pvals else None,
                "isolated": isolated,
                "size_histogram": {str(v): vals.count(v) for v in sorted(set(vals))},
                "closure_sizes": sizes,
                "note": "闭包节点含「命题 + 卡」两类 id ⇒ avg_closure_size 是全体节点口径；"
                        "avg_closure_props 只数可达命题"}
    finally:
        conn.close()


def _print_closure(key: str, info: dict) -> None:
    print(f"[closure] {key} ⇒ 闭包 {info['size']} 节点")
    print(f"  可达命题（{len(info['closure_props'])}）：")
    for p in info["closure_props"]:
        print(f"    - {p}")
    cards = [n for n in info["nodes"] if n not in set(info["closure_props"])]
    print(f"  可达卡（{len(cards)}）：{', '.join(cards)}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="命题闭包（只读；Python/SQL 双实现对账）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("stats", help="全库闭包统计")
    f = sub.add_parser("from", help="从指定命题出发的闭包")
    f.add_argument("--id", required=True, help="命题 prop_key（`<卡>/prop-1`）或卡内 prop_id（如 prop-1）")
    c = sub.add_parser("cross-check", help="双实现全量对账")
    for sp in (s, f, c):
        sp.add_argument("--db", default=str(DEFAULT_DB))
        sp.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.cmd == "cross-check":
        bad = cross_check(a.db)
        total = len(prop_keys(a.db))
        if a.json:
            print(json.dumps({"tool": "prop_closure", "version": VERSION, "checked": total,
                              "mismatches": bad}, ensure_ascii=False, indent=1))
        else:
            print(f"[closure] 双实现对账：{total - len(bad)}/{total} 一致"
                  + ("" if not bad else f"，**{len(bad)} 条不一致**"))
            for m in bad:
                print(f"  ❌ {m['prop_key']}  仅 Python {m['only_python']} / 仅 SQL {m['only_sql']}")
        return 0 if not bad else 2

    if a.cmd == "stats":
        st = stats(a.db)
        if a.json:
            print(json.dumps(st, ensure_ascii=False, indent=1))
            return 0
        print(f"[closure] 命题 {st['propositions']} · 命题所属卡 {st['cards']}"
              f" · 卡节点 {st['card_nodes']}（其中证据卡 {st['evidence_cards']}）"
              f" · 边 {st['edges']} · 连通分量 {st['components']}")
        print(f"[closure] 闭包大小（全体节点）avg {st['avg_closure_size']} / "
              f"max {st['max_closure_size']} / min {st['min_closure_size']}"
              f" · 分布 {st['size_histogram']}")
        print(f"[closure] 可达命题数 avg {st['avg_closure_props']} / max {st['max_closure_props']}")
        print(f"[closure] 孤立命题（闭包 = 自身）{len(st['isolated'])} 条"
              + (f"：{st['isolated'][:10]}" if st["isolated"] else ""))
        print(f"[closure] 注：{st['note']}")
        return 0

    # from
    all_props = set(prop_keys(a.db))
    edges = load_edges(a.db)
    keys = resolve(a.db, a.id)
    if not keys:
        print(f"[closure] 找不到命题 {a.id!r}（可用 prop_key `<卡>/<prop-id>` 或卡内 prop_id）",
              file=sys.stderr)
        return 1
    if len(keys) > 1 and not a.json:
        print(f"[closure] {a.id!r} 是卡内 id、命中 {len(keys)} 条（跨卡重名），逐条列出：")
    payload = {}
    adj = build_adjacency(edges)
    for k in keys:
        nodes = closure(k, adj)
        info = {"size": len(nodes), "nodes": sorted(nodes),
                "closure_props": sorted(nodes & all_props)}
        payload[k] = info
        if not a.json:
            _print_closure(k, info)
    if a.json:
        print(json.dumps({"tool": "prop_closure", "version": VERSION, "query": a.id,
                          "closures": payload}, ensure_ascii=False, indent=1))
    return 0

if __name__ == "__main__":
    if "--check" in sys.argv:
        print("OK: prop_closure --check（只读：加载即校验，不执行任何业务逻辑）")
        sys.exit(0)
    raise SystemExit(main())
