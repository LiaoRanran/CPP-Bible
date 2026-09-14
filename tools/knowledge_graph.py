#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""knowledge_graph.py — 知识图谱 L1（508 任务5）。

为什么（497/508）：原子/证据/误解/工件之间的关系此前只能靠"逐个 Read 卡"或
`impact_analysis.py` 的**单层**查询来理解。跨层的多跳问题（"改这个夹具会波及哪些原子"、
"这颗原子的完整前置链是什么"、"哪些节点其实无人引用"）每次都要人工拼。L1 把这些关系
物化成一张 SQLite 图，使多跳查询变成一次 SQL。

设计取舍
========
* **SQLite 而非图数据库**：零新依赖（stdlib `sqlite3`），单文件可随备份带走，
  百级节点规模下 WAL + mmap 足够；图数据库引入的部署成本换不来收益。
* **`data/knowledge_graph.db` 是派生物**：可随时 `build` 重建，故进 `.gitignore`
  （与 `data/traces/` 同口径）；备份由 `backup.py` 负责（任务 7 白名单含它）。
* **关系归一复用单点**：`relations` 字段的解析走 `impact_analysis._all_rels`
  （它又复用 `gate_engine._relations_norm` 与 `_as_list`），**不另写一套**
  ——373 §5 的教训：同一份语法写两套语义，改一处漏一处。
* **悬空目标不吞**：`relations` 指向未锻造的 id（如 `ATOM-UB-ALIAS-001`）时，
  插入 **stub 节点**（`status='dangling'`）并保留边——外键仍成立，且
  `orphans`/`stats` 能看见它们（"规划中前向引用"是知识库的正常状态，不该被静默丢弃）。

用法
====
    python tools/knowledge_graph.py build      # 重建图（幂等：先 DROP 再建）
    python tools/knowledge_graph.py stats      # 节点/边数 + 类型分布
    python tools/knowledge_graph.py deps  ATOM-MEM-MOVE-002     # 直接依赖（出边）
    python tools/knowledge_graph.py impact Examples/atoms/_atom_x.cpp   # 上游影响（改这个文件波及谁）
    python tools/knowledge_graph.py chain ATOM-MEM-MOVE-002    # 完整依赖链（多跳）
    python tools/knowledge_graph.py orphans    # 孤立节点（无入边无出边）
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import gate_engine as ge               # noqa: E402
import impact_analysis as imp          # noqa: E402
import atom_evidence_replay as replay  # noqa: E402

