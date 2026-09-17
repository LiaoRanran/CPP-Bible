"""530 T7 · task_queue 回归锁：幂等入队 / 原子认领 / deps 门 / 认领者绑定 / stale 接管。

为什么这些用例值得单独锁（都是**真实会吃亏**的形态）：
- 幂等键失效 ⇒ 重跑一次 enqueue 就多一份任务，红队会重复烧一遍钱；
- 认领非原子 ⇒ 两个 worker 同时领到同一行，同一颗原子被两个人各改一半；
- 无认领者绑定 ⇒ 谁都能把别人的 claimed 标成 done（"签收"机制形同不存在）；
- stale 不回收 ⇒ worker 崩了任务永久卡死；无重试上限 ⇒ 崩一次重试到天荒地老。
"""
from __future__ import annotations

import datetime as dt
import hashlib
import json
import os
import sqlite3
import subprocess
import sys
import threading
from pathlib import Path

import pytest

import task_queue as tq

# d976170 的 tasks 表原样（14 列；534 规格 §1.1 写"15 列"，实测 PRAGMA 为 14 —— 以磁盘为准）。
LEGACY_DDL = """
CREATE TABLE tasks(
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
CREATE INDEX idx_tasks_pick ON tasks(status, priority, created_at);
"""
LEGACY_COLS = {"id", "type", "payload_ref", "status", "priority", "deps", "claimed_by",
               "claimed_at", "heartbeat_at", "attempts", "result_ref", "error",
               "created_at", "updated_at"}


