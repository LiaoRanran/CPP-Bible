"""647 E1–E3 · 打靶准备交付物回归锁（编号 E-1..E-5）。"""
from __future__ import annotations

import json
import os

import targeting_prep_647 as T


def test_e1_three_docs_exist_and_long_enough():
    res = T.audit()
    assert res["n"] == 3
    for r in res["docs"]:
        assert r["exists"] and r["chars"] >= 1500, (r["doc"], r.get("chars"))


def test_e2_sections_complete():
    for r in T.audit()["docs"]:
        assert r["missing_sections"] == [], (r["doc"], r["missing_sections"])


def test_e3_boundary_declared():
    """E 线必须**明确声明不越界**（只调研、不建卡）。"""
    for r in T.audit()["docs"]:
        assert r["declares_no_cards"] is True, r["doc"]
        assert r["boundary_markers"], r["doc"]


def test_e4_workload_quantified():
    for r in T.audit()["docs"]:
        assert r["has_workload"] is True, r["doc"]


def test_e5_report_and_selftest():
    assert T.selftest() == 0
    assert T.main(["--report"]) == 0
    assert os.path.isfile(T.OUT_MD)
    doc = T.audit()
    assert json.dumps(doc, ensure_ascii=False) and doc["all_ok"] is True
