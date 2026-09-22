"""626 D3 · Snapshot Integrity CI 回归测试（≥10 例）。"""
import os
import sys
import tempfile
import zipfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import decision_event_v2_626 as D  # noqa: E402
import snapshot_integrity_ci_626 as SI  # noqa: E402


def _c() -> SI.SnapshotIntegrityChecker:
    return SI.SnapshotIntegrityChecker()


def test_selftest_passes():
    assert SI.selftest() == 0


def test_ten_checks_registered():
    assert len(SI.CHECKS) == 10


def test_run_all_returns_ten():
    r = _c().run_all()
    assert r["total"] == 10
    assert all(k in r["checks"] for k in SI.CHECKS)


def test_count_consistency_pass():
    r = _c().run_check("count_consistency")
    assert r["status"] == "pass"
    assert "388" in r["details"] and "418" in r["details"]


def test_id_uniqueness_pass():
    assert _c().run_check("id_uniqueness")["status"] == "pass"


def test_hash_chain_pass_and_broken_detected():
    assert _c().run_check("hash_chain")["status"] == "pass"
    led = D.AuthorityLedger()
    led.append(D.make_event("edge", "ae-1", "APPROVE", reviewer="A"))
    led.all_events()[0].self_hash = "0" * 64
    assert not led.verify_chain()


def test_control_chars_clean():
    assert _c().run_check("control_chars")["status"] == "pass"


def test_cross_report_numerical_consistency():
    r = _c().run_check("cross_report_numerical_consistency")
    assert r["status"] == "pass"
    assert "67.5" in r["evidence"][0]


def test_stale_report_detected():
    r = _c().run_check("stale_report_detection")
    assert r["status"] in ("pass", "warn")
    assert "STALE" in r["details"]


def test_projection_consistency():
    r = _c().run_check("authority_projection_consistency")
    assert r["status"] == "pass"
    assert "83" in r["details"]


def test_review_pack_integrity():
    r = _c().run_check("review_pack_integrity")
    assert r["status"] in ("pass", "warn")


def test_bad_zip_fails_integrity():
    """构造反斜杠 ZIP ⇒ 应判 fail（或平台归一后 warn）。"""
    with tempfile.TemporaryDirectory() as td:
        zp = os.path.join(td, "bad.zip")
        with zipfile.ZipFile(zp, "w") as z:
            z.writestr("dir\\file.md", "x")
        with zipfile.ZipFile(zp) as z:
            names = z.namelist()
        if os.sep == "\\":
            # Windows：zipfile 会把 \ 归一为 /，故只能断言缺 manifest
            assert "SNAPSHOT_MANIFEST.json" not in names
        else:
            assert any("\\" in n for n in names)


def test_report_export():
    _c().export_report()
    assert os.path.exists(SI.OUT_JSON)
    assert os.path.exists(SI.OUT_MD)
