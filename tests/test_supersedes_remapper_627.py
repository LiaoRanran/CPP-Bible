"""627 A2 · supersedes 重映射 单测（≥4 例）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import decision_event_v2_626 as D
import supersedes_remapper_627 as R


def test_source_ledger_untouched():
    import hashlib
    before = hashlib.sha256(open(R.SRC_LEDGER, "rb").read()).hexdigest()
    R.remap()
    after = hashlib.sha256(open(R.SRC_LEDGER, "rb").read()).hexdigest()
    assert before == after


def test_all_51_resolved():
    r = R.remap()
    assert r["replace_events"] == 51
    assert r["resolved"] == 51
    assert r["unresolved"] == 0


def test_remapped_chain_and_no_dangling():
    r = R.remap()
    rem = D.AuthorityLedger.import_jsonl(r["out"])
    assert rem.verify_chain()
    assert len(rem.all_events()) == 452
    ids = {e.event_id for e in rem.all_events()}
    dangling = [s for e in rem.all_events()
                if e.operation == "REPLACE"
                for s in (e.supersedes or []) if s not in ids]
    assert not dangling


def test_original_ledger_still_valid():
    D.AuthorityLedger.import_jsonl(R.SRC_LEDGER).verify_chain()


def test_remap_table_written():
    R.remap()
    import json
    mp = json.load(open(R.OUT_MAP, encoding="utf-8"))
    assert mp["summary"]["resolved"] == 51
    assert len(mp["remap_table"]) == 51
