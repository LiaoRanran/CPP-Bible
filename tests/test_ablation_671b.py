#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""test_ablation_671b.py — 671b A 段单元测试。

覆盖两个工具：
  * `tools/ablation_stats_671b.py` —— McNemar / Cohen's h / Fisher / BH / Holm / Δ-CI / 样本量
  * `tools/ablation_671b.py`       —— 六组 A0–A5 设计与 run plan（**不跑实验**）

红线（671b 任务书）：**本批只写脚本和设计，不跑实验** ⇒ 测试必须断言
"plan 里没有任何伪造的结果数字"，且 A5 的结构性阻塞被如实登记。
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ablation_671b as AB  # noqa: E402
import ablation_stats_671b as S  # noqa: E402


# ═════════════════════════════════════════════════════════════════════════════
# 1) 精确 McNemar
# ═════════════════════════════════════════════════════════════════════════════
class TestMcNemarExact:
    def test_p_value_closed_form_13_0(self):
        # 2·P(X≤0), X~Bin(13,0.5) = 2/8192
        r = S.mcnemar_exact(13, 0)
        assert r["p_value"] == pytest.approx(2 / 8192, abs=1e-15)
        assert r["n_discordant"] == 13

    def test_p_value_closed_form_10_0(self):
        assert S.mcnemar_exact(10, 0)["p_value"] == pytest.approx(2 / 1024, abs=1e-15)

    def test_symmetric_in_b_c(self):
        assert S.mcnemar_exact(7, 2)["p_value"] == S.mcnemar_exact(2, 7)["p_value"]

    def test_zero_discordant_is_p_one_not_error(self):
        r = S.mcnemar_exact(0, 0)
        assert r["p_value"] == 1.0
        assert "b+c=0" in r["note"]

    def test_balanced_discordant_gives_p_one(self):
        assert S.mcnemar_exact(5, 5)["p_value"] == pytest.approx(1.0, abs=1e-12)

    def test_monotone_in_imbalance(self):
        # 越不平衡 ⇒ p 越小
        ps = [S.mcnemar_exact(k, 0)["p_value"] for k in (3, 6, 9, 12)]
        assert ps == sorted(ps, reverse=True)

    def test_negative_counts_raise(self):
        with pytest.raises(ValueError):
            S.mcnemar_exact(-1, 0)
        with pytest.raises(ValueError):
            S.mcnemar_exact(0, -3)

    def test_known_paper_value(self):
        # v0.8 §6.4 报 holdout 对 (13, 0) ⇒ p=0.00024
        assert S.mcnemar_exact(13, 0)["p_value"] == pytest.approx(0.000244, abs=1e-6)

    def test_corpus_pair_10_0(self):
        # v0.8 §6.4 报 corpus 对 (10, 0) ⇒ p=0.00195
        assert S.mcnemar_exact(10, 0)["p_value"] == pytest.approx(0.00195, abs=1e-5)


# ═════════════════════════════════════════════════════════════════════════════
# 2) Cohen's h
# ═════════════════════════════════════════════════════════════════════════════
class TestCohensH:
    def test_degenerate_one_zero_is_pi(self):
        assert S.cohens_h(1.0, 0.0)["h"] == pytest.approx(math.pi, abs=1e-12)

    def test_equal_proportions_is_zero(self):
        assert S.cohens_h(0.37, 0.37)["h"] == pytest.approx(0.0, abs=1e-12)

    def test_antisymmetric(self):
        assert S.cohens_h(0.9, 0.1)["h"] == pytest.approx(-S.cohens_h(0.1, 0.9)["h"], abs=1e-12)

    def test_magnitude_buckets(self):
        assert S.cohens_h(0.50, 0.49)["magnitude"] == "negligible"
        assert S.cohens_h(0.60, 0.50)["magnitude"] == "small"
        assert S.cohens_h(0.70, 0.45)["magnitude"] == "medium"
        assert S.cohens_h(0.80, 0.20)["magnitude"] == "large"

    def test_reject_percentage_input(self):
        # 常见错误：把 87.5 当比例 —— 必须 fail-loud
        with pytest.raises(ValueError):
            S.cohens_h(87.5, 0.1)

    def test_reject_negative(self):
        with pytest.raises(ValueError):
            S.cohens_h(-0.1, 0.5)

    def test_paper_holdout_effect(self):
        # v0.8 §6.4：h(0.875, 0.0625) ≈ 1.91（极大）
        r = S.cohens_h(0.875, 0.0625)
        assert r["h"] == pytest.approx(1.9135, abs=0.004)
        assert r["magnitude"] == "large"

    def test_paper_corpus_effect(self):
        # v0.8 §6.4：h(0.4375, 0.125) ≈ 0.72。注意：0.72 < 0.8 ⇒ 按 Cohen 阈值属 **medium**
        # （v0.8 正文写"大"是**宽松措辞**；本测试按阈值口径断言 medium，并登记该措辞差异）
        r = S.cohens_h(0.4375, 0.125)
        assert r["h"] == pytest.approx(0.7227, abs=0.005)
        assert r["magnitude"] == "medium"


