"""622 A3 · 新逃逸根因分析 单测"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import escape_root_cause_622 as E  # noqa: E402

ROWS = [
    {"mutation_id": "a", "card": "atoms/x.md", "verdict": "blocked",
     "new_block_rules": ["ATOM-FM-REQUIRED"], "lost_rules": []},
    {"mutation_id": "b", "card": "evidence/y.md", "verdict": "neutral",
     "new_block_rules": [], "lost_rules": []},
    {"mutation_id": "c", "card": "evidence/y.md", "verdict": "infra_error",
     "reason": "无法施加 op=M7"},
]
BY_ID = {
    "a": {"mutation_id": "a", "attack_type": "rule_blind_spot",
          "content": json.dumps({"op": "M1", "target_card": "atoms/x.md"})},
    "b": {"mutation_id": "b", "attack_type": "evidence_ambiguity",
          "content": json.dumps({"op": "M4", "target_card": "evidence/y.md"})},
    "c": {"mutation_id": "c", "attack_type": "evidence_ambiguity",
          "content": json.dumps({"op": "M7", "target_card": "evidence/y.md"})},
}
V7 = [{"card": "atoms/x.md", "op": "M1"}, {"card": "zzz", "op": "M2"}]


def test_strategy_coverage_counts():
    cov = E.strategy_coverage(ROWS, BY_ID)
    assert cov["rule_blind_spot"]["n"] == 1
    assert cov["rule_blind_spot"]["blocked"] == 1
    assert cov["evidence_ambiguity"]["n"] == 2
    assert cov["evidence_ambiguity"]["applicable"] == 1
    assert cov["evidence_ambiguity"]["applicable_rate"] == 0.5


def test_strategy_block_rate_uses_applicable():
    cov = E.strategy_coverage(ROWS, BY_ID)
    assert cov["rule_blind_spot"]["block_rate"] == 1.0
    assert cov["evidence_ambiguity"]["block_rate"] == 0.0


def test_v7_overlap():
    ov = E.v7_overlap([BY_ID["a"], BY_ID["b"]], V7)
    assert ov["total"] == 2
    assert ov["card_op_overlap"] == 1
    assert ov["card_overlap"] == 1
    assert ov["card_op_overlap_rate"] == 0.5


def test_rule_coverage():
    rc = E.rule_coverage(ROWS)
    assert rc["ATOM-FM-REQUIRED"] == 1


def test_root_cause_rule_blind_spot():
    rc = E.root_cause({"mutation_id": "x", "card": "atoms/z.md",
                       "lost_rules": [], "new_block_rules": []},
                      {"x": {"content": json.dumps({"op": "M8"})}})
    assert any("规则盲区" in d for d in rc["dimensions"])


def test_root_cause_evidence_ambiguity():
    rc = E.root_cause({"mutation_id": "y", "card": "evidence/z.md",
                       "lost_rules": ["EV-ARTIFACT-PRODUCER"], "new_block_rules": []},
                      {"y": {"content": json.dumps({"op": "M4"})}})
    assert any("证据歧义" in d for d in rc["dimensions"])
    assert any("provenance" in d for d in rc["dimensions"])


def test_suggestions_nonempty_and_actionable():
    cov = E.strategy_coverage(ROWS, BY_ID)
    sug = E.suggestions(cov, E.v7_overlap([BY_ID["a"], BY_ID["b"]], V7),
                        E.rule_coverage(ROWS), {"neutral": 1})
    assert len(sug) >= 3
    assert any("schema-aware" in s for s in sug)
    # 「新颖性」建议仅在 (卡,op) 重叠率 > 80% 时给出；此样例 0.5 ⇒ 不应出现
    assert not any("新颖性" in s for s in sug)
    # 高重叠时应出现
    sug2 = E.suggestions(cov, {"total": 10, "card_op_overlap": 10,
                               "card_op_overlap_rate": 1.0},
                         E.rule_coverage(ROWS), {"neutral": 1})
    assert any("新颖性" in s for s in sug2)


def test_render_zero_and_escape_branches():
    cov = E.strategy_coverage(ROWS, BY_ID)
    zero = E.render({"mode": "zero", "distribution": {"blocked": 1},
                     "strategy_coverage": cov, "v7_overlap": E.v7_overlap([], V7),
                     "rule_coverage": {}, "suggestions": ["x"]})
    assert "0 逃逸深度分析" in zero
    esc = E.render({"mode": "escapes", "escapes": [{"mutation_id": "q"}],
                    "root_causes": [{"mutation_id": "q", "card": "c", "op": "M1",
                                     "lost_rules": ["R"], "dimensions": ["d"]}]})
    assert "根因分析" in esc


def test_analyze_real_results_is_zero_mode():
    if not os.path.exists(E.RESULTS):
        return
    res = E.analyze()
    assert res["mode"] == "zero"
    assert res["distribution"]["escaped"] if "escaped" in res["distribution"] else True
    assert res["v7_overlap"]["card_op_overlap_rate"] == 1.0


def test_selftest_passes():
    assert E.selftest() == 0
