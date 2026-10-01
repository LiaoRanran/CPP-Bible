# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""672k W6 统计重做测试（≥30 条断言）：拒绝域一致性 / 功效 / 样本量 / e-process / 产物口径。"""
from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


def _load(rel: str):
    spec = importlib.util.spec_from_file_location(Path(rel).stem, str(ROOT / rel))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


K = _load("tools/stats_672k.py")
A = _load("tools/ablation_stats_671b.py")
CS = _load("tools/confidence_sequence.py")


# ── 拒绝域与配对口径 ─────────────────────────────────────────────────────────
def test_mcnemar_reject_matches_canonical():
    for b, c in ((13, 0), (5, 5), (6, 1), (10, 2), (16, 0), (29, 0), (33, 0), (0, 0)):
        assert K.mcnemar_reject(b, c) == (A.mcnemar_exact(b, c)["p_value"] <= 0.05), (b, c)
    assert K.mcnemar_reject(0, 0) is False
    assert K.mcnemar_reject(33, 0) is True


def test_arm_reconstruction_matches_baseline_products():
    br = json.loads((ROOT / "data/experiments/baseline_random.json").read_text(encoding="utf-8"))
    bs = json.loads((ROOT / "data/experiments/baseline_static.json").read_text(encoding="utf-8"))
    h = K.arm_verdicts(K.holdout_rows(), "static")
    c = K.arm_verdicts(K.corpus_rows(), "static")
    k_h = sum(1 for v in h.values() if v == "catch")
    k_c = sum(1 for v in c.values() if v == "catch")
    assert k_h == bs["holdout"]["measurable"]["k"] == 1
    assert k_c == bs["corpus"]["measurable"]["k"] == 11
    r_h = K.arm_verdicts(K.holdout_rows(), "random", set(br["selection"]["holdout"]["picked"]))
    r_c = K.arm_verdicts(K.corpus_rows(), "random", set(br["selection"]["corpus"]["picked"]))
    assert sum(1 for v in r_h.values() if v == "catch") == br["holdout"]["measurable"]["k"] == 4
    assert sum(1 for v in r_c.values() if v == "catch") == br["corpus"]["measurable"]["k"] == 14


def test_pair_stats_against_canonical():
    fd = {"a": "catch", "b": "miss", "c": "catch", "d": "miss"}
    st = {"a": "miss", "b": "miss", "c": "catch", "d": "catch"}
    p = K.pair(fd, st)
    assert p["n"] == 4 and p["arm_a_k"] == 2 and p["arm_b_k"] == 2
    assert p["discordant"] == {"b_a_only": 1, "c_b_only": 1, "n_discordant": 2}
    assert abs(p["cohens_h"]) < 1e-12                       # 同比例 ⇒ h=0
    ref = A.delta_ci_paired(1, 1, 4)
    assert abs(p["delta_ci95_pct"][0] - ref["ci_low"] * 100) < 0.01


# ── post-hoc power ───────────────────────────────────────────────────────────
def test_posthoc_power_properties():
    assert K.posthoc_power(0, 0)["power"] is None
    assert K.posthoc_power(33, 0)["power"] == 1.0
    assert K.posthoc_power(1, 0)["power"] < 0.2
    # 单调：同一不平衡方向，样本越多功效越高
    assert K.posthoc_power(10, 5)["power"] < K.posthoc_power(20, 10)["power"]
    # 方向性：全一致方向（c=0）功效高于对半分（b=c 时必不显著 ⇒ 功效=α 量级）
    pw_balanced = K.posthoc_power(10, 10)["power"]
    assert pw_balanced < 0.06
    assert K.posthoc_power(20, 0)["power"] > pw_balanced


# ── 样本量 ───────────────────────────────────────────────────────────────────
def test_sample_size_precision_monotone_and_plausible():
    n3 = K.sample_size_for_precision(0.83, 3.0)["n"]
    n5 = K.sample_size_for_precision(0.83, 5.0)["n"]
    n10 = K.sample_size_for_precision(0.83, 10.0)["n"]
    assert n3 and n5 and n10
    assert n3 > n5 > n10 > 0
    # 已知量级：p≈0.83、±5pp ⇒ 约 200~300
    assert 150 < n5 < 400
    # 极端 p 附近半宽更小（CP 不对称）⇒ 需要样本不会更多
    assert K.sample_size_for_precision(0.97, 5.0)["n"] <= n5


