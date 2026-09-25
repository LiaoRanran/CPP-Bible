#!/usr/bin/env python3
"""565 Part 3 · 命题状态图（**只读派生视图**）：把卡里的 `claim_structured` 落成可查询库。

为什么不塞进 knowledge_graph.db：**命题 ≠ 概念**（525"标签袋不是概念图"的教训）。命题是"卡声明的
一句话 + 它的机验/签署状态"，概念是跨卡归一后的词表；混表会让两边都不再可信。故本工具用**独立库**
`data/propositions.db`（与 `data/knowledge_graph.db` 分离，绝不碰 concepts 表）。

只读纪律（本批冻结项）：
  * **绝不改卡**、**绝不自动入库新命题**（自动入库仍在冻结期）——只抽卡里已经写好的
    `claim_structured`；抽完 `git status` 必须零差异（`tests/test_prop_graph.py` 锁这条）。
  * 库是**派生视图**（可随时 `build` 重建）⇒ 与 knowledge_graph.db 同口径进 .gitignore。

状态标注（当前实测底座，不许假装）：
  * 命题级 `signed_by`：**当前 0 条**；
  * 卡级人签 = 卡的 `verified_by` 非空（26 张卡有）；
  * `machine_verified`：所属卡**或**其任一 evidence 卡有机器锚点（`artifact` / `actual.run_*` /
    `kind ∈ {asm, run}`）——atom 卡本身无锚点，靠 evidence 卡带锚。

用法：
  python tools/prop_graph.py build [--db data/propositions.db]
  python tools/prop_graph.py stats [--json]
  python tools/prop_graph.py query [--id P] [--card C] [--type observation|inference]
                                   [--machine yes|no] [--sign prop_signed|card_signed|unsigned]
                                   [--json]
"""
# mypy: ignore-errors
# 存量工具：类型注解债务，CI 先转绿，后续逐步修
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any

from path_config_625 import root as _queyi_root  # noqa: E402  (625 C1 路径解耦)

ROOT = _queyi_root()
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_engine as ge  # noqa: E402

VERSION = "v1.1"
DEFAULT_DB = ROOT / "data" / "propositions.db"

# 566 任务 0（监工验收抓出的真 bug）：**schema 版本化 + 自愈**。
#   病：565b 给 props 加了 `anchor_source` 列，但已存在的旧库（15 列）不会被自动升级 ⇒
#       直接跑 `stats` / `query` 会崩 `sqlite3.OperationalError: no such column`（监工踩到，
#       手动跑一次 build 才恢复）。根因是**读路径不校验 schema**、且 build 的自愈不可见。
#   治（按监工处方选更简单的一条）：① 记 `schema_version` 到 meta；② build 开头先体检，
#       版本不符或缺列就**整库重建**（命题图是**纯派生视图**，重建无损 ⇒ 不做 ALTER 迁移）；
#       ③ 读路径（stats/query）先校验，不兼容就 fail-loud 并**直接给出重建命令**，
#       绝不把裸 OperationalError 抛给用户。
SCHEMA_VERSION = "2"          # 1 = 首版（无 anchor_source）；2 = +anchor_source（565b 加列）
PROPS_COLUMNS = ("prop_key", "card", "card_path", "card_kind", "prop_id", "claim_type",
                 "subject", "predicate", "object", "statement", "extracted_by", "signed_by",
                 "evidence", "machine_verified", "anchor_source", "signoff_state")


def schema_state(db: Path | str) -> tuple[str, list[str]]:
    """体检：(库内 schema_version, props 表**缺失的列**)。库/表不存在 ⇒ `("missing", [])`。

    旧库没有 `schema_version` 键（首版没写）⇒ 记作 `"1"`，正好与当前 `"2"` 不符 ⇒ 触发重建。
    """
    p = Path(db)
    if not p.is_file():
        return "missing", []
    conn = sqlite3.connect(str(p))
    try:
        cols = {r[1] for r in conn.execute("PRAGMA table_info(props)")}
        if not cols:
            return "missing", []
        try:
            row = conn.execute("SELECT value FROM meta WHERE key='schema_version'").fetchone()
            ver = str(row[0]) if row else "1"          # 无该键 = 首版库
        except sqlite3.Error:
            ver = "1"
        return ver, sorted(set(PROPS_COLUMNS) - cols)
    finally:
        conn.close()


