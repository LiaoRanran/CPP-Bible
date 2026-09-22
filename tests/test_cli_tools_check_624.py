"""624 D1 · 3 个 CLI 工具 `--check` 测试（每个工具 1 例）。"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PY = sys.executable
TOOLS = ["authority_to_annotations_sync_623.py", "w2_recompute_623.py", "run_623_gate.py"]


def _run_check(tool: str) -> int:
    p = subprocess.run([PY, os.path.join(ROOT, "tools", tool), "--check"],
                       capture_output=True, text=True)
    return p.returncode


def test_authority_sync_check():
    assert _run_check("authority_to_annotations_sync_623.py") == 0


def test_w2_recompute_check():
    assert _run_check("w2_recompute_623.py") == 0


def test_run_623_gate_check():
    assert _run_check("run_623_gate.py") == 0


def test_all_three_have_check_flag():
    # 冒烟：--help 中应出现 --check
    for t in TOOLS:
        p = subprocess.run([PY, os.path.join(ROOT, "tools", t), "--help"],
                           capture_output=True, text=True)
        assert "--check" in (p.stdout + p.stderr)
