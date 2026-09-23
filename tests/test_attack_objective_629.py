"""629 D1 · 攻击目标函数 单测（6 例）。"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import attack_objective_629 as A


def test_v7_pool_size():
    vs = A.v7_variants()
    assert len(vs) == 1593, "任务书：v7 候选 1593 条"
    assert all("card" in v and "verdict" in v for v in vs[:5])


def test_ranking_is_deterministic_and_sorted():
    r1 = [x["idx"] for x in A.ranked()[:20]]
    r2 = [x["idx"] for x in A.ranked()[:20]]
    assert r1 == r2
    top = A.seeds()
    assert len(top) == 20
    assert all(top[i]["score"] >= top[i + 1]["score"] for i in range(19))


def test_score_is_product_of_rounded_components():
    for x in A.ranked():
        assert x["score"] == round(x["disagreement"] * x["ambiguity"] * x["provenance"], 6)
        assert 0.0 <= x["disagreement"] <= 1.0
        assert 0.0 <= x["ambiguity"] <= 1.0
        assert 0.0 <= x["provenance"] <= 1.0


def test_escaped_gets_max_disagreement():
    import pytest

    assert A.disagreement({"verdict": "escaped"}) == 1.0
    assert A.disagreement({"verdict": "neutral", "new_block": [], "new_warn": []}) == 0.0
    assert A.disagreement({"verdict": "blocked",
                           "new_block": ["R:path"]}) == pytest.approx(1 / 3)
    # 分量在 score_of 里才四舍五入（保证「报告数字相乘 == 报告 score」）
    assert A.score_of({"verdict": "blocked", "new_block": ["R:path"],
                       "point": "删 artifact_sha256",
                       "card": "evidence/conc/EV-CONC-001.md"}) == {
        "disagreement": 0.3333, "ambiguity": 1.0, "provenance": 1.0,
        "score": 0.3333}


def test_target_rule_reverse_extraction():
    v = {"new_block": ["EV-FM-REQUIRED:evidence/x.md"], "new_warn": []}
    assert A.target_rule_of(v) == "EV-FM-REQUIRED"
    assert A.target_rule_of({"new_block": [], "new_warn": ["OBSERVATION-LIVENESS:e.md"]}) \
        == "OBSERVATION-LIVENESS"
    assert A.target_rule_of({}) == ""


def test_outputs_and_selftest():
    d = A.write_outputs()
    assert d["variants"] == 1593 and len(d["seeds"]) == 20
    assert "×" in d["objective"] and d["proxy_definitions"]
    saved = json.load(open(A.OUT_JSON, encoding="utf-8"))
    assert saved["seeds"] == d["seeds"]
    md = open(A.OUT_MD, encoding="utf-8").read()
    for kw in ("目标函数", "代理定义", "Top20 种子", "局限"):
        assert kw in md
    assert A.selftest() == 0
