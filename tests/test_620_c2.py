"""620 C2 · Authority 日志（append-only + 哈希链）单测"""
from __future__ import annotations

import os
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import authority_log_620 as AL  # noqa: E402


def _log(td):
    return os.path.join(td, "authority_log.jsonl")


def _dec(power="ACCEPT", tid="ATOM-CONC-FENCE-001", reviewer="human:LiaoRanran",
         reason="逐条核对", **kw):
    d = {"target": {"type": "certificate", "id": tid}, "power": power,
         "reviewer": reviewer, "reason": reason}
    d.update(kw)
    return d


def test_append_and_query():
    with tempfile.TemporaryDirectory() as td:
        log = _log(td)
        e = AL.append(log, _dec())
        assert e["decision_id"] == "dec-000001"
        assert e["prev_hash"] == AL.GENESIS
        assert len(AL.query(log, target_id="ATOM-CONC-FENCE-001")) == 1
        assert len(AL.query(log, power="ACCEPT")) == 1


def test_append_only_no_delete():
    with tempfile.TemporaryDirectory() as td:
        log = _log(td)
        e1 = AL.append(log, _dec())
        AL.append(log, _dec(power="OVERRIDE", reason="推翻", overrides=e1["decision_id"]))
        assert len(AL.list_all(log)) == 2  # 撤销是追加，不是删除


def test_hash_chain_verifies():
    with tempfile.TemporaryDirectory() as td:
        log = _log(td)
        for i in range(3):
            AL.append(log, _dec(reason=f"r{i}"))
        ok, errs = AL.verify(log)
        assert ok and errs == []


def test_tamper_detected():
    with tempfile.TemporaryDirectory() as td:
        log = _log(td)
        AL.append(log, _dec())
        entries = AL.load_entries(log)
        entries[0]["reason"] = "被偷偷改了"
        with open(log, "w", encoding="utf-8") as fh:
            for e in entries:
                fh.write(AL._canonical(e) + "\n")
        ok, errs = AL.verify(log)
        assert not ok
        assert any("self_hash" in x for x in errs)


def test_prev_hash_break_detected():
    with tempfile.TemporaryDirectory() as td:
        log = _log(td)
        AL.append(log, _dec())
        entries = AL.load_entries(log)
        entries[0]["prev_hash"] = "f" * 64
        with open(log, "w", encoding="utf-8") as fh:
            for e in entries:
                fh.write(AL._canonical(e) + "\n")
        ok, errs = AL.verify(log)
        assert not ok


def test_invalid_decisions_rejected():
    cases = [
        _dec(reviewer="human:"),                      # 空名签收
        _dec(power="BOGUS"),                          # 非法 power
        _dec(reason=""),                              # 空 reason
        _dec(power="OVERRIDE"),                       # OVERRIDE 缺 overrides
    ]
    for c in cases:
        try:
            with tempfile.TemporaryDirectory() as td:
                AL.append(_log(td), c)
            raise AssertionError(f"应被拒绝却通过：{c}")
        except ValueError:
            pass


def test_empty_log():
    with tempfile.TemporaryDirectory() as td:
        log = _log(td)
        assert AL.list_all(log) == []
        assert AL.verify(log)[0] is True


def test_import_history_is_readonly_and_chained():
    if not os.path.exists(AL.DEFAULT_HISTORY):
        return
    with tempfile.TemporaryDirectory() as td:
        log = _log(td)
        n = AL.import_history(log)
        assert n > 0
        ok, errs = AL.verify(log)
        assert ok, errs[:3]
        assert len(AL.load_entries(log)) == n


def test_import_history_does_not_modify_source():
    if not os.path.exists(AL.DEFAULT_HISTORY):
        return
    before = open(AL.DEFAULT_HISTORY, encoding="utf-8").read()
    with tempfile.TemporaryDirectory() as td:
        AL.import_history(_log(td))
    after = open(AL.DEFAULT_HISTORY, encoding="utf-8").read()
    assert before == after


def test_selftest_passes():
    assert AL.selftest() == 0
