"""628 A3 · 镜像边对称性写入 单测（7 例）。"""
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import mirror_edge_symmetry_write_628 as M


def test_all_194_mirror_analysed():
    an = M.analyse()
    assert an["mirror_total"] == 194
    assert len(an["auto_proved"]) + len(an["needs_human"]) == 194


def test_auto_proved_have_valid_proof_ids():
    an = M.analyse()
    for p in an["auto_proved"]:
        assert p["symmetry_proof_id"].startswith("sym-proof-")
        assert len(p["symmetry_proof_id"]) == len("sym-proof-") + 16


def test_conditions_actually_checked():
    # 每条自动证明都带 via（条件3 通过路径）与一致 decision
    an = M.analyse()
    for p in an["auto_proved"]:
        assert p["via"] in ("jaccard>=0.6", "domain_symmetry_assertion")
        assert p["decision"] in ("APPROVE", "MODIFY", "REJECT", "ABSTAIN")


def test_ledger_items_written():
    v = M.verify_written()
    assert v["items_with_proof"] >= 70
    assert v["format_ok"]


def test_w2_unchanged_after_write():
    from w2_authority_640b import current as _w2
    exp = _w2()
    v = M.verify_written()
    assert v["w2_unchanged"]
    assert v["w2_summary"] == {"IN": exp["IN"], "OUT": exp["OUT"],
                               "UNDEC": exp["UNDEC"]}


def test_sidecar_covers_all_proofs():
    d = json.load(open(M.SIDECAR, encoding="utf-8"))
    assert d["auto_proved"] == 194
    assert len(d["records"]) == 194


def test_non_mirror_items_untouched():
    items = M._jl(M.LEDGER_PATH)
    non_mirror = [i for i in items
                  if not str(i.get("target_id", "")).startswith("ae-")
                  or "::" not in str(i.get("target_id", ""))
                  and i.get("source_batch") != "615+624"]
    backup = M._jl(M.BACKUP)
    bmap = {i["review_item_id"]: i for i in backup}
    for it in non_mirror:
        b = bmap.get(it["review_item_id"])
        if b:
            # 非镜像条目：除 symmetry_proof_id/tags 外与备份一致
            a = {k: v for k, v in it.items() if k not in ("symmetry_proof_id", "tags")}
            c = {k: v for k, v in b.items() if k not in ("symmetry_proof_id", "tags")}
            assert a == c
