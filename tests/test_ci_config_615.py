#!/usr/bin/env python3
"""615 D1 回归测试：CI 配置确认（非实跑）。"""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def _jobs() -> dict:
    return yaml.safe_load((ROOT / ".github" / "workflows" / "ci.yml").read_text(
        encoding="utf-8"))["jobs"]


def _runs(job: dict) -> str:
    return "\n".join((s.get("run") or "") for s in job.get("steps", []) if isinstance(s, dict))


def test_pyyaml_in_gate_and_quality() -> None:
    j = _jobs()
    assert "pyyaml" in _runs(j["gate"]), "gate job 缺 pyyaml 安装"
    assert "pyyaml" in _runs(j["quality"]), "quality job 缺 pyyaml 安装"


def test_four_jobs_complete() -> None:
    j = _jobs()
    for name in ("gate", "quality", "pytest", "replay"):
        assert name in j, f"缺 job {name}"
        assert len(j[name].get("steps", [])) >= 2, f"{name} 步骤不足"
    assert "pytest-xdist" in _runs(j["pytest"]) or "xdist" in _runs(j["pytest"])
