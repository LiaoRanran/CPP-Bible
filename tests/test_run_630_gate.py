"""630 E1 · 收工门禁 单测（6 例）。

**不能在 pytest 里跑完整门禁**（会再跑 pytest 与全量套件）⇒ 行为类断言用
`--check --no-tests` 子进程（约 2 分钟，跑除 pytest 外的全部步骤）。
"""
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import run_630_gate as G


@pytest.fixture(scope="module")
def gate_run():
    return subprocess.run([sys.executable, G.__file__, "--check", "--no-tests"],
                          cwd=G.ROOT, capture_output=True, text=True, check=False)


def test_tool_manifest_complete_by_batch_marker():
    """按 **630 标记**核验（而不是「所有新增文件」）⇒ 后续批次新增工具不会让本门禁变红。"""
    assert len(G.NEW_TOOLS) == 9
    assert all(os.path.exists(os.path.join(G.ROOT, "tools", t)) for t in G.NEW_TOOLS)
    missing = set(G.added_files("tools", "_630")) - set(G.NEW_TOOLS) - {"run_630_gate.py"}
    assert not missing, f"门禁漏掉本批工具：{sorted(missing)}"
    assert "run_629_gate.py" not in G.added_files("tools", "_630"), "标记过滤必须只收 630"


def test_baseline_frozen_and_categorized():
    assert len(G.BASELINE_FAILURES) == 11
    assert sum(G.BASELINE_CATEGORIES.values()) == 11
    assert all(n.startswith("tests/") and "::" in n for n in G.BASELINE_FAILURES)
    # 630 自己修的 4 项断言过期型**不在**基线里（应已转绿）
    assert not [n for n in G.BASELINE_FAILURES if "pck_hash_drift_analyzer_627::test_content"
                in n or "test_mypy_fix_625::test_no_bulk" in n]


def test_no_monitor_gate_invocation():
    assert G.forbidden_invocations() == []
    src = open(G.__file__, encoding="utf-8").read()
    for name in G.FORBIDDEN_GATES:
        assert f'os.path.join("tools", "{name}")' not in src


def test_failure_parser():
    assert G.new_failures("FAILED tests/a.py::x - E\nFAILED tests/b.py::y\n") == \
        ["tests/a.py::x", "tests/b.py::y"]


def test_gate_other_steps_pass(gate_run):
    assert gate_run.returncode == 0, gate_run.stdout[-900:]
    assert "PASS" in gate_run.stdout and "[FAIL]" not in gate_run.stdout
    assert "[skip] 非 slow 全量 pytest" in gate_run.stdout
    assert "push 后 `origin/master..HEAD` = 0" in gate_run.stdout


def test_controlled_clean_and_selftest():
    for d in G.CONTROLLED:
        if os.path.isdir(os.path.join(G.ROOT, d)):
            p = subprocess.run(["git", "diff", "--quiet", "--", d], cwd=G.ROOT,
                               capture_output=True, check=False)
            assert p.returncode == 0, f"{d} 被污染"
    assert G.selftest() == 0
