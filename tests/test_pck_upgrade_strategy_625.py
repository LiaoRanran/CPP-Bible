"""625 D4 · PCK 提升策略设计（只设计不代签）回归测试（≥4 例）。"""
import glob
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import pck_upgrade_strategy_625 as P  # noqa: E402

CERT_DIR = os.path.join(ROOT, "data", "pck", "certificates")


def test_selftest_passes():
    assert P.selftest() == 0


def test_current_rate_below_target():
    a = P.analyze()
    assert a["rate"] < P.TARGET_RATE
    assert a["need_approve_more"] >= 1


def test_no_cert_modified():
    before = sorted(glob.glob(os.path.join(CERT_DIR, "*.pck.yaml")))
    P.analyze()
    P.render(P.analyze())
    after = sorted(glob.glob(os.path.join(CERT_DIR, "*.pck.yaml")))
    assert before == after


def test_strategies_well_formed():
    a = P.analyze()
    txt = P.render(a)
    for s in ("S1", "S2", "S3", "S4"):
        assert s in txt
    assert "只设计，不代签" in txt


def test_report_exists():
    p = os.path.join(ROOT, "data", "pck_upgrade_strategy_625.md")
    assert os.path.exists(p) and os.path.getsize(p) > 600
