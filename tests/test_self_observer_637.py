# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""637 A · self_observer_637 单测（纯标准库，≥5 例）。编号 TA-1..TA-7。"""
from __future__ import annotations

import self_observer_637 as S


# TA-1：规则数 67
def test_rules():
    assert S.count_rules() == 67


# TA-2：工具/测试规模
def test_tools_tests():
    assert S.count_tools() > 100 and S.count_tests() > 100


# TA-3：接地率 35.8
def test_grounding():
    assert abs(S.grounding_pct() - 35.8) < 0.1


# TA-4：治理指标（例外 231 / 观察态 67）
def test_governance():
    # 674d：例外条目常数 **227 → 231**。674b/674c（本批之前提交）新增 4 条例外登记，
    # 674a 已登记为"钉的常数过期"。实测 `exception_review_635.stats()["total_entries"]`
    # = 231（total 7 / existing 7 / 无缺源、无免期豁免）⇒ 更新钉定值以反映**已提交**状态，
    # 不改断言结构（仍是"恰好等于当前台账条目数"这一硬钉定）。
    assert S.exception_entries() == 231 and S.observation_rules() == 67


# TA-5：击败器覆盖率与 taint
def test_defeater():
    d = S.defeater_stats()
    assert d["coverage_pct"] == 100.0 and d["taint_cards"] == 8


# TA-6：轻量采集不跑重指标、指标键 ≥14
def test_collect_light():
    obs = S.collect(heavy=False)
    assert obs["metrics"]["pytest_failures"] is None
    assert obs["metrics"]["ruff_errors"] is None
    assert len(obs["metrics"]) >= 14


# TA-7：--check 自检通过
def test_selftest():
    assert S.selftest() == 0
