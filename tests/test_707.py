# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""707 批测试：科研落地工具的行为断言（只读，不跑 detect）。

覆盖：707-A 公理独立性 / 707-B 零成本 P1/P2/P3 / 707-C 可纠错边界 T6 / 707-D 双设计样本量。
跑法：python -m pytest tests/test_707.py -q
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import asset_capabilities as ac          # noqa: E402
import audit_protocol as ap              # noqa: E402
import check_drift_correctability as cdc  # noqa: E402
import sample_size_calculator as ssc     # noqa: E402


def test_p1_zero_yield_declaration():
    # 707-B P1：两个零产资产被排除出有效声明池
    assert ac.ZERO_YIELD_ASSETS == ("wunsequenced", "compile-time")
    assert "wunsequenced" not in ac.EFFECTIVE_ASSETS
    assert "compile-time" not in ac.EFFECTIVE_ASSETS
    assert len(ac.EFFECTIVE_ASSETS) == 6


def test_p2_accounting_aware_vs_unaware():
    # 707-B P2：aware 记账在无 catch 且有 env_gap 时返回 unknown（暴露静默退化）
    pa = {"compiler-warn": "miss", "cross-compile": "miss", "linker": "miss"}
    assert ac.or_verdict(pa, ac.E2_SUPPORTED, accounting="unaware") == "miss"
    assert ac.or_verdict(pa, ac.E2_SUPPORTED, accounting="aware",
                         env_gap=ac.ENV_GAP_E2) == "unknown"


def test_p3_aggregation_rules_and_validation():
    # 707-B P3：OR 对零产免疫、mean 稀释 —— 在冻结矩阵上复算并与 703 对账
    doc = ac.validate()
    assert doc["P1"]["claim_p1_holds"] is True
    assert doc["P2"]["claim_p2_holds"] is True
    assert doc["P3"]["claim_p3_holds"] is True
    assert abs(doc["P3"]["mean_dilution_factor"] - 1.333331) < 1e-3
    assert doc["all_claims_hold"] is True


def test_sample_sizes_match_700C():
    # 707-D / 700-C：Type I=849、II=17、III/IV=∞
    assert ssc.by_type("I")["n_total"] == 849
    assert ssc.by_type("II")["n_total"] == 17
    assert ssc.by_type("III")["n_total"] == float("inf")
    assert ssc.by_type("IV")["n_total"] == float("inf")


def test_t6_environment_gate_must_retest():
    # 707-C / 698-B T6：环境门控撤除（asan/ubsan/tsan）⇒ 必须重测
    body = cdc.case_692_e1e2()
    assert body["claim_T6_holds"] is True
    assert body["classification"]["must_retest"] is True
    assert set(body["classification"]["acquisition_layer_assets"]) == {"asan", "ubsan", "tsan"}


def test_dual_design_routing():
    # 707-D / 700-C：ψ>0 ⇒ 配对；ψ=0 ⇒ 设计级对照
    assert ap.dual_design(0.353357, 0.353357)["paired_arm"]["applicable"] is True
    assert ap.dual_design(0.0, 0.0)["paired_arm"]["applicable"] is False
    assert "design-level" in ap.dual_design(0.0, 0.0)["routing"]


def test_axiom_independence_classification():
    # 707-A / 700-A：只有 A2/A5 有反例；A3/A4/A6/A7 恒真
    import test_axiom_independence as tai
    cm = tai.load_700()
    cls = tai.classify(cm)
    assert cls["genuine_axioms"] == ["A2", "A5"]
    assert sorted(cls["theorems"]) == ["A3", "A4", "A6", "A7"]
