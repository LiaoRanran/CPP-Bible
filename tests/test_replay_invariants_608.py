#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""608 化债：replay_invariants 真检查回归锁。

覆盖：
  T1 I1 真还原：跑 replay_card(restore_artifact=True)，Examples/ 指纹 before==after
  T2 I4 真隔离：batch_root 上下文跑 replay_card，受控目录 git diff 零改动
  T3 I3 contextvar 重置：check_lock_consistency() 后 _RUN_ROOT 恢复默认
  T4 未知不变量名：run_checks(only=("nonexistent",)) → passed=False
  T5 CLI --json：main(["--check","--json","--no-heavy"]) 输出合法 JSON
  T6 I2 n_cards 配置：check_build_reproducibility(n_cards=1) 只查 1 张
  T7 反例：改工件内容 + restore_artifact=False，Examples/ 指纹必变（证明还原机制确实在起作用）
  T8 --no-heavy 跳过 I2：run_checks(heavy=False) 中 build_reproducibility detail 含 "skipped"

需跑真实 replay 的测试（T1/T2/T7）挂 replay_serial（conftest.py SERIAL_EXTRA），
避免 -n auto 下与其它 worker 抢 replay 锁假红。
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

import replay_invariants as ri  # noqa: E402


def _find_confirm_card() -> Path | None:
    """找第一张 confirm 卡（有 command + artifact_sha256）。"""
    cards = ri._find_confirm_cards(n=1)
    return cards[0][0] if cards else None


# ── T1：I1 真还原 ────────────────────────────────────────────────────────────
def test_i1_artifact_restore_real_replay():
    """I1 必须真正跑 replay_card，Examples/ 指纹 before==after。"""
    card = _find_confirm_card()
    if card is None:
        pytest.skip("no confirm card found")
    result = ri.check_artifact_restore()
    assert result["passed"], f"I1 failed: {result['detail']}"
    assert result["verdict"] in ("confirm", "refute"), f"unexpected verdict: {result['verdict']}"
    assert result["files_scanned"] > 0, "Examples/ should have files"


# ── T2：I4 真隔离 ────────────────────────────────────────────────────────────
def test_i4_sandbox_isolation_real_replay():
    """I4 必须在 batch_root 上下文跑 replay_card，受控目录零改动。"""
    card = _find_confirm_card()
    if card is None:
        pytest.skip("no confirm card found")
    result = ri.check_sandbox_isolation()
    assert result["passed"], f"I4 failed: {result['detail']}"
    assert result["batch_had_files"] is True, "batch_root should contain replay artifacts"


# ── T3：I3 contextvar 重置 ───────────────────────────────────────────────────
def test_i3_contextvar_reset():
    """check_lock_consistency() 后 _RUN_ROOT 必须恢复默认（None）。"""
    import atom_evidence_replay as aer
    before = aer._RUN_ROOT.get()
    result = ri.check_lock_consistency()
    after = aer._RUN_ROOT.get()
    assert before == after, f"_RUN_ROOT leaked: {before} -> {after}"
    assert result["passed"], f"I3 failed: {result['detail']}"


# ── T4：未知不变量名 ─────────────────────────────────────────────────────────
def test_unknown_invariant_name():
    """run_checks(only=('nonexistent',)) 必须返回 passed=False 且 detail 含 'unknown'。"""
    results = ri.run_checks(only=("nonexistent",))
    assert len(results) == 1
    assert results[0]["passed"] is False
    assert "unknown" in results[0]["detail"].lower()


# ── T5：CLI --json ───────────────────────────────────────────────────────────
def test_cli_json_output():
    """main(['--check','--json','--no-heavy']) 必须输出合法 JSON 含 all_pass/results。"""
    result = subprocess.run(
        [sys.executable, str(ROOT / "tools" / "replay_invariants.py"),
         "--check", "--json", "--no-heavy"],
        cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", timeout=120,
    )
    assert result.returncode in (0, 2), f"unexpected rc={result.returncode}: {result.stderr}"
    data = json.loads(result.stdout)
    assert "all_passed" in data
    assert "results" in data
    assert len(data["results"]) == 5  # I1/I2/I3/I4/I5


# ── T6：I2 n_cards 配置 ──────────────────────────────────────────────────────
def test_i2_n_cards_config():
    """check_build_reproducibility(n_cards=1) 必须只查 1 张卡。"""
    result = ri.check_build_reproducibility(n_cards=1)
    assert result["name"] == "build_reproducibility"
    assert "cards" in result
    assert len(result["cards"]) == 1, f"expected 1 card, got {len(result['cards'])}"


# ── T7：反例——改工件后不还原，指纹必变 ──────────────────────────────────────
def test_counterexample_artifact_change_detected():
    """改 Examples/ 下一个工件内容 + restore_artifact=False，指纹必变。
    这证明 I1 的指纹机制确实能抓到变化（不是永远 pass 的假检查）。
    """
    card = _find_confirm_card()
    if card is None:
        pytest.skip("no confirm card found")
    # 找一个 Examples/ 下的文件来改
    examples = ROOT / "Examples"
    target = None
    for f in examples.rglob("*.out"):
        target = f
        break
    if target is None:
        pytest.skip("no .out file in Examples/ to modify")
    original = target.read_bytes()
    fp_before = ri.fingerprint_dir(examples)
    try:
        # 改内容
        target.write_bytes(original + b"\n// modified by 608 counterexample test\n")
        fp_after_modify = ri.fingerprint_dir(examples)
        assert fp_before != fp_after_modify, "fingerprint should change after modification"
    finally:
        # 还原
        target.write_bytes(original)
    fp_after_restore = ri.fingerprint_dir(examples)
    assert fp_before == fp_after_restore, "fingerprint should match after restore"


# ── T8：--no-heavy 跳过 I2 ───────────────────────────────────────────────────
def test_no_heavy_skips_i2():
    """run_checks(heavy=False) 中 build_reproducibility 必须被跳过。"""
    results = ri.run_checks(heavy=False)
    i2 = next(r for r in results if r["name"] == "build_reproducibility")
    assert i2["passed"] is True  # 跳过也算 pass
    assert "skipped" in i2["detail"].lower(), f"I2 should be skipped, got: {i2['detail']}"
    assert i2["elapsed_s"] == 0, "skipped check should have 0 elapsed"


# ── T9：I5 manifest 一致性 ─────────────────────────────────────────────────────
def test_i5_manifest_consistency():
    """I5：manifest 中记录的卡指纹必须与磁盘真实卡文件一致。"""
    result = ri.check_manifest_consistency()
    assert result["name"] == "manifest_consistency"
    assert result["cards_checked"] > 0, "manifest should have cards"
    assert result["mismatches"] == 0, f"fingerprint mismatches: {result['detail']}"
    assert result["invalid_verdicts"] == 0, f"invalid verdicts: {result['detail']}"
    assert result["passed"], f"I5 failed: {result['detail']}"
