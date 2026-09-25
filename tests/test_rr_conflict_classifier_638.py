"""638 B2 · RR 冲突分类器单测（>=5 例，纯标准库）。"""
from __future__ import annotations

import os

import tools.rr_conflict_classifier_638 as m


def _r(rid, sev, scope="atom"):
    return {"id": rid, "severity": sev, "scope": scope}


# B2-1：前缀族与同族判定
def test_prefix_and_family():
    assert m.prefix("ATOM-REL-TARGET") == "ATOM-REL"
    assert m.prefix("ATOM-REL-TARGET-HC") == "ATOM-REL"
    assert m.prefix("EV-FM-REQUIRED") == "EV-FM"
    assert m.family("ATOM-REL-TARGET-HC") == "ATOM-REL-TARGET"
    assert m.family("ATOM-REL-TARGET") == "ATOM-REL-TARGET"


# B2-2：四型分类判据（type1/2/3/4）
def test_four_types():
    t3 = m.classify_pair(_r("A-B", "block"), _r("A-B-HC", "block"))
    assert t3["type"] == "type3" and t3["severity"] == "P1" and t3["confidence"] == "high"
    t1 = m.classify_pair(_r("A-B-X", "block"), _r("A-B-Y", "warn"))
    assert t1["type"] == "type1" and t1["severity"] == "P0"
    t2 = m.classify_pair(_r("A-B-X", "advice", "repo"), _r("A-B-Y", "advice", "repo"))
    assert t2["type"] == "type2" and t2["severity"] == "P2"
    t4 = m.classify_pair(_r("A-X", "block"), _r("B-Y", "warn"))
    assert t4["type"] == "type4" and t4["confidence"] == "low"


# B2-3：跨 scope 不成对；候选对总数 927
def test_pairs_scope_restricted():
    assert len(m.rule_pairs([_r("A", "block"), _r("B", "block", "repo")])) == 0
    pairs = m.rule_pairs()
    assert len(pairs) == 927
    assert all(p["scope"] in ("atom", "evidence", "repo") for p in pairs)


# B2-4：高置信 + 低置信 = 候选；高置信全部同前缀族
def test_confidence_split():
    s = m.summary()
    assert s["n_high"] + s["n_low"] == s["n_pairs"]
    assert s["n_high"] < s["n_pairs"]          # 多数是低置信同域对
    assert all(p["confidence"] == "high" for p in s["high_pairs"])
    assert sum(s["high_type_dist"].values()) == s["n_high"]


# B2-5：top3 三条互不重复 rule_a，且都有建议
def test_top3_distinct_and_actionable():
    s = m.summary()
    assert len(s["top3"]) == 3
    names = [p["rule_a"] for p in s["top3"]]
    assert len(set(names)) == 3
    for p in s["top3"]:
        assert p["suggestion"] and p["severity"] in ("P0", "P1", "P2")
        assert p["type"] in ("type1", "type2", "type3", "type4")


# B2-6：冲突度非退化（同前缀族内计算，max < scope 内规则数-1）
def test_degree_is_not_degenerate():
    s = m.summary()
    assert s["max_degree"] < 35            # 若按同 scope 全配对则恒为 35（退化）
    assert s["top_degree_rules"]
    assert s["top3"][0]["severity"] == "P0"


# B2-7：卡级 23 张全部有类型/建议（对齐 636）
def test_card_level_covers_23():
    s = m.summary()
    assert s["n_cards"] == 23
    assert all(c["type"] in ("type1", "type2", "type3", "type4") for c in s["cards"])
    assert sum(s["card_type_dist"].values()) == 23


# B2-8：输出路径在 data 下（--check 不写盘）
def test_output_paths_under_data():
    assert m.OUT_MD.startswith(os.path.join(m.ROOT, "data"))
    assert m.OUT_JSON.startswith(os.path.join(m.ROOT, "data"))
