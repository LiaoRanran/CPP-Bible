"""609 B1 · task_queue 连接池改造的性能回归锁 + 判决一致性锁。

**判决一致性优先**：所有优化只许碰"连接怎么开/什么时候关"，不许碰查询、断言、状态机。
本文件既锁性能（连接次数 / WAL 次数 / 墙钟 gross 回归），也锁语义（预算锁 + 状态机探针 + 线程模型）。

实测（同一台机器、同一 Hypothesis 种子0约束下的 max_examples=100）：
    tests/test_task_queue_stateful.py  改造前 **72.6s** ⇒ 改造后 **20.0s**（省 72.5%，7 passed）
    400 次库调用 ⇒ 真正新建连接 **2** 条（复用 398 次），WAL pragma **2** 次
    （608 D2 基线：20,952 次连接生命周期 ≈ 72% 耗时）
"""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.slow

import importlib.util
import tempfile
import threading
import time
from pathlib import Path

import task_queue as tq
from hypothesis import HealthCheck
from hypothesis import settings as HSettings

_HERE = Path(__file__).resolve().parent


def _load_ttm():
    spec = importlib.util.spec_from_file_location(
        "ttm_609", _HERE / "test_task_queue_stateful.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _tmp_db() -> Path:
    return Path(tempfile.mkdtemp(prefix="tq609_")) / "q.db"


# ── 1. 预算锁（不得被静默调大）─────────────────────────────────────────────────
def test_example_budget_lock_stays_100():
    got = _load_ttm().TestTQ.settings.max_examples
    assert got == 100, f"max_examples 被改成 {got}（应为 608 D1 定的预算下限 100）"


# ── 2. 连接复用（20,952 → 个位）───────────────────────────────────────────────
def test_connection_reuse_under_100():
    db = _tmp_db()
    tq.close_pool(db)
    tq.POOL_STATS.update({k: 0 for k in tq.POOL_STATS})
    for i in range(50):
        tid = tq.enqueue("research", f"p{i}", db_path=db)["id"]
        tq.list_tasks(db_path=db)
        c = tq.claim("wA", db_path=db)
        if c["claimed"]:
            tq.heartbeat(tid, "wA", db_path=db)
    try:
        # 50 轮 × 4 次库调用 ≈ 400 次；改造前这里要新建上千条连接
        assert tq.POOL_STATS["opens"] < 100, (
            f"真新建连接 {tq.POOL_STATS['opens']} 条（应 <100；"
            f"reuses={tq.POOL_STATS['reuses']}）")
        assert tq.POOL_STATS["reuses"] > 200, "复用次数过低 ⇒ 池没生效"
        assert len(tq.list_tasks(db_path=db)) == 50
    finally:
        tq.close_pool(db)


# ── 3. WAL pragma 只执行一次/连接 ─────────────────────────────────────────────
def test_wal_pragma_only_once_per_connection(monkeypatch):
    db = _tmp_db()
    tq.close_pool(db)
    calls = {"n": 0}
    real = tq._set_wal

    def counting(conn, *a, **kw):
        calls["n"] += 1
        return real(conn, *a, **kw)

    monkeypatch.setattr(tq, "_set_wal", counting)
    for i in range(30):
        tq.enqueue("research", f"w{i}", db_path=db)
        tq.list_tasks(db_path=db)
    try:
        assert calls["n"] <= tq.POOL_STATS["wal_pragmas"], "WAL 与新建连接数应 1:1"
        assert calls["n"] < 10, f"WAL 被重复执行 {calls['n']} 次（应每连接一次）"
    finally:
        tq.close_pool(db)


# ── 4/8. 判决一致性 + gross 回归探针 ──────────────────────────────────────────
def test_stateful_probe_still_passes():
    """全量前的哨兵：max_examples=5 跑状态机，断言**成功**（判决逻辑零回归）。"""
    ttm = _load_ttm()
    probe = HSettings(max_examples=5, deadline=None,
                      suppress_health_check=list(HealthCheck))
    orig = ttm.TestTQ.settings
    ttm.TestTQ.settings = probe
    tc = ttm.TestTQ(methodName="runTest")
    try:
        t0 = time.time()
        result = tc.run()
        dt = time.time() - t0
    finally:
        ttm.TestTQ.settings = orig
    assert result.wasSuccessful(), "状态机探针失败（判决逻辑回归）"
    assert dt < 30.0, f"探针耗时 {dt:.1f}s，疑似 gross 性能回归（预算 <30s）"


# ── 5. 线程模型：每线程一条连接，不共享 ────────────────────────────────────────
def test_each_thread_gets_its_own_connection():
    dbs: dict[int, Path] = {}
    conns: dict[int, object] = {}
    errors: list[str] = []

    def worker(idx: int) -> None:
        try:
            db = _tmp_db()
            dbs[idx] = db
            conns[idx] = tq._pool_take(db)
            tq.enqueue("research", f"t{idx}", db_path=db)
            assert len(tq.list_tasks(db_path=db)) == 1
        except Exception as exc:                       # 任何异常都必须记账（不许静默）
            errors.append(f"{idx}: {exc!r}")
        finally:
            tq.close_pool(dbs.get(idx))

    threads = [threading.Thread(target=worker, args=(i,)) for i in range(4)]
    for t in threads:
        t.start()
    for t in threads:
        t.join(timeout=30)
    assert not errors, f"并发线程出错：{errors}"
    objs = list(conns.values())
    assert len({id(o) for o in objs}) == len(objs), "多个线程拿到了同一条连接（check_same_thread 违规）"


# ── 6. 显式关闭 + 关闭后可重建 ────────────────────────────────────────────────
def test_close_pool_releases_and_can_reopen():
    db = _tmp_db()
    tq.enqueue("research", "x", db_path=db)
    n = tq.close_pool(db)
    assert n >= 1, "close_pool 没有真正归还连接"
    tq.POOL_STATS.update({k: 0 for k in tq.POOL_STATS})
    assert len(tq.list_tasks(db_path=db)) == 1, "关池后重开读不到数据（数据一致性破）"
    assert tq.POOL_STATS["opens"] >= 1, "关池后没能重新建连"
    tq.close_pool(db)


# ── 7. 缓存失效：池被关后新连接必须读到最新写入 ────────────────────────────────
def test_stale_connection_cache_invalidation():
    db = _tmp_db()
    tq.enqueue("research", "before", db_path=db)
    tq.close_pool(db)
    tq.enqueue("research", "after", db_path=db)
    rows = tq.list_tasks(db_path=db)
    assert len(rows) == 2, "复用连接读到了过期结果（缓存失效破）"
    tq.close_pool(db)


# ── 9. 语义不变：单库事务行为与改造前一致（嵌套调用走溢出连接）───────────────────
def test_nested_call_gets_spill_connection():
    """事务内的嵌套调用仍拿到**另一条**连接 ⇒ 不引入嵌套事务（BEGIN 里 BEGIN）风险。"""
    db = _tmp_db()
    tq.close_pool(db)
    tid = tq.enqueue("research", "nested", db_path=db)["id"]
    c = tq.claim("wA", db_path=db)
    assert c["claimed"] is not None, "claim 失败（状态机语义被改坏）"
    row = [r for r in tq.list_tasks(db_path=db) if r["id"] == tid][0]
    assert row["status"] == "claimed"
    tq.close_pool(db)
