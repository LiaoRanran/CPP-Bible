"""629 F1 · 收工门禁 单测（6 例）。

**不能在 pytest 里跑完整门禁**：门禁第 4/5 步会再跑 pytest（递归）与全量非慢套件（数分钟）。
因此：结构类断言直接读模块常量；行为类断言用 `--no-tests` 子进程（约 60-90s，跳过 pytest 步骤）。
"""
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import baseline_629 as B
import run_629_gate as G


@pytest.fixture(scope="module")
def gate_run():
    p = subprocess.run([sys.executable, G.__file__, "--check", "--no-tests"],
                       cwd=G.ROOT, capture_output=True, text=True, check=False)
    return p


def test_tool_manifest_is_complete():
    assert len(G.NEW_TOOLS) == 14
    assert all(os.path.exists(os.path.join(G.ROOT, "tools", t)) for t in G.NEW_TOOLS)
    assert not set(G.NEW_TOOLS) & set(G.FORBIDDEN_GATES)
    # git 交叉核验：本批新增的 tools/ 文件都被清单覆盖
    missing = set(G.added_files("tools")) - set(G.NEW_TOOLS) - {"run_629_gate.py"}
    assert not missing, f"门禁漏掉本批新工具：{sorted(missing)}"


def test_gate_never_invokes_monitor_gates():
    assert G.forbidden_invocations() == []
    src = open(G.__file__, encoding="utf-8").read()
    for name in G.FORBIDDEN_GATES:
        assert f'os.path.join("tools", "{name}")' not in src


def test_failure_parser_and_baseline_freeze():
    fails, summary = G.new_failures(
        "FAILED tests/a.py::x - AssertionError\n"
        "FAILED tests/b.py::y\n1 failed, 2 passed in 2.0s\n")
    assert fails == ["tests/a.py::x", "tests/b.py::y"]
    assert summary and "passed" in list(summary)[0]
    assert len(B.BASELINE_FAILURES) == 11, "629 修正后的既有失败基线（首测 19 项含 8 项自伤/回归）"
    assert sum(B.BASELINE_CATEGORIES.values()) == 11


def test_gate_other_steps_pass(gate_run):
    assert gate_run.returncode == 0, gate_run.stdout[-800:]
    assert "PASS" in gate_run.stdout and "FAIL" not in gate_run.stdout
    assert "[skip] 非 slow 全量 pytest" in gate_run.stdout, "测试步骤应被 --no-tests 跳过"


def test_controlled_dirs_clean_and_ci_untouched():
    for d in G.CONTROLLED:
        if os.path.isdir(os.path.join(G.ROOT, d)):
            p = subprocess.run(["git", "diff", "--quiet", "--", d], cwd=G.ROOT,
                               capture_output=True, check=False)
            assert p.returncode == 0, f"{d} 被污染"
    p = subprocess.run(["git", "diff", "--quiet", G.BATCH_BASE, "HEAD", "--",
                        ".github/workflows/ci.yml"], cwd=G.ROOT, capture_output=True,
                       check=False)
    assert p.returncode == 0, "629 不得改动 ci.yml"


def test_selftest_passes():
    assert G.selftest() == 0
