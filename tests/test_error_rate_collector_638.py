"""638 B1 · known_error_rate 收集器单测（>=5 例，纯标准库）。"""
from __future__ import annotations

import os

import tools.error_rate_collector_638 as m


# B1-1：分档规则（0 → 无数据；<30 → 先验；>=30 → tier=rule）
def test_estimation_tiers():
    r0 = m.estimate_rule({"id": "R", "severity": "block", "scope": "atom"}, 0, {})
    assert r0["tier"] == "无数据" and r0["fp_rate"] is None and r0["n_samples"] == 0
    r5 = m.estimate_rule({"id": "R", "severity": "block", "scope": "atom"}, 5, {})
    assert r5["tier"] == "scope" and r5["fp_rate"] == m.PRIOR
    assert "样本不足" in r5["confidence"]
    r30 = m.estimate_rule({"id": "R", "severity": "block", "scope": "atom"}, 30, {})
    assert r30["tier"] == "rule" and r30["fp_rate"] is None


# B1-2：67 条规则全有行（验收：67 条全部有估算值或标注）
def test_all_67_rules_have_rows():
    e = m.estimate_all()
    assert e["n_rules"] == 67 and len(e["rows"]) == 67
    for r in e["rows"]:
        assert r["rule_id"] and r["confidence"]
        assert r["fp_rate"] is not None or r["confidence"] == "无数据"


# B1-3：ledger 无规则字段 ⇒ 规则级样本恒为 0（不编造）
def test_ledger_has_no_rule_attribution():
    led = m.load_jsonl(m.LEDGER)
    assert len(led) == 452
    assert m.rule_samples(led) == {}
    assert not any(f in led[0] for f in m.RULE_FIELD_CANDIDATES)


# B1-4：代理指标数字真实（与台账/人审/逃逸一致）
def test_global_proxies_real_numbers():
    p = m.global_proxies(m.load_jsonl(m.LEDGER), m.load_jsonl(m.HUMAN),
                          m.load_jsonl(m.ESCAPE))
    assert p["ledger_n"] == 452
    assert p["ledger_approve"] == 367 and p["ledger_modify"] == 85
    assert p["ledger_reject"] == 0
    assert p["fp_proxy_modify_rate"] == round(85 / 452, 4)
    assert p["human_n"] == 388 and p["human_modify"] == 34
    assert p["escape_n"] == 1 and p["escape_judged"] == 1406
    assert p["fn_proxy_escape_rate"] == round(1 / 1406, 6)


# B1-5：逐规则样本注入时可归属（验证归一路径确实可用）
def test_rule_samples_attribution_path():
    led = [{"rule_id": "ATOM-ID-UNIQUE"}, {"rule_id": "ATOM-ID-UNIQUE"}, {"x": 1}]
    assert m.rule_samples(led) == {"ATOM-ID-UNIQUE": 2}


# B1-6：层级分布与无数据清单自洽
def test_tier_distribution_consistent():
    e = m.estimate_all()
    assert sum(e["tier_dist"].values()) == e["n_rules"]
    assert e["no_data_n"] == len(e["no_data_rules"])
    assert set(e["scope_dist"]) <= {"atom", "evidence", "repo", "unknown"}


# B1-7：输出路径在 data 下（--check 不写盘）
def test_output_paths_under_data():
    assert m.OUT_MD.startswith(os.path.join(m.ROOT, "data"))
    assert m.OUT_JSON.startswith(os.path.join(m.ROOT, "data"))
    assert m.PRIOR == 0.05 and m.MIN_SAMPLES == 30
