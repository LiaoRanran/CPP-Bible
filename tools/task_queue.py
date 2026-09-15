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
`busy_timeout` **先于** `journal_mode=WAL`（切 WAL 要排它锁），建表 + 增量列 + `events` 表包在
**一个** `BEGIN IMMEDIATE` 里，用 `PRAGMA user_version` 做版本门。
旧版（d976170）逐条 ALTER 各自自动提交时，第二个冷启动进程会读到"加列中途"的中间态 ⇒
两进程补同一列 ⇒ `duplicate column name`（沙箱实测冷启动 6/8 失败）。
**实测加码（534 归因不完整）**：光调 PRAGMA 顺序不够——`PRAGMA journal_mode` 的模式切换路径
**不走 busy handler**，busy_timeout 对它无效，仍会偶发 `database is locked`；故 `_set_wal()`
显式退避重试（已是 WAL 则直接返回）。修后冷启动并发 pytest 12/12 稳定零失败。
回退：`downgrade --yes`（逐列 `DROP COLUMN`，需 SQLite ≥ 3.35）。

用法：
  python tools/task_queue.py enqueue --type redteam --payload-ref docs/tasks/t1.md --priority 50
  python tools/task_queue.py enqueue --type atom_produce --payload-ref atoms/x.md \
      --touch Examples/atoms/x.cpp --verify-cmd "replay --card atoms/x.md" --steps 4 --goal "..."
  python tools/task_queue.py next                       # 只读预览：下一个该派谁
  python tools/task_queue.py claim --worker liaoranran --types redteam
  python tools/task_queue.py claim --worker b --takeover <id> --force --reason "旧会话被 kill"
  python tools/task_queue.py checkpoint <id> --worker liaoranran --handoff data/tasks/<id>.handoff.json
  python tools/task_queue.py yield <id> --worker liaoranran --handoff data/tasks/<id>.handoff.json
  python tools/task_queue.py heartbeat <id> --worker liaoranran
  python tools/task_queue.py done <id> --worker liaoranran --result-ref data/tasks/t1.out
  python tools/task_queue.py fail <id> --worker liaoranran --error "编译失败：见日志"
  python tools/task_queue.py blocked <id> --worker liaoranran --reason "缺 g++ 15.3"
  python tools/task_queue.py list [--status queued] [--json]

退出码（**两类分开**，脚本可只对后者特判）：
  0 = 成功；1 = d976170 既有拒绝路径（状态/所有权/参数/无此任务）；
  **2 = 新增 fail-closed 门**：deps 环、handoff 质量不过、complete 缺 verify_cmd 又缺
  result-ref、心跳新鲜时的软 takeover（见 535 C2/C5/C6）。
