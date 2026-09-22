"""626 B1 · DecisionEvent v2 / AuthorityLedger 回归测试（≥10 例）。"""
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import decision_event_v2_626 as D  # noqa: E402


def _ledger2() -> D.AuthorityLedger:
    led = D.AuthorityLedger()
    e1 = D.make_event("edge", "ae-1", "APPROVE", reviewer="A", decided_at="2026-01-01")
    led.append(e1)
    e2 = D.make_event("edge", "ae-1", "REJECT", reviewer="A", decided_at="2026-01-02",
                      operation="REPLACE", supersedes=[e1.event_id])
    led.append(e2)
    return led


def test_event_creation_and_hash():
    e = D.make_event("edge", "ae-1", "APPROVE", reviewer="A")
    e.finalize(prev_hash=D.GENESIS, seq=1)
    assert len(e.self_hash) == 64
    assert e.event_id.startswith("AE-000001-")
    assert e.compute_self_hash() == e.self_hash


def test_ledger_append_and_chain():
    led = _ledger2()
    assert len(led) == 2
    assert led.verify_chain()
    assert led.all_events()[1].prev_hash == led.all_events()[0].self_hash


def test_supersedes_get_current():
    led = _ledger2()
    cur = led.get_current("edge", "ae-1")
    assert cur is not None and cur.result == "REJECT"
    assert len(led.get_all("edge", "ae-1")) == 2


def test_export_import_roundtrip():
    led = _ledger2()
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "l.jsonl")
        led.export_jsonl(p)
        led2 = D.AuthorityLedger.import_jsonl(p)
    assert len(led2) == 2
    assert led2.verify_chain()
    assert [e.self_hash for e in led2.all_events()] == \
        [e.self_hash for e in led.all_events()]


def test_count_by_review_method_and_origin():
    led = _ledger2()
    assert led.count_by_review_method() == {"BATCH_AUTH": 2}
    assert led.count_by_decision_origin() == {"human_observed": 2}


def test_independent_human_review_count_zero():
    led = _ledger2()
    assert led.independent_human_review_count() == 0
    led.append(D.make_event("edge", "ae-9", "APPROVE", reviewer="A",
                            review_method="ITEM_BLIND",
                            decision_origin="human_observed"))
    assert led.independent_human_review_count() == 1


def test_append_only_no_update_delete():
    led = D.AuthorityLedger()
    assert not hasattr(led, "update")
    assert not hasattr(led, "delete")


def test_illegal_event_rejected():
    led = D.AuthorityLedger()
    bad = D.make_event("edge", "ae-2", "MODIFY")      # 缺 modification
    assert bad.validate()
    try:
        led.append(bad)
        assert False, "应抛 ValueError"
    except ValueError:
        pass
    assert len(led) == 0


def test_replace_requires_supersedes():
    e = D.make_event("edge", "ae-3", "APPROVE", operation="REPLACE")
    assert any("supersedes" in x for x in e.validate())


def test_cross_granularity_warning_field():
    e = D.make_event("card", "ATOM-X", "APPROVE",
                     cross_granularity_warning="edge→card 不自动升级")
    assert e.cross_granularity_warning
    assert "cross_granularity_warning" in e.to_dict()


def test_selftest_passes():
    assert D.selftest() == 0
