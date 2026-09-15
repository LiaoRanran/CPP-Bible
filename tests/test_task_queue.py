"""530 T7 · task_queue 回归锁：幂等入队 / 原子认领 / deps 门 / 认领者绑定 / stale 接管。

为什么这些用例值得单独锁（都是**真实会吃亏**的形态）：
- 幂等键失效 ⇒ 重跑一次 enqueue 就多一份任务，红队会重复烧一遍钱；
- 认领非原子 ⇒ 两个 worker 同时领到同一行，同一颗原子被两个人各改一半；
- 无认领者绑定 ⇒ 谁都能把别人的 claimed 标成 done（"签收"机制形同不存在）；
- stale 不回收 ⇒ worker 崩了任务永久卡死；无重试上限 ⇒ 崩一次重试到天荒地老。
"""
from __future__ import annotations

import hashlib
import json
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
    """C2+ 沙箱：库与**锚根**都指到 tmp（相对路径产物、verify 工作目录、git 审计都在此）。"""
    monkeypatch.setattr(tq, "DB_PATH", tmp_path / "queue.db")
    monkeypatch.setattr(tq, "ANCHOR_ROOT", tmp_path)
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
    assert json.loads(row["touch_set"]) == ["a/b.txt", "c.txt"], "反斜杠须归一为 posix 并去重"
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
    assert json.loads(kids[0]["touch_set"]) == ["work/shared.txt"], "touch_set 须继承"
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
        {"id": tb, "blocked_by": [{"task": ta, "files": ["work/shared.txt"]}]}]
    # 预览同口径：next 也报"谁被挡、在等谁"（此刻 TB 是唯一候选，且被 TA 挡着）
    rn = tq.next_task()
    assert rn["next"] is None
    assert rn["blocked_by_touch"] == [
        {"id": tb, "blocked_by": [{"task": ta, "files": ["work/shared.txt"]}]}]
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