def test_sample_size_for_delta_uses_canonical():
    r = K.sample_size_for_delta(0.83, 0.024, 0.8, power=0.8)
    assert r["power"] == 0.8 and r["psi_discordant_rate"] == 0.8
    assert r["n_pairs"] is None or r["n_pairs"] > 0
    # 规范库同参一致
    ref = A.sample_size_paired_mcnemar(0.83, 0.024, 0.8, power=0.8)
    assert r["n_pairs"] == ref.get("n")


# ── e-process / 序贯 ─────────────────────────────────────────────────────────
def test_e_value_properties():
    assert K.e_value(0, 0)["e_value"] == 1.0
    assert K.e_value(0, 0)["reject_at_alpha"] is False
    e_big = K.e_value(33, 0)
    assert e_big["reject_at_alpha"] is True and e_big["e_value"] > 20
    assert e_big["anytime_p"] <= 0.05
    # 方向单调
    assert K.e_value(10, 3)["e_value"] > K.e_value(7, 6)["e_value"]
    # 与 confidence_sequence 单一来源一致（产物保留 4 位小数 ⇒ 容差 1e-3）
    assert abs(K.e_value(20, 5)["e_value"] - CS.eprocess(0.5, 20, 25)) < 1e-3


def test_anytime_interval_wider_than_fixed_sample():
    lo_cs, hi_cs = CS.cs_interval(33, 33, 0.05)
    r = _load("tools/stat_bounds.py").proportion(33, 33, 0.95)
    assert (hi_cs - lo_cs) >= (r["cp_high"] - r["cp_low"]) - 1e-9


# ── 产物口径 ─────────────────────────────────────────────────────────────────
def test_product_shape_and_numbers():
    p = ROOT / "data/experiments/stats_672k.json"
    if not p.is_file():
        return
    d = json.loads(p.read_text(encoding="utf-8"))
    assert d["schema"] == "queyi-stats/672k" and d["alpha"] == 0.05
    for s in ("holdout", "corpus"):
        blk = d["sets"][s]
        st, rn = blk["fd_vs_static"], blk["fd_vs_random_proxy"]
        assert st["delta_pp"] > 0 and rn["delta_pp"] > 0
        assert st["mcnemar_p"] < 0.05 and rn["mcnemar_p"] < 0.05
        assert st["discordant"]["c_b_only"] == 0        # 观测：static 没有独家命中
        assert blk["e_value_static"]["reject_at_alpha"] is True
        assert blk["posthoc_power_static"]["power"] == 1.0
        # Δ 的 CI 不跨 0
        assert st["delta_ci95_pct"][0] > 0
        # CI 必须包住点值
        assert st["delta_ci95_pct"][0] <= st["delta_pp"] <= st["delta_ci95_pct"][1]
    # LLM 臂：固定样本显著 vs 任意时刻不显著 —— 必须并列落盘
    llm = d["llm_arm"]
    assert llm["mcnemar_p"] < 0.05
    assert llm["e_value_llm_better"]["reject_at_alpha"] is False
    assert llm["e_value_llm_better"]["e_value"] < 20


def test_current_numbers_synced_with_stats():
    cn = json.loads((ROOT / "data/current_numbers.json").read_text(encoding="utf-8"))
    st = json.loads((ROOT / "data/experiments/stats_672k.json").read_text(encoding="utf-8"))
    for key, s in (("holdout_fd_vs_static", "holdout"),
                   ("corpus_fd_vs_static", "corpus")):
        assert cn["comparisons"][key]["delta_pp"] == st["sets"][s]["fd_vs_static"]["delta_pp"]
        assert cn["comparisons"][key]["mcnemar_p"] == st["sets"][s]["fd_vs_static"]["mcnemar_p"]
    assert cn["comparisons"]["holdout_fd_vs_random"]["e_value"] == \
        st["sets"]["holdout"]["e_value_random"]["e_value"]
    assert cn["sample_size_672k"]["holdout"]["±5pp"]["n"] == \
        st["sample_size"]["precision"]["holdout"]["±5pp"]["n"]
    assert "posthoc_power" in cn["stats_672k_note"]
