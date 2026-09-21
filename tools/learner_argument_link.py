#!/usr/bin/env python3
"""614 线B B4：学习者-论证层联动。

联动逻辑：
  1. 学习者掌握某 KC（原子卡）→ **自动识别该 KC 相关的论证链**
     （= `data/propositions.db` 中 card==KC 的全部命题：observation 前提 → inference 结论）。
  2. 检查用户是否理解论证链的**推理**：用户对链上每个命题标记 understood（理解/未理解）。
  3. `data/learner_argument_understanding.jsonl`（append-only）记录理解状态（latest-wins）。
  4. **影响推荐路径**：已掌握但论证链未理解透的 KC ⇒ 推荐「论证复盘」。

CLI：
  python tools/learner_argument_link.py chains --kc <id>          # 查看该 KC 的论证链
  python tools/learner_argument_link.py mark --kc <id> --prop <prop_key> --understood yes|no [--note ..]
  python tools/learner_argument_link.py status [--kc <id>]         # 理解状态
  python tools/learner_argument_link.py review                     # 推荐「论证复盘」的 KC
  python tools/learner_argument_link.py --check                    # 自验证（exit 0=通过）

铁律：记录 append-only（latest-wins 读取）；命题库为只读派生视图（绝不写回卡）；
  单用户 default；未理解绝不臆造为已理解。
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, cast

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

DEFAULT_DB = ROOT / "data" / "propositions.db"
DEFAULT_STORE = ROOT / "data" / "learner_argument_understanding.jsonl"
USER = "default"
MASTERY_THRESHOLD = 0.5


def _now() -> str:
    return datetime.now().isoformat(timespec="seconds")


def chains_for_kc(kc: str, db: Path | str = DEFAULT_DB) -> list[dict]:
    """该 KC 的论证链：observation 前提在前、inference 结论在后（卡内顺序）。"""
    p = Path(db)
    if not p.is_file():
        return []
    conn = sqlite3.connect(str(p))
    try:
        rows = conn.execute(
            "SELECT prop_key, prop_id, claim_type, statement, evidence, machine_verified, "
            "signoff_state FROM props WHERE card=? ORDER BY "
            "CASE claim_type WHEN 'observation' THEN 0 ELSE 1 END, prop_id",
            (kc,)).fetchall()
    finally:
        conn.close()
    return [{"prop_key": r[0], "prop_id": r[1], "claim_type": r[2], "statement": r[3],
             "evidence": r[4], "machine_verified": r[5], "signoff_state": r[6]} for r in rows]


def load_all(store: Path) -> list[dict]:
    if not store.is_file():
        return []
    out: list[dict] = []
    for line in store.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        out.append(cast("dict[str, Any]", json.loads(line)))
    return out


def record(store: Path, user: str, kc: str, prop_key: str, understood: bool,
           note: str | None = None) -> dict:
    rec = {"user_id": user, "kc_id": kc, "prop_key": prop_key, "understood": bool(understood),
           "marked_time": _now()}
    if note:
        rec["note"] = note
    store.parent.mkdir(parents=True, exist_ok=True)
    with store.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(rec, ensure_ascii=False) + "\n")
    return rec


def understanding(store: Path, user: str = USER, kc: str | None = None) -> dict[str, bool]:
    """latest-wins：遍历 append-only 记录，后写覆盖前写。返回 prop_key→understood。"""
    out: dict[str, bool] = {}
    for r in load_all(store):
        if r.get("user_id") != user:
            continue
        if kc and r.get("kc_id") != kc:
            continue
        out[r["prop_key"]] = bool(r.get("understood"))
    return out


def chain_status(store: Path, kc: str, db: Path | str = DEFAULT_DB,
                 user: str = USER) -> dict:
    chain = chains_for_kc(kc, db)
    und = understanding(store, user, kc)
    total = len(chain)
    n_ok = sum(1 for c in chain if und.get(c["prop_key"]))
    return {"kc_id": kc, "total_props": total, "understood_props": n_ok,
            "fully_understood": total > 0 and n_ok == total}


def recommend_argument_review(learner_store: Path, store: Path, user: str = USER,
                              threshold: float = MASTERY_THRESHOLD,
                              db: Path | str = DEFAULT_DB) -> list[str]:
    """已掌握（≥阈值）但论证链未理解透的 KC ⇒ 推荐论证复盘。"""
    import learner_behavior_logger as b1  # noqa: E402
    mastery = b1.replay(learner_store, user)
    out: list[str] = []
    for kc, m in mastery.items():
        if m < threshold:
            continue
        st = chain_status(store, kc, db, user)
        if st["total_props"] > 0 and not st["fully_understood"]:
            out.append(kc)
    return sorted(out)


def check(db: Path | str, store: Path) -> list[str]:
    import tempfile
    problems: list[str] = []
    with tempfile.TemporaryDirectory() as td:
        tdb = Path(td) / "props.db"
        conn = sqlite3.connect(str(tdb))
        conn.execute("CREATE TABLE props (prop_key TEXT, card TEXT, prop_id TEXT, "
                     "claim_type TEXT, statement TEXT, evidence TEXT, machine_verified INT, "
                     "signoff_state TEXT)")
        conn.execute("INSERT INTO props VALUES ('ATOM-X::prop-1','ATOM-X','prop-1','observation','前提','EV',1,'signed')")
        conn.execute("INSERT INTO props VALUES ('ATOM-X::prop-2','ATOM-X','prop-2','inference','结论','EV',0,'unsigned')")
        conn.commit()
        conn.close()
        # 1) 论证链识别（observation 在前）
        chain = chains_for_kc("ATOM-X", tdb)
        if [c["claim_type"] for c in chain] != ["observation", "inference"]:
            problems.append("论证链应为 observation→inference 有序")
        # 2) 记录 append-only + latest-wins
        tstore = Path(td) / "u.jsonl"
        record(tstore, USER, "ATOM-X", "ATOM-X::prop-1", True)
        record(tstore, USER, "ATOM-X", "ATOM-X::prop-1", False)  # 后写覆盖
        if understanding(tstore, USER, "ATOM-X").get("ATOM-X::prop-1") is not False:
            problems.append("理解状态应 latest-wins")
        # 3) 影响推荐：已掌握但未理解透 ⇒ 进入论证复盘
        import learner_behavior_logger as b1  # noqa: E402
        lstore = Path(td) / "beh.jsonl"
        for _ in range(10):
            b1.record(lstore, USER, "ATOM-X", "correct", "exercise", None, False)
        recs = recommend_argument_review(lstore, tstore, USER, 0.5, tdb)
        if "ATOM-X" not in recs:
            problems.append("已掌握但论证未理解透的 KC 应进入论证复盘推荐")
        # 全部标记理解后应移出
        record(tstore, USER, "ATOM-X", "ATOM-X::prop-1", True)
        record(tstore, USER, "ATOM-X", "ATOM-X::prop-2", True)
        recs2 = recommend_argument_review(lstore, tstore, USER, 0.5, tdb)
        if "ATOM-X" in recs2:
            problems.append("论证全理解后应移出论证复盘推荐")
    return problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="614 B4 学习者-论证层联动")
    ap.add_argument("command", nargs="?", default="status",
                    choices=["chains", "mark", "status", "review"], help="子命令（默认 status）")
    ap.add_argument("--kc", default=None)
    ap.add_argument("--prop", default=None)
    ap.add_argument("--understood", default=None, choices=["yes", "no"])
    ap.add_argument("--note", default=None)
    ap.add_argument("--user", default=USER)
    ap.add_argument("--db", default=None)
    ap.add_argument("--store", default=None)
    ap.add_argument("--learner-store", default=None)
    ap.add_argument("--check", action="store_true", help="自验证（exit 0=通过）")
    a = ap.parse_args(argv)
    db = Path(a.db) if a.db else DEFAULT_DB
    store = Path(a.store) if a.store else DEFAULT_STORE

    if a.check:
        problems = check(db, store)
        if problems:
            print("[link] ❌ 自检失败：", file=sys.stderr)
            for p in problems:
                print(f"    - {p}", file=sys.stderr)
            return 1
        print("[link] ✅ 自验证通过：论证链识别 / 理解状态 latest-wins / 论证复盘推荐 均一致")
        return 0

    cmd = a.command
    if cmd == "chains":
        if not a.kc:
            print("[link] ❌ chains 需要 --kc", file=sys.stderr)
            return 2
        chain = chains_for_kc(a.kc, db)
        if not chain:
            print(f"[link] ⚠ 未找到 {a.kc} 的论证链（命题库缺失或无该卡）", file=sys.stderr)
            return 2
        print(json.dumps(chain, ensure_ascii=False, indent=1))
        return 0
    if cmd == "mark":
        if not a.kc or not a.prop or a.understood is None:
            print("[link] ❌ mark 需要 --kc --prop --understood yes|no", file=sys.stderr)
            return 2
        rec = record(store, a.user, a.kc, a.prop, a.understood == "yes", a.note)
        print(json.dumps(rec, ensure_ascii=False))
        return 0
    if cmd == "review":
        lstore = Path(a.learner_store) if a.learner_store else None
        if lstore is None:
            import learner_behavior_logger as b1  # noqa: E402
            lstore = b1.DEFAULT_STORE
        recs = recommend_argument_review(lstore, store, a.user, MASTERY_THRESHOLD, db)
        print(json.dumps({"argument_review_kc": recs, "count": len(recs)},
                         ensure_ascii=False, indent=1))
        return 0
    # status
    if a.kc:
        print(json.dumps(chain_status(store, a.kc, db, a.user), ensure_ascii=False, indent=1))
    else:
        und = understanding(store, a.user)
        print(json.dumps({"user": a.user, "marked_props": len(und),
                          "understood": sum(1 for v in und.values() if v)},
                         ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
