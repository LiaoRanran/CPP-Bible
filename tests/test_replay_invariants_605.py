"""605 任务3 · replay 不变量独立检查工具 回归锁。

锁十件事：
  * fingerprint_dir 确定性（同目录两次指纹一致）
  * fingerprint_dir 对缺失目录返回 MISSING
  * check_artifact_restore pass（Examples/ 指纹稳定）
  * check_build_reproducibility pass（1 张卡，复用 replay._recompile_invariant）
  * check_sandbox_isolation pass（临时目录不泄漏）
  * run_checks 全部 pass
  * CLI --list 输出 3 个不变量
  * CLI --check exit 0
  * CLI --check --invariant artifact_restore 只跑一个
  * CLI --json 输出合法 JSON 且 all_passed=true
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import replay_invariants as ri

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "tools" / "replay_invariants.py"


# ── fingerprint_dir ─────────────────────────────────────────────────────────────
def test_fingerprint_dir_deterministic(tmp_path: Path):
    (tmp_path / "a.txt").write_text("hello", encoding="utf-8")
    (tmp_path / "b.txt").write_text("world", encoding="utf-8")
    fp1 = ri.fingerprint_dir(tmp_path)
    fp2 = ri.fingerprint_dir(tmp_path)
    assert fp1 == fp2
    assert fp1 != "MISSING"


def test_fingerprint_dir_missing():
    assert ri.fingerprint_dir("/nonexistent/path/xyz") == "MISSING"


def test_fingerprint_dir_detects_change(tmp_path: Path):
    (tmp_path / "a.txt").write_text("v1", encoding="utf-8")
    fp1 = ri.fingerprint_dir(tmp_path)
    (tmp_path / "a.txt").write_text("v2", encoding="utf-8")
    fp2 = ri.fingerprint_dir(tmp_path)
    assert fp1 != fp2


# ── 不变量检查 ──────────────────────────────────────────────────────────────────
def test_check_artifact_restore_pass():
    r = ri.check_artifact_restore()
    assert r["name"] == "artifact_restore"
    assert r["passed"] is True
    assert r["files_scanned"] > 0


def test_check_build_reproducibility_pass():
    r = ri.check_build_reproducibility(n_cards=1)
    assert r["name"] == "build_reproducibility"
    assert r["passed"] is True
    assert len(r["cards"]) == 1
    assert r["cards"][0]["match"] is True


def test_check_sandbox_isolation_pass():
    r = ri.check_sandbox_isolation()
    assert r["name"] == "sandbox_isolation"
    assert r["passed"] is True
    assert r["temp_dir_cleaned"] is True


def test_run_checks_all_pass():
    results = ri.run_checks()
    assert len(results) == 3
    assert all(r["passed"] for r in results)


def test_run_checks_only_one():
    results = ri.run_checks(only=("artifact_restore",))
    assert len(results) == 1
    assert results[0]["name"] == "artifact_restore"


def test_run_checks_unknown_invariant():
    results = ri.run_checks(only=("nonexistent",))
    assert len(results) == 1
    assert results[0]["passed"] is False
    assert "unknown invariant" in results[0]["detail"]


# ── CLI ─────────────────────────────────────────────────────────────────────────
def test_cli_list():
    proc = subprocess.run([sys.executable, str(TOOL), "--list"],
                          capture_output=True, text=True, timeout=10)
    assert proc.returncode == 0
    assert "artifact_restore" in proc.stdout
    assert "build_reproducibility" in proc.stdout
    assert "sandbox_isolation" in proc.stdout


def test_cli_check_exit_0():
    proc = subprocess.run([sys.executable, str(TOOL), "--check"],
                          capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0
    assert "全部通过" in proc.stdout


def test_cli_check_single_invariant():
    proc = subprocess.run([sys.executable, str(TOOL), "--check", "--invariant", "sandbox_isolation"],
                          capture_output=True, text=True, timeout=30)
    assert proc.returncode == 0
    assert "sandbox_isolation" in proc.stdout


def test_cli_json_valid():
    proc = subprocess.run([sys.executable, str(TOOL), "--check", "--json"],
                          capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert data["all_passed"] is True
    assert len(data["results"]) == 3
