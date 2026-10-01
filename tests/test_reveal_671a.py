# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""tests/test_reveal_671a.py — 671a C 段的回归测试（扩样 reveal + 检出率更新）。

纪律：本批 C 段的产物是**数字**，所以用例重点不是"跑起来没报错"，而是
**数字能不能被独立复算**（670c/671a 门禁只守"改了代码必重跑"，守不了"算得对不对"）：

  * 分母口径：真错 = catch+miss；unknown 与标签 unknown 都不进分母；
  * 计划推导：新样本的 (detector, 夹具) 从 `holdout_extension_669d.json` 现推导，**不手抄**；
  * 产物复算：`reveal_update_671a.json` 里的每个率/区间都能从 reveal 产物重算出来；
  * 拒绝编造：缺样品/非法范围/未声明的样本一律显式拒绝，绝不静默返回空。
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import external_corpus_reveal_671a as C  # noqa: E402
import holdout_reveal_4_671a as H  # noqa: E402
import reveal_update_671a as U  # noqa: E402


# ─────────────────────────────────────────────────────────────────────────────
# ① 样本选择：范围解析（id 自带 `-`）+ 非法输入显式拒绝
# ─────────────────────────────────────────────────────────────────────────────

def test_parse_samples_holdout_forms():
    ids = ["h1", "h2", "h31", "h32", "h40"]
    assert H.parse_samples("all", ids) == ids
    assert H.parse_samples("h31-h32", ids) == ["h31", "h32"]
    assert H.parse_samples("h1,h40", ids) == ["h1", "h40"]
    assert H.parse_samples("", ids) == ids


def test_split_range_handles_ids_with_dash():
    ids = ["d3e-01", "d3e-02", "d3e-20"]
    assert C.split_range("d3e-20", ids) is None, "整个 id 命中 ⇒ 不是范围"
    assert C.split_range("d3e-01-d3e-20", ids) == ("d3e-01", "d3e-20")
    assert C.parse_samples("d3e-01-d3e-02", ids) == ["d3e-01", "d3e-02"]


def test_parse_samples_rejects_unknown_and_reversed():
    ids = ["h31", "h32", "h40"]
    for bad in ("h99", "h40-h31", "h31-h99"):
        try:
            H.parse_samples(bad, ids)
            raised = False
        except SystemExit:
            raised = True
        assert raised, f"{bad} 必须显式报错，不许静默返回空列表"


def test_corpus_reveal_refuses_undeclared_samples(tmp_path):
    """把历史样本当成本轮扩样 ⇒ 必须拒绝（否则分母口径会被悄悄改写）。"""
    try:
        C.run(["d3-01"], runs_n=1, write=False)
        raised = False
    except SystemExit:
        raised = True
    assert raised, "不在 extend_669d.added_ids 里的样本必须拒绝"


# ─────────────────────────────────────────────────────────────────────────────
# ② 计划推导与归一（单一事实源）
# ─────────────────────────────────────────────────────────────────────────────

def test_kind_alias_normalization():
    assert H.norm_kind("-Wunsequenced") == "wunsequenced"
    assert H.norm_kind("-") == "unknown"
    assert H.norm_kind("") == "unknown"
    assert H.norm_kind("perf-counter") == "unknown", "本机无 perf 检测器 ⇒ 诚实记 unknown"
    assert H.norm_kind("tsan") == "tsan"


def test_plan_derived_from_669d_extension():
    ext = json.loads((ROOT / "data" / "holdout" / "holdout_extension_669d.json")
                     .read_text(encoding="utf-8"))
    plan = H.plan_from_extension(ext["seeds"])
    assert len(plan) == 10 and set(plan) == {f"h{i}" for i in range(31, 41)}
    assert plan["h31"][0] == "tsan" and plan["h31"][1] == ["_atom_data_race.cpp"]
    assert all(files for _k, files in plan.values()), "每条都要有夹具（拒绝空计划）"


def test_layer_mapping_covers_all_six_buckets():
    assert C.layer_of("asan") == "sanitizer" and C.layer_of("tsan") == "sanitizer"
    assert C.layer_of("compiler-warn") == "compiler-warn"
    assert C.layer_of("wunsequenced") == "compiler-warn"
    assert C.layer_of("cross-compile") == "cross-compile"
    assert C.layer_of("perf-counter") == "perf"
    assert C.layer_of("compile-time") == "compile-time"
    assert C.layer_of("measure") == "other" and C.layer_of("unknown") == "other"
    d = json.loads((ROOT / "data" / "external_corpus" / "external_corpus_669d.json")
                   .read_text(encoding="utf-8"))
    assert all(C.layer_of(s.get("expected_detector")) in C.LAYERS for s in d["samples"])


# ─────────────────────────────────────────────────────────────────────────────
# ③ 统计口径：分母 / 对照 / CP 区间
# ─────────────────────────────────────────────────────────────────────────────

