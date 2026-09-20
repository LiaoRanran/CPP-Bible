#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tq_ext.py — 534 增量原型（沙箱）。基线 = 苦力落地版 tools/task_queue.py（d976170）。

纪律：不复制落地版逻辑，import 它当库，只做它还没有的四件事：
  ① 结构化 handoff + checkpoint（断点续跑）
  ② yield 到顶让出 + 残任务切子任务（parent 回指）
  ③ touch_set 文件级写冲突锁（claim 候选过滤 + 冲突任务 id 回报）
  ④ complete 验证门禁（先跑 verify_cmd，过了才 done；不过回 queued，attempts+1）
外加 534 自攻面：人工 takeover（租约内不抢活）、worker token  possession（E12）、
enqueue 环检测、心跳假活指纹。

用法（探针用 --db 指向沙箱库；落地施工后 --db 与落地版同款）：
  python tq_ext.py --db X.db --json enqueue --type atom_produce --payload-ref p --touch f1,f2 ...
  python tq_ext.py --db X.db --json claim  --worker B [--takeover T --force --reason ...]
  python tq_ext.py --db X.db --json checkpoint <id> --worker B --handoff h.json
  python tq_ext.py --db X.db --json heartbeat <id> --worker B --used 320
  python tq_ext.py --db X.db --json yield <id> --worker B --handoff h.json [--force]
  python tq_ext.py --db X.db --json complete <id> --worker B [--result-ref r]
  python tq_ext.py --db X.db --json doctor
未列出的子命令（init/list/fail/blocked/done…）原样转发落地版 task_queue.main。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import socket
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parent.parent
sys.path.insert(0, str(REPO / "tools"))
import task_queue as tq  # noqa: E402  落地版 d976170

ANCHOR_ROOT = Path(os.environ.get("TQ_ROOT", str(tq.ROOT)))
# 探针/施工期环境覆盖（函数体内引用模块全局，patch 对 _pick/_sweep_stale 生效）
tq.MAX_ATTEMPTS = int(os.environ.get("TQ_MAX_ATTEMPTS") or tq.MAX_ATTEMPTS)
GRACE_S = int(os.environ.get("TQ_TAKEOVER_GRACE", "120"))   # 心跳新鲜宽限：内须 force 接管
YIELD_BUDGET_LEFT = int(os.environ.get("TQ_YIELD_BUDGET_LEFT", "100"))
MAX_CHILDREN = int(os.environ.get("TQ_MAX_CHILDREN", "4"))
MIN_CHILD_BUDGET = int(os.environ.get("TQ_MIN_CHILD_BUDGET", "80"))

NEW_COLS: dict[str, str] = {
    "touch_set": "TEXT NOT NULL DEFAULT '[]'",
    "budget_calls": "INTEGER NOT NULL DEFAULT 500",
    "budget_used_calls": "INTEGER NOT NULL DEFAULT 0",
    "handoff_path": "TEXT",
    "verify_cmd": "TEXT NOT NULL DEFAULT ''",
    "parent_task": "TEXT",
    "produced_by_model": "TEXT",
    "steps_total": "INTEGER NOT NULL DEFAULT 0",
    "steps_done": "INTEGER NOT NULL DEFAULT 0",
    "checkpoint": "TEXT NOT NULL DEFAULT '{}'",
    "cp_fingerprint": "TEXT NOT NULL DEFAULT ''",
    "claimed_token": "TEXT",
    "verify_hash": "TEXT",
    "last_hb_fp": "TEXT",
    "hb_same_count": "INTEGER NOT NULL DEFAULT 0",
}
EVENTS_DDL = """
CREATE TABLE IF NOT EXISTS events(
  seq INTEGER PRIMARY KEY AUTOINCREMENT,
  task_id TEXT NOT NULL, at TEXT NOT NULL, actor TEXT NOT NULL,
  event TEXT NOT NULL, detail TEXT NOT NULL DEFAULT ''
);"""


class TQError(Exception):
    """业务拒绝（CLI exit 2，区别于落地版 SystemExit exit 1；探针据此断言）。"""


# ── 迁移（幂等 ALTER，零破坏）──────────────────────────────────────────────────
SCHEMA_VERSION = 1


