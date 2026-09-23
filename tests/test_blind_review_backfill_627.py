"""627 C2 · Blind Review 回填 单测（≥4 例）。"""
import hashlib
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import blind_review_backfill_627 as B


def test_build_entry_valid():
    e = B.build_backfill_entry("RI-x", "edge", "ae-A->B", "APPROVE",
                               "r", "HUMAN", seq=1)
    assert e["review_method"] == "ITEM_BLIND"
    assert e["decision_origin"] == "human_observed"
    assert not B.validate_entries([e])


def test_stage_does_not_touch_ledger():
    before = hashlib.sha256(open(B.LEDGER, "rb").read()).hexdigest()
    B.stage([{"review_item_id": "RI-x", "target_type": "edge",
              "target_id": "ae-A->B", "decision": "APPROVE",
              "rationale": "t", "reviewer": "H"}], B.STAGE)
    after = hashlib.sha256(open(B.LEDGER, "rb").read()).hexdigest()
    assert before == after
    assert os.path.exists(B.STAGE)


def test_load_decisions_from_unfilled_pack_empty():
    # 默认包无 human_decision ⇒ 返回空
    assert B.load_decisions_from_pack() == []


def test_append_to_ledger_not_called_in_check():
    # selftest 已静态确认；此处再确认运行 --check 不修改 ledger 大小
    before = os.path.getsize(B.LEDGER)
    rc = B.selftest()
    after = os.path.getsize(B.LEDGER)
    assert rc == 0
    assert before == after