"""
from __future__ import annotations

import argparse
import datetime as _dt
import hashlib
import json
import os
import secrets
import socket
import sqlite3
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent.parent
DB_PATH = ROOT / "data" / "tasks" / "queue.db"
# 锚根：handoff 里的相对路径、verify_cmd 的工作目录、touch 审计的 git 根。
# 独立全局量（不直接用 ROOT）是为了让 pytest 能把它指到 tmp 沙箱，不碰真实仓库。
ANCHOR_ROOT = ROOT

VERSION = "v1.0"
STALE_AFTER_S = 600      # heartbeat 超此秒数 ⇒ 视为 worker 已死，可被接管
MAX_ATTEMPTS = 3         # attempts > 此值 ⇒ 自动 blocked（防无限重试）
YIELD_BUDGET_LEFT = 100  # 预算剩余 ≥ 此值 ⇒ **不许逃**（yield 需 --force 才放行）
MAX_CHILDREN = 4         # 单次 yield 最多切几个子任务（防碎片）
MIN_CHILD_BUDGET = 80    # 每个子任务的预算下限（防"切到没法干活"）
LEASE_GRACE_S = 120      # 心跳新鲜宽限：此窗口内裸 claim/takeover 都拿不到活（见 C5）
STATUSES = ("queued", "claimed", "done", "failed", "blocked", "yielded")
TRUST_LEVELS = ("L1", "L2", "L3")   # handoff verified_facts 的信任三级（见 validate_handoff）

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


def _set_wal(conn: sqlite3.Connection, retries: int = 10) -> None:
    """切 WAL（幂等 + **显式重试**）。调用前必须先设 busy_timeout。

    为什么必须自己重试（535 C1 实测挖到的更深一层坑）：`PRAGMA journal_mode=WAL` 需要排它锁，
    而 SQLite 在**模式切换**这条路径上**不调用 busy handler**（切换要原子完成、不能半路重试）
    ⇒ busy_timeout 对它**完全无效**。把 busy_timeout 排到前面（534/沙箱的归因）是必要的，
    但**不充分**：两个进程同时冷启动建库时仍会直接 `database is locked`（在全量 pytest 里
    实测偶发命中，12 轮里出现 1 次）。故这里显式退避重试；已是 WAL 的连接直接返回（不切换）。
    """
    try:
        if str(conn.execute("PRAGMA journal_mode").fetchone()[0]).lower() == "wal":
            return
    except sqlite3.Error:
        pass
    for i in range(retries):
        try:
            conn.execute("PRAGMA journal_mode=WAL")
            return
        except sqlite3.OperationalError:
            if i == retries - 1:
                raise
            time.sleep(0.05 * (i + 1))


def _connect(db_path: Path | str | None = None) -> sqlite3.Connection:
    """独立连接（含 busy_timeout）；`isolation_level=None` ⇒ 事务显式写 `BEGIN IMMEDIATE`。"""
    p = Path(db_path) if db_path else DB_PATH
    p.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(p), timeout=10.0, isolation_level=None)
    conn.row_factory = sqlite3.Row
    # 顺序：busy_timeout 先于 journal_mode（切 WAL 要排它锁，先有锁等待预算；见 _set_wal）
    conn.execute("PRAGMA busy_timeout=10000")
    _set_wal(conn)
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
        _set_wal(conn)
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


def _jload(s: str | None, default: Any) -> Any:
    """容错 JSON 读（供 deps/touch_set/checkpoint 这类列使用；坏值 ⇒ default）。"""
    try:
        return json.loads(s) if s else default
    except json.JSONDecodeError:
        return default


def _has_cycle(conn: sqlite3.Connection, tid: str, deps: list[str]) -> bool:
    """新边 `tid → deps` 是否成环：沿依赖链找回到 tid 的路径（DFS）。

    诚实边界（534 §2.4）：在"deps 仅 enqueue 时声明 + 新节点只指出新边"的约束下，当前
    构造不出环；本检测的价值在①自引用笔误（另有前置拦截）②未来若开"加边/改 deps"命令。
    不夸口它挡得住现约束下不存在的环。
    """
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
            # 回收即交还 token（tasks 行不再持有所有权 ⇒ 不留旧 secret）
            conn.execute(
                "UPDATE tasks SET status='queued', claimed_by=NULL, claimed_token=NULL, "
                "heartbeat_at=NULL, updated_at=? WHERE id=?", (now, tid))
        moved.append(tid)
    return moved


def _claimed_touch(conn: sqlite3.Connection) -> dict[str, set[str]]:
    """在飞任务的写集合快照：`{task_id: {file,...}}`（只在 `claimed` 态持有文件锁）。"""
    return {r["id"]: set(_jload(r["touch_set"], []))
            for r in conn.execute("SELECT id,touch_set FROM tasks WHERE status='claimed'")}


def _conflicts(touch: list[str], claimed: dict[str, set[str]]) -> list[dict[str, Any]]:
    """候选的 touch_set 与在飞任务相交 ⇒ `[{"task": 占用者, "files": [相交文件]}]`。"""
    want = {str(t).replace("\\", "/") for t in touch}
    if not want:
        return []
    out = []
    for tid, files in claimed.items():
        inter = sorted(files & want)
        if inter:
            out.append({"task": tid, "files": inter})
    return out


def _pick(conn: sqlite3.Connection, types: list[str] | None, now: str,
          claimed_touch: dict[str, set[str]] | None = None,
          only: str | None = None
          ) -> tuple[sqlite3.Row | None, list[dict[str, Any]]]:
    """挑一个可领任务（**只读**，不改状态，除 attempts 超限就地判 blocked 外）。

    顺序：deps 全 done 的最高优先级 queued（priority 小者先）。
    535 C4：候选 touch_set 与任一**在飞**任务相交 ⇒ 跳过它继续看下一个，并记下
    "在等谁、等哪个文件"（把 55b53ae/527 那类"两人同改同一批文件互不知"的事故
    从事后清理变成**派发时可见拒绝**）。返回 (选中行 | None, 被 touch 挡下的候选清单)。
    """
    blocked_touch: list[dict[str, Any]] = []
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
        if not ok:
            continue
        if only and row["id"] != only:
            continue
        conf = _conflicts(_jload(row["touch_set"], []), claimed_touch or {})
        if conf:
            blocked_touch.append({"id": row["id"], "blocked_by": conf})
            continue
        return row, blocked_touch
    return None, blocked_touch


def _reject(msg: str, code: int = 1) -> None:
    """拒绝并给出可见原因。code=1 沿用 d976170 的既有语义（状态/所有权/参数），
    code=2 = **新增 fail-closed 门**（deps 环、handoff 质量、软 takeover、
    complete 缺 verify_cmd 又缺 result-ref）——两类分开，脚本可只对后者做特判。
    """
    print(f"[task_queue] {msg}", file=sys.stderr)
    raise SystemExit(code)


# ── handoff 交接物（535 C2：结构化、机器可校验、fail-closed）──────────────────
# 断点续跑最可能"看似接上、其实接错"的一步是**信任继承**：盘上哈希只能证明"与上一会话
# 记录的哈希逐字一致"（挡损坏/偷换），证明不了"内容是对的"。因此信任不整体开关，
# 按 verified_facts 的 trust 三级判（见 validate_handoff 的 C7 段）。


def handoff_path_for(task_id: str, db_path: Path | str | None = None) -> Path:
    """handoff 的**规范落点**（534 §3.1）：`data/tasks/<id>.handoff.json`。

    worker 直接把交接物写到这儿，`checkpoint --handoff` 可省略；也可用 `--handoff`
    指定别处（会按锚根相对路径记进 `handoff_path` 列）。
    """
    p = Path(db_path) if db_path else DB_PATH
    return p.parent / f"{task_id}.handoff.json"


def _rel_store(path: Path, root: Path | str | None = None) -> str:
    """handoff 路径入列：在锚根内 ⇒ 相对 posix（可随仓库搬移）；否则绝对。"""
    base = Path(root) if root else ANCHOR_ROOT
    try:
        return path.resolve().relative_to(Path(base).resolve()).as_posix()
    except ValueError:
        return str(path)


def _load_handoff(rel: str | None) -> dict[str, Any] | None:
    """读回 handed-off 交接物；路径不存在/坏 JSON ⇒ None（不抛：claim 输出不该因它崩）。"""
    if not rel:
        return None
    p = Path(rel)
    if not p.is_absolute():
        p = ANCHOR_ROOT / rel
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None


def _anchor_ok(anchor: str, root: Path) -> bool:
    """锚点可解析：`cmd:`/`git:` 只要有实质内容；文件锚点必须在盘。

    文件锚点支持 `path` 与 `path:line`（`:line` 只是人读定位，不进盘上判定）。
    """
    if anchor.startswith(("cmd:", "git:")):
        return len(anchor.strip()) > 6
    if not anchor or anchor.startswith(":"):
        return False
    return (root / anchor.split(":", 1)[0]).is_file()


def validate_handoff(h: dict[str, Any], *, for_yield: bool = False,
                     root: Path | str | None = None) -> list[str]:
    """handoff v1 机器校验（**纯函数**：只看传入 dict + 磁盘产物，不碰 DB/全局状态，
    gate 可原样 import 复用）。返回错误列表，空 = 通过（fail-closed：不过即拒）。

    字段判据（534 §3.1）：
      goal            非空
      next_action     长度 ≥ 4（"继续"这类不算具体动作）
      steps_done[]    每项有 title；outputs.path 必须在盘；给了 sha256 必须逐字相等
                      （防产物被偷换 / 半成品冒认——半成品文件在但哈希对不上）
      verified_facts[]≥1 条；trust ∈ L1/L2/L3；anchor 必填且可解析；**L2 必须 cmd: 锚**
      budget_used     非负整数
      steps_remaining for_yield=True 时必填非空（空 remaining 应走 complete 而非 yield）

    —— C7 三级信任判据（信任不整体开关，按事实分级）——
      L1 物证（编译产物/测试结果）：文件锚点 + 可选 sha256 ⇒ **可继承**，但新会话必须
         **独立重算**盘上哈希核对（只防损坏/偷换，不证明内容正确）。
      L2 判决（verdict/规则结论）：必须 `cmd:` 锚点 ⇒ **一律重跑**，不继承声明。
      L3 裁决（人签/红队/外部事实/标准条文）：无机器锚点 ⇒ **永不自动继承**，
         续跑方须进 open_questions 交人/红队重判，不得作为跳过步骤的理由。
    """
    base = Path(root) if root else ANCHOR_ROOT
    errs: list[str] = []
    if not str(h.get("goal") or "").strip():
        errs.append("goal 为空（完成判据必须写在交接物里）")
    na = str(h.get("next_action") or "").strip()
    if len(na) < 4:
        errs.append("next_action 缺失或不像具体动作（续跑方据此开工）")
    sd = h.get("steps_done")
    if not isinstance(sd, list):
        errs.append("steps_done 必须是列表")
    else:
        for i, st in enumerate(sd):
            if not isinstance(st, dict) or not str(st.get("title") or "").strip():
                errs.append(f"steps_done[{i}] 缺 title")
                continue
            outs = st.get("outputs") or []
            if not isinstance(outs, list):
                errs.append(f"steps_done[{i}].outputs 必须是列表")
                continue
            for o in outs:
                if not isinstance(o, dict) or not o.get("path"):
                    errs.append(f"steps_done[{i}] 产物项缺 path")
                    continue
                f = base / str(o["path"])
                if not f.is_file():
                    errs.append(f"steps_done[{i}] 产物不存在：{o['path']}")
                elif o.get("sha256") and \
                        hashlib.sha256(f.read_bytes()).hexdigest() != str(o["sha256"]):
                    errs.append(f"steps_done[{i}] 产物哈希不符：{o['path']}（防偷换/半成品）")
    vf = h.get("verified_facts")
    if not isinstance(vf, list) or not vf:
        errs.append("verified_facts 为空（至少一条带锚点结论）")
    else:
        for i, fct in enumerate(vf):
            if not isinstance(fct, dict):
                errs.append(f"verified_facts[{i}] 必须是对象")
                continue
            trust = fct.get("trust")
            if trust not in TRUST_LEVELS:
                errs.append(f"verified_facts[{i}] 缺 trust∈{{L1,L2,L3}}")
            a = str(fct.get("anchor") or "").strip()
            if not a or not _anchor_ok(a, base):
                errs.append(f"verified_facts[{i}] 无锚点或锚点不存在：{a[:60]}")
            elif trust == "L2" and not a.startswith("cmd:"):
                errs.append(f"verified_facts[{i}] L2 判决必须用 cmd: 锚点（可重跑，不许继承）")
            elif trust == "L1" and fct.get("sha256") and not a.startswith(("cmd:", "git:")):
                fp = base / a.split(":", 1)[0]
                if fp.is_file() and \
                        hashlib.sha256(fp.read_bytes()).hexdigest() != str(fct["sha256"]):
                    errs.append(f"verified_facts[{i}] L1 物证哈希不符：{a[:60]}（防偷换/半成品）")
    bu = h.get("budget_used")
    if not isinstance(bu, int) or isinstance(bu, bool) or bu < 0:
        errs.append("budget_used 必须是非负整数")
    if for_yield:
        sr = h.get("steps_remaining")
        if not isinstance(sr, list) or not sr:
            errs.append("yield 时 steps_remaining 为空（无剩余应走 complete）")
    return errs


def resume_plan(h: dict[str, Any], *, root: Path | str | None = None) -> dict[str, Any]:
    """续跑计划（535 C7）：把"哪些能继承、哪些必须重算、哪些只能走人"算成机器清单。

    **信任不是整体开关**——盘上哈希只能证明"与上一会话记录的哈希逐字一致"（挡损坏/偷换），
    证明不了"内容是对的"；所以按事实分级：

      L1 物证（编译产物/测试结果）：**可继承**，但新会话必须**独立重算**盘上哈希核对
         （`status`: match / mismatch / no_digest〔没记哈希⇒自己重新度量〕/ no_file）；
      L2 判决（verdict/规则结论）：**一律重跑** `cmd:` 锚点里的命令，不信声明；
      L3 裁决（人签/红队/外部事实）：**永不自动继承** ⇒ 进 l3_human + open_questions 交人。
    `blocked=True`（有 L1 物证对不上）⇒ 不得按"继承"继续，须人工介入。
    """
    base = Path(root) if root else ANCHOR_ROOT
    l1: list[dict[str, Any]] = []
    l2: list[dict[str, Any]] = []
    l3: list[dict[str, Any]] = []
    for i, fct in enumerate(h.get("verified_facts") or []):
        if not isinstance(fct, dict):
            continue
        trust, anchor = fct.get("trust"), str(fct.get("anchor") or "")
        item: dict[str, Any] = {"i": i, "fact": fct.get("fact"), "anchor": anchor}
        if trust == "L1":
            if anchor.startswith(("cmd:", "git:")):
                item["status"] = "no_file"
            else:
                fp = base / anchor.split(":", 1)[0]
                if not fp.is_file():
                    item["status"] = "no_file"
                elif fct.get("sha256"):
                    item["status"] = ("match" if hashlib.sha256(fp.read_bytes()).hexdigest()
                                      == str(fct["sha256"]) else "mismatch")
                else:
                    item["status"] = "no_digest"
            l1.append(item)
        elif trust == "L2":
            item["cmd"] = anchor[4:].strip() if anchor.startswith("cmd:") else ""
            l2.append(item)
        elif trust == "L3":
            l3.append(item)
    bad = [x for x in l1 if x["status"] in ("mismatch", "no_file")]
    return {"l1_verify": l1, "l2_rerun": l2, "l3_human": l3,
            "open_questions": list(h.get("open_questions") or []),
            "blocked": bool(bad),
            "note": "L1 可继承但须新会话独立重算哈希；L2 一律重跑；L3 永不自动继承（走人/红队）"}


def cp_fingerprint(h: dict[str, Any]) -> str:
    """进度指纹：done 步的 (n + 产物 path/sha256) + remaining 条数 ⇒ 16 hex。

    用途：① fake-progress 检测（心跳指纹不推进 = 假活）；② 续跑方一眼看出
    "交接物自上次 checkpoint 后有没有动过"。
    """
    x = hashlib.sha256()
    for st in h.get("steps_done") or []:
        if not isinstance(st, dict):
            continue
        x.update(str(st.get("n")).encode())
        for o in st.get("outputs") or []:
            if isinstance(o, dict):
                x.update(str(o.get("path")).encode())
                x.update(str(o.get("sha256")).encode())
    x.update(str(len(h.get("steps_remaining") or [])).encode())
    return x.hexdigest()[:16]


# ── 写操作（皆 `BEGIN IMMEDIATE` 原子） ──────────────────────────────────────


def enqueue(task_type: str, payload_ref: str, priority: int = 100,
            deps: list[str] | None = None, task_id: str | None = None,
            db_path: Path | str | None = None, *, touch: list[str] | None = None,
            verify_cmd: str = "", budget: int = 500, parent: str | None = None,
            model: str | None = None, steps: int = 0, goal: str = "",
            worker: str = "enqueuer") -> dict[str, Any]:
    """入队（幂等）。已存在 ⇒ {"created": False}，不报错（可安全重跑）。

    535 C2 扩参：`touch`（写冲突锁的声明集，posix 相对路径）、`verify_cmd`（complete 门禁）、
    `budget/steps/goal/parent/model`（预算与交接物语境）。deps 引用不存在的任务仍只**提示**
    （d976170 契约：任务照建，只是 claim 不到）；但**自引用与成环一律拒**（fail-closed）。
    """
    if not task_type or not payload_ref:
        raise SystemExit("[task_queue] --type 与 --payload-ref 必填")
    init(db_path)
    tid = task_id or make_id(task_type, payload_ref)
    deps = list(deps or [])
    if tid in deps:
        _reject(f"deps 自引用：{tid} 依赖自身（永不可 claim，入队即拒）", 2)
    conn = _connect(db_path)
    try:
        conn.execute("BEGIN IMMEDIATE")
        if conn.execute("SELECT id FROM tasks WHERE id=?", (tid,)).fetchone():
            conn.execute("COMMIT")
            return {"id": tid, "created": False, "reason": "同 id 已存在（幂等）"}
        # 依赖不存在 ⇒ 可见提示（不静默：缺依赖的任务会永远 claim 不到）
        missing = [d for d in deps if not conn.execute(
            "SELECT 1 FROM tasks WHERE id=?", (d,)).fetchone()]
        if _has_cycle(conn, tid, deps):
            _rollback(conn)
            _reject(f"deps 成环：沿依赖链可回到 {tid}（入队即拒）", 2)
        now = _now()
        touch_set = sorted({str(t).replace("\\", "/") for t in (touch or []) if str(t).strip()})
        conn.execute(
            "INSERT INTO tasks(id,type,payload_ref,status,priority,deps,attempts,"
            "created_at,updated_at,touch_set,verify_cmd,budget_calls,parent_task,"
            "produced_by_model,steps_total,goal) "
            "VALUES(?,?,?,'queued',?,?,0,?,?,?,?,?,?,?,?,?)",
            (tid, task_type, payload_ref, int(priority),
             json.dumps(deps, ensure_ascii=False), now, now,
             json.dumps(touch_set, ensure_ascii=False), verify_cmd, int(budget),
             parent, model, int(steps), goal))
        _event(conn, tid, worker, "enqueue",
               f"deps={deps} touch={touch_set} steps={int(steps)} "
               f"budget={int(budget)} verify_cmd={verify_cmd!r} parent={parent}")
        conn.execute("COMMIT")
        return {"id": tid, "created": True, "deps_missing": missing, "touch_set": touch_set}
    except BaseException:
        _rollback(conn)
        raise
    finally:
        conn.close()


def claim(worker: str, types: list[str] | None = None,
          db_path: Path | str | None = None, *, takeover: str | None = None,
          force: bool = False, reason: str = "") -> dict[str, Any]:
    """原子领走一个任务：deps 全 done 的最高优先级 queued。

    返回 `{"claimed": <任务 dict 或 None>, "taken_over": [回收的 id],
    "blocked_by_touch": [...]}`；`claimed` 里附 handoff 全文与 next_action。

    **租约语义（535 C5）**：任务已被 claim 且心跳在 `LEASE_GRACE_S`(120s) 内时，
    裸 claim **抢不到**（它只挑 queued 行）——否则新会话一进来就顶掉别人正在干的活。
    接管只有两条路：①心跳过期走既有 stale 回收（机器判定死亡，600s）；
    ②人显式 `--takeover <id> --force --reason <原因>`（人担责，events 记 manual_takeover）。
    心跳新鲜又没 force ⇒ 软拒绝（exit 2 + 提示）；force 无 reason ⇒ 拒绝（不许无痕接管）。
    """
    if not worker:
        raise SystemExit("[task_queue] --worker 必填")
    init(db_path)
    conn = _connect(db_path)
    try:
        conn.execute("BEGIN IMMEDIATE")
        now = _now()
        moved: list[str] = []
        target_id: str | None = None
        if takeover:
            tr = conn.execute("SELECT * FROM tasks WHERE id=?", (takeover,)).fetchone()
            if tr is None:
                _rollback(conn)
                raise SystemExit(f"[task_queue] 接管目标不存在：{takeover}")
            if tr["status"] != "claimed":
                _rollback(conn)
                _reject(f"接管目标 {takeover} 状态={tr['status']}（仅 claimed 可接管）", 2)
            age = _age_s(tr["heartbeat_at"] or tr["claimed_at"])
            if (age is None or age < LEASE_GRACE_S) and not force:
                _rollback(conn)
                shown = "未知" if age is None else f"{int(age)}s 前"
                _reject(f"{takeover} 心跳 {shown}（租约 {LEASE_GRACE_S}s 内），疑似仍在跑；"
                        f"人确认旧会话已死后用 --takeover {takeover} --force "
                        f"--reason <原因> 接管", 2)
            if force and not reason.strip():
                _rollback(conn)
                _reject("--force 接管必须给 --reason（人担责留痕，不许无痕顶掉在跑的会话）", 2)
            conn.execute(
                "UPDATE tasks SET status='queued',claimed_by=NULL,claimed_token=NULL,"
                "heartbeat_at=NULL,updated_at=? WHERE id=?", (now, takeover))
            _event(conn, takeover, worker, "manual_takeover",
                   f"from={tr['claimed_by']} age={'?' if age is None else int(age)}s "
                   f"force={force} reason={reason}")
            target_id = takeover
        else:
            moved = _sweep_stale(conn, now)
        # 快照须在 stale 回收**之后**取：被回收的任务已不持有文件锁
        row, blocked_touch = _pick(conn, types, now, _claimed_touch(conn), only=target_id)
        if row is None:
            conn.execute("COMMIT")
            return {"claimed": None, "taken_over": moved, "blocked_by_touch": blocked_touch}
        # 显式 `AND status='queued'`（双保险）：即便事务语义有变，也不可能重复认领同一行
        # token possession（E12）：认领即落盘 128-bit secret，行里存副本；
        # heartbeat/checkpoint/yield/complete 三处都要"名字对 + token 对"。
        secret = worker_secret(db_path, worker, register=True)
        cur = conn.execute(
            "UPDATE tasks SET status='claimed',claimed_by=?,claimed_token=?,claimed_at=?,"
            "heartbeat_at=?,attempts=attempts+1,updated_at=? WHERE id=? AND status='queued'",
            (worker, secret, now, now, now, row["id"]))
        if cur.rowcount != 1:
            _rollback(conn)
            _reject(f"认领竞争失败：{row['id']} 已被别的会话领走（重跑一次即可）", 2)
        _event(conn, row["id"], worker, "claim", f"attempt={int(row['attempts'] or 0) + 1}")
        out = _as_row_dict(
            conn.execute("SELECT * FROM tasks WHERE id=?", (row["id"],)).fetchone())
        conn.execute("COMMIT")
        # 冷启动一条命令接上（535 C2）：认领即交出 handoff 全文 + next_action
        return {"claimed": _with_handoff(out), "taken_over": moved,
                "blocked_by_touch": blocked_touch}
    except BaseException:
        _rollback(conn)
        raise
    finally:
        conn.close()


def _with_handoff(row: dict[str, Any]) -> dict[str, Any]:
    """在任务 dict 上挂 handoff（`handoff`=全文；`next_action`/`steps_remaining` 摘要）。

    交接物不在盘/坏 JSON ⇒ handoff=None 且 `handoff_error` 显形（**不静默**：续跑方
    必须知道"有人声称交接过但文件没了"，而不是以为这是全新任务）。
    """
    if not row.get("handoff_path"):
        return row
    h = _load_handoff(row["handoff_path"])
    row["handoff"] = h
    if h is None:
        row["handoff_error"] = f"handoff_path={row['handoff_path']} 不可读（缺文件/坏 JSON）"
    else:
        row["next_action"] = h.get("next_action")
        row["steps_remaining"] = h.get("steps_remaining")
        # C7：认领即把"哪些可继承/必须重跑/只能走人"摆给新会话，不让它凭感觉续跑
        row["resume_plan"] = resume_plan(h)
    return row


def workers_dir(db_path: Path | str | None = None) -> Path:
    """worker token 目录（`data/tasks/workers/`，随队列库同目录、已 gitignore）。"""
    d = (Path(db_path) if db_path else DB_PATH).parent / "workers"
    d.mkdir(parents=True, exist_ok=True)
    return d


def worker_secret(db_path: Path | str | None, worker: str, *, register: bool) -> str:
    """worker 的 128-bit secret（文件 possession = 所有权的第二因子，534 §6.1 E12）。

    - 已注册：读文件里的 secret；
    - 未注册且 `register=False`：**拒绝**（fail-closed——名前缀对不上就说明不是本人）；
    - 未注册且 `register=True`：首次 claim 时生成并落盘（含 host/pid/创建时间，便于人审）。
    诚实边界：同一 Windows 用户能读该文件就能冒充——本机单人场景**文件系统权限即信任
    边界**；跨用户/CI 场景须升级为 OS keyring/签名（本批不做）。
    """
    if not worker or any(c in worker for c in ("/", "\\", ":")):
        _reject(f"worker 名非法（不得为空或含路径分隔符）：{worker!r}", 1)
    p = workers_dir(db_path) / f"{worker}.token"
    if p.is_file():
        try:
            data = json.loads(p.read_text(encoding="utf-8"))
            return str(data["secret"])
        except (json.JSONDecodeError, KeyError, OSError, TypeError) as exc:
            _reject(f"worker token 文件损坏：{p}（{exc}）；人工检查或删除后重新 claim", 2)
    if not register:
        _reject(f"worker {worker!r} 未注册（缺 workers/{worker}.token）⇒ 疑似冒名，拒绝", 2)
    secret = secrets.token_hex(16)
    p.write_text(json.dumps({"id": worker, "secret": secret, "host": socket.gethostname(),
                             "pid": os.getpid(), "at": _now()},
                            ensure_ascii=False, indent=1), encoding="utf-8")
    return secret


def _authorize(row: sqlite3.Row | dict[str, Any], worker: str, action: str,
               db_path: Path | str | None = None) -> None:
    """工作命令的**唯一授权点**：状态必须 claimed + 必须是认领者本人 + 必须持有 token。

    d976170 只比 `claimed_by` 字符串——知道名字就能冒充（534 §6.1 E12）；C5 在此单点
    叠加 token possession，不在别处再写一遍。**兼容残留**：d976170 时代认领的行
    `claimed_token` 为 NULL（升级前认领的任务），无从核对 ⇒ 放行（只认名字），
    代价是那批在飞任务保留旧弱授权；新认领一律带 token。诚实边界见 `worker_secret`。
    """
    if row["status"] != "claimed":
        raise SystemExit(
            f"[task_queue] {row['id']} 当前状态 {row['status']}，非 claimed ⇒ 拒绝 {action}")
    if row["claimed_by"] != worker:
        raise SystemExit(
            f"[task_queue] 拒绝 {action}：{row['id']} 由 {row['claimed_by']!r} 认领，非 {worker!r}")
    tok = row["claimed_token"] if "claimed_token" in row.keys() else None
    if tok:
        disk = worker_secret(db_path, worker, register=False)
        if disk != tok:
            _reject(f"拒绝 {action}：{worker!r} 未持有 {row['id']} 的 token"
                    f"（知道名字不等于有所有权，E12 冒名拦截）", 2)


def _age_s(ts: str | None) -> float | None:
    """心跳时间戳距现在的秒数（本地 ISO 秒级字符串，与写入方同口径；解析失败 ⇒ None）。"""
    if not ts:
        return None
    try:
        return time.time() - time.mktime(time.strptime(str(ts), "%Y-%m-%dT%H:%M:%S"))
    except ValueError:
        return None


def _read_handoff_file(hp: Path) -> dict[str, Any]:
    """读交接物文件（缺文件/坏 JSON/非对象 ⇒ 明确拒绝，绝不静默当空交接物）。"""
    if not hp.is_file():
        _reject(f"handoff 文件不存在：{hp}（先写交接物再 checkpoint/yield）", 1)
    try:
        h = json.loads(hp.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        _reject(f"handoff 不是合法 JSON：{hp}（{exc}）", 1)
    if not isinstance(h, dict):
        _reject(f"handoff 顶层必须是对象：{hp}", 1)
    return h


def checkpoint(task_id: str, worker: str, handoff_path: Path | str | None = None, *,
               used: int | None = None, force: bool = False,
               db_path: Path | str | None = None) -> dict[str, Any]:
    """关键步骤落盘（535 C2）：校验交接物 → 写 checkpoint/指纹/steps_done/心跳。

    落盘点判据（534 §3.2）：**"这一步若丢了，新会话需要重跑一条命令才能恢复"就值得
    checkpoint**；读取/思考类动作不落盘。任意时刻被杀最多丢一步（checkpoint 各自独立提交）。
    fail-closed：handoff 质量不过 ⇒ 拒绝落盘（`--force` 是人给自己的口子，事件里留痕）。
    """
    if not worker:
        raise SystemExit("[task_queue] --worker 必填")
    hp = Path(handoff_path) if handoff_path else handoff_path_for(task_id, db_path)
    init(db_path)
    conn = _connect(db_path)
    try:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if row is None:
            _rollback(conn)
            raise SystemExit(f"[task_queue] 无此任务：{task_id}")
        # 先认人（状态+本人+token），再看交接物：非本人连"质量哪里不过"都不该看到
        _authorize(row, worker, "checkpoint", db_path)
        h = _read_handoff_file(hp)
        errs = validate_handoff(h)
        if errs and not force:
            _reject("checkpoint 质量不过（fail-closed，逐条修或人签 --force）：\n  - "
                    + "\n  - ".join(errs), 2)
        fp = cp_fingerprint(h)
        steps_done = len(h.get("steps_done") or [])
        used_n = int(used if used is not None else (h.get("budget_used") or 0))
        now = _now()
        conn.execute(
            "UPDATE tasks SET checkpoint=?,cp_fingerprint=?,steps_done=?,handoff_path=?,"
            "budget_used_calls=?,heartbeat_at=?,updated_at=? WHERE id=?",
            (json.dumps(h, ensure_ascii=False), fp, steps_done, _rel_store(hp),
             used_n, now, now, task_id))
        _event(conn, task_id, worker, "checkpoint",
               f"steps_done={steps_done} fp={fp} used={used_n} forced={bool(errs)}"
               + (f" errors={errs}" if errs else ""))
        conn.execute("COMMIT")
        return {"id": task_id, "steps_done": steps_done, "fingerprint": fp,
                "budget_used": used_n, "handoff_path": _rel_store(hp),
                "forced": bool(errs), "errors": errs}
    except BaseException:
        _rollback(conn)
        raise
    finally:
        conn.close()


def yield_task(task_id: str, worker: str, handoff_path: Path | str | None = None, *,
               force: bool = False, db_path: Path | str | None = None) -> dict[str, Any]:
    """到顶让出（535 C3）：交接物 fail-closed 校验 → 父转 `yielded` → 残步骤切子任务。

    三道量化闸门（534 §6.5）：
      ① 预算剩余 ≥ `YIELD_BUDGET_LEFT` ⇒ **不许逃**（`--force` 是人给自己留的口子）；
      ② 单次切分 ≤ `MAX_CHILDREN` 个、空组拒绝（防碎片）、每子预算 ≥ `MIN_CHILD_BUDGET`；
      ③ 父回卷：全部子任务 done ⇒ 父自动 done（见 `_rollup_parent`）。
    **`--force` 只解预算闸门，不解 handoff 质量闸门**——"缺 next_action / 无锚点"一律拒让出。
    """
    hp = Path(handoff_path) if handoff_path else handoff_path_for(task_id, db_path)
    init(db_path)
    conn = _connect(db_path)
    try:
        conn.execute("BEGIN IMMEDIATE")
        row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        if row is None:
            _rollback(conn)
            raise SystemExit(f"[task_queue] 无此任务：{task_id}")
        _authorize(row, worker, "yield", db_path)      # 先认人，再看交接物
        h = _read_handoff_file(hp)
        errs = validate_handoff(h, for_yield=True)
        if errs:
            _reject("yield 被拒（fail-closed，让出前必须交代清楚）：\n  - "
                    + "\n  - ".join(errs), 2)
        now = _now()
        used = int(h.get("budget_used") or 0)
        left = max(0, int(row["budget_calls"]) - used)
        if left >= YIELD_BUDGET_LEFT and not force:
            _rollback(conn)
            _reject(f"预算尚余 {left} ≥ {YIELD_BUDGET_LEFT}：不许让出（确有需要请人签 --force）", 2)
        remaining = list(h["steps_remaining"])
        groups = h.get("step_groups")
        groups = (groups[:MAX_CHILDREN] if isinstance(groups, list) and groups
                  else [{"steps": remaining}])
        if any(not (isinstance(g, dict) and g.get("steps")) for g in groups):
            _rollback(conn)
            _reject("切出空子任务（碎片防护）：每个子任务至少要带一步", 2)
        per = max(MIN_CHILD_BUDGET, left // len(groups))
        parent_touch = _jload(row["touch_set"], [])
        child_ids: list[str] = []
        prev: str | None = None
        for i, g in enumerate(groups, 1):
            cid = f"{task_id}.c{i}"
            if conn.execute("SELECT 1 FROM tasks WHERE id=?", (cid,)).fetchone():
                _rollback(conn)
                _reject(f"子任务已存在：{cid}（防重复切分；人工清理后再 yield）", 2)
            cdeps = [d for d in (g.get("deps") or [])]
            if prev:
                cdeps.append(prev)          # 组间自动串行（后组等前组）
            ch = {
                "schema": h.get("schema") or "tq-handoff/v1",
                "task_id": cid,
                "goal": f"[续] {h.get('goal', '')}",
                # 父的**已验事实**整段继承（它是续跑方的信任基线：L1 可继承、L2 必重跑、L3 走人），
                # 但 steps_done 归零——子任务自己没做过那些步，不许冒认（"产物未被枚举一律重做"）。
                "verified_facts": h.get("verified_facts") or [],
                "tried_and_failed": h.get("tried_and_failed") or [],
                "open_questions": h.get("open_questions") or [],
                "steps_done": [],
                "steps_remaining": g["steps"],
                "next_action": f"领到后从 step {g['steps'][0].get('n')} 继续，逐步 checkpoint",
                "touched_files": [],
                "budget_used": 0,
            }
            chp = handoff_path_for(cid, db_path)
            chp.write_text(json.dumps(ch, ensure_ascii=False, indent=1), encoding="utf-8")
            conn.execute(
                "INSERT INTO tasks(id,type,payload_ref,status,priority,deps,attempts,"
                "created_at,updated_at,touch_set,verify_cmd,budget_calls,parent_task,"
                "produced_by_model,steps_total,goal,handoff_path) "
                "VALUES(?,?,?,'queued',?,?,0,?,?,?,?,?,?,?,?,?,?)",
                (cid, row["type"], row["payload_ref"], row["priority"],
                 json.dumps(cdeps, ensure_ascii=False), now, now,
                 json.dumps(g.get("touch") or parent_touch, ensure_ascii=False),
                 row["verify_cmd"], per, task_id, row["produced_by_model"],
                 len(g["steps"]), ch["goal"], _rel_store(chp)))
            _event(conn, cid, worker, "enqueue_child",
                   f"parent={task_id} budget={per} steps={len(g['steps'])} deps={cdeps}")
            child_ids.append(cid)
            prev = cid
        conn.execute(
            "UPDATE tasks SET status='yielded',handoff_path=?,checkpoint=?,cp_fingerprint=?,"
            "steps_done=?,claimed_by=NULL,claimed_token=NULL,heartbeat_at=NULL,"
            "budget_used_calls=?,updated_at=? WHERE id=?",
            (_rel_store(hp), json.dumps(h, ensure_ascii=False), cp_fingerprint(h),
             len(h.get("steps_done") or []), used, now, task_id))
        _event(conn, task_id, worker, "yield",
               f"children={child_ids} used={used} left={left} force={force}")
        conn.execute("COMMIT")
        return {"yielded": task_id, "children": child_ids, "budget_per_child": per,
                "budget_left": left, "status": "yielded"}
    except BaseException:
        _rollback(conn)
        raise
    finally:
        conn.close()


# 535 C6 · type → verify_cmd 绑定表（534 §4.3；`--verify-cmd` 可覆盖）。
# 理由：worker **不得自证**——"干完了"必须由可重跑的命令说话。`{py}` 用运行本工具的解释器，
# `{payload}` 用任务的 payload_ref。research/custom 无机器判决 ⇒ 空（强制 --result-ref 转人审）。
DEFAULT_VERIFY_CMDS: dict[str, str] = {
    "atom_produce": '"{py}" tools/atom_evidence_replay.py --card {payload} --no-sanitizer',
    "redteam": '"{py}" tools/poison_drill.py',
    "replay_batch": '"{py}" tools/atom_evidence_replay.py --check --no-sanitizer',
    "tool_change": '"{py}" -m pytest tests/ -m fast -q',
    "doc": '"{py}" tools/doc_frontmatter.py',
    "research": "",
    "reverify_model": '"{py}" tools/atom_evidence_replay.py --check --no-sanitizer',
    "custom": "",
}


def default_verify_cmd(task_type: str, payload_ref: str) -> str:
    """按 type 取默认门禁命令（表里没有的 type ⇒ 空字符串 = 必须 --result-ref）。"""
    tpl = DEFAULT_VERIFY_CMDS.get(task_type, "")
    return tpl.format(py=sys.executable, payload=payload_ref) if tpl else ""


def _touch_audit(row: sqlite3.Row | dict[str, Any],
                 root: Path | str | None = None) -> tuple[list[str], str]:
    """完成后审计（535 C6）：`git status --porcelain -uall` 的真实改动 − 声明集 − 系统豁免。

    系统豁免：`data/tasks/**`（队列库/worker token/handoff/logs 全在这里，属调度装置自身，
    不是业务改动——534 §4.1 实测教训：worker 自己的运行日志会污染审计）。
    返回 `(undeclared, audit_note)`：**审计没跑成要显形**（`audit_note` 非空），
    不许把"没观测到"当成"已核对"（fail-closed 的信息面）。
    """
    base = Path(root) if root else ANCHOR_ROOT
    declared = {str(x).replace("\\", "/") for x in _jload(row["touch_set"], [])}
    hp = row["handoff_path"] if "handoff_path" in row.keys() else None
    if hp:
        declared.add(str(hp).replace("\\", "/"))
    try:
        # `-c core.quotepath=false`：否则 git 把非 ASCII 路径写成八进制转义（本仓中文文件名常见，
        # 实测会输出 References/architecture_/346/236/... 这种不可读形态，审计等于白做）。
        p = subprocess.run(["git", "-c", "core.quotepath=false",
                            "status", "--porcelain", "-uall"], cwd=str(base),
                           capture_output=True, text=True, encoding="utf-8",
                           errors="replace", timeout=30)
    except (OSError, subprocess.SubprocessError) as exc:
        return [], f"touch 审计未执行（{type(exc).__name__}: {exc}）——未观测到是否有未声明改动"
    if p.returncode != 0:
        return [], (f"touch 审计未执行（git status rc={p.returncode}："
                    f"{(p.stderr or '').strip()[:120]}）——未观测到是否有未声明改动")
    changed: set[str] = set()
    for ln in p.stdout.splitlines():
        if not ln.strip():
            continue
        f = ln[3:].strip()
        if " -> " in f:                     # rename/copy：取目标侧
            f = f.split(" -> ")[-1].strip()
        changed.add(f.replace("\\", "/").strip('"'))
    undeclared = sorted(f for f in changed
                        if f not in declared and not f.startswith("data/tasks/"))
    return undeclared, ""


def complete(task_id: str, worker: str, *, result_ref: str | None = None,
             timeout: int = 900, db_path: Path | str | None = None) -> dict[str, Any]:
    """完成验证闭环（535 C6）：**worker 不得自证**——先跑门禁命令，过了才 done。

    - rc=0 ⇒ `done`，`verify_hash = sha256(stdout+stderr)[:16]@<耗时>s rc=0`（可追溯的"非否认"轻量替代）；
    - rc≠0 ⇒ `attempts+1`、error 记尾部 300 字，超 `MAX_ATTEMPTS` ⇒ `blocked`，否则回 `queued`（释放所有权）；
    - 无 verify_cmd ⇒ 必须 `--result-ref`，`verify_hash=HUMAN_REVIEW_REQUIRED`（研究/文档类转人审，不许裸 done）；
    - 收尾审计：`git status -uall` 里**没在 touch_set 声明却真被改了**的文件要显形
      （沙箱实测真抓出过 worker 的运行日志 ⇒ 不是理论顾虑）。
    父回卷与 `done` 同一实现（`_rollup_parent`），两条收尾路径不分叉。
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
        _authorize(row, worker, "complete", db_path)   # 先认人
        now = _now()
        verify = row["verify_cmd"] or default_verify_cmd(row["type"], row["payload_ref"])
        if not verify:
            if not result_ref:
                _reject(f"{task_id}（type={row['type']}）无 verify_cmd：complete 必须给 "
                        f"--result-ref（转人审，不许 worker 自证）", 2)
            vhash = "HUMAN_REVIEW_REQUIRED"
            dt = 0.0
        else:
            t0 = time.perf_counter()
            try:
                pr = subprocess.run(verify, shell=True, cwd=str(ANCHOR_ROOT),
                                    capture_output=True, text=True, encoding="utf-8",
                                    errors="replace", timeout=timeout)
            except subprocess.TimeoutExpired:
                pr = None
                dt = time.perf_counter() - t0
                out_txt = f"verify 超时（>{timeout}s）：{verify}"
                rc = -1
            else:
                dt = time.perf_counter() - t0
                rc = pr.returncode
                out_txt = (pr.stdout or "") + (pr.stderr or "")
            vhash = (hashlib.sha256(out_txt.encode("utf-8", "replace")).hexdigest()[:16]
                     + f"@{dt:.2f}s rc={rc}")
            if rc != 0:
                att = int(row["attempts"]) + 1
                conn.execute("UPDATE tasks SET attempts=?,error=?,updated_at=? WHERE id=?",
                             (att, f"verify rc={rc}: {out_txt[-300:]}", now, task_id))
                _event(conn, task_id, worker, "verify_failed",
                       f"{vhash} cmd={verify[:200]}")
                if att > MAX_ATTEMPTS:
                    _block(conn, task_id, f"verify 反复失败 attempts={att}>{MAX_ATTEMPTS}", now)
                    _event(conn, task_id, worker, "blocked", "verify 失败超上限")
                    conn.execute("COMMIT")
                    return {"id": task_id, "status": "blocked", "attempts": att,
                            "verify_hash": vhash, "verify_cmd": verify}
                conn.execute(
                    "UPDATE tasks SET status='queued',claimed_by=NULL,claimed_token=NULL,"
                    "heartbeat_at=NULL,updated_at=? WHERE id=?", (now, task_id))
                _event(conn, task_id, worker, "requeue", f"verify 失败回 queued attempts={att}")
                conn.execute("COMMIT")
                return {"id": task_id, "status": "queued", "attempts": att,
                        "verify_hash": vhash, "verify_cmd": verify}
        undeclared, audit_note = _touch_audit(row)
        conn.execute(
            "UPDATE tasks SET status='done',result_ref=?,verify_hash=?,updated_at=?,"
            "heartbeat_at=? WHERE id=?",
            (result_ref or row["result_ref"], vhash, now, now, task_id))
        _event(conn, task_id, worker, "done",
               f"verify={vhash} undeclared={undeclared}"
               + (f" audit_note={audit_note}" if audit_note else ""))
        rolled = _rollup_parent(conn, row, worker, now)
        conn.execute("COMMIT")
        return {"id": task_id, "status": "done", "verify_hash": vhash, "verify_cmd": verify,
                "undeclared_touch": undeclared, "audit_note": audit_note,
                "parent_rolled_up": rolled}
    except BaseException:
        _rollback(conn)
        raise
    finally:
        conn.close()


