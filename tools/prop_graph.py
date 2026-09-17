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
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
import gate_engine as ge  # noqa: E402

VERSION = "v1.0"
DEFAULT_DB = ROOT / "data" / "propositions.db"

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
    """重建库（**幂等**：同输入 ⇒ 同内容；表全 DROP 重建，不存任何时间戳）。"""
    db = Path(db_path) if db_path else DEFAULT_DB
    db.parent.mkdir(parents=True, exist_ok=True)
    rows = extract()
    conn = sqlite3.connect(str(db))
    try:
        for t in ("meta", "props", "prop_evidence"):
            conn.execute(f"DROP TABLE IF EXISTS {t}")
        conn.executescript(SCHEMA)
        conn.executemany(
            "INSERT INTO meta(key,value) VALUES(?,?)",
            [("schema", "1"), ("tool", "prop_graph.py"), ("version", VERSION),
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
    p = Path(db)
    if not p.is_file():
        raise SystemExit(f"[prop] 库不存在：{p}（先跑 `prop_graph.py build`）")
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
    raise SystemExit(main())
