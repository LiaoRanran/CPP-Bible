#!/usr/bin/env python3
"""B3 回归测试：quality_gate_613（CI quality job 步骤复跑器）。

注意：不在 pytest 内跑全量 28 步（约 40s+ 且与 CI 同步骤重复）；
只校验步骤表构造、单步执行器、报告渲染，并对最关键的两个 D5 门禁做单步断言。
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import quality_gate_613 as q  # noqa: E402


def test_steps_wellformed():
    assert len(q.STEPS) >= 20
    for name, argv, hard in q.STEPS:
        assert name and argv, f"步骤 {name} 参数不完整"
        assert isinstance(hard, bool)


def test_d5_steps_included():
    names = {s[0] for s in q.STEPS}
    assert "d5_appendix_audit" in names
    assert "d5_source_integrity" in names


def test_run_step_reports_rc():
    r = q.run_step("ruff", ["-m", "ruff", "check", "tools/"], timeout=120)
    assert r["name"] == "ruff" and r["rc"] == 0


def test_run_step_unknown_module():
    r = q.run_step("nonexistent", ["-m", "no_such_module_xyz"], timeout=60)
    assert r["rc"] != 0


def test_render_marks_failures():
    page = q.render([{"name": "x", "rc": 1, "sec": 0.1, "tail": "boom"}],
                    {"name": "worktree_cleanliness", "rc": 0, "sec": 0.0, "tail": "干净"})
    assert "失败明细" in page and "boom" in page


def test_check_passes():
    assert q.main(["--check"]) == 0