DB = ROOT / "data" / "knowledge_graph.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS nodes (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL,  -- ATOM/EVIDENCE/MISCONCEPTION/FIXTURE/ARTIFACT/RULE
    path TEXT,
    title TEXT,
    status TEXT
);
CREATE TABLE IF NOT EXISTS edges (
    src TEXT NOT NULL,
    dst TEXT NOT NULL,
    type TEXT NOT NULL,
    PRIMARY KEY (src, dst, type),
    FOREIGN KEY (src) REFERENCES nodes(id),
    FOREIGN KEY (dst) REFERENCES nodes(id)
);
CREATE INDEX IF NOT EXISTS idx_edges_src ON edges(src);
CREATE INDEX IF NOT EXISTS idx_edges_dst ON edges(dst);
CREATE INDEX IF NOT EXISTS idx_edges_type ON edges(type);
CREATE INDEX IF NOT EXISTS idx_nodes_type ON nodes(type);
"""

# 关系名 → 边类型（大小写/同义词归一）。表外取值归 REFERENCES 并在 build 时计数留痕
# （472 P1-4：结束同义词枚举，未知不静默——但图谱是**分析**工具，不该因未知类型而中断，
# 故这里是"归入 REFERENCES + 计数"，与 gate 的 ATOM-REL-UNKNOWN 各司其职）。
REL_MAP = {
    "prerequisite": "PREREQUISITE", "requires": "PREREQUISITE",
    "specializes": "SPECIALIZES", "subtype": "SPECIALIZES",
    "realizes": "REALIZES", "implements": "REALIZES",
    "evolved_from": "EVOLVED_FROM", "successor_of": "EVOLVED_FROM",
    "contrasts": "CONTRADICTS", "contradicts": "CONTRADICTS",
    "refutes": "CONTRADICTS", "misconceived_as": "CONTRADICTS",
    "see_also": "REFERENCES", "references": "REFERENCES", "related": "REFERENCES",
}


def connect(path: Path | None = None) -> sqlite3.Connection:
    p = path or DB
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(p))
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-64000")
    conn.execute("PRAGMA mmap_size=268435456")
    return conn


def _meta(p: Path) -> dict:
    try:
        return replay.parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
    except ValueError:
        return {}


def _stub_type(nid: str) -> str:
    if nid.startswith("ATOM-"):
        return "ATOM"
    if nid.startswith("EV-"):
        return "EVIDENCE"
    if nid.startswith("MIS-"):
        return "MISCONCEPTION"
    return "ATOM"


def _infer_type(rel: str | None) -> str:
    """关系名首词的**单数**形态 → 节点类型（`contrasts: ATOM-X` → ATOM）。"""
    return _stub_type(str(rel or ""))


def build(conn: sqlite3.Connection, *, verbose: bool = True) -> dict:
    """重建图（幂等）：DROP → 建表 → 扫卡 → 插节点/边。返回统计。"""
    conn.executescript("DROP TABLE IF EXISTS edges; DROP TABLE IF EXISTS nodes;")
    conn.executescript(SCHEMA)
    nodes: dict[str, tuple] = {}

    def add(nid: str, ntype: str, path: str = "", title: str = "", status: str = "") -> None:
        if not nid:
            return
        if nid not in nodes:
            nodes[nid] = (nid, ntype, path, title, status)
        elif path and not nodes[nid][2]:           # 先建了 stub，后用真实信息补全
            nodes[nid] = (nid, ntype, path, title, status)

    # ── 节点：原子 / 证据 / 误解 ────────────────────────────────────────────
    for p in ge._cards(ge.ATOMS, "ATOM-*.md"):
        m = _meta(p)
        add(str(m.get("id") or p.stem), "ATOM", ge._rel(p),
            str(m.get("title") or ""), str(m.get("status") or ""))
    for p in ge._cards(ge.EVIDENCE, "EV-*.md"):
        m = _meta(p)
        add(str(m.get("id") or p.stem), "EVIDENCE", ge._rel(p),
            str(m.get("hypothesis") or "")[:80], str(m.get("verdict") or ""))
    mis = ROOT / "misconceptions"
    if mis.is_dir():
        for p in sorted(mis.rglob("*.md")):
            if p.name.startswith("README"):
                continue
            m = _meta(p)
            add(str(m.get("id") or p.stem), "MISCONCEPTION", ge._rel(p),
                str(m.get("name") or ""), str(m.get("level") or ""))

    # ── 节点：规则（来自 gate 注册表；无路径，只有 id/severity）─────────────
    for r in ge.RULES:
        add(r.id, "RULE", "", r.title, r.severity)

    edges: list[tuple[str, str, str]] = []
    unknown_rel = 0

    def add_edge(src: str, dst: str, etype: str) -> None:
        if src and dst and src != dst:
            edges.append((src, dst, etype))

    # ── 边：证据卡 → 原子（SERVES）/ 夹具（USES）/ 工件（ASSERTS）───────────
    for p in ge._cards(ge.EVIDENCE, "EV-*.md"):
        m = _meta(p)
        eid = str(m.get("id") or p.stem)
        for s in ge._as_list(m.get("serves")):
            add(str(s), "ATOM", status="dangling" if str(s) not in nodes else "")
            add_edge(eid, str(s), "SERVES")
        for key, ntype, etype in (("fixture", "FIXTURE", "USES"),
                                  ("artifact", "ARTIFACT", "ASSERTS")):
            rel = str(m.get(key) or "").strip()
            if rel:
                nid = f"{ntype.lower()}:{rel}"
                add(nid, ntype, rel, "", "dangling" if not (ROOT / rel).is_file() else "")
                add_edge(eid, nid, etype)
        for e in ge._as_list(m.get("artifacts")):
            rel = e if isinstance(e, str) else (
                (e.get("path") or e.get("file")) if isinstance(e, dict) else "")
            if rel:
                nid = f"artifact:{rel}"
                add(nid, "ARTIFACT", str(rel), "",
                    "dangling" if not (ROOT / str(rel)).is_file() else "")
                add_edge(eid, nid, "ASSERTS")

    # ── 边：原子 relations（复用单点归一）────────────────────────────────────
    for p in ge._cards(ge.ATOMS, "ATOM-*.md"):
        m = _meta(p)
        aid = str(m.get("id") or p.stem)
        for rel in imp._all_rels(m):
            rtype = str(rel.get("type") or "")
            tgt = str(rel.get("target") or "")
            if not tgt:
                continue
            et = REL_MAP.get(rtype.lower())
            if et is None:
                unknown_rel += 1
                et = "REFERENCES"
            add(tgt, _infer_type(rtype), status="dangling" if tgt not in nodes else "")
            add_edge(aid, tgt, et)

    # ── 边：误解卡 related_atoms → 原子 ────────────────────────────────────
    # 用中性的 REFERENCES 而不是 CONTRADICTS：卡里写的是"相关原子"（related_atoms），
    # 并未声明"谁推翻谁"。语义强弱不能替作者加码——要表达 refutes/contrasts 时应写进
    # 原子的 relations（那是 gate 的 `ATOM-REL-*` 视野）。连上这条边的价值是让
    # `orphans` 真正只剩"确实无人引用"的节点，并让 `impact`（改工件波及谁）能穿到误解层。
    if mis.is_dir():
        for p in sorted(mis.rglob("*.md")):
            if p.name.startswith("README"):
                continue
            m = _meta(p)
            mid = str(m.get("id") or p.stem)
            for a in ge._as_list(m.get("related_atoms")):
                tgt = str(a).strip()
                if not tgt:
                    continue
                add(tgt, "ATOM", status="dangling" if tgt not in nodes else "")
                add_edge(mid, tgt, "REFERENCES")

    conn.executemany("INSERT OR REPLACE INTO nodes VALUES (?,?,?,?,?)",
                     list(nodes.values()))
    conn.executemany("INSERT OR IGNORE INTO edges VALUES (?,?,?)", edges)
    conn.commit()
    out = {"nodes": len(nodes), "edges": len({(a, b, c) for a, b, c in edges}),
           "unknown_relations": unknown_rel}
    if verbose:
        print(f"[kg] built {DB.relative_to(ROOT).as_posix()}: "
              f"{out['nodes']} nodes / {out['edges']} edges"
              + (f"（未知关系名 {unknown_rel} 条已归 REFERENCES）" if unknown_rel else ""))
    return out


def _need(conn: sqlite3.Connection) -> None:
    if not conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='nodes'"
                        ).fetchone():
        sys.exit("[kg] 图未构建，先跑：python tools/knowledge_graph.py build")


def stats(conn: sqlite3.Connection) -> dict:
    _need(conn)
    n = conn.execute("SELECT COUNT(*) FROM nodes").fetchone()[0]
    e = conn.execute("SELECT COUNT(*) FROM edges").fetchone()[0]
    by_type = dict(conn.execute("SELECT type, COUNT(*) FROM nodes GROUP BY type "
                                "ORDER BY COUNT(*) DESC").fetchall())
    by_edge = dict(conn.execute("SELECT type, COUNT(*) FROM edges GROUP BY type "
                                "ORDER BY COUNT(*) DESC").fetchall())
    dangling = [r[0] for r in conn.execute(
        "SELECT id FROM nodes WHERE status='dangling' ORDER BY id").fetchall()]
    # 「卡节点」= 人写的知识实体（原子/证据/误解）；FIXTURE/ARTIFACT/RULE 是基础设施节点，
    # 单列出来便于与"知识库规模"口径对照（否则总数会因工件/规则而虚高）。
    card_nodes = sum(v for k, v in by_type.items()
                     if k in ("ATOM", "EVIDENCE", "MISCONCEPTION"))
    return {"nodes": n, "edges": e, "card_nodes": card_nodes,
            "nodes_by_type": by_type, "edges_by_type": by_edge, "dangling": dangling}


def deps(conn: sqlite3.Connection, atom_id: str) -> dict:
    """直接依赖（出边中语义为"依赖/前置/特化"的四类）。"""
    _need(conn)
    rows = conn.execute(
        "SELECT dst, type FROM edges WHERE src=? AND type IN "
        "('PREREQUISITE','SPECIALIZES','REALIZES','EVOLVED_FROM') ORDER BY type, dst",
        (atom_id,)).fetchall()
    return {"atom": atom_id, "deps": [{"id": d, "type": t} for d, t in rows]}


def chain(conn: sqlite3.Connection, atom_id: str, max_depth: int = 8) -> dict:
    """完整依赖链（多跳，递归 CTE；带深度上限防环爆栈）。"""
    _need(conn)
    rows = conn.execute(
        """
        WITH RECURSIVE walk(id, depth) AS (
            SELECT ?, 0
            UNION
            SELECT e.dst, w.depth + 1 FROM edges e JOIN walk w ON e.src = w.id
             WHERE e.type IN ('PREREQUISITE','SPECIALIZES','REALIZES','EVOLVED_FROM')
               AND w.depth < ?
        )
        SELECT id, MIN(depth) AS d FROM walk WHERE depth > 0 GROUP BY id ORDER BY d, id
        """, (atom_id, max_depth)).fetchall()
    return {"atom": atom_id, "chain": [{"id": i, "depth": d} for i, d in rows]}


def impact(conn: sqlite3.Connection, target: str) -> dict:
    """上游影响：改 `target`（文件路径或节点 id）会波及哪些**原子**。

    路径 → 匹配 FIXTURE/ARTIFACT 节点的 path；再走 入边(EVIDENCE) → SERVES → ATOM。
    """
    _need(conn)
    ids = [r[0] for r in conn.execute(
        "SELECT id FROM nodes WHERE id=? OR path=?", (target, target)).fetchall()]
    if not ids:
        return {"target": target, "found": False, "atoms": []}
    atoms: set[str] = set()
    for nid in ids:
        for (ev,) in conn.execute("SELECT src FROM edges WHERE dst=?", (nid,)).fetchall():
            for (at,) in conn.execute(
                    "SELECT dst FROM edges WHERE src=? AND type='SERVES'", (ev,)).fetchall():
                atoms.add(at)
    return {"target": target, "found": True, "nodes": ids, "atoms": sorted(atoms)}


def orphans(conn: sqlite3.Connection) -> list[dict]:
    """孤立节点：既无入边也无出边（RULE 与 stub 天然如此，分类列出便于甄别）。"""
    _need(conn)
    rows = conn.execute(
        "SELECT id, type, status FROM nodes WHERE id NOT IN (SELECT src FROM edges) "
        "AND id NOT IN (SELECT dst FROM edges) ORDER BY type, id").fetchall()
    return [{"id": i, "type": t, "status": s} for i, t, s in rows]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="知识图谱 L1（508 任务5）")
    ap.add_argument("cmd", choices=("build", "stats", "deps", "impact", "chain", "orphans"))
    ap.add_argument("arg", nargs="?", default=None, help="deps/impact/chain 的目标")
    ap.add_argument("--db", default=None, help="覆盖数据库路径（测试用）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    conn = connect(Path(a.db) if a.db else None)
    if a.cmd == "build":
        out = build(conn)
    elif a.cmd == "stats":
        out = stats(conn)
    elif a.cmd == "orphans":
        o = orphans(conn)
        out = {"orphans": len(o), "items": o}
    elif a.cmd == "deps":
        out = deps(conn, a.arg or "")
    elif a.cmd == "chain":
        out = chain(conn, a.arg or "")
    else:
        out = impact(conn, a.arg or "")
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    elif a.cmd == "build":
        print(f"[kg] 建图完成：{out['nodes']} 节点 / {out['edges']} 边"
              + (f"（未知关系名 {out['unknown_relations']} 条已归 REFERENCES）"
                 if out.get("unknown_relations") else ""))
    elif a.cmd == "stats":
        print(f"[kg] 节点 {out['nodes']}（其中卡节点 {out['card_nodes']}）· 边 {out['edges']}")
        print("     节点分布：" + "、".join(f"{k}={v}" for k, v in out["nodes_by_type"].items()))
        print("     边分布：  " + "、".join(f"{k}={v}" for k, v in out["edges_by_type"].items())
              or "     （无边）")
        if out["dangling"]:
            print(f"     悬空目标 {len(out['dangling'])}：{', '.join(out['dangling'][:8])}")
    elif a.cmd == "orphans":
        print(f"[kg] 孤立节点 {out['orphans']}")
        for it in out["items"]:
            print(f"   {it['type']:<14} {it['id']}")
    elif a.cmd == "deps":
        print(f"[kg] {out['atom']} 直接依赖 {len(out['deps'])}：")
        for d in out["deps"]:
            print(f"   {d['type']:<14} {d['id']}")
    elif a.cmd == "chain":
        print(f"[kg] {out['atom']} 依赖链 {len(out['chain'])}（多跳）：")
        for c in out["chain"]:
            print(f"   depth={c['depth']}  {c['id']}")
    else:
        if not out.get("found"):
            print(f"[kg] 未找到节点：{out.get('target', a.arg)}（提示：先 build；"
                  "或用节点 id / 仓库相对路径）")
            return 1
        print(f"[kg] 改 {out['target']} 波及 {len(out['atoms'])} 颗原子：")
        for at in out["atoms"]:
            print(f"   {at}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
