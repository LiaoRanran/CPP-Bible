"""锁定 `ci_local_precheck` 的解析器契约。

该工具的价值是"push 前本地复跑 CI 步骤、一次暴露全部失败"，前提是**能把 ci.yml 的步骤
解析全**——漏抽一步就会得到"本地全绿但 CI 红"的假安慰（2026-09-10 三次盲查后的固化）。
"""
from __future__ import annotations

import ci_local_precheck as cl


def test_parses_all_quality_steps():
    """步骤数与关键步都在：数量级护栏防止 ci.yml 结构变化后静默漏抽。"""
    steps = cl.parse_steps()
    names = [n for n, _ in steps]
    assert len(steps) >= 30, f"quality 步骤数异常（{len(steps)}），可能解析漏抽"
    for must in ("Evidence Replay", "Pytest", "Gate Engine", "S1-S6 Controls"):
        assert any(must in n for n in names), f"缺少步骤：{must}"


def test_extracts_multiline_run_blocks():
    """`run: |` 的多行块必须逐行抽全（不是只抽第一行）。"""
    steps = dict(cl.parse_steps())
    pytest_cmds = next(c for n, c in steps.items() if "Pytest" in n)
    assert any("pip install" in c for c in pytest_cmds)
    assert any("pytest tests/ -q" in c for c in pytest_cmds)
    replay = next(c for n, c in steps.items() if "Evidence Replay" in n)
    assert any(c.startswith("python3 tools/atom_evidence_replay.py") for c in replay)


def test_list_mode(capsys):
    assert cl.main(["--list"]) == 0
    out = capsys.readouterr().out
    assert "Evidence Replay" in out
