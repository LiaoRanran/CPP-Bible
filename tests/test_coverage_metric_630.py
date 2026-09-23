"""630 C1 · coverage 第四元指标 单测（6 例）。"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import coverage_metric_630 as C


@pytest.fixture(scope="module")
def m():
    return C.measure()


def test_vector_pool_is_35(m):
    assert m["total"] == 35
    assert m["probe_ready_count"] + m["no_probe_count"] == 35


def test_mappings_are_subsets_of_vectors(m):
    ids = {v["id"] for v in C.vectors()}
    assert set(m["real_event"]) <= ids
    assert set(m["exercised_by_630"]) <= ids
    assert set(m["ran"]) == set(m["real_event"]) | set(m["exercised_by_630"])


def test_coverage_arithmetic(m):
    assert m["coverage"] == round(m["ran_count"] / 35, 4)
    assert m["ran_count"] + m["never_run_count"] == 35
    assert 0 < m["coverage"] < 1


def test_every_exercised_vector_has_a_reason(m):
    for vid in m["exercised_by_630"]:
        assert m["exercised_note"][vid].strip(), f"{vid} 缺映射理由"


def test_unmapped_op_gap_is_registered(m):
    assert m["unmapped_ops"], "M1 无对应向量这一缺口必须登记"
    assert any("M1" in k for k in m["unmapped_ops"])


def test_four_metrics_and_report(m):
    fm = m["four_metrics"]
    assert len(fm) == 4
    assert any("逃逸率" in k for k in fm) and any("自身免疫率" in k for k in fm)
    assert any("触达率" in k for k in fm) and any("coverage" in k for k in fm)
    p = C.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("定义与口径", "本批送审映射", "从未跑过", "四元组联合报告", "局限"):
        assert kw in md, f"报告缺：{kw}"
    assert json.load(open(C.OUT_JSON, encoding="utf-8"))["ran_count"] == m["ran_count"]
    assert C.selftest() == 0
