"""640 A2 单测：闭环路线图对齐（≥5 例）。"""
from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import roadmap_align_640 as R  # noqa: E402


def test_direction_classification():
    assert R.classify_direction("四态理论建设与FSM迁移") == "theory"
    assert R.classify_direction("core 通用化与插件化架构") == "arch"
    assert R.classify_direction("外骨骼验证框架与信任根独立") == "exo"
    assert R.classify_direction("修测试补字段") == "maintenance"


def test_weight_mechanism():
    assert R.weight_for("theory", "theory") == 1.5
    assert R.weight_for("arch", "theory") == 0.5
    assert R.weight_for("maintenance", "theory") == 1.0
    assert R.weight_for("theory", "maintenance") == 1.0


def test_candidate_category():
    assert R.candidate_category({"name": "理论框架落地", "action": "规则哲学"}) == "theory"
    assert R.candidate_category({"name": "修失败测试", "action": "定位修复"}) == "maintenance"


def test_realign_sorts_by_weighted_score():
    items = [{"anomaly": {"key": "k"}, "candidates": [
        {"name": "理论A", "action": "", "benefit": "高", "risk_class": "report"},
        {"name": "维护B", "action": "", "benefit": "高", "risk_class": "tool"},
        {"name": "架构C", "action": "", "benefit": "高", "risk_class": "report"},
    ]}]
    out = R.realign(items, "theory")
    scores = [r["score"] for r in out["ranked"]]
    assert scores == sorted(scores, reverse=True)
    # 公式 = benefit(高=3) × risk(report=.5/tool=1) × roadmap_weight：
    #   理论A = 3×.5×1.5 = 2.25（对齐者较未加权 1.5 **提升**）；维护B = 3×1×1 = 3.0；
    #   架构C = 3×.5×0.5 = 0.75（不一致者被压后）
    by_name = {r["name"]: r["score"] for r in out["ranked"]}
    assert by_name["理论A"] == 2.25 and by_name["维护B"] == 3.0 and by_name["架构C"] == 0.75
    assert by_name["理论A"] > 1.5, "对齐者应比未加权基线（3×.5）更高"


def test_run_structure():
    r = R.run()
    assert r["direction"] in R.DIRECTIONS
    assert r["n_candidates"] > 0
    assert len(r["top3"]) <= 3
    assert all(0.5 <= x["roadmap_weight"] <= 1.5 for x in r["ranked"])