def migrate(db_path: Path) -> None:
    """冷启动并发安全迁移：落地版建表（IF NOT EXISTS 本身幂等）+ 单事务升级。

    实测教训：逐条 ALTER 自动提交时，两个冷启动进程会读到"加列中途"的中间态，
    各自补同一列 → duplicate column name（冷启动 6/8 命中）。修法：整段升级包在
    BEGIN IMMEDIATE 内，并用 PRAGMA user_version 做版本门；第二个进程等锁后看到
    版本已升即整段跳过。
    """
    # 单连接单事务：busy_timeout 必须先于 journal_mode（落地版 _connect 顺序相反，
    # 在全新库冷启动瞬间 PRAGMA WAL 需排它而此时还没有等待预算）；建表也并入本事务，
    # 消除"init 连接关闭→迁移连接开启"之间的缝隙（该缝隙曾 1/10 复现 locked）。
    import sqlite3 as _sq
    conn = _sq.connect(str(db_path), timeout=15.0, isolation_level=None)
    conn.row_factory = tq.sqlite3.Row
    try:
        conn.execute("PRAGMA busy_timeout=15000")
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("BEGIN IMMEDIATE")
        ver = conn.execute("PRAGMA user_version").fetchone()[0]
        if ver < SCHEMA_VERSION:
            conn.executescript(tq.DDL)          # 引用落地版表结构，不复制
            have = {r["name"] for r in conn.execute("PRAGMA table_info(tasks)")}
            for col, decl in NEW_COLS.items():
                if col not in have:
                    conn.execute(f"ALTER TABLE tasks ADD COLUMN {col} {decl}")
            conn.executescript(EVENTS_DDL)
            conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
        conn.commit()
    except BaseException:
        tq._rollback(conn)
        raise
    finally:
        conn.close()


def _conn(db_path: Path):
    migrate(db_path)
    return tq._connect(db_path)


def _event(conn, task_id: str, actor: str, event: str, detail: str = "") -> None:
    conn.execute("INSERT INTO events(task_id,at,actor,event,detail) VALUES(?,?,?,?,?)",
                 (task_id, tq._now(), actor, event, detail[:1500]))


def _jload(s: str | None, default):
    try:
        return json.loads(s) if s else default
    except json.JSONDecodeError:
        return default


# ── worker token（E12：claimed_by 字符串可冒充；叠加文件 possession）────────────
def workers_dir(db_path: Path) -> Path:
    d = db_path.parent / "workers"
    d.mkdir(parents=True, exist_ok=True)
    return d


def worker_secret(db_path: Path, worker: str, *, register: bool) -> str:
    p = workers_dir(db_path) / f"{worker}.token"
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))["secret"]
    if not register:
        raise TQError(f"worker {worker} 未注册（无 workers/{worker}.token，冒名拦截）")
    secret = secrets.token_hex(16)
    p.write_text(json.dumps({"id": worker, "secret": secret,
                             "host": socket.gethostname(), "pid": os.getpid(),
                             "at": tq._now()}, ensure_ascii=False, indent=1),
                 encoding="utf-8")
    return secret


def _authorize(conn, row, worker: str, db_path: Path) -> None:
    if row["claimed_by"] != worker:
        raise TQError(f"任务由 {row['claimed_by']!r} claim，{worker!r} 无权（认领者绑定）")
    disk = worker_secret(db_path, worker, register=False)
    if row["claimed_token"] != disk:
        raise TQError("worker token 不符（须持有 claim 时落盘的 token 文件，E12 冒名拦截）")


# ── enqueue 增量：touch/verify/budget/parent/model/steps + 环检测 ───────────────
def _has_cycle(conn, tid: str, deps: list[str]) -> bool:
    """新边 tid→deps（tid 依赖 deps）；若任一 dep 能沿 deps 链回到 tid 则成环。"""
    stack, seen = list(deps), set()
    while stack:
        cur = stack.pop()
        if cur == tid:
            return True
        if cur in seen:
            continue
        seen.add(cur)
        r = conn.execute("SELECT deps FROM tasks WHERE id=?", (cur,)).fetchone()
        if r:
            stack.extend(_jload(r["deps"], []))
    return False


