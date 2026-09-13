"""470 P0-G1 回归锁（452 E09）：replay 并发隔离锁。"""
from __future__ import annotations

import os
import time
from pathlib import Path

import pytest

import atom_evidence_replay as replay


@pytest.fixture()
def lock(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    p = tmp_path / ".replay_lock"
    monkeypatch.setattr(replay, "_REPLAY_LOCK", p)
    return p


def test_acquire_release(lock: Path):
    replay._acquire_replay_lock()
    assert lock.is_file(), "取锁后锁文件必须存在"
    replay._release_replay_lock()
    assert not lock.exists()


def test_stale_lock_taken_over(lock: Path, monkeypatch: pytest.MonkeyPatch):
    """陈旧锁（mtime 超 stale_after）自动接管——进程被杀不永久锁死。"""
    lock.write_text("99999", encoding="utf-8")
    past = time.time() - 3600
    os.utime(lock, (past, past))
    replay._acquire_replay_lock(wait_timeout=5, stale_after=600)
    assert lock.is_file()
    replay._release_replay_lock()


def test_busy_lock_times_out(lock: Path):
    """活锁被占用：短等待必须抛 TimeoutError，且不得接管活锁（fail-closed）。"""
    replay._acquire_replay_lock(wait_timeout=60, stale_after=3600)
    try:
        with pytest.raises(TimeoutError):
            replay._acquire_replay_lock(wait_timeout=0.6, stale_after=3600)
        assert lock.is_file(), "活锁不得被短等待接管"
    finally:
        replay._release_replay_lock()


def test_replay_card_returns_infra_when_busy(lock: Path, tmp_path: Path,
                                             monkeypatch: pytest.MonkeyPatch):
    """锁被占用时 replay_card 返回 infra_error:replay_busy（不崩溃、不假失败）。"""
    monkeypatch.setattr(replay, "ROOT", tmp_path)
    card = tmp_path / "EV-B.md"
    card.write_text("---\nid: EV-B\ncommand: g++ a.cpp\nartifact: a.asm\n"
                    "artifact_sha256: " + "0" * 64 + "\n"
                    "actual:\n  run_match_file: fx.out\n  run_match_keys: [k]\n"
                    "---\n", encoding="utf-8")
    monkeypatch.setattr(replay, "_LOCK_WAIT_SEC", 0.6)
    monkeypatch.setattr(replay, "_LOCK_STALE_SEC", 3600.0)
    replay._acquire_replay_lock(wait_timeout=60, stale_after=3600)
    try:
        verdict, log = replay.replay_card(card, do_sanitizer=False)
        assert verdict == "infra_error:replay_busy", "\n".join(log)
    finally:
        replay._release_replay_lock()


def test_lock_serializes_processes(lock: Path, tmp_path: Path):
    """真并发：两进程各取锁——第二个必须等第一个释放（判据=获锁时刻间隔）。"""
    import subprocess
    import sys
    script = (
        "import sys, time\n"
        "sys.path.insert(0, r'%s')\n"
        "import atom_evidence_replay as replay\n"
        "from pathlib import Path\n"
        "replay._REPLAY_LOCK = Path(r'%s')\n"
        "replay._acquire_replay_lock(wait_timeout=30, stale_after=3600)\n"
        "print(time.time(), flush=True)\n"
        "time.sleep(1.5)\n"
        "replay._release_replay_lock()\n" % (str(Path(replay.__file__).parent), str(lock)))
    ps = [subprocess.Popen([sys.executable, "-c", script],
                           stdout=subprocess.PIPE, text=True) for _ in range(2)]
    outs = [p.communicate(timeout=60)[0].strip() for p in ps]
    assert all(p.returncode == 0 for p in ps), f"并发进程失败：{outs}"
    times = sorted(float(o) for o in outs if o)
    assert len(times) == 2, f"两个进程都应获锁：{outs}"
    assert times[1] - times[0] >= 1.3, \
        f"两进程必须串行（获锁间隔 {times[1] - times[0]:.2f}s < 持锁时间）"
