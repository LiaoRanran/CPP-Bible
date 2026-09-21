"""621 A2 · 第一轮新 mutation 生成 + 判决预测 单测"""
from __future__ import annotations

import collections
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import mutation_generator_621 as G  # noqa: E402

ROUND1 = os.path.join(ROOT, "data", "mutation", "new_mutations_621_round1.jsonl")


def _load():
    if not os.path.exists(ROUND1):
        return None
    return [json.loads(ln) for ln in open(ROUND1, encoding="utf-8") if ln.strip()]


def test_round1_generated_50():
    items = _load()
    if items is None:
        return
    assert len(items) == 50
    assert len({x["mutation_id"] for x in items}) == 50


def test_round1_covers_all_three_strategies():
    items = _load()
    if items is None:
        return
    kinds = collections.Counter(x["attack_type"] for x in items)
    assert set(kinds) == set(G.STRATEGIES)
    assert all(v >= 10 for v in kinds.values())  # 每种策略都应有实质份额


def test_round1_format_valid():
    items = _load()
    if items is None:
        return
    assert all(G.validate_record(x) == [] for x in items)


def test_round1_reproducible():
    """用相同卡清单与固定时间戳重生成，应逐字节一致（除 generated_at）。"""
    items = _load()
    if items is None:
        return
    cards = [x["target_card"] for x in items]
    from datetime import datetime, timezone
    again = G.generate(cards, count=50, strategy="all",
                       now=datetime(2026, 9, 22, tzinfo=timezone.utc))
    assert [x["mutation_id"] for x in again] == [x["mutation_id"] for x in items]


def test_prediction_integration():
    v7 = G.load_v7()
    if not v7:
        return
    items = _load() or G.generate(["atoms/mem/ATOM-MEM-LEAK-001.md"], count=3)
    vb = G.verify_batch(items, v7)
    assert vb["total"] == len(items)
    assert set(vb["distribution"]) <= {"blocked", "escaped", "n_a", "infra_error"}
    assert all(r["basis"] and r["confidence"] for r in vb["rows"])


def test_prediction_is_deterministic():
    v7 = G.load_v7()
    items = _load() or G.generate(["evidence/conc/EV-CONC-001.md"], count=3)
    a = G.verify_batch(items, v7)
    b = G.verify_batch(items, v7)
    assert a == b


def test_predict_verdict_falls_back_to_strategy_prior():
    m = G.generate(["atoms/zzz/ATOM-ZZZ-001.md"], count=1, strategy="rule_blind_spot")[0]
    p = G.predict_verdict(m, [])  # 空 v7 ⇒ 只能走策略先验
    assert p["verdict"] == G.STRATEGY_PRIOR["rule_blind_spot"]
    assert p["confidence"] == "low"


def test_round1_written_to_whitelisted_dir():
    assert G.is_safe_path(ROUND1)


def test_selftest_passes():
    assert G.selftest() == 0