def enqueue_ext(db_path: Path, *, task_type: str, payload_ref: str,
                priority: int = 100, deps: list[str] | None = None,
                task_id: str | None = None, touch: list[str] | None = None,
                verify_cmd: str = "", budget: int = 500, goal: str = "",
                parent: str | None = None, model: str | None = None,
                steps: int = 0, worker: str = "enqueuer") -> dict[str, Any]:
    conn = _conn(db_path)
    try:
        conn.execute("BEGIN IMMEDIATE")
        tid = task_id or tq.make_id(task_type, payload_ref)
        if conn.execute("SELECT 1 FROM tasks WHERE id=?", (tid,)).fetchone():
            conn.commit()
            return {"id": tid, "created": False, "reason": "同 id 已存在（幂等）"}
        deps = list(deps or [])
        missing = [d for d in deps if not conn.execute(
            "SELECT 1 FROM tasks WHERE id=?", (d,)).fetchone()]
        if missing:
            conn.rollback()
            raise TQError(f"deps 引用不存在任务：{missing}")
        if _has_cycle(conn, tid, deps):
            conn.rollback()
            raise TQError(f"deps 成环（{tid} 沿依赖链可回到自身），enqueue 即拒")
        now = tq._now()
        conn.execute(
            "INSERT INTO tasks(id,type,payload_ref,status,priority,deps,attempts,"
            "created_at,updated_at,touch_set,verify_cmd,budget_calls,parent_task,"
            "produced_by_model,steps_total,steps_done,checkpoint) "
            "VALUES(?,?,?,'queued',?,?,0,?,?,?,?,?,?,?,?,0,'{}')",
            (tid, task_type, payload_ref, int(priority),
             json.dumps(deps, ensure_ascii=False), now, now,
             json.dumps(sorted(set(touch or [])), ensure_ascii=False),
             verify_cmd, int(budget), parent, model, int(steps)))
        _event(conn, tid, worker, "enqueue",
               f"deps={deps} touch={sorted(set(touch or []))} steps={steps}")
        conn.commit()
        return {"id": tid, "created": True, "deps_missing": []}
    except BaseException:
        tq._rollback(conn)
        raise
    finally:
        conn.close()


# ── claim 增强：touch_set 过滤 + 人工 takeover（租约内不抢活）──────────────────
def _touch_conflicts(conn, touch: list[str]) -> list[tuple[str, list[str]]]:
    out = []
    for r in conn.execute("SELECT id,touch_set FROM tasks WHERE status='claimed'"):
        inter = sorted(set(_jload(r["touch_set"], [])) & set(touch))
        if inter:
            out.append((r["id"], inter))
    return out


def claim_ext(db_path: Path, worker: str, *, types: list[str] | None = None,
              takeover: str | None = None, force: bool = False,
              reason: str = "") -> dict[str, Any]:
    conn = _conn(db_path)
    try:
        conn.execute("BEGIN IMMEDIATE")
        now = tq._now()
        if takeover:
            tr = conn.execute("SELECT * FROM tasks WHERE id=?", (takeover,)).fetchone()
            if not tr:
                conn.rollback(); raise TQError(f"接管目标不存在：{takeover}")
            if tr["status"] != "claimed":
                conn.rollback()
                raise TQError(f"接管目标状态={tr['status']}（仅 claimed 可接管）")
            age = 999999
            if tr["heartbeat_at"]:
                age = (time.time() - time.mktime(
                    time.strptime(tr["heartbeat_at"], "%Y-%m-%dT%H:%M:%S")))
            if age < GRACE_S and not force:
                conn.rollback()
                raise TQError(
                    f"{takeover} 心跳仅 {tr['heartbeat_at']}（{int(age)}s 前），疑似仍在跑；"
                    f"人确认旧会话已死后用 --takeover {takeover} --force --reason <原因>")
            if force and not reason.strip():
                conn.rollback()
                raise TQError("--force 接管必须给 --reason（留痕担责）")
            conn.execute(
                "UPDATE tasks SET status='queued',claimed_by=NULL,claimed_token=NULL,"
                "heartbeat_at=NULL,updated_at=? WHERE id=?", (now, takeover))
            _event(conn, takeover, worker, "manual_takeover",
                   f"from={tr['claimed_by']} age={int(age)}s force={force} reason={reason}")
            target_id = takeover
        else:
            tq._sweep_stale(conn, now)
            target_id = None

        # 候选：落地版排序（priority, created_at, id）+ deps 门，新增 touch 过滤
        sql = "SELECT * FROM tasks WHERE status='queued'"
        args: list[Any] = []
        if types:
            sql += f" AND type IN ({','.join('?' * len(types))})"
            args += types
        sql += " ORDER BY priority ASC, created_at ASC, id ASC"
        chosen, blocked_touch = None, []
        for row in conn.execute(sql, args).fetchall():
            if int(row["attempts"] or 0) > tq.MAX_ATTEMPTS:
                tq._block(conn, row["id"],
                          f"attempts={row['attempts']} > {tq.MAX_ATTEMPTS}", now)
                continue
            ok, _pending = tq._deps_done(conn, row["deps"])
            if not ok:
                continue
            if target_id and row["id"] != target_id:
                continue
            conf = _touch_conflicts(conn, _jload(row["touch_set"], []))
            if conf:
                blocked_touch.append({"id": row["id"], "blocked_by":
                                      [{"task": i, "files": f} for i, f in conf]})
                continue
            chosen = row
            break
        if chosen is None:
            conn.commit()
            return {"claimed": None, "blocked_by_touch": blocked_touch}
        secret = worker_secret(db_path, worker, register=True)
        conn.execute(
            "UPDATE tasks SET status='claimed',claimed_by=?,claimed_token=?,claimed_at=?,"
            "heartbeat_at=?,attempts=attempts+1,updated_at=? "
            "WHERE id=? AND status='queued'",
            (worker, secret, now, now, now, chosen["id"]))
        _event(conn, chosen["id"], worker, "claim", f"attempt={chosen['attempts']+1}")
        out = tq._as_row_dict(conn.execute(
            "SELECT * FROM tasks WHERE id=?", (chosen["id"],)).fetchone())
        conn.commit()
        out["handoff"] = _load_handoff(out.get("handoff_path"))
        return {"claimed": out, "blocked_by_touch": blocked_touch}
    except BaseException:
        tq._rollback(conn)
        raise
    finally:
        conn.close()


