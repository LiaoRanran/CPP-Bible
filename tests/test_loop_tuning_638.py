"""638 C2 · 闭环规则调优单测（>=5 例，纯标准库）。"""
from __future__ import annotations

import os

import tools.loop_tuning_638 as m

_SAMPLE = {"observation_pct": 100.0, "exception_clauses": 227, "taint_cards": 8,
           "grounding_pct": 35.8, "ahead": 9}


# C2-1：调优表结构完整（3 项，含 before/after/why/expected）
def test_tuning_table_shape():
    assert len(m.TUNING) == 3
    for t in m.TUNING:
        assert t["id"] and t["key"] and t["why"] and t["expected"]
        assert "before" in t and "after" in t


# C2-2：T1 停用 observation_pct（误报消除）
def test_t1_disables_observation():
    assert m.TUNED_THRESHOLDS["observation_pct"] is None
    assert m.ORIGINAL_THRESHOLDS["observation_pct"] == 30.0
    before = {a["key"] for a in m.detect_with(_SAMPLE, m.ORIGINAL_THRESHOLDS)}
    after = {a["key"] for a in m.detect_with(_SAMPLE, m.TUNED_THRESHOLDS)}
    assert "observation_pct" in before and "observation_pct" not in after


# C2-3：T2 放宽 exception_clauses 到 250
def test_t2_relaxes_exceptions():
    assert m.ORIGINAL_THRESHOLDS["exception_clauses"] == 100.0
    assert m.TUNED_THRESHOLDS["exception_clauses"] == 250.0
    after = {a["key"] for a in m.detect_with(_SAMPLE, m.TUNED_THRESHOLDS)}
    assert "exception_clauses" not in after
    # 300 条仍应命中（放宽不是取消）
    hit = m.detect_with({"exception_clauses": 300}, m.TUNED_THRESHOLDS)
    assert any(a["key"] == "exception_clauses" for a in hit)


# C2-4：真实异常不因调参被掩盖
def test_real_anomalies_preserved():
    before = {a["key"] for a in m.detect_with(_SAMPLE, m.ORIGINAL_THRESHOLDS)}
    after = {a["key"] for a in m.detect_with(_SAMPLE, m.TUNED_THRESHOLDS)}
    assert "taint_cards" in before and "taint_cards" in after
    assert "grounding_pct" in before and "grounding_pct" in after
    assert after < before          # 调后更少（消除误报）


# C2-5：T3 风险系数重算（report 0.5 → 0.75）
def test_t3_rescore_risk_factor():
    assert m.TUNED_RISK_FACTOR["report"] == 0.75
    rows = m.rescore([{"candidate": "a", "cost": "低", "benefit": "中", "risk_class": "report"},
                      {"candidate": "b", "cost": "低", "benefit": "中", "risk_class": "tool"}])
    assert rows[0]["candidate"] == "b"          # tool 1.0 > report 0.75
    assert {r["candidate"]: r["score"] for r in rows} == {"a": 1.5, "b": 2.0}


# C2-6：compare() 注入指标后的差异（消除两项误报，保留两项真异常）
def test_compare_removes_two_false_alarms():
    metrics = {"observation_pct": 100.0, "exception_clauses": 227, "taint_cards": 8,
               "grounding_pct": 35.8, "ahead": 9, "tools_total": 100, "tests_total": 100}
    c = m.compare(metrics)
    assert set(c["removed"]) == {"observation_pct", "exception_clauses"}
    assert c["added"] == []
    assert set(c["kept"]) == {"grounding_pct", "taint_cards"}
    assert c["n_after"] < c["n_before"]


# C2-6b：真实实时指标也能跑通（不依赖落盘 637_observer.json 的过期值）
def test_compare_with_fresh_metrics_runs():
    fm = m.fresh_metrics()
    assert fm and fm.get("rules") == 67
    c = m.compare(fm)
    assert c["n_after"] <= c["n_before"]
    assert "observation_pct" not in {a["key"] for a in c["after"]}
    assert "exception_clauses" not in {a["key"] for a in c["after"]}


# C2-7：未修改 637 工具（覆盖层独立性）
def test_overlay_does_not_touch_637():
    assert m.OBSERVER_JSON.endswith(os.path.join("data", "637_observer.json"))
    src_637 = open(os.path.join(m.ROOT, "tools", "error_detector_637.py"),
                   encoding="utf-8").read()
    assert "638" not in src_637           # 637 工具未被本批写入标记
    assert m.OUT_MD.startswith(os.path.join(m.ROOT, "data"))
