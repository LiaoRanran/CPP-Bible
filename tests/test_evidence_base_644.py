"""644 共享基础模块单测（B0-1..B0-8）。"""
from __future__ import annotations

import os

import evidence_base_644 as base


# B0-1：内容寻址 hash 稳定且长度正确
def test_sha256_stable():
    assert base.sha256_text("hello") == base.sha256_text("hello")
    assert len(base.sha256_text("x")) == 64


# B0-2：相同内容 → 相同 EvidenceID；不同内容 → 不同
def test_evidence_id_unique():
    a = base.sha256_text("abc")
    b = base.sha256_text("abd")
    assert a != b


# B0-3：等级枚举与描述完整
def test_grades_complete():
    assert base.GRADES == ("L1", "L2", "L3", "L4", "L5")
    for g in base.GRADES:
        assert g in base.GRADE_DESC and g in base.GRADE_CREDIBILITY


# B0-4：source_type → 等级映射（多编译器实测=L1，单编译器=L2，标准=L2）
def test_grade_from_source():
    assert base.grade_from_source("compiler_run", compilers=2)[0] == "L1"
    assert base.grade_from_source("compiler_run", compilers=1)[0] == "L2"
    assert base.grade_from_source("iso_standard")[0] == "L2"
    assert base.grade_from_source("cppreference")[0] == "L3"
    assert base.grade_from_source("single_blog")[0] == "L4"
    assert base.grade_from_source("ai_generated")[0] == "L5"


# B0-5：可信度在 [0,1] 且 L1 高于 L5
def test_credibility_range_and_order():
    _, c1 = base.grade_from_source("compiler_run", compilers=2)
    _, c5 = base.grade_from_source("ai_generated")
    assert 0.0 <= c1 <= 1.0 and 0.0 <= c5 <= 1.0
    assert c1 > c5


# B0-6：解析 frontmatter（真实卡，数量按文件系统动态校验）
def test_parse_frontmatter():
    atoms = base.list_atoms()
    expected = 0
    for domain in ("conc", "hist", "lang", "mem", "ub"):
        d = os.path.join(base.ATOMS_DIR, domain)
        if os.path.isdir(d):
            expected += sum(1 for fn in os.listdir(d) if fn.endswith(".md"))
    assert len(atoms) == expected and expected >= 25
    a0 = atoms[0]
    assert "id" in a0["meta"] and isinstance(a0["evidence_refs"], list)


# B0-7：现有证据文件可列且含 serves
def test_list_existing_evidence():
    evs = base.list_existing_evidence()
    assert len(evs) > 0
    assert all("id" in e for e in evs)


# B0-8：selftest 通过
def test_selftest():
    assert base.selftest() == 0
