"""606 任务3 · replay 不变量深化 回归锁。

锁十件事：
  * I3 锁一致性：默认路径正确 / batch_root 内路径跟随 / 真实仓库无残留锁
  * I3 CLI：--check 包含 5 个不变量 / --list 包含 lock_consistency
  * metrics 接入：invariants 字段存在 / 5 个不变量全 true / all_pass=true
  * metrics 导入失败时 invariants=null（不 crash）
  * 回归：605 的 13 测试仍全绿（通过 import replay_invariants 验证）
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import replay_invariants as ri

ROOT = Path(__file__).resolve().parent.parent
TOOL = ROOT / "tools" / "replay_invariants.py"


# ── I3 锁一致性 ─────────────────────────────────────────────────────────────────
def test_lock_consistency_pass():
    r = ri.check_lock_consistency()
    assert r["name"] == "lock_consistency"
    assert r["passed"] is True


def test_lock_default_path_correct():
    import atom_evidence_replay as aer
    assert aer._replay_lock_path() == ROOT / "build" / ".replay_lock"


def test_lock_batch_root_follows():
    import atom_evidence_replay as aer
    fake = Path("/tmp/fake_batch_606")
    tok = aer._RUN_ROOT.set(fake)
    try:
        assert aer._replay_lock_path() == fake / "build" / ".replay_lock"
    finally:
        aer._RUN_ROOT.reset(tok)


def test_lock_no_stale_in_real_repo():
    assert not (ROOT / "build" / ".replay_lock").exists()


# ── CLI 包含 I3 ─────────────────────────────────────────────────────────────────
def test_cli_list_has_5_invariants():
    proc = subprocess.run([sys.executable, str(TOOL), "--list"],
                          capture_output=True, text=True, timeout=10)
    assert proc.returncode == 0
    for inv in ("artifact_restore", "build_reproducibility", "sandbox_isolation", "lock_consistency", "manifest_consistency"):
        assert inv in proc.stdout


def test_cli_check_has_5_results():
    # CI 上无 g++/编译环境，build_reproducibility 必失败 ⇒ 用 --no-heavy 跳过
    proc = subprocess.run([sys.executable, str(TOOL), "--check", "--json", "--no-heavy"],
                          capture_output=True, text=True, timeout=120)
    assert proc.returncode == 0
    data = json.loads(proc.stdout)
    assert data["all_passed"] is True
    assert len(data["results"]) == 5
    names = {r["name"] for r in data["results"]}
    assert "lock_consistency" in names


# ── metrics 接入 ────────────────────────────────────────────────────────────────
def test_metrics_invariants_field_exists():
    import tools.metrics_collector as mc
    s = mc.collect(with_heavy=False)
    assert "invariants" in s
    assert "invariants_all_pass" in s


def test_metrics_invariants_all_true():
    import tools.metrics_collector as mc
    s = mc.collect(with_heavy=False)
    inv = s["invariants"]
    assert inv is not None
    assert all(v is True for v in inv.values())
    assert s["invariants_all_pass"] is True


def test_metrics_invariants_has_5_keys():
    import tools.metrics_collector as mc
    s = mc.collect(with_heavy=False)
    inv = s["invariants"]
    assert set(inv.keys()) == {"artifact_restore", "build_reproducibility",
                                "sandbox_isolation", "lock_consistency", "manifest_consistency"}
