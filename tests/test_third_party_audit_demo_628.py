"""628 B4 · 他验端到端演示 单测（7 例）。

子进程调用 B1/B2/B3 较慢 ⇒ 用 module 级 fixture 缓存链路结果。

幂等性说明：
- `--check`（`check_result`）**只读**：fixture 前后对凭证目录与日志做字节快照，
  由 `test_check_is_read_only` 断言零变化。
- 端到端实跑（`e2e_result`，生成交付报告）按定义会**新增 1 张凭证 + 1 条日志**，
  且随即追加入册（系统状态保持自洽：不存在未入册凭证）。
"""
import json
import os
import subprocess
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import third_party_audit_demo_628 as D


def _state() -> tuple:
    creds = tuple(sorted(os.listdir(D.VSA_DIR)))
    with open(D.LOG, "rb") as fh:
        return creds, fh.read()


@pytest.fixture(scope="module")
def check_result():
    before = _state()
    r = D.run_check()
    r["_state_before"], r["_state_after"] = before, _state()
    return r


@pytest.fixture(scope="module")
def e2e_result():
    return D.run_e2e(write_report=True)


def test_e2e_check_all_green(check_result):
    assert check_result["all_ok"], check_result["checks"]


def test_check_is_read_only(check_result):
    before, after = check_result["_state_before"], check_result["_state_after"]
    assert before[0] == after[0], "B4 --check 不得新增/删除凭证"
    assert before[1] == after[1], "B4 --check 不得改动透明日志"


def test_independent_matches_system_v2(check_result):
    import w2_authority_640b as A
    exp = A.current()
    c = check_result["checks"]
    assert c["verifier_vs_system"] and c["w2_match"]
    assert check_result["independent_w2"] == {"IN": exp["IN"], "OUT": exp["OUT"],
                                              "UNDEC": exp["UNDEC"]}


def test_pck_ledger_unique_consistency(check_result):
    c = check_result["checks"]
    assert c["pck_authorized_match"] and c["ledger_chain_valid"] and c["unique_match"]
    assert c["logged_vsa_valid"] and c["logged_vsa_in_log"]
    assert c["log_files_ok"] and c["all_credentials_logged"]


def test_vsa_generated_appended_and_valid(e2e_result):
    path = os.path.join(D.ROOT, e2e_result["vsa_path"])
    assert os.path.exists(path)
    assert e2e_result["log_append"]["ok"]
    assert e2e_result["inclusion"]["included"]
    assert e2e_result["inclusion"]["log_index"] == e2e_result["log_append"]["log_index"]
    assert e2e_result["log_state"]["chain_valid"]
    # 交叉验证：B2 按路径验证该凭证（独立于 B4 自己读到的字段）
    p = subprocess.run([sys.executable, D.VSA_TOOL, "--verify-path", path],
                       capture_output=True, text=True, cwd=D.ROOT, check=False)
    assert p.returncode == 0
    assert json.loads(p.stdout)["valid"]


def test_e2e_run_writes_audit_report(e2e_result):
    assert e2e_result["all_green"]
    assert os.path.exists(D.OUT_MD) and os.path.exists(D.OUT_JSON)
    md = open(D.OUT_MD, encoding="utf-8").read()
    for kw in ("独立验证者", "VSA", "透明日志", "审计声明"):
        assert kw in md
    saved = json.load(open(D.OUT_JSON, encoding="utf-8"))
    assert saved["all_green"] and saved["audit_statement"]
    assert saved["inclusion"]["included"]


def test_audit_statement_mentions_chain(e2e_result):
    s = e2e_result["audit_statement"]
    assert "独立验证者" in s and "透明日志" in s and "一致" in s
    assert e2e_result["inclusion"]["included"]
    assert e2e_result["log_state"]["chain_valid"]
