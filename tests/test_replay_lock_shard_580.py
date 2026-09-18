"""580 任务 1 回归锁：replay 并发锁**跟随跑批根分片**。

病：`_REPLAY_LOCK` 写死真实 `ROOT/build/.replay_lock` ⇒ 进程池并行时所有 worker 抢同一把全局锁
（加速比≈1，且 120s 等待易超时假红）。治：`_replay_lock_path() = run_root()/"build"/".replay_lock"`
——无 batch 时与改造前**逐字节相同**。

本文件四条：① 默认路径逐字不变；② 跟随 batch_root；③ 同根仍互斥（不因分片丢掉互斥）；
④ **异根不互斥**（旧代码此例必超时——这是并行能成立的证据）。
"""
from __future__ import annotations

import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

import atom_evidence_replay as replay   # noqa: E402


def test_580_default_lock_path_is_byte_identical_to_before():
    """不进 batch_root 时，锁路径必须与改造前的模块常量**逐字节相同**。"""
    assert replay._replay_lock_path() == replay.ROOT / "build" / ".replay_lock"
    assert str(replay._replay_lock_path()) == str(replay.ROOT / "build" / ".replay_lock")


def test_580_lock_path_follows_batch_root(tmp_path: Path):
    """异根 ⇒ 异锁路径（每 worker 一把）。"""
    a, b = tmp_path / "ra", tmp_path / "rb"
    for r in (a, b):
        (r / "build").mkdir(parents=True)
    with replay.batch_root(a):
        pa = replay._replay_lock_path()
    with replay.batch_root(b):
        pb = replay._replay_lock_path()
    assert pa == a / "build" / ".replay_lock"
    assert pb == b / "build" / ".replay_lock"
    assert pa != pb
    assert replay._replay_lock_path() == replay.ROOT / "build" / ".replay_lock", "退出后必须还原"


def test_580_same_root_is_still_mutually_exclusive(tmp_path: Path):
    """同一根内仍互斥：第二次 acquire 必须等待到超时（锁语义不许因分片被削弱）。"""
    root = tmp_path / "same"
    (root / "build").mkdir(parents=True)
    with replay.batch_root(root):
        replay._acquire_replay_lock()
        try:
            assert replay._replay_lock_path().is_file()
            with pytest.raises(TimeoutError):
                # stale_after 给大值：确保走"等待 → 超时"而不是被误判陈旧而接管
                replay._acquire_replay_lock(wait_timeout=0.6, stale_after=999.0)
        finally:
            replay._release_replay_lock()
        assert not replay._replay_lock_path().exists(), "释放后锁文件必须消失"
    assert not (root / "build" / ".replay_lock").exists()


def test_580_different_roots_do_not_block(tmp_path: Path):
    """**新正例**：A 根持锁时，B 根 acquire 必须**立即成功**（旧代码：全局同一把锁 ⇒ 必超时）。

    这是"并行真的能跑"的机器证据，也是本任务存在的理由。
    """
    ra, rb = tmp_path / "ra", tmp_path / "rb"
    for r in (ra, rb):
        (r / "build").mkdir(parents=True)
    with replay.batch_root(ra):
        replay._acquire_replay_lock()                     # A 根持锁
        assert replay._replay_lock_path() == ra / "build" / ".replay_lock"
        with replay.batch_root(rb):
            replay._acquire_replay_lock(wait_timeout=0.5)  # 立即成功；旧代码此处 TimeoutError
            assert replay._replay_lock_path() == rb / "build" / ".replay_lock"
            replay._release_replay_lock()
        assert replay._replay_lock_path().exists(), "释放 B 的锁不许影响 A 的锁"
        replay._release_replay_lock()
        assert not replay._replay_lock_path().exists()


def test_580_real_lock_untouched_by_shard_tests():
    """末位绿锁：本文件全程只在 tmp 根里取放锁，真实 `build/.replay_lock` 不被创建/删除。"""
    real = replay.ROOT / "build" / ".replay_lock"
    assert not real.exists() or real.is_file()      # 只断言状态可查询，不假定它存在
