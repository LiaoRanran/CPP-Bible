"""621 B3 · CI 并发安全检查 单测"""
from __future__ import annotations

import os
import sys

import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import ci_concurrency_check_621 as C  # noqa: E402

CI = os.path.join(ROOT, ".github", "workflows", "ci.yml")


def _good():
    return {
        "replay": {"steps": [{"run": "python3 tools/atom_evidence_replay.py --check"}]},
        "gate": {"needs": ["replay"], "steps": [{"run": "python3 tools/gate_engine.py --check"}]},
    }


def _bad():
    return {
        "replay": {"steps": [{"run": "python3 tools/atom_evidence_replay.py --check"}]},
        "gate": {"steps": [{"run": "python3 tools/gate_engine.py --check"}]},
    }


def test_writer_detected():
    assert C.classify(_good())[0] == ["replay"]


def test_reader_detected():
    assert C.classify(_good())[1] == ["gate"]


def test_good_config_passes():
    assert C.check(_good())["ok"] is True
    assert C.check(_good())["violations"] == []


def test_missing_needs_violation():
    r = C.check(_bad())
    assert r["ok"] is False
    assert r["violations"][0]["reader"] == "gate"
    assert r["violations"][0]["missing_writers"] == ["replay"]


def test_transitive_needs_satisfies():
    jobs = {
        "replay": {"steps": [{"run": "tools/atom_evidence_replay.py"}]},
        "mid": {"needs": ["replay"], "steps": [{"run": "echo hi"}]},
        "gate": {"needs": ["mid"], "steps": [{"run": "gate_engine.py"}]},
    }
    assert C.check(jobs)["ok"] is True


def test_empty_jobs_ok():
    assert C.check({})["ok"] is True


def test_real_ci_yml_passes():
    r = C.check(C.load_jobs(CI))
    assert r["ok"] is True, r["violations"]
    assert "replay" in r["writers"]
    assert "gate" in r["readers"] and "quality" in r["readers"]


def test_real_ci_yml_has_concurrency_safety_job():
    with open(CI, encoding="utf-8") as fh:
        jobs = yaml.safe_load(fh)["jobs"]
    assert "concurrency-safety" in jobs


def test_report_renders():
    assert "并发安全检查" in C.render(C.check(_good()))


def test_selftest_passes():
    assert C.selftest() == 0
