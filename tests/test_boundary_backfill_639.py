"""639 D1 单测：边界三元组回填（≥5 例）。"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))

import boundary_backfill_639 as B  # noqa: E402


def test_verified_cards_is_23():
    assert len(B.verified_cards()) == 23


def test_all_cards_derived_with_real_triplet():
    r = B.run()
    assert r["dist"]["unverifiable"] == 0, "23 卡全部可由基线重算"
    for x in r["rows"]:
        t = x["triplet"]
        assert len(t["mutation_set_hash"]) == 64
        assert int(t["mutation_count"]) > 0
        assert t["generator_version"].startswith("full_baseline_v")


def test_triplet_reproducible():
    """同卡两次推导哈希一致（可复现，非随机）。"""
    r1 = B.run()
    r2 = B.run()
    m1 = {x["card"]: x["triplet"]["mutation_set_hash"] for x in r1["rows"]}
    m2 = {x["card"]: x["triplet"]["mutation_set_hash"] for x in r2["rows"]}
    assert m1 == m2


def test_count_consistent_with_baseline_by_card():
    """mutation_count 与基线 by_card 的 blocked+escaped+n_a 一致。"""
    import json
    r = B.run()
    stats = {}
    for f in os.listdir(os.path.join(B.ROOT, "data", "mutation")):
        if f.startswith("full_baseline_v") and f.endswith(".json"):
            d = json.load(open(os.path.join(B.ROOT, "data", "mutation", f),
                               encoding="utf-8"))
            for k, v in (d.get("by_card") or {}).items():
                stats[k.replace(os.sep, "/")] = v
    for x in r["rows"]:
        s = stats.get(x["card"])
        if s:
            assert int(x["triplet"]["mutation_count"]) == \
                s["blocked"] + s["escaped"] + s["n_a"]


def test_controlled_dirs_untouched():
    """工具输出只落 data/，不写受控目录。"""
    assert B.OUT_MD.startswith(os.path.join(B.ROOT, "data"))
    assert B.OUT_JSON.startswith(os.path.join(B.ROOT, "data"))


def test_four_state_rerun_present():
    r = B.run()
    assert "error" not in r["four_state_rerun"]
    assert r["four_state_rerun"]["n_cards"] == 23
