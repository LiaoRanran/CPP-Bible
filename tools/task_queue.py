#!/usr/bin/env python3
"""530 T7 · L2 调度最小骨架（task_queue）——"谁该干什么 / 干完没"。

与 `tools/task_state.py` 的**分工（勿混）**：
  - `task_state.py` = 长任务**进度笔记本**（一个任务内部走到哪一步）；
  - `task_queue.py` = **队列**（任务之间排队 / 认领 / 完成）。
v1 由人执行 `task_queue next` 手动派活，**不写自动 Supervisor Loop**（无数据支撑自动路由）。

零新依赖（标准库 sqlite3）；并发安全靠 `BEGIN IMMEDIATE` 原子事务 + WAL。

优先级方向（**唯一定义在此，勿在别处再猜**）：`priority` **数值小 = 优先级高**
（`ORDER BY priority ASC`），与仓库内 P0<P1<P2 的排序习惯一致。默认 100。

幂等键：`id = "<type>-<sha256(payload_ref)[:12]>"`（可用 `--id` 显式覆盖）；
同 type+payload_ref 重复 enqueue 只入队一次，第二次打印"已存在"并 exit 0。

状态机：`queued → claimed → done | failed | blocked`；stale 接管可 `claimed → queued`。
`heartbeat/done/fail/blocked` **必须由 claim 者本人执行**（`claimed_by` 一致），否则拒绝。

stale 接管：`claimed` 且 `heartbeat_at`（无则 `claimed_at`）超过 `STALE_AFTER_S`(600s)
⇒ 下次 claim 时回收：`attempts <= MAX_ATTEMPTS` 回 `queued`（**attempts 保留**），
`attempts > MAX_ATTEMPTS`(3) 直接 `blocked`（防无限重试）。

数据：`data/tasks/queue.db`（已 gitignore，不入库；与 task_state 的 `<id>.json` 同目录共存）。

建库/迁移（535 C1，**真并发缺陷修复**）：所有入口一律先 `migrate()`——PRAGMA 顺序必须是
`busy_timeout` **先于** `journal_mode=WAL`（关掉 WAL 要排它锁，此刻还没有锁等待预算），
建表 + 增量列 + `events` 表包在**一个** `BEGIN IMMEDIATE` 里，用 `PRAGMA user_version` 做版本门。
旧版（d976170）逐条 ALTER 各自自动提交时，第二个冷启动进程会读到"加列中途"的中间态 ⇒
两进程补同一列 ⇒ `duplicate column name`（沙箱实测冷启动 6/8 失败；修后 12/12 零失败）。
回退：`downgrade --yes`（逐列 `DROP COLUMN`，需 SQLite ≥ 3.35）。

用法：
  python tools/task_queue.py enqueue --type redteam --payload-ref docs/tasks/t1.md --priority 50
  python tools/task_queue.py next                       # 只读预览：下一个该派谁
  python tools/task_queue.py claim --worker liaoranran --types redteam
  python tools/task_queue.py heartbeat <id> --worker liaoranran
  python tools/task_queue.py done <id> --worker liaoranran --result-ref data/tasks/t1.out
  python tools/task_queue.py fail <id> --worker liaoranran --error "编译失败：见日志"
  python tools/task_queue.py blocked <id> --worker liaoranran --reason "缺 g++ 15.3"
  python tools/task_queue.py list [--status queued] [--json]
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import sqlite3
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "tasks" / "queue.db"

VERSION = "v1.0"
STALE_AFTER_S = 600      # heartbeat 超此秒数 ⇒ 视为 worker 已死，可被接管
MAX_ATTEMPTS = 3         # attempts > 此值 ⇒ 自动 blocked（防无限重试）
STATUSES = ("queued", "claimed", "done", "failed", "blocked")

# 表结构由 530 T7 规格钉定（勿加列：加列会让"结果引用/原因"这类字段出现多份真源）
DDL = """
CREATE TABLE IF NOT EXISTS tasks(
  id TEXT PRIMARY KEY,
  type TEXT NOT NULL,
  payload_ref TEXT NOT NULL,
  status TEXT NOT NULL,
  priority INTEGER NOT NULL DEFAULT 100,
  deps TEXT NOT NULL DEFAULT '[]',
  claimed_by TEXT, claimed_at TEXT, heartbeat_at TEXT,
  attempts INTEGER NOT NULL DEFAULT 0, result_ref TEXT, error TEXT,
  created_at TEXT NOT NULL, updated_at TEXT NOT NULL
);
CREATE INDEX IF NOT EXISTS idx_tasks_pick ON tasks(status, priority, created_at);
"""

# ── 535 C1 · 增量迁移（幂等 + 单事务 + 版本门）────────────────────────────────
# 列清单来源：535 批次 1 C2（touch_set/budget_calls/budget_used_calls/handoff_path/verify_cmd/
# parent_task/produced_by_model/steps_total/steps_done/checkpoint/cp_fingerprint/claimed_token）
# + C6 的 verify_hash（verify 留痕的唯一载体）+ goal（`--goal` 的落点；534 §2.2 要求 enqueue 接
# --goal，但 NEW_COLS 原型漏了列 ⇒ 施工补一列，见 _worklog_535.md 偏差表）。
SCHEMA_VERSION = 1
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
    "goal": "TEXT NOT NULL DEFAULT ''",
}
EVENTS_DDL = """
CREATE TABLE IF NOT EXISTS events(
  seq INTEGER PRIMARY KEY AUTOINCREMENT,
  task_id TEXT NOT NULL, at TEXT NOT NULL, actor TEXT NOT NULL,
  event TEXT NOT NULL, detail TEXT NOT NULL DEFAULT ''
);"""


def _now() -> str:
    return _dt.datetime.now().isoformat(timespec="seconds")


def _rollback(conn: sqlite3.Connection) -> None:
    """容错回滚：已 COMMIT / 事务已被自动结束时不抛（否则会**盖掉真正的报错**）。"""
    try:
        conn.execute("ROLLBACK")
    except sqlite3.Error:
        pass


def _cutoff(seconds: int = STALE_AFTER_S) -> str:
    return (_dt.datetime.now() - _dt.timedelta(seconds=seconds)).isoformat(timespec="seconds")


def _event(conn: sqlite3.Connection, task_id: str, actor: str, event: str,
           detail: str = "") -> None:
    """append-only 审计留痕（claim/takeover/checkpoint/yield/verify/done 全在此）。

    调用方必须已在事务内：事件与状态变更**同事务提交**，否则"改了状态但没留痕"。
    """
    conn.execute("INSERT INTO events(task_id,at,actor,event,detail) VALUES(?,?,?,?,?)",
                 (task_id, _now(), actor, event, detail[:1500]))


def _connect(db_path: Path | str | None = None) -> sqlite3.Connection:
    """独立连接（含 busy_timeout）；`isolation_level=None` ⇒ 事务显式写 `BEGIN IMMEDIATE`。"""
    p = Path(db_path) if db_path else DB_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(p), timeout=10.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    # 顺序铁律（535 C1）：busy_timeout 必须在 journal_mode 之前——切 WAL 要排它锁，
    # 排在后面时冷启动瞬间没有任何锁等待预算，直接 OperationalError（实测 6/8 失败）。
    conn.execute("PRAGMA busy_timeout=10000")
    conn.execute("PRAGMA journal_mode=WAL")
    return conn


def _exec_ddl(conn: sqlite3.Connection, script: str) -> None:
    """逐句执行 DDL（**不用 `executescript`**：它会在有未结事务时先隐式 COMMIT，
    从而把"整段迁移一个事务"拆开——那正是 C1 要消灭的中间态）。"""
    for stmt in (s.strip() for s in script.split(";")):
        if stmt:
            conn.execute(stmt)


def migrate(db_path: Path | str | None = None) -> int:
    """幂等迁移到 `SCHEMA_VERSION`；返回迁移前的版本号（供 pytest 断言）。

    单连接、单事务、版本门：
      ① `busy_timeout` → `journal_mode=WAL`（顺序见 `_connect`）；
      ② 建表 + 全部 ALTER + `events` 表 **同处一个 `BEGIN IMMEDIATE`**；
      ③ 第二个进程在锁上等待，见 `user_version` 已升 ⇒ 整段跳过（不再补同一列）。
    建表也并入本事务：消除"init 连接关闭 → 迁移连接开启"之间的缝隙（曾 1/10 复现 locked）。
    """
    p = Path(db_path) if db_path else DB_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(p), timeout=15.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA busy_timeout=15000")
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("BEGIN IMMEDIATE")
        ver = int(conn.execute("PRAGMA user_version").fetchone()[0])
        if ver < SCHEMA_VERSION:
            _exec_ddl(conn, DDL)
            have = {r["name"] for r in conn.execute("PRAGMA table_info(tasks)")}
            for col, decl in NEW_COLS.items():
                if col not in have:
                    conn.execute(f"ALTER TABLE tasks ADD COLUMN {col} {decl}")
            _exec_ddl(conn, EVENTS_DDL)
            conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
        conn.execute("COMMIT")
        return ver
    except BaseException:
        _rollback(conn)
        raise
    finally:
        conn.close()


def init(db_path: Path | str | None = None) -> None:
    """建表 + 迁移（幂等）。所有入口都会先调它，故无需人工 init（535 C1 起 = `migrate`）。"""
    migrate(db_path)


def downgrade(db_path: Path | str | None = None) -> dict[str, Any]:
    """回退迁移（535 C1 附带）：删 `events` 表 → 逐列 `DROP COLUMN` → `user_version` 归 0。

    前提：SQLite ≥ 3.35（`DROP COLUMN`）；不满足则**显式报错**（fail-closed，绝不静默跳过）。
    只回退**结构**，不删任务行（行里的新列数据随之消失，这是回退的定义）。
    """
    if sqlite3.sqlite_version_info < (3, 35, 0):
        raise SystemExit(f"[task_queue] downgrade 需 SQLite ≥ 3.35（当前 "
                         f"{sqlite3.sqlite_version}）：请用标准 12 步重建表")
    p = Path(db_path) if db_path else DB_PATH
    if not p.exists():
        raise SystemExit(f"[task_queue] 库不存在：{p}")
    conn = sqlite3.connect(str(p), timeout=15.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    try:
        conn.execute("PRAGMA busy_timeout=15000")
        conn.execute("BEGIN IMMEDIATE")
        have = {r["name"] for r in conn.execute("PRAGMA table_info(tasks)")}
        dropped = [c for c in NEW_COLS if c in have]
        conn.execute("DROP TABLE IF EXISTS events")
        for col in dropped:
            conn.execute(f"ALTER TABLE tasks DROP COLUMN {col}")
        conn.execute("PRAGMA user_version=0")
        conn.execute("COMMIT")
        return {"db": str(p), "dropped_columns": dropped, "user_version": 0}
    except BaseException:
        _rollback(conn)
        raise
    finally:
        conn.close()


def make_id(task_type: str, payload_ref: str) -> str:
    """幂等键：同 type + payload_ref ⇒ 同 id。"""
    h = hashlib.sha256(payload_ref.encode("utf-8")).hexdigest()[:12]
    return f"{task_type}-{h}"


def _as_row_dict(row: sqlite3.Row) -> dict[str, Any]:
    d = {k: row[k] for k in row.keys()}
    try:
        d["deps"] = json.loads(d.get("deps") or "[]")
    except json.JSONDecodeError:
        d["deps_raw"] = d.get("deps")
        d["deps"] = []
    return d


def _deps_done(conn: sqlite3.Connection, deps_json: str) -> tuple[bool, list[str]]:
    """(是否全部 done, 未满足的 dep 列表)。坏 JSON ⇒ 视为未满足（fail-closed，宁可挡住）。"""
    try:
        deps = json.loads(deps_json or "[]")
    except json.JSONDecodeError:
        return False, [f"<deps 非法 JSON: {deps_json!r}>"]
    if not isinstance(deps, list) or not deps:
        return (isinstance(deps, list), [])
    q = ",".join("?" * len(deps))
    got = {r["id"]: r["status"] for r in
           conn.execute(f"SELECT id, status FROM tasks WHERE id IN ({q})", list(deps))}
    pending = [d for d in deps if got.get(d) != "done"]
    return (not pending), pending


def _stale_ids(conn: sqlite3.Connection) -> list[str]:
    return [r["id"] for r in conn.execute(
        "SELECT id FROM tasks WHERE status='claimed' "
        "AND COALESCE(heartbeat_at, claimed_at) < ?", (_cutoff(),))]


def _block(conn: sqlite3.Connection, tid: str, why: str, now: str) -> None:
    """判 blocked 的**唯一落点**（stale 接管与 claim 挑选用同一句 SQL，防两处口径漂移）。"""
    conn.execute("UPDATE tasks SET status='blocked', error=?, updated_at=? WHERE id=?",
                 (why, now, tid))


def _sweep_stale(conn: sqlite3.Connection, now: str) -> list[str]:
    """回收 stale claimed：attempts>MAX ⇒ blocked，否则回 queued（attempts 保留）。

    调用方必须已在 `BEGIN IMMEDIATE` 事务内（否则两进程会重复回收同一行）。
    """
    moved: list[str] = []
    for tid in _stale_ids(conn):
        row = conn.execute("SELECT attempts FROM tasks WHERE id=?", (tid,)).fetchone()
        att = int(row["attempts"] or 0)
        if att > MAX_ATTEMPTS:
            _block(conn, tid, f"stale 接管时 attempts={att} > {MAX_ATTEMPTS}（防无限重试）", now)
        else:
            conn.execute(
                "UPDATE tasks SET status='queued', claimed_by=NULL, heartbeat_at=NULL, "
                "updated_at=? WHERE id=?", (now, tid))
        moved.append(tid)
    return moved


def _pick(conn: sqlite3.Connection, types: list[str] | None,
          now: str) -> sqlite3.Row | None:
    """挑一个可领任务（**只读**，不改状态，除 attempts 超限就地判 blocked 外）。

    顺序：deps 全 done 的最高优先级 queued（priority 小者先）。
    """
    sql = "SELECT * FROM tasks WHERE status='queued'"
    args: list[Any] = []
    if types:
        sql += f" AND type IN ({','.join('?' * len(types))})"
        args += types
    sql += " ORDER BY priority ASC, created_at ASC, id ASC"
    for row in conn.execute(sql, args).fetchall():
        if int(row["attempts"] or 0) > MAX_ATTEMPTS:
            _block(conn, row["id"],
                   f"attempts={row['attempts']} > {MAX_ATTEMPTS}（防无限重试）", now)
            continue
        ok, _pending = _deps_done(conn, row["deps"])
        if ok:
            return row
    return None


# ── 写操作（皆 `BEGIN IMMEDIATE` 原子） ──────────────────────────────────────


def enqueue(task_type: str, payload_ref: str, priority: int = 100,
            deps: list[str] | None = None, task_id: str | None = None,
            db_path: Path | str | None = None) -> dict[str, Any]:
    """入队（幂等）。已存在 ⇒ {"created": False}，不报错（可安全重跑）。"""
    if not task_type or not payload_ref:
        raise SystemExit("[task_queue] --type 与 --payload-ref 必填")
    init(db_path)
    tid = task_id or make_id(task_type, payload_ref)
    deps = list(deps or [])
    conn = _connect(db_path)
    try:
        conn.execute("BEGIN IMMEDIATE")
        if conn.execute("SELECT id FROM tasks WHERE id=?", (tid,)).fetchone():
            conn.execute("COMMIT")
            return {"id": tid, "created": False, "reason": "同 id 已存在（幂等）"}
        # 依赖不存在 ⇒ 可见提示（不静默：缺依赖的任务会永远 claim 不到）
        missing = [d for d in deps if not conn.execute(
            "SELECT 1 FROM tasks WHERE id=?", (d,)).fetchone()]
        now = _now()
        conn.execute(
            "INSERT INTO tasks(id,type,payload_ref,status,priority,deps,attempts,"
            "created_at,updated_at) VALUES(?,?,?,'queued',?,?,0,?,?)",
            (tid, task_type, payload_ref, int(priority),
             json.dumps(deps, ensure_ascii=False), now, now))
        conn.execute("COMMIT")
        return {"id": tid, "created": True, "deps_missing": missing}
    except BaseException:
        _rollback(conn)
        raise
    finally:
        conn.close()


def claim(worker: str, types: list[str] | None = None,
          db_path: Path | str | None = None) -> dict[str, Any]:
    """原子领走一个任务：deps 全 done 的最高优先级 queued。

    返回 {"claimed": <任务 dict 或 None>, "taken_over": [回收的 id]}。
    """
    if not worker:
        raise SystemExit("[task_queue] --worker 必填")
    init(db_path)
    conn = _connect(db_path)
    try:
        conn.execute("BEGIN IMMEDIATE")
        now = _now()
        moved = _sweep_stale(conn, now)
        row = _pick(conn, types, now)
        if row is None:
            conn.execute("COMMIT")
            return {"claimed": None, "taken_over": moved}
        # 显式 `AND status='queued'`：即便事务语义有变，也不可能重复认领同一行
        conn.execute(
            "UPDATE tasks SET status='claimed', claimed_by=?, claimed_at=?, heartbeat_at=?, "
            "attempts=attempts+1, updated_at=? WHERE id=? AND status='queued'",
            (worker, now, now, now, row["id"]))
        out = _as_row_dict(
            conn.execute("SELECT * FROM tasks WHERE id=?", (row["id"],)).fetchone())
        conn.execute("COMMIT")
        return {"claimed": out, "taken_over": moved}
    except BaseException:
        _rollback(conn)
        raise
    finally:
        conn.close()


def next_task(types: list[str] | None = None,
              db_path: Path | str | None = None) -> dict[str, Any]:
    """`claim` 的**只读预览**：不改任何状态（含不回收 stale，但把 stale 视为可接管候选）。"""
    init(db_path)
    conn = _connect(db_path)
    try:
        stale = set(_stale_ids(conn))
        sql = "SELECT * FROM tasks WHERE status IN ('queued','claimed')"
        args: list[Any] = []
        if types:
            sql += f" AND type IN ({','.join('?' * len(types))})"
            args += types
        sql += " ORDER BY priority ASC, created_at ASC, id ASC"
        pending_deps: list[dict[str, Any]] = []
        for row in conn.execute(sql, args).fetchall():
            if row["status"] == "claimed" and row["id"] not in stale:
                continue
            if int(row["attempts"] or 0) > MAX_ATTEMPTS:
                continue
            ok, pending = _deps_done(conn, row["deps"])
            if not ok:
                pending_deps.append({"id": row["id"], "pending": pending})
                continue
            out = _as_row_dict(row)
            out["would_take_over"] = row["id"] in stale
            return {"next": out}
        return {"next": None, "stale_claimed": sorted(stale),
                "blocked_by_deps": pending_deps}
    finally:
        conn.close()


def _worker_update(task_id: str, worker: str, action: str,
                   result_ref: str | None = None, error: str | None = None,
                   db_path: Path | str | None = None) -> dict[str, Any]:
    """heartbeat/done/fail/blocked 的**公共入口**：只允许 claim 者本人，且必为 claimed 态。

    非 claim 者一律 `SystemExit`（exit 1）——这是"谁干的谁签收"的单点，别在别处再写一遍。
    """
    if not worker:
        raise SystemExit("[task_queue] --worker 必填")
    init(db_path)
    conn = _connect(db_path)
    try:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if row is None:
            _rollback(conn)
            raise SystemExit(f"[task_queue] 无此任务：{task_id}")
        if row["status"] != "claimed":
            cur = row["status"]
            _rollback(conn)
            raise SystemExit(f"[task_queue] {task_id} 当前状态 {cur}，非 claimed ⇒ 拒绝 {action}")
        if row["claimed_by"] != worker:
            owner = row["claimed_by"]
            _rollback(conn)
            raise SystemExit(
                f"[task_queue] 拒绝 {action}：{task_id} 由 {owner!r} 认领，非 {worker!r}")
        now = _now()
        if action == "heartbeat":
            conn.execute("UPDATE tasks SET heartbeat_at=?, updated_at=? WHERE id=?",
                         (now, now, task_id))
        elif action == "done":
            conn.execute("UPDATE tasks SET status='done', result_ref=?, heartbeat_at=?, "
                         "updated_at=? WHERE id=?", (result_ref, now, now, task_id))
        elif action == "fail":
            conn.execute("UPDATE tasks SET status='failed', error=?, updated_at=? WHERE id=?",
                         (error, now, task_id))
        elif action == "blocked":
            # 无 reason 列（表结构钉定）⇒ 原因的**唯一载体**是 error 列
            conn.execute("UPDATE tasks SET status='blocked', error=?, updated_at=? WHERE id=?",
                         (error, now, task_id))
        else:
            _rollback(conn)
            raise SystemExit(f"[task_queue] 未知 action：{action}")
        out = _as_row_dict(
            conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone())
        conn.execute("COMMIT")
        return out
    except BaseException:
        _rollback(conn)
        raise
    finally:
        conn.close()


def heartbeat(task_id: str, worker: str, db_path: Path | str | None = None) -> dict[str, Any]:
    return _worker_update(task_id, worker, "heartbeat", db_path=db_path)


def done(task_id: str, worker: str, result_ref: str | None = None,
         db_path: Path | str | None = None) -> dict[str, Any]:
    return _worker_update(task_id, worker, "done", result_ref=result_ref, db_path=db_path)


def fail(task_id: str, worker: str, error: str | None = None,
         db_path: Path | str | None = None) -> dict[str, Any]:
    return _worker_update(task_id, worker, "fail", error=error, db_path=db_path)


def blocked(task_id: str, worker: str, reason: str | None = None,
            db_path: Path | str | None = None) -> dict[str, Any]:
    return _worker_update(task_id, worker, "blocked", error=reason, db_path=db_path)


def list_tasks(status: str | None = None, type_filter: str | None = None,
               db_path: Path | str | None = None) -> list[dict[str, Any]]:
    """按优先级列出任务（只读）。空库/空结果 ⇒ 空列表（不崩）。"""
    init(db_path)
    conn = _connect(db_path)
    try:
        sql = "SELECT * FROM tasks"
        args: list[Any] = []
        where = []
        if status:
            where.append("status=?")
            args.append(status)
        if type_filter:
            where.append("type=?")
            args.append(type_filter)
        if where:
            sql += " WHERE " + " AND ".join(where)
        sql += " ORDER BY priority ASC, created_at ASC, id ASC"
        return [_as_row_dict(r) for r in conn.execute(sql, args).fetchall()]
    finally:
        conn.close()


def _row_line(d: dict[str, Any]) -> str:
    return (f"  {d['id']:<28}{d['type']:<16}{d['status']:<9}"
            f"p{d['priority']:<5}{'by=' + str(d['claimed_by']):<20}"
            f"att={d['attempts']:<4}deps={d['deps']}")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="L2 调度最小骨架（530 T7）")
    # `--json`/`--db` 同时挂主解析器与各子命令（T6 同款坑：只有主解析器时
    # 放在子命令之后会 unrecognized arguments）。子命令侧 default=SUPPRESS，
    # 免其默认值覆写主解析器已解析出的值。
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--json", action="store_true", default=argparse.SUPPRESS)
    common.add_argument("--db", default=argparse.SUPPRESS)
    ap.add_argument("--json", action="store_true", help="机器可读 JSON 输出")
    ap.add_argument("--db", default=None, help="queue.db 路径（默认 data/tasks/queue.db）")
    sub = ap.add_subparsers(dest="cmd", required=True)

    en = sub.add_parser("enqueue", parents=[common])
    en.add_argument("--type", required=True)
    en.add_argument("--payload-ref", required=True)
    en.add_argument("--priority", type=int, default=100)
    en.add_argument("--deps", default="")
    en.add_argument("--id", default=None)

    cl = sub.add_parser("claim", parents=[common])
    cl.add_argument("--worker", required=True)
    cl.add_argument("--types", default="")

    for name in ("heartbeat", "done", "fail", "blocked"):
        p = sub.add_parser(name, parents=[common])
        p.add_argument("id")
        p.add_argument("--worker", required=True)
        if name == "done":
            p.add_argument("--result-ref", default=None)
        elif name in ("fail", "blocked"):
            p.add_argument("--error" if name == "fail" else "--reason", default=None)

    ls = sub.add_parser("list", parents=[common])
    ls.add_argument("--status", default=None, choices=STATUSES)
    ls.add_argument("--type", dest="type_filter", default=None)
    sub.add_parser("next", parents=[common])
    sub.add_parser("init", parents=[common])
    dg = sub.add_parser("downgrade", parents=[common])
    dg.add_argument("--yes", action="store_true", help="确认执行回退（缺此参数一律拒绝）")
    a = ap.parse_args(argv)
    db = a.db
    types = [t for t in (getattr(a, "types", "") or "").split(",") if t]

    if a.cmd == "init":
        init(db)
        print(f"[task_queue] {VERSION} 已建表：{db or DB_PATH}")
        return 0
    if a.cmd == "downgrade":
        if not a.yes:
            print("[task_queue] 回退迁移会删掉增量列与 events 表；确认请加 --yes",
                  file=sys.stderr)
            return 2
        r = downgrade(db)
        print(f"[task_queue] 已回退到 user_version=0：{r['db']}")
        print(f"[task_queue] 删除列 {len(r['dropped_columns'])}：{r['dropped_columns']}")
        return 0
    if a.cmd == "enqueue":
        deps = [d for d in (a.deps or "").split(",") if d]
        r = enqueue(a.type, a.payload_ref, a.priority, deps, a.id, db)
        if a.json:
            print(json.dumps(r, ensure_ascii=False))
        elif r["created"]:
            print(f"[task_queue] 已入队 {r['id']}")
        else:
            print(f"[task_queue] 已存在 {r['id']}（幂等，未重复入队）")
        if r.get("deps_missing"):
            print(f"[task_queue] ⚠ 依赖尚不存在：{r['deps_missing']}"
                  f"（该任务在它们 done 前 claim 不到）", file=sys.stderr)
        return 0
    if a.cmd == "claim":
        r = claim(a.worker, types, db)
        if a.json:
            print(json.dumps(r, ensure_ascii=False))
        elif r["claimed"]:
            c = r["claimed"]
            print(f"[task_queue] {a.worker} 领到 {c['id']}（{c['type']}，"
                  f"attempts={c['attempts']}）payload={c['payload_ref']}")
        else:
            print(f"[task_queue] 无可领任务（{a.worker}）")
        if r["taken_over"]:
            print(f"[task_queue] 回收 stale：{r['taken_over']}", file=sys.stderr)
        return 0
    if a.cmd == "next":
        r = next_task(types, db)
        if a.json:
            print(json.dumps(r, ensure_ascii=False))
        elif r["next"]:
            n = r["next"]
            print(f"[task_queue] 下一个该派：{n['id']}（{n['type']}，p{n['priority']}，"
                  f"attempts={n['attempts']}）"
                  f"{' ⚠ 接管 stale' if n.get('would_take_over') else ''}")
        else:
            print("[task_queue] 无可派任务")
        if r.get("blocked_by_deps"):
            print(f"[task_queue] 等依赖：{r['blocked_by_deps']}", file=sys.stderr)
        return 0
    if a.cmd in ("heartbeat", "done", "fail", "blocked"):
        row = _worker_update(a.id, a.worker, a.cmd,
                            result_ref=getattr(a, "result_ref", None),
                            error=getattr(a, "error", None) or getattr(a, "reason", None),
                            db_path=db)
        print(json.dumps({k: row[k] for k in ("id", "status", "claimed_by", "attempts",
                                              "result_ref", "error", "updated_at")},
                         ensure_ascii=False))
        return 0
    if a.cmd == "list":
        rows = list_tasks(a.status, a.type_filter, db)
        if a.json:
            print(json.dumps({"count": len(rows), "tasks": rows}, ensure_ascii=False))
        else:
            print(f"[task_queue] {len(rows)} 条（priority 小者优先）")
            for d in rows:
                print(_row_line(d))
        return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main())


