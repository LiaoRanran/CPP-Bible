# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""624 A5 VFDR v2 + 热力图 v2 · 单元测试（≥4 例）。"""
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import vfdr_updater_v2_624 as m  # noqa: E402


def test_rounds_six():
    res = m.compute()
    assert [r["round"] for r in res["rounds"]] == ["R1", "R2", "R3", "R4", "R5", "R6"]


def test_cumulative_and_blind():
    res = m.compute()
    assert res["total_rules"] == 67  # 661 A2：引擎/清单统一 67
    assert res["cumulative_count"] == 34
    assert res["blind_count"] == 33
    assert res["blind_count"] == 67 - res["cumulative_count"]


def test_blind_reduction():
    res = m.compute()
    assert res["blind_reduction"] == {"from": 37, "to": 33, "reduced_by": 4}  # 661 A2：67 基数


def test_heatmap_shape():
    res = m.compute()
    assert len(res["heatmap"]) == 67
    for v in res["heatmap"].values():
        assert set(v) == {"R1", "R2", "R3", "R4", "R5", "R6"}


def test_markdown_render():
    md = m.to_markdown(m.compute())
    assert "规则触达热力图 v2" in md
    assert "累计触达 34/67" in md
    assert md.count("|") > 67 * 9


def test_detect_rate_r5r6_full():
    res = m.compute()
    rates = {r["round"]: r["detect_rate"] for r in res["rounds"]}
    assert rates["R5"] == 1.0 and rates["R6"] == 0.95
