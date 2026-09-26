"""644 C3 证据完整性与漂移检测单测（I3-1..I3-5）。"""
from __future__ import annotations

from dataclasses import replace

import evidence_base_644 as base
import evidence_integrity_644 as c3


# I3-1：已知漂移必检出（错误 id → is_valid False）
def test_hash_mismatch():
    rec = base.store_evidence("c3 content", source_type="single_blog", grade="L4",
                             credibility=0.5, acquired_at="2026-09-26",
                             acquisition_method="test")
    bad = replace(rec, evidence_id="0" * 64)
    assert not bad.is_valid()
    os_removed = c3  # 占位避免未使用告警
    assert os_removed is not None
    import os as _os
    _os.remove(base.store_path(rec.evidence_id))


# I3-2：引用但缺失检测
def test_referenced_missing():
    fake = {"links": [], "by_card": {}, "by_evidence": {"deadbeef" * 8: ["C1"]}}
    rm = c3.check_referenced_but_missing(fake)
    assert any(m["kind"] == "referenced_missing" for m in rm)


# I3-3：无 URL 重取不崩溃（no_url）
def test_no_url_refetch():
    rec = replace(base.EvidenceRecord(evidence_id="x" * 64, content="c",
                                     source_type="single_blog", grade="L4",
                                     credibility=0.5, acquired_at="2026-09-26",
                                     acquisition_method="test"), source_url=None)
    r = c3.refetch_compare(rec)
    assert r["kind"] == "no_url"


# I3-4：网络降级（无效 URL → fetch_failed，不崩溃）
def test_network_degradation():
    rec = replace(base.EvidenceRecord(evidence_id="y" * 64, content="c",
                                     source_type="single_blog", grade="L4",
                                     credibility=0.5, acquired_at="2026-09-26",
                                     acquisition_method="test"),
                 source_url="http://127.0.0.1:0/impossible")
    r = c3.refetch_compare(rec)
    assert r["kind"] == "fetch_failed"


# I3-5：selftest 通过
def test_selftest():
    assert c3.selftest() == 0
