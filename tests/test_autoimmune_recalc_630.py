"""630 A3 · 修复后干跑复算 单测（6 例）。

含真求值（gate `_prop_liveness_ok` / `principal_ok`）⇒ module fixture 缓存。
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import autoimmune_diagnose_630 as D
import autoimmune_fix_proposal_630 as P
import autoimmune_recalc_630 as R


@pytest.fixture(scope="module")
def s():
    return R.scenarios()


def test_v23_thresholds_parsed(s):
    th = s["thresholds"]
    assert th["found"]
    assert (th["hard_target_pct"], th["hard_cap_pct"]) == (5, 10)
    assert (th["soft_target_pct"], th["soft_fatigue_pct"]) == (20, 40)


def test_strict_scenario_real_verification(s):
    assert s["strict"]["filled_auto"] == 42
    assert s["strict"]["verified_pass"] == 42 and not s["strict"]["failed"], \
        "auto 建议必须经 gate 自己的判定放行，否则不算可自动修复"
    assert s["strict"]["remaining_warns"] == s["total_warns"] - 42
    assert s["strict"]["cards_became_clean"] == 0
    assert s["strict"]["cards_still_warned"] == 23


def test_liveness_verification_is_real():
    a = P.plan_a()
    item = [i for i in a["items"] if i["mode"] == "auto"][0]
    path = os.path.join(R.ROOT, item["card_rel"])
    good = R.verify_liveness_fill(path, item["prop_id"], item["value"]["symbol"])
    bad = R.verify_liveness_fill(path, item["prop_id"], "totally-bogus-symbol-xyz")
    assert good["ok"] and not bad["ok"], "判定必须能区分有效符号与伪造符号"


def test_optimistic_scenario(s):
    o = s["optimistic"]
    assert o["signoff_verified"]["ok"] and o["signoff_verified"]["principal"] \
        in [f"human:{n}" for n in R._ge().HUMAN_PRINCIPALS]
    assert o["object_total"] == o["object_verified_by_suggestion"] \
        + o["object_without_suggestion"]
    assert o["remaining_warns"] == 0 and o["soft_rate_pct"] == 0.0
    assert any("语义正确性机器不能验证" in a for a in o["assumptions"])


def test_pessimistic_scenario_worse_than_nothing(s):
    p = s["pessimistic"]
    assert not p["principal_ok"]["ok"], "机器代签必须被判失败"
    assert p["block_events"] == s["optimistic"]["signed_by_total"] > 0
    assert p["hard_rate_pct"] > s["thresholds"]["hard_target_pct"], \
        "悲观情景硬开火率必须越过 v23 目标（这是本批最重要的风险提示）"


def test_read_only_report_and_selftest(s):
    assert D.git_atoms_clean()
    p = R.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("三情景对比", "阈值对照", "关键解读", "人填清单", "局限"):
        assert kw in md, f"报告缺：{kw}"
    saved = json.load(open(R.OUT_JSON, encoding="utf-8"))
    assert saved["strict"]["verified_pass"] == s["strict"]["verified_pass"]
    assert R.selftest() == 0
