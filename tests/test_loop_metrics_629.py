"""629 D3 · 闭环三维联测 单测（6 例）。

注意：`autoimmune_dim()` 会实跑 A1（gate 全量只读）与 A2（镜像探针，约 20s）⇒ module fixture 缓存。
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import loop_metrics_629 as L


@pytest.fixture(scope="module")
def dims():
    return {"escape": L.escape_dim(), "autoimmune": L.autoimmune_dim(),
            "coverage": L.coverage_dim(), "asym": L.asymmetry(), "trend": L.trend()}


def test_escape_dimension():
    e = L.escape_dim()
    assert (e["hits"], e["denom"]) == (1, 1406)
    assert abs(e["pct"] - 0.0711) < 0.001 and e["cs_upper"] == 0.9062


def test_autoimmune_dimension_matches_a1(dims):
    import autoimmune_rate_framework as A

    m = A.measure()
    a = dims["autoimmune"]
    assert a["clean_cards"] == m["total"] == 23
    assert a["warned_cards"] == m["warned_count"]
    assert a["hard_defect"] + a["caliber_only"] == m["warned_count"]


def test_coverage_dimension(dims):
    c = dims["coverage"]
    assert (c["touched"], c["rules_total"], c["blind"]) == (36, 67, 31)
    assert c["round8_seeds"] == 20 and c["round8_escaped"] == 0
    assert isinstance(c["round8_distribution"], dict)


def test_trend_covers_v1_to_v7(dims):
    tr = dims["trend"]
    assert len(tr) >= 7
    assert tr[0]["variants"] and tr[-1]["escaped"] == 1
    # 逃逸率显著下降（v1 → 现役）
    live = [t for t in tr if not t["superseded_by"]]
    assert live[-1]["escape_rate"] < tr[0]["escape_rate"] / 10


def test_asymmetry_is_computed(dims):
    a = dims["asym"]
    assert a["ratio"] and a["ratio"] > 100
    assert a["symmetric"] is False, "两向错误严重不对称，必须显式判定为不对称"


def test_report_and_selftest():
    p = L.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("三维当前点", "v1–v7 逃逸趋势", "tradeoff 分析", "无历史点", "局限"):
        assert kw in md, f"报告缺：{kw}"
    saved = json.load(open(L.OUT_JSON, encoding="utf-8"))
    assert saved["coverage"]["touched"] == 36 and saved["asymmetry"]["ratio"] > 100
    assert L.selftest() == 0
