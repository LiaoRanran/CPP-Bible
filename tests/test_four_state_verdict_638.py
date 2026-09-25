"""638 3.1 · 四态结论 schema 单测（>=6 例，纯标准库）。"""
from __future__ import annotations

import os

import tools.four_state_verdict_638 as m

B = {
    "mutation_set_hash": "d7556d622e92fbf918cf9b49c39d97da0733c88fb686be7e734df7fca294ac57",
    "mutation_count": "1593",
    "generator_version": "mutation_fuzz@v7",
}


# 3.1-1：schema 四态完备
def test_schema_has_four_states():
    assert sorted(m.SCHEMA) == sorted(m.STATES)
    assert m.STATES == ["pass", "pass_with_exception", "fail", "unknown"]
    assert m.SCHEMA["unknown"]["requires"] == []


# 3.1-2：有边界 + pass/block 正常定态
def test_boundary_keeps_state():
    assert m.enforce({**B, "verdict": "pass"}) == "pass"
    assert m.enforce({**B, "verdict": "block"}) == "fail"


# 3.1-3：无边界一律降级 unknown（§3.1.3 核心）
def test_missing_boundary_downgrades_to_unknown():
    r = m.classify({"verdict": "pass"})
    assert r["state"] == "unknown"
    assert r["downgraded"] is True
    assert r["requested"] == "pass"
    assert r["boundary_ok"] is False
    assert any("mutation_set_hash" in x for x in r["reasons"])


# 3.1-4：边界格式非法也降级（hash / count / version 三种）
def test_invalid_boundary_forms_downgrade():
    assert m.enforce({"verdict": "pass", "mutation_set_hash": "zz",
                      "mutation_count": 3, "generator_version": "v"}) == "unknown"
    assert m.enforce({"verdict": "pass", "mutation_set_hash": B["mutation_set_hash"],
                      "mutation_count": 0, "generator_version": "v"}) == "unknown"
    assert m.enforce({"verdict": "pass", "mutation_set_hash": B["mutation_set_hash"],
                      "mutation_count": 3, "generator_version": "  "}) == "unknown"
    assert m.has_boundary(B) is True
    assert m.has_boundary({"mutation_count": "3"}) is False


# 3.1-5：pass_with_exception 必须有 explanation，否则降级
def test_pass_with_exception_requires_explanation():
    ok = {**B, "verdict": "pass", "exception": "条款X", "explanation": "因为 Y"}
    assert m.enforce(ok) == "pass_with_exception"
    bad = {**B, "verdict": "pass", "exception": "条款X"}
    r = m.classify(bad)
    assert r["state"] == "unknown" and r["downgraded"] is True
    assert r["boundary_ok"] is True   # 有边界，仍因缺 explanation 降级


# 3.1-6：边界描述完整（三字段 + 顺序稳定）
def test_boundary_of_shape():
    got = m.boundary_of(B)
    assert set(got) == set(m.BOUNDARY_FIELDS)
    assert got["mutation_count"] == "1593"


# 3.1-7：迁移计划是纯函数（只算不写、映射正确）
def test_migrate_plan_is_pure_mapping():
    plan = m.migrate_plan([{"file": "a.md", "state": "block"},
                           {"file": "b.md", "state": "pass"},
                           {"file": "c.md", "state": "???"}])
    assert [p["map_to"] for p in plan] == ["fail", "pass", "unknown"]
    assert plan[0]["legacy"] == "block"


# 3.1-8：真实语料审计（23 张 verified 卡在无边界下全部 unknown）
def test_audit_real_corpus():
    a = m.audit()
    assert len(a["baselines"]) >= 30
    assert set(a["baseline_dist"]) <= set(m.STATES)
    assert len(a["cards"]) >= 20
    # 实测：卡当前无边界三元组 ⇒ 全部 unknown（如实断言，若日后回填则此断言会失败并暴露）
    assert a["cards_with_boundary"] == 0
    assert a["card_dist"] == {"unknown": len(a["cards"])}


# 3.1-9：输出路径在 data 下（--check 不写盘）
def test_output_paths_under_data():
    assert m.OUT_MD.startswith(os.path.join(m.ROOT, "data"))
    assert m.OUT_JSON.startswith(os.path.join(m.ROOT, "data"))
