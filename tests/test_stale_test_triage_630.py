"""630 D1 · 既有测试失败分类 单测（6 例）。

只读解析已落盘的原始 pytest 输出（`data/stale_test_raw_630.txt`），不重跑全量。
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import stale_test_triage_630 as T


@pytest.fixture(scope="module")
def tri():
    return T.triage()


def test_classifier_four_types():
    assert T.classify({"nodeid": "t::n", "evidence": "E assert 82 == 0"})["type"] \
        == "断言过期型"
    assert T.classify({"nodeid": "t::f",
                       "evidence": "FileNotFoundError: No such file"})["type"] \
        == "文件不存在型"
    assert T.classify({"nodeid": "t::a",
                       "evidence": "TypeError: unexpected keyword argument"})["type"] \
        == "API 变更型"
    assert T.classify({"nodeid": "t::e", "evidence": "socket.timeout: timed out"})["type"] \
        == "外部依赖型"


def test_override_tables_are_honoured():
    for nid in T.OVERRIDES:
        r = T.classify({"nodeid": nid, "evidence": "assert False"})
        assert r["type"] == T.OVERRIDES[nid][0] and r["overridden"]
        assert r["why"].strip()
    for nid in T.FIXED_BY_630:
        assert T.classify({"nodeid": nid, "evidence": "x"})["type"] == "已修复（630 自纠）"


def test_raw_output_and_parse(tri):
    assert os.path.exists(T.RAW), "原始输出必须先落盘"
    assert tri["total"] >= 11, f"629 基线 11 项，实测 {tri['total']}"
    assert tri["total"] == len(tri["rows"])


def test_every_row_typed_and_counted(tri):
    valid = {"断言过期型", "文件不存在型", "API 变更型", "外部依赖型",
             "环境依赖型（不可修）", "工具自检过期型（不可修）", "跨批脆弱型（不可修）",
             "已修复（630 自纠）", "未分类"}
    assert all(r["type"] in valid for r in tri["rows"])
    assert sum(tri["per_type"].values()) == tri["total"]
    assert len(tri["fixable"]) + len(tri["not_fixable"]) == tri["total"]


def test_fixable_set_is_number_only(tri):
    """可修清单必须**只**含断言过期型，且都有"更新数字"的 hint（§十.2 不改逻辑）。"""
    for nid in tri["fixable"]:
        row = [r for r in tri["rows"] if r["nodeid"] == nid][0]
        assert row["type"] == "断言过期型"
        assert any(k in (row["hint"] + row["why"]) for k in ("数字", "更新")), \
            f"{nid} 的修复说明未交代「更新为当前值」"


def test_report_json_and_selftest(tri):
    p = T.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("分类统计", "逐条分类", "待修清单", "不修的", "诚实登记"):
        assert kw in md, f"报告缺：{kw}"
    saved = json.load(open(T.OUT_JSON, encoding="utf-8"))
    assert saved["total"] == tri["total"] and saved["per_type"] == tri["per_type"]
    assert T.selftest() == 0
