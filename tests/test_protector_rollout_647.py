"""647 B5 · 五保护器真上岗联调回归锁（编号 BR-1..BR-8）。"""
from __future__ import annotations

import hashlib
import json
import os

import protector_mode_647 as M
import protector_rollout_647 as R


def test_br1_zero_drift_on_production(monkeypatch):
    monkeypatch.setenv(M.ENV, "enforce")
    r = R.rollout()
    assert r["zero_drift"] is True, r["drift"]
    assert set(r["effects"]) == set(R.PROTECTORS)


def test_br2_mark_namespaces_disjoint_and_layers_distinct():
    lc = R.layer_check()
    assert lc["keys_disjoint"] is True
    assert lc["layers_distinct"] is True
    assert lc["n_keys"] == sum(len(R.MARK_NAMESPACES[p]) for p in R.PROTECTORS)


def test_br3_marks_merge_and_conflict():
    m: dict = {}
    for p in R.PROTECTORS:
        m = R.merge_marks(m, {R.MARK_NAMESPACES[p][0]: p})
    assert len(m) == 5
    try:
        R.merge_marks({"conflict_flag": True}, {"conflict_flag": False})
        assert False, "应抛 MarkConflictError"
    except R.MarkConflictError:
        pass


def test_br4_rollback_marks_to_empty(monkeypatch):
    monkeypatch.setenv(M.ENV, "enforce")
    m = dict(R.collect_marks())
    for p in R.PROTECTORS:
        m = R.rollback_marks(m, p)
    assert m == {}


def test_br5_shadow_zero_enforcement(monkeypatch):
    monkeypatch.setenv(M.ENV, "shadow")
    e = R.enforce_effects()
    assert e["B1"]["判决态被改变（enforce 强制量）"] == 0
    assert e["B2"]["冻结不入队（enforce 强制量）"] == 0
    assert e["B3"]["强制盲化（enforce 强制量）"] == 0
    assert e["B4"]["降级（enforce 强制量）"] == 0 and e["B4"]["暂停（enforce 强制量）"] == 0
    assert e["B5"]["不放行（enforce 强制量）"] == 0


def test_br6_rollback_verified_and_no_side_effect(monkeypatch, tmp_path):
    monkeypatch.setenv(M.ENV, "enforce")
    f = tmp_path / "mode.json"
    monkeypatch.setattr(M, "MODE_FILE", str(f))
    rb = R.rollback_and_verify()
    assert rb["zero_enforcement"] is True and rb["new_mode"] == "shadow"
    assert rb["restored"] is True and not f.exists(), "--check/--report 不得留下模式文件"


def test_br7_protectors_touch_no_production_files(monkeypatch):
    monkeypatch.setenv(M.ENV, "enforce")
    targets = [os.path.join(R.ROOT, "data", "authority", "decision_event_v2_ledger.jsonl"),
               os.path.join(R.ROOT, "data", "transparency_log.jsonl"),
               R.b2.QUEUE]
    before = [hashlib.sha256(open(p, "rb").read()).hexdigest() for p in targets]
    R.rollout()
    assert [hashlib.sha256(open(p, "rb").read()).hexdigest() for p in targets] == before


def test_br8_report_and_selftest():
    assert R.selftest() == 0
    assert R.main(["--report"]) == 0
    doc = json.load(open(R.OUT_JSON, encoding="utf-8"))
    assert doc["enforce"]["zero_drift"] is True
    assert doc["rollback"]["zero_enforcement"] is True
    assert os.path.isfile(R.OUT_MD)