def _rollup_parent(conn: sqlite3.Connection, row: sqlite3.Row | dict[str, Any],
                   actor: str, now: str) -> str | None:
    """父回卷（534 §3.4）：最后一个子任务 complete 时，父（yielded）的所有子任务全 done
    ⇒ 父自动 done。返回被回卷的父 id（没有则 None）。
    """
    parent = row["parent_task"]
    if not parent:
        return None
    pr = conn.execute("SELECT id,status FROM tasks WHERE id=?", (parent,)).fetchone()
    if pr is None or pr["status"] != "yielded":
        return None
    open_n = conn.execute(
        "SELECT COUNT(*) FROM tasks WHERE parent_task=? AND status!='done'", (parent,)
    ).fetchone()[0]
    if open_n == 0:
        conn.execute("UPDATE tasks SET status='done',updated_at=? WHERE id=?", (now, parent))
        _event(conn, parent, actor, "done_rollup", f"via child {row['id']}")
        return parent
    return None


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
        # C4：预览也要显示"谁被 touch 挡下、在等谁"——否则人看到的 next 与 claim 结果不一致。
        # stale 的在飞任务即将被回收，不算持锁者（与 claim 里 sweep 后取快照同口径）。
        claimed_touch = {tid: files for tid, files in _claimed_touch(conn).items()
                         if tid not in stale}
        blocked_touch: list[dict[str, Any]] = []
        for row in conn.execute(sql, args).fetchall():
            if row["status"] == "claimed" and row["id"] not in stale:
                continue
            if int(row["attempts"] or 0) > MAX_ATTEMPTS:
                continue
            ok, pending = _deps_done(conn, row["deps"])
            if not ok:
                pending_deps.append({"id": row["id"], "pending": pending})
                continue
            others = {k: v for k, v in claimed_touch.items() if k != row["id"]}
            conf = _conflicts(_jload(row["touch_set"], []), others)
            if conf:
                blocked_touch.append({"id": row["id"], "blocked_by": conf})
                continue
            out = _as_row_dict(row)
            out["would_take_over"] = row["id"] in stale
            return {"next": out, "blocked_by_touch": blocked_touch}
        return {"next": None, "stale_claimed": sorted(stale),
                "blocked_by_deps": pending_deps, "blocked_by_touch": blocked_touch}
    finally:
        conn.close()


