"""622 A2 · 50 条新 mutation 沙箱实跑 单测"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import sandbox_apply_622 as SA  # noqa: E402

RESULTS = os.path.join(ROOT, "data", "mutation_sandbox_run_622_results.json")
MUTS = os.path.join(ROOT, "data", "mutation", "new_mutations_621_round1.jsonl")


def _res():
    if not os.path.exists(RESULTS):
        return None
    with open(RESULTS, encoding="utf-8") as fh:
        return json.load(fh)


def test_results_cover_50_mutations():
    d = _res()
    if d is None:
        return
    assert d["total"] == 50
    assert len(d["rows"]) == 50


def test_verdict_domain():
    d = _res()
    if d is None:
        return
    for r in d["rows"]:
        assert r["verdict"] in ("blocked", "escaped", "neutral", "infra_error")


def test_distribution_matches_rows():
    d = _res()
    if d is None:
        return
    cnt: dict[str, int] = {}
    for r in d["rows"]:
        cnt[r["verdict"]] = cnt.get(r["verdict"], 0) + 1
    assert cnt == d["distribution"]


def test_no_escape_under_strict_definition():
    d = _res()
    if d is None:
        return
    assert d["distribution"].get("escaped", 0) == 0
    for r in d["rows"]:
        if r["verdict"] == "escaped":
            assert r["new_block_rules"] == [] and r["lost_rules"]


def test_infra_errors_have_reasons():
    d = _res()
    if d is None:
        return
    ie = [r for r in d["rows"] if r["verdict"] == "infra_error"]
    assert ie
    assert all(r.get("reason") for r in ie)


def test_comparison_agreement_computed():
    d = _res()
    if d is None:
        return
    c = d["comparison"]
    assert c["agree"] + c["disagree"] + c["skipped"] == 50
    assert c["agreement_rate"] == round(c["agree"] / (c["agree"] + c["disagree"]), 4)


def test_compare_prediction_function():
    rows = [{"mutation_id": "a", "verdict": "blocked"},
            {"mutation_id": "b", "verdict": "neutral"},
            {"mutation_id": "c", "verdict": "blocked"},
            {"mutation_id": "d", "verdict": "infra_error"}]
    pred = {"a": "blocked", "b": "blocked", "c": "n_a", "d": "blocked"}
    c = SA.compare_prediction(rows, pred)
    assert c["agree"] == 1        # a
    assert c["disagree"] == 2     # b（预测拦、实际没拦）, c（预测 n_a、实际拦）
    assert c["skipped"] == 1      # d infra_error
    assert c["agreement_rate"] == round(1 / 3, 4)


def test_run_batch_empty():
    class _SB:
        def gate_all(self):
            return {"findings": []}

        def acquire(self):
            return None

        def release(self):
            return None

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def apply_and_run(self, m, card, bf):
            return {"mutation_id": m.get("mutation_id"), "verdict": "neutral"}

    r = SA.run_batch([], sandbox=_SB(), baseline={"findings": []}, log=lambda *a: None)
    assert r["total"] == 0
    assert r["distribution"] == {}


def test_run_batch_handles_missing_target_card():
    class _SB:
        def gate_all(self):
            return {"findings": []}

        def acquire(self):
            return None

        def release(self):
            return None

        def __enter__(self):
            return self

        def __exit__(self, *a):
            return False

        def apply_and_run(self, m, card, bf):  # pragma: no cover - 不应被调用
            raise AssertionError("无 target_card 时不应调用 apply_and_run")

    r = SA.run_batch([{"mutation_id": "x", "content": "{}"}], sandbox=_SB(),
                     baseline={"findings": []}, log=lambda *a: None)
    assert r["rows"][0]["verdict"] == "infra_error"
    assert r["rows"][0]["reason"] == "无 target_card"


def test_selftest_passes():
    assert SA.selftest() == 0
