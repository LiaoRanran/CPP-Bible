"""645 B5 证据等级单测（fast 组：真实证据库分级）。"""
import sys

sys.path.insert(0, "tools")

import evidence_grading_645 as b5


def test_selftest_passes():
    assert b5.selftest() == 0


def test_grade_all_has_real_evidence():
    res = b5.grade_all()
    # 真实数据：现有 EV 卡（56）+ 本批 store（≥28）→ 远超目标 30
    assert res["total"] >= 30, "应真实分级 ≥30 条证据"
    assert res["grade_distribution"]["L1"] + res["grade_distribution"]["L2"] > 0


def test_grade_levels_valid():
    for g in b5.grade_all()["graded"]:
        assert g["grade"] in b5.GRADES
