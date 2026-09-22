"""625 A3 · CI pytest 红因修复回归测试（≥3 例）。"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))


def test_governance_manifest_verified():
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "governance_doc_guard.py"),
                        "verify"], cwd=ROOT, capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr


def test_poison_exemptions_counts_updated():
    import poison_drill as pd
    ex = pd.load_exemptions()
    legacy = [k for k, v in ex.items() if v["redteam_seen"] == "legacy"]
    backed = [k for k, v in ex.items() if v["reason_verified"] == "backed"]
    assert len(legacy) == 27
    assert len(backed) == 28
    assert all(v["reason_verified"] != "missing-test" for v in ex.values())
    assert all(v["reason_verified"] != "weak-test" for v in ex.values())


def test_coverage_total_is_67():
    import poison_drill as pd
    rep = pd.coverage_report()
    assert rep["total"] == 67
    assert len(rep["legacy_exempt"]) == 27


def test_report_exists():
    p = os.path.join(ROOT, "data", "ci_pytest_fix_625.md")
    assert os.path.exists(p) and os.path.getsize(p) > 500
