"""631 A1 · CI pytest 失败分类 单测（6 例）。

只读解析已落盘的原始输出，不重跑全量。
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import ci_pytest_triage_631 as T


@pytest.fixture(scope="module")
def tri():
    return T.triage()


def test_raw_present_and_parsed(tri):
    assert os.path.exists(T.RAW), "原始全量输出必须先落盘"
    assert tri["raw_present"] and tri["total"] >= 12
    assert len(tri["rows"]) == tri["total"]
    assert all(r["nodeid"].startswith("tests/") and "::" in r["nodeid"]
               for r in tri["rows"])


def test_four_categories_only(tri):
    assert all(r["category"] in T.CATEGORIES for r in tri["rows"])
    assert sum(tri["per_category"].values()) == tri["total"]
    assert tri["per_category"]["真实缺陷型"] == 0, "630→631 未发现真 bug"


def test_classifier_rules():
    assert T.classify("tests/test_run_629_gate.py::test_selftest_passes") \
        == "跨批脆弱型"
    assert T.classify("tests/test_pre_push_checklist_627.py::x") == "工具自检过期型"
    assert T.classify("tests/test_governance_doc_guard_591.py::y") == "环境依赖型"
    assert T.classify("tests/test_something_new.py::z") == "真实缺陷型"


def test_every_row_has_root_and_fix(tri):
    for r in tri["rows"]:
        assert r["root"] and not r["root"].startswith("（未登记"), r["nodeid"]
        assert r["fix"] and not r["fix"].startswith("（未登记"), r["nodeid"]


def test_fixable_subset_is_cross_batch_only(tri):
    for nid in tri["fixable"]:
        assert T.classify(nid) == "跨批脆弱型"
    assert len(tri["fixable"]) + len(tri["not_fixable"]) == tri["total"]


def test_report_json_and_selftest(tri):
    p = T.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("分类统计", "逐条分类", "与 630 冻结基线的差额", "诚实登记"):
        assert kw in md, f"报告缺：{kw}"
    saved = json.load(open(T.OUT_JSON, encoding="utf-8"))
    assert saved["total"] == tri["total"]
    assert T.selftest() == 0
