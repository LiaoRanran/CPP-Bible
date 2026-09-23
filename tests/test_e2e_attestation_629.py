"""629 C4 · 端到端他验编排 单测（6 例）。

module 级 fixture 跑一次真实端到端（约 5-10s：含 RSA-2048 生成 + 独立验证者子进程）。
"""
import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import e2e_attestation_629 as E
import transparency_log_628 as T


@pytest.fixture(scope="module")
def result():
    before = T.status()["entries"]
    d = E.run_e2e()
    d["_log_before"], d["_log_after"] = before, T.status()["entries"]
    return d


def test_e2e_all_green(result):
    assert result["all_green"], [s for s in result["steps"] if not s["ok"]]


def test_six_steps_with_timings(result):
    assert len(result["steps"]) == 6
    assert all(s["seconds"] >= 0 and s["detail"] for s in result["steps"])
    assert sum(s["seconds"] for s in result["steps"]) < 120


def test_production_log_zero_drift(result):
    assert result["_log_before"] == result["_log_after"], "演示不得写生产链（应走临时日志）"
    assert result["temp_log_entries"] == 1, "临时日志应恰好 1 条"


def test_credential_is_dual_signed(result):
    cred = result["credential"]
    assert cred["vsa_version"] == "1.0"
    assert cred["attestation"], "628 形态 HMAC attestation 必须保留"
    assert cred["signature"] and cred["signature_scheme"].startswith("RSA-2048")
    assert result["hmac"]["hmac_valid"] and result["hmac"]["input_hashes_valid"]
    assert result["pub_fingerprint"]


def test_independent_reverification_and_tamper(result):
    reverify = [s for s in result["steps"] if s["step"].startswith("⑤")][0]
    tamper = [s for s in result["steps"] if s["step"].startswith("⑥")][0]
    assert reverify["ok"] and "inclusion=True" in reverify["detail"]
    assert tamper["ok"], "篡改 results 后复验必须失败"


def test_report_written_with_chain_tree():
    p = E.write_report()
    md = open(p, encoding="utf-8").read()
    for kw in ("各步结果与耗时", "凭证链（文本树）", "生产日志", "局限"):
        assert kw in md, f"报告缺：{kw}"
    assert "RSA-2048" in md and "临时日志" in md
