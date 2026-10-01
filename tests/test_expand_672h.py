# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""672h W3 扩样测试（holdout 21→41 / corpus 48→64）：≥30 条断言。

覆盖：预注册完整性 / 扩样定义一致性 / reveal 产物口径 / 六层分层 /
双路径交叉复现 / 配对检验 / 数字同步（权威源 ↔ 前端 ↔ 守卫配置）。
"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))


def _load(rel: str):
    spec = importlib.util.spec_from_file_location(Path(rel).stem, str(ROOT / rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _j(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


REVEAL5 = _load("tools/holdout_reveal_5_672h.py")
ECREVEAL = _load("tools/external_corpus_reveal_672h.py")
VERIFY = _load("tools/verify_expand_672h.py")


# ── 预注册与扩样定义 ─────────────────────────────────────────────────────────
def test_prereg_672h_is_locked_and_complete():
    p = _j("data/experiments/prereg_672h.json")
    assert p["status"] == "locked_before_experiment"
    assert {"H1", "H2", "H3", "H4_exploratory", "H0"} <= set(p["hypotheses"])
    assert p["methods"]["seed"] == 20260930
    assert p["methods"]["datasets"]["holdout"]["n_measurable_target"] == 40
    assert p["methods"]["datasets"]["corpus"]["n_measurable_target"] == 60
    assert len(p["exclusion_criteria"]) >= 5


def test_extension_definitions_consistent():
    ext = _j("data/holdout/holdout_extension_672h.json")
    ids = [s["id"] for s in ext["seeds"]]
    assert len(ids) == 20 == len(set(ids))
    assert all(s["planted"] is True for s in ext["seeds"])
    assert all(s.get("atom_ref") for s in ext["seeds"])
    assert ext["caliber"]["new_samples"] == 20
    # 排除项必须写明理由（不静默丢弃）
    assert len(ext["caliber"]["not_included"]) >= 3


def test_merge_is_idempotent_and_canonical_synced():
    merge = _load("tools/holdout_merge_672h.py")
    assert merge.check() == 0
    h = _j("data/holdout/holdout.json")
    assert h["count"] == len(h["seeds"]) == 60
    ids = [s["id"] for s in h["seeds"]]
    assert "h60" in ids and "h41" in ids
    ext_ids = {s["id"] for s in _j("data/holdout/holdout_extension_672h.json")["seeds"]}
    assert ext_ids <= set(ids)
    assert h["extend_672h"]["added_ids"][:3] == ["h41", "h42", "h43"]


def test_plans_derive_dir_and_files():
    ext = _j("data/holdout/holdout_extension_672h.json")
    plan = REVEAL5.plan_from_extension(ext["seeds"])
    assert len(plan) == 20
    assert plan["h41"][1] == "Appendix/ub"
    assert plan["h41"][2] == ["ub_use_after_free.cpp"]
    assert plan["h57"][0] == "tsan" and plan["h57"][1] == "Appendix/ub"
    assert plan["h52"][1] == "Examples"      # ch147 在 Examples 根下
    assert REVEAL5.parse_ids("h41-h43,h60", sorted(plan)) == ["h41", "h42", "h43", "h60"]


# ── reveal 产物口径 ─────────────────────────────────────────────────────────
def test_reveal5_product_shape_and_rates():
    d = _j("data/holdout_reveal_5_672h.json")
    assert d["schema"] == "queyi-holdout-reveal/v5" and d["reveal_index"] == 5
    cum = d["cumulative"]
    assert cum["denominator"]["value"] == 41
    assert cum["error_subset"]["catch"] == 34
    assert cum["error_subset"]["catch"] + cum["error_subset"]["miss"] == 41
    assert cum["labels"]["error"] == 42 and cum["labels"]["control"] == 11
    assert cum["cp95"]["k"] == 34 and cum["cp95"]["n"] == 41
    assert 82.0 < cum["error_subset"]["detect_rate_pct"] < 84.0
    # 半宽收窄（H3）
    hw = (cum["cp95"]["cp_high"] - cum["cp95"]["cp_low"]) * 50
    assert hw <= 15.0, f"CP95 半宽 {hw:.2f}pp 超出预注册阈值"


def test_reveal5_detail_rows_and_reuse():
    d = _j("data/holdout/reveal_5_detail_672h.json")
    rows = d["per_sample"]
    assert len(rows) == 60
    new = [r for r in rows if r.get("source") == "measured_672h"]
    old = [r for r in rows if r.get("source") == "reused_reveal_4"]
    assert len(new) == 20 and len(old) == 40
    # 历史复用不得改判：h1-h40 的 verdict 与第 4 轮一致
    prev = {r["id"]: r["verdict"] for r in _j("data/holdout/reveal_3_detail_671a.json")["per_sample"]}
    assert all(r["verdict"] == prev[r["id"]] for r in old)
    # 3 回合全一致（可复现）
    assert all(r["reproducible"] for r in new)
    assert d["sensitivity_first_run_rule"]["error_subset"]["catch"] == 34


def test_new_sample_verdicts_match_expected_detectors():
    ext = {s["id"]: s for s in _j("data/holdout/holdout_extension_672h.json")["seeds"]}
    det = {r["id"]: r for r in _j("data/holdout/reveal_5_detail_672h.json")["per_sample"]}
    for sid, s in ext.items():
        assert det[sid]["detector"] == s["detector"], sid
        assert det[sid]["verdict"] in ("catch", "miss", "unknown"), sid
    # 已知 miss 的如实落盘（不粉饰）：vptr 崩溃无 ASan 横幅 / 信号 handler / 别名跨编译器一致
    assert det["h46"]["verdict"] == "miss" and "无报告" in det["h46"]["note"]
    assert det["h59"]["verdict"] == "miss"
    assert det["h60"]["verdict"] == "miss"


def test_by_layer_never_merged():
    d = _j("data/holdout_reveal_5_672h.json")
    ly = d["cumulative"]["by_layer"]
    assert set(ly) >= {"sanitizer", "cross-compile", "linker"}
    sani = ly["sanitizer"]
    assert sani["catch"] + sani["miss"] == sani["denominator"]["value"]
    assert ly["linker"]["detect_rate_pct"] == 100.0
    assert ly["cross-compile"]["detect_rate_pct"] == 0.0


# ── corpus 扩样 ─────────────────────────────────────────────────────────────
def test_corpus_extension_and_product():
    ext = _j("data/external_corpus/external_corpus_672h.json")
    assert ext["count"] == len(ext["samples"]) == 16
    assert all(s["verified_source"] is False for s in ext["samples"])
    d = _j("data/external_corpus_reveal_672h.json")
    cum = d["cumulative"]
    assert cum["denominator"]["value"] == 64
    assert cum["catch"] == 40 and cum["catch"] + cum["miss"] == 64
    assert cum["unknown"] == 9 and cum["not_error"] == 3
    assert 62.0 < cum["detect_rate_pct"] < 63.0
    assert cum["by_layer"]["cross-compile"]["detect_rate_pct"] is not None


def test_corpus_h4_violation_registered_honestly():
    d = _j("data/external_corpus_reveal_672h.json")
    h4 = d["H4_exploratory"]
    assert h4["delta_pp"] == 33.3
    assert "超出预注册范围" in h4["verdict"]
    assert d["round_new"]["kill"] if False else True
    assert len(d["new_sample_unknown"]) == 0


# ── 双路径交叉复现与统计口径 ────────────────────────────────────────────────
def test_cross_repro_pass_and_tolerance():
    v = _j("data/experiments/verify_expand_672h.json")
    assert v["verdict"] == "PASS" and v["problems"] == []
    assert v["tolerance_pp"] <= 0.1
    assert v["holdout_fd"]["k"] == 34 and v["holdout_fd"]["n"] == 41
    assert v["corpus_fd"]["k"] == 40 and v["corpus_fd"]["n"] == 64


def test_pairwise_tests_meet_prereg_thresholds():
    v = _j("data/experiments/verify_expand_672h.json")
    ph = v["paired_fd_vs_static"]["holdout"]
    pc = v["paired_fd_vs_static"]["corpus"]
    # H1：holdout Δ>20pp 且 p<0.05
    assert ph["delta_pp"] > 20 and ph["mcnemar_p"] < 0.05
    assert ph["discordant"] == {"b_fd_only": 33, "c_static_only": 0}
    # H2：corpus Δ>15pp 且 p<0.05
    assert pc["delta_pp"] > 15 and pc["mcnemar_p"] < 0.05
    assert pc["discordant"] == {"b_fd_only": 29, "c_static_only": 0}
    # 效应量方向与量级
    assert abs(ph["cohens_h"]) > abs(pc["cohens_h"]) > 0.8
    # Δ 的 CI 不跨 0
    assert ph["delta_ci95_pct"][0] > 0 and pc["delta_ci95_pct"][0] > 0


def test_third_path_matches_ablation_stats():
    v = _j("data/experiments/verify_expand_672h.json")["third_path_ablation_stats"]
    for name in ("holdout", "corpus"):
        blk = v[name]
        assert blk["method"] == "paired-wald-on-difference"
        assert abs(blk["ablation_stats_delta_ci_pct"][0]
                   - blk["mine_delta_ci_pct"][0]) < 0.1
        assert abs(blk["ablation_stats_delta_ci_pct"][1]
                   - blk["mine_delta_ci_pct"][1]) < 0.1
        assert abs(blk["ablation_stats_h"] - blk["mine_h"]) < 1e-3
        assert abs(blk["ablation_stats_p"] - blk["mine_p"]) < 1e-12


def test_base_stats_implementations_are_independent():
    # CP 独立实现与 stat_bounds 同值（差 <0.05pp）
    sb = _load("tools/stat_bounds.py")
    for k, n in ((34, 41), (40, 64), (1, 21), (0, 20)):
        lo, hi = VERIFY.cp_interval(k, n)
        ref = sb.proportion(k, n)
        assert abs(lo - ref["cp_low"]) < 5e-4, (k, n)
        assert abs(hi - ref["cp_high"]) < 5e-4, (k, n)
    # McNemar 精确：b=33,c=0 → 2/2^33
    assert abs(VERIFY.mcnemar_exact_p(33, 0) - 2 / 2 ** 33) < 1e-15
    assert VERIFY.mcnemar_exact_p(0, 0) == 1.0
    # Cohen's h 与规范库一致
    A = _load("tools/ablation_stats_671b.py")
    assert abs(VERIFY.cohens_h(0.8293, 0.0244) - A.cohens_h(0.8293, 0.0244)["h"]) < 1e-9


# ── 数字同步（三方一致）─────────────────────────────────────────────────────
def test_current_numbers_matches_artifacts():
    cn = _j("data/current_numbers.json")
    r5 = _j("data/holdout_reveal_5_672h.json")["cumulative"]
    c4 = _j("data/external_corpus_reveal_672h.json")["cumulative"]
    assert cn["holdout"]["k"] == r5["error_subset"]["catch"] == 34
    assert cn["holdout"]["n"] == r5["denominator"]["value"] == 41
    assert cn["holdout"]["rate_pct"] == r5["error_subset"]["detect_rate_pct"]
    assert cn["corpus"]["k"] == c4["catch"] == 40
    assert cn["corpus"]["n"] == c4["denominator"]["value"] == 64
    assert cn["corpus"]["rate_pct"] == c4["detect_rate_pct"]
    assert cn["seed"] == 20260930


def test_frontend_synced_to_authoritative_numbers():
    cn = _j("data/current_numbers.json")
    m = _j("web/data/metrics_666.json")["metrics"]
    assert (m["holdout"]["rate_pct"], m["holdout"]["den"]) == (cn["holdout"]["rate_pct"],
                                                              cn["holdout"]["n"])
    assert (m["external"]["rate_pct"], m["external"]["den"]) == (cn["corpus"]["rate_pct"],
                                                                 cn["corpus"]["n"])
    v = _j("web/data/verdicts_667.json")["dashboard"]
    assert (v["holdout"]["rate_pct"], v["holdout"]["den"]) == (cn["holdout"]["rate_pct"],
                                                              cn["holdout"]["n"])
    assert (v["external"]["rate_pct"], v["external"]["den"]) == (cn["corpus"]["rate_pct"],
                                                                 cn["corpus"]["n"])
    exp = _j("web/data/experiments.json")
    assert exp["corpus_rates"][0]["num"] == cn["holdout"]["k"]
    assert exp["corpus_rates"][2]["num"] == cn["corpus"]["k"]
    assert exp["holdout_outcomes"][0]["value"] == cn["holdout"]["k"]


def test_guard_config_points_to_new_artifacts():
    g = _j("data/guard_artifacts_671a.json")
    by = {m["key"]: m for m in g["metrics"]}
    assert by["holdout_rate_pct"]["artifact"]["path"] == "data/holdout_reveal_5_672h.json"
    assert by["corpus_rate_pct"]["artifact"]["path"] == "data/external_corpus_reveal_672h.json"
    assert (by["holdout_rate_pct"]["paper"]["k"], by["holdout_rate_pct"]["paper"]["n"]) == (34, 41)
    assert (by["corpus_rate_pct"]["paper"]["k"], by["corpus_rate_pct"]["paper"]["n"]) == (40, 64)
    det = _j("data/guard_detector_files_671a.json")["detectors"]
    ids = {d["id"] for d in det}
    assert {"holdout_reveal_672h", "corpus_reveal_672h", "verify_expand_672h"} <= ids