def _rel_store(path: Path) -> str:
    """handoff 路径存储：在锚根内存相对 posix，否则绝对。"""
    try:
        return path.resolve().relative_to(ANCHOR_ROOT.resolve()).as_posix()
    except ValueError:
        return str(path)


def _load_handoff(rel: str | None) -> dict | None:
    if not rel:
        return None
    p = Path(rel)
    if not p.is_absolute():
        p = ANCHOR_ROOT / rel
    if not p.is_file():
        return None
    return json.loads(p.read_text(encoding="utf-8"))


# ── handoff 质量校验（gate 可复用的纯函数）──────────────────────────────────────
def _anchor_ok(anchor: str) -> bool:
    if anchor.startswith(("cmd:", "git:")):
        return len(anchor) > 6
    p = anchor.split(":", 1)[0]
    return (ANCHOR_ROOT / p).is_file()


def validate_handoff(h: dict, *, for_yield: bool) -> list[str]:
    errs: list[str] = []
    if not str(h.get("goal") or "").strip():
        errs.append("goal 为空")
    na = str(h.get("next_action") or "").strip()
    if len(na) < 4:
        errs.append("next_action 缺失或不像具体动作")
    sd = h.get("steps_done") or []
    if not isinstance(sd, list):
        errs.append("steps_done 必须是列表")
    else:
        for i, st in enumerate(sd):
            if not isinstance(st, dict) or not st.get("title"):
                errs.append(f"steps_done[{i}] 缺 title")
                continue
            for o in st.get("outputs") or []:
                if isinstance(o, dict) and o.get("path"):
                    f = ANCHOR_ROOT / str(o["path"])
                    if not f.is_file():
                        errs.append(f"steps_done[{i}] 产物不存在：{o['path']}")
                    elif o.get("sha256") and \
                            hashlib.sha256(f.read_bytes()).hexdigest() != str(o["sha256"]):
                        errs.append(f"steps_done[{i}] 产物哈希不符：{o['path']}（防偷换）")
    vf = h.get("verified_facts") or []
    if not isinstance(vf, list) or not vf:
        errs.append("verified_facts 为空（至少一条带锚点结论）")
    else:
        for i, fct in enumerate(vf):
            if fct.get("trust") not in ("L1", "L2", "L3"):
                errs.append(f"verified_facts[{i}] 缺 trust∈L1/L2/L3")
            a = str(fct.get("anchor") or "")
            if not a or not _anchor_ok(a):
                errs.append(f"verified_facts[{i}] 无锚点或锚点不存在：{a[:60]}")
            if fct.get("trust") == "L2" and not a.startswith("cmd:"):
                errs.append(f"verified_facts[{i}] L2 判决事实必须用 cmd: 锚点（可重跑）")
    if for_yield:
        sr = h.get("steps_remaining") or []
        if not isinstance(sr, list) or not sr:
            errs.append("yield 时 steps_remaining 为空（无剩余应 complete）")
    return errs


