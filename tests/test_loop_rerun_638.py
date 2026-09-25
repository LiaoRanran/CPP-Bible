"""638 C1 · 闭环第二次运行单测（>=5 例，纯标准库）。"""
from __future__ import annotations

import os

import tools.loop_rerun_638 as m


# C1-1：闭环跑通且结构完整
def test_run_loop_structure():
    r = m.run_loop()
    assert r["metrics"] and r["metrics"].get("rules") == 67
    assert isinstance(r["anomalies_before"], list) and isinstance(r["anomalies"], list)
    assert r["n_candidates"] >= 1
    assert len(r["top3"]) == 3


# C1-2：调优生效（调后异常更少 + 误报被消除）
def test_tuning_effect_in_second_run():
    r = m.run_loop()
    before = {a["key"] for a in r["anomalies_before"]}
    after = {a["key"] for a in r["anomalies"]}
    assert after < before                     # 真子集：只减不增
    assert not (set(m.FALSE_ALARMS_637) & after)
    assert set(m.FALSE_ALARMS_637) <= before


# C1-3：top3 按分数降序，且都带建议与理由
def test_top3_sorted_and_actionable():
    r = m.run_loop()
    scores = [x["score"] for x in r["top3"]]
    assert scores == sorted(scores, reverse=True)
    for x in r["top3"]:
        assert x["candidate"] and x["action"] and x["reason"]
        assert "score" in x["reason"]


# C1-4：与第一次对比（误报率 0.5 → 0.0）
# 639 修正：改用**注入指标**的确定性断言。原实现用实时指标，库规模每增一批
# （如 639 新增工具/测试）就会让 637 原始阈值多触发一条"增长类"异常，
# 0.5 这类具体比率随之漂移——调参语义本身没变（见 C1-4b 的实时版）。
def test_comparison_with_first_run():
    fake = {
        "generated": "x", "metrics": {},
        "anomalies_before": [{"key": k} for k in
                             ("observation_pct", "exception_clauses",
                              "grounding_pct", "taint_cards")],
        "anomalies": [{"key": k} for k in ("grounding_pct", "taint_cards")],
        "n_candidates": 1, "top3": [{"candidate": "x"}],
    }
    c = m.compare(fake)
    assert c["false_alarm_first"] == 2 and c["false_alarm_second"] == 0
    assert c["false_alarm_rate_first"] == 0.5
    assert c["false_alarm_rate_second"] == 0.0
    assert c["n_anomalies_second"] < c["n_anomalies_first"]
    assert isinstance(c["top3_changed"], bool)
    assert isinstance(c["top3_overlap"], list)


# C1-4b：实时指标版（结构性断言，不锁具体比率——库增长不破坏）
def test_comparison_with_live_run_structure():
    c = m.compare()
    assert c["n_anomalies_second"] <= c["n_anomalies_first"]
    assert c["false_alarm_second"] == 0          # 调后不再有 637 已知误报
    assert isinstance(c["top3_overlap"], list)


# C1-5：对比可注入（纯函数性，便于回归）
def test_compare_accepts_injected_run():
    fake = {"generated": "x", "metrics": {}, "anomalies_before": [{"key": "observation_pct"}],
            "anomalies": [], "n_candidates": 0, "top3": [{"candidate": "z"}]}
    c = m.compare(fake)
    assert c["n_anomalies_first"] == 1 and c["n_anomalies_second"] == 0
    assert c["false_alarm_first"] == 1 and c["false_alarm_second"] == 0
    assert c["second_top3"] == ["z"]


# C1-6：memo 正文含 637 门禁要求的三处标记
def test_memo_has_required_markers():
    r = m.run_loop()
    txt = m.memo_text(r, m.compare(r))
    assert "自动生成" in txt
    assert "人审批后才执行" in txt
    assert "我建议下一步做什么" in txt
    assert "与第一次产出（637）的对比" in txt


# C1-7：体检状态判定（停用项显示停用，真缺口显示告警）
def test_status_display():
    assert m._status("observation_pct", 100.0, None) == "— (停用)"
    assert m._status("grounding_pct", 35.8, 50.0) == "⚠️"
    assert m._status("grounding_pct", 60.0, 50.0) == "✅"
    assert m._status("taint_cards", 8, 5.0) == "⚠️"
    assert m._status("pytest_failures", None, 5.0) == "❓"


# C1-8：只读契约与输出路径
def test_paths_and_readonly():
    assert m.OUT_MD.startswith(os.path.join(m.ROOT, "data"))
    assert m.OUT_JSON.startswith(os.path.join(m.ROOT, "data"))
    assert m.SCORED_637.endswith(os.path.join("data", "637_scored.json"))
    src = open(os.path.join(m.ROOT, "tools", "loop_rerun_638.py"), encoding="utf-8").read()
    assert "--check" in src
