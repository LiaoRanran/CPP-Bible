"""647 B4 · 校准追踪器真上岗回归锁（编号 B4-1..B4-8）。"""
from __future__ import annotations

import json
import os

import calibration_tracker_647 as C
import protector_mode_647 as M

SYNTH = {"ok20": {"rule_id": "ok20", "total": 100, "error": 20, "known_error_rate": 0.20},
         "warn21": {"rule_id": "warn21", "total": 100, "error": 21, "known_error_rate": 0.21},
         "sus51": {"rule_id": "sus51", "total": 100, "error": 51, "known_error_rate": 0.51}}


def test_b4_1_thresholds_and_boundaries():
    assert C.THETA_WARN == 0.20 and C.THETA_SUSPEND == 0.50
    assert C.effective_action("ok20", "block", SYNTH, enforce=True)["action"] == "ok"
    d = C.effective_action("warn21", "block", SYNTH, enforce=True)
    assert d["action"] == "degraded_warn" and d["effective_severity"] == "warn"
    assert d["enforced"] is True
    s = C.effective_action("sus51", "block", SYNTH, enforce=True)
    assert s["action"] == "suspended" and s["active"] is False and s["enforced"] is True


def test_b4_2_shadow_never_enforces():
    s = C.effective_action("sus51", "block", SYNTH, enforce=False)
    assert s["enforced"] is False and s["active"] is True
    assert s["effective_severity"] == "block"


def test_b4_3_classify_is_single_source():
    assert C.classify("r", None)[0] == "ok"
    assert C.classify("r", 0.20)[0] == "ok"
    assert C.classify("r", 0.2001)[0] == "degraded_warn"
    assert C.classify("r", 0.50)[0] == "degraded_warn"
    assert C.classify("r", 0.5001)[0] == "suspended"
    assert C.classify("r", 0.0, suspended=True)[0] == "suspended"


def test_b4_4_real_rates_are_per_rule():
    rates = C.rule_error_rates()
    assert len(rates) == 67, "逐规则样本（647 首次做到）"
    g = C.grader(rates)
    assert g["n"] == 67 and g["n_with_samples"] == 67
    assert all(0.0 <= r["known_error_rate"] <= 1.0 for r in rates.values())


def test_b4_5_restore_requires_human():
    try:
        C.restore("x", by="bot")
        assert False, "应抛 HumanReviewRequired"
    except C.HumanReviewRequired:
        pass
    try:
        C.restore("x", by="", human_authorized=True)
        assert False, "应抛 ValueError"
    except ValueError:
        pass


def test_b4_6_synthetic_two_thresholds():
    syn = C.synthetic_check()
    assert {s["got"] for s in syn} >= {"ok", "degraded_warn", "suspended"}
    assert all(s["ok"] for s in syn)


def test_b4_7_no_samples_means_no_change():
    g = C.grader({})
    assert g["by_action"] == {"ok": 67}
    assert all(x["has_samples"] is False for x in g["rows"])


def test_b4_8_report_and_selftest():
    assert C.selftest() == 0
    assert C.main(["--report"]) == 0
    doc = json.load(open(C.OUT_JSON, encoding="utf-8"))
    assert doc["grader"]["n"] == 67
    assert os.path.isfile(C.OUT_MD) and doc["mode"] in M.MODES