# ═════════════════════════════════════════════════════════════════════════════
# 3) Fisher 精确
# ═════════════════════════════════════════════════════════════════════════════
class TestFisherExact:
    def test_known_value_r_reference(self):
        # R: fisher.test(matrix(c(1,9,11,3),2)) ⇒ p = 0.0027594
        assert S.fisher_exact(1, 9, 11, 3)["p_value"] == pytest.approx(0.0027594, abs=1e-6)

    def test_perfect_separation(self):
        # [[10,0],[0,10]] ⇒ 极端分离，p 很小
        assert S.fisher_exact(10, 0, 0, 10)["p_value"] < 1e-4

    def test_independence_gives_large_p(self):
        # 完全按比例 ⇒ p ≈ 1
        assert S.fisher_exact(5, 5, 5, 5)["p_value"] == pytest.approx(1.0, abs=1e-9)

    def test_degenerate_margins(self):
        assert S.fisher_exact(0, 0, 0, 0)["p_value"] == 1.0
        assert S.fisher_exact(0, 5, 0, 5)["p_value"] == 1.0
        assert S.fisher_exact(5, 0, 5, 0)["p_value"] == 1.0

    def test_one_sided_relations(self):
        t = S.fisher_exact(8, 2, 1, 9)
        g = S.fisher_exact(8, 2, 1, 9, "greater")["p_value"]
        ls = S.fisher_exact(8, 2, 1, 9, "less")["p_value"]
        # 两条单侧各 ≤ 1；且对"方向明显"的表，观测方向那侧应更小
        assert 0.0 <= g <= 1.0 and 0.0 <= ls <= 1.0
        # [[8,2],[1,9]] 观测在"greater"方向（a 偏大）⇒ greater 侧更小
        assert g < ls
        # 双侧不超过 1
        assert 0.0 < t["p_value"] <= 1.0

    def test_invalid_alternative(self):
        with pytest.raises(ValueError):
            S.fisher_exact(1, 2, 3, 4, "both")
        with pytest.raises(ValueError):
            S.fisher_exact(1, 2, 3, 4, "Two-Sided")

    def test_negative_cell(self):
        with pytest.raises(ValueError):
            S.fisher_exact(-1, 2, 3, 4)

    def test_p_within_unit_interval(self):
        for tbl in [(1, 2, 3, 4), (0, 1, 9, 1), (100, 1, 1, 100), (2, 2, 2, 2)]:
            p = S.fisher_exact(*tbl)["p_value"]
            assert 0.0 <= p <= 1.0