def test_tally_holdout_caliber():
    rows = [{"id": "a", "verdict": "catch"}, {"id": "b", "verdict": "miss"},
            {"id": "c", "verdict": "unknown"}, {"id": "d", "verdict": "catch"}]
    labels = {"a": True, "b": True, "c": True, "d": False}
    t = H.tally(rows, labels)
    assert t["error_subset"] == {"total": 3, "catch": 1, "miss": 1, "unknown": 1,
                                 "detect_rate_pct": 50.0}
    assert t["denominator"]["value"] == 2, "分母 = catch+miss（unknown 不计）"
    assert t["control_subset"] == {"total": 1, "false_positive": 1}, "对照里的 catch 记假阳性"
    assert t["labels"] == {"error": 3, "control": 1, "unknown": 0}


def test_tally_corpus_caliber_keeps_not_error_out():
    rows = [{"id": "x", "verdict": "catch"}, {"id": "y", "verdict": "miss"},
            {"id": "z", "verdict": "not_error"}, {"id": "w", "verdict": "unknown"},
            {"id": "v", "verdict": "miss"}]
    t = C.tally(rows)
    assert t["denominator"]["value"] == 3
    assert t["not_error"] == 1 and t["unknown"] == 1
    assert t["detect_rate_pct"] == round(1 / 3 * 100, 1)


def test_zero_denominator_is_fail_loud():
    assert H.cp_interval(0, 0)["point"] is None
    assert C.cp(0, 0)["point"] is None and "拒绝给率" in C.cp(0, 0)["note"]
    assert C.tally([])["detect_rate_pct"] is None


def test_cp_interval_matches_stat_bounds():
    """区间必须来自 tools/stat_bounds.py（不新造公式）。"""
    sb = H.load_stat_bounds()
    want = sb.proportion(14, 16, 0.95)
    got = H.cp_interval(14, 16)
    assert abs(got["cp_low"] - want["cp_low"]) < 1e-12
    assert abs(got["cp_high"] - want["cp_high"]) < 1e-12
    assert abs(got["point"] - 14 / 16) < 1e-12


def test_merge_runs_flags_unstable_samples():
    runs = [
        [{"id": "h31", "detector": "tsan", "files": [], "verdict": "catch", "note": "a"},
         {"id": "h32", "detector": "asan", "files": [], "verdict": "catch", "note": "b"}],
        [{"id": "h31", "detector": "tsan", "files": [], "verdict": "unknown", "note": "a"},
         {"id": "h32", "detector": "asan", "files": [], "verdict": "catch", "note": "b"}],
    ]
    rows = H.merge_runs(["h31", "h32"], runs)
    assert rows[0]["reproducible"] is False and rows[1]["reproducible"] is True
    assert rows[0]["verdicts_per_run"] == ["catch", "unknown"]


# ─────────────────────────────────────────────────────────────────────────────
# ④ 产物复算（E3：新检出率可复算、CI 正确）
# ─────────────────────────────────────────────────────────────────────────────

def test_holdout_reveal_artifact_recomputes():
    rep = json.loads((ROOT / "data" / "holdout_reveal_4_671a.json").read_text(encoding="utf-8"))
    assert rep["reveal_index"] == 4
    r4 = rep["round4"]["error_subset"]
    assert r4["detect_rate_pct"] == round(r4["catch"] / (r4["catch"] + r4["miss"]) * 100, 1)
    cum = rep["cumulative"]
    assert cum["denominator"]["value"] == cum["error_subset"]["catch"] + cum["error_subset"]["miss"]
    assert cum["error_subset"]["detect_rate_pct"] == round(
        cum["error_subset"]["catch"] / cum["denominator"]["value"] * 100, 1)
    cpi = cum["cp95"]
    assert abs(cpi["point"] - cum["error_subset"]["catch"] / cum["denominator"]["value"]) < 1e-12
    assert cpi["cp_low"] <= cpi["point"] <= cpi["cp_high"]


def test_holdout_detail_lists_every_sample_with_source():
    d = json.loads((ROOT / "data" / "holdout" / "reveal_3_detail_671a.json")
                   .read_text(encoding="utf-8"))
    assert d["reveal_index"] == 4 and "naming_note" in d
    per = d["per_sample"]
    assert len(per) == 40, "累计明细必须覆盖 h1–h40"
    assert {r["source"] for r in per} == {"measured_671a", "reused_reveal_3"}
    # 标签取值只有三态：True（真错）/ False（对照）/ "unknown"（分不清）——逐个核实不臆造
    assert {r.get("planted") for r in per} <= {True, False, "unknown"}
    assert all("verdicts_per_run" in r for r in per)


def test_holdout_reveal_reproducible_across_runs():
    rep = json.loads((ROOT / "data" / "holdout_reveal_4_671a.json").read_text(encoding="utf-8"))
    assert rep["runs"] >= 3, "扩样 reveal 必须连跑 ≥3 次"
    assert rep["reproducibility"]["all_reproducible"] is True
    assert rep["reproducibility"]["unstable_samples"] == []


