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
# mypy: ignore-errors
# 存量工具：类型注解债务，CI 先转绿，后续逐步修
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

from path_config_625 import root as _queyi_root  # noqa: E402  (625 C1 路径解耦)

ROOT = _queyi_root()
sys.path.insert(0, str(Path(__file__).resolve().parent))

import atom_evidence_replay as replay  # noqa: E402
import gate_engine as ge  # noqa: E402
import impact_analysis as imp  # noqa: E402

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
-- 526 批次E：概念层（命题级）。与 nodes/edges 分开存是刻意的——
--   nodes 的 id 是"身份"（ATOM-/EV-/RULE- 等），带 path/status；概念名是自然语言短语
--   （如"内存屏障(fence)"），没有 path/status。混进 nodes 会让 orphans 把概念全判成孤立，
--   也会污染 deps/impact 的遍历语义。概念层只服务"哪些命题在谈什么"这类问题。
CREATE TABLE IF NOT EXISTS concepts (
    name TEXT PRIMARY KEY,
    props INTEGER NOT NULL DEFAULT 0,      -- 出现的命题条数
    as_subject INTEGER NOT NULL DEFAULT 0,
    as_object INTEGER NOT NULL DEFAULT 0,
    atoms TEXT NOT NULL DEFAULT ''         -- 涉及原子 id（逗号分隔，供人眼速览）
);
CREATE TABLE IF NOT EXISTS concept_edges (
    src TEXT NOT NULL,                     -- subject 概念
    dst TEXT NOT NULL,                     -- object 概念
    atom TEXT NOT NULL,                    -- 命题所在原子（必须能回溯到卡）
    prop TEXT NOT NULL,                    -- 命题 id（prop-1…）
    predicate TEXT,
    claim_type TEXT,
    statement TEXT,
    PRIMARY KEY (src, dst, atom, prop),
    FOREIGN KEY (atom) REFERENCES nodes(id)
);
CREATE INDEX IF NOT EXISTS idx_ce_src ON concept_edges(src);
CREATE INDEX IF NOT EXISTS idx_ce_dst ON concept_edges(dst);
CREATE INDEX IF NOT EXISTS idx_ce_atom ON concept_edges(atom);
"""

# 关系名 → 边类型（大小写/同义词归一）。表外取值归 REFERENCES 并在 build 时计数留痕
# （472 P1-4：结束同义词枚举，未知不静默——但图谱是**分析**工具，不该因未知类型而中断，
# 故这里是"归入 REFERENCES + 计数"，与 gate 的 ATOM-REL-UNKNOWN 各司其职）。
REL_MAP = {
    "prerequisite": "PREREQUISITE", "requires": "PREREQUISITE",
    "specializes": "SPECIALIZES", "subtype": "SPECIALIZES",
    "realizes": "REALIZES", "implements": "REALIZES",
    "evolved_from": "EVOLVED_FROM", "successor_of": "EVOLVED_FROM",
    # 530 任务3：contrasts（对照）与 contradicts（矛盾）拆成两类边。
    #   CONTRASTS = 对照（同一主题的不同写法/取舍，非逻辑矛盾，只进浏览清单不报警）；
    #   CONTRADICTS = 矛盾/推翻（refutes/misconceived_as 仍归此，进冲突候选）。
    "contrasts": "CONTRASTS", "contradicts": "CONTRADICTS",
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


CONCEPT_ALIASES = ROOT / "tools" / "concept_aliases.txt"


def load_concept_aliases(path: Path | None = None) -> dict[str, str]:
    """读概念别名表 → {别名(归一化键) : 规范名}。

    格式：`规范名 <- 别名1, 别名2`；`#` 注释；空行忽略。缺文件返回 {}（不报错——
    别名表是**可选**增强，没它图谱照常建，只是不做归一）。
    """
    p = path or CONCEPT_ALIASES
    try:
        lines = p.read_text(encoding="utf-8").splitlines()
    except OSError:
        return {}
    out: dict[str, str] = {}
    for ln in lines:
        body = ln.split("#")[0].strip()
        if not body or "<-" not in body:
            continue
        canon, _, aliases = body.partition("<-")
        canon = canon.strip()
        if not canon:
            continue
        for a in aliases.split(","):
            key = a.strip()
            if key:
                out[_alias_key(key)] = canon
    return out


def _alias_key(name: str) -> str:
    """别名匹配键：去首尾空白 + casefold（中文无影响，英文大小写不敏感）。

    **只用于整串匹配**：子串改写会制造胡说（`锁` 是 `自旋锁` 的子串，
    `fence` 嵌在 `atomic_signal_fence` 里）——概念名是命题级短语，只该整串认。
    """
    return name.strip().casefold()


def _canon_concept(name: str, aliases: dict[str, str]) -> tuple[str, bool]:
    """概念名归一：命中别名 → 规范名。返回 (名称, 是否发生改写)。

    未命中也要 `strip()`：概念名是**键**，带首尾空白会分裂成两个节点
    （`" 栅栏 "` 与 `"栅栏"` 不是同一概念）——调用点虽已 strip，但这是单点职责，
    不能靠调用方记得。
    """
    name = name.strip()
    canon = aliases.get(_alias_key(name))
    if canon and canon != name:
        return canon, True
    return name, False


def build(conn: sqlite3.Connection, *, verbose: bool = True) -> dict:
    """重建图（幂等）：DROP → 建表 → 扫卡 → 插节点/边。返回统计。"""
    conn.executescript("DROP TABLE IF EXISTS edges; DROP TABLE IF EXISTS nodes;"
                       "DROP TABLE IF EXISTS concept_edges;"
                       "DROP TABLE IF EXISTS concepts;")
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

    # ── 概念层（526 批次E）：命题级 subject→object ──────────────────────────
    # 只有**带 claim_structured 的原子**才进概念层。缺字段的卡不是"错"，而是"还没拆"
    # （gate 的 ATOM-CLAIM-STRUCTURED 在 warn 它们）——图谱不该替门禁判合规，
    # 只如实反映"目前有多少命题可推理"。
    concepts: dict[str, list[int | set]] = {}   # name -> [props, as_subj, as_obj, atoms]
    cedges: list[tuple] = []
    aliases = load_concept_aliases()            # 527：概念名归一（Book/ 口语 → 规范名）
    alias_hits = 0
    for p in ge._cards(ge.ATOMS, "ATOM-*.md"):
        m = _meta(p)
        aid = str(m.get("id") or p.stem)
        for pr in ge._claim_props(m):
            subj = str(pr.get("subject") or "").strip()
            obj = str(pr.get("object") or "").strip()
            if not subj or not obj:
                continue                        # 三元组不完整 ⇒ 不进概念层（gate 已单独判）
            # 命题里若写了别名（如 Book/ 口语"栅栏"），先归一到规范名再入图——
            # 否则同一概念会分裂成两个节点，矛盾检测/覆盖度统计全乱。
            subj, hit_s = _canon_concept(subj, aliases)
            obj, hit_o = _canon_concept(obj, aliases)
            alias_hits += int(hit_s) + int(hit_o)
            pid = str(pr.get("id") or f"prop-{len(cedges) + 1}")
            for name, is_subj in ((subj, True), (obj, False)):
                slot = concepts.setdefault(name, [0, 0, 0, set()])
                slot[0] += 1
                slot[1 if is_subj else 2] += 1
                slot[3].add(aid)
            cedges.append((subj, obj, aid, pid,
                           str(pr.get("predicate") or "").strip(),
                           str(pr.get("claim_type") or "").strip(),
                           str(pr.get("statement") or "").strip()))
    conn.executemany("INSERT OR REPLACE INTO concepts VALUES (?,?,?,?,?)",
                     [(n, v[0], v[1], v[2], ",".join(sorted(v[3])))
                      for n, v in concepts.items()])
    conn.executemany("INSERT OR REPLACE INTO concept_edges VALUES (?,?,?,?,?,?,?)",
                     cedges)
    conn.commit()
    out = {"nodes": len(nodes), "edges": len({(a, b, c) for a, b, c in edges}),
           "unknown_relations": unknown_rel,
           "concepts": len(concepts), "concept_edges": len(cedges),
           "aliases": len(aliases), "alias_hits": alias_hits}
    if verbose:
        print(f"[kg] built {DB.relative_to(ROOT).as_posix()}: "
              f"{out['nodes']} nodes / {out['edges']} edges"
              f" · 概念 {out['concepts']} / 命题边 {out['concept_edges']}"
              + (f"（未知关系名 {unknown_rel} 条已归 REFERENCES）" if unknown_rel else "")
              + (f"｜别名归一 {alias_hits} 处（表 {len(aliases)} 条）"
                 if aliases else "｜无别名表"))
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
    # 526：概念层规模（表可能尚不存在——旧库未重建时不报错，返回 0）
    try:
        cn = conn.execute("SELECT COUNT(*) FROM concepts").fetchone()[0]
        ce = conn.execute("SELECT COUNT(*) FROM concept_edges").fetchone()[0]
        # 530 任务3：跨原子概念数（出现在 ≥2 颗原子的概念）；首跑预期≈0。
        # concepts.atoms 是逗号分隔的原子 id。
        cma = 0
        for (atoms_csv,) in conn.execute("SELECT atoms FROM concepts WHERE atoms <> ''"):
            if len([x for x in atoms_csv.split(",") if x]) >= 2:
                cma += 1
        # 最大连通分量（概念节点经 concept_edges 无向连通，union-find）。
        comp = -1
        rows_ce = conn.execute("SELECT src, dst FROM concept_edges").fetchall()
        parent: dict[str, str] = {}
        if rows_ce:
            def _find(x: str) -> str:
                parent.setdefault(x, x)
                while parent[x] != x:
                    parent[x] = parent[parent[x]]
                    x = parent[x]
                return x

            def _union(a: str, b: str) -> None:
                ra, rb = _find(a), _find(b)
                if ra != rb:
                    parent[ra] = rb
            for s, d in rows_ce:
                _union(s, d)
            sizes: dict[str, int] = {}
            for node in parent:
                sizes[_find(node)] = sizes.get(_find(node), 0) + 1
            comp = max(sizes.values()) if sizes else -1
    except sqlite3.OperationalError:
        cn = ce = cma = 0
        comp = -1
    return {"nodes": n, "edges": e, "card_nodes": card_nodes,
            "concepts": cn, "concept_edges": ce, "concepts_multi_atom": cma,
            "max_component": comp,
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


def concepts(conn: sqlite3.Connection, name: str | None = None) -> dict:
    """概念查询（526 批次E）：无参 → 概念清单；带名 → **该概念出现在哪些命题**。

    概念来自命题的 subject/object（只有带 `claim_structured` 的原子会进概念层）。
    返回的每条命题都带 `atom`——**概念不能脱离卡存在**，任何命题结论都要能回到原子卡
    找它的证据与命题类型（observation/inference），这是本图谱不做"纯概念库"的底线。
    """
    _need(conn)
    try:
        if name:
            # 527：查询也走别名（`concepts 栅栏` 应命中规范名「内存屏障(fence)」）——
            # 526 的原始痛点正是"用户按口语查，图谱按规范名存，于是查不到"。
            canon, aliased = _canon_concept(name, load_concept_aliases())
            rows = conn.execute(
                "SELECT src, dst, atom, prop, predicate, claim_type, statement "
                "FROM concept_edges WHERE src = ? OR dst = ? "
                "ORDER BY atom, prop", (canon, canon)).fetchall()
            props = [{"subject": s, "predicate": p, "object": d, "atom": a,
                      "prop": pid, "claim_type": ct, "statement": st}
                     for s, d, a, pid, p, ct, st in rows]
            kinds: dict[str, int] = {}
            for it in props:
                kinds[it["claim_type"]] = kinds.get(it["claim_type"], 0) + 1
            info = conn.execute("SELECT props, as_subject, as_object, atoms "
                                "FROM concepts WHERE name = ?", (canon,)).fetchone()
            return {"concept": canon, "query": name, "aliased": aliased,
                    "found": info is not None,
                    "props": len(props), "claim_types": kinds,
                    "atoms": (info[3].split(",") if info else []),
                    "items": props}
        rows = conn.execute("SELECT name, props, as_subject, as_object, atoms "
                            "FROM concepts ORDER BY props DESC, name").fetchall()
        return {"concepts": len(rows),
                "items": [{"name": n, "props": p, "as_subject": s, "as_object": o,
                           "atoms": a.split(",") if a else []}
                          for n, p, s, o, a in rows]}
    except sqlite3.OperationalError:
        sys.exit("[kg] 概念层不存在，先重跑：python tools/knowledge_graph.py build")


# ── 528 任务2：概念冲突候选（L1 结构检测，**不判对错**）──────────────────────
# 语义上"两条命题是否真矛盾"是人的判断（或红队/LLM 的事）。本工具只做**结构候选**：
#   ① 同一 subject 下两条命题的 object 极性相反（显式反义词对，非模糊子串）；
#   ② 两条命题所在原子之间存在 CONTRADICTS 边（卡面 relations 已声明的矛盾）。
# 输出里带上"命中的词"，让人一眼看出为什么被列为候选——候选≠结论。
_POLARITY = (
    (("阻止", "禁止", "不提供", "不会", "不能", "不可", "不保证", "未定义", "不建立"),
     ("允许", "提供", "会", "能", "可", "保证", "定义", "建立")),
)


def _polarity_hit(a: str, b: str) -> tuple[str, str] | None:
    """两条 object 的极性是否相反（返回 (a 侧命中词, b 侧命中词)，否则 None）。"""
    for neg, pos in _POLARITY:
        na = next((w for w in neg if w in a), None)
        pb = next((w for w in pos if w in b), None)
        if na and pb and a != b:
            return (na, pb)
        nb = next((w for w in neg if w in b), None)
        pa = next((w for w in pos if w in a), None)
        if nb and pa and a != b:
            return (pa, nb)
    return None


def conflicts(conn: sqlite3.Connection) -> dict:
    """候选矛盾命题对（**只报候选**，不做语义裁决，也不进门禁）。

    530 任务3：CONTRADICTS（矛盾/推翻）边进冲突候选；CONTRASTS（对照）边只进
    `contrast_pairs` 浏览清单、不报警（对照≠矛盾，误报噪声大，交人眼速览）。
    """
    _need(conn)
    try:
        rows = conn.execute(
            "SELECT src, dst, atom, prop, predicate, claim_type, statement "
            "FROM concept_edges ORDER BY src, atom, prop").fetchall()
        contra = {(a, b) for a, b, t in conn.execute(
            "SELECT src, dst, type FROM edges WHERE type='CONTRADICTS'").fetchall()}
        contrast_pairs = {(a, b) for a, b, t in conn.execute(
            "SELECT src, dst, type FROM edges WHERE type='CONTRASTS'").fetchall()}
    except sqlite3.OperationalError:
        sys.exit("[kg] 概念层不存在，先跑：python tools/knowledge_graph.py build")

    def _d(r) -> dict:
        return {"subject": r[0], "object": r[1], "atom": r[2], "prop": r[3],
                "predicate": r[4], "claim_type": r[5], "statement": r[6]}

    by_atom: dict[str, list[dict]] = {}
    for r in rows:
        by_atom.setdefault(r[2], []).append(_d(r))
    atoms = sorted(by_atom)
    out: list[dict] = []
    browse: list[dict] = []
    for i, a1 in enumerate(atoms):
        for a2 in atoms[i + 1:]:
            # ① 同 subject 且 object 极性相反（**精确**信号，逐命题对给出）
            pol: list[dict] = []
            for pa in by_atom[a1]:
                for pb in by_atom[a2]:
                    if pa["subject"] != pb["subject"]:
                        continue
                    hit = _polarity_hit(pa["object"], pb["object"])
                    if hit:
                        pol.append({"tokens": list(hit), "a": pa, "b": pb})
            # ② 两原子间存在 CONTRADICTS 边（逻辑矛盾声明，须人工裁决）
            if (a1, a2) in contra or (a2, a1) in contra:
                out.append({"kind": "contradiction_edge",
                            "reason": "两原子之间存在 CONTRADICTS 边（矛盾/推翻声明，须人工裁决）",
                            "a_atom": a1, "b_atom": a2,
                            "a_props": by_atom[a1], "b_props": by_atom[a2],
                            "polarity_pairs": pol})
            # ②' 两原子间仅存在 CONTRASTS 边（对照，非矛盾）→ 只进浏览清单，不报警
            elif (a1, a2) in contrast_pairs or (a2, a1) in contrast_pairs:
                browse.append({"a_atom": a1, "b_atom": a2,
                               "a_props": by_atom[a1], "b_props": by_atom[a2]})
            elif pol:
                out.append({"kind": "polarity",
                            "reason": "同 subject 且 object 极性相反",
                            "a_atom": a1, "b_atom": a2,
                            "a_props": by_atom[a1], "b_props": by_atom[a2],
                            "polarity_pairs": pol})
    return {"candidates": len(out), "contrast_pairs": len(browse),
            "items": out, "browse": browse}


def concept_islands(conn: sqlite3.Connection) -> dict:
    """只出现在 1 颗原子里的概念（回填/合并 backlog），只读、不修改任何文件。

    530 任务3：让"标签袋"变"图"后的清理入口——这些概念无法跨原子连通，是孤岛。
    """
    _need(conn)
    rows = conn.execute("SELECT name, atoms FROM concepts WHERE atoms <> ''").fetchall()
    islands = [r[0] for r in rows if len([x for x in r[1].split(",") if x]) == 1]
    islands.sort()
    return {"islands": len(islands), "items": islands}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="知识图谱 L1（508 任务5 + 526 概念层）")
    ap.add_argument("cmd", choices=("build", "stats", "deps", "impact", "chain", "orphans",
                                    "concepts", "conflicts", "concept-islands"))
    ap.add_argument("arg", nargs="?", default=None,
                    help="deps/impact/chain 的目标；concepts 的概念名（省略=列全部）")
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
    elif a.cmd == "concepts":
        out = concepts(conn, a.arg)
    elif a.cmd == "conflicts":
        out = conflicts(conn)
    elif a.cmd == "concept-islands":
        out = concept_islands(conn)
    else:
        out = impact(conn, a.arg or "")
    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=2))
    elif a.cmd == "build":
        print(f"[kg] 建图完成：{out['nodes']} 节点 / {out['edges']} 边"
              + (f"（未知关系名 {out['unknown_relations']} 条已归 REFERENCES）"
                 if out.get("unknown_relations") else ""))
    elif a.cmd == "stats":
        print(f"[kg] 节点 {out['nodes']}（其中卡节点 {out['card_nodes']}）· 边 {out['edges']}"
              f" · 概念 {out.get('concepts', 0)} / 命题边 {out.get('concept_edges', 0)}")
        print("     节点分布：" + "、".join(f"{k}={v}" for k, v in out["nodes_by_type"].items()))
        print("     边分布：  " + "、".join(f"{k}={v}" for k, v in out["edges_by_type"].items())
              or "     （无边）")
        print(f"     概念连通：跨原子概念 {out.get('concepts_multi_atom', 0)} / "
              f"最大连通分量 {out.get('max_component', -1)}")
        if out["dangling"]:
            print(f"     悬空目标 {len(out['dangling'])}：{', '.join(out['dangling'][:8])}")
    elif a.cmd == "orphans":
        print(f"[kg] 孤立节点 {out['orphans']}")
        for it in out["items"]:
            print(f"   {it['type']:<14} {it['id']}")
    elif a.cmd == "concepts":
        if out.get("concept") and not out.get("found"):
            print(f"[kg] 概念库里没有「{out['concept']}」"
                  "（先 build；概念名须与卡上 subject/object 逐字一致）")
            return 1
        if out.get("concept"):
            print(f"[kg] 概念「{out['concept']}」出现在 {out['props']} 条命题"
                  f"（{out['claim_types'] or '—'}）涉及原子 {','.join(out['atoms'])}："
                  + (f"　[别名解析：{out['query']} → {out['concept']}]"
                     if out.get("aliased") else ""))
            for it in out["items"]:
                print(f"   [{it['claim_type'] or '?':<11}] {it['atom']}:{it['prop']}  "
                      f"{it['subject']} —{it['predicate']}→ {it['object']}")
        else:
            print(f"[kg] 概念 {out['concepts']} 个（按命题数降序）：")
            for it in out["items"]:
                print(f"   {it['props']:>3} 条  {it['name']}"
                      f"（主 {it['as_subject']} / 宾 {it['as_object']}）"
                      f"  原子 {','.join(it['atoms'])}")
    elif a.cmd == "conflicts":
        print(f"[kg] 候选矛盾 {out['candidates']} 组（**只报候选，语义裁决归人/红队**）：")
        if out.get("contrast_pairs"):
            print(f"   （另 {out['contrast_pairs']} 组 CONTRASTS 对照对仅入浏览清单、不报警）")
        for it in out["items"]:
            print(f"   — {it['a_atom']} × {it['b_atom']}：{it['reason']}")
            for pr in it["polarity_pairs"]:
                print(f"       命中词 {pr['tokens']}：{pr['a']['prop']}「{pr['a']['object'][:40]}」"
                      f" ↔ {pr['b']['prop']}「{pr['b']['object'][:40]}」")
            if not it["polarity_pairs"]:
                print("       （无极性相反对，仅凭声明的 CONTRADICTS 边 → 矛盾须人工裁决）")
    elif a.cmd == "concept-islands":
        print(f"[kg] 概念孤岛 {out['islands']} 个（只出现在 1 颗原子，回填/合并 backlog）：")
        for name in out["items"][:60]:
            print(f"   · {name}")
        if out["islands"] > 60:
            print(f"   …（其余 {out['islands'] - 60} 个省略）")
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