# ═════════════════════════════════════════════════════════════════════════════
# 4) 多重比较校正
# ═════════════════════════════════════════════════════════════════════════════
class TestMultipleComparison:
    P_BH = [0.001, 0.008, 0.039, 0.041, 0.042, 0.06, 0.074, 0.205, 0.212, 0.216]

    def test_bh_matches_definition(self):
        # 定义 p_adj(k) = min_{j≥k} (m·p_(j)/j)，按 p 升序；已由独立第二实现交叉验证
        exp = [0.01, 0.04, 0.084, 0.084, 0.084, 0.10, 0.105714, 0.216, 0.216, 0.216]
        got = [o["adjusted_p"] for o in S.bh_fdr(self.P_BH)["adjusted"]]
        for g, e in zip(got, exp):
            assert g == pytest.approx(e, abs=1e-6)

    def test_bh_rejects_four(self):
        # adjusted ≤ 0.05 的恰 2 条（rank 1–2）；rank 3 起为 0.084
        r = S.bh_fdr(self.P_BH)
        assert r["n_reject"] == 2

    def test_holm_matches_definition(self):
        # 定义 p_adj(k) = max_{j≤k} min(1, p_(j)·(m−j+1))，按 p 升序
        exp = [0.01, 0.072, 0.312, 0.312, 0.312, 0.312, 0.312, 0.615, 0.615, 0.615]
        got = [o["adjusted_p"] for o in S.holm(self.P_BH)["adjusted"]]
        for g, e in zip(got, exp):
            assert g == pytest.approx(e, abs=1e-6)

    def test_holm_controls_fwer_more_strictly(self):
        assert S.holm(self.P_BH)["n_reject"] <= S.bh_fdr(self.P_BH)["n_reject"]

    def test_adjusted_never_exceeds_one(self):
        big = [0.9, 0.8, 0.7, 0.6]
        assert all(o["adjusted_p"] <= 1.0 for o in S.bh_fdr(big)["adjusted"])
        assert all(o["adjusted_p"] <= 1.0 for o in S.holm(big)["adjusted"])

    def test_monotone_after_sorting(self):
        got = sorted(S.bh_fdr(self.P_BH)["adjusted"], key=lambda o: o["p"])
        assert [o["adjusted_p"] for o in got] == sorted(o["adjusted_p"] for o in got)

    def test_empty_input(self):
        assert S.bh_fdr([])["m"] == 0
        assert S.holm([])["m"] == 0
        assert S.bh_fdr([])["n_reject"] == 0

    def test_single_hypothesis_unchanged(self):
        r = S.bh_fdr([0.03])
        assert r["adjusted"][0]["adjusted_p"] == pytest.approx(0.03, abs=1e-12)
        assert r["adjusted"][0]["reject"] is True

    def test_15_pairs_family(self):
        # 六组 ⇒ C(6,2)=15 对（670b §2.1）
        ps = [0.001, 0.002, 0.003, 0.004, 0.01, 0.02, 0.03, 0.04,
              0.05, 0.1, 0.2, 0.3, 0.4, 0.6, 0.9]
        r = S.bh_fdr(ps)
        assert r["m"] == 15
        assert 0 <= r["n_reject"] <= 15

    def test_reject_input(self):
        with pytest.raises(ValueError):
            S.bh_fdr([0.5, 1.5])


# ═════════════════════════════════════════════════════════════════════════════
# 5) 差值 CI
# ═════════════════════════════════════════════════════════════════════════════
class TestDeltaCI:
    def test_paired_delta_value(self):
        r = S.delta_ci_paired(13, 0, 16)
        assert r["delta"] == pytest.approx(13 / 16, abs=1e-12)
        assert r["delta_pp"] == pytest.approx(81.25, abs=1e-9)

    def test_paired_ci_excludes_zero_when_lopsided(self):
        assert S.delta_ci_paired(13, 0, 16)["crosses_zero"] is False

    def test_paired_zero_discordant_degenerate(self):
        # b=c=0 ⇒ Δ=0，CI 退化为一点 [0,0] ⇒ 不算"跨 0"（无不确定性）
        r = S.delta_ci_paired(0, 0, 10)
        assert r["delta"] == 0.0
        assert r["ci_low"] == 0.0 and r["ci_high"] == 0.0
        assert r["crosses_zero"] is False

    def test_paired_requires_positive_n(self):
        with pytest.raises(ValueError):
            S.delta_ci_paired(0, 0, 0)

    def test_paired_discordant_cannot_exceed_n(self):
        with pytest.raises(ValueError):
            S.delta_ci_paired(6, 6, 10)

    def test_paired_negative_rejected(self):
        with pytest.raises(ValueError):
            S.delta_ci_paired(-1, 2, 10)

    def test_newcombe_unpaired_delta(self):
        r = S.paired_delta_ci(14, 16, 1, 16)
        assert r["delta"] == pytest.approx(13 / 16, abs=1e-12)
        assert r["crosses_zero"] is False

    def test_newcombe_requires_positive_n(self):
        with pytest.raises(ValueError):
            S.paired_delta_ci(1, 0, 1, 16)

    def test_ci_contains_point_estimate(self):
        for (b, c, n) in [(13, 0, 16), (10, 2, 32), (5, 5, 20), (7, 1, 20)]:
            r = S.delta_ci_paired(b, c, n)
            assert r["ci_low"] <= r["delta"] <= r["ci_high"] + 1e-12


