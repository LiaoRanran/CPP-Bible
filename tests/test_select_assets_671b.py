#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""test_select_assets_671b.py — 671b B 段：真 B3 资产选择接口测试。

覆盖：
  * `tools/select_assets_671b.py` —— `select_assets(pool, n, strategy, seed)` 三种策略 + 预算对齐
  * `tools/run_b3_671b.py`        —— B3 run plan（**不跑实验**）+ 与 670a 代理臂的一致性
  * `data/experiments/b3_design_671b.json` —— 设计文档与实现一致

红线：本批只写脚本和设计，不跑实验 ⇒ 测试断言"plan 无伪造结果数字"。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import run_b3_671b as B3          # noqa: E402
import select_assets_671b as SA   # noqa: E402

DESIGN = ROOT / "data" / "experiments" / "b3_design_671b.json"
BASELINE_RANDOM = ROOT / "data" / "experiments" / "baseline_random.json"


# ═════════════════════════════════════════════════════════════════════════════
# 1) select_assets 接口
# ═════════════════════════════════════════════════════════════════════════════
class TestSelectAssets:
    POOL = list(SA.INSTRUMENT_POOL)

    def test_random_reproducible_same_seed(self):
        a = SA.select_assets(self.POOL, 4, "random", 20260930)
        b = SA.select_assets(self.POOL, 4, "random", 20260930)
        assert a == b

    def test_random_differs_across_seeds(self):
        a = SA.select_assets(self.POOL, 4, "random", 1)
        c = SA.select_assets(self.POOL, 4, "random", 2)
        assert a != c

    def test_random_length_and_uniqueness(self):
        r = SA.select_assets(self.POOL, 5, "random", 7)
        assert len(r) == 5
        assert len(set(r)) == 5

    def test_zero_returns_empty(self):
        assert SA.select_assets(self.POOL, 0, "random") == []

    def test_full_pool_selection(self):
        assert len(SA.select_assets(self.POOL, 10, "random", 1)) == 10

    def test_n_exceeds_pool_raises(self):
        with pytest.raises(ValueError):
            SA.select_assets(self.POOL, 11, "random")

    def test_negative_n_raises(self):
        with pytest.raises(ValueError):
            SA.select_assets(self.POOL, -1, "random")

    def test_unknown_strategy_raises(self):
        with pytest.raises(ValueError):
            SA.select_assets(self.POOL, 2, "greedy")

    def test_failure_driven_descending(self):
        pool = [{"id": x, "fail_hits": v} for x, v in
                [("a", 1), ("b", 9), ("c", 5), ("d", 7)]]
        assert [x["id"] for x in SA.select_assets(pool, 2, "failure_driven")] == ["b", "d"]

    def test_failure_driven_deterministic_ties(self):
        pool = [{"id": x, "fail_hits": 5} for x in ("c", "a", "b")]
        got = [x["id"] for x in SA.select_assets(pool, 3, "failure_driven")]
        assert got == ["a", "b", "c"]      # 同分按 id 升序 ⇒ 确定性

    def test_oracle_descending(self):
        pool = [{"id": x, "true_catch": v} for x, v in
                [("a", 1), ("b", 9), ("c", 5), ("d", 7)]]
        assert [x["id"] for x in SA.select_assets(pool, 2, "oracle")] == ["b", "d"]

    def test_failure_driven_missing_field_raises(self):
        with pytest.raises(ValueError):
            SA.select_assets([{"id": "x"}], 1, "failure_driven")

    def test_oracle_missing_field_raises(self):
        with pytest.raises(ValueError):
            SA.select_assets([{"id": "x"}], 1, "oracle")

    def test_accepts_dict_assets_and_returns_them(self):
        pool = [{"id": "a", "fail_hits": 1}, {"id": "b", "fail_hits": 2}]
        got = SA.select_assets(pool, 1, "failure_driven")
        assert got[0]["id"] == "b"

    def test_strategies_constant(self):
        assert SA.STRATEGIES == ("failure_driven", "random", "oracle")

    def test_selftest_passes(self):
        assert SA.selftest() == 0