def _worker_update(task_id: str, worker: str, action: str,
                   result_ref: str | None = None, error: str | None = None,
                   db_path: Path | str | None = None) -> dict[str, Any]:
    """heartbeat/done/fail/blocked 的**公共入口**：授权一律走 `_authorize` 单点。

    （状态=claimed + 认领者本人 + token possession；非 claim 者一律 SystemExit。）
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
        _authorize(row, worker, action, db_path)   # 拒绝由外层 except 统一回滚
        now = _now()
        rolled: str | None = None
        if action == "heartbeat":
            conn.execute("UPDATE tasks SET heartbeat_at=?, updated_at=? WHERE id=?",
                         (now, now, task_id))
        elif action == "done":
            conn.execute("UPDATE tasks SET status='done', result_ref=?, heartbeat_at=?, "
                         "updated_at=? WHERE id=?", (result_ref, now, now, task_id))
            # `done` 保留（d976170 契约），升级方向是 `complete`（C6：worker 不得自证）；
            # 父回卷两条路径都要做（yield 切出的子任务可能被 done 收尾）。
            rolled = _rollup_parent(conn, row, worker, now)
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
        if action == "done" and rolled:
            out["parent_rolled_up"] = rolled
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
    """CLI 入口：**把业务拒绝统一收敛成返回码**（0 成功 / 1 既有拒绝 / 2 fail-closed 门）。

    库函数仍以 `SystemExit` 表达拒绝（调用方一眼看到"这不是正常返回"）；CLI 层兜住它，
    免得调用方（脚本/pytest）拿到异常而不是退出码。
    """
    try:
        return _main(argv)
    except SystemExit as exc:
        code = exc.code
        if isinstance(code, str) and code:
            print(code, file=sys.stderr)
            return 1
        return int(code) if isinstance(code, int) else (0 if code is None else 1)


def _main(argv: list[str] | None = None) -> int:
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
    en.add_argument("--touch", default="", help="写冲突锁声明集（posix 相对路径，逗号分隔）")
    en.add_argument("--verify-cmd", default="", help="complete 门禁命令（空则按 type 默认表）")
    en.add_argument("--budget", type=int, default=500, help="调用预算（yield 的门槛依据）")
    en.add_argument("--parent", default=None, help="父任务 id（子任务回指）")
    en.add_argument("--model", default=None, help="产出模型（produced_by_model，溯源用）")
    en.add_argument("--steps", type=int, default=0, help="计划总步数（steps_total）")
    en.add_argument("--goal", default="", help="一句话可验证目标")

    cl = sub.add_parser("claim", parents=[common])
    cl.add_argument("--worker", required=True)
    cl.add_argument("--types", default="")
    cl.add_argument("--takeover", default=None,
                    help="人工接管指定任务 id（心跳新鲜时须 --force --reason）")
    cl.add_argument("--force", action="store_true", help="人担责强制接管（必须配 --reason）")
    cl.add_argument("--reason", default="", help="接管原因（留痕进 events.manual_takeover）")

    ck = sub.add_parser("checkpoint", parents=[common])
    ck.add_argument("id")
    ck.add_argument("--worker", required=True)
    ck.add_argument("--handoff", default=None,
                    help="交接物路径（默认 data/tasks/<id>.handoff.json）")
    ck.add_argument("--used", type=int, default=None, help="已用调用数（写进 budget_used_calls）")
    ck.add_argument("--force", action="store_true", help="人签放行质量不过的交接物（留痕）")

    yl = sub.add_parser("yield", parents=[common])
    yl.add_argument("id")
    yl.add_argument("--worker", required=True)
    yl.add_argument("--handoff", default=None,
                    help="交接物路径（默认 data/tasks/<id>.handoff.json；须含 steps_remaining）")
    yl.add_argument("--force", action="store_true",
                    help="预算还足时人签放行（**不解** handoff 质量闸门）")

    cp = sub.add_parser("complete", parents=[common])
    cp.add_argument("id")
    cp.add_argument("--worker", required=True)
    cp.add_argument("--result-ref", default=None, help="结果引用（无 verify_cmd 时必填 ⇒ 转人审）")
    cp.add_argument("--timeout", type=int, default=900, help="verify_cmd 超时秒数（默认 900）")

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
        r = enqueue(a.type, a.payload_ref, a.priority, deps, a.id, db,
                    touch=[t for t in (a.touch or "").split(",") if t],
                    verify_cmd=a.verify_cmd, budget=a.budget, parent=a.parent,
                    model=a.model, steps=a.steps, goal=a.goal)
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
        r = claim(a.worker, types, db, takeover=a.takeover, force=a.force, reason=a.reason)
        if a.json:
            print(json.dumps(r, ensure_ascii=False))
        elif r["claimed"]:
            c = r["claimed"]
            print(f"[task_queue] {a.worker} 领到 {c['id']}（{c['type']}，"
                  f"attempts={c['attempts']}）payload={c['payload_ref']}")
            # 冷启动：把交接物直接摊在眼前（新会话零上下文接上）
            if c.get("handoff"):
                print(f"[task_queue] 交接物 {c['handoff_path']}："
                      f"goal={c['handoff'].get('goal')}")
                print(f"[task_queue] next_action：{c['handoff'].get('next_action')}")
                print(f"[task_queue] steps_done={c.get('steps_done')} "
                      f"cp_fingerprint={c.get('cp_fingerprint')} "
                      f"budget_used={c.get('budget_used_calls')}")
                rp = c.get("resume_plan")
                if rp:
                    l1_bad = [x for x in rp["l1_verify"] if x["status"] != "match"]
                    print(f"[task_queue] 续跑计划：L1 待独立核对 {len(l1_bad)}/{len(rp['l1_verify'])}"
                          f" · L2 必重跑 {len(rp['l2_rerun'])} · L3 走人 {len(rp['l3_human'])}"
                          + ("  ⚠ 有 L1 物证对不上 ⇒ 须人工介入" if rp["blocked"] else ""))
            elif c.get("handoff_error"):
                print(f"[task_queue] ⚠ {c['handoff_error']}", file=sys.stderr)
        else:
            print(f"[task_queue] 无可领任务（{a.worker}）")
        if r["taken_over"]:
            print(f"[task_queue] 回收 stale：{r['taken_over']}", file=sys.stderr)
        if r.get("blocked_by_touch"):
            print(f"[task_queue] ⚠ 被文件锁跳过：{r['blocked_by_touch']}", file=sys.stderr)
        return 0
    if a.cmd == "checkpoint":
        r = checkpoint(a.id, a.worker, a.handoff, used=a.used, force=a.force, db_path=db)
        print(json.dumps(r, ensure_ascii=False))
        return 0
    if a.cmd == "yield":
        r = yield_task(a.id, a.worker, a.handoff, force=a.force, db_path=db)
        if a.json:
            print(json.dumps(r, ensure_ascii=False))
        else:
            print(f"[task_queue] {r['yielded']} 已让出（{r['status']}）⇒ 子任务 "
                  f"{r['children']}（每子预算 {r['budget_per_child']}）")
        return 0
    if a.cmd == "complete":
        r = complete(a.id, a.worker, result_ref=a.result_ref, timeout=a.timeout, db_path=db)
        if a.json:
            print(json.dumps(r, ensure_ascii=False))
        else:
            print(f"[task_queue] {r['id']} → {r['status']}（verify {r['verify_hash']}）")
            if r.get("verify_cmd"):
                print(f"[task_queue] verify_cmd：{r['verify_cmd']}")
            if r["status"] == "done" and r.get("undeclared_touch"):
                print(f"[task_queue] ⚠ 未在 touch_set 声明却被改动：{r['undeclared_touch']}"
                      f"（已在 done 事件留痕）", file=sys.stderr)
            if r.get("audit_note"):
                print(f"[task_queue] ⚠ {r['audit_note']}", file=sys.stderr)
            if r.get("parent_rolled_up"):
                print(f"[task_queue] 父任务 {r['parent_rolled_up']} 全部子任务完成 ⇒ 自动 done")
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
        if r.get("blocked_by_touch"):
            print(f"[task_queue] 等文件锁：{r['blocked_by_touch']}", file=sys.stderr)
        return 0
    if a.cmd in ("heartbeat", "done", "fail", "blocked"):
        if a.cmd == "done":
            print("[task_queue] 提示：done 是 worker 自证路径（d976170 遗留，保留兼容）；"
                  "正式收尾请用 complete（先跑 verify_cmd，过了才 done）", file=sys.stderr)
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