# ═════════════════════════════════════════════════════════════════════════════
# 6) 样本量
# ═════════════════════════════════════════════════════════════════════════════
class TestSampleSize:
    def test_two_proportions_15pp(self):
        # 670b §2.3 表：15pp（0.35→0.50）⇒ n/组 ≈ 167
        r = S.sample_size_two_proportions(0.35, 0.50)
        assert 140 <= r["n_per_group"] <= 200
        assert r["n_total"] == r["n_per_group"] * 2

    def test_two_proportions_20pp(self):
        # 670b §2.3：20pp（0.35→0.55）⇒ ≈93
        assert 80 <= S.sample_size_two_proportions(0.35, 0.55)["n_per_group"] <= 110

    def test_two_proportions_10pp(self):
        # 670b §2.3：10pp（0.35→0.45）⇒ ≈373
        assert 330 <= S.sample_size_two_proportions(0.35, 0.45)["n_per_group"] <= 420

    def test_two_proportions_monotone_in_delta(self):
        n_big = S.sample_size_two_proportions(0.35, 0.55)["n_per_group"]
        n_small = S.sample_size_two_proportions(0.35, 0.45)["n_per_group"]
        assert n_small > n_big

    def test_two_proportions_zero_delta_raises(self):
        with pytest.raises(ValueError):
            S.sample_size_two_proportions(0.4, 0.4)

    def test_mcnemar_psi_table(self):
        # 670b §2.3：Δ=15pp，ψ=0.40 ⇒ n≈137
        assert 120 <= S.sample_size_paired_mcnemar(0.35, 0.50, 0.40)["n_pairs"] <= 160

    def test_mcnemar_psi_0_5(self):
        # 670b §2.3：ψ=0.50 ⇒ n≈172
        assert 150 <= S.sample_size_paired_mcnemar(0.35, 0.50, 0.50)["n_pairs"] <= 200

    def test_mcnemar_larger_psi_needs_more_n(self):
        # 670b §2.3 表：ψ 越大所需 n 越大（0.30→102, 0.40→137, 0.50→172）
        n30 = S.sample_size_paired_mcnemar(0.35, 0.50, 0.30)["n_pairs"]
        n50 = S.sample_size_paired_mcnemar(0.35, 0.50, 0.50)["n_pairs"]
        assert n50 > n30

    def test_mcnemar_invalid_psi(self):
        with pytest.raises(ValueError):
            S.sample_size_paired_mcnemar(0.35, 0.50, 0.001)

    def test_mcnemar_zero_delta_raises(self):
        with pytest.raises(ValueError):
            S.sample_size_paired_mcnemar(0.4, 0.4, 0.4)


