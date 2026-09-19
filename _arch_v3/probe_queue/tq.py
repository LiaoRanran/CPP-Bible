#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""tq.py — 534 L2 调度层原型（沙箱版；施工时进 tools/task_queue.py）。

在 529 P1-3 草案（tasks 表/6 子命令/BEGIN IMMEDIATE/attempts>3 blocked）上深化：
  - 表新增 touch_set / budget_calls / budget_used_calls / handoff_path / verify_cmd /
    parent_task / produced_by_model / steps_* / checkpoint / cp_fingerprint / claimed_token
  - 8 子命令：enqueue/next/claim/heartbeat/checkpoint/yield/complete/fail/blocked
    （529 的 done 升级为 complete：强制 verify_cmd 通过才 done；保留 done 为隐藏别名）
  - next = 零上下文冷启动唯一入口：原子选任务（拓扑→优先级→入队序）+ touch_set 冲突避让
  - yield = 到顶前主动让出：handoff fail-closed 校验 + 残任务切子任务（parent 回指）
所有路径经 TQ_DB / TQ_ROOT 环境变量可重定向到沙箱；默认 data/tasks/queue.db。
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import secrets
import secrets as _sec
import socket
import subprocess
import sys
import time
from pathlib import Path

PROBE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PROBE_ROOT.parent.parent
DB_PATH = Path(os.environ.get("TQ_DB", str(REPO_ROOT / "data" / "tasks" / "queue.db")))
ANCHOR_ROOT = Path(os.environ.get("TQ_ROOT", str(REPO_ROOT)))
LEASE_SECONDS = int(os.environ.get("TQ_LEASE", "600"))
MAX_ATTEMPTS = int(os.environ.get("TQ_MAX_ATTEMPTS", "3"))
MAX_CHILDREN = int(os.environ.get("TQ_MAX_CHILDREN", "4"))
MIN_CHILD_BUDGET = int(os.environ.get("TQ_MIN_CHILD_BUDGET", "80"))
YIELD_BUDGET_LEFT = int(os.environ.get("TQ_YIELD_BUDGET_LEFT", "100"))

TASK_TYPES = ("atom_produce", "redteam", "replay_batch", "tool_change",
              "doc", "research", "reverify_model", "custom")
STATUSES = ("pending", "in_progress", "done", "failed", "blocked", "yielded")

# type → verify_cmd 模板（{root} 占位；payload_ref 为卡路径时 {card} 可用）
VERIFY_DEFAULT = {
    "atom_produce": '"{py}" "{root}/tools/atom_evidence_replay.py" --card {card} --no-sanitizer',
    "redteam": '"{py}" "{root}/tools/poison_drill.py"',
    "replay_batch": '"{py}" "{root}/tools/atom_evidence_replay.py" --check --no-sanitizer',
    "tool_change": '"{py}" -m pytest tests/ -m fast -q',
    "doc": '"{py}" "{root}/tools/doc_frontmatter.py"',
    "research": "",   # 调研类无机器验证 → complete 要求 --result-ref 且记录 needs_human
    "reverify_model": '"{py}" "{root}/tools/atom_evidence_replay.py" --check --no-sanitizer',
    "custom": "",
}


def now() -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S")


def _jload(s: str | None, default):
    if not s:
        return default
    try:
        return json.loads(s)
    except ValueError:
        return default


