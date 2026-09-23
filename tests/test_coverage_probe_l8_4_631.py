"""631 D2 · 探针 L8.4（透明日志伪造）单测（4 例）。

探针只攻击**临时副本**，生产日志必须零改动（用 sha256 前后比对断言）。
"""
import hashlib
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import coverage_probe_l8_4_631 as P


def _log_hash() -> str:
    return hashlib.sha256(open(P.PROD_LOG, "rb").read()).hexdigest()


def test_production_log_untouched():
    before = _log_hash()
    m = P.measure()
    assert _log_hash() == before, "探针必须只攻击临时副本"
    assert m["prod_entries"] > 0


def test_five_scenarios_all_run():
    m = P.measure()
    ids = [s["id"] for s in m["scenarios"]]
    assert ids == [0, 1, 2, 3, 4], ids
    assert m["detected_all"] is True


def test_baseline_valid_and_tampering_detected():
    m = P.measure()
    by_id = {s["id"]: s for s in m["scenarios"]}
    assert by_id[0]["chain_valid"] is True, "基线（原样拷贝）链必须完整"
    for i in (1, 2, 3):
        assert by_id[i]["chain_valid"] is False, f"场景 {i} 的伪造必须被检出"
    assert by_id[4]["rejected"] is True, "凭证不存在 ⇒ 追加必须被拒"


def test_report_and_selftest():
    md = P.write_report()
    text = open(md, encoding="utf-8").read()
    for kw in ("透明日志伪造", "诚实登记"):
        assert kw in text
    assert json.load(open(P.OUT_JSON, encoding="utf-8"))["vector"] == "L8.4"
    assert P.selftest() == 0
    assert _log_hash() == _log_hash()
