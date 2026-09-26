"""642 A2 · anti_windup_642 单测（半饱和边界 / 预算边界 / 老化升级 / 灰度零损失）。编号 A2-1..A2-9。"""
from __future__ import annotations

import anti_windup_642 as A


# A2-1：半饱和边界（占用恰 50% ⇒ 正常；51% ⇒ 半饱和）
def test_half_saturation_boundary():
    assert A.queue_state(n=50, weekly_new=20)["level"] == "正常"
    assert A.queue_state(n=51, weekly_new=20)["level"] == "半饱和"
    assert A.occupancy_pct(50) == 50.0


# A2-2：预算边界（20/周 不超；21/周 超）
def test_budget_boundary():
    assert A.queue_state(n=10, weekly_new=20)["budget_exceeded"] is False
    assert A.queue_state(n=10, weekly_new=21)["budget_exceeded"] is True


# A2-3：超预算 ⇒ 冻结低优先级，高优先级不受影响
def test_budget_freezes_low_priority_only():
    st = A.queue_state(n=10, weekly_new=21)
    assert A.plan_admission("低", st)["frozen"] is True
    assert A.plan_admission("高", st)["frozen"] is False
    assert A.plan_admission("中", st)["queued_pending"] is True


# A2-4：老化边界（30 天不升；31 天升一级且解冻）
def test_aging_boundary_and_unfreeze():
    st = A.queue_state(n=10, weekly_new=21)
    assert A.plan_admission("低", st, 30.0)["upgraded"] is False
    p = A.plan_admission("低", st, 31.0)
    assert p["upgraded"] is True
    assert p["priority_out"] == "中"
    assert p["frozen"] is False


# A2-5：升级顶格不越界
def test_bump_caps_at_top():
    assert A.bump("高") == "高"
    assert A.bump("低") == "中"
    assert A.bump("未知") == "未知"


# A2-6：饱和 ⇒ 中优先级也冻结
def test_saturated_freezes_mid():
    st = A.queue_state(n=101, weekly_new=21)
    assert st["level"] == "饱和"
    assert A.plan_admission("中", st)["frozen"] is True
    assert A.plan_admission("高", st)["frozen"] is False


# A2-7：正常队列照常入队
def test_normal_queue_admits():
    st = A.queue_state(n=1, weekly_new=1)
    p = A.plan_admission("中", st)
    assert p["queued_pending"] is False and p["frozen"] is False


# A2-8：等待代理单调 —— 越靠前等待越久
def test_wait_proxy_is_monotonic():
    waits = [A.estimate_wait_days(i, 65) for i in range(65)]
    assert waits == sorted(waits, reverse=True)
    assert A.estimate_wait_days(0, 65) == 22.8


# A2-9：实跑只标记不改文件 + --check 自检
def test_replay_is_readonly_and_selftest():
    import hashlib
    before = hashlib.sha256(open(A.QUEUE, "rb").read()).hexdigest()
    r = A.replay_queue()
    after = hashlib.sha256(open(A.QUEUE, "rb").read()).hexdigest()
    assert before == after, "上岗报告不得改写人审队列文件"
    assert r["n"] >= 1 and r["n_frozen"] <= r["n"]
    assert A.selftest() == 0
