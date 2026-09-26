"""643 C2 · targeted_mutator_643 单测（5 类算子/空变异/算子选择/计划/dry-run）。
编号 C2-1..C2-9。
"""
from __future__ import annotations

import os

import targeted_mutator_643 as C2

CARD = ("---\nid: ATOM-X-001\ntitle: T\nstatus: verified\nn: 3\nflag: true\n"
        "relations:\n  - ATOM-Y-001\n---\n\n必须做到。\n")


# C2-1：field_delete 删除字段行
def test_field_delete():
    t, why = C2.apply_op(CARD, "field_delete", "title")
    assert "title:" not in t and "删除" in why


# C2-2：field_delete 找不到目标 ⇒ 空变异（原文返回，不抛错）
def test_field_delete_missing_is_noop():
    t, why = C2.apply_op(CARD, "field_delete", "not_exist")
    assert t == CARD and "未找到" in why


# C2-3：value_tamper 数值 +1
def test_value_tamper_numeric():
    t, why = C2.apply_op(CARD, "value_tamper", None)
    assert "n: 4" in t and "3 → 4" in why


# C2-4：value_tamper 布尔翻转（**本批实测过 IndexError，专门锁死**）
def test_value_tamper_boolean():
    t, why = C2.apply_op("---\nverified: true\n---\n", "value_tamper", None)
    assert "verified: false" in t, why
    t2, why2 = C2.apply_op("---\nok: false\n---\n", "value_tamper", None)
    assert "ok: true" in t2, why2


# C2-5：break_ref 把关系目标改成不存在的 id
def test_break_ref():
    t, why = C2.apply_op(CARD, "break_ref", None)
    assert "ATOM-Y-001-XX" in t and "不存在" in why


# C2-6：format_perturb 只动格式（语义等价：字段值不变）
def test_format_perturb_keeps_semantics():
    t, _ = C2.apply_op(CARD, "format_perturb", None)
    assert "status: verified" in t and "n: 3" in t
    assert t != CARD


# C2-7：equiv_rewrite 同义改写；未知算子返回原文（不炸）
def test_equiv_rewrite_and_unknown():
    t, why = C2.apply_op(CARD, "equiv_rewrite", None)
    assert "应当做到" in t, why
    t2, why2 = C2.apply_op(CARD, "no_such_op", None)
    assert t2 == CARD and "未知算子" in why2


# C2-8：算子选择（含阈、顺序稳定、无字段不凑 field_delete）
def test_ops_for():
    assert "field_delete" in C2.ops_for({"field_missing_silent"}, ["status"])
    assert "field_delete" not in C2.ops_for(set(), [])
    for kinds in ({"field_missing_silent"}, {"regex_fragile"}, {"numeric_threshold"}):
        n = len(C2.ops_for(kinds, ["status"]))
        assert C2.MIN_PER_RULE <= n <= C2.MAX_PER_RULE
    assert C2.ops_for({"regex_fragile"}, []) == C2.ops_for({"regex_fragile"}, [])


# C2-9：计划形态（dry-run：不带 apply；每规则 3–5 条；expected_oracle 指向目标规则）
def test_plan_shape_and_dry_run():
    p = C2.make_plan()
    assert p["dry_run"] is True and p["n"] > 0
    assert all(x["expected_oracle"] == x["target_rule"] for x in p["plans"])
    per_rule: dict[str, int] = {}
    for x in p["plans"]:
        per_rule[x["target_rule"]] = per_rule.get(x["target_rule"], 0) + 1
    assert all(3 <= v <= 5 for v in per_rule.values())
    assert all(x["op"] in C2.OPS for x in p["plans"])
    assert os.path.isdir(os.path.join(C2.ROOT, "atoms"))
    assert C2.selftest() == 0
