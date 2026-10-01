#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""test_stats_671b.py — 671b D 段：统计口径与样本量工具测试。

覆盖：
  * `tools/sample_size_671b.py`      —— 样本量现算（两比例 / 配对 McNemar / CI 半宽 / 效力曲线）
  * `research/671b_统计口径_ablation.md` —— 文档与实现的一致性（不许文档说的和代码做的不一样）
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import ablation_stats_671b as AS   # noqa: E402
import sample_size_671b as SS      # noqa: E402
import stat_bounds as sb           # noqa: E402

CALIBER_DOC = ROOT / "research" / "671b_统计口径_ablation.md"


class TestSampleSizeTables:
    def test_two_proportions_has_four_rows(self):
        assert len(SS.two_proportion_table()) == 4

    def test_two_proportions_monotone_in_delta(self):
        rows = sorted(SS.two_proportion_table(), key=lambda x: x["delta_pp"])
        ns = [r["n_per_group"] for r in rows]
        assert ns == sorted(ns, reverse=True)

    def test_two_proportions_within_15pct_of_doc(self):
        for r in SS.two_proportion_table():
            rel = abs(r["drift_vs_doc"]) / r["doc_value"]
            assert rel < 0.15, f"Δ={r['delta_pp']} 漂移 {rel:.1%}"

    def test_two_proportions_specific_values(self):
        got = {(r["p1"], r["p2"]): r["n_per_group"] for r in SS.two_proportion_table()}
        assert got[(0.35, 0.50)] == 170
        assert got[(0.35, 0.55)] == 96

    def test_mcnemar_has_three_rows(self):
        assert len(SS.mcnemar_table()) == 3

    def test_mcnemar_monotone_in_psi(self):
        rows = sorted(SS.mcnemar_table(), key=lambda x: x["psi"])
        ns = [r["n_pairs"] for r in rows]
        assert ns == sorted(ns)

    def test_mcnemar_specific_values(self):
        got = {r["psi"]: r["n_pairs"] for r in SS.mcnemar_table()}
        assert got[0.30] == 103
        assert got[0.40] == 138
        assert got[0.50] == 173

    def test_mcnemar_within_15pct_of_doc(self):
        for r in SS.mcnemar_table():
            rel = abs(r["drift_vs_doc"]) / r["doc_value"]
            assert rel < 0.15

    def test_ci_halfwidth_monotone(self):
        rows = SS.ci_halfwidth_table()
        hw = [r["halfwidth_pp"] for r in rows]
        assert hw == sorted(hw, reverse=True)

    def test_ci_halfwidth_matches_stat_bounds(self):
        # 与 stat_bounds 的 CP 区间交叉核对（同一来源）
        for r in SS.ci_halfwidth_table():
            lo, hi = sb.cp_interval(r["n"] // 2, r["n"])
            assert r["halfwidth_pp"] == pytest.approx((hi - lo) / 2 * 100, abs=0.06)

    def test_current_gap_target_n_in_expected_range(self):
        # 669d §4：±10pp ⇒ n ≈ 93–104
        n = SS.current_gap()["n_needed_for_target"]
        assert 90 <= n <= 110

    def test_current_gap_positive(self):
        g = SS.current_gap()
        assert all(v > 0 for v in g["gap"].values())
        # 671a 扩样后：holdout 21 可测 / corpus 48 可测（reveal_update_671a.json）
        assert g["current"]["holdout_measurable"] == 21
        assert g["current"]["corpus_measurable"] == 48

    def test_power_curve_monotone(self):
        md = [r["min_detectable_delta_pp"] for r in SS.power_curve()]
        assert md == sorted(md, reverse=True)

    def test_power_curve_endpoints(self):
        rows = {r["n_per_group"]: r["min_detectable_delta_pp"] for r in SS.power_curve()}
        assert rows[21] > 40          # n=21 只能检出巨大差异（671a 扩样后最小档）
        assert rows[392] < 11         # n=392 可检出 ~10pp

    def test_power_curve_consistent_with_sample_size(self):
        # n=170 处，可检出 Δ 应接近 15pp
        rows = {r["n_per_group"]: r["min_detectable_delta_pp"] for r in SS.power_curve()}
        assert 14.0 <= rows[172] <= 16.0

    def test_run_returns_expected_keys(self):
        r = SS.run()
        for k in ("schema", "two_proportions", "paired_mcnemar", "ci_halfwidth",
                  "current_gap", "power_curve", "red_lines", "note"):
            assert k in r

    def test_selftest_passes(self):
        assert SS.selftest() == 0


class TestCaliberDocument:
    def test_doc_exists(self):
        assert CALIBER_DOC.is_file()

    def test_doc_declares_design_only(self):
        t = CALIBER_DOC.read_text(encoding="utf-8")
        assert "DESIGN ONLY" in t or "设计稿" in t
        assert "只写脚本和设计，不跑实验" in t

    def test_doc_cites_implementations(self):
        t = CALIBER_DOC.read_text(encoding="utf-8")
        assert "ablation_stats_671b.py" in t
        assert "sample_size_671b.py" in t
        assert "ablation_671b.py" in t

    def test_doc_states_tests_not_blended(self):
        t = CALIBER_DOC.read_text(encoding="utf-8")
        assert "McNemar" in t and "Fisher" in t and "BH-FDR" in t
        assert "不得" in t

    def test_doc_mcnemar_values_match_implementation(self):
        t = CALIBER_DOC.read_text(encoding="utf-8")
        for psi, n in ((0.30, 103), (0.40, 138), (0.50, 173)):
            assert str(n) in t, f"文档缺 ψ={psi} 的现算值 {n}"

    def test_doc_two_prop_values_match_implementation(self):
        t = CALIBER_DOC.read_text(encoding="utf-8")
        for n in (170, 96, 376):
            assert str(n) in t

    def test_doc_records_effect_size_wording_fix(self):
        # h=0.72 应为 medium，v0.8 写"大"是宽松措辞 —— 必须登记
        t = CALIBER_DOC.read_text(encoding="utf-8")
        assert "0.72" in t
        assert "medium" in t or "中" in t

    def test_doc_red_line_sample_size(self):
        t = CALIBER_DOC.read_text(encoding="utf-8")
        assert "不得" in t and "显著优于" in t

    def test_doc_marks_a2_as_unpaired(self):
        t = CALIBER_DOC.read_text(encoding="utf-8")
        assert "A2" in t and ("unpaired" in t or "独立" in t)

    def test_doc_no_result_numbers(self):
        # 红线：本批不跑实验 ⇒ 文档里不得出现 ablation 的"结果"表
        t = CALIBER_DOC.read_text(encoding="utf-8")
        assert "{{TODO_ablation" in t or "本批不跑" in t


class TestAblationStatsIntegration:
    """样本量工具与统计原语的一致性（不许两处各算一份）。"""

    def test_two_prop_matches_pure_primitive(self):
        for r in SS.two_proportion_table():
            p = AS.sample_size_two_proportions(r["p1"], r["p2"])
            assert r["n_per_group"] == p["n_per_group"]

    def test_mcnemar_matches_pure_primitive(self):
        for r in SS.mcnemar_table():
            p = AS.sample_size_paired_mcnemar(r["p1"], r["p2"], r["psi"])
            assert r["n_pairs"] == p["n_pairs"]

    def test_artifact_written_by_run(self, tmp_path, monkeypatch):
        monkeypatch.setattr(SS, "OUT", tmp_path / "ss.json")
        assert SS.main(["--run"]) == 0
        doc = json.loads((tmp_path / "ss.json").read_text(encoding="utf-8"))
        assert doc["schema"] == "queyi-sample-size/671b"
        assert len(doc["paired_mcnemar"]) == 3
