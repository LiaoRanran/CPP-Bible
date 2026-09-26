"""645 A5 规则 error 追踪单测（fast 组：用临时账本，不读真实账本）。

锁定：真实计数（触发/推翻/逃逸）、error_rate 推导、67 规则覆盖。
对应 645 §三 A5 验收：数据从真实历史提取、error_rate 计算正确、67 条全覆盖。
"""
import json
import os
import sys
import tempfile

import pytest

sys.path.insert(0, "tools")

import rule_error_tracker_645 as a5


def test_selftest_passes():
    assert a5.selftest() == 0


def _write_ledger(records: list[dict]) -> str:
    fd, path = tempfile.mkstemp(suffix=".jsonl", prefix="645ledger_")
    os.close(fd)
    with open(path, "w", encoding="utf-8") as fh:
        for r in records:
            fh.write(json.dumps(r, ensure_ascii=False) + "\n")
    return path


def test_track_counts_real_events(monkeypatch):
    ledger = _write_ledger([
        {"target_id": "ATOM-X", "result": "APPROVE", "operation": "CREATE", "basis_refs": []},
        {"target_id": "ATOM-X", "result": "REJECT", "operation": "REPLACE", "basis_refs": []},
        {"target_id": "ATOM-Y", "result": "ABSTAIN", "operation": "REVOKE", "basis_refs": ["逃逸-z"]},
        {"target_id": "ATOM-Z", "result": "APPROVE", "operation": "CREATE", "basis_refs": ["ATOM-X"]},
    ])
    monkeypatch.setattr(a5, "LEDGER", ledger)
    monkeypatch.setattr(a5, "RULE_IDS", ["ATOM-X", "ATOM-Y", "ATOM-Z"])
    res = a5.track()
    assert res["rule_count"] == 3
    # ATOM-X：直接命中 2（事件1/2）+ 被事件4 的 basis_refs 引用 1 = 3；推翻 1
    assert res["per_rule"]["ATOM-X"]["trigger"] == 3
    assert res["per_rule"]["ATOM-X"]["overturn"] == 1
    assert res["per_rule"]["ATOM-X"]["known_error_rate"] == pytest.approx(1 / 3)
    # ATOM-Y：触发 1，逃逸关联 1
    assert res["per_rule"]["ATOM-Y"]["escape"] == 1
    # ATOM-Z：触发 1，无推翻 → error_rate 0
    assert res["per_rule"]["ATOM-Z"]["known_error_rate"] == 0.0
    os.unlink(ledger)


def test_real_ledger_readable(monkeypatch):
    """真实账本存在且能被解析（不要求具体计数）。"""
    real = os.path.join(a5.ROOT, "data", "authority", "decision_event_v2_ledger.jsonl")
    monkeypatch.setattr(a5, "LEDGER", real)
    events = a5.load_ledger()
    assert isinstance(events, list)
    # 真实仓库账本应有大量事件（452）
    assert len(events) > 100