def _needs_rebuild(db: Path | str) -> tuple[bool, str]:
    """是否需要整库重建 + 一句人读理由（build 打印用，让"自愈"这件事**可见**）。"""
    ver, missing = schema_state(db)
    if ver == "missing":
        return False, "库不存在或表缺失（首次构建）"
    if ver != SCHEMA_VERSION:
        return True, f"schema_version {ver} ≠ 当前 {SCHEMA_VERSION}"
    if missing:
        return True, f"props 表缺列 {missing}"
    return False, "schema 已是最新"

SCHEMA = """
CREATE TABLE meta(key TEXT PRIMARY KEY, value TEXT NOT NULL);
CREATE TABLE props(
  prop_key         TEXT PRIMARY KEY,   -- "<卡id>/<prop-id>"（prop-1 卡内唯一，跨卡会重名）
  card             TEXT NOT NULL,      -- 卡 id
  card_path        TEXT NOT NULL,      -- 相对仓根路径
  card_kind        TEXT NOT NULL,      -- atom | evidence
  prop_id          TEXT NOT NULL,
  claim_type       TEXT NOT NULL,      -- observation | inference
  subject          TEXT NOT NULL DEFAULT '',
  predicate        TEXT NOT NULL DEFAULT '',
  object           TEXT NOT NULL DEFAULT '',
  statement        TEXT NOT NULL DEFAULT '',
  extracted_by     TEXT NOT NULL DEFAULT '',
  signed_by        TEXT NOT NULL DEFAULT '',
  evidence         TEXT NOT NULL DEFAULT '',   -- 原样（逗号分隔），便于人读
  machine_verified INTEGER NOT NULL,           -- 0/1（有机器锚点）
  anchor_source    TEXT NOT NULL,              -- card（本卡自带）/ evidence（靠证据卡）/ none
  signoff_state    TEXT NOT NULL               -- prop_signed|card_signed|unsigned
);
CREATE TABLE prop_evidence(
  prop_key   TEXT NOT NULL,
  evidence_id TEXT NOT NULL,
  PRIMARY KEY(prop_key, evidence_id)
);
"""


def _as_list(v: Any) -> list[str]:
    if isinstance(v, list):
        return [str(x) for x in v if str(x).strip()]
    if isinstance(v, str):
        return [x.strip() for x in v.replace(",", " ").split() if x.strip()]
    return []


def _machine_anchors() -> dict[str, bool]:
    """每张卡是否有**机器锚点**（artifact / actual.run_* / kind ∈ {asm, run}）。"""
    out: dict[str, bool] = {}
    for pat, root in (("ATOM-*.md", ge.ATOMS), ("EV-*.md", ge.EVIDENCE)):
        for p in sorted(root.rglob(pat)):
            if "README" in p.name:
                continue
            m = ge._meta(p)
            cid = str(m.get("id") or p.stem)
            actual = m.get("actual") or {}
            run_keys = [k for k in actual if str(k).startswith("run")] \
                if isinstance(actual, dict) else []
            out[cid] = bool(str(m.get("artifact") or "")) or bool(run_keys) \
                or str(m.get("kind") or "") in ("asm", "run")
    return out


def extract() -> list[dict[str, Any]]:
    """只读抽取：27 张卡的 `claim_structured` → 命题行（排序确定，便于幂等对账）。"""
    anchors = _machine_anchors()
    signed_cards: dict[str, str] = {}
    rows: list[dict[str, Any]] = []
    for pat, root, kind in (("ATOM-*.md", ge.ATOMS, "atom"), ("EV-*.md", ge.EVIDENCE, "evidence")):
        for p in sorted(root.rglob(pat)):
            if "README" in p.name:
                continue
            m = ge._meta(p)
            cid = str(m.get("id") or p.stem)
            signed_cards[cid] = str(m.get("verified_by") or "")
            cs = m.get("claim_structured")
            if not cs:
                continue
            for it in cs:
                if not isinstance(it, dict):
                    continue
                pid = str(it.get("id") or "?")
                ev = _as_list(it.get("evidence"))
                # 有锚要分清"本卡自带"还是"靠证据卡"：atom 卡本身无锚（实测 27 张全无），
                # 它的命题只能靠 evidence 卡带锚 —— 混成一列会让"机验"看起来比实际更强
                if anchors.get(cid):
                    src = "card"
                elif any(anchors.get(e) for e in ev):
                    src = "evidence"
                else:
                    src = "none"
                has_anchor = src != "none"
                sig = str(it.get("signed_by") or "")
                if sig:
                    state = "prop_signed"
                elif signed_cards.get(cid):
                    state = "card_signed"
                else:
                    state = "unsigned"
                rows.append({
                    "prop_key": f"{cid}/{pid}", "card": cid,
                    "card_path": p.relative_to(ROOT).as_posix(), "card_kind": kind,
                    "prop_id": pid, "claim_type": str(it.get("claim_type") or ""),
                    "subject": str(it.get("subject") or ""),
                    "predicate": str(it.get("predicate") or ""),
                    "object": str(it.get("object") or ""),
                    "statement": str(it.get("statement") or ""),
                    "extracted_by": str(it.get("extracted_by") or ""),
                    "signed_by": sig, "evidence": ", ".join(ev),
                    "machine_verified": 1 if has_anchor else 0,
                    "anchor_source": src,
                    "signoff_state": state, "_ev": ev,
                })
    rows.sort(key=lambda r: (r["card"], r["prop_id"]))
    return rows


