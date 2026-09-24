"""630 A1 · 口径差异诊断 单测（6 例）。

含实跑 gate 全量只读求值（`ge.run()`）⇒ module fixture 缓存诊断结果。
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import autoimmune_diagnose_630 as D


@pytest.fixture(scope="module")
def diag():
    return D.diagnose()


def test_caliber_warns_only_three_rules(diag):
    # 633 A2：631 已落地 auto liveness ⇒ 部分口径规则不再告警（3→1），
    # 过期断言 `== set(RULE_FIELD)` 改为子集（仍须落在口径规则集合内）。
    rules = {r["rule"] for r in diag["rows"]}
    assert rules <= set(D.RULE_FIELD), f"只应诊断口径规则：{sorted(rules)}"
    assert diag["cards"] >= 1


def test_only_caliber_cards_covered(diag):
    import autoimmune_rate_framework as F

    assert set(F.measure()["caliber_only_cards"]) <= set(diag["caliber_only_cards"])


def test_classify_taxonomy():
    # 空值（含 {}）算「缺失」：没有可用取值 ⇒ 与"键不存在"同类
    assert D.classify("OBSERVATION-LIVENESS", {})["type"] == "字段缺失型"
    assert D.classify("OBSERVATION-LIVENESS", {"liveness": {}})["type"] == "字段缺失型"
    # 键在但结构不是 {kind, symbol} 字典 ⇒ 格式型
    assert D.classify("OBSERVATION-LIVENESS",
                      {"liveness": "fixture_symbol:x"})["type"] == "格式型"
    # 结构合规但被规则拒绝（符号没能通过锚检查）⇒ 值不符型
    assert D.classify("OBSERVATION-LIVENESS",
                      {"liveness": {"symbol": "x"}})["type"] == "字段值不符型"
    assert D.classify("ATOM-CLAIM-CONCEPT-NORMALIZED",
                      {"object": "这是一句很长的话，包含句读，因此是句子而不是概念。"})["type"] \
        == "格式型"
    assert D.classify("ATOM-CLAIM-CONCEPT-NORMALIZED",
                      {"object": "常量折叠"})["type"] == "字段值不符型"
    assert D.classify("INFERENCE-NOT-MACHINE-VERIFIED",
                      {"signed_by": "bot"})["type"] == "格式型"


def test_human_required_rules(diag):
    """机器不可代签：signed_by 类一律 human；object 语义判断一律 human。"""
    for r in diag["rows"]:
        if r["rule"] == "INFERENCE-NOT-MACHINE-VERIFIED":
            assert not r["auto"]
    assert diag["auto_fixable"] + diag["human_required"] == diag["warns"]


def test_read_only_no_card_mutation():
    assert D.git_atoms_clean(), "诊断工具不得改动 atoms/"
    assert D.prop_of.__module__.startswith("autoimmune_diagnose_630")


def test_report_json_and_selftest(diag):
    p = D.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("分类统计", "逐卡逐条诊断", "修复建议", "关键诚实"):
        assert kw in md, f"报告缺：{kw}"
    saved = json.load(open(D.OUT_JSON, encoding="utf-8"))
    assert saved["warns"] == diag["warns"] and saved["cards"] == diag["cards"]
    assert sum(saved["per_type"].values()) == saved["warns"]
    assert os.path.exists(D.OUT_JSON)
    assert D.selftest() == 0
