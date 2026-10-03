# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""646 阶段 A2 · 三层耦合打通单测（fast）。"""
import os
import sys

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

import three_layer_orchestrator_646 as c2  # noqa: E402


def _kernel_repo_available() -> bool:
    """兄弟仓 `queyi-verifier/tools/queyi_core_v10_641.py` 是否可探测到。

    与 `tests/conftest.py::_kernel_canonical_available` 同口径（自 `tools/` 起向上 8 级）。
    """
    d = os.path.join(ROOT, "tools")
    for _ in range(8):
        if os.path.isfile(os.path.join(d, "queyi-verifier", "tools", "queyi_core_v10_641.py")):
            return True
        d = os.path.dirname(d)
    return False


# 674d：`c2.orchestrate()` 经 `queyi_data_models_645` 读拆仓内核 ⇒ 单仓检出/CI 上必然
# RuntimeError（工具 fail-loud 是设计，不改工具）。条件 skip；双仓布局下行为不变。
_NEEDS_KERNEL_REPO = pytest.mark.skipif(
    not _kernel_repo_available(),
    reason="拆仓 queyi-verifier 未检出 ⇒ orchestrate() 需内核 canonical（fail-loud）",
)


def test_selftest_passes():
    """--check 只读自检。"""
    assert c2.selftest() == 0


@_NEEDS_KERNEL_REPO
def test_coupling_reaches_targets():
    """真实编排：≥5 链证据≠0、归因可复核率 ≥0.5。"""
    res = c2.orchestrate(min_chains=5)
    assert res["chain_count"] >= 5
    assert res["chains_with_evidence"] >= 5
    assert res["attribution_rate"] >= 0.5
    assert res["met"] is True


@_NEEDS_KERNEL_REPO
def test_every_chain_has_rule_and_verdict():
    """每条链都带规则 id 与尾端判决。"""
    res = c2.orchestrate()
    for c in res["chains"]:
        assert c["rule"] and c["verification"]["verdict"] in (
            "pass", "fail", "escape", "needs_human", "false_positive", "unknown")