def build(db_path: Path | str | None = None) -> Path:
    """重建库（**幂等**：同输入 ⇒ 同内容；表全 DROP 重建，不存任何时间戳）。

    566 任务 0：对**旧 schema 的库也自愈**——开头先体检，版本不符或缺列就整库重建
    （纯派生视图 ⇒ 丢历史无损，不做 ALTER 迁移），并把"为什么重建"打出来（自愈要可见）。
    """
    db = Path(db_path) if db_path else DEFAULT_DB
    db.parent.mkdir(parents=True, exist_ok=True)
    stale, why = _needs_rebuild(db)
    if stale:
        print(f"[prop] 旧 schema 自愈：{why} ⇒ 整库重建（纯派生视图，重建无损）")
    rows = extract()
    conn = sqlite3.connect(str(db))
    try:
        for t in ("meta", "props", "prop_evidence"):
            conn.execute(f"DROP TABLE IF EXISTS {t}")
        conn.executescript(SCHEMA)
        conn.executemany(
            "INSERT INTO meta(key,value) VALUES(?,?)",
            [("schema", "1"), ("schema_version", SCHEMA_VERSION),
             ("tool", "prop_graph.py"), ("version", VERSION),
             ("source", "cards.claim_structured（只读抽取；不自动入库新命题）")])
        for r in rows:
            conn.execute(
                "INSERT INTO props(prop_key,card,card_path,card_kind,prop_id,claim_type,"
                "subject,predicate,object,statement,extracted_by,signed_by,evidence,"
                "machine_verified,anchor_source,signoff_state) "
                "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (r["prop_key"], r["card"], r["card_path"], r["card_kind"], r["prop_id"],
                 r["claim_type"], r["subject"], r["predicate"], r["object"], r["statement"],
                 r["extracted_by"], r["signed_by"], r["evidence"],
                 r["machine_verified"], r["anchor_source"], r["signoff_state"]))
            for e in r["_ev"]:
                conn.execute("INSERT OR IGNORE INTO prop_evidence(prop_key,evidence_id) "
                             "VALUES(?,?)", (r["prop_key"], e))
        conn.commit()
    finally:
        conn.close()
    return db


def _connect(db: Path | str) -> sqlite3.Connection:
    """打开库并**先校验 schema**（566 任务 0）：不兼容 ⇒ fail-loud + 给出重建命令，
    绝不把裸 `OperationalError: no such column` 抛给用户（那正是监工踩到的形态）。"""
    p = Path(db)
    if not p.is_file():
        raise SystemExit(f"[prop] 库不存在：{p}（先跑 `prop_graph.py build`）")
    ver, missing = schema_state(p)
    if ver != SCHEMA_VERSION or missing:
        raise SystemExit(
            f"[prop] 库 schema 不兼容（schema_version={ver}，缺列 {missing or '无'}）\n"
            f"[prop] 修法：`.venv\\Scripts\\python.exe tools/prop_graph.py build`"
            "（命题图是纯派生视图，整库重建无损）")
    conn = sqlite3.connect(str(p))
    conn.row_factory = sqlite3.Row
    return conn


def query(db: Path | str = DEFAULT_DB, *, prop_id: str | None = None,
          card: str | None = None, ctype: str | None = None,
          machine: bool | None = None, sign: str | None = None) -> list[dict[str, Any]]:
    """按 id / 卡 / claim_type / 机验状态 / 签署状态检索（全条件为 AND；空 = 全量）。"""
    sql = "SELECT * FROM props"
    where: list[str] = []
    args: list[Any] = []
    if prop_id:
        where.append("(prop_key=? OR prop_id=?)")
        args += [prop_id, prop_id]
    if card:
        where.append("card=?")
        args.append(card)
    if ctype:
        where.append("claim_type=?")
        args.append(ctype)
    if machine is not None:
        where.append("machine_verified=?")
        args.append(1 if machine else 0)
    if sign:
        where.append("signoff_state=?")
        args.append(sign)
    if where:
        sql += " WHERE " + " AND ".join(where)
    sql += " ORDER BY card, prop_id"
    conn = _connect(db)
    try:
        return [dict(r) for r in conn.execute(sql, args).fetchall()]
    finally:
        conn.close()


