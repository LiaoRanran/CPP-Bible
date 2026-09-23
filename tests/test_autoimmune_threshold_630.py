"""630 C3 · 自身免疫率阈值对照 单测（6 例）。"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import autoimmune_threshold_630 as T


@pytest.fixture(scope="module")
def c():
    return T.compare()


def test_v23_thresholds_parsed(c):
    th = c["thresholds"]
    assert th["found"] and th["source"].endswith("02_自身免疫率度量框架.md")
    assert (th["hard_target"], th["hard_cap"]) == (5, 10)
    assert (th["soft_target"], th["soft_fatigue"]) == (20, 40)


def test_external_basis_extracted(c):
    assert len(c["external_basis"]) >= 3
    assert c["actions"], "v23 §建议3 的动作映射必须被摘录"


def test_measured_reconciles(c):
    me = c["measured"]
    assert me["hard_block_cards"] == 0 and me["hard_rate_pct"] == 0.0
    assert abs(me["soft_rate_pct"] - me["soft_warn_cards"] / me["cards"] * 100) < 0.05
    assert me["caliber_cards"] + me["hard_defect_cards"] == me["soft_warn_cards"]


def test_verdict_and_ratios(c):
    assert c["verdict"]["hard"] == "达标"
    assert "超疲劳线" in c["verdict"]["soft"]
    assert c["soft_ratio"] == pytest.approx(5.0)          # 100% / 20%
    assert c["fatigue_ratio"] == pytest.approx(2.5)       # 100% / 40%


def test_urgency_protects_hard_layer(c):
    assert "不要动 block 层" in c["urgency"]
    assert "批量调参" in c["urgency"]


def test_report_and_selftest(c):
    p = T.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("对照表", "外部依据", "紧迫度评估", "建议动作映射", "诚实登记"):
        assert kw in md, f"报告缺：{kw}"
    saved = json.load(open(T.OUT_JSON, encoding="utf-8"))
    assert saved["measured"]["soft_rate_pct"] == c["measured"]["soft_rate_pct"]
    assert T.selftest() == 0
