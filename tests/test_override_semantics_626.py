"""626 C2 · OVERRIDE 语义验证回归测试（≥6 例）。"""
import sys
import tempfile

import pytest

ROOT = __import__("os").path.dirname(__import__("os").path.dirname(
    __import__("os").path.abspath(__file__)))
sys.path.insert(0, ROOT + "/tools")
import decision_event_v2_626 as D  # noqa: E402
import override_semantics_verify_626 as O  # noqa: E402


def _ledger_with_replace():
    led = D.AuthorityLedger()
    e1 = D.make_event("edge", "ae-1", "APPROVE", reviewer="A")
    led.append(e1)
    e2 = D.make_event("edge", "ae-1", "MODIFY", reviewer="A", operation="REPLACE",
                      supersedes=[e1.event_id], modification="改判")
    led.append(e2)
    return led


def test_selftest_passes():
    assert O.selftest() == 0


def test_valid_replace_passes():
    led = _ledger_with_replace()
    with tempfile.TemporaryDirectory() as td:
        p = td + "/l.jsonl"
        led.export_jsonl(p)
        r = O.verify(p)
    assert r["ok"] and not r["problems"]
    assert r["replace_events"] == 1


def test_replace_without_supersedes_fails():
    led = D.AuthorityLedger()
    # 强行构造：先建合法 REPLACE 再清空 supersedes
    e1 = D.make_event("edge", "ae-1", "APPROVE", reviewer="A")
    led.append(e1)
    e2 = D.make_event("edge", "ae-1", "MODIFY", reviewer="A", operation="REPLACE",
                      supersedes=[e1.event_id], modification="改判")
    led.append(e2)
    e2.supersedes = []           # 破坏语义
    with tempfile.TemporaryDirectory() as td:
        p = td + "/l.jsonl"
        led.export_jsonl(p)
        r = O.verify(p)
    assert not r["ok"]
    assert any("supersedes" in x for x in r["problems"])


def test_supersedes_dangling_is_warning_not_failure():
    """旧式引用（dec-* / legacy:*）非空可溯源 ⇒ 判据 5 已满足，仅告警。"""
    led = _ledger_with_replace()
    led.all_events()[1].supersedes = ["dec-000178"]
    with tempfile.TemporaryDirectory() as td:
        p = td + "/l.jsonl"
        led.export_jsonl(p)
        r = O.verify(p)
    assert r["ok"], r["problems"]
    assert r["unresolved_legacy_refs"] == 1
    assert r["warnings"]


def test_replace_must_have_result():
    led = _ledger_with_replace()
    led.all_events()[1].result = ""
    with tempfile.TemporaryDirectory() as td:
        p = td + "/l.jsonl"
        led.export_jsonl(p)
        r = O.verify(p)
    assert not r["ok"]
    assert any("result" in x for x in r["problems"])


def test_real_ledger_replace_semantics():
    r = O.verify()
    assert r["chain_ok"]
    assert r["replace_events"] == 51
    assert r["ok"], r["problems"]


@pytest.mark.parametrize("result", ["APPROVE", "REJECT", "MODIFY", "ABSTAIN"])
def test_all_results_accepted(result):
    led = D.AuthorityLedger()
    e1 = D.make_event("edge", "ae-1", "APPROVE", reviewer="A")
    led.append(e1)
    kw = {"operation": "REPLACE", "supersedes": [e1.event_id]}
    if result == "MODIFY":
        kw["modification"] = "改判"
    if result == "ABSTAIN":
        kw["abstain_reason"] = "证据不足"
    led.append(D.make_event("edge", "ae-1", result, reviewer="A", **kw))
    assert led.verify_chain()
