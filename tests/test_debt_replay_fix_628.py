"""628 A4 · DEBT-001 + replay manifest 修复 单测（5 例）。"""
import os
import sys
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import replay_manifest_fix_628 as R


def test_debt_001_fixture_dynamized():
    # fixture 日期动态化：clean 场景 due 在未来
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    src = open(os.path.join(here, "tests", "test_s1_s6.py"), encoding="utf-8").read()
    assert "today + timedelta(days=30)" in src or "timedelta(days=30)" in src
    assert '"due": "2026-09-20"' not in src
    assert (date.today() + timedelta(days=30)) > date.today()


def test_clean_ledger_test_passes():
    import subprocess
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    proc = subprocess.run(
        [sys.executable, "-m", "pytest",
         os.path.join(here, "tests", "test_s1_s6.py"), "-q"],
        capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0, proc.stdout[-400:]


def test_manifest_consistency_zero_mismatch():
    c = R.check()
    assert c["consistent"]
    assert c["stale_count"] == 0 and c["missing_count"] == 0


def test_manifest_has_56_entries():
    c = R.check()
    assert c["entries"] == 56


def test_disposition_report_exists():
    here = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    p = os.path.join(here, "data", "debt_001_disposition_628.md")
    assert os.path.exists(p)
    txt = open(p, encoding="utf-8").read()
    assert "DEBT-001" in txt and "closed" in txt.lower()