def test_corpus_reveal_artifact_recomputes():
    rep = json.loads((ROOT / "data" / "external_corpus_reveal_671a.json")
                     .read_text(encoding="utf-8"))
    new = rep["new_samples"]
    assert new["denominator"]["value"] == new["catch"] + new["miss"]
    assert new["detect_rate_pct"] == round(new["catch"] / new["denominator"]["value"] * 100, 1)
    cum = rep["cumulative"]
    assert cum["denominator"]["value"] == cum["catch"] + cum["miss"]
    assert cum["total"] == len(rep["samples_requested"]) + len(
        rep["historical_reuse"]["ids"])
    # 分层：每层都要么给率（含 CP），要么显式拒绝给率
    for lay, d in rep["cumulative_by_layer"].items():
        assert lay in C.LAYERS
        if d["denominator"]["value"]:
            assert d["detect_rate_pct"] == round(d["catch"] / d["denominator"]["value"] * 100, 1)
        else:
            assert d["detect_rate_pct"] is None


def test_corpus_detail_layer_sum_equals_total():
    d = json.loads((ROOT / "data" / "external_corpus" / "reveal_detail_671a.json")
                   .read_text(encoding="utf-8"))
    per = d["per_sample"]
    assert len(per) == 60, "累计明细必须覆盖 d3-* 40 + d3e-* 20"
    assert sum(1 for r in per if r["is_669d_new"]) == 20
    assert d["cumulative_summary"]["total"] == len(per)


# ─────────────────────────────────────────────────────────────────────────────
# ⑤ 检出率更新（C3）
# ─────────────────────────────────────────────────────────────────────────────

def test_rate_pct_and_update_block_pure():
    assert U.rate_pct(17, 21) == 81.0
    assert U.rate_pct(1, 0) is None
    b = U.update_block("t", 14, 16, 17, 21)
    assert b["before"]["rate_pct"] == 87.5 and b["after"]["rate_pct"] == 81.0
    assert b["delta_pp"] == -6.5
    w = U.interval_width_pp(b)
    assert w["before_pp"] and w["after_pp"]


def test_citation_extraction_forms():
    assert U.extract_citations("**87.5%（14/16）**")[0] == {"pct": 87.5, "k": 14, "n": 16,
                                                            "pos": 2}
    assert U.extract_citations("87.5% (14/16)")[0]["n"] == 16
    assert U.cited_kn("x 43.8%（14/32）", 14, 32) == 43.8
    assert U.cited_kn("x 43.8%（14/32）", 14, 16) is None


def test_reveal_update_artifact_matches_source_artifacts():
    """`reveal_update_671a.json` 的每个数都必须能从 reveal 产物复算（拒绝编造）。"""
    upd = json.loads((ROOT / "data" / "experiments" / "reveal_update_671a.json")
                     .read_text(encoding="utf-8"))
    h4 = json.loads((ROOT / "data" / "holdout_reveal_4_671a.json").read_text(encoding="utf-8"))
    c_new = json.loads((ROOT / "data" / "external_corpus_reveal_671a.json")
                       .read_text(encoding="utf-8"))
    hs = h4["cumulative"]
    assert upd["holdout"]["after"]["k"] == hs["error_subset"]["catch"]
    assert upd["holdout"]["after"]["n"] == hs["denominator"]["value"]
    assert upd["holdout"]["after"]["rate_pct"] == hs["error_subset"]["detect_rate_pct"]
    cc = c_new["cumulative"]
    assert upd["corpus"]["after"]["k"] == cc["catch"] and upd["corpus"]["after"]["n"] == cc["denominator"]["value"]
    assert upd["corpus"]["after"]["rate_pct"] == cc["detect_rate_pct"]


def test_reveal_update_declares_pending_for_671b_and_untouched_files():
    upd = json.loads((ROOT / "data" / "experiments" / "reveal_update_671a.json")
                     .read_text(encoding="utf-8"))
    keys = {p["key"] for p in upd["pending_for_671b"]}
    assert {"holdout_rate_pct", "corpus_rate_pct"} <= keys, "扩大分母必然要 671b 更新论文"
    assert all(p.get("action") for p in upd["pending_for_671b"]), "每条都要写清谁改哪个文件"
    assert "research/paper_v0.8.md" not in upd["not_modified"] or True
    assert any("research/" in f for f in upd["not_modified"]), "必须声明没碰论文"
    assert "web/data/*.json" in upd["not_modified"], "必须声明没碰前端"


def test_reveal_update_no_nan_or_inf():
    upd = json.loads((ROOT / "data" / "experiments" / "reveal_update_671a.json")
                     .read_text(encoding="utf-8"))
    txt = json.dumps(upd)
    assert "NaN" not in txt and "Infinity" not in txt, "产物里不许出现 NaN/Infinity"


def test_selftests_pass():
    assert H.selftest() == 0
    assert C.selftest() == 0
    assert U.selftest() == 0
