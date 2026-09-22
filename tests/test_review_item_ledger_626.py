"""626 B3 · 唯一审查账本回归测试（≥8 例）。"""
import os
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import review_item_ledger_626 as R  # noqa: E402

LEDGER = os.path.join(ROOT, "data", "review_item_ledger.jsonl")


def test_selftest_passes():
    assert R.selftest() == 0


def test_migration_93_unique_110_records():
    led, st = R.migrate()
    assert st["from_615"] == 30
    assert st["from_624"] == 80
    assert st["overlap"] == 17
    assert st["records"] == 110            # 记录条数
    assert st["unique"] == 93              # 唯一复核对象（判据 2）


def test_duplicate_add_does_not_create_record():
    led = R.ReviewItemLedger()
    it = R.ReviewItem(target_type="edge", target_id="ae-x")
    led.add(it)
    led.add(R.ReviewItem(target_type="edge", target_id="ae-x"))
    assert led.get_record_count() == 1
    assert led.get_unique_count() == 1


def test_uniqueness_verification():
    led, _st = R.migrate()
    assert led.verify_uniqueness()
    assert led.verify_statuses()


def test_revision_and_supersedes():
    led = R.ReviewItemLedger()
    it = R.ReviewItem(target_type="edge", target_id="ae-y")
    rid1 = led.add(it)
    led.mark_decided(rid1, "AE-000001-aaaaaaaa")
    rid2 = led.add(R.ReviewItem(target_type="edge", target_id="ae-y"))
    assert rid1 != rid2                        # id 含 revision，全局唯一
    newer = led.get(rid2)
    assert newer.review_revision == 2
    assert rid1 in newer.supersedes


def test_state_machine_mark_decided():
    led = R.ReviewItemLedger()
    rid = led.add(R.ReviewItem(target_type="edge", target_id="ae-z"))
    assert led.get(rid).status == "pending"
    assert led.mark_decided(rid, "AE-000002-bbbbbbbb")
    assert led.get(rid).status == "decided"
    assert led.get(rid).current_decision_id == "AE-000002-bbbbbbbb"


def test_export_import_roundtrip():
    led, _st = R.migrate()
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "r.jsonl")
        led.export_jsonl(p)
        led2 = R.ReviewItemLedger.import_jsonl(p)
    assert led2.get_record_count() == led.get_record_count()
    assert led2.get_unique_count() == 93


def test_sorted_by_ambiguity():
    led, _st = R.migrate()
    s = led.sorted_by_ambiguity()
    scores = [it.ambiguity_score for it in s]
    assert scores == sorted(scores, reverse=True)


def test_ledger_file_generated():
    assert os.path.exists(LEDGER)
    led = R.ReviewItemLedger.import_jsonl(LEDGER)
    assert led.get_unique_count() == 93
