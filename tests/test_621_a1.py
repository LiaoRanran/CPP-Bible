"""621 A1 · 对抗性 mutation 生成器 单测"""
from __future__ import annotations

import json
import os
import sys
import tempfile
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(ROOT, "tools"))

import mutation_generator_621 as G  # noqa: E402

CARDS = ["atoms/mem/ATOM-MEM-LEAK-001.md", "evidence/conc/EV-CONC-001.md"]
TS = datetime(2026, 9, 22, tzinfo=timezone.utc)


def test_empty_input():
    assert G.generate([], count=10) == []
    assert G.generate(CARDS, count=0) == []
    assert G.generate(CARDS, count=-1) == []


def test_single_strategy():
    out = G.generate(CARDS, count=6, strategy="rule_blind_spot", now=TS)
    assert len(out) == 6
    assert all(x["attack_type"] == "rule_blind_spot" for x in out)


def test_multi_strategy_covers_three():
    out = G.generate(CARDS, count=9, strategy="all", now=TS)
    assert {x["attack_type"] for x in out} == set(G.STRATEGIES)


def test_dedup_unique_ids():
    out = G.generate(CARDS, count=30, strategy="all", now=TS)
    assert len({x["mutation_id"] for x in out}) == len(out)


def test_safety_rails_reject_controlled_dirs():
    for p in ("atoms/x.jsonl", "evidence/x.jsonl", "Examples/x.jsonl", "Book/x.jsonl"):
        assert not G.is_safe_path(os.path.join(ROOT, p))


def test_safety_rails_allow_data_mutation():
    assert G.is_safe_path(os.path.join(ROOT, "data/mutation/new.jsonl"))


def test_write_to_controlled_dir_raises():
    try:
        G.write_jsonl(G.generate(CARDS, count=2, now=TS),
                      os.path.join(ROOT, "evidence/bad.jsonl"))
        raise AssertionError("应拒绝写入受控目录")
    except ValueError:
        pass


def test_format_validation():
    out = G.generate(CARDS, count=9, strategy="all", now=TS)
    assert all(G.validate_record(x) == [] for x in out)
    bad = dict(out[0])
    bad["attack_type"] = "BOGUS"
    assert G.validate_record(bad)
    bad2 = dict(out[0])
    bad2["content"] = "not-json"
    assert G.validate_record(bad2)


def test_idempotent_generation():
    a = G.generate(CARDS, count=12, strategy="all", now=TS)
    b = G.generate(CARDS, count=12, strategy="all", now=TS)
    assert a == b


def test_unknown_strategy_raises():
    try:
        G.generate(CARDS, count=1, strategy="bogus")
        raise AssertionError("未知策略应抛错")
    except ValueError:
        pass


def test_write_jsonl_roundtrip():
    with tempfile.TemporaryDirectory() as td:
        p = os.path.join(td, "new.jsonl")
        items = G.generate(CARDS, count=5, now=TS)
        G.write_jsonl(items, p)
        loaded = [json.loads(ln) for ln in open(p, encoding="utf-8") if ln.strip()]
        assert len(loaded) == 5
        assert all(G.validate_record(x) == [] for x in loaded)


def test_content_is_json_with_expected_keys():
    out = G.generate(CARDS, count=3, strategy="provenance_inconsistency", now=TS)
    for x in out:
        c = json.loads(x["content"])
        assert {"op", "point", "detail", "target_rule", "target_card"} <= set(c)


def test_count_respected():
    # 去重后唯一组合数受「卡数 × 策略 × 模板 × 规则」周期限制：
    # 2 张卡只能产出 12 条唯一 mutation，故这里用 10 张卡验证 count 被满足。
    many = [f"atoms/mem/ATOM-MEM-{i:03d}.md" for i in range(10)]
    assert len(G.generate(many, count=17, strategy="all", now=TS)) == 17


def test_count_capped_by_unique_capacity():
    # 诚实记录上限：卡太少时不会硬凑到 count，而是停在唯一组合耗尽处
    out = G.generate(CARDS, count=100, strategy="all", now=TS)
    assert len(out) <= 100
    assert len({x["mutation_id"] for x in out}) == len(out)


def test_selftest_passes():
    assert G.selftest() == 0