def stats(db: Path | str = DEFAULT_DB) -> dict[str, Any]:
    """总量与分布（总数 / 按 claim_type / 按签署状态 / 机验数）。"""
    conn = _connect(db)
    try:
        total = conn.execute("SELECT COUNT(*) FROM props").fetchone()[0]
        by_type = {r[0]: r[1] for r in conn.execute(
            "SELECT claim_type, COUNT(*) FROM props GROUP BY claim_type ORDER BY claim_type")}
        by_sign = {r[0]: r[1] for r in conn.execute(
            "SELECT signoff_state, COUNT(*) FROM props GROUP BY signoff_state "
            "ORDER BY signoff_state")}
        mv = conn.execute("SELECT COUNT(*) FROM props WHERE machine_verified=1").fetchone()[0]
        by_anchor = {r[0]: r[1] for r in conn.execute(
            "SELECT anchor_source, COUNT(*) FROM props GROUP BY anchor_source "
            "ORDER BY anchor_source")}
        cards = conn.execute("SELECT COUNT(DISTINCT card) FROM props").fetchone()[0]
    finally:
        conn.close()
    return {"tool": "prop_graph", "version": VERSION, "propositions": total,
            "cards": cards, "by_claim_type": by_type, "by_signoff": by_sign,
            "machine_verified": mv, "by_anchor_source": by_anchor,
            "machine_verified_note":
            "有机器锚点 ≠ 已人签；两者独立（当前命题级 signed_by 0 条，签署靠卡级 verified_by 兜底）。"
            "anchor_source 区分「本卡自带」与「靠证据卡」——atom 卡实测全无锚点"}


# ── 566 任务 1：人审交接视图（pending / backlog）──────────────────────────────
def pending_signoff(db: Path | str = DEFAULT_DB) -> list[dict[str, Any]]:
    """**未人签**的命题（`signoff_state='unsigned'`）= 命题级 `signed_by` 与卡级
    `verified_by` **都没有**的那些（当前实测 3 条，即三张红队卡的解释性论断）。

    口径不与 `card_signed` 混：卡级人签（`verified_by`）算 `card_signed`，
    **不进**本视图——本视图只列"一个签名都没有"的命题。
    """
    return query(db, sign="unsigned")


BACKLOG_WHY = ("卡面无 claim_structured 字段：命题回填属**人审/写作工序**，"
               "本工具只列清单、不自动回填、不改卡（自动入库仍在冻结期）")


def backlog(db: Path | str = DEFAULT_DB) -> tuple[list[dict[str, Any]], int]:
    """还没写 `claim_structured` 命题的**原子卡**清单：返回 (清单, 原子卡总数)。

    只读卡面 + 库里的卡集合做差（不依赖库时退化为直接读卡），**绝不**自动回填。
    """
    db_cards: set[str] = set()
    try:
        db_cards = {r["card"] for r in query(db)}
    except SystemExit:
        db_cards = set()                     # 库缺/旧也不影响"只列清单"（视图 fail-soft）
    items: list[dict[str, Any]] = []
    total = 0
    for p in sorted(ge.ATOMS.rglob("ATOM-*.md")):
        if "README" in p.name:
            continue
        total += 1
        m = ge._meta(p)
        cid = str(m.get("id") or p.stem)
        if cid in db_cards or m.get("claim_structured"):
            continue
        items.append({"card": cid, "path": p.relative_to(ROOT).as_posix(),
                      "status": str(m.get("status") or "（无 status 字段）"),
                      "why": BACKLOG_WHY})
    return items, total


SIGNOFF_HOWTO = (
    "[prop] 人签指引（**仓库既有约定**，不是新协议：卡面 `verified_by: human:<名>`；\n"
    "       gate 会校验 `<名>` 与**该文件最后一次 git 提交的作者**一致 —— 见\n"
    "       gate_engine 的 verified_by/git-author 规则，别自己造签署字段）：\n"
    "  1) 编辑卡面加一行：  verified_by: human:<你的 git 提交者名>\n"
    "  2) 重建视图：        .venv\\Scripts\\python.exe tools/prop_graph.py build\n"
    "  3) 复核生效：        .venv\\Scripts\\python.exe tools/prop_graph.py query --pending-signoff"
)


