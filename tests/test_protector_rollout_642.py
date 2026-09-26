"""642 A6 · protector_rollout_642 单测（联调不互相干扰 / 标记可叠加 / 回滚有效 / 零漂移）。
编号 A6-1..A6-7。
"""
from __future__ import annotations

import protector_rollout_642 as R
import pytest


# A6-1：联调**零生产判决被改变**（5 个 CORE_TOOLS + 账本 + 队列 + 卡清单指纹前后一致）
def test_rollout_has_zero_drift():
    r = R.rollout()
    assert r["zero_drift"] is True
    assert r["drift"] == []
    assert r["critical_changed"] == 0


# A6-2：五个保护器都被联调到，且各有触发计数
def test_all_five_protectors_are_exercised():
    r = R.rollout()
    assert set(r["triggers"]) == set(R.PROTECTORS)
    assert r["triggers"]["A1"]["卡片"] == 23
    assert r["triggers"]["A2"]["队列"] >= 1
    assert r["triggers"]["A3"]["历史判决"] == 452


# A6-3：五个保护器的键空间**互不重叠**（联调不互相干扰的结构保证）
def test_mark_namespaces_are_disjoint():
    all_keys = [k for p in R.PROTECTORS for k in R.MARK_NAMESPACES[p]]
    assert len(all_keys) == len(set(all_keys))
    assert set(R.PROTECTORS) == set(R.MARK_NAMESPACES)


# A6-4：标记可叠加（五键全在、互不覆盖）
def test_marks_are_additive():
    merged: dict = {}
    for i, pid in enumerate(R.PROTECTORS):
        merged = R.merge_marks(merged, {R.MARK_NAMESPACES[pid][0]: i})
    assert len(merged) == 5
    assert merged == {R.MARK_NAMESPACES[p][0]: i for i, p in enumerate(R.PROTECTORS)}


# A6-5：同名键冲突 ⇒ 抛错（**不静默覆盖**）
def test_mark_conflict_is_loud():
    with pytest.raises(R.MarkConflictError):
        R.merge_marks({"conflict_flag": True}, {"conflict_flag": False})
    # 同值不算冲突（幂等）
    assert R.merge_marks({"conflict_flag": True},
                         {"conflict_flag": True})["conflict_flag"] is True


# A6-6：回滚方案有效（按保护器精确摘除 ⇒ 逐个到底即回到灰度前）
def test_rollback_is_effective_and_precise():
    r = R.rollout()
    marks = dict(r["marks"])
    for pid in R.PROTECTORS:
        other_keys = {k for p in R.PROTECTORS if p != pid for k in R.MARK_NAMESPACES[p]}
        before_others = {k: v for k, v in marks.items() if k in other_keys}
        marks = R.rollback_marks(marks, pid)
        after_others = {k: v for k, v in marks.items() if k in other_keys}
        assert before_others == after_others, f"回滚 {pid} 动到了别的保护器"
        assert not (set(R.MARK_NAMESPACES[pid]) & set(marks))
    assert marks == {}


# A6-7：风险汇总覆盖五个保护器 + --check 自检
def test_risk_summary_and_selftest():
    risks = R.risk_summary()
    assert {x["protector"] for x in risks} == set(R.PROTECTORS)
    assert all(x["rollback"] for x in risks)
    assert R.selftest() == 0
