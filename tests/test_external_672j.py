# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""672j W5 外部锚定测试（≥20 条断言）：数据集来源可复核 + 产物口径 + 预注册判定。"""
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


def _j(rel: str):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))


A = _load("tools/external_anchor_672j.py")
F = _load("tools/external_anchor_fetch_672j.py")


# ── 数据集：来源与可复核性 ───────────────────────────────────────────────────
def test_dataset_counts_and_ids():
    ds = _j("data/external_anchor/external_anchor_672j.json")
    assert ds["schema"] == "queyi-external-anchor/672j"
    assert ds["counts"] == {"total": 50, "guideline_bad_verbatim": 35, "ub_reconstructed": 15}
    ids = [s["id"] for s in ds["samples"]]
    assert len(ids) == len(set(ids)) == 50
    assert ds["prereg"] == "data/experiments/prereg_672j.json"


def test_verbatim_subset_is_traceable():
    ds = _j("data/external_anchor/external_anchor_672j.json")
    va = [s for s in ds["samples"] if s["subset"] == "guideline_bad_verbatim"]
    assert len(va) == 35
    # 每条都要能凭 URL + 文档 sha + 代码 sha 复核
    assert all(s["source_url"].startswith("https://raw.githubusercontent.com/isocpp/") for s in va)
    assert all(len(s["source_doc_sha256"]) == 64 and len(s["code_sha256"]) == 64 for s in va)
    assert all(s["verbatim"] is True for s in va)
    assert len({s["rule_id"] for s in va}) == 35, "同一规则只取一条"
    assert all(s.get("rule_id", "").count(".") == 1 for s in va)
    # 抓取元数据必须落盘（时间 + 字节 + sha）
    assert len(ds["source"]["sha256"]) == 64 and ds["source"]["bytes"] > 100000
    assert ds["source"]["fetched_at"]


def test_reconstructed_subset_labeled_honestly():
    ds = _j("data/external_anchor/external_anchor_672j.json")
    rb = [s for s in ds["samples"] if s["subset"] == "ub_reconstructed"]
    assert len(rb) == 15
    assert all(s["verbatim"] is False and s["verified_source"] is False for s in rb)
    assert all(s["citation"] for s in rb)
    assert all(s["source_url"] is None for s in rb)


def test_harness_and_filter_deviations_registered():
    ds = _j("data/external_anchor/external_anchor_672j.json")
    assert "prelude_v1" in ds["harness"]["subset_a"]
    assert "deviation_from_prereg" in ds["harness"]          # 方法补充必须登记
    cf = ds["compilability_filter"]
    assert cf["scanned_unique_rules"] >= 35
    assert isinstance(cf["skipped_uncompilable_rules"], list) and cf["skipped_uncompilable_rules"]
    # verbatim 样本必须逐条记录 harness
    va = [s for s in ds["samples"] if s["subset"] == "guideline_bad_verbatim"]
    assert all("prelude_v1" in (s.get("harness") or "") for s in va)


def test_detector_mapping_is_mechanical():
    # 含 thread → tsan；有 main → asan+ubsan；片段 → compiler-warn
    assert F.detect_mapping("#include <thread>\nint main(){}")[0] == ["tsan"]
    assert F.detect_mapping("int main(){return 0;}")[0] == ["asan", "ubsan"]
    assert F.detect_mapping("void f(){}")[0] == ["compiler-warn"]
    ds = _j("data/external_anchor/external_anchor_672j.json")
    legal = {"asan", "ubsan", "tsan", "compiler-warn", "cross-compile"}
    assert all(set(s["expected_detectors"]) <= legal and s["expected_detectors"]
               for s in ds["samples"])
    assert all(s.get("detector_note") for s in ds["samples"])


# ── 揭示产物与统计 ───────────────────────────────────────────────────────────
def test_reveal_product_shape():
    r = _j("data/external_anchor_reveal_672j.json")
    assert r["schema"] == "queyi-external-anchor-reveal/672j"
    assert r["total"]["denominator"]["value"] + r["total"]["unknown"] == 50
    assert r["subset_a_guideline_verbatim"]["total"] == 35
    assert r["subset_b_ub_reconstructed"]["total"] == 15
    # 两部分分母之和 = 总分母（不混算但可加）
    assert (r["subset_a_guideline_verbatim"]["denominator"]["value"]
            + r["subset_b_ub_reconstructed"]["denominator"]["value"]
            == r["total"]["denominator"]["value"])
    assert r["total"]["cp95"]["k"] == r["total"]["catch"]


def test_reveal_verdicts_consistency():
    r = _j("data/external_anchor_reveal_672j.json")
    for blk in (r["subset_a_guideline_verbatim"], r["subset_b_ub_reconstructed"], r["total"]):
        assert blk["catch"] + blk["miss"] + blk["unknown"] == blk["total"]
        if blk["denominator"]["value"]:
            assert abs(blk["rate_pct"] - blk["catch"] / blk["denominator"]["value"] * 100) < 0.06
    # 逐样本判决与 per_detector 一致（catch 蕴含至少一个检测器 catch）
    for row in r["per_sample"]:
        if row["verdict"] == "catch":
            assert "catch" in row["per_detector"], row["id"]
        if row["verdict"] == "miss":
            assert "catch" not in row["per_detector"], row["id"]
    assert r["reproducibility"]["unstable"] == []


def test_hypothesis_verdicts_match_numbers():
    r = _j("data/external_anchor_reveal_672j.json")
    h = r["hypothesis_verdicts"]
    delta = r["compare"]["diff_vs_corpus_pp"]
    assert delta is not None
    assert (h["H1_corpus_minus_guideline_gt_10pp"] == "成立") == (delta > 10)
    assert r["subset_a_guideline_verbatim"]["rate_pct"] < r["compare"]["corpus_672h"]["rate_pct"]
    assert r["subset_b_ub_reconstructed"]["rate_pct"] > r["compare"]["corpus_hist_reference_pct"]
    assert (h["H3_total_rate_ge_30pct"] == "成立") == (r["total"]["rate_pct"] >= 30)


def test_newcombe_impl_sanity():
    lo, hi = A.newcombe_diff(34, 41, 10, 35)
    d = 34 / 41 - 10 / 35
    assert lo < d < hi
    assert -1.0 <= lo <= hi <= 1.0
    lo2, hi2 = A.newcombe_diff(0, 0, 5, 10)
    assert lo2 <= hi2
    lo3, hi3 = A.newcombe_diff(1, 1, 0, 1)
    assert lo3 <= hi3


def test_tally_excludes_unknown():
    rows = [{"id": "a", "verdict": "catch"}, {"id": "b", "verdict": "unknown"},
            {"id": "c", "verdict": "miss"}]
    t = A.tally(rows)
    assert t["denominator"]["value"] == 2 and t["unknown"] == 1
    assert t["rate_pct"] == 50.0 and t["cp95"]["n"] == 2


def test_prereg_672j_locked():
    p = _j("data/experiments/prereg_672j.json")
    assert p["status"] == "locked_before_experiment"
    assert p["methods"]["dataset"]["subset_a_verbatim"]["n_target"] == 35
    assert p["methods"]["dataset"]["subset_b_reconstructed"]["n_target"] == 15
    # 源可得性必须如实登记（只有 Core Guidelines 可取）
    assert "403" in p["context"]["source_availability"]["cppreference"]
    assert "403" in p["context"]["source_availability"]["stackoverflow"]
    assert p["decision_thresholds"]["H1"].startswith("Δ = corpus率 − 准则例率 > 10pp")