def cp_fingerprint(h: dict) -> str:
    x = hashlib.sha256()
    for st in h.get("steps_done") or []:
        x.update(str(st.get("n")).encode())
        for o in st.get("outputs") or []:
            x.update(str(o.get("path")).encode()); x.update(str(o.get("sha256")).encode())
    x.update(str(len(h.get("steps_remaining") or [])).encode())
    return x.hexdigest()[:16]


def checkpoint_ext(db_path: Path, tid: str, worker: str, handoff_path: Path,
                   *, used: int | None = None, force: bool = False) -> dict:
    h = json.loads(handoff_path.read_text(encoding="utf-8"))
    hard = [e for e in validate_handoff(h, for_yield=False) if not e.startswith("yield ")]
    if hard and not force:
        raise TQError("checkpoint 质量不过：\n  - " + "\n  - ".join(hard))
    conn = _conn(db_path)
    try:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
        if not row:
            conn.rollback(); raise TQError("无此任务")
        _authorize(conn, row, worker, db_path)
        rel = _rel_store(handoff_path)
        conn.execute(
            "UPDATE tasks SET checkpoint=?,cp_fingerprint=?,steps_done=?,handoff_path=?,"
            "budget_used_calls=?,heartbeat_at=?,updated_at=? WHERE id=?",
            (json.dumps(h, ensure_ascii=False), cp_fingerprint(h),
             len(h.get("steps_done") or []), rel,
             int(used if used is not None else h.get("budget_used") or 0),
             tq._now(), tq._now(), tid))
        _event(conn, tid, worker, "checkpoint", f"steps_done={len(h.get('steps_done') or [])}")
        conn.commit()
        return {"id": tid, "steps_done": len(h.get("steps_done") or []),
                "fingerprint": cp_fingerprint(h)}
    except BaseException:
        tq._rollback(conn)
        raise
    finally:
        conn.close()


def heartbeat_ext(db_path: Path, tid: str, worker: str, *, used: int = 0,
                  handoff_path: Path | None = None) -> dict:
    conn = _conn(db_path)
    try:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
        if not row:
            conn.rollback(); raise TQError("无此任务")
        _authorize(conn, row, worker, db_path)
        fp = row["cp_fingerprint"]
        same = int(row["hb_same_count"] or 0)
        if handoff_path:
            h = json.loads(handoff_path.read_text(encoding="utf-8"))
            fp = cp_fingerprint(h)
            # 僵尸判据：心跳携带的进度指纹与**上次心跳**相同（checkpoint 落盘的不算，
            # 那是正常推进）；连续第 2 次相同才告警（长步骤里单次不告警，施工版再叠加
            # 心跳间隔阈值，探针用次数复现判定逻辑）。
            if row["last_hb_fp"] is not None and fp == row["last_hb_fp"]:
                same += 1
            else:
                same = 0
        # same>=1 = 与上次心跳指纹相同（基线后的第一次重复即告警；施工版叠加
        # "距上次心跳须 ≥ 一个完整心跳周期"的间隔阈值，长步骤单次不告警）
        zombie = same >= 1
        conn.execute(
            "UPDATE tasks SET heartbeat_at=?,budget_used_calls=?,last_hb_fp=?,"
            "hb_same_count=?,updated_at=? WHERE id=?",
            (tq._now(), int(used), fp, same, tq._now(), tid))
        _event(conn, tid, worker, "heartbeat_zombie" if zombie else "heartbeat",
               f"fp={fp} same={same} used={used}")
        conn.commit()
        return {"id": tid, "zombie_suspect": zombie, "fingerprint": fp,
                "same_count": same}
    except BaseException:
        tq._rollback(conn)
        raise
    finally:
        conn.close()


