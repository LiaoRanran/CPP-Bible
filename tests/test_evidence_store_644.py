"""644 C1 内容寻址存储单测（S1-1..S1-5）。"""
from __future__ import annotations

import os

import evidence_base_644 as base
import evidence_store_644 as c1


# S1-1：hash 计算正确（64 位 hex）
def test_hash_len():
    assert len(base.sha256_text("x")) == 64


# S1-2：存储路径正确（前 2 位分目录）
def test_path_format():
    eid = base.sha256_text("abc")
    assert c1.path_for(eid) == os.path.join(base.STORE_DIR, eid[:2], eid)


# S1-3：不可变 / 幂等（重复写入同内容，EvidenceID 相同、文件唯一）
def test_immutable_idempotent():
    rec = c1.store("c1 content", source_type="single_blog", grade="L4",
                   credibility=0.5, acquired_at="2026-09-26", acquisition_method="test")
    rec2 = c1.store("c1 content", source_type="single_blog", grade="L4",
                    credibility=0.5, acquired_at="2026-09-26", acquisition_method="test")
    assert rec.evidence_id == rec2.evidence_id
    assert os.path.exists(c1.path_for(rec.evidence_id))
    os.remove(c1.path_for(rec.evidence_id))


# S1-4：is_valid 对错误 id 返回 False
def test_is_valid():
    rec = c1.store("c1b", source_type="single_blog", grade="L4", credibility=0.5,
                   acquired_at="2026-09-26", acquisition_method="test")
    from dataclasses import replace
    assert not replace(rec, evidence_id="0" * 64).is_valid()
    os.remove(c1.path_for(rec.evidence_id))


# S1-5：selftest 通过
def test_selftest():
    assert c1.selftest() == 0
