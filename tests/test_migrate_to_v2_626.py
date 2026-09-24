"""626 B2 · 数据迁移回归测试（≥8 例）。"""
import hashlib
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import decision_event_v2_626 as D  # noqa: E402
import migrate_to_decision_event_v2_626 as M  # noqa: E402
import soft_baseline_634 as SB  # 634 A3  # noqa: E402

ANN = os.path.join(ROOT, "data", "human_attack_edge_annotations.jsonl")
AUTH = os.path.join(ROOT, "data", "authority", "authority_log.jsonl")
LEDGER = os.path.join(ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")


def test_selftest_passes():
    assert M.selftest() == 0


def test_input_counts():
    evs, st = M.build_events()
    assert st["annotations"] == 388
    assert st["authority"] == 418
    assert st["annotations"] + st["authority"] == 806
    assert len(evs) == 806


def test_migration_dedup_and_size():
    led, st = M.migrate()
    assert st["ledger_size"] == st["after_dedup"]
    assert st["ledger_size"] == st["input_total"] - st["duplicates_removed"]
    assert st["duplicates_removed"] > 0      # 确实发生了去重（非 806 直抄）


def test_hash_chain_valid():
    led, _st = M.migrate()
    assert led.verify_chain()


def test_review_method_mapping():
    led, st = M.migrate()
    by = led.count_by_review_method()
    # 634 A3：全局计数，读单一基线
    assert by.get("ITEM_OPEN") == SB.soft("item_open", by.get("ITEM_OPEN"))
    assert by.get("MIRROR_DERIVED") == st["mirror"]  # 194 镜像边
    assert sum(by.values()) == len(led)


def test_independent_human_review_is_zero():
    led, _st = M.migrate()
    assert led.independent_human_review_count() == 0
    assert led.count_by_decision_origin().get("user_authorized_execution") == 30


def test_backward_compat_old_files_untouched():
    before_ann = hashlib.sha256(open(ANN, "rb").read()).hexdigest()
    before_auth = hashlib.sha256(open(AUTH, "rb").read()).hexdigest()
    M.migrate()
    assert hashlib.sha256(open(ANN, "rb").read()).hexdigest() == before_ann
    assert hashlib.sha256(open(AUTH, "rb").read()).hexdigest() == before_auth


def test_ledger_file_generated():
    assert os.path.exists(LEDGER)
    led = D.AuthorityLedger.import_jsonl(LEDGER)
    assert len(led) > 0
    assert led.verify_chain()


def test_report_generated():
    led, st = M.migrate()
    txt = M.render_report(led, st)
    assert "迁移条数" in txt and "向后兼容" in txt
    assert os.path.exists(os.path.join(ROOT, "data", "migration_report_v2_626.md"))
