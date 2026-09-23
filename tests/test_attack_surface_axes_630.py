"""630 C2 · 攻击面横切面 单测（6 例）。"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import attack_surface_axes_630 as A


@pytest.fixture(scope="module")
def m():
    return A.matrix()


def test_all_35_annotated_with_legal_values(m):
    assert m["total"] == 35
    for r in m["rows"]:
        assert r["time"] in A.TIME_VALUES
        assert r["sched"] in A.SCHED_VALUES
        assert r["time_basis"] and r["sched_basis"]


def test_annotation_rules_are_deterministic():
    v = {"name": "证据内容漂移", "desc": "随文件变化漂移", "probe": None}
    assert A.annotate_time(v)["time"] == "周期性"
    v2 = {"name": "regex heuristic 绕过", "desc": "对手持续调整", "probe": None}
    assert A.annotate_time(v2)["time"] == "持续演化"
    v3 = {"name": "普通规则", "desc": "无特征", "probe": None}
    assert A.annotate_time(v3)["time"] == "一次性"
    assert A.annotate_sched(v3)["sched"] == "自发"


def test_scheduling_axis_keywords():
    assert A.annotate_sched({"name": "rubber-stamp", "desc": "人审",
                             "probe": None})["sched"] == "被诱导"
    assert A.annotate_sched({"name": "执行时序依赖", "desc": "needs",
                             "probe": None})["sched"] == "被触发"


def test_matrix_counts_reconcile(m):
    assert sum(m["by_time"].values()) == 35
    assert sum(m["by_sched"].values()) == 35
    assert sum(m["cells"].values()) == 35
    assert m["empty_count"] == 72 - m["cell_count"] == 72 - len(m["cells"])


def test_layer_prefixes_in_cells(m):
    for key in m["cells"]:
        assert key.startswith("L") and len(key.split("|")) == 3


def test_report_and_selftest(m):
    p = A.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("两轴定义", "分布", "三维矩阵", "逐向量标注", "局限"):
        assert kw in md, f"报告缺：{kw}"
    saved = json.load(open(A.OUT_JSON, encoding="utf-8"))
    assert saved["by_time"] == m["by_time"] and saved["cell_count"] == m["cell_count"]
    assert A.selftest() == 0
    assert os.path.exists(A.OUT_MD)
