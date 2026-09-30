# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""624 B2 规则回归 + 误报分析 · 单元测试（≥3 例，只读取证）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import gate_engine as ge  # noqa: E402
import poison_drill as pd  # noqa: E402

HC_IDS = {"EV-SERVES-EXIST-HC", "ATOM-REL-TARGET-HC",
          "ATOM-REL-UNKNOWN-HC", "CARD-PATH-NOT-CANONICAL-HC"}


def test_gate_rule_count_67():
    assert len(ge.RULES) == 67
    assert HC_IDS <= {r.id for r in ge.RULES}


def test_gate_baseline_block_zero_no_false_positive(monkeypatch):
    """624 B2：新接入的 4 条 HC 规则对存量**零误报**。

    670a 修正口径：原断言「全库 block == []」把**别的规则**的存量 block 也算进来，
    与题干（HC 规则误报）不符，且会随语料演进假红。改为：HC 规则零命中
    （block 或任何 severity），全库 block 数**不冻结**（由 669 P0 门禁台账跟踪）。
    """
    monkeypatch.setenv("CPPBIBLE_OBS", "0")
    findings = ge.run(include_advice=True)
    hc_hits = [f for f in findings if f.rule_id in HC_IDS]
    assert hc_hits == [], f"新 HC 规则对存量误报：{hc_hits}"
    # 诚实登记：全库 block 非空是**其它规则**的存量债，不属 624 题干；此处只保证 HC 不引入 block
    assert all(f.rule_id not in HC_IDS for f in findings if f.severity == "block")


def test_poison_coverage_total_now_67():
    _covered, total, _uncovered = pd.rule_coverage()
    assert total == 67


def test_hc_rules_exempted_by_poison():
    _covered, total, uncovered = pd.rule_coverage()
    assert total == 67
    # poison 端到端覆盖为 0 ⇒ 已登记豁免（非 uncovered）；豁免台账含 4 条 HC
    assert HC_IDS.isdisjoint(set(uncovered))
    assert HC_IDS <= set(pd.load_exemptions())


def test_report_exists():
    p = os.path.join(ROOT, "data", "high_complexity_rules_regression_624.md")
    assert os.path.exists(p) and os.path.getsize(p) > 500
