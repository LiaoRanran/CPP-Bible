"""624 A4 闭环第五轮 · 单元测试（≥3 例）。"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import round5_mutator_624 as m  # noqa: E402

RUN = os.path.join(ROOT, "data", "adversarial_loop_round5_624.json")
RUN4 = os.path.join(ROOT, "data", "cross_card_sandbox_run_624.json")

NEW_RULES = {"ATOM-MISCONCEPTION-REF", "ATOM-VERIFIED-BOUND",
             "OBSERVATION-NEEDS-ARTIFACT", "S2-EVIDENCE-VERDICT"}


def _j(p):
    with open(p, encoding="utf-8") as fh:
        return json.load(fh)


def test_generate_40():
    muts = m.generate_round5(m.cc.load_inventory(), per_strategy=10)
    assert len(muts) == 40
    assert {x["strategy"] for x in muts} == {"X5", "X6", "X7", "X8"}


def test_round5_all_blocked_no_escape():
    d = _j(RUN)
    assert d["total"] == 40
    assert d["distribution"].get("blocked") == 40
    assert d["escaped"] == []


def test_round5_new_rules_and_cumulative():
    d = _j(RUN)
    assert NEW_RULES <= set(d["touched_all"])
    assert set(d["touched_all"]) - NEW_RULES == {"ATOM-FM-REQUIRED"}
    # 六轮累计 = 623(26) ∪ A2 ∪ R5
    t623 = {
        "ATOM-FM-REQUIRED", "ATOM-ID-FORMAT", "ATOM-ID-UNIQUE", "ATOM-NO-UNVERIFIED",
        "ATOM-STATUS-VALUE", "ATOM-DAL-MATCH", "ATOM-REL-DAG", "ATOM-GRAY-ZONE",
        "ATOM-AUDIENCE", "ATOM-PREREQ-READABLE", "EV-FM-REQUIRED", "EV-ID-UNIQUE",
        "EV-MATRIX", "EV-ARTIFACT-VERSION-MATCH", "EV-ASSERT-COUNT-BELOW-BASELINE",
        "EV-ASSERT-SYMBOL-MAPPED", "EV-ARTIFACT-PRODUCER", "EV-MSCV-NO-VERIFY",
        "EV-FM-DUP-KEY", "EV-FM-YAML-HARDENING", "ATOM-CLAIM-STRUCTURED",
        "ATOM-REL-TARGET", "EV-SERVES-EXIST", "ATOM-VERIFY-REASON",
        "ATOM-REL-UNKNOWN", "CARD-PATH-NOT-CANONICAL"}
    cum = t623 | set(_j(RUN4)["touched_all"]) | set(d["touched_all"])
    assert len(cum) == 32
    assert len(cum) < 45  # 诚实登记：未达 >45 目标


def test_round5_report_exists():
    p = os.path.join(ROOT, "data", "adversarial_loop_round5_624.md")
    assert os.path.exists(p) and os.path.getsize(p) > 500