# ── yield：残任务切子任务（默认一个续跑子任务，携带全部剩余步骤）────────────────
def yield_ext(db_path: Path, tid: str, worker: str, handoff_path: Path, *,
              force: bool = False) -> dict:
    h = json.loads(handoff_path.read_text(encoding="utf-8"))
    errs = validate_handoff(h, for_yield=True)
    if errs:
        raise TQError("yield 被拒（fail-closed）：\n  - " + "\n  - ".join(errs))
    conn = _conn(db_path)
    try:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
        if not row:
            conn.rollback(); raise TQError("无此任务")
        _authorize(conn, row, worker, db_path)
        used = int(h.get("budget_used") or 0)
        left = max(0, int(row["budget_calls"]) - used)
        if left >= YIELD_BUDGET_LEFT and not force:
            conn.rollback()
            raise TQError(f"预算尚余 {left}（<{YIELD_BUDGET_LEFT} 才允许 yield）")
        remaining = h["steps_remaining"]
        # 切分：handoff.step_groups 可选（≤MAX_CHILDREN），默认 1 个续跑子任务
        groups = h.get("step_groups")
        if isinstance(groups, list) and groups:
            groups = groups[:MAX_CHILDREN]
        else:
            groups = [{"steps": remaining, "touch": _jload(row["touch_set"], [])}]
        if any(not g.get("steps") for g in groups):
            conn.rollback(); raise TQError("切出空子任务（碎片防护），拒绝")
        per = max(MIN_CHILD_BUDGET, left // len(groups))
        child_ids, prev = [], None
        for i, g in enumerate(groups, 1):
            cid = f"{tid}.c{i}"
            if conn.execute("SELECT 1 FROM tasks WHERE id=?", (cid,)).fetchone():
                conn.rollback(); raise TQError(f"子任务已存在：{cid}（人工清理后再 yield）")
            cdeps = list(g.get("deps") or [])
            if prev:
                cdeps.append(prev)
            h2 = dict(h)
            h2["steps_remaining"] = g["steps"]
            h2["goal"] = f"[续] {h.get('goal','')}"
            hp = db_path.parent / f"{cid}.handoff.json"
            hp.write_text(json.dumps(h2, ensure_ascii=False, indent=1), encoding="utf-8")
            now = tq._now()
            conn.execute(
                "INSERT INTO tasks(id,type,payload_ref,status,priority,deps,attempts,"
                "created_at,updated_at,touch_set,verify_cmd,budget_calls,parent_task,"
                "produced_by_model,steps_total,handoff_path) "
                "VALUES(?,?,?,'queued',?,?,0,?,?,?,?,?,?,?,?,?)",
                (cid, row["type"], row["payload_ref"], row["priority"],
                 json.dumps(cdeps, ensure_ascii=False), now, now,
                 json.dumps(g.get("touch") or _jload(row["touch_set"], []), ensure_ascii=False),
                 row["verify_cmd"], per, tid, row["produced_by_model"],
                 len(g["steps"]), _rel_store(hp)))
            _event(conn, cid, worker, "enqueue_child", f"parent={tid} budget={per}")
            child_ids.append(cid)
            prev = cid
        conn.execute(
            "UPDATE tasks SET status='yielded',handoff_path=?,checkpoint=?,"
            "cp_fingerprint=?,steps_done=?,claimed_by=NULL,claimed_token=NULL,"
            "heartbeat_at=NULL,budget_used_calls=?,updated_at=? WHERE id=?",
            (_rel_store(handoff_path), json.dumps(h, ensure_ascii=False), cp_fingerprint(h),
             len(h.get("steps_done") or []), used, tq._now(), tid))
        _event(conn, tid, worker, "yield", f"children={child_ids} used={used}")
        conn.commit()
        return {"yielded": tid, "children": child_ids}
    except BaseException:
        tq._rollback(conn)
        raise
    finally:
        conn.close()


# ── complete：verify 门禁（worker 不得自证 done）────────────────────────────────
def _touch_audit(row) -> list[str]:
    """完成后审计：真实改动（git -uall 逐文件展开）超出声明 touch_set 的部分。

    豁免（调度装置自身，不是业务改动）：queue.db*/workers/*.token（data/tasks 运行时态）、
    handoff_path 已登记的交接文件、events 只在库里。沙箱实测教训：不加 -uall 时
    整个未跟踪目录只显示成 'work/'，永远匹配不到逐文件声明。
    """
    declared = set(_jload(row["touch_set"], []))
    exempt = set()
    if row["handoff_path"]:
        exempt.add(str(row["handoff_path"]).replace("\\", "/"))
    try:
        p = subprocess.run(["git", "status", "--porcelain", "-uall"],
                           cwd=str(ANCHOR_ROOT), capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=10)
        changed = set()
        for ln in p.stdout.splitlines():
            if not ln.strip():
                continue
            f = ln[3:].strip().split(" -> ")[-1].strip().replace("\\", "/")
            base = f.rsplit("/", 1)[-1]
            if base.startswith("queue.db") or "/workers/" in f or f.endswith(".token"):
                continue
            changed.add(f)
        return sorted(f for f in changed if f not in declared and f not in exempt)
    except Exception:
        return []


def complete_ext(db_path: Path, tid: str, worker: str, *,
                 result_ref: str | None = None, timeout: int = 900) -> dict:
    conn = _conn(db_path)
    try:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
        if not row:
            conn.rollback(); raise TQError("无此任务")
        _authorize(conn, row, worker, db_path)
        verify = row["verify_cmd"] or ""
        now = tq._now()
        if not verify:
            if not result_ref:
                conn.rollback()
                raise TQError("无 verify_cmd 的任务 complete 必须 --result-ref（转人审，不得自证）")
            vhash = "HUMAN_REVIEW_REQUIRED"
        else:
            t0 = time.perf_counter()
            p = subprocess.run(verify, shell=True, cwd=str(ANCHOR_ROOT),
                               capture_output=True, text=True, encoding="utf-8",
                               errors="replace", timeout=timeout)
            dt = time.perf_counter() - t0
            vhash = (hashlib.sha256((p.stdout + p.stderr).encode("utf-8", "replace"))
                     .hexdigest()[:16] + f"@{dt:.2f}s rc={p.returncode}")
            if p.returncode != 0:
                att = int(row["attempts"]) + 1
                conn.execute("UPDATE tasks SET attempts=?,error=?,updated_at=? WHERE id=?",
                             (att, f"verify rc={p.returncode}: "
                                    f"{(p.stderr or p.stdout)[-300:]}", now, tid))
                _event(conn, tid, worker, "verify_failed", vhash)
                if att > tq.MAX_ATTEMPTS:
                    tq._block(conn, tid, f"verify 反复失败 attempts={att}>{tq.MAX_ATTEMPTS}", now)
                    _event(conn, tid, worker, "blocked", "verify 失败超上限")
                    conn.commit()
                    return {"id": tid, "status": "blocked", "verify_hash": vhash}
                conn.execute(
                    "UPDATE tasks SET status='queued',claimed_by=NULL,claimed_token=NULL,"
                    "heartbeat_at=NULL,updated_at=? WHERE id=?", (now, tid))
                _event(conn, tid, worker, "requeue", f"verify 失败回 queued attempts={att}")
                conn.commit()
                return {"id": tid, "status": "queued", "attempts": att,
                        "verify_hash": vhash}
        undeclared = _touch_audit(row)
        conn.execute(
            "UPDATE tasks SET status='done',result_ref=?,verify_hash=?,updated_at=?,"
            "heartbeat_at=? WHERE id=?",
            (result_ref or row["result_ref"], vhash, now, now, tid))
        if undeclared:
            conn.execute("UPDATE tasks SET error=? WHERE id=?",
                         (f"undeclared_touch={undeclared}", tid))
        _event(conn, tid, worker, "done", f"verify={vhash} undeclared={undeclared}")
        # 父回卷：yielded 父任务的全部子任务 done → 父 done
        parent = row["parent_task"]
        if parent:
            pr = conn.execute("SELECT * FROM tasks WHERE id=?", (parent,)).fetchone()
            if pr and pr["status"] == "yielded":
                open_n = conn.execute(
                    "SELECT COUNT(*) FROM tasks WHERE parent_task=? AND status!='done'",
                    (parent,)).fetchone()[0]
                if open_n == 0:
                    conn.execute("UPDATE tasks SET status='done',updated_at=? WHERE id=?",
                                 (now, parent))
                    _event(conn, parent, worker, "done_rollup", f"via child {tid}")
        conn.commit()
        return {"id": tid, "status": "done", "verify_hash": vhash,
                "undeclared_touch": undeclared,
                "parent_rolled_up": bool(parent)}
    except BaseException:
        tq._rollback(conn)
        raise
    finally:
        conn.close()


def doctor_ext(db_path: Path) -> dict:
    conn = _conn(db_path)
    try:
        out = []
        now = time.time()
        for r in conn.execute("SELECT * FROM tasks WHERE status='claimed'"):
            hb = r["heartbeat_at"]
            age = int(now - time.mktime(time.strptime(hb, "%Y-%m-%dT%H:%M:%S"))) if hb else None
            item = {"id": r["id"], "claimed_by": r["claimed_by"], "heartbeat_age_s": age,
                    "fingerprint": r["cp_fingerprint"], "budget_used": r["budget_used_calls"]}
            if age is not None and age > tq.STALE_AFTER_S:
                item["note"] = "stale：下次 claim 自动回收"
            elif int(r["hb_same_count"] or 0) >= 1:
                item["note"] = "zombie_suspect：心跳指纹与上次相同（假活，施工版叠间隔阈值）"
            elif r["budget_used_calls"] >= int(r["budget_calls"]) - 60:
                item["note"] = "预算将尽：应尽快 yield"
            out.append(item)
        return {"claimed": out}
    finally:
        conn.close()


# ── CLI ────────────────────────────────────────────────────────────────────────
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="534 增量原型（基线 d976170）")
    ap.add_argument("--db", required=True)
    ap.add_argument("--json", action="store_true")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("enqueue")
    s.add_argument("--type", required=True); s.add_argument("--payload-ref", required=True)
    s.add_argument("--id", default=None); s.add_argument("--priority", type=int, default=100)
    s.add_argument("--deps", default=""); s.add_argument("--touch", default="")
    s.add_argument("--verify-cmd", default=""); s.add_argument("--budget", type=int, default=500)
    s.add_argument("--goal", default=""); s.add_argument("--parent", default=None)
    s.add_argument("--model", default=None); s.add_argument("--steps", type=int, default=0)
    s.add_argument("--worker", default="enqueuer")

    s = sub.add_parser("claim")
    s.add_argument("--worker", required=True); s.add_argument("--types", default="")
    s.add_argument("--takeover", default=None); s.add_argument("--force", action="store_true")
    s.add_argument("--reason", default="")

    s = sub.add_parser("checkpoint")
    s.add_argument("id"); s.add_argument("--worker", required=True)
    s.add_argument("--handoff", required=True); s.add_argument("--used", type=int, default=None)
    s.add_argument("--force", action="store_true")

    s = sub.add_parser("heartbeat")
    s.add_argument("id"); s.add_argument("--worker", required=True)
    s.add_argument("--used", type=int, default=0); s.add_argument("--handoff", default=None)

    s = sub.add_parser("yield")
    s.add_argument("id"); s.add_argument("--worker", required=True)
    s.add_argument("--handoff", required=True); s.add_argument("--force", action="store_true")

    s = sub.add_parser("complete")
    s.add_argument("id"); s.add_argument("--worker", required=True)
    s.add_argument("--result-ref", default=None); s.add_argument("--timeout", type=int, default=900)

    sub.add_parser("doctor")

    a, rest = ap.parse_known_args(argv)
    db = Path(a.db)
    try:
        if a.cmd == "enqueue":
            r = enqueue_ext(db, task_type=a.type, payload_ref=a.payload_ref,
                            priority=a.priority,
                            deps=[x for x in a.deps.split(",") if x], task_id=a.id,
                            touch=[x for x in a.touch.split(",") if x],
                            verify_cmd=a.verify_cmd, budget=a.budget, goal=a.goal,
                            parent=a.parent, model=a.model, steps=a.steps, worker=a.worker)
        elif a.cmd == "claim":
            r = claim_ext(db, a.worker, types=[x for x in a.types.split(",") if x],
                          takeover=a.takeover, force=a.force, reason=a.reason)
        elif a.cmd == "checkpoint":
            r = checkpoint_ext(db, a.id, a.worker, Path(a.handoff), used=a.used, force=a.force)
        elif a.cmd == "heartbeat":
            r = heartbeat_ext(db, a.id, a.worker, used=a.used,
                              handoff_path=Path(a.handoff) if a.handoff else None)
        elif a.cmd == "yield":
            r = yield_ext(db, a.id, a.worker, Path(a.handoff), force=a.force)
        elif a.cmd == "complete":
            r = complete_ext(db, a.id, a.worker, result_ref=a.result_ref, timeout=a.timeout)
        elif a.cmd == "doctor":
            r = doctor_ext(db)
        else:
            return tq.main(["--db", str(db), *argv]) if argv else 1
    except TQError as e:
        print(json.dumps({"error": str(e)}, ensure_ascii=False), file=sys.stderr)
        return 2
    print(json.dumps(r, ensure_ascii=False, indent=1 if a.json else None))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
