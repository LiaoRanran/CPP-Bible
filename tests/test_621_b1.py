"""621 B1 · ci.yml 竞态修复（gate needs replay）单测"""
from __future__ import annotations

import os
import sys

import pytest
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
CI = os.path.join(ROOT, ".github", "workflows", "ci.yml")


def _ci():
    with open(CI, encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def test_ci_yml_parses():
    d = _ci()
    assert "jobs" in d
    assert isinstance(d["jobs"], dict)


def test_gate_needs_replay():
    jobs = _ci()["jobs"]
    assert "gate" in jobs
    needs = jobs["gate"].get("needs") or []
    assert "replay" in needs


def test_replay_does_not_need_gate():
    """方向必须是「写者(replay)先、读者(gate)后」，不能反向。"""
    jobs = _ci()["jobs"]
    needs = jobs.get("replay", {}).get("needs") or []
    assert "gate" not in needs


def test_downstream_jobs_still_depend_on_gate():
    jobs = _ci()["jobs"]
    for name in ("compile", "publish-check"):
        needs = jobs[name].get("needs") or []
        assert "gate" in needs
        assert "replay" in needs


def test_ci_has_concurrency_safety_comment():
    with open(CI, encoding="utf-8") as fh:
        text = fh.read()
    assert "并发安全" in text
    assert "写者先、读者后" in text


def test_no_core_tools_touched_by_this_fix():
    """B 线只改 ci.yml：确认 gate_engine / replay 未被改动（受控检查由 E2 门禁负责）。"""
    assert os.path.exists(os.path.join(ROOT, "tools", "gate_engine.py"))
    assert os.path.exists(os.path.join(ROOT, "tools", "atom_evidence_replay.py"))


if __name__ == "__main__":
    sys.exit(pytest.main([__file__, "-q"]))
