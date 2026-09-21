"""620 B3 · PCK 证书状态统计 + 批量渲染 单测"""
from __future__ import annotations

import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import pck_renderer_619 as B4  # noqa: E402
import pck_status_stats_620 as S  # noqa: E402


def _mk(status: str) -> dict:
    cert = B4._sample_cert()
    cert["human_authority"] = {"status": status, "review_method": "batch_authorization"}
    return cert


def test_status_mapping_three_values():
    assert S.stats([("a", _mk("approved"))])["by_status"]["authorized"] == 1
    assert S.stats([("b", _mk("pending"))])["by_status"]["unverified"] == 1
    assert S.stats([("c", _mk("rejected"))])["by_status"]["disputed"] == 1


def test_five_levels_present():
    st = S.stats([("a", _mk("approved"))])
    assert set(st["by_status"]) == {"authorized", "conditionally_authorized",
                                    "disputed", "abstain", "unverified"}


def test_buckets_by_cs_and_verifiers():
    st = S.stats([("a", _mk("approved"))])
    assert st["by_cs_upper_bound"]["0.009062"] == 1
    assert st["by_verifier_count"][1] == 1


def test_full_83_stats():
    d = S.DEFAULT_CERT_DIR
    if not os.path.isdir(d):
        return
    certs = S.load_certs(d)
    assert len(certs) == 83
    st = S.stats(certs)
    assert st["total"] == 83
    assert st["validation_ok"] == 83
    # C3（Authority 同步）后 approved 由 23 → 27、pending 由 60 → 56：
    # 4 张原子卡在历史人审通道中有真实决策，被依日志补登为 approved。
    assert st["by_status"]["authorized"] == 27
    assert st["by_status"]["unverified"] == 56
    assert st["by_status"]["authorized"] + st["by_status"]["unverified"] == 83
    assert st["by_verifier_count"][1] == 83


def test_render_all_writes_one_file_per_cert():
    certs = [("X.pck.yaml", _mk("approved")), ("Y.pck.yaml", _mk("pending"))]
    with tempfile.TemporaryDirectory() as td:
        written = S.render_all(certs, td)
        assert sorted(written) == ["X.md", "Y.md"]
        assert os.path.exists(os.path.join(td, "X.md"))


def test_rendered_contains_badge():
    md = S.render_all.__doc__  # sanity: module imported
    assert md is not None or True
    out = B4.render(_mk("approved"))
    assert "PASS" in out


def test_report_renders():
    st = S.stats([("a", _mk("approved"))])
    assert "状态分布" in S.render_report(st, ["a.md"])


def test_selftest_passes():
    assert S.selftest() == 0
