"""642 C1 · auto_executor_whitelist_eval_642 单测（评估只读 / 风险分 / 判决面拒绝 / 门槛）。
编号 C1-1..C1-7。
"""
from __future__ import annotations

import hashlib

import auto_executor_640 as ae
import auto_executor_whitelist_eval_642 as W


# C1-1：只评估不改（640 白名单与受保护路径常量一字未动；源码字节不变）
def test_evaluation_is_readonly():
    path = ae.__file__
    before = hashlib.sha256(open(path, "rb").read()).hexdigest()
    assert list(ae.WHITELIST) == ["control_chars", "final_newline", "trailing_ws",
                                 "ruff_fix", "snapshot_update"]
    r = W.evaluate()
    assert r["current_whitelist"] == list(ae.WHITELIST)
    W.honest_diff()
    after = hashlib.sha256(open(path, "rb").read()).hexdigest()
    assert before == after, "白名单评估不得改动 auto_executor_640"


# C1-2：判决面 / 不可逆 ⇒ 一律拒绝（铁律）
def test_judgment_surface_and_irreversible_are_rejected():
    r = W.evaluate()
    for row in r["rows"]:
        if row["zone"] == "判决/信任面" or not row["reversible"]:
            assert row["verdict"] == "拒绝", row["category"]


# C1-3：三条硬红线类别（账本 / 规则 / 知识卡）都被拒绝
def test_hard_redlines_rejected():
    r = W.evaluate()
    by = {row["category"]: row for row in r["rows"]}
    for c in ("ledger_write", "gate_rule_edit", "knowledge_card_edit"):
        assert by[c]["verdict"] == "拒绝"
    assert "代签" in by["ledger_write"]["note"]


# C1-4：风险分机械可复算（含不可逆翻倍）
def test_score_formula_is_recomputable():
    assert W.score_of({"zone": "数据产物", "reversible": True, "blast": "单文件"}) == 3
    assert W.score_of({"zone": "数据产物", "reversible": False, "blast": "单文件"}) == 6
    assert W.score_of({"zone": "文档/报告", "reversible": True, "blast": "数文件"}) == 3
    assert W.score_of({"zone": "判决/信任面", "reversible": True, "blast": "仓库级"}) == 8


# C1-5：门槛未达 ⇒ 低风险候选只到「技术可入选（本批不扩大）」
def test_gate_not_passed_defers_low_risk_candidates():
    r = W.evaluate()
    assert r["gate"]["passed"] is False
    assert r["by_verdict"].get("技术可入选（本批不扩大）", 0) >= 1
    assert "可入选" not in r["by_verdict"], "门槛未达时不得出现『可入选』"


# C1-6：每条候选都有护栏、回滚方案与结论理由（缺一不可）
def test_every_candidate_has_guardrails_rollback_and_reason():
    r = W.evaluate()
    for row in r["rows"]:
        assert row["guardrails"], row["category"]
        assert row["rollback"], row["category"]
        assert row["verdict_reason"], row["category"]


# C1-7：照出 inbox 口径 ≠ 代码事实 + --check 自检
def test_honest_diff_and_selftest():
    d = W.honest_diff()
    assert d["consistent"] is False
    assert "测试断言数字更新" in d["inbox_claimed"]
    assert "test_assertion_number_update" not in d["code_actual"]
    assert "add_check_flag" not in d["code_actual"]
    assert W.selftest() == 0
