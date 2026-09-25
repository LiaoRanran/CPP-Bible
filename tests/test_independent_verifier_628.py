"""628 B1 · 独立验证者 单测（8 例）。"""
import json
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import independent_verifier_628 as I

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def test_zero_import_of_project_tools():
    src = open(I.__file__, encoding="utf-8").read()
    bad = re.findall(
        r"^\s*(?:import|from)\s+(?!json|hashlib|os|sys|argparse|re|tempfile|typing|__future__)(\w+)",
        src, re.MULTILINE)
    assert not bad


def test_w2_independent_recompute_matches():
    """独立重算（零项目导入的朴素实现）必须与系统权威源一致（640b：动态比对）。"""
    import w2_authority_640b as A
    exp = A.current()
    r = I.verify_w2()
    assert r["summary"] == {"IN": exp["IN"], "OUT": exp["OUT"], "UNDEC": exp["UNDEC"]}
    assert r["nodes"] == 121 and r["frozen_labels_match"]


def test_pck_independent_count_matches():
    p = I.verify_pck()
    assert p["total"] == 83
    assert p["authorized"] == 27
    assert p["pending"] == 56


def test_ledger_chain_valid():
    c = I.verify_ledger_chain()
    assert c["chain_valid"] and c["events"] == 452
    assert c["first_prev"] == "GENESIS"


def test_unique_review_items():
    u = I.verify_unique_review()
    assert u["unique"] == 93 and u["records"] == 93


def test_tamper_ledger_detected(tmp_path):
    src = os.path.join(HERE, "data", "authority", "decision_event_v2_ledger.jsonl")
    dst = tmp_path / "tampered.jsonl"
    lines = open(src, encoding="utf-8").read().splitlines()
    ev = json.loads(lines[10])
    ev["result"] = "REJECT"                    # 篡改一条结果
    lines[10] = json.dumps(ev, ensure_ascii=False)
    dst.write_text("\n".join(lines) + "\n", encoding="utf-8")
    c = I.verify_ledger_chain(str(dst))
    assert not c["chain_valid"], "篡改后哈希链必须断裂"


def test_tamper_pck_detected(tmp_path):
    src_dir = os.path.join(HERE, "data", "pck", "certificates")
    td = tmp_path / "certs"
    shutil.copytree(src_dir, td)
    # 篡改一张证书的 human_authority.status: approved → pending
    for name in sorted(os.listdir(td)):
        p = td / name
        txt = p.read_text(encoding="utf-8")
        if "status: approved" in txt:
            p.write_text(txt.replace("status: approved", "status: pending", 1),
                         encoding="utf-8")
            break
    p2 = I.verify_pck(str(td))
    assert p2["authorized"] == 26, "篡改后 authorized 数必须变化"


def test_run_all_aggregates():
    r = I.run_all()
    assert r["all_match"]
    assert set(r["checks"]) == {"w2_summary_match", "w2_frozen_labels_match",
                                "pck_authorized_match", "ledger_chain_valid",
                                "ledger_events_match", "unique_match"}