# ── DB ─────────────────────────────────────────────────────────────────────
SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks(
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  payload_ref TEXT NOT NULL DEFAULT '',
  goal TEXT NOT NULL DEFAULT '',
  status TEXT NOT NULL DEFAULT 'pending',
  priority INTEGER NOT NULL DEFAULT 100,
  deps TEXT NOT NULL DEFAULT '[]',
  touch_set TEXT NOT NULL DEFAULT '[]',
  verify_cmd TEXT NOT NULL DEFAULT '',
  budget_calls INTEGER NOT NULL DEFAULT 500,
  budget_used_calls INTEGER NOT NULL DEFAULT 0,
  handoff_path TEXT,
  parent_task TEXT,
  produced_by_model TEXT,
  steps_total INTEGER NOT NULL DEFAULT 0,
  steps_done INTEGER NOT NULL DEFAULT 0,
  steps_remaining TEXT NOT NULL DEFAULT '[]',
  checkpoint TEXT NOT NULL DEFAULT '{}',
  cp_fingerprint TEXT NOT NULL DEFAULT '',
  claimed_by TEXT, claimed_token TEXT, lease_expires TEXT, heartbeat_at TEXT,
  attempts INTEGER NOT NULL DEFAULT 0,
  result_ref TEXT, verify_hash TEXT, error TEXT,
  enqueued_seq INTEGER NOT NULL DEFAULT 0,
  created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS events(
  seq INTEGER PRIMARY KEY AUTOINCREMENT,
  task_id TEXT NOT NULL, at TEXT NOT NULL, actor TEXT NOT NULL,
  event TEXT NOT NULL, detail TEXT NOT NULL DEFAULT ''
);
CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
"""


class DB:
    def __init__(self, path: Path = DB_PATH):
        path.parent.mkdir(parents=True, exist_ok=True)
        self.path = path
        self.con = sqlite3_connect(str(path), timeout=15)
        self.con.row_factory = Row
        self.con.execute("PRAGMA busy_timeout=15000")
        # WAL：多进程读写不互锁（Windows 实测章节给出开关结果）
        try:
            self.con.execute("PRAGMA journal_mode=WAL")
        except Exception:
            pass
        self.con.execute("PRAGMA foreign_keys=ON")
        self.con.executescript(SCHEMA)
        self.con.commit()

    def event(self, task_id: str, actor: str, event: str, detail: str = "") -> None:
        self.con.execute(
            "INSERT INTO events(task_id,at,actor,event,detail) VALUES(?,?,?,?,?)",
            (task_id, now(), actor, event, detail[:2000]))

    def close(self) -> None:
        self.con.commit()
        self.con.close()


# 延迟 import，保持文件头可读
import sqlite3  # noqa: E402
from sqlite3 import Row  # noqa: E402


def sqlite3_connect(path: str, timeout: float = 15.0) -> sqlite3.Connection:
    return sqlite3.connect(path, timeout=timeout, isolation_level=None)  # autocommit；事务显式管


# ── worker 身份（E12 教训：claimed_by 绑定，不允许冒名改任务）────────────────
def workers_dir() -> Path:
    d = DB_PATH.parent / "workers"
    d.mkdir(parents=True, exist_ok=True)
    return d


def worker_token(worker: str) -> str | None:
    """worker 首次注册时生成随机 token 落盘；之后一切变更须持有该文件（possession）。"""
    p = workers_dir() / f"{worker}.token"
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8")).get("secret")
    except ValueError:
        return None


def worker_register(worker: str) -> str:
    p = workers_dir() / f"{worker}.token"
    if p.is_file():
        return json.loads(p.read_text(encoding="utf-8"))["secret"]
    secret = secrets.token_hex(16)
    p.write_text(json.dumps({
        "id": worker, "secret": secret, "host": socket.gethostname(),
        "user": os.environ.get("USERNAME") or os.environ.get("USER") or "?",
        "pid": os.getpid(), "created_at": now(),
    }, ensure_ascii=False, indent=1), encoding="utf-8")
    return secret


def auth(db: DB, t: Row, worker: str) -> str | None:
    """返回 None=通过；否则拒绝原因。"""
    if t["claimed_by"] != worker:
        return f"任务由 {t['claimed_by']} claim，{worker} 无权操作（E12 冒名拦截）"
    tok = worker_token(worker)
    if not tok or t["claimed_token"] != tok:
        return "worker token 不匹配（须持有 claim 时的 workers/<id>.token）"
    return None


# ── 选择规则（拓扑序→优先级→最早入队），touch_set 与 in-progress 不相交 ───────
def _topo_weight(con, tid: str) -> int:
    """有多少任务（传递）依赖本任务：被依赖越多越先派（关键路径优先）。"""
    seen: set[str] = set()
    frontier = [tid]
    weight = 0
    while frontier:
        cur = frontier.pop()
        for r in con.execute("SELECT id,deps FROM tasks"):
            if r["id"] in seen:
                continue
            if cur in _jload(r["deps"], []):
                seen.add(r["id"])
                frontier.append(r["id"])
                weight += 1
    return weight


def pick_candidate(db: DB, types: list[str] | None = None):
    """在调用方事务内选任务；返回 (row, conflict_ids)。必须在 BEGIN IMMEDIATE 后调用。"""
    con = db.con
    rows = con.execute(
        "SELECT * FROM tasks WHERE status='pending'"
        + (" AND type IN (%s)" % ",".join("?" * len(types)) if types else ""),
        types or []).fetchall()
    inprog = con.execute(
        "SELECT id,touch_set FROM tasks WHERE status='in_progress'").fetchall()
    held: dict[str, list[str]] = {r["id"]: _jload(r["touch_set"], []) for r in inprog}
    eligible, conflicts = [], {}
    for r in rows:
        deps = _jload(r["deps"], [])
        dep_rows = {x["id"]: x["status"] for x in
                    con.execute("SELECT id,status FROM tasks").fetchall()}
        if any(dep_rows.get(d) != "done" for d in deps):
            continue
        touch = _jload(r["touch_set"], [])
        blockers = [tid for tid, fs in held.items() if set(fs) & set(touch)]
        if blockers:
            conflicts[r["id"]] = blockers
            continue
        eligible.append(r)
    if not eligible:
        return None, conflicts
    eligible.sort(key=lambda r: (-_topo_weight(con, r["id"]),
                                  r["priority"], r["enqueued_seq"]))
    return eligible[0], conflicts


def _lease_ts(seconds: int = LEASE_SECONDS) -> str:
    return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time() + seconds))


# ── handoff 校验（任务2：fail-closed，废 checkpoint 不许让出）─────────────────
def _anchor_check(path_part: str) -> bool:
    """verified_facts 锚点存在性：path:line 或 file 路径（相对 ANCHOR_ROOT）。"""
    if path_part.startswith("cmd:") or path_part.startswith("git:"):
        return len(path_part) > 6
    p = path_part.split(":", 1)[0]
    f = ANCHOR_ROOT / p
    return f.is_file()


def validate_handoff(h: dict, *, for_yield: bool) -> list[str]:
    errs: list[str] = []
    if not str(h.get("goal") or "").strip():
        errs.append("goal 为空（一句话可验证目标必填）")
    na = str(h.get("next_action") or "").strip()
    if not na or len(na) < 4:
        errs.append("next_action 缺失或不像具体命令")
    sd = h.get("steps_done") or []
    if not isinstance(sd, list):
        errs.append("steps_done 必须是列表")
    else:
        for i, st in enumerate(sd):
            if not isinstance(st, dict) or not st.get("title"):
                errs.append(f"steps_done[{i}] 缺 title")
                continue
            for out in st.get("outputs") or []:
                if isinstance(out, dict) and out.get("path"):
                    f = ANCHOR_ROOT / str(out["path"])
                    if not f.is_file():
                        errs.append(f"steps_done[{i}] 产物不存在：{out['path']}")
                    elif out.get("sha256"):
                        got = hashlib.sha256(f.read_bytes()).hexdigest()
                        if got != str(out["sha256"]):
                            errs.append(
                                f"steps_done[{i}] 产物哈希不符：{out['path']}（防产物被偷换）")
    vf = h.get("verified_facts") or []
    if not isinstance(vf, list) or not vf:
        errs.append("verified_facts 为空（至少一条带锚点的已验证结论；无则此任务不该让出）")
    else:
        for i, fct in enumerate(vf):
            if not isinstance(fct, dict):
                errs.append(f"verified_facts[{i}] 不是对象")
                continue
            if fct.get("trust") not in ("L1", "L2", "L3"):
                errs.append(f"verified_facts[{i}] 缺 trust∈L1/L2/L3")
            anchor = str(fct.get("anchor") or "")
            if not anchor or not _anchor_check(anchor):
                errs.append(f"verified_facts[{i}] 锚点不存在或无锚点：{anchor[:60]}")
            if fct.get("trust") == "L2" and not anchor.startswith("cmd:"):
                errs.append(f"verified_facts[{i}] L2 判决事实必须用 cmd: 锚点（可重跑）")
    sr = h.get("steps_remaining") or []
    if for_yield and (not isinstance(sr, list) or not sr):
        errs.append("yield 时 steps_remaining 为空（无剩余步骤应 complete 而非 yield）")
    if for_yield and int(h.get("budget_used") or 0) < 0:
        errs.append("budget_used 非法")
    return errs


def cp_fingerprint_of(h: dict) -> str:
    """假活检测指纹：steps_done 步数 + 各产物路径/哈希。两次心跳间不变=没推进。"""
    hh = hashlib.sha256()
    for st in h.get("steps_done") or []:
        hh.update(str(st.get("n")).encode())
        for o in st.get("outputs") or []:
            hh.update(str(o.get("path")).encode())
            hh.update(str(o.get("sha256")).encode())
    hh.update(str(len(h.get("steps_remaining") or [])).encode())
    return hh.hexdigest()[:16]


# ── 子命令实现 ────────────────────────────────────────────────────────────────
def cmd_init(args) -> int:
    db = DB(); db.event("SYSTEM", args.worker or "init", "db_init"); db.close()
    print(f"[tq] initialized {DB_PATH}")
    return 0


def _parse_csv(s: str | None) -> list[str]:
    return [x.strip() for x in (s or "").split(",") if x.strip()]


def _cycle(con, tid: str, deps: list[str]) -> list[str]:
    """enqueue 时环检测：沿新边 tid→deps 反向找，若依赖者能回到 tid 则成环。"""
    # 新边语义：tid 依赖 deps；检查图中是否存在 dep →…→ tid 的路径
    graph: dict[str, list[str]] = {}
    for r in con.execute("SELECT id,deps FROM tasks"):
        graph[r["id"]] = _jload(r["deps"], [])
    graph.setdefault(tid, [])
    stack = list(deps)
    seen = set()
    while stack:
        cur = stack.pop()
        if cur == tid:
            return [tid]
        if cur in seen:
            continue
        seen.add(cur)
        stack.extend(graph.get(cur, []))
    return []


def cmd_enqueue(args) -> int:
    db = DB()
    con = db.con
    tid = args.id or f"{args.type}-{int(time.time())}-{_sec.token_hex(2)}"
    try:
        con.execute("BEGIN IMMEDIATE")
        if con.execute("SELECT 1 FROM tasks WHERE id=?", (tid,)).fetchone():
            con.commit()
            print(f"[tq] 已存在（幂等）{tid}")
            return 0
        deps = _parse_csv(args.deps)
        for d in deps:
            if not con.execute("SELECT 1 FROM tasks WHERE id=?", (d,)).fetchone():
                con.rollback()
                print(f"[tq] deps 引用不存在任务：{d}", file=sys.stderr)
                return 2
        cyc = _cycle(con, tid, deps)
        if cyc:
            con.rollback()
            print(f"[tq] deps 成环：{'→'.join(cyc)}（enqueue 即拒，不留给运行时挂死）",
                  file=sys.stderr)
            return 2
        seq = con.execute("SELECT COALESCE(MAX(enqueued_seq),0)+1 FROM tasks").fetchone()[0]
        py = sys.executable
        verify = args.verify_cmd
        if verify is None:
            tmpl = VERIFY_DEFAULT.get(args.type, "")
            verify = tmpl.format(py=py, root=str(ANCHOR_ROOT),
                                 card=args.payload_ref or "<payload>") if tmpl else ""
        con.execute(
            "INSERT INTO tasks(id,type,payload_ref,goal,status,priority,deps,touch_set,"
            "verify_cmd,budget_calls,parent_task,produced_by_model,steps_total,"
            "steps_remaining,enqueued_seq,created_at,updated_at)"
            " VALUES(?,?,?,?,'pending',?,?,?,?,?,?,?,?,?,?,?,?)",
            (tid, args.type, args.payload_ref or "", args.goal or "", args.priority,
             json.dumps(deps), json.dumps(_parse_csv(args.touch)), verify,
             args.budget, args.parent, args.model, args.steps,
             json.dumps([{"n": i} for i in range(1, args.steps + 1)]),
             seq, now(), now()))
        db.event(tid, args.worker or "enqueuer", "enqueue",
                 f"deps={deps} touch={_parse_csv(args.touch)}")
        con.commit()
        print(tid)
        return 0
    finally:
        db.close()


def _do_claim(db: DB, worker: str, tid: str | None,
              types: list[str] | None, *,
              takeover: str | None = None, take_force: bool = False,
              reason: str = "") -> tuple[int, object]:
    """原子 claim 的核心事务。返回 (exit_code, payload)。"""
    con = db.con
    con.execute("BEGIN IMMEDIATE")
    # ── 人工接管（人知道旧会话已死；机器无法自己知道）──────────────────────────
    # 与 600s 自动回收的区别：这是"人开新会话时显式下的一个命令"，必须留痕；
    # 心跳尚新（<grace）时默认拒绝（防抢活人的任务），--force+reason 留痕担责。
    if takeover:
        tr = con.execute("SELECT * FROM tasks WHERE id=?", (takeover,)).fetchone()
        if not tr:
            con.rollback(); return 2, {"error": f"接管目标不存在 {takeover}"}
        if tr["status"] != "in_progress":
            con.rollback()
            return 2, {"error": f"接管目标状态={tr['status']}（仅 in_progress 可接管）"}
        grace = int(os.environ.get("TQ_TAKEOVER_GRACE", "120"))
        fresh = tr["heartbeat_at"] and \
            (time.time() - time.mktime(time.strptime(tr["heartbeat_at"],
                                                     "%Y-%m-%dT%H:%M:%S"))) < grace
        if fresh and not take_force:
            con.rollback()
            return 2, {"error": f"{takeover} 心跳仅 {tr['heartbeat_at']}，疑似仍在跑；"
                                f"确认旧会话已死后用 --takeover {takeover} --force --reason",
                       "claimed_by": tr["claimed_by"]}
        if take_force and not reason:
            con.rollback()
            return 2, {"error": "--force 接管必须给 --reason（留痕担责）"}
        con.execute(
            "UPDATE tasks SET status='pending',claimed_by=NULL,claimed_token=NULL,"
            "lease_expires=NULL WHERE id=?", (takeover,))
        db.event(takeover, worker, "manual_takeover",
                 f"from={tr['claimed_by']} force={take_force} reason={reason[:120]}")
        tid = takeover
    else:
        # 租约过期自动回收（wait/stale 分离教训：活锁不接管，只接管真过期）
        recycled = [r["id"] for r in con.execute(
            "UPDATE tasks SET status='pending',claimed_by=NULL,claimed_token=NULL,"
            "lease_expires=NULL,error=COALESCE(error,'')||? "
            "WHERE status='in_progress' AND lease_expires IS NOT NULL AND lease_expires < ? "
            "RETURNING id",
            (f"[{now()} lease 过期回收] ", now()))]
        for rid in recycled:
            db.event(rid, worker, "lease_recycled", "租约过期，claim 事务内回收")
    if tid:
        r = con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
        if not r:
            con.rollback(); return 2, {"error": f"任务不存在 {tid}"}
        if r["status"] != "pending":
            con.rollback(); return 2, {"error": f"任务状态={r['status']}，不可 claim"}
        deps = _jload(r["deps"], [])
        dep_status = {x["id"]: x["status"] for x in con.execute("SELECT id,status FROM tasks")}
        bad = [d for d in deps if dep_status.get(d) != "done"]
        if bad:
            con.rollback(); return 2, {"error": f"deps 未完成：{bad}"}
        held = [(x["id"], set(_jload(x["touch_set"], [])) & set(_jload(r["touch_set"], [])))
                for x in con.execute("SELECT * FROM tasks WHERE status='in_progress'")]
        blockers = [(i, sorted(s)) for i, s in held if s]
        if blockers:
            con.rollback(); return 2, {"error": "touch_set 冲突", "blocked_by": blockers}
        chosen = r
        conflicts: dict = {}
    else:
        chosen, conflicts = pick_candidate(db, types)
        if not chosen:
            con.rollback()
            if conflicts:
                return 2, {"error": "无可派任务：候选全部 touch_set 冲突",
                           "conflicts": {k: v for k, v in list(conflicts.items())[:10]}}
            return 1, {"error": "队列空或任务均未就绪"}
    secret = worker_register(worker)
    con.execute(
        "UPDATE tasks SET status='in_progress',claimed_by=?,claimed_token=?,"
        "lease_expires=?,heartbeat_at=?,attempts=attempts+1,updated_at=? WHERE id=?",
        (worker, secret, _lease_ts(), now(), now(), chosen["id"]))
    db.event(chosen["id"], worker, "claim", f"attempt={chosen['attempts']+1}")
    con.commit()
    return 0, dict(chosen)


def cmd_next(args) -> int:
    db = DB()
    try:
        code, payload = _do_claim(db, args.worker, args.id, _parse_csv(args.types),
                                  takeover=args.takeover, take_force=args.force_takeover,
                                  reason=args.reason or "")
        if code != 0:
            print(json.dumps(payload, ensure_ascii=False), file=sys.stderr)
            return code
        t = payload
        handoff = _jload(t.get("checkpoint"), {})
        out = {"task_id": t["id"], "type": t["type"], "goal": t["goal"],
               "payload_ref": t["payload_ref"], "attempts": t["attempts"] + 1,
               "steps_done": t["steps_done"], "steps_total": t["steps_total"],
               "handoff": handoff or None,
               "next_action": (handoff or {}).get("next_action"),
               "hint": ("从 handoff.steps_remaining 第一步继续；steps_done 的产物哈希"
                        "已在盘上核对，勿重做" if handoff else "全新任务，从 steps_remaining[0] 开始")}
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0
    finally:
        db.close()


cmd_claim = cmd_next  # claim = 不打印 handoff 提示的同一事务（CLI 层差异仅在输出）


def _load_owned(db: DB, tid: str, worker: str) -> tuple[Row | None, str | None]:
    r = db.con.execute("SELECT * FROM tasks WHERE id=?", (tid,)).fetchone()
    if not r:
        return None, "任务不存在"
    why = auth(db, r, worker)
    if why:
        return None, why
    return r, None


def cmd_heartbeat(args) -> int:
    db = DB()
    try:
        db.con.execute("BEGIN IMMEDIATE")
        r, why = _load_owned(db, args.task, args.worker)
        if why:
            db.con.rollback(); print(why, file=sys.stderr); return 2
        # 假活检测：与上一个指纹比对（checkpoint 内容）
        h = _jload(args.handoff_file and Path(args.handoff_file).read_text(encoding="utf-8"),
                   _jload(r["checkpoint"], {}))
        fp = cp_fingerprint_of(h)
        zombie = (fp == r["cp_fingerprint"] and bool(h.get("steps_done")))
        db.con.execute(
            "UPDATE tasks SET heartbeat_at=?,lease_expires=?,budget_used_calls=?,"
            "updated_at=? WHERE id=?",
            (now(), _lease_ts(), args.used, now(), args.task))
        db.event(args.task, args.worker,
                 "heartbeat_zombie" if zombie else "heartbeat",
                 f"fp={fp} budget={args.used}")
        db.con.commit()
        print(("ZOMBIE_SUSPECT fp 未变" if zombie else "alive") + f" lease+{LEASE_SECONDS}s")
        return 0
    finally:
        db.close()


def cmd_checkpoint(args) -> int:
    """关键步骤落盘：原子更新 handoff（被杀时最多丢一步的保证来源）。"""
    db = DB()
    try:
        db.con.execute("BEGIN IMMEDIATE")
        r, why = _load_owned(db, args.task, args.worker)
        if why:
            db.con.rollback(); print(why, file=sys.stderr); return 2
        h = json.loads(Path(args.handoff).read_text(encoding="utf-8"))
        errs = validate_handoff(h, for_yield=False)
        # checkpoint 允许 steps_remaining 暂时为空以外的不完整，但硬错误仍拒
        hard = [e for e in errs if not e.startswith("yield 时")]
        if hard and not args.force:
            db.con.rollback()
            print("[tq] checkpoint 质量不过：\n  - " + "\n  - ".join(hard), file=sys.stderr)
            return 2
        sd = h.get("steps_done") or []
        db.con.execute(
            "UPDATE tasks SET checkpoint=?,cp_fingerprint=?,steps_done=?,"
            "steps_remaining=?,handoff_path=?,budget_used_calls=?,heartbeat_at=?,"
            "lease_expires=?,updated_at=? WHERE id=?",
            (json.dumps(h, ensure_ascii=False), cp_fingerprint_of(h), len(sd),
             json.dumps(h.get("steps_remaining") or []), str(args.handoff),
             int(h.get("budget_used") or 0), now(), _lease_ts(), now(), args.task))
        db.event(args.task, args.worker, "checkpoint", f"steps_done={len(sd)}")
        db.con.commit()
        print(f"[tq] checkpoint 落盘 steps_done={len(sd)} fp={cp_fingerprint_of(h)}")
        return 0
    finally:
        db.close()


def cmd_yield(args) -> int:
    db = DB()
    try:
        con = db.con
        con.execute("BEGIN IMMEDIATE")
        r, why = _load_owned(db, args.task, args.worker)
        if why:
            con.rollback(); print(why, file=sys.stderr); return 2
        h = json.loads(Path(args.handoff).read_text(encoding="utf-8"))
        errs = validate_handoff(h, for_yield=True)
        if errs:
            con.rollback()
            print("[tq] yield 被拒（fail-closed，废交接物不许让出）：\n  - "
                  + "\n  - ".join(errs), file=sys.stderr)
            return 2
        remaining = h.get("steps_remaining") or []
        budget_left = max(0, int(r["budget_calls"]) - int(h.get("budget_used") or 0))
        if budget_left >= YIELD_BUDGET_LEFT and not args.force:
            con.rollback()
            print(f"[tq] 预算尚余 {budget_left}（<{YIELD_BUDGET_LEFT} 才允许 yield），"
                  "先继续做", file=sys.stderr)
            return 2
        # 切子任务：默认 1 个续跑子任务（携带全部剩余步骤）；payload 显式分组时最多 MAX_CHILDREN
        groups = h.get("step_groups")
        if isinstance(groups, list) and groups:
            groups = groups[:MAX_CHILDREN]
        else:
            groups = [{"steps": remaining, "touch": _jload(r["touch_set"], [])}]
        if any(len(g.get("steps") or []) == 0 for g in groups):
            con.rollback(); print("[tq] 切出空子任务，拒绝（碎片防护）", file=sys.stderr); return 2
        per_child_budget = max(MIN_CHILD_BUDGET, budget_left // max(len(groups), 1))
        child_ids: list[str] = []
        seq0 = con.execute("SELECT COALESCE(MAX(enqueued_seq),0) FROM tasks").fetchone()[0]
        prev = None
        for i, g in enumerate(groups):
            cid = f"{r['id']}.c{i+1}"
            if con.execute("SELECT 1 FROM tasks WHERE id=?", (cid,)).fetchone():
                con.rollback(); print(f"[tq] 子任务已存在：{cid}", file=sys.stderr); return 2
            cdeps = _parse_csv(args.child_deps)
            if prev:
                cdeps.append(prev)
            h2 = dict(h)
            h2["steps_remaining"] = g["steps"]
            h2["goal"] = f"[续] {h.get('goal','')}"
            hp = DB_PATH.parent / f"{cid}.handoff.json"
            hp.write_text(json.dumps(h2, ensure_ascii=False, indent=1), encoding="utf-8")
            seq0 += 1
            con.execute(
                "INSERT INTO tasks(id,type,payload_ref,goal,status,priority,deps,touch_set,"
                "verify_cmd,budget_calls,parent_task,produced_by_model,steps_total,"
                "steps_remaining,handoff_path,enqueued_seq,created_at,updated_at)"
                " VALUES(?,?,?,?, 'pending',?,?,?,?,?,?,?,?,?,?,?,?,?)",
                (cid, r["type"], r["payload_ref"], h2["goal"], r["priority"],
                 json.dumps(cdeps), json.dumps(g.get("touch") or _jload(r["touch_set"], [])),
                 r["verify_cmd"], per_child_budget, r["id"], r["produced_by_model"],
                 len(g["steps"]), json.dumps(g["steps"]), str(hp), seq0, now(), now()))
            db.event(cid, args.worker, "enqueue_child", f"parent={r['id']}")
            child_ids.append(cid)
            prev = cid
        con.execute(
            "UPDATE tasks SET status='yielded',handoff_path=?,checkpoint=?,"
            "cp_fingerprint=?,steps_done=?,steps_remaining='[]',claimed_by=NULL,"
            "claimed_token=NULL,lease_expires=NULL,heartbeat_at=?,budget_used_calls=?,"
            "result_ref=?,updated_at=? WHERE id=?",
            (str(args.handoff), json.dumps(h, ensure_ascii=False), cp_fingerprint_of(h),
             len(h.get("steps_done") or []), now(), int(h.get("budget_used") or 0),
             child_ids[0], now(), args.task))
        db.event(args.task, args.worker, "yield",
                 f"children={child_ids} budget_used={h.get('budget_used')}")
        con.commit()
        print(json.dumps({"yielded": args.task, "children": child_ids}, ensure_ascii=False))
        return 0
    finally:
        db.close()


def cmd_complete(args) -> int:
    db = DB()
    try:
        con = db.con
        con.execute("BEGIN IMMEDIATE")
        r, why = _load_owned(db, args.task, args.worker)
        if why:
            con.rollback(); print(why, file=sys.stderr); return 2
        if r["status"] != "in_progress":
            con.rollback(); print(f"状态={r['status']}，不可 complete", file=sys.stderr); return 2
        verify = args.verify_cmd or r["verify_cmd"]
        if not verify:
            if not args.result_ref:
                con.rollback()
                print("[tq] 无 verify_cmd 的任务 complete 必须 --result-ref（人审线索，不得自证 done）",
                      file=sys.stderr)
                return 2
            verify_hash = "HUMAN_REVIEW_REQUIRED"
            rc, out, err = 0, "", ""
        else:
            t0 = time.perf_counter()
            p = subprocess.run(verify, shell=True, cwd=str(ANCHOR_ROOT),
                               capture_output=True, text=True, errors="replace",
                               timeout=args.timeout)
            dt = time.perf_counter() - t0
            rc, out, err = p.returncode, p.stdout, p.stderr
            verify_hash = hashlib.sha256((out + err).encode("utf-8", "replace")).hexdigest()[:16]
            verify_hash = f"{verify_hash}@{dt:.2f}s"
        if rc != 0:
            attempts = r["attempts"] + 0  # claim 时已 +1，失败再 +1
            con.execute(
                "UPDATE tasks SET attempts=attempts+1,error=?,updated_at=? WHERE id=?",
                (f"verify rc={rc}: {err[-300:] or out[-300:]}", now(), args.task))
            db.event(args.task, args.worker, "verify_failed", f"rc={rc} {verify_hash}")
            con.commit()
            if r["attempts"] + 1 > MAX_ATTEMPTS:
                con.execute("UPDATE tasks SET status='blocked',updated_at=? WHERE id=?",
                            (now(), args.task))
                db.event(args.task, args.worker, "blocked", "verify 反复失败超上限")
                con.commit()
                print(f"[tq] verify 失败且 attempts>{MAX_ATTEMPTS} → blocked", file=sys.stderr)
                return 1
            con.execute("UPDATE tasks SET status='pending',claimed_by=NULL,claimed_token=NULL,"
                        "lease_expires=NULL WHERE id=?", (args.task,))
            db.event(args.task, args.worker, "requeue", "verify 失败回 pending 重试")
            con.commit()
            print(f"[tq] verify 失败 rc={rc}：回 pending 重试（attempts 将达 "
                  f"{r['attempts']+1}/{MAX_ATTEMPTS}）", file=sys.stderr)
            return 1
        # touch_set 事后审计：git 视角改动超出声明集 → 记事件（不否决定案，但留痕）
        undeclared = _touch_audit(r)
        con.execute(
            "UPDATE tasks SET status='done',result_ref=?,verify_hash=?,error='',"
            "lease_expires=NULL,updated_at=? WHERE id=?",
            (args.result_ref or r["result_ref"], verify_hash, now(), args.task))
        db.event(args.task, args.worker, "done",
                 f"verify={verify_hash} undeclared={undeclared}")
        # 父任务回卷：续跑子任务 done → yielded 父任务一并 done
        parent = r["parent_task"]
        if parent:
            pr = con.execute("SELECT * FROM tasks WHERE id=?", (parent,)).fetchone()
            if pr and pr["status"] == "yielded":
                con.execute("UPDATE tasks SET status='done',updated_at=? WHERE id=?",
                            (now(), parent))
                db.event(parent, args.worker, "done_rollup", f"via child {args.task}")
        con.commit()
        print(json.dumps({"done": args.task, "verify_hash": verify_hash,
                          "undeclared_touch": undeclared}, ensure_ascii=False))
        return 0
    finally:
        db.close()


def _touch_audit(r: Row) -> list[str]:
    """完成后对比声明 touch_set 与真实改动（git 仓库用 git status；沙箱用声明目录快照）。"""
    declared = set(_jload(r["touch_set"], []))
    try:
        p = subprocess.run("git status --porcelain", shell=True, cwd=str(ANCHOR_ROOT),
                           capture_output=True, text=True, errors="replace", timeout=10)
        changed = {ln[3:].split(" -> ")[-1].strip() for ln in p.stdout.splitlines() if ln.strip()}
        return sorted(f for f in changed if f.endswith((".py", ".md", ".cpp", ".json"))
                      and f not in declared and "/data/" not in f and not f.startswith("_arch_v"))
    except Exception:
        return []


def cmd_fail(args) -> int:
    db = DB()
    try:
        db.con.execute("BEGIN IMMEDIATE")
        r, why = _load_owned(db, args.task, args.worker)
        if why:
            db.con.rollback(); print(why, file=sys.stderr); return 2
        db.con.execute(
            "UPDATE tasks SET status='failed',error=?,updated_at=? WHERE id=?",
            (args.error[:500], now(), args.task))
        db.event(args.task, args.worker, "fail", args.error[:300])
        db.con.commit()
        print(f"[tq] {args.task} failed")
        return 0
    finally:
        db.close()


def cmd_blocked(args) -> int:
    db = DB()
    try:
        db.con.execute("BEGIN IMMEDIATE")
        r = db.con.execute("SELECT * FROM tasks WHERE id=?", (args.task,)).fetchone()
        if not r:
            db.con.rollback(); print("任务不存在", file=sys.stderr); return 2
        if r["claimed_by"] and r["claimed_by"] != args.worker:
            db.con.rollback()
            print(f"任务由 {r['claimed_by']} 持有，{args.worker} 无权 blocked", file=sys.stderr)
            return 2
        db.con.execute(
            "UPDATE tasks SET status='blocked',error=?,claimed_by=NULL,claimed_token=NULL,"
            "lease_expires=NULL,updated_at=? WHERE id=?",
            (args.reason[:500], now(), args.task))
        db.event(args.task, args.worker or r["claimed_by"] or "?", "blocked", args.reason[:300])
        db.con.commit()
        print(f"[tq] {args.task} blocked：{args.reason}")
        return 0
    finally:
        db.close()


def cmd_list(args) -> int:
    db = DB()
    try:
        q = "SELECT id,type,status,priority,claimed_by,attempts,steps_done,steps_total,parent_task FROM tasks"
        rows = db.con.execute(q).fetchall()
        if args.json:
            print(json.dumps([dict(r) for r in rows], ensure_ascii=False, indent=1))
        else:
            for r in rows:
                print(f"{r['id']:<22} {r['type']:<14} {r['status']:<11} p{r['priority']:<4} "
                      f"{str(r['claimed_by']):<10} try{r['attempts']} "
                      f"step {r['steps_done']}/{r['steps_total']}"
                      + (f" ←{r['parent_task']}" if r["parent_task"] else ""))
        return 0
    finally:
        db.close()


def cmd_doctor(args) -> int:
    """假活/僵尸巡检：心跳在但指纹长期不变；租约过期清单。"""
    db = DB()
    try:
        out = []
        for r in db.con.execute("SELECT * FROM tasks WHERE status='in_progress'"):
            item = {"id": r["id"], "claimed_by": r["claimed_by"],
                    "heartbeat_at": r["heartbeat_at"], "fp": r["cp_fingerprint"]}
            if r["lease_expires"] and r["lease_expires"] < now():
                item["note"] = "lease_expired（下次 next 自动回收）"
            out.append(item)
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0
    finally:
        db.close()


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(description="534 task_queue 原型")
    sub = ap.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("init"); s.add_argument("--worker", default="init"); s.set_defaults(fn=cmd_init)

    s = sub.add_parser("enqueue")
    s.add_argument("--type", required=True, choices=TASK_TYPES)
    s.add_argument("--id"); s.add_argument("--payload-ref", default="")
    s.add_argument("--goal", default=""); s.add_argument("--priority", type=int, default=100)
    s.add_argument("--deps", default=""); s.add_argument("--touch", default="")
    s.add_argument("--verify-cmd", default=None); s.add_argument("--budget", type=int, default=500)
    s.add_argument("--parent", default=None); s.add_argument("--model", default=None)
    s.add_argument("--steps", type=int, default=0); s.add_argument("--worker", default="enqueuer")
    s.set_defaults(fn=cmd_enqueue)

    def add_worker(p):
        p.add_argument("--worker", required=True)
        p.add_argument("--id", default=None, help="指定 claim 某任务（否则自动选）")
        p.add_argument("--types", default=None)

    s = sub.add_parser("next"); add_worker(s)
    s.add_argument("--takeover", default=None, help="人工接管已死会话持有的任务 id")
    s.add_argument("--force-takeover", action="store_true",
                   help="心跳尚新也接管（须 --reason，事件留痕）")
    s.add_argument("--reason", default="", help="接管/强制操作的留痕理由")
    s.set_defaults(fn=cmd_next)
    s = sub.add_parser("claim"); add_worker(s)
    s.add_argument("--takeover", default=None)
    s.add_argument("--force-takeover", action="store_true")
    s.add_argument("--reason", default="")
    s.set_defaults(fn=cmd_claim)

    s = sub.add_parser("heartbeat")
    s.add_argument("task"); s.add_argument("--worker", required=True)
    s.add_argument("--used", type=int, default=0); s.add_argument("--handoff-file", default=None)
    s.set_defaults(fn=cmd_heartbeat)

    s = sub.add_parser("checkpoint")
    s.add_argument("task"); s.add_argument("--worker", required=True)
    s.add_argument("--handoff", required=True); s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_checkpoint)

    s = sub.add_parser("yield")
    s.add_argument("task"); s.add_argument("--worker", required=True)
    s.add_argument("--handoff", required=True); s.add_argument("--force", action="store_true")
    s.add_argument("--child-deps", default="")
    s.set_defaults(fn=cmd_yield)

    s = sub.add_parser("complete")
    s.add_argument("task"); s.add_argument("--worker", required=True)
    s.add_argument("--result-ref", default=None); s.add_argument("--verify-cmd", default=None)
    s.add_argument("--timeout", type=int, default=900)
    s.set_defaults(fn=cmd_complete)
    s = sub.add_parser("done"); s.add_argument("task"); s.add_argument("--worker", required=True)
    s.add_argument("--result-ref", default=None); s.add_argument("--verify-cmd", default=None)
    s.add_argument("--timeout", type=int, default=900); s.set_defaults(fn=cmd_complete)

    s = sub.add_parser("fail")
    s.add_argument("task"); s.add_argument("--worker", required=True)
    s.add_argument("--error", required=True); s.set_defaults(fn=cmd_fail)

    s = sub.add_parser("blocked")
    s.add_argument("task"); s.add_argument("--worker", default="")
    s.add_argument("--reason", required=True); s.set_defaults(fn=cmd_blocked)

    s = sub.add_parser("list"); s.add_argument("--json", action="store_true"); s.set_defaults(fn=cmd_list)
    s = sub.add_parser("doctor"); s.set_defaults(fn=cmd_doctor)
    return ap


def main(argv: list[str] | None = None) -> int:
    a = build_parser().parse_args(argv)
    return a.fn(a)


if __name__ == "__main__":
    raise SystemExit(main())
