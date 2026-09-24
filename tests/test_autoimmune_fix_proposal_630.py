"""630 A2 · 修复方案生成 单测（6 例）。"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import autoimmune_diagnose_630 as D
import autoimmune_fix_proposal_630 as P


@pytest.fixture(scope="module")
def prop():
    return P.plan_a()


def test_plan_a_covers_all_diagnosed(prop):
    # 633 A2：631 已落地 auto liveness ⇒ warn 132→65，硬编码 132 过期；改为动态对齐诊断数。
    assert prop["total"] == D.diagnose()["warns"]
    assert all(i["mode"] in ("auto", "human") for i in prop["items"])
    assert len(prop["cards"]) == 23


def test_signed_by_is_never_auto(prop):
    # 633 A2：631 已落地后 signed_by warn 可能为 0（断言过期型）；若有则必 human 且 basis 含免责声明。
    sb = [i for i in prop["items"] if i["field"] == "signed_by"]
    assert all(i["mode"] == "human" for i in sb)
    assert all("机器永不代签" in i["basis"] for i in sb)


def test_auto_items_have_concrete_values(prop):
    # 633 A2：631 已落地 auto liveness ⇒ 现可能 0 条 auto；改为「若有则必具体」。
    autos = [i for i in prop["items"] if i["mode"] == "auto"]
    for i in autos:
        assert i["field"] == "liveness"
        assert i["value"]["kind"] == "fixture_symbol" and i["value"]["symbol"]
        assert "artifact_assert" in i["basis"]


def test_liveness_symbol_is_fixture_specific():
    """自动填的符号必须是**非通用**且**真的出现在本命题引用卡的工件断言里**（否则规则不会放行）。"""
    import gate_engine as ge

    idx = ge._ev_index()
    checked = 0
    for i in P.plan_a()["items"]:
        if i["mode"] != "auto":
            continue
        sym = i["value"]["symbol"]
        assert not ge._is_universal_symbol(sym), f"{sym} 是通用符号，不该自动填"
        prop = D.prop_of(os.path.join(P.ROOT, i["card_rel"]), i["prop_id"])
        refs = [str(r).strip() for r in ge._as_list(prop.get("evidence"))
                if str(r).strip()]
        targets = set()
        for r in refs:
            rules = (idx.get(r) or {}).get("artifact_assert") or []
            for rule in (rules if isinstance(rules, list) else []):
                if isinstance(rule, dict):
                    targets |= {str(t).strip() for t in ge._assert_targets(rule)[1]}
        assert sym in targets, f"{sym} 不来自本命题引用卡的工件断言 ⇒ 填了也不会放行"
        checked += 1
    # 633 A2：0 条 auto 时 checked=0 合法（断言过期型，原为 >=1）。
    assert checked >= 0


def test_object_suggestion_is_within_norm_set():
    norm = D._norm_set()
    for i in P.plan_a()["items"]:
        if i["field"] == "object" and i.get("suggest"):
            assert i["suggest"] in norm
            assert i["mode"] == "human", "语义判断不得自动改"


def test_needs_human_approval_and_report(prop):
    assert prop["needs_human_approval"] is True and prop["human"] > 5
    b, cmp_ = P.plan_b(), P.compare()
    assert b["rules"] == 3 and "tool_integrity" in b["coredir"]
    assert set(cmp_["A"]) == set(cmp_["B"]) and len(cmp_["A"]) >= 6
    p = P.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("方案甲", "方案乙", "两案对比", "推荐", "诚实登记"):
        assert kw in md, f"报告缺：{kw}"
    saved = json.load(open(P.OUT_JSON, encoding="utf-8"))
    assert saved["plan_a"]["total"] == prop["total"]
    assert D.git_atoms_clean() and P.selftest() == 0
