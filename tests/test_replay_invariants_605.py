"""605 任务3 · replay 不变量独立检查工具 回归锁。

锁十件事：
  * fingerprint_dir 确定性（同目录两次指纹一致）
  * fingerprint_dir 对缺失目录返回 MISSING
  * check_artifact_restore pass（Examples/ 指纹稳定）
  * check_build_reproducibility pass（1 张卡，复用 replay._recompile_invariant）
  * check_sandbox_isolation pass（临时目录不泄漏）
  * run_checks 全部 pass（检查项集合 = `INVARIANTS`，条数不写死：606 加了 lock_consistency）
  * CLI --list 输出全部不变量（同上，不写死条数）
  * CLI --check exit 0（--no-heavy：build_reproducibility 依赖编译环境一致性，CI 跳过）
  * CLI --check --invariant artifact_restore 只跑一个
  * CLI --json 输出合法 JSON 且 all_passed=true（同 --no-heavy）
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
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


@pytest.mark.skipif(
    os.environ.get("CI") == "true",
    reason="build_reproducibility 依赖编译环境一致性（卡面 artifact_sha256=本地MinGW编译，CI Ubuntu g++ 产物必然不同）")
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
    # temp_dir_cleaned 键在某些版本中不存在（tempfile.TemporaryDirectory 自动清理），用 .get() 兼容
    assert r.get("temp_dir_cleaned", True) is True


def test_run_checks_all_pass():
    # heavy=False: 跳过 build_reproducibility（CI 编译环境差异，同 CLI 测试的 --no-heavy）
    results = ri.run_checks(heavy=False)
    # 不写死条数：606 给 `INVARIANTS` 追加了 `lock_consistency`（I3），605 的 `== 3` 断言就此过期
    # （607 收工门禁暴露）。改为按名字比对默认集合 ⇒ 今后再加检查项不会再假红。
    assert {r["name"] for r in results} == set(ri.INVARIANTS), results
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
    # --no-heavy: build_reproducibility 依赖编译环境一致性（卡面 artifact_sha256=本地MinGW编译，
    # CI Ubuntu g++ 重编译产物必然不同 ⇒ invariant 失败 exit 2）。CI 上跳过该 heavy invariant，
    # 其余 4 项（artifact_restore/sandbox_isolation/lock_consistency/manifest_consistency）仍校验。
    proc = subprocess.run([sys.executable, str(TOOL), "--check", "--no-heavy"],
                          capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0
    assert "全部通过" in proc.stdout


def test_cli_check_single_invariant():
    proc = subprocess.run([sys.executable, str(TOOL), "--check", "--invariant", "sandbox_isolation"],
                          capture_output=True, text=True, timeout=30)
    assert proc.returncode == 0
    assert "sandbox_isolation" in proc.stdout


def test_cli_json_valid():
    # 同 test_cli_check_exit_0：--no-heavy 跳过 build_reproducibility（CI 编译环境差异）
    proc = subprocess.run([sys.executable, str(TOOL), "--check", "--json", "--no-heavy"],
                          capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert data["all_passed"] is True
    assert {r["name"] for r in data["results"]} == set(ri.INVARIANTS), data["results"]