# ═════════════════════════════════════════════════════════════════════════════
# 2) 预算对齐
# ═════════════════════════════════════════════════════════════════════════════
class TestBudgetAlignment:
    SAMPLES = [{"id": "s1", "detector": "asan"}, {"id": "s2", "detector": "ubsan"},
               {"id": "s3", "detector": "linker"}, {"id": "s4", "detector": "perf-counter"}]
    VERD = {"s1": "catch", "s2": "catch", "s3": "miss", "s4": "unknown"}

    def test_budget_uses_only_catch_and_in_pool(self):
        got = SA.budget("failure_driven", self.SAMPLES, self.VERD)
        assert got == ["asan", "ubsan"]

    def test_budget_excludes_out_of_pool(self):
        s = [{"id": "x", "detector": "not-a-detector"}]
        assert SA.budget("failure_driven", s, {"x": "catch"}) == []

    def test_select_for_arm_fd_matches_budget(self):
        r = SA.select_for_arm("failure_driven", list(SA.INSTRUMENT_POOL), self.SAMPLES, self.VERD)
        assert r["picked"] == ["asan", "ubsan"]
        assert r["seed"] is None

    def test_select_for_arm_random_same_count(self):
        fd = SA.select_for_arm("failure_driven", list(SA.INSTRUMENT_POOL), self.SAMPLES, self.VERD)
        rn = SA.select_for_arm("random", list(SA.INSTRUMENT_POOL), self.SAMPLES, self.VERD, seed=1)
        assert rn["n_assets"] == fd["n_assets"] == 2

    def test_select_for_arm_random_reproducible(self):
        a = SA.select_for_arm("random", list(SA.INSTRUMENT_POOL), self.SAMPLES, self.VERD, seed=5)
        b = SA.select_for_arm("random", list(SA.INSTRUMENT_POOL), self.SAMPLES, self.VERD, seed=5)
        assert a["picked"] == b["picked"]
        assert a["seed"] == 5

    def test_allocation_table_has_rank(self):
        rn = SA.select_for_arm("random", list(SA.INSTRUMENT_POOL), self.SAMPLES, self.VERD, seed=1)
        assert [r["rank"] for r in rn["allocation_table"]] == [1, 2]

    def test_unknown_arm_raises(self):
        with pytest.raises(ValueError):
            SA.select_for_arm("oracle", list(SA.INSTRUMENT_POOL), self.SAMPLES, self.VERD)


# ═════════════════════════════════════════════════════════════════════════════
# 3) 与 670a 代理臂的一致性（同 seed 同集合）
# ═════════════════════════════════════════════════════════════════════════════
class TestProxyConsistency:
    @pytest.mark.skipif(not BASELINE_RANDOM.is_file(), reason="670a baseline_random 未跑")
    def test_shim_matches_670a_same_set(self):
        ref = json.loads(BASELINE_RANDOM.read_text(encoding="utf-8"))
        picked = ref["selection"]["holdout"]["picked"]
        got = list(SA.select_assets(list(SA.INSTRUMENT_POOL), len(picked), "random", SA.DEFAULT_SEED))
        assert set(got) == set(picked)

    def test_proxy_consistency_reports_ok(self):
        r = B3.proxy_consistency()
        assert r["ok"] is True
        assert r["same_set"] is True
        assert r["seed"] == 20260930

    def test_default_seed_is_20260930(self):
        assert SA.DEFAULT_SEED == 20260930


