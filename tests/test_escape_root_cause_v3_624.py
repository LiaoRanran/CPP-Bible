"""624 A3 逃逸根因分析 v3 · 单元测试（≥6 例）。"""
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))
import escape_root_cause_v3_624 as m  # noqa: E402


def test_four_dims():
    assert len(m.CROSS_CARD_DIMS) == 4


def test_classify_dangling():
    c = m.classify_escape(["ATOM-REL-TARGET", "EV-SERVES-EXIST"])
    assert "悬空引用绕过" in c["dims"]
    assert all(f["kind"] in ("规则修复", "证据修复", "卡面修复", "架构修复") for f in c["fixes"])


def test_classify_conflict():
    c = m.classify_escape(["ATOM-REL-CONFLICT"])
    assert c["dims"] == ["矛盾引用绕过"]


def test_classify_cycle():
    c = m.classify_escape(["ATOM-REL-DAG"])
    assert "循环引用绕过" in c["dims"]


def test_analyze_zero_escapes():
    fake = {"touched_all": ["ATOM-REL-CONFLICT", "EV-ARTIFACT-FILE-EXISTS"],
            "escaped": [], "total": 60,
            "distribution": {"blocked": 47, "detected_nonblock": 13}}
    a = m.analyze(fake)
    assert a["escaped_count"] == 0
    assert set(a["zero_analysis"]) == {"q1_策略覆盖度", "q2_规则覆盖度", "q3_沙箱限制", "q4_复杂度校准"}


def test_new_and_cumulative():
    fake = {"touched_all": ["ATOM-REL-CONFLICT", "EV-ARTIFACT-FILE-EXISTS", "ATOM-REL-TARGET"],
            "escaped": [], "total": 60, "distribution": {}}
    a = m.analyze(fake)
    assert a["new"] == ["ATOM-REL-CONFLICT", "EV-ARTIFACT-FILE-EXISTS"]
    assert a["cumulative"] == len(m.TOUCHED_623) + 2


def test_next_strategies_x5_to_x8():
    a = m.analyze({"touched_all": [], "escaped": [], "total": 0, "distribution": {}})
    assert [s["id"] for s in a["next_strategies"]] == ["X5", "X6", "X7", "X8"]
    assert {s["target_rule"] for s in a["next_strategies"]} == {
        "S2-EVIDENCE-VERDICT", "OBSERVATION-NEEDS-ARTIFACT",
        "ATOM-MISCONCEPTION-REF", "ATOM-VERIFIED-BOUND"}


def test_analyze_real_a2():
    p = os.path.join(ROOT, "data", "cross_card_sandbox_run_624.json")
    a = m.analyze(json.load(open(p, encoding="utf-8")))
    assert a["escaped_count"] == 0
    assert a["cumulative"] == 28
