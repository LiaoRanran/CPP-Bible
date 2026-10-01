# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671g D5：LLM fuzz 三姿势框架（5 条）。"""
from __future__ import annotations

import llm_fuzz_671g as F


def test_posture1_oracle_labels():
    r = F.posture1_code_to_label("int x;", "asan",
                              runner=lambda c, s: {"oracle_hit": True, "rc": 1})
    assert r["label"] == "defect" and r["status"] == "labeled"
    r2 = F.posture1_code_to_label("int x;", "asan",
                               runner=lambda c, s: {"oracle_hit": False, "rc": 0})
    assert r2["label"] == "clean"


def test_posture1_bad_sanitizer_rejected():
    assert F.posture1_code_to_label("x", "magic", None)["status"] == "rejected"


def test_posture1_no_runner_no_label():
    r = F.posture1_code_to_label("x", "asan", None)
    assert r["status"] == "framework_only" and r["label"] is None


def test_posture2_kill_and_framework_only():
    case = {"mutant_code": "x", "mutation_op": "del"}
    assert F.posture2_mutant_kill(case, lambda c: "catch")["killed"] is True
    assert F.posture2_mutant_kill(case, lambda c: "miss")["killed"] is False
    assert F.posture2_mutant_kill(case, None)["status"] == "framework_only"
    assert F.posture2_mutant_kill({}, lambda c: "catch")["status"] == "rejected"


def test_posture3_human_truth_required():
    case = {"fake_citation": {"id": "EV-x"}}
    r = F.posture3_counterfactual(case, lambda c: "catch", None)
    assert r["status"] == "quarantined" and r["human_truth"] is None
    r2 = F.posture3_counterfactual(case, lambda c: "catch", "original_holds")
    assert r2["status"] == "labeled" and r2["agree"] is True
    assert F.posture3_counterfactual({}, lambda c: "x")[0] if False else \
        F.posture3_counterfactual({}, lambda c: "x", "x")["status"] == "rejected"


def test_batch_quarantine_count():
    items = [{"fake_citation": {}}, {"code": "x", "sanitizer": "asan"}, {"mutant_code": "x"}]
    rep = F.run_batch(3, items)
    assert rep["n"] == 3 and rep["quarantined"] >= 1 and rep["llm_attached"] is False