# ═════════════════════════════════════════════════════════════════════════════
# 4) B3 run plan（不跑实验）
# ═════════════════════════════════════════════════════════════════════════════
class TestB3Plan:
    def test_not_executed(self):
        assert B3.build_plan()["executed"] is False

    def test_two_arms(self):
        assert set(B3.build_plan()["arms"]) == {"FD", "B3_random"}

    def test_results_are_placeholders(self):
        p = B3.build_plan()
        for arm in p["arms"].values():
            for k, v in arm.items():
                if k.startswith("detect_rate"):
                    assert str(v).startswith("{{TODO_")
        assert p["comparison"]["delta_placeholder"].startswith("{{TODO_")
        assert p["comparison"]["cohens_h_placeholder"].startswith("{{TODO_")

    def test_no_fabricated_result_keys(self):
        p = B3.build_plan()
        bad = {"catch", "miss", "k", "n", "p_value", "result"}
        for arm in p["arms"].values():
            assert not (bad & set(arm))

    def test_allocation_table_present_with_seed(self):
        b3 = B3.build_plan()["arms"]["B3_random"]
        assert b3["seed"] == 20260930
        assert len(b3["allocation_table"]) == len(b3["picked"]) == 4
        assert all("rank" in r for r in b3["allocation_table"])

    def test_budget_alignment_required(self):
        ba = B3.build_plan()["budget_alignment"]
        assert ba["required"] is True
        assert "资产数" in ba["matched_dims"]

    def test_comparison_uses_mcnemar_and_cohens_h(self):
        c = B3.build_plan()["comparison"]
        assert "McNemar" in c["test"]
        assert "Cohen" in c["effect_size"]
        assert c["design"] == "paired"

    def test_decision_rule_mentions_ci_crossing_zero(self):
        assert "跨 0" in B3.build_plan()["comparison"]["decision_rule"]

    def test_true_b3_blocked(self):
        bl = B3.build_plan()["blocked"]
        assert any(b["status"] == "BLOCKED" and "真 B3" in b["item"] for b in bl)

    def test_related_a5_blocked(self):
        assert B3.build_plan()["related_ablation"]["A5_status"] == "BLOCKED"

    def test_sample_size_reality_current_n(self):
        r = B3.build_plan()["sample_size_reality"]
        assert r["current_holdout"] == 16
        assert r["current_corpus"] == 32

    def test_red_lines_recorded(self):
        rl = B3.build_plan()["red_lines"]
        assert any("不跑实验" in x for x in rl)
        assert any("代理" in x for x in rl)

    def test_selftest_passes(self):
        assert B3.selftest() == 0

    def test_plan_artifact_roundtrip(self, tmp_path, monkeypatch):
        monkeypatch.setattr(B3, "OUT", tmp_path / "b3.json")
        assert B3.main(["--run"]) == 0
        doc = json.loads((tmp_path / "b3.json").read_text(encoding="utf-8"))
        assert doc["schema"] == "queyi-b3-plan/671b"
        assert doc["executed"] is False


# ═════════════════════════════════════════════════════════════════════════════
# 5) 设计文档与实现一致
# ═════════════════════════════════════════════════════════════════════════════
class TestB3DesignDoc:
    @pytest.fixture(scope="class")
    @staticmethod
    def doc():
        if not DESIGN.is_file():
            pytest.skip("b3_design_671b.json 不存在")
        return json.loads(DESIGN.read_text(encoding="utf-8"))

    def test_schema_and_not_executed(self, doc):
        assert doc["schema"] == "queyi-b3-design/671b"
        assert doc["executed"] is False

    def test_interface_signature(self, doc):
        assert doc["interface"]["signature"] == "select_assets(pool, n, strategy, seed) -> [asset]"

    def test_three_strategies_documented(self, doc):
        assert set(doc["interface"]["strategies"]) == set(SA.STRATEGIES)

    def test_shim_declared_as_proxy(self, doc):
        shim = doc["interface"]["implementations"]["main_repo_shim"]
        assert shim["status"].startswith("PROXY")
        assert "方向性读法" in shim["caveat"]

    def test_true_impl_blocked(self, doc):
        assert doc["interface"]["implementations"]["authoritative"]["status"] == "BLOCKED"

    def test_allocation_table_required(self, doc):
        assert doc["allocation_table"]["required"] is True
        assert doc["allocation_table"]["seed"] == 20260930

    def test_seed_matches_shim(self, doc):
        assert doc["allocation_table"]["seed"] == SA.DEFAULT_SEED

    def test_proxy_picked_list_matches_shim(self, doc):
        got = [_id(a) for a in SA.select_assets(list(SA.INSTRUMENT_POOL), 4, "random", SA.DEFAULT_SEED)]
        assert set(doc["main_repo_proxy_check"]["random_picked_main_repo"]) == set(got)

    def test_result_placeholders(self, doc):
        for v in doc["result_placeholders"].values():
            assert str(v).startswith("{{TODO_")

    def test_sample_size_reality(self, doc):
        r = doc["sample_size_reality_check"]
        assert r["current_measurable"] == {"holdout": 16, "corpus": 32}
        assert r["n_pairs_needed_psi_0.40"] == 138

    def test_red_lines(self, doc):
        rl = doc["red_lines"]
        assert any("不跑实验" in x for x in rl)
        assert any("预算" in x for x in rl)


def _id(a) -> str:
    return str(a["id"] if isinstance(a, dict) else a)
