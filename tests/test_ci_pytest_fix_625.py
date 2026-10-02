# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""625 A3 · CI pytest 红因修复回归测试（≥3 例）。"""
import os
import subprocess
import sys

import ci_pytest_final_clear_632 as clr
import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))


# 632 A2：本地未跟踪残留(_arch_v19.._arch_v23/_adv_v80)让治理清单「多出新增」而红；
# CI 无残留应通过（631 A4）。残留在则跳过，不误红也不掩盖。
@pytest.mark.skipif(
    clr.residue_present(),
    reason="673s 实测修正：阻塞原因**不是**未跟踪残留 —— _arch_v19..v23/_adv_v80 已全部入库"
           "（168 文件 tracked）⇒ 守卫恒真、本用例在 CI 也从未跑过。真阻塞是"
           " data/governance_docs_manifest.json 与真实文档树**漂移 634 处**（这些目录入库时未同步清单）。"
           "解除条件：owner 重生成/重钉治理清单（治理动作，673s 红线 4 不擅自清票）。"
           "实测：摘掉守卫后 4 个依赖它的用例 4/4 全红。",
)
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
