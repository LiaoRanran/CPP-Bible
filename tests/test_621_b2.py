"""621 B2 · CI 并发竞态复现工具 单测"""
from __future__ import annotations

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import ci_race_reproducer_621 as R  # noqa: E402


def test_dryrun_does_not_run_gates():
    d = R.reproduce(iterations=3, real=False)
    assert d["mode"] == "dry-run"
    assert d["runs"] == []
    assert d["block_rate"] is None


def test_dryrun_states_reason():
    d = R.reproduce(iterations=1, real=False)
    assert "不跑监工门禁" in d["reason"]


def test_historical_evidence_present():
    d = R.reproduce(iterations=1, real=False)
    assert d["historical"]["concurrent_observed"]["block"] == 2
    assert d["historical"]["serial_observed"]["block"] == 0


def test_block_regex_parses():
    found = R.BLOCK_RE.findall("[BLOCK ] EV-ARTIFACT-FILE-EXISTS  x.md")
    assert found == ["EV-ARTIFACT-FILE-EXISTS"]


def test_hits_regex_parses():
    m = R.HITS_RE.search("命中 191 (block=0 warn=186 advice=5)")
    assert m is not None
    assert int(m.group(1)) == 191
    assert int(m.group(2)) == 0


def test_real_mode_requires_explicit_flag():
    """默认 reproduce(real=False) 不应触发任何子进程；real 仅在显式传入时为真。"""
    d = R.reproduce(iterations=2)
    assert d["mode"] == "dry-run"
    assert d["block_seen"] == 0


def test_report_renders_dryrun_section():
    md = R.render_report(R.reproduce(iterations=2, real=False))
    assert "未真跑门禁" in md
    assert "历史实测" in md


def test_ci_yml_gate_needs_replay_still_present():
    """与 B1 修复联动：竞态修复仍在位。"""
    import yaml
    ci = os.path.join(ROOT, ".github", "workflows", "ci.yml")
    with open(ci, encoding="utf-8") as fh:
        jobs = yaml.safe_load(fh)["jobs"]
    assert "replay" in (jobs["gate"].get("needs") or [])


def test_selftest_passes():
    assert R.selftest() == 0
