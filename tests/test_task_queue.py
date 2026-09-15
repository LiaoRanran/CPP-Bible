"""530 T7 · task_queue 回归锁：幂等入队 / 原子认领 / deps 门 / 认领者绑定 / stale 接管。

为什么这些用例值得单独锁（都是**真实会吃亏**的形态）：
- 幂等键失效 ⇒ 重跑一次 enqueue 就多一份任务，红队会重复烧一遍钱；
- 认领非原子 ⇒ 两个 worker 同时领到同一行，同一颗原子被两个人各改一半；
- 无认领者绑定 ⇒ 谁都能把别人的 claimed 标成 done（"签收"机制形同不存在）；
- stale 不回收 ⇒ worker 崩了任务永久卡死；无重试上限 ⇒ 崩一次重试到天荒地老。
"""
from __future__ import annotations

import json
import sqlite3
import threading
from pathlib import Path

import pytest

import task_queue as tq


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