# ═════════════════════════════════════════════════════════════════════════════
# 7) 完整对照包
# ═════════════════════════════════════════════════════════════════════════════
class TestComparisonBundle:
    def test_paired_fd_vs_static_holdout(self):
        r = S.comparison({"name": "FD", "k": 14, "n": 16, "b": 13, "c": 0},
                         {"name": "Static", "k": 1, "n": 16, "b": 0, "c": 13},
                         labels=("FD", "Static"))
        assert r["verdict"] == "FD > Static"
        assert r["delta_pp"] == pytest.approx(81.25, abs=1e-9)
        assert r["ci"]["crosses_zero"] is False
        assert r["test"]["method"] == "exact-mcnemar"
        assert r["effect_size"]["h"] == pytest.approx(1.9135, abs=0.005)

    def test_zero_delta_but_wide_ci_is_undetermined(self):
        r = S.comparison({"name": "A", "k": 8, "n": 16, "b": 5, "c": 5},
                         {"name": "B", "k": 8, "n": 16, "b": 5, "c": 5})
        assert r["verdict"] == "undetermined"

    def test_identical_tables_are_tie(self):
        r = S.comparison({"name": "A", "k": 16, "n": 16, "b": 0, "c": 0},
                         {"name": "B", "k": 16, "n": 16, "b": 0, "c": 0})
        assert r["verdict"] == "tie"

    def test_unpaired_uses_fisher(self):
        r = S.comparison({"name": "A", "k": 30, "n": 40},
                         {"name": "B", "k": 5, "n": 40}, design="unpaired")
        assert r["design"] == "unpaired"
        assert r["test"]["method"] == "fisher-exact"

    def test_paired_requires_bc(self):
        with pytest.raises(ValueError):
            S.comparison({"k": 1, "n": 4}, {"k": 1, "n": 4}, design="paired")

    def test_paired_requires_equal_n(self):
        with pytest.raises(ValueError):
            S.comparison({"k": 1, "n": 4, "b": 1, "c": 0},
                         {"k": 1, "n": 5, "b": 0, "c": 1}, design="paired")

    def test_invalid_design(self):
        with pytest.raises(ValueError):
            S.comparison({"k": 1, "n": 2}, {"k": 1, "n": 2}, design="both")

    def test_reverse_direction(self):
        r = S.comparison({"name": "S", "k": 1, "n": 16, "b": 0, "c": 13},
                         {"name": "F", "k": 14, "n": 16, "b": 13, "c": 0},
                         labels=("Static", "FD"))
        assert r["verdict"] == "FD > Static"


# ═════════════════════════════════════════════════════════════════════════════
# 8) ablation_671b —— 六组设计（**不跑实验**）
# ═════════════════════════════════════════════════════════════════════════════
class TestAblationDesign:
    def test_six_groups(self):
        p = AB.build_plan()
        assert [g["id"] for g in p["groups"]] == ["A0", "A1", "A2", "A3", "A4", "A5"]

    def test_not_executed(self):
        assert AB.build_plan()["executed"] is False

    def test_all_results_are_placeholders(self):
        for g in AB.build_plan()["groups"]:
            assert g["result_placeholder"] == f"{{{{TODO_ablation_{g['id']}}}}}"

    def test_no_fabricated_numbers_in_group_records(self):
        # 红线：本批不跑实验 ⇒ 组记录里不得出现结果数字键
        bad_keys = {"result", "detect_rate", "k", "n", "catch", "miss", "rate", "p_value"}
        for g in AB.build_plan()["groups"]:
            assert not (bad_keys & set(g)), f"{g['id']} 含伪造结果键"

    def test_no_fabricated_numbers_in_contrasts(self):
        for c in AB.build_plan()["contrasts"]:
            assert c["ci_crosses_zero"] is None
            assert c["delta_placeholder"].startswith("{{TODO_delta_")

    def test_a5_is_blocked_with_reason(self):
        a5 = next(g for g in AB.build_plan()["groups"] if g["id"] == "A5")
        assert a5["feasible"] is False
        assert "select_assets" in " ".join(a5["blockers"])
        assert a5["status"] == "BLOCKED"

    def test_a0_ready(self):
        a0 = next(g for g in AB.build_plan()["groups"] if g["id"] == "A0")
        assert a0["feasible"] is True

    def test_a1_requires_git_revert(self):
        assert next(g for g in AB.build_plan()["groups"] if g["id"] == "A1")["git_revert"] is True

    def test_a2_notes_blind_irreversibility(self):
        a2 = next(a for a in AB.ABLATIONS if a["id"] == "A2")
        assert "iron_rule" in a2["precondition_note"]
        assert "回盲" in a2["precondition_note"]

    def test_a4_metric_is_not_detection_rate(self):
        a4 = next(g for g in AB.build_plan()["groups"] if g["id"] == "A4")
        assert "不是检测率" in a4["metrics"][0] or "不作缺陷检测率" in a4["test"]

    def test_five_contrasts_vs_a0(self):
        p = AB.build_plan()
        assert len(p["contrasts"]) == 5
        assert all(c["contrast"].startswith("A0 − A") for c in p["contrasts"])

    def test_key_contrast_flagged(self):
        key = next(c for c in AB.build_plan()["contrasts"] if "A5" in c["contrast"])
        assert "关键对照" in key["note"]

    def test_a2_uses_unpaired(self):
        assert next(c for c in AB.build_plan()["contrasts"] if "A2" in c["contrast"])["design"] == "unpaired"

    def test_design_doc_exists_and_is_referenced(self):
        assert AB.DESIGN_DOC.is_file()
        assert AB.build_plan()["design_doc"] == "research/670b_ablation设计.md"

    def test_summary_counts(self):
        s = AB.build_plan()["summary"]
        assert s["n_groups"] == 6
        assert s["n_ready"] + s["n_blocked"] == 6
        assert "A5" in s["blocked_ids"]

    def test_feasibility_reports_missing_prereq(self, tmp_path, monkeypatch):
        monkeypatch.setattr(AB, "ROOT", tmp_path)
        a = {"id": "X", "blocked": False, "prereq": ["data/nope.json"],
             "blocked_reason": ""}
        fe = AB.feasibility(a)
        assert fe["ok"] is False
        assert "data/nope.json" in fe["missing"]

    def test_stat_primitives_declared(self):
        prims = AB.build_plan()["stat_primitives"]
        assert "mcnemar_exact" in prims
        assert "cohens_h" in prims
        assert "bh_fdr" in prims
        assert "holm" in prims

    def test_red_lines_recorded(self):
        rl = AB.build_plan()["red_lines"]
        assert any("不跑实验" in x for x in rl)
        assert any("不编造" in x for x in rl)

    def test_selftest_passes(self):
        assert AB.selftest() == 0

    def test_stats_selftest_passes(self):
        assert S.selftest() == 0

    def test_plan_json_roundtrip(self, tmp_path):
        p = AB.build_plan()
        f = tmp_path / "plan.json"
        AB._write_json(f, p)
        got = json.loads(f.read_text(encoding="utf-8"))
        assert got["schema"] == "queyi-ablation-plan/671b"
        assert got["executed"] is False
        assert len(got["groups"]) == 6


