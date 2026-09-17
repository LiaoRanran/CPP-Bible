"""559 Part B：读真实仓库工件状态的测试，与 replay **同一把锁**串行——回归锁。

背景（558 验收暴露）：`replay_card` 校验一卡是「删旧工件 → 重生成 → 比 sha → 还原」，
期间 `Examples/atoms/*.asm` **瞬时**不存在/内容不同。若另一个 worker 恰在此时读它
（golden_lock 的门禁扫描 / writer_selfcheck 的 WC-01「磁盘 sha == 卡值」）就会假红。
559 实测探针（并发起一个真 replay，同时跑 `golden_lock check --json`）：**3/3 非 pass**。

508 已证 `--dist loadgroup` + `xdist_group("serial")` 在本版 xdist **不生效**（调度器读不到
marker、测试仍散到各 worker），故本批不重走那条死路，改用"真互斥"：`replay_serial` fixture
复用 replay 自己的 `build/.replay_lock`，拿不到锁就**带因 skip**（绝不假失败）。

本文件锁两件事：① 锁契约本身（取到⇒锁在 / 释放⇒锁无 / 被占⇒超时⇒skip 的依据）；
② 三个读真实仓库状态的用例**必须**挂着 `replay_serial`（谁把它删掉就红）。
"""
from __future__ import annotations

import importlib
import inspect
import os
import time
from pathlib import Path

import atom_evidence_replay as replay
import pytest

SENSITIVE = (
    # 只列**自身不跑 replay** 的读敏感用例：挂 replay_serial 期间会独占 `build/.replay_lock`，
    # 若该用例自己也要跑 replay（如 `golden_lock check` 内部逐卡调 `replay_card`），
    # 外层持锁会把它逼成 `infra_error:replay_busy`（每卡等 120s）⇒ 反而变慢/变红。
    ("test_json_output", "test_gate_engine_json"),
    ("test_writer_selfcheck", "test_stock_zero_false_positive"),
    # 559 实测补入：它跑**全库门禁**（逐变体 `ge.run()`），误跑法下冻结集合会多出
    # `EV-ARTIFACT-FILE-EXISTS`（并发 replay 的工件瞬时态）⇒ 假红；只用 M3/M4（不跑 replay）
    # ⇒ 持锁不自锁。
    ("test_mutation_fuzz", "test_548_perf_conclusions_unchanged"),
)


def test_replay_serial_fixture_contract():
    """正例：取到锁 ⇒ 锁文件在（并发 replay 被挡在改写之前）；释放 ⇒ 锁无。
    反例：锁已被占（本进程 pid，存活 ⇒ 不会被当僵尸接管）⇒ `_acquire_replay_lock` 超时
    ⇒ fixture 据此 **skip**（带因跳过，不是假失败）。
    """
    lock = replay._REPLAY_LOCK
    if lock.exists():
        pytest.skip("锁被占（有 replay 在跑）⇒ 本用例不适用")
    replay._acquire_replay_lock(wait_timeout=0.6)
    try:
        assert lock.exists(), "持锁期间锁文件必须在（否则并发 replay 不会被挡住）"
    finally:
        replay._release_replay_lock()
    assert not lock.exists(), "释放后锁文件不得残留（残留会变成僵尸锁）"

    lock.parent.mkdir(exist_ok=True)
    lock.write_text(f"{os.getpid()}\n{time.time()}\n", encoding="utf-8")
    try:
        t0 = time.time()
        with pytest.raises(TimeoutError):
            replay._acquire_replay_lock(wait_timeout=0.6, stale_after=300.0)
        assert time.time() - t0 < 30, "超时必须由 wait_timeout 决定，不是无限等"
    finally:
        lock.unlink(missing_ok=True)
    assert not lock.exists()


def test_try_unlink_lock_tolerates_oserror(monkeypatch: pytest.MonkeyPatch,
                                           tmp_path: Path):
    """反例（559 B 真 bug）：删除锁文件抛 `OSError` 时，`_try_unlink_lock` 返回 False、
    释放函数**绝不抛** —— 否则一次释放失败就把整个 `replay_card` 崩掉
    （实测：`golden_lock check` 因此崩、无 JSON 输出 ⇒ `test_golden_lock_json` 假红）。

    本环境有 safe-delete 拦截层（删除改道 trash，并发下报
    `Some operations were aborted`），故这条不是纸面推演，是实测故障的回归锁。
    """
    class _Boom:
        def unlink(self, missing_ok: bool = False) -> None:
            raise OSError("[safe-delete] 操作失败：Some operations were aborted")

    monkeypatch.setattr(replay, "_REPLAY_LOCK", _Boom())
    assert replay._try_unlink_lock() is False, "删不掉必须返回 False，不是抛异常"
    replay._release_replay_lock()                     # 绝不抛（残留锁交给 pid/陈旧接管自愈）


def test_try_unlink_lock_removes_real_file(monkeypatch: pytest.MonkeyPatch,
                                           tmp_path: Path):
    """正例：正常文件能删掉并返回 True（不是把"删不了"当常态）。"""
    f = tmp_path / ".replay_lock"
    f.write_text("x", encoding="utf-8")
    monkeypatch.setattr(replay, "_REPLAY_LOCK", f)
    assert replay._try_unlink_lock() is True
    assert not f.exists()


def test_sensitive_read_tests_are_serialized():
    """回归锁：三个读真实仓库工件状态的用例必须挂 `replay_serial`（删掉即红）。"""
    missing: list[str] = []
    for mod_name, fn_name in SENSITIVE:
        mod = importlib.import_module(mod_name)
        fn = getattr(mod, fn_name)
        if "replay_serial" not in inspect.signature(fn).parameters:
            missing.append(f"{mod_name}::{fn_name}")
    assert not missing, f"这些用例读真实仓库状态，必须与 replay 同锁串行：{missing}"


def test_two_phase_commands_documented():
    """权威两阶段跑法（fast 并行 + slow 串行）必须写在 pyproject 注释里，别静默丢。"""
    pyproject = Path(__file__).resolve().parent.parent / "pyproject.toml"
    txt = pyproject.read_text(encoding="utf-8")
    assert 'pytest -m "not slow" -n auto' in txt, "pyproject 缺 fast 并行阶段命令"
    assert "pytest -m slow -n0" in txt, "pyproject 缺 slow 串行阶段命令"
