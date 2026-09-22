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
    monkeypatch.setenv("CPPBIBLE_OBS", "0")
    findings = ge.run(include_advice=True)
    blocks = [f for f in findings if f.severity == "block"]
    assert blocks == []                       # 新规则对存量 0 误报
    assert not [f for f in findings if f.rule_id in HC_IDS]


def test_poison_coverage_total_now_67():
    _covered, total, _uncovered = pd.rule_coverage()
    assert total == 67


def test_hc_rules_uncovered_by_poison():
    _covered, _total, uncovered = pd.rule_coverage()
    assert HC_IDS <= set(uncovered)           # 诚实登记：新规则 poison 覆盖为 0


def test_report_exists():
    p = os.path.join(ROOT, "data", "high_complexity_rules_regression_624.md")
    assert os.path.exists(p) and os.path.getsize(p) > 500
