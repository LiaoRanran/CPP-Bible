"""608 D2 · slow 测试性能回归锁（锁定 test_task_queue_stateful 跑批时间）。

两个锁：
  * 预算锁：`TestTQ.settings.max_examples == 100`（608 D1 定的最小样例预算下限），
    防止被静默调大 ⇒ 跑批时间失控（608 D0 已证明运行时间与样例数近似线性）；
  * 探针：用 `max_examples=5` 跑一遍状态机，断言成功且 << 全量预算（抓库级 gross 回归，
    如 task_queue 连接复用改造后意外变慢 / 变快 —— 见 data/slow_performance_profile.md 登记的待分析项）。

本锁不重跑 70s 全量（避免 flaky 与拖慢门禁）；预算锁是无状态硬断言，探针只用 5 例。
"""
from __future__ import annotations

import pytest

pytestmark = pytest.mark.slow

import importlib.util
import time
from pathlib import Path

from hypothesis import HealthCheck
from hypothesis import settings as HSettings

_HERE = Path(__file__).resolve().parent


def _load_ttm():
    spec = importlib.util.spec_from_file_location(
        "ttm_608", _HERE / "test_task_queue_stateful.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def test_tq_example_budget_lock():
    """预算锁：max_examples 必须停在 608 D1 定的下限 100（防静默调大拖慢全量）。"""
    ttm = _load_ttm()
    got = ttm.TestTQ.settings.max_examples
    assert got == 100, (
        f"TestTQ max_examples 被改：{got}（应为 100，见 608 D0/D1 最小样例预算）")


def test_tq_perf_probe():
    """探针：max_examples=5 跑状态机，断言成功且 < 30s（抓 gross 性能回归）。"""
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
    assert result.wasSuccessful(), "状态机探针运行失败（判决逻辑回归）"
    assert dt < 30.0, f"状态机探针耗时 {dt:.1f}s，疑似 gross 性能回归（预算 <30s）"