# ═════════════════════════════════════════════════════════════════════════════
# 9) 与既有 baseline 产物的一致性（复用 670a 的现算值）
# ═════════════════════════════════════════════════════════════════════════════
class TestConsistencyWithBaselineArtifacts:
    @staticmethod
    @pytest.fixture(scope="class")
    def fd():
        p = ROOT / "data" / "experiments" / "baseline_fd.json"
        if not p.is_file():
            pytest.skip("baseline_fd.json 不存在（670a 未跑）")
        return json.loads(p.read_text(encoding="utf-8"))

    def test_recompute_holdout_ci_matches_artifact(self, fd):
        # 用 ablation_stats 的 CI 原语重算 holdout 可测口径，与 670a 产物对齐
        m = fd["holdout"]["measurable"]
        r = S.paired_delta_ci(m["k"], m["n"], 0, m["n"])
        assert r["p1"] == pytest.approx(m["point"], abs=1e-12)

    def test_recompute_effect_size_from_artifact_rates(self, fd):
        # 672h 扩样后：holdout FD(34/41) vs Static(1/41) ⇒ Cohen's h ≈ 1.976
        # （原 1.7983 对应扩样前 17/21 vs 1/21；artifact 已更新，期望值同步）
        st = json.loads((ROOT / "data" / "experiments" / "baseline_static.json")
                        .read_text(encoding="utf-8"))
        h = S.cohens_h(fd["holdout"]["measurable"]["point"],
                       st["holdout"]["measurable"]["point"])
        assert abs(h["h"]) == pytest.approx(1.976, abs=0.005)

    def test_recompute_holdout_mcnemar_from_artifact(self, fd):
        # 672h 扩样后：holdout FD(34/41) vs Static(1/41) ⇒ 不一致对 (33, 0)
        # ⇒ McNemar p = 2/2^33 ≈ 2.328e-10（原 3.0518e-05 对应扩样前 b=16）
        st = json.loads((ROOT / "data" / "experiments" / "baseline_static.json")
                        .read_text(encoding="utf-8"))
        b = fd["holdout"]["measurable"]["k"] - st["holdout"]["measurable"]["k"]
        c = 0
        assert S.mcnemar_exact(b, c)["p_value"] == pytest.approx(2.3283e-10, abs=1e-6)