def _print_rows(rows: list[dict[str, Any]]) -> None:
    for r in rows:
        ev = r["evidence"] or "（无 evidence 字段）"
        rat = r["statement"][:80]
        print(f"- {r['prop_key']}  [{r['claim_type']}] {rat}")
        print(f"    卡 {r['card']}（{r['card_kind']}，{r['card_path']}）")
        print(f"    证据 {ev} · 机验 {'有锚' if r['machine_verified'] else '无锚'}"
              f" · 签署 {r['signoff_state']}（signed_by={r['signed_by'] or '空'}）")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="命题状态图（只读派生视图；独立于 concepts 表）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    b = sub.add_parser("build", help="重建库（幂等）")
    b.add_argument("--db", default=str(DEFAULT_DB))
    s = sub.add_parser("stats", help="总量与分布")
    s.add_argument("--db", default=str(DEFAULT_DB))
    s.add_argument("--json", action="store_true")
    q = sub.add_parser("query", help="按条件检索")
    q.add_argument("--db", default=str(DEFAULT_DB))
    q.add_argument("--id")
    q.add_argument("--card")
    q.add_argument("--type", dest="ctype", choices=["observation", "inference"])
    q.add_argument("--machine", choices=["yes", "no"])
    q.add_argument("--sign", choices=["prop_signed", "card_signed", "unsigned"])
    q.add_argument("--pending-signoff", action="store_true",
                   help="566：列出未人签的命题 + 可直接照做的人签指引")
    q.add_argument("--backlog", action="store_true",
                   help="566：列出还没有命题的原子卡（待回填清单；只列清单不动手）")
    q.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.cmd == "build":
        db = build(a.db)
        st = stats(db)
        print(f"[prop] 已重建 {db}：命题 {st['propositions']} 条（卡 {st['cards']} 张）"
              f"· 按类型 {st['by_claim_type']} · 按签署 {st['by_signoff']}"
              f"· 机验 {st['machine_verified']}")
        return 0
    if a.cmd == "stats":
        st = stats(a.db)
        if a.json:
            print(json.dumps(st, ensure_ascii=False, indent=1))
        else:
            print(f"[prop] 命题 {st['propositions']} 条 / 卡 {st['cards']} 张 · "
                  f"类型 {st['by_claim_type']} · 签署 {st['by_signoff']} · "
                  f"机验 {st['machine_verified']}")
            print(f"[prop] 注：{st['machine_verified_note']}")
        return 0
    if a.pending_signoff:                       # 566 任务 1：人审交接视图（待签）
        rows = pending_signoff(a.db)
        if a.json:
            print(json.dumps({"tool": "prop_graph", "version": VERSION,
                              "view": "pending_signoff", "count": len(rows),
                              "rows": rows, "howto": SIGNOFF_HOWTO},
                             ensure_ascii=False, indent=1))
            return 0
        if not rows:
            print("[prop] 无待办：没有未人签的命题 ✓")
            return 0
        print(f"[prop] 未人签命题 {len(rows)} 条（命题级 signed_by 与卡级 verified_by 都没有）：")
        _print_rows(rows)
        print(SIGNOFF_HOWTO)
        return 0
    if a.backlog:                               # 566 任务 1：人审交接视图（待回填）
        items, total = backlog(a.db)
        if a.json:
            print(json.dumps({"tool": "prop_graph", "version": VERSION, "view": "backlog",
                              "count": len(items), "atoms_total": total,
                              "rows": items, "why": BACKLOG_WHY},
                             ensure_ascii=False, indent=1))
            return 0
        if not items:
            print(f"[prop] 无待办：原子卡 {total} 张全部已有 claim_structured 命题 ✓")
            return 0
        print(f"[prop] 待回填原子卡 {len(items)} 张（总原子卡 {total} − 带命题 {total - len(items)}）：")
        for it in items:
            print(f"- {it['card']}  状态 {it['status']}  （{it['path']}）")
            print(f"    为什么还没回填：{it['why']}")
        return 0
    rows = query(a.db, prop_id=a.id, card=a.card, ctype=a.ctype,
                 machine=None if a.machine is None else a.machine == "yes", sign=a.sign)
    if a.json:
        print(json.dumps({"tool": "prop_graph", "version": VERSION, "count": len(rows),
                          "rows": rows}, ensure_ascii=False, indent=1))
    else:
        print(f"[prop] 命中 {len(rows)} 条：")
        _print_rows(rows)
    return 0

if __name__ == "__main__":
    if "--check" in sys.argv:
        print("OK: prop_graph --check（只读：加载即校验，不执行任何业务逻辑）")
        sys.exit(0)
    raise SystemExit(main())
