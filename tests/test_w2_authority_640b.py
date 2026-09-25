"""640b A1 单测：W2 数字单一权威源（≥5 例）。"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import w2_authority_640b as A  # noqa: E402


def test_two_paths_agree():
    """现算（事实源求解）与产物（入库文件）必须一致（交叉校验）。"""
    s = A.summary()
    assert s["consistent"], f"不一致项：{s['mismatch']}"
    assert s["mismatch"] == []


def test_totals_self_consistent():
    c = A.current()
    assert c["IN"] + c["OUT"] + c["UNDEC"] == c["nodes"] == 121
    assert c["edges"] > 0 and c["defeating_edges"] > 0


def test_triple_matches_current():
    assert A.triple() == (A.current()["IN"], A.current()["OUT"],
                          A.current()["UNDEC"])


def test_artifact_summary_reads_file():
    a = A.artifact_summary()
    assert a["source"].endswith("grounded_labels_w2.json")
    assert a["nodes"] == 121


def test_recompute_is_independent_path():
    """两条路径同源不同实现：recompute 走求解器，artifact 直读文件。"""
    assert A.compute_w2_summary()["source"] == "recompute"
    assert A.artifact_summary()["source"] != "recompute"


def test_selftest_passes():
    assert A.selftest() == 0
