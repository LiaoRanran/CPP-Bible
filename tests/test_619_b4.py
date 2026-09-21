"""619 B4 单测：PCK 证书渲染器（tools/pck_renderer_619.py）

验证：渲染徽标、诚实注释、负向测试表、含错证书 FAIL、--check 自检。不写盘。
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import pck_renderer_619 as B4  # noqa: E402


def _sample():
    return {
        "schema_version": B4.B2.SCHEMA_VERSION,
        "claim": {"id": "X", "statement": "s", "domain": "conc", "type": "observation"},
        "evidence": [{"type": "replay", "ref": "evidence/conc/EV-X.md"}],
        "negative_tests": [{"mutation_id": "a|M1|p", "result": "blocked"}],
        "verifiers": [{"name": "gate_engine", "result": "pass"}],
        "human_authority": {"status": "approved", "review_method": "batch_authorization"},
        "uncertainty": {"cs_upper_bound": 0.009062, "estimand": "L1"},
        "provenance": {"commit": "abc", "first_authorized_at": "2026-09-12"},
    }


def test_render_has_title_and_badge():
    md = B4.render(_sample())
    assert "# PCK 证书" in md
    assert "✅ PASS" in md


def test_render_honest_notes():
    md = B4.render(_sample())
    assert "verifier_disagreement" in md
    assert "batch_authorization" in md


def test_render_negative_tests_table():
    md = B4.render(_sample())
    assert "negative_tests" in md


def test_render_failure_badge():
    bad = _sample()
    bad["schema_version"] = "old"
    bad["evidence"] = []
    md = B4.render(bad)
    assert "❌ FAIL" in md
    assert "结构错误" in md


def test_check_runs_clean():
    r = subprocess.run(
        [sys.executable, os.path.join(ROOT, "tools", "pck_renderer_619.py"), "--check"],
        capture_output=True, text=True)
    assert r.returncode == 0, (r.stdout + r.stderr)
