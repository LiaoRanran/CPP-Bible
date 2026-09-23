"""629 B1 · 验证器攻击面分类学 单测（6 例）。"""
import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import attack_surface_taxonomy as T


def test_eight_layers_and_scale():
    vs = T.vectors()
    assert sorted(T.LAYERS) == [f"L{i}" for i in range(1, 9)]
    assert len(vs) >= 30, "任务书要求约 30 个向量"
    st = T.layer_stats()
    assert set(st) == set(T.LAYERS)
    assert all(s["vectors"] >= 3 for s in st.values()), "每层 3-5 个向量"


def test_vector_ids_unique_and_wellformed():
    vs = T.vectors()
    ids = [v["id"] for v in vs]
    assert len(set(ids)) == len(ids)
    assert all(re.match(r"^L[1-8]\.[0-9]+$", i) for i in ids)
    assert all(v["id"].split(".")[0] == v["layer"] for v in vs)


def test_risk_and_coverage_fields_consistent():
    for v in T.vectors():
        assert v["risk"] in T.VALID_RISK, v["id"]
        assert v["covered"] == (v["probe"] is not None), v["id"]
        assert v["name"] and v["desc"], v["id"]
        assert isinstance(v["layer_name"], str) and v["layer_name"]


def test_layer_stats_reconcile():
    st, vs = T.layer_stats(), T.vectors()
    assert sum(s["vectors"] for s in st.values()) == len(vs)
    assert sum(s["covered"] for s in st.values()) == sum(1 for v in vs if v["covered"])
    assert sum(s["high"] for s in st.values()) == sum(1 for v in vs if v["risk"] == "high")


def test_report_written():
    p = T.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("8 层攻击面模型", "攻击向量总表", "覆盖概览", "局限"):
        assert kw in md, f"报告缺：{kw}"
    for v in T.vectors():
        assert f"`{v['id']}`" in md


def test_selftest_passes():
    assert T.selftest() == 0
