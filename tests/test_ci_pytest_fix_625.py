# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""625 A3 · CI pytest 红因修复回归测试（≥3 例）。"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))


# 673u：**摘除 632 A2 的 `residue_present()` 守卫**（该守卫恒真 —— `_arch_v19..v23/_adv_v80`
# 早已入库 ⇒ 任何检出都为 True ⇒ 本用例此前从未真跑过）。673u 定位并修复了真正的阻塞
# （治理清单漂移 634 处 = 扫描面含 gitignore 的本机落盘口 + 哈希未归一换行），并在
# **干净检出（git worktree）**下复验 `tools/governance_doc_guard.py verify` exit 0
# ⇒ 守卫失去理由，恢复真跑（回归锁重新有效）。未改动任何断言。
def test_governance_manifest_verified():
    p = subprocess.run([sys.executable, os.path.join(ROOT, "tools", "governance_doc_guard.py"),
                        "verify"], cwd=ROOT, capture_output=True, text=True)
    assert p.returncode == 0, p.stdout + p.stderr


def test_poison_exemptions_counts_updated():
    import poison_drill as pd
    ex = pd.load_exemptions()
    legacy = [k for k, v in ex.items() if v["redteam_seen"] == "legacy"]
    backed = [k for k, v in ex.items() if v["reason_verified"] == "backed"]
    assert len(legacy) == 27
    assert len(backed) == 28
    assert all(v["reason_verified"] != "missing-test" for v in ex.values())
    assert all(v["reason_verified"] != "weak-test" for v in ex.values())


def test_coverage_total_is_67():
    import poison_drill as pd
    rep = pd.coverage_report()
    assert rep["total"] == 67
    assert len(rep["legacy_exempt"]) == 27


def test_report_exists():
    p = os.path.join(ROOT, "data", "ci_pytest_fix_625.md")
    assert os.path.exists(p) and os.path.getsize(p) > 500