@pytest.fixture()
def q(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """把默认库指到 tmp：证明的是**默认路径接线**，不是"能传参"。"""
    db = tmp_path / "queue.db"
    monkeypatch.setattr(tq, "DB_PATH", db)
    return db


def _sql(db: Path, sql: str, args: tuple = ()) -> None:
    conn = sqlite3.connect(str(db), timeout=10.0)
    try:
        conn.execute(sql, args)
        conn.commit()
    finally:
        conn.close()


def _get(db: Path, task_id: str) -> dict:
    conn = sqlite3.connect(str(db), timeout=10.0)
    conn.row_factory = sqlite3.Row
    try:
        row = conn.execute("SELECT * FROM tasks WHERE id=?", (task_id,)).fetchone()
        return {k: row[k] for k in row.keys()} if row else {}
    finally:
        conn.close()


def _expire(db: Path, task_id: str) -> None:
    """把 heartbeat 推到过去 ⇒ 触发 stale 判定（无需 sleep 600s）。"""
    _sql(db, "UPDATE tasks SET heartbeat_at='2000-01-01T00:00:00' WHERE id=?", (task_id,))


# ① 幂等入队
def test_enqueue_is_idempotent(q: Path):
    a = tq.enqueue("redteam", "docs/task1.md")
    b = tq.enqueue("redteam", "docs/task1.md")
    assert a["created"] is True and b["created"] is False
    assert a["id"] == b["id"] == tq.make_id("redteam", "docs/task1.md")
    assert len(tq.list_tasks()) == 1
    # 显式 --id 也走同一条幂等路径
    c = tq.enqueue("redteam", "docs/task2.md", task_id="fixed-id")
    d = tq.enqueue("replay_batch", "docs/other.md", task_id="fixed-id")
    assert c["created"] is True and d["created"] is False
    assert len(tq.list_tasks()) == 2


# ② 两连接争抢同一行，只一个 claim 成功
def test_two_connections_only_one_claims(q: Path):
    tq.init()
    tq.enqueue("redteam", "docs/only-one.md")
    results: list[dict] = []
    barrier = threading.Barrier(2)

    def worker(name: str) -> None:
        barrier.wait(timeout=10)
        results.append(tq.claim(name))

    ts = [threading.Thread(target=worker, args=(n,)) for n in ("w1", "w2")]
    for t in ts:
        t.start()
    for t in ts:
        t.join(timeout=20)

    got = [r["claimed"] for r in results if r["claimed"]]
    assert len(got) == 1, f"只应有一个 worker 领到，实际 {len(got)}：{results}"
    rows = tq.list_tasks()
    assert len(rows) == 1
    assert rows[0]["status"] == "claimed"
    assert rows[0]["attempts"] == 1, "重复认领会让 attempts 多加（并发漏网的直接证据）"
    assert rows[0]["claimed_by"] == got[0]["claimed_by"]


# ③ deps 未完成不可 claim
def test_deps_block_claim_until_done(q: Path):
    a = tq.enqueue("atom_produce", "docs/a.md", priority=100)["id"]
    b = tq.enqueue("redteam", "docs/b.md", priority=1, deps=[a])["id"]  # b 优先级更高
    # b 优先级更高但依赖未 done ⇒ 仍不可领，只能领到 a
    assert tq.claim("w1")["claimed"]["id"] == a
    assert tq.claim("w2")["claimed"] is None, "a 尚未 done，b 绝不可被领走"
    assert tq.next_task()["blocked_by_deps"] == [{"id": b, "pending": [a]}]
    tq.done(a, "w1", result_ref="out/a.txt")
    assert tq.claim("w2")["claimed"]["id"] == b
    # 依赖不存在 ⇒ 永不满足（可见提示而非静默挂起）
    ghost = tq.enqueue("redteam", "docs/ghost.md", deps=["no-such-task"])
    assert ghost["deps_missing"] == ["no-such-task"]
    assert tq.next_task()["next"] is None


# ④ 非 claim 者 done 被拒
def test_non_claimer_done_rejected(q: Path):
    tid = tq.enqueue("atom_produce", "docs/c.md")["id"]
    tq.claim("alice")
    with pytest.raises(SystemExit):
        tq.done(tid, "bob", result_ref="out/c.txt")
    assert _get(q, tid)["status"] == "claimed", "被拒后状态不得变化"
    assert _get(q, tid)["result_ref"] is None, "非认领者不得写入 result_ref"
    # 认领者本人可以；终态后连本人也不能再改
    assert tq.heartbeat(tid, "alice")["status"] == "claimed"
    assert tq.done(tid, "alice", result_ref="out/c.txt")["status"] == "done"
    with pytest.raises(SystemExit):
        tq.heartbeat(tid, "alice")
    with pytest.raises(SystemExit):
        tq.blocked(tid, "alice", reason="反悔")


# ⑤ heartbeat 超时可接管（attempts 保留）
def test_stale_heartbeat_takeover(q: Path):
    tid = tq.enqueue("replay_batch", "docs/d.md")["id"]
    tq.claim("alice")
    # 未超时 ⇒ 不可接管，且不能被第二个 claim 抢走
    assert tq.claim("bob")["claimed"] is None
    _expire(q, tid)                      # 超过 STALE_AFTER_S 未心跳 ⇒ worker 视为已死
    assert tq.next_task()["next"]["would_take_over"] is True
    r = tq.claim("bob")
    assert r["taken_over"] == [tid]
    assert r["claimed"]["id"] == tid and r["claimed"]["claimed_by"] == "bob"
    assert r["claimed"]["attempts"] == 2, "接管须保留并累加 attempts（不许清零）"
    with pytest.raises(SystemExit):
        tq.done(tid, "alice", result_ref="out/stale.txt")   # 原主已失去所有权
    assert tq.done(tid, "bob", result_ref="out/stale.txt")["status"] == "done"


# ⑥ attempts > MAX ⇒ 自动 blocked
def test_attempts_over_max_auto_blocked(q: Path):
    tid = tq.enqueue("redteam", "docs/e.md")["id"]
    for expected in (1, 2, 3, 4):
        assert tq.claim(f"w{expected}")["claimed"]["attempts"] == expected
        _expire(q, tid)
    # 第 5 次：attempts 已 4 > MAX_ATTEMPTS(3) ⇒ 回收时直接 blocked，不再发活
    r = tq.claim("w5")
    assert r["claimed"] is None
    row = _get(q, tid)
    assert row["status"] == "blocked"
    assert row["attempts"] == 4, "attempts 必须保留（blocked 的原因要可追溯）"
    assert str(tq.MAX_ATTEMPTS) in row["error"]
    assert tq.next_task()["next"] is None


# ⑦ 空队列不崩 + 只读预览不改状态
def test_empty_queue_and_next_is_read_only(q: Path):
    assert tq.list_tasks() == []
    r = tq.next_task()
    assert r["next"] is None and r["stale_claimed"] == [] and r["blocked_by_deps"] == []
    tid = tq.enqueue("redteam", "docs/f.md")["id"]
    before = _get(q, tid)
    assert tq.next_task()["next"]["id"] == tid
    assert _get(q, tid) == before, "next 是只读预览，不得改动任何一列"
    assert tq.list_tasks(status="queued")[0]["id"] == tid
    assert tq.list_tasks(status="done") == []
    # 优先级方向：数值小者先（p10 抢在 p100 前）
    lo = tq.enqueue("redteam", "docs/f2.md", priority=10)["id"]
    assert tq.next_task()["next"]["id"] == lo


# ⑧ CLI：--json 前后置都认、幂等 exit 0、空库 list 不崩
def test_cli_contract(q: Path, capsys: pytest.CaptureFixture):
    assert tq.main(["init"]) == 0
    assert tq.main(["enqueue", "--type", "redteam", "--payload-ref", "docs/g.md"]) == 0
    assert tq.main(["enqueue", "--type", "redteam", "--payload-ref", "docs/g.md"]) == 0
    assert "已存在" in capsys.readouterr().out
    assert tq.main(["--json", "list"]) == 0
    front = json.loads(capsys.readouterr().out)
    assert front["count"] == 1 and front["tasks"][0]["status"] == "queued"
    assert tq.main(["list", "--json"]) == 0            # 后置 --json（cppbible 式调用）
    assert json.loads(capsys.readouterr().out)["count"] == 1
    assert tq.main(["claim", "--worker", "alice"]) == 0
    out = capsys.readouterr().out
    assert "alice 领到" in out
    # 空库 list 不崩（0 条也要正常退出）
    tq.list_tasks()
    assert tq.main(["list", "--status", "failed"]) == 0
    assert "0 条" in capsys.readouterr().out


# ── 535 C1：冷启动建库竞态 + user_version 版本门迁移 ──────────────────────────
# 为什么值得单独锁：d976170 的 _connect 把 journal_mode 排在 busy_timeout 之前，且增量列
# 逐条 ALTER 各自自动提交——两个进程对**不存在的库**同时冷启动时，后到者会读到"加列中途"
# 的中间态并补同一列 ⇒ duplicate column name。沙箱实测 6/8 轮失败，修后 12/12 零失败。
# 该缺陷只在"多会话首次建库"的瞬间出现，日常稳态（库已存在）永远看不到。


def _columns(db: Path) -> set[str]:
    conn = sqlite3.connect(str(db), timeout=10.0)
    try:
        return {r[1] for r in conn.execute("PRAGMA table_info(tasks)")}
    finally:
        conn.close()


def _scalar(db: Path, sql: str):
    conn = sqlite3.connect(str(db), timeout=10.0)
    try:
        return conn.execute(sql).fetchone()[0]
    finally:
        conn.close()


def test_cold_start_two_processes_12_rounds(tmp_path: Path):
    """双进程同时对不存在的库首次 enqueue：12 轮必须零失败（旧版 6/8 失败）。"""
    script = Path(tq.__file__).resolve()
    for rnd in range(12):
        db = tmp_path / f"cold{rnd}" / "queue.db"
        procs = [
            subprocess.Popen(
                [sys.executable, str(script), "--db", str(db), "enqueue",
                 "--type", "redteam", "--payload-ref", f"cold/{rnd}/p{i}"],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True, encoding="utf-8", errors="replace")
            for i in range(2)
        ]
        outs = [p.communicate(timeout=180) for p in procs]
        for i, (p, (o, e)) in enumerate(zip(procs, outs)):
            assert p.returncode == 0, f"第 {rnd} 轮进程{i} 冷启动失败：\n{o}\n{e}"
        assert _scalar(db, "PRAGMA user_version") == tq.SCHEMA_VERSION, "版本门未落"
        assert str(_scalar(db, "PRAGMA journal_mode")).lower() == "wal", "WAL 未生效"
        assert len(tq.list_tasks(db_path=db)) == 2, f"第 {rnd} 轮应有两行"


def test_legacy_db_upgrades_in_place(tmp_path: Path):
    """d976170 建的旧库原地升级：存量行保留、新列拿默认值、版本门升到 1 且幂等。"""
    db = tmp_path / "legacy.db"
    conn = sqlite3.connect(str(db))
    try:
        conn.executescript(LEGACY_DDL)
        conn.execute(
            "INSERT INTO tasks(id,type,payload_ref,status,priority,deps,attempts,"
            "created_at,updated_at) VALUES('old-1','redteam','docs/old.md','queued',"
            "100,'[]',0,'2026-01-01T00:00:00','2026-01-01T00:00:00')")
        conn.commit()
    finally:
        conn.close()
    assert _columns(db) == LEGACY_COLS, "前置：旧库不应有增量列"
    assert tq.migrate(db) == 0, "首迁：迁移前版本应为 0"
    assert tq.migrate(db) == tq.SCHEMA_VERSION, "再迁：已是当前版本（幂等，不再改列）"
    assert _columns(db) == LEGACY_COLS | set(tq.NEW_COLS), "增量列应齐"
    old = _get(db, "old-1")
    assert old["status"] == "queued" and old["attempts"] == 0, "存量行不得被改"
    assert old["touch_set"] == "[]" and old["budget_calls"] == 500, "新列须有默认值"
    assert tq.list_tasks(db_path=db)[0]["id"] == "old-1", "迁移后仍可读"


def test_downgrade_roundtrip(tmp_path: Path, capsys: pytest.CaptureFixture):
    """回退脚本可与迁移成对使用（SQLite≥3.35 逐列 DROP COLUMN），且回退后能再升回来。"""
    db = tmp_path / "rt.db"
    tq.enqueue("redteam", "docs/rt.md", db_path=db)
    assert _columns(db) == LEGACY_COLS | set(tq.NEW_COLS)
    # 无 --yes ⇒ 拒绝（exit 2），库分毫不动
    assert tq.main(["downgrade", "--db", str(db)]) == 2
    assert _columns(db) == LEGACY_COLS | set(tq.NEW_COLS)
    r = tq.downgrade(db)
    assert set(r["dropped_columns"]) == set(tq.NEW_COLS)
    assert _columns(db) == LEGACY_COLS
    assert _scalar(db, "PRAGMA user_version") == 0
    conn = sqlite3.connect(str(db))
    try:
        assert conn.execute(
            "SELECT name FROM sqlite_master WHERE name='events'").fetchall() == []
    finally:
        conn.close()
    assert tq.migrate(db) == 0, "回退后可再升级"
    assert _columns(db) == LEGACY_COLS | set(tq.NEW_COLS)
    assert tq.list_tasks(db_path=db)[0]["id"] == tq.make_id("redteam", "docs/rt.md")
    capsys.readouterr()


# ── 535 C2：enqueue 扩参 + 环检测 + handoff 交接物（fail-closed）──────────────


@pytest.fixture()
def sb(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """C2+ 沙箱：库与**锚根**都指到 tmp（相对路径产物、verify 工作目录、git 审计都在此）。

    559 Part C：pytest 临时目录已移进**仓内**（`--basetemp=.pytest_tmp`，见 pyproject）⇒
    沙箱落在 git 工作树里，`git status` 会**成功**（本 fixture 想要的"审计看不到真仓库"
    这一语义被环境变化破坏，`test_c6_audit_unavailable_is_visible` 因此红）。
    这里用 `GIT_CEILING_DIRECTORIES` 把语义**显式钉死**：git 从 tmp 向上找仓库时到
    `tmp_path.parent` 为止（该目录不再被搜索）⇒ 沙箱内确定"not a git repository"。
    实测：ceiling=父目录 + cwd=子目录 ⇒ rc=128 ✓（ceiling 不能设成 tmp 自身——CWD 始终被搜索）。
    注意：`gitrepo` fixture 在 `tmp_path/anchor` 里 `git init`，`.git` 就在 cwd ⇒ 不受影响。
    """
    monkeypatch.setattr(tq, "DB_PATH", tmp_path / "queue.db")
    monkeypatch.setattr(tq, "ANCHOR_ROOT", tmp_path)
    monkeypatch.setenv("GIT_CEILING_DIRECTORIES", str(tmp_path.parent))
    return tmp_path


def _events(db: Path, task_id: str) -> list[dict]:
    conn = sqlite3.connect(str(db), timeout=10.0)
    conn.row_factory = sqlite3.Row
    try:
        return [dict(r) for r in conn.execute(
            "SELECT * FROM events WHERE task_id=? ORDER BY seq", (task_id,))]
    finally:
        conn.close()


def _handoff(root: Path, task_id: str, **over) -> Path:
    """写一份**合格**的 tq-handoff/v1（steps_done 的产物哈希按盘上真值算）。"""
    work = root / "work"
    work.mkdir(parents=True, exist_ok=True)
    out = work / "step1.txt"
    out.write_text("step1 done\n", encoding="utf-8")
    h: dict = {
        "schema": "tq-handoff/v1",
        "task_id": task_id,
        "goal": "让 step1-3 全部落盘且 verify 通过",
        "steps_done": [{"n": 1, "title": "写 step1",
                        "outputs": [{"path": "work/step1.txt",
                                     "sha256": hashlib.sha256(out.read_bytes()).hexdigest()}]}],
        "steps_remaining": [{"n": 2, "title": "写 step2", "action": "写 work/step2.txt",
                             "touch": ["work/step2.txt"]}],
        "verified_facts": [{"fact": "step1 产物字节一致", "trust": "L1",
                            "anchor": "work/step1.txt"}],
        "tried_and_failed": [],
        "next_action": "继续 step 2：写 work/step2.txt 后立即 checkpoint",
        "touched_files": ["work/step1.txt"],
        "budget_used": 42,
        "open_questions": [],
    }
    h.update(over)
    p = root / f"{task_id}.handoff.json"
    p.write_text(json.dumps(h, ensure_ascii=False), encoding="utf-8")
    return p


def test_c2_enqueue_ext_params(q: Path):
    """扩参全部落到各自的列（touch 归一并去重）；既有列不受影响。"""
    r = tq.enqueue("atom_produce", "docs/x.md", priority=5,
                   touch=["a\\b.txt", "c.txt", "c.txt"], verify_cmd="echo ok",
                   budget=200, parent="P", model="m1", steps=3, goal="让 replay 单卡 confirm")
    row = _get(q, r["id"])
    # 538 T0：入库形态改为 `_norm_touch`（os.path.normcase 平台相关）——断言写成"归一形态"
    # 而非写死分隔符方向，跨平台都成立；关键是**去重**：`a\b.txt` 与 `c.txt` 只留两条。
    assert json.loads(row["touch_set"]) == [tq._touch_store("a\\b.txt"), "c.txt"]
    assert (row["verify_cmd"], row["budget_calls"], row["parent_task"], row["goal"]) == \
        ("echo ok", 200, "P", "让 replay 单卡 confirm")
    assert (row["produced_by_model"], row["steps_total"], row["steps_done"]) == ("m1", 3, 0)
    assert row["checkpoint"] == "{}" and row["claimed_token"] is None, "新列须是空初值"
    assert [e["event"] for e in _events(q, r["id"])] == ["enqueue"]


def test_c2_self_ref_and_cycle_rejected(q: Path, capsys: pytest.CaptureFixture):
    """自引用/成环 ⇒ exit 2 且**不入队**（fail-closed）；缺依赖的老契约保持不变。"""
    with pytest.raises(SystemExit) as e1:
        tq.enqueue("redteam", "docs/self.md", task_id="SELF", deps=["SELF"])
    assert e1.value.code == 2 and "自引用" in capsys.readouterr().err
    assert tq.list_tasks() == []
    # 依赖"尚不存在"的老契约：照建 + 可见提示（不是拒绝）
    a = tq.enqueue("redteam", "docs/cyc-a.md", deps=["B"])
    assert a["deps_missing"] == ["B"] and a["created"] is True
    # 再建 B 并让它依赖 a ⇒ 环（a→B→a），必须在入队事务内拒绝
    with pytest.raises(SystemExit) as e2:
        tq.enqueue("redteam", "docs/cyc-b.md", task_id="B", deps=[a["id"]])
    assert e2.value.code == 2 and "成环" in capsys.readouterr().err
    assert _get(q, "B") == {}, "被拒的任务不得留下半行"


@pytest.mark.parametrize("key,needle,extra", [
    ("next_action", "next_action", {"next_action": "x"}),
    ("goal", "goal", {"goal": "   "}),
    ("verified_facts", "verified_facts", {"verified_facts": []}),
    ("anchor", "无锚点或锚点不存在", {"verified_facts": [
        {"fact": "f", "trust": "L1", "anchor": "work/nope.txt"}]}),
    ("l2_file_anchor", "L2 判决必须用 cmd:", {"verified_facts": [
        {"fact": "f", "trust": "L2", "anchor": "work/step1.txt"}]}),
    ("trust", "trust", {"verified_facts": [
        {"fact": "f", "trust": "L9", "anchor": "work/step1.txt"}]}),
    ("outputs_missing", "产物不存在", {"steps_done": [
        {"n": 1, "title": "t", "outputs": [{"path": "work/ghost.txt"}]}]}),
    ("outputs_hash", "哈希不符", {"steps_done": [
        {"n": 1, "title": "t", "outputs": [
            {"path": "work/step1.txt", "sha256": "0" * 64}]}]}),
    ("budget", "budget_used", {"budget_used": -1}),
    ("empty_remaining", "steps_remaining 为空", {"steps_remaining": []}),
])
def test_c2_validate_handoff_negative(sb: Path, key: str, needle: str, extra: dict):
    """每条机器判据各有一个反例（fail-closed 的牙齿）；正例见下一个用例。"""
    h = json.loads(_handoff(sb, "TV").read_text(encoding="utf-8"))
    h.update(extra)
    errs = tq.validate_handoff(h, for_yield=(key == "empty_remaining"))
    assert any(needle in e for e in errs), f"{key} 未被拦下：{errs}"


def test_c2_validate_handoff_positive(sb: Path):
    """合格交接物零错误；yield 形态（remaining 非空）同样零错误；L2 用 cmd: 锚放行。"""
    h = json.loads(_handoff(sb, "TOK").read_text(encoding="utf-8"))
    assert tq.validate_handoff(h) == []
    assert tq.validate_handoff(h, for_yield=True) == []
    h["verified_facts"].append({"fact": "单卡 replay confirm", "trust": "L2",
                                "anchor": "cmd:python tools/atom_evidence_replay.py --card x"})
    h["verified_facts"].append({"fact": "红队未推翻", "trust": "L3", "anchor": "git:abc1234"})
    assert tq.validate_handoff(h) == []


def test_c2_checkpoint_writes_and_audits(q: Path, sb: Path):
    """checkpoint 落盘：checkpoint/指纹/steps_done/handoff_path/budget_used + 心跳续租 + 事件。"""
    tid = tq.enqueue("atom_produce", "docs/cp.md", steps=3)["id"]
    tq.claim("alice")
    hp = _handoff(sb, tid)
    before = _get(q, tid)
    r = tq.checkpoint(tid, "alice", hp, used=42)
    h = json.loads(hp.read_text(encoding="utf-8"))
    assert r["steps_done"] == 1 and r["fingerprint"] == tq.cp_fingerprint(h)
    row = _get(q, tid)
    assert json.loads(row["checkpoint"])["goal"] == h["goal"], "交接物全文须入 checkpoint 列"
    assert (row["steps_done"], row["budget_used_calls"]) == (1, 42)
    assert row["handoff_path"].endswith(f"{tid}.handoff.json")
    assert row["cp_fingerprint"] == r["fingerprint"]
    assert row["heartbeat_at"] >= before["heartbeat_at"], "checkpoint 须续心跳（长步骤不误判 stale）"
    assert [e["event"] for e in _events(q, tid)] == ["enqueue", "claim", "checkpoint"]


def test_c2_checkpoint_fail_closed(q: Path, sb: Path, capsys: pytest.CaptureFixture):
    """质量不过 ⇒ exit 2 且**不落盘**；--force 是人签放行（留痕），不是静默通过。"""
    tid = tq.enqueue("atom_produce", "docs/cp2.md")["id"]
    tq.claim("alice")
    hp = _handoff(sb, tid, next_action="x")
    with pytest.raises(SystemExit) as e:
        tq.checkpoint(tid, "alice", hp)
    assert e.value.code == 2 and "next_action" in capsys.readouterr().err
    assert _get(q, tid)["checkpoint"] == "{}", "被拒的交接物不得进库"
    r = tq.checkpoint(tid, "alice", hp, force=True)
    assert r["forced"] is True and r["errors"], "人签放行必须把'质量不过'写进返回体与事件"
    assert any("forced=True" in e["detail"] for e in _events(q, tid))
    # 缺文件 ⇒ 明确拒绝（不是静默跳过）
    with pytest.raises(SystemExit) as e2:
        tq.checkpoint(tid, "alice", sb / "nope.json")
    assert e2.value.code == 1


def test_c2_checkpoint_default_path_and_ownership(q: Path, sb: Path):
    """省略 --handoff 时用规范落点 data/tasks/<id>.handoff.json；非本人/非 claimed 一律拒。"""
    tid = tq.enqueue("atom_produce", "docs/cp3.md")["id"]
    tq.claim("alice")
    canonical = tq.handoff_path_for(tid)
    canonical.write_text(_handoff(sb, tid).read_text(encoding="utf-8"), encoding="utf-8")
    assert tq.checkpoint(tid, "alice")["steps_done"] == 1, "默认落点须生效"
    with pytest.raises(SystemExit):
        tq.checkpoint(tid, "bob")
    tq.done(tid, "alice")
    with pytest.raises(SystemExit) as e:
        tq.checkpoint(tid, "alice")
    assert "非 claimed" in str(e.value.code), "终态后连本人也不得再 checkpoint"


def test_c2_claim_hands_off(q: Path, sb: Path):
    """冷启动一条命令接上：claim 返回 handoff 全文 + next_action（stale 接管场景实测）。"""
    tid = tq.enqueue("atom_produce", "docs/ho.md")["id"]
    tq.claim("alice")
    tq.checkpoint(tid, "alice", _handoff(sb, tid))
    _expire(q, tid)                       # A 掉线 ⇒ B 接管
    got = tq.claim("bob")["claimed"]
    assert got["id"] == tid and got["handoff"]["next_action"].startswith("继续 step 2")
    assert got["steps_remaining"][0]["n"] == 2
    # 交接物被删 ⇒ 显形（不静默当新任务）
    tq.handoff_path_for(tid).unlink(missing_ok=True)
    _sql(q, "UPDATE tasks SET handoff_path='data/tasks/ghost.handoff.json' WHERE id=?", (tid,))
    _expire(q, tid)
    got2 = tq.claim("carol")["claimed"]
    assert got2["handoff"] is None and "不可读" in got2["handoff_error"]


# ── 535 C3：yield 让出（切子任务 + 父回卷），三道量化闸门 ─────────────────────


def test_c3_yield_splits_child_and_rolls_up(q: Path, sb: Path):
    """主场景（534 S4 同构）：父 yield → 子承接剩余步骤 → 子 done ⇒ 父自动 done。"""
    tid = tq.enqueue("atom_produce", "docs/y.md", budget=150, steps=3)["id"]
    tq.claim("alice")
    hp = _handoff(sb, tid, budget_used=100, steps_remaining=[
        {"n": 2, "title": "写 step2", "action": "写 work/step2.txt"},
        {"n": 3, "title": "写 step3", "action": "写 work/step3.txt"}])
    tq.checkpoint(tid, "alice", hp, used=100)          # left = 150-100 = 50 < 100 ⇒ 可让出
    r = tq.yield_task(tid, "alice", hp)
    assert r["status"] == "yielded" and r["children"] == [f"{tid}.c1"]
    assert r["budget_left"] == 50
    assert r["budget_per_child"] == tq.MIN_CHILD_BUDGET, "子预算下限须生效（防切到没法干活）"
    parent = _get(q, tid)
    assert parent["status"] == "yielded" and parent["claimed_by"] is None
    assert parent["checkpoint"] != "{}" and parent["steps_done"] == 1, "让出要**保留** checkpoint"
    child = _get(q, f"{tid}.c1")
    assert (child["status"], child["parent_task"]) == ("queued", tid)
    assert (child["budget_calls"], child["steps_total"]) == (tq.MIN_CHILD_BUDGET, 2)
    ch = json.loads((sb / f"{tid}.c1.handoff.json").read_text(encoding="utf-8"))
    assert [s["n"] for s in ch["steps_remaining"]] == [2, 3], "子任务携带全部剩余步骤"
    assert ch["steps_done"] == [], "子任务不许冒认父已做的步骤"
    assert ch["verified_facts"], "父的已验事实是续跑方的信任基线，须整段继承"
    assert [e["event"] for e in _events(q, tid)] == ["enqueue", "claim", "checkpoint", "yield"]
    # 子任务领走 → 做完 ⇒ 父自动回卷
    assert tq.claim("bob")["claimed"]["id"] == f"{tid}.c1"
    out = tq.done(f"{tid}.c1", "bob", result_ref="out/y.txt")
    assert out["parent_rolled_up"] == tid and _get(q, tid)["status"] == "done"
    assert any(e["event"] == "done_rollup" for e in _events(q, tid))


def test_c3_yield_budget_gate(q: Path, sb: Path, capsys: pytest.CaptureFixture):
    """预算还足 ⇒ 不许逃（exit 2）；人签 --force 才放行（534 §6.5 闸门①）。"""
    tid = tq.enqueue("atom_produce", "docs/y2.md", budget=500)["id"]
    tq.claim("alice")
    hp = _handoff(sb, tid, budget_used=0)
    with pytest.raises(SystemExit) as e:
        tq.yield_task(tid, "alice", hp)
    assert e.value.code == 2 and "不许让出" in capsys.readouterr().err
    assert _get(q, tid)["status"] == "claimed", "被拒后状态不得变化"
    r = tq.yield_task(tid, "alice", hp, force=True)
    assert r["children"] and r["budget_left"] == 500


def test_c3_yield_fail_closed(q: Path, sb: Path, capsys: pytest.CaptureFixture):
    """handoff 质量闸门是**硬门**：--force 只解预算，不解"缺 next_action / 无锚点"。"""
    tid = tq.enqueue("atom_produce", "docs/y3.md", budget=100)["id"]
    tq.claim("alice")
    with pytest.raises(SystemExit) as e:
        tq.yield_task(tid, "alice", _handoff(sb, tid, budget_used=100, next_action="x"),
                      force=True)
    assert e.value.code == 2 and "next_action" in capsys.readouterr().err
    assert _get(q, tid)["status"] == "claimed"
    # remaining 为空 ⇒ 该走 complete，不是 yield
    with pytest.raises(SystemExit) as e2:
        tq.yield_task(tid, "alice", _handoff(sb, tid, budget_used=100, steps_remaining=[]))
    assert e2.value.code == 2 and "steps_remaining" in capsys.readouterr().err
    assert _get(q, tid)["status"] == "claimed"


def test_c3_yield_groups_cap_and_fragments(q: Path, sb: Path,
                                           capsys: pytest.CaptureFixture):
    """分组闸门：≤MAX_CHILDREN、组间串 deps、touch 继承、空组拒绝、重复切分拒绝。"""
    tid = tq.enqueue("atom_produce", "docs/y4.md", budget=400, touch=["work/shared.txt"])["id"]
    tq.claim("alice")
    hp = _handoff(sb, tid, budget_used=350, step_groups=[
        {"steps": [{"n": n, "title": f"step{n}"}]} for n in (2, 3, 4, 5, 6)])
    r = tq.yield_task(tid, "alice", hp)
    assert len(r["children"]) == tq.MAX_CHILDREN, "单次切分须封顶（防碎片）"
    kids = [_get(q, c) for c in r["children"]]
    assert json.loads(kids[1]["deps"]) == [r["children"][0]], "组间须自动串 deps"
    assert json.loads(kids[2]["deps"]) == [r["children"][1]]
    assert json.loads(kids[0]["touch_set"]) == [tq._touch_store("work/shared.txt")], \
        "touch_set 须继承（538 T0 后为归一形态）"
    assert tq.claim("bob")["claimed"]["id"] == r["children"][0], "只有第一组可领"
    assert tq.claim("carol")["claimed"] is None, "后组等前组 done"
    # 空组 = 碎片，拒绝
    tid2 = tq.enqueue("atom_produce", "docs/y5.md", budget=100)["id"]
    tq.claim("dave")
    with pytest.raises(SystemExit) as e:
        tq.yield_task(tid2, "dave", _handoff(sb, tid2, budget_used=100,
                                             step_groups=[{"steps": []}]))
    assert e.value.code == 2 and "空子任务" in capsys.readouterr().err
    # 子任务已存在（重跑过 yield）⇒ 拒绝，不覆盖
    tq.enqueue("atom_produce", "docs/y6.md", task_id=f"{tid2}.c1")
    with pytest.raises(SystemExit) as e2:
        tq.yield_task(tid2, "dave", _handoff(sb, tid2, budget_used=100))
    assert e2.value.code == 2 and "子任务已存在" in capsys.readouterr().err
    assert _get(q, tid2)["status"] == "claimed"


# ── 535 C4：touch_set 文件锁（派发时预防；把"两人同改一批文件互不知"变可见）────


def test_c4_touch_blocks_dispatch_and_reports_waiter(q: Path):
    """A 持 shared 时：B 跳过共 touch 的 TB、领走不冲突的 TC，并拿到"TB 在等 TA"点名。"""
    ta = tq.enqueue("atom_produce", "docs/ta.md", touch=["work/shared.txt"], priority=1)["id"]
    tb = tq.enqueue("atom_produce", "docs/tb.md", touch=["work/shared.txt"], priority=30)["id"]
    tc = tq.enqueue("atom_produce", "docs/tc.md", touch=["work/other.txt"], priority=50)["id"]
    assert tq.claim("A")["claimed"]["id"] == ta
    r = tq.claim("B")
    assert r["claimed"]["id"] == tc, "TB 优先级最高但被文件锁跳过 ⇒ 领不冲突的 TC"
    assert r["blocked_by_touch"] == [
        {"id": tb, "blocked_by": [{"task": ta, "files": [tq._touch_store("work/shared.txt")]}]}]
    # 预览同口径：next 也报"谁被挡、在等谁"（此刻 TB 是唯一候选，且被 TA 挡着）
    rn = tq.next_task()
    assert rn["next"] is None
    assert rn["blocked_by_touch"] == [
        {"id": tb, "blocked_by": [{"task": ta, "files": [tq._touch_store("work/shared.txt")]}]}]
    # B 干完 TA ⇒ 文件锁释放 ⇒ TB 可领
    tq.done(ta, "A", result_ref="out/ta.txt")
    assert tq.claim("B")["claimed"]["id"] == tb
    # 不相交的文件不挡（精确到文件，不是目录粒度）
    te = tq.enqueue("atom_produce", "docs/te.md", touch=["work/third.txt"], priority=1)["id"]
    assert tq.claim("C")["claimed"]["id"] == te, "另一文件仍可并行"


def test_c4_touch_preview_reports_blocked_candidate(q: Path):
    """只读预览不得改状态，但必须显示"等文件锁"（否则人看到的 next 与 claim 结果不一致）。"""
    ta = tq.enqueue("atom_produce", "docs/pa.md", touch=["x.txt"], priority=1)["id"]
    tb = tq.enqueue("atom_produce", "docs/pb.md", touch=["x.txt"], priority=2)["id"]
    tq.claim("A")
    before = {tid: _get(q, tid) for tid in (ta, tb)}
    r = tq.next_task()
    assert r["next"] is None and r["blocked_by_touch"] == [
        {"id": tb, "blocked_by": [{"task": ta, "files": ["x.txt"]}]}]
    assert {tid: _get(q, tid) for tid in (ta, tb)} == before, "next 仍须只读"
    # stale 的持锁者不算持锁者（与 claim 里 sweep 后取快照同口径）：TA 变可接管候选，TB 不再被挡
    _expire(q, ta)
    r2 = tq.next_task()
    assert r2["blocked_by_touch"] == []
    assert r2["next"]["id"] == ta and r2["next"]["would_take_over"] is True


# ── 535 C5：租约语义 + 人工 takeover + token possession（E12 冒名）────────────


def test_c5_lease_blocks_bare_claim_and_soft_takeover(q: Path,
                                                      capsys: pytest.CaptureFixture):
    """租约内裸 claim 抢不到；软 takeover 被拒（rc=2 并提示）；只有 --force --reason 可接管。"""
    tid = tq.enqueue("atom_produce", "docs/lease.md")["id"]
    assert tq.claim("alice")["claimed"]["id"] == tid
    assert tq.claim("bob")["claimed"] is None, "租约内裸 claim 不得顶掉正在干的活"
    with pytest.raises(SystemExit) as e:
        tq.claim("bob", takeover=tid)
    assert e.value.code == 2 and "疑似仍在跑" in capsys.readouterr().err
    assert _get(q, tid)["claimed_by"] == "alice", "软拒后持有者不得变"
    # force 但不给原因 ⇒ 拒（不许无痕顶掉别人）
    with pytest.raises(SystemExit) as e2:
        tq.claim("bob", takeover=tid, force=True)
    assert e2.value.code == 2 and "--reason" in capsys.readouterr().err
    assert _get(q, tid)["claimed_by"] == "alice"
    # 人担责接管：留痕 + attempts 保留累加 + 原主失权
    r = tq.claim("bob", takeover=tid, force=True, reason="A 会话到顶被 kill")
    assert r["claimed"]["id"] == tid and r["claimed"]["claimed_by"] == "bob"
    assert r["claimed"]["attempts"] == 2, "接管须保留并累加 attempts"
    ev = [e["event"] for e in _events(q, tid)]
    assert ev[:3] == ["enqueue", "claim", "manual_takeover"] and "claim" == ev[3]
    detail = [e["detail"] for e in _events(q, tid) if e["event"] == "manual_takeover"][0]
    assert "from=alice" in detail and "A 会话到顶被 kill" in detail, "接管原因须留痕"
    with pytest.raises(SystemExit):
        tq.heartbeat(tid, "alice")
    assert tq.heartbeat(tid, "bob")["status"] == "claimed"
    # 接管目标非 claimed / 不存在 ⇒ 拒绝
    with pytest.raises(SystemExit):
        tq.claim("carol", takeover="no-such-task")
    tq.done(tid, "bob")
    with pytest.raises(SystemExit) as e3:
        tq.claim("carol", takeover=tid, force=True, reason="x")
    assert e3.value.code == 2 and "仅 claimed 可接管" in capsys.readouterr().err


def test_c5_token_possession_blocks_impersonation(q: Path, capsys: pytest.CaptureFixture):
    """知道名字 ≠ 有所有权：token 文件缺失/被换 ⇒ 工作命令一律拒（E12 冒名拦截）。"""
    tid = tq.enqueue("atom_produce", "docs/tok.md")["id"]
    tq.claim("alice")
    tok = tq.workers_dir() / "alice.token"
    assert tok.is_file() and json.loads(tok.read_text(encoding="utf-8"))["id"] == "alice"
    assert tq.heartbeat(tid, "alice")["status"] == "claimed", "本人持 token ⇒ 放行"
    # ① 删掉 token 文件（换机/换用户只剩名字）⇒ 拒
    tok.unlink()
    with pytest.raises(SystemExit) as e:
        tq.heartbeat(tid, "alice")
    assert e.value.code == 2 and "未注册" in capsys.readouterr().err
    # ② token 文件被换成别的 secret ⇒ 拒
    tok.write_text(json.dumps({"id": "alice", "secret": "0" * 32}), encoding="utf-8")
    with pytest.raises(SystemExit) as e2:
        tq.checkpoint(tid, "alice")
    assert e2.value.code == 2 and "未持有" in capsys.readouterr().err
    # ③ 恢复原 secret ⇒ 放行（拒绝不是永久性的，别把人锁死）
    tok.write_text(json.dumps({"id": "alice", "secret": _get(q, tid)["claimed_token"]}),
                   encoding="utf-8")
    assert tq.heartbeat(tid, "alice")["status"] == "claimed"


def test_c5_legacy_row_without_token_still_works(q: Path):
    """升级前认领的行 claimed_token 为 NULL ⇒ 只认名字放行（诚实残留，不因升级把在飞任务锁死）。"""
    tid = tq.enqueue("atom_produce", "docs/legacy.md")["id"]
    tq.claim("alice")
    _sql(q, "UPDATE tasks SET claimed_token=NULL WHERE id=?", (tid,))
    (tq.workers_dir() / "alice.token").unlink()
    assert tq.heartbeat(tid, "alice")["status"] == "claimed"
    # 但下一次认领会重新落 token ⇒ 从此具备双因子
    _expire(q, tid)
    assert tq.claim("bob")["claimed"]["claimed_token"]
    assert _get(q, tid)["claimed_token"], "新认领必须带 token"


# ── 535 C6：complete 验证闭环（worker 不得自证）+ touch 收尾审计 ──────────────


@pytest.fixture()
def gitrepo(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """临时 git 仓库当锚根：touch 收尾审计必须跑在真 git 根里（不碰真实仓库）。"""
    root = tmp_path / "anchor"
    root.mkdir()
    subprocess.run(["git", "init", "-q"], cwd=str(root), check=True,
                   capture_output=True, text=True)
    monkeypatch.setattr(tq, "ANCHOR_ROOT", root)
    monkeypatch.setattr(tq, "DB_PATH", tmp_path / "queue.db")
    return root


def test_c6_complete_runs_verify_and_audits_touch(q: Path, gitrepo: Path):
    """rc=0 ⇒ done + verify_hash 留痕；未声明却被改的文件必须显形（沙箱真抓出过运行日志）。"""
    (gitrepo / "work").mkdir()
    (gitrepo / "work" / "a.txt").write_text("declared\n", encoding="utf-8")
    (gitrepo / "journal.log").write_text("worker log\n", encoding="utf-8")   # 未声明
    (gitrepo / "未声明.log").write_text("中文名\n", encoding="utf-8")        # 未声明（非 ASCII）
    (gitrepo / "data" / "tasks").mkdir(parents=True)
    (gitrepo / "data" / "tasks" / "x.log").write_text("queue runtime\n", encoding="utf-8")
    tid = tq.enqueue("atom_produce", "docs/c6.md", touch=["work/a.txt"],
                     verify_cmd="echo verify-ok")["id"]
    tq.claim("alice")
    # 546 T-A7：verify 是 enqueue 自带的（custom）⇒ 自证不裸 done，须异方确认（本例关注
    # verify_hash 与收尾审计，故直接给 --second-party；自证路径见 T-A7 回归锁）
    r = tq.complete(tid, "alice", second_party="bob")
    assert r["status"] == "done" and "rc=0" in r["verify_hash"]
    assert r["verify_cmd"] == "echo verify-ok"
    # 未声明改动要显形；data/tasks 豁免；非 ASCII 路径须是**可读**形态（git 默认八进制转义）
    assert r["undeclared_touch"] == ["journal.log", "未声明.log"], r["undeclared_touch"]
    assert r["audit_note"] == ""
    row = _get(q, tid)
    assert row["status"] == "done" and row["verify_hash"] == r["verify_hash"]
    assert "journal.log" in [e["detail"] for e in _events(q, tid) if e["event"] == "done"][0]


def test_c6_complete_failed_verify_requeues_then_blocks(q: Path):
    """verify rc≠0 ⇒ 回 queued（attempts+1，释放所有权）；超限 ⇒ blocked（不许无限重试）。"""
    tid = tq.enqueue("replay_batch", "docs/c6b.md", verify_cmd="exit /b 3")["id"]
    tq.claim("w1")
    r1 = tq.complete(tid, "w1")
    assert r1["status"] == "queued" and r1["attempts"] == 2
    assert "rc=3" in r1["verify_hash"]
    row = _get(q, tid)
    assert row["claimed_by"] is None and row["claimed_token"] is None, "回 queued 要释放所有权"
    assert "verify rc=3" in row["error"]
    assert tq.claim("w2")["claimed"]["id"] == tid
    r2 = tq.complete(tid, "w2")
    assert r2["status"] == "blocked" and r2["attempts"] == 4
    assert str(tq.MAX_ATTEMPTS) in _get(q, tid)["error"]
    ev = [e["event"] for e in _events(q, tid)]
    assert ev.count("verify_failed") == 2 and "requeue" in ev and "blocked" in ev


def test_c6_no_verify_needs_result_ref(q: Path, sb: Path, capsys: pytest.CaptureFixture):
    """无 verify_cmd 的 type（research/custom）⇒ 必须 --result-ref 转人审，不许裸 done。"""
    tid = tq.enqueue("research", "docs/c6c.md")["id"]
    tq.claim("alice")
    with pytest.raises(SystemExit) as e:
        tq.complete(tid, "alice")
    assert e.value.code == 2 and "result-ref" in capsys.readouterr().err
    assert _get(q, tid)["status"] == "claimed", "被拒不得改状态"
    r = tq.complete(tid, "alice", result_ref="data/tasks/c6c.out")
    assert r["status"] == "done" and r["verify_hash"] == "HUMAN_REVIEW_REQUIRED"
    assert _get(q, tid)["result_ref"] == "data/tasks/c6c.out"


def test_c6_type_default_verify_cmd(q: Path, sb: Path, monkeypatch: pytest.MonkeyPatch):
    """type → verify_cmd 绑定表：表里没有的 type 为空；有默认可直接跑（--verify-cmd 可覆盖）。"""
    assert "--card atoms/x.md" in tq.default_verify_cmd("atom_produce", "atoms/x.md")
    assert tq.default_verify_cmd("research", "docs/x.md") == ""
    assert tq.default_verify_cmd("no-such-type", "docs/x.md") == ""
    monkeypatch.setitem(tq.DEFAULT_VERIFY_CMDS, "custom", "echo custom-ok")
    tid = tq.enqueue("custom", "docs/c6d.md")["id"]
    tq.claim("alice")
    r = tq.complete(tid, "alice")
    assert r["status"] == "done" and r["verify_cmd"] == "echo custom-ok", "须走 type 默认表"


def test_c6_audit_unavailable_is_visible(q: Path, sb: Path):
    """审计跑不成（非 git 根）⇒ 显形 audit_note，绝不静默当作"已核对无问题"。"""
    tid = tq.enqueue("doc", "docs/c6e.md", verify_cmd="echo ok")["id"]
    tq.claim("alice")
    r = tq.complete(tid, "alice", second_party="bob")   # 546 T-A7：custom verify ⇒ 异方确认
    assert r["status"] == "done"
    assert "未观测到是否有未声明改动" in r["audit_note"]
    detail = [e["detail"] for e in _events(q, tid) if e["event"] == "done"][0]
    assert "audit_note=" in detail


def test_c6_cli_full_chain(q: Path, sb: Path, capsys: pytest.CaptureFixture):
    """CLI 接线全链（argparse 漏挂参数会在这里现形）：enqueue→claim→checkpoint→complete→yield。"""
    assert tq.main(["enqueue", "--type", "custom", "--payload-ref", "docs/cli.md",
                    "--touch", "work/a.txt", "--steps", "2", "--goal", "CLI 全链",
                    "--verify-cmd", "echo cli-ok"]) == 0
    capsys.readouterr()
    assert tq.main(["claim", "--worker", "alice", "--json"]) == 0
    tid = json.loads(capsys.readouterr().out)["claimed"]["id"]
    assert tq.main(["checkpoint", tid, "--worker", "alice", "--used", "10",
                    "--handoff", str(_handoff(sb, tid)), "--json"]) == 0
    capsys.readouterr()
    # 546 T-A7：--verify-cmd 自带 ⇒ 须异方确认（CLI 接线一并锁住）
    assert tq.main(["complete", tid, "--worker", "alice", "--second-party", "bob",
                    "--json"]) == 0
    done = json.loads(capsys.readouterr().out)
    assert done["status"] == "done" and "rc=0" in done["verify_hash"]
    assert tq.main(["list", "--status", "done", "--json"]) == 0
    assert json.loads(capsys.readouterr().out)["count"] == 1
    # yield 的接线：预算 100 用满 ⇒ 可直接让出
    t2 = tq.enqueue("custom", "docs/cli2.md", budget=100, verify_cmd="echo cli-ok")["id"]
    tq.claim("bob")
    assert tq.main(["yield", t2, "--worker", "bob", "--handoff",
                    str(_handoff(sb, t2, budget_used=100))]) == 0
    assert "已让出" in capsys.readouterr().out
    assert _get(q, t2)["status"] == "yielded"
    # 软 takeover 的接线：rc=2 + 提示怎么接管（p1 确保 carol 领到的是 t3 而不是子任务）
    t3 = tq.enqueue("custom", "docs/cli3.md", priority=1)["id"]
    assert tq.claim("carol")["claimed"]["id"] == t3
    assert tq.main(["claim", "--worker", "dave", "--takeover", t3]) == 2
    assert "疑似仍在跑" in capsys.readouterr().err
    # 自引用（fail-closed）在 CLI 层同样得到 rc=2 而不是异常
    assert tq.main(["enqueue", "--type", "custom", "--payload-ref", "docs/cli4.md",
                    "--id", "SELF4", "--deps", "SELF4"]) == 2
    assert "自引用" in capsys.readouterr().err


# ── 535 C7：三级信任判据（L1 可继承但要独立验哈希 / L2 必重跑 / L3 永不继承）──


def test_c7_resume_plan_classifies_by_trust(sb: Path):
    """一份交接物里三级事实各归其位；L1 哈希对不上 ⇒ blocked（不得按继承继续）。"""
    work = sb / "work"
    work.mkdir(parents=True, exist_ok=True)
    good, bad = work / "good.txt", work / "bad.txt"
    good.write_text("ok\n", encoding="utf-8")
    bad.write_text("tampered\n", encoding="utf-8")
    h = {
        "goal": "g", "next_action": "继续 step 2 并 checkpoint", "budget_used": 1,
        "verified_facts": [
            {"fact": "产物字节一致", "trust": "L1", "anchor": "work/good.txt",
             "sha256": hashlib.sha256(good.read_bytes()).hexdigest()},
            {"fact": "产物被偷换", "trust": "L1", "anchor": "work/bad.txt",
             "sha256": hashlib.sha256(b"original\n").hexdigest()},
            {"fact": "没记哈希的物证", "trust": "L1", "anchor": "work/good.txt"},
            {"fact": "单卡 replay confirm", "trust": "L2",
             "anchor": "cmd:python tools/atom_evidence_replay.py --card x --no-sanitizer"},
            {"fact": "红队未推翻", "trust": "L3", "anchor": "git:abc1234"},
        ],
    }
    rp = tq.resume_plan(h)
    assert [x["status"] for x in rp["l1_verify"]] == ["match", "mismatch", "no_digest"]
    assert rp["l2_rerun"][0]["cmd"].startswith("python tools/atom_evidence_replay.py")
    assert rp["l3_human"][0]["anchor"] == "git:abc1234", "L3 只能走人，不得混进 L1/L2"
    assert rp["blocked"] is True, "有 L1 对不上 ⇒ 必须人工介入"
    assert len(rp["l1_verify"]) + len(rp["l2_rerun"]) + len(rp["l3_human"]) == 5
    # 干净交接物（只有能继承的 L1 + 可重跑的 L2）⇒ 不 blocked
    clean = dict(h, verified_facts=[h["verified_facts"][0], h["verified_facts"][3]])
    assert tq.resume_plan(clean)["blocked"] is False


def test_c7_validate_rejects_l1_hash_mismatch(sb: Path):
    """L1 记了哈希但盘上不符 ⇒ 交接物直接拒收（不许把被偷换的物证带进交接链）。"""
    h = json.loads(_handoff(sb, "T7").read_text(encoding="utf-8"))
    h["verified_facts"][0].update({"trust": "L1", "anchor": "work/step1.txt",
                                   "sha256": "0" * 64})
    errs = tq.validate_handoff(h)
    assert any("L1 物证哈希不符" in e for e in errs), errs


def test_c7_claim_returns_resume_plan(q: Path, sb: Path, capsys: pytest.CaptureFixture):
    """冷启动方拿到的不只是 handoff，还有"该重算什么"的机器清单（claim 输出实测）。"""
    tid = tq.enqueue("atom_produce", "docs/c7.md")["id"]
    tq.claim("alice")
    hp = _handoff(sb, tid)
    h = json.loads(hp.read_text(encoding="utf-8"))
    h["verified_facts"] = [
        {"fact": "产物字节一致", "trust": "L1", "anchor": "work/step1.txt"},
        {"fact": "单卡 replay confirm", "trust": "L2",
         "anchor": "cmd:python tools/atom_evidence_replay.py --card x"},
        {"fact": "人签放行", "trust": "L3", "anchor": "git:deadbee"},
    ]
    hp.write_text(json.dumps(h, ensure_ascii=False), encoding="utf-8")
    tq.checkpoint(tid, "alice", hp)
    # CLI 冷启动路径：接管后输出里直接给出"该重算什么"的摘要
    assert tq.main(["claim", "--worker", "bob", "--takeover", tid, "--force",
                    "--reason", "A 到顶"]) == 0
    out = capsys.readouterr().out
    assert "续跑计划" in out and "L2 必重跑 1" in out and "L3 走人 1" in out
    # 库路径：认领返回体带结构化清单（新会话可按它逐条动作）
    _expire(q, tid)
    got = tq.claim("carol")["claimed"]
    rp = got["resume_plan"]
    assert (len(rp["l1_verify"]), len(rp["l2_rerun"]), len(rp["l3_human"])) == (1, 1, 1)
    assert rp["l1_verify"][0]["status"] == "no_digest", "没记哈希 ⇒ 自己重新度量，别当已核对"
    assert rp["l3_human"][0]["fact"] == "人签放行"
    assert rp["blocked"] is False


# ── 537 T4：touch 审计的沙箱正式豁免（告警疲劳治理；白名单，不是黑名单）──────


def test_t4_sandbox_paths_exempt_formal_dirs_still_caught(q: Path, gitrepo: Path):
    """沙箱顶层目录不报；**正式目录里的未声明文件仍必须被抓**（豁免只看第一段）。"""
    for rel in ("_arch_v3/probe/x.py", "_adv_critique/y.md", "_worklog_530.md",
                "_t528k/case/atoms/A.md", "_po528base.txt", "_rp528.out"):
        f = gitrepo / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("sandbox\n", encoding="utf-8")
    for rel in ("tools/stray.py", "atoms/mem/ATOM-MEM-STRAY.md", "data/tasks/x.log"):
        f = gitrepo / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text("formal\n", encoding="utf-8")
    tid = tq.enqueue("doc", "docs/t4.md", verify_cmd="echo ok")["id"]
    tq.claim("alice")
    r = tq.complete(tid, "alice", second_party="bob")   # 546 T-A7：custom verify ⇒ 异方确认
    assert r["status"] == "done" and r["audit_note"] == ""
    assert r["undeclared_touch"] == ["atoms/mem/ATOM-MEM-STRAY.md", "tools/stray.py"], \
        r["undeclared_touch"]
    assert "_arch_v3/probe/x.py" not in r["undeclared_touch"], "沙箱顶层目录须豁免"
    assert not any(u.startswith("data/tasks/") for u in r["undeclared_touch"]), "队列自身豁免"
    # 白名单是集中的、可审的（新增前缀必须显式加一行，不许隐式规则）
    assert tq.SANDBOX_GLOBS == ("_arch_*", "_adv_*", "_worklog_*", "_t*", "_po*", "_rp*")
    assert tq._is_sandbox_path("_arch_v3/a/b.md") and not tq._is_sandbox_path("tools/a.md")
    assert not tq._is_sandbox_path("atoms/_t_x.md"), "正式目录内不因文件名像沙箱而豁免"


# ── 538 T0：touch 路径归一化（E1 P0 逃逸修复：同一物理文件不同写法绕过文件锁）──
# 修前实测：wB 用 4 种大小写/`.` 变体声明同一文件，4/4 全部逃逸（_adv_v90/probe_touch_case.py）。

_WIN = os.name == "nt"


def test_t0_dot_variants_collide_on_all_platforms(q: Path):
    """`./x` 与 `a/./x` 解析后是同一路径（PurePath 平台无关）⇒ 任一平台都必须撞锁。"""
    ta = tq.enqueue("atom_produce", "docs/t0a.md", touch=["tools/task_queue.py"],
                    priority=1)["id"]
    tq.enqueue("atom_produce", "docs/t0b.md", touch=["./tools/task_queue.py"], priority=2)
    tq.enqueue("atom_produce", "docs/t0c.md", touch=["tools/./task_queue.py"], priority=3)
    assert tq.claim("wA")["claimed"]["id"] == ta
    r = tq.claim("wB")
    assert r["claimed"] is None, "同一物理文件的 ./ 变体必须被挡住"
    assert len(r["blocked_by_touch"]) == 2
    assert {b["blocked_by"][0]["task"] for b in r["blocked_by_touch"]} == {ta}


@pytest.mark.skipif(not _WIN, reason="Windows 文件系统大小写不敏感；Linux 保持大小写敏感语义")
def test_t0_case_and_backslash_variants_blocked_on_windows(q: Path):
    """Windows：大小写变体与 `\\` 变体声明的是**同一物理文件** ⇒ 必须全部撞锁（修前 4/4 逃逸）。"""
    ta = tq.enqueue("atom_produce", "docs/t0d.md", touch=["tools/task_queue.py"],
                    priority=1)["id"]
    variants = ("TOOLS/TASK_QUEUE.PY", "Tools/Task_Queue.py", "tools\\task_queue.py")
    for i, v in enumerate(variants):
        tq.enqueue("atom_produce", f"docs/t0e{i}.md", touch=[v], priority=2)
    assert tq.claim("wA")["claimed"]["id"] == ta
    r = tq.claim("wB")
    assert r["claimed"] is None
    assert len(r["blocked_by_touch"]) == len(variants)
    # 入库即归一：库里存的应是归一后的同一条串（历史库读回也有双保险）
    # 539 A1：库中 canonical 形态是**纯 posix**（不再被 normcase 弄成反斜杠）
    assert json.loads(_get(q, ta)["touch_set"]) == ["tools/task_queue.py"]


@pytest.mark.skipif(_WIN, reason="仅在大小写敏感平台成立（Linux/macOS）")
def test_t0_case_sensitive_semantics_preserved_on_posix(q: Path):
    """Linux 大小写敏感：仅大小写不同的两个**真实不同**文件**不许**被合并成一把锁。"""
    assert tq._norm_touch("Tools/A.py") != tq._norm_touch("tools/a.py")
    assert tq._norm_touch("tools\\a.py") == "tools\\a.py", "posix 下反斜杠是文件名字符，不是分隔符"
    tq.enqueue("atom_produce", "docs/t0f.md", touch=["Tools/A.py"], priority=1)
    tq.enqueue("atom_produce", "docs/t0g.md", touch=["tools/a.py"], priority=2)
    assert tq.claim("wA") is not None
    assert tq.claim("wB")["claimed"] is not None, "不同文件不得假冲突"


def test_t0_regression_existing_touch_lock_still_works(q: Path):
    """回归：原有 touch 锁行为不变（同写法正常挡、不相交不挡、无 touch 不挡）。"""
    ta = tq.enqueue("atom_produce", "docs/t0h.md", touch=["work/shared.txt"], priority=1)["id"]
    tb = tq.enqueue("atom_produce", "docs/t0i.md", touch=["work/shared.txt"], priority=9)["id"]
    tc = tq.enqueue("atom_produce", "docs/t0j.md", touch=["work/other.txt"], priority=50)["id"]
    assert tq.claim("A")["claimed"]["id"] == ta
    r = tq.claim("B")
    assert r["claimed"]["id"] == tc, "同写法冲突须跳过并领不冲突的那个"
    assert r["blocked_by_touch"] == [
        {"id": tb, "blocked_by": [{"task": ta, "files": [tq._touch_store("work/shared.txt")]}]}]


# ── 546 T-A5：yield 深度上界 + 累计预算账（把 545 异族探针 A5 转成回归锁）─────


# ── 546 T-A7：verify 来源 + 自证不许裸 done（把 545 异族探针 A7 转成回归锁）───


def test_a7_custom_verify_self_certified_goes_needs_review(q: Path, capsys):
    """探针 A7 原形态：`--verify-cmd "echo attacker-pass"` 自带考卷 + 同一人收尾 ⇒ **不许 done**。

    修前：complete 跑 rc=0 ⇒ 直接 done（自己给自己出考卷、自己判卷、自己签收）。
    修后：转 `needs_review`，`verify_hash` 前缀 `SELF_VERIFIED`。
    """
    tid = tq.enqueue("custom", "docs/a7.md", task_id="A7",
                     verify_cmd="echo attacker-pass")["id"]
    assert _get(q, tid)["verify_source"] == "custom", "自带 verify_cmd 须标 custom"
    tq.claim("A")
    r = tq.complete(tid, "A")
    assert r["status"] == "needs_review", "自证不得裸 done"
    assert r["verify_hash"].startswith("SELF_VERIFIED")
    assert _get(q, tid)["status"] == "needs_review"
    assert [e["event"] for e in _events(q, tid)] == ["enqueue", "claim", "needs_review"]
    # 无凭据再来一次 ⇒ 仍被拒（不给"多试几次就放行"的口子）
    with pytest.raises(SystemExit) as e:
        tq.complete(tid, "A")
    assert e.value.code == 2 and "second-party" in capsys.readouterr().err
    # 自证者本人当第二方 ⇒ 拒（自己复核自己 = 没复核）
    with pytest.raises(SystemExit) as e2:
        tq.complete(tid, "A", second_party="A")
    assert e2.value.code == 2 and "本人" in capsys.readouterr().err


def test_a7_second_party_or_human_signoff_completes(q: Path):
    """异方 `--second-party`（≠ 自证者）或人签 `--force --reason` ⇒ done，两条都留痕。"""
    tid = tq.enqueue("custom", "docs/a7b.md", task_id="A7B", verify_cmd="echo ok")["id"]
    tq.claim("alice")
    assert tq.complete(tid, "alice")["status"] == "needs_review"
    r = tq.complete(tid, "alice", second_party="bob")
    assert r["status"] == "done" and "2nd=bob" in r["verify_hash"]
    assert _get(q, tid)["verify_hash"] == r["verify_hash"]
    ev = [e["event"] for e in _events(q, tid)]
    assert ev == ["enqueue", "claim", "needs_review", "done", "second_party_confirm"]

    t2 = tq.enqueue("custom", "docs/a7c.md", task_id="A7C", verify_cmd="echo ok")["id"]
    tq.claim("carol")
    r2 = tq.complete(t2, "carol", force=True, reason="人已复核产物与日志")
    assert r2["status"] == "done" and "human=人已复核产物与日志" in r2["verify_hash"]
    assert "human_signoff_done" in [e["event"] for e in _events(q, t2)]
    # 人签不给原因 ⇒ 拒（不许无痕放行）
    t3 = tq.enqueue("custom", "docs/a7d.md", task_id="A7D", verify_cmd="echo ok")["id"]
    tq.claim("dave")
    with pytest.raises(SystemExit):
        tq.complete(t3, "dave", force=True)
    assert _get(q, t3)["status"] == "claimed"


def test_a7_default_verify_still_done_and_source_recorded(q: Path,
                                                          monkeypatch: pytest.MonkeyPatch):
    """type 默认表的 verify（`default` 来源）维持现状直接 done；来源标记三种取值都落库。"""
    monkeypatch.setitem(tq.DEFAULT_VERIFY_CMDS, "custom", "echo default-ok")
    d = tq.enqueue("custom", "docs/a7e.md", task_id="A7E")["id"]          # 走默认表
    c = tq.enqueue("custom", "docs/a7f.md", task_id="A7F", verify_cmd="echo x")["id"]
    n = tq.enqueue("research", "docs/a7g.md", task_id="A7G")["id"]        # 无 verify ⇒ 空
    assert (_get(q, d)["verify_source"], _get(q, c)["verify_source"],
            _get(q, n)["verify_source"]) == ("default", "custom", "")
    tq.claim("alice")
    assert tq.complete(d, "alice")["status"] == "done", "type 默认表不是自证 ⇒ 直 done"
    assert "second_party_confirm" not in [e["event"] for e in _events(q, d)]
    # 无 verify + --result-ref ⇒ 仍是 HUMAN_REVIEW_REQUIRED（C6 不回归）
    tq.claim("bob")                       # 领到 A7F（custom，非本例目标）
    assert tq.claim("carol")["claimed"]["id"] == n
    rn = tq.complete(n, "carol", result_ref="data/tasks/a7g.out")
    assert rn["status"] == "done" and rn["verify_hash"] == "HUMAN_REVIEW_REQUIRED"


def test_a7_child_inherits_verify_source(q: Path, sb: Path):
    """yield 切出的子任务继承父的 verify_cmd **与来源**（custom 不许靠切子任务洗白）。"""
    tid = tq.enqueue("custom", "docs/a7h.md", task_id="A7H", budget=150,
                     verify_cmd="echo inherited")["id"]
    tq.claim("alice")
    hp = _handoff(sb, tid, budget_used=100)
    tq.checkpoint(tid, "alice", hp, used=100)
    kid = tq.yield_task(tid, "alice", hp)["children"][0]
    krow = _get(q, kid)
    assert (krow["verify_cmd"], krow["verify_source"]) == ("echo inherited", "custom")
    tq.claim("bob")
    assert tq.complete(kid, "bob")["status"] == "needs_review", "子任务同样不许自证裸 done"


# ── 546 T-A3：未来心跳 clamp + 年龄用 UTC（把 545 异族探针 A3 转成回归锁）──────


def _future_iso(hours: int = 1) -> str:
    """`now + hours` 的 UTC ISO 秒（与库里口径一致；探针原写的是本地裸 ISO）。"""
    return (dt.datetime.now(dt.timezone.utc) + dt.timedelta(hours=hours)
            ).strftime("%Y-%m-%dT%H:%M:%SZ")


def test_a3_future_heartbeat_is_clamped_at_write(q: Path):
    """写端：传入 now+1h 的心跳 ⇒ 一律 clamp 到 now，并留 `heartbeat_clamped` 事件。

    修前 `heartbeat_at` 可以被写成未来值 ⇒ `_sweep_stale` 的"早于 now-600s"永不命中
    ⇒ 任务恒 claimed，他人 claim/next 都拿不到（除人 --force）。
    """
    tid = tq.enqueue("custom", "docs/a3.md", task_id="A3")["id"]
    tq.claim("alice")
    fut = _future_iso(1)
    tq.heartbeat(tid, "alice", at=fut)
    row = _get(q, tid)
    assert row["heartbeat_at"] != fut and row["heartbeat_at"].endswith("Z"), row["heartbeat_at"]
    assert abs(tq._age_s(row["heartbeat_at"])) < 30, "clamp 后年龄≈0（不是未来）"
    ev = [e["detail"] for e in _events(q, tid) if e["event"] == "heartbeat_clamped"]
    assert ev and f"given={fut}" in ev[0] and "clamped_to=" in ev[0]


def test_a3_future_heartbeat_in_db_is_swept(q: Path):
    """读端（探针原形态：直接改库写未来心跳）⇒ 不采信 ⇒ 他人**当场**可接管，占坑拿不到租约。"""
    tid = tq.enqueue("custom", "docs/a3b.md", task_id="A3B")["id"]
    tq.claim("alice")
    _sql(q, "UPDATE tasks SET heartbeat_at=? WHERE id=?", (_future_iso(1), tid))
    assert tq.next_task()["next"]["id"] == tid, "未来心跳须被视作可接管候选"
    r = tq.claim("bob")
    assert r["claimed"] and r["claimed"]["id"] == tid, "他人必须能接管（旧行为：拿不到）"
    assert r["claimed"]["claimed_by"] == "bob"
    assert any(e["event"] == "heartbeat_clamped" for e in _events(q, tid)), "回收要留痕"


def test_a3_normal_heartbeat_unchanged(q: Path):
    """正常心跳（now / now-700s）不回归：不 clamp、新鲜时不被接管、过期后可接管。"""
    tid = tq.enqueue("custom", "docs/a3c.md", task_id="A3C")["id"]
    tq.claim("alice")
    old = (dt.datetime.now(dt.timezone.utc) - dt.timedelta(seconds=700)
           ).strftime("%Y-%m-%dT%H:%M:%SZ")
    tq.heartbeat(tid, "alice", at=old)             # 过去值：原样存（不挪时间）
    row = _get(q, tid)
    assert row["heartbeat_at"].endswith("Z") and 690 < tq._age_s(row["heartbeat_at"]) < 720
    assert not [e for e in _events(q, tid) if e["event"] == "heartbeat_clamped"], "过去值不 clamp"
    assert tq.claim("bob")["claimed"]["id"] == tid, "过期 700s > STALE_AFTER_S ⇒ 可接管"
    # 新鲜心跳仍受租约保护（不许借"未来不采信"把正常在跑的活抢走）
    tid2 = tq.enqueue("custom", "docs/a3d.md", task_id="A3D")["id"]
    assert tq.claim("carol")["claimed"]["id"] == tid2
    assert tq.claim("dave")["claimed"] is None, "租约内裸 claim 仍抢不到（C5 不回归）"


def test_a3_age_is_timezone_independent():
    """`_age_s` 不再靠 `time.mktime`（本机时区）：`…Z` 与 `+08:00` 两种写法同一时刻同一年龄。"""
    now_utc = dt.datetime.now(dt.timezone.utc)
    z = now_utc.strftime("%Y-%m-%dT%H:%M:%SZ")
    plus8 = now_utc.astimezone(dt.timezone(dt.timedelta(hours=8))).isoformat(timespec="seconds")
    minus5 = now_utc.astimezone(dt.timezone(-dt.timedelta(hours=5))).isoformat(timespec="seconds")
    for s in (z, plus8, minus5):
        assert abs(tq._age_s(s)) < 5, f"{s} 的年龄应与机器时区无关"
    assert tq._age_s(_future_iso(1)) < -3500, "未来心跳算出负年龄（线索不被夹掉）"
    assert tq._is_future_ts(_future_iso(1)) and not tq._is_future_ts(z)
    assert tq._age_s("不是时间") is None and tq._age_s("") is None


def test_a5_depth_cap_blocks_endless_yield(q: Path, sb: Path,
                                           capsys: pytest.CaptureFixture):
    """异族探针 A5 主形态：P→c1→c1.c1… 无 --force 只能到 MAX_YIELD_DEPTH 级。

    修前：每级子任务都拿**全新**预算（下限 80 < YIELD_BUDGET_LEFT 100）⇒ 每级都能无签再让出，
    实测 5 级仍可继续（层级与总调用预算双无上界）。修后：depth 上界是硬闸，人签才放行。
    """
    tid = tq.enqueue("custom", "docs/a5.md", task_id="P", budget=500)["id"]
    tq.claim("w0")
    h0 = _handoff(sb, tid, budget_used=450)      # left = 500-450 = 50 < 100 ⇒ 可让出
    tq.checkpoint(tid, "w0", h0, used=450)
    cur = tq.yield_task(tid, "w0", h0)["children"][0]
    assert _get(q, cur)["depth"] == 1, "根任务直接切出的子任务 depth=1"
    for i in range(1, tq.MAX_YIELD_DEPTH):       # 补到 depth=MAX_YIELD_DEPTH
        tq.claim(f"w{i}")
        nxt = tq.yield_task(cur, f"w{i}", _handoff(sb, cur, budget_used=0))["children"][0]
        assert _get(q, nxt)["depth"] == i + 1
        cur = nxt
    # 第 MAX_YIELD_DEPTH+1 级：无 force ⇒ 拒（exit 2），状态与子树都不被动
    tq.claim("wX")
    hx = _handoff(sb, cur, budget_used=0)
    with pytest.raises(SystemExit) as e:
        tq.yield_task(cur, "wX", hx)
    assert e.value.code == 2 and "深度" in capsys.readouterr().err
    assert _get(q, cur)["status"] == "claimed" and _get(q, f"{cur}.c1") == {}
    # 人签 --force ⇒ 放行（口子留在人手里）+ 事件留痕（谁放的、放到第几级）
    r = tq.yield_task(cur, "wX", hx, force=True)
    assert r["child_depth"] == tq.MAX_YIELD_DEPTH + 1
    assert _get(q, r["children"][0])["depth"] == tq.MAX_YIELD_DEPTH + 1
    assert any(e2["event"] == "yield_depth_override" for e2 in _events(q, cur))


def test_a5_cumulative_budget_pool_caps_total(q: Path, sb: Path,
                                              capsys: pytest.CaptureFixture):
    """累计账：本次下发 + 子树已发 > **根任务预算** ⇒ 无 force 拒（旧行为是每级凭空发 80）。

    父**剩余**池被下限（MIN_CHILD_BUDGET）突破是 534 §6.5 闸门② 的既有语义（C3 回归锁：
    budget=150/used=100 ⇒ 子 80），故不在此拒；改为两件事：①累计池=根预算（真·上界）；
    ②破了父剩余要在 yield 事件里显形（overdraw=…）。
    """
    tid = tq.enqueue("custom", "docs/a5b.md", task_id="B", budget=150)["id"]
    tq.claim("w0")
    h0 = _handoff(sb, tid, budget_used=100)
    tq.checkpoint(tid, "w0", h0, used=100)       # left=50 ⇒ 子预算按下限 80
    c1 = tq.yield_task(tid, "w0", h0)["children"][0]
    assert _get(q, c1)["budget_calls"] == tq.MIN_CHILD_BUDGET, "下限语义不得被破坏（C3 契约）"
    det = [e2["detail"] for e2 in _events(q, tid) if e2["event"] == "yield"][0]
    assert "overdraw=80>50" in det, "破了父剩余须显形（不许静默）"
    # 第二级：再发 80 ⇒ 累计 160 > 根预算 150 ⇒ 拒
    tq.claim("w1")
    h1 = _handoff(sb, c1, budget_used=0)
    with pytest.raises(SystemExit) as e:
        tq.yield_task(c1, "w1", h1)
    assert e.value.code == 2 and "累计池" in capsys.readouterr().err
    assert _get(q, c1)["status"] == "claimed" and _get(q, f"{c1}.c1") == {}
    # 人签放行：累计数字进 yield 事件（事后可审"总共发出去多少"）
    r = tq.yield_task(c1, "w1", h1, force=True)
    assert (r["issued_total"], r["root_budget"]) == (160, 150)
    det2 = [e2["detail"] for e2 in _events(q, c1) if e2["event"] == "yield"][0]
    assert "issued=160/root=150" in det2


def test_t0_storage_posix_compare_folded_539_a1(q: Path):
    """539 A1：**存的是纯 posix（跨平台一致），比的时候才折叠平台差异**。

    538 的 `_norm_touch` 直接把 normcase 结果入库 ⇒ Windows 库里出现反斜杠、与审计侧
    （git 输出恒 posix）两套形态。A1 拆成 `_touch_store`（入库）+ `_norm_touch`（比较键）。
    """
    r = tq.enqueue("atom_produce", "docs/a1.md",
                   touch=["tools\\task_queue.py", "./tools/task_queue.py", "docs/./a.md"])
    stored = json.loads(_get(q, r["id"])["touch_set"])
    assert stored == ["docs/a.md", "tools/task_queue.py"], stored
    assert all("\\" not in s for s in stored), "库中不得出现反斜杠形态"
    assert tq._touch_store("./docs/./a.md") == "docs/a.md", "`./` 归一（平台无关）"
    if os.name == "nt":
        assert tq._touch_store("a\\b.txt") == "a/b.txt", "Windows：反斜杠入库前转 posix"
        assert tq._norm_touch("A/B.TXT") == tq._norm_touch("a\\b.txt"), "比较键折叠大小写与分隔符"
    else:
        assert tq._norm_touch("A/B.txt") != tq._norm_touch("a/b.txt"), "posix 保持大小写敏感"
