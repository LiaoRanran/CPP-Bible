"""644 B1 证据等级体系单测（G1-1..G1-6）。"""
from __future__ import annotations

import evidence_base_644 as base
import evidence_grading_644 as b1


# G1-1：映射正确（多编译器实测=L1，单编译器=L2，cppreference=L3，AI=L5）
def test_grade_mapping():
    assert b1.grade_existing_evidence  # 函数存在
    assert base.grade_evidence_record("compiler_run", compilers=2)[0] == "L1"
    assert base.grade_evidence_record("compiler_run", compilers=1)[0] == "L2"
    assert base.grade_evidence_record("cppreference")[0] == "L3"
    assert base.grade_evidence_record("ai_generated")[0] == "L5"


# G1-2：kind → source_type 映射
def test_source_type_mapping():
    assert base.source_type_from_ev("run", 1) == "compiler_run"
    assert base.source_type_from_ev("traceable_argument") == "multi_blog"
    assert base.source_type_from_ev("weird") == "single_blog"


# G1-3：可信度在 [0,1] 且 L1>L5
def test_credibility_order():
    _, c1 = base.grade_evidence_record("compiler_run", compilers=2)
    _, c5 = base.grade_evidence_record("ai_generated")
    assert 0.0 <= c1 <= 1.0 and 0.0 <= c5 <= 1.0
    assert c1 > c5


# G1-4：现有证据全部分级且等级合法
def test_grade_existing_valid():
    recs = b1.grade_existing_evidence()
    assert len(recs) > 0
    assert all(r["grade"] in base.GRADES for r in recs)


# G1-5：分布完整（求和==总量）
def test_distribution_sum():
    recs = b1.grade_existing_evidence()
    dist = b1.grade_distribution(recs)
    assert sum(dist.values()) == len(recs)


# G1-6：selftest 通过
def test_selftest():
    assert b1.selftest() == 0
