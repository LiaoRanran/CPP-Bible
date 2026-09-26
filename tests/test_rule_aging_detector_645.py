"""645 A6 规则老化检测单测（fast 组：用合成带时间戳账本）。"""
import json
import os
import sys
import tempfile

sys.path.insert(0, "tools")

import rule_aging_detector_645 as a6
import rule_error_tracker_645 as a5


def test_selftest_passes():
    assert a6.selftest() == 0


def test_detect_trend_declining(monkeypatch):
    ledger = []
    # R1：更早窗口触发 5 次，近窗触发 1 次 → 明显下滑 → 老化
    for i in range(5):
        ledger.append({"target_id": "R1", "result": "APPROVE", "operation": "CREATE",
                       "basis_refs": [], "decided_at": "2026-01-0%dT00:00:00" % (i + 1)})
    for i in range(1):
        ledger.append({"target_id": "R1", "result": "APPROVE", "operation": "CREATE",
                       "basis_refs": [], "decided_at": "2026-09-1%dT00:00:00" % (i + 1)})
    fd, path = tempfile.mkstemp(suffix=".jsonl", prefix="645age_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as fh:
        for r in ledger:
            fh.write(json.dumps(r) + "\n")
    monkeypatch.setattr(a5, "LEDGER", path)
    res = a6.detect(rules=["R1"])
    assert "R1" in res["aging_rules"], "下滑规则应被判为老化"
    assert res["per_rule"]["R1"]["aging_signal"] > 0.1
    os.unlink(path)


def test_real_ledger_readable():
    from datetime import datetime
    res = a6.detect(rules=a5.RULE_IDS or [], now=datetime(2026, 9, 26))
    assert "per_rule" in res
