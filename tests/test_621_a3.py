"""621 A3 · 新 mutation 质量评估 + 去重 单测"""
from __future__ import annotations

import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import mutation_generator_621 as MG  # noqa: E402
import mutation_quality_621 as Q  # noqa: E402

CARDS = ["atoms/mem/ATOM-MEM-LEAK-001.md", "evidence/conc/EV-CONC-001.md"]
V7 = [{"card": CARDS[0], "op": "M1", "point": "删 artifact_sha256", "verdict": "blocked"},
      {"card": CARDS[0], "op": "M6", "point": "块式→flow", "verdict": "blocked"}]


def _muts():
    return MG.generate(CARDS, count=6, strategy="all")


def test_four_dimensions_present():
    res = Q.evaluate(_muts(), V7)
    for s in res["scored"]:
        assert {"novelty", "attack_strength", "semantic_validity", "reproducibility"} <= set(s)


def test_dedup_removes_duplicates():
    muts = _muts()
    kept, dropped = Q.dedup(muts + muts[:2])
    assert dropped == 2
    assert len(kept) == len(muts)


def test_dedup_key_composition():
    m = _muts()[0]
    k = Q.dedup_key(m)
    assert m["target_rule"] in k and m["target_card"] in k


def test_attack_strength_mapping():
    assert Q.attack_strength("escaped")[0] == 1.0
    assert Q.attack_strength("n_a")[0] == 0.5
    assert Q.attack_strength("blocked")[0] == 0.0


def test_semantic_validity_rejects_bad():
    m = _muts()[0]
    assert Q.semantic_validity(m)[0] == 1.0
    bad = dict(m)
    bad["content"] = "not-json"
    assert Q.semantic_validity(bad)[0] == 0.0


def test_reproducibility_self_check():
    for m in _muts():
        assert Q.reproducibility(m)[0] == 1.0
    bad = dict(_muts()[0])
    bad["mutation_id"] = "MUT-621-bogusbogus"
    assert Q.reproducibility(bad)[0] == 0.0


def test_novelty_levels():
    m = _muts()[0]
    c = json.loads(m["content"])
    idx = Q._v7_index(V7)
    # 与 v7 完全重合的（卡,算子,变异点）→ 0.0
    exact = {**m, "content": json.dumps({**c, "card": CARDS[0], "target_card": CARDS[0],
                                         "op": "M1", "point": "删 artifact_sha256"},
                                        ensure_ascii=False, sort_keys=True)}
    assert Q.novelty(exact, idx)[0] == 0.0
    # 卡不在 v7 → 1.0
    far = {**m, "content": json.dumps({**c, "target_card": "atoms/zzz/ATOM-ZZZ-001.md"},
                                      ensure_ascii=False, sort_keys=True)}
    assert Q.novelty(far, idx)[0] == 1.0


def test_empty_input():
    res = Q.evaluate([], V7)
    assert res["kept"] == 0 and res["scored"] == []


def test_top_n_respected():
    res = Q.evaluate(_muts(), V7, top_n=3)
    assert len(res["top"]) <= 3


def test_report_renders():
    res = Q.evaluate(_muts(), V7)
    assert "质量评估" in Q.render_report(res)


def test_round1_artifact_evaluable():
    p = os.path.join(ROOT, "data", "mutation", "new_mutations_621_round1.jsonl")
    if not os.path.exists(p):
        return
    muts = [json.loads(ln) for ln in open(p, encoding="utf-8") if ln.strip()]
    res = Q.evaluate(muts, MG.load_v7(), top_n=10)
    assert res["kept"] == len(muts)
    assert len(res["top"]) == 10


def test_selftest_passes():
    assert Q.selftest() == 0
