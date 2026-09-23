"""628 B4 · 他验端到端演示 单测（6 例）。

子进程调用 B1/B2/B3 较慢 ⇒ 用 module 级 fixture 缓存链路结果。
凡是生成了新凭证的测试都**随即追加进日志**，保证系统状态自洽
（最新凭证必须在册，否则后续 inclusion 检查会失败）。
"""
import json
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import third_party_audit_demo_628 as D


@pytest.fixture(scope="module")
def check_result():
    return D.run_check()


@pytest.fixture(scope="module")
def e2e_result():
    return D.run_e2e(write_report=True)


def test_e2e_check_all_green(check_result):
    assert check_result["all_ok"], check_result["checks"]


def test_independent_matches_system_v2(check_result):
    c = check_result["checks"]
    assert c["verifier_vs_system"] and c["w2_match"]
    assert check_result["independent_w2"] == {"IN": 114, "OUT": 7, "UNDEC": 0}


def test_pck_ledger_unique_consistency(check_result):
    c = check_result["checks"]
    assert c["pck_authorized_match"] and c["ledger_chain_valid"] and c["unique_match"]
    assert c["latest_vsa_valid"] and c["latest_vsa_in_log"]


def test_vsa_generated_appended_and_valid():
    path = D.step3_generate_vsa()
    assert os.path.exists(path)
    ap = D.step4_append_log(path)
    assert ap["ok"]
    inc = D.step_inclusion(path)
    assert inc["included"] and inc["log_index"] == ap["log_index"]
    assert D.step5_verify_log()["chain_valid"]


def test_e2e_run_writes_audit_report(e2e_result):
    assert e2e_result["all_green"]
    assert os.path.exists(D.OUT_MD) and os.path.exists(D.OUT_JSON)
    md = open(D.OUT_MD, encoding="utf-8").read()
    for kw in ("独立验证者", "VSA", "透明日志", "审计声明"):
        assert kw in md
    saved = json.load(open(D.OUT_JSON, encoding="utf-8"))
    assert saved["all_green"] and saved["audit_statement"]


def test_audit_statement_mentions_chain(e2e_result):
    s = e2e_result["audit_statement"]
    assert "独立验证者" in s and "透明日志" in s and "一致" in s
    assert e2e_result["inclusion"]["included"]
    assert e2e_result["log_state"]["chain_valid"]
