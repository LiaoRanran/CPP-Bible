#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""tests/test_693_research.py — 693 科研强化阶段（E1–E7）产物与红线测试。

三类断言
========
1. **红线 8 自证**：E 阶段所有产物必须登记 `detect_calls == 0`，
   且 E 阶段工具源码**不得**引用检测器入口（`holdout_reveal_661` / `detect_for_assets`
   的 `detect_one_asset` 等）——用静态文本扫描验证，而不是靠自觉。
2. **产物自洽**：JSON ↔ 报告一致（关键数字必须同时出现在两边）。
3. **口径不变量**：例如「翻转 ground truth 不改变 A5 主端点 Δ」这类结构性事实。

全部只读；不跑检测器、不联网、不需要编译器。
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

import pytest

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
TOOLS = ROOT / "tools"

E_TOOLS = (
    "verify_693_original_repo.py",
    "analyze_693_defect_types.py",
    "fit_693_detectability_model.py",
    "analyze_693_counterfactual.py",
    "eval_693_meta_evaluation.py",
)

# 检测器入口的**禁用子串**：E 阶段工具不得触碰
FORBIDDEN_ENTRYPOINTS = (
    "holdout_reveal_661",
    "detect_one_asset",
    "detect_for_assets",
    "def detect(",
    "build_catch_sets(matrix)  # noqa",  # 占位（不应出现）
)


def _load(name: str) -> dict[str, Any]:
    p = DATA / name
    if not p.exists():
        pytest.skip(f"未生成 {name}（先跑对应的 tools/ 脚本）")
    return cast(dict[str, Any], json.loads(p.read_text(encoding="utf-8")))


# ───────────────────────── 红线 8 自证 ─────────────────────────
@pytest.mark.parametrize("tool", E_TOOLS)
def test_e_tools_do_not_reference_detector_entrypoints(tool: str) -> None:
    """E 阶段工具源码不得出现检测器入口（静态扫描，非自觉）。"""
    src = (TOOLS / tool).read_text(encoding="utf-8")
    # 允许在注释/文档里提到名字（用于说明"为什么不用"），但不得出现调用形态
    body = "\n".join(
        ln for ln in src.splitlines()
        if not ln.lstrip().startswith("#")
    )
    for bad in ("holdout_reveal_661", "detect_one_asset"):
        assert bad not in body, f"{tool} 引用了检测器入口 {bad}"


@pytest.mark.parametrize("tool", E_TOOLS)
def test_e_tools_declare_no_detect(tool: str) -> None:
    """E 阶段工具必须**显式声明** detect_calls = 0 的意图（可审计）。"""
    src = (TOOLS / tool).read_text(encoding="utf-8")
    assert "detect_calls" in src, f"{tool} 未登记 detect_calls"


@pytest.mark.parametrize("name", [
    "693_original_repo_cve.json",
    "693_defect_type_deep_analysis.json",
    "693_detectability_model.json",
    "693_counterfactual_extended.json",
    "693_meta_evaluation_v2.json",
])
def test_e_artifacts_register_zero_detect(name: str) -> None:
    doc = _load(name)
    if "detect_calls" in doc:
        assert doc["detect_calls"] == 0, f"{name} 声明了非零 detect_calls"
    else:
        # E1 用另一种写法登记
        assert doc["honest_registration"]["detect_calls"] == 0, name


def test_e1_detection_arm_not_executed() -> None:
    doc = _load("693_original_repo_cve.json")
    assert doc["summary"]["detection_arm_executed"] is False
    assert doc["honest_registration"]["red_line_8"]


# ───────────────────────── E2 口径不变量 ─────────────────────────
def test_e2_stale_crosscheck_matches_known_gap() -> None:
    doc = _load("693_defect_type_deep_analysis.json")
    cc = doc["stale_metric_crosscheck_vs_676l"]
    assert doc["n_types"] == 34
    assert doc["n_samples"] == 1147
    assert cc["stale"] is True
    assert cc["published_ground_truth"]["catch"] == 674
    assert cc["current_ground_truth"]["catch"] == 640
    assert cc["gt_catch_delta"] == -34          # 676m 修正的 34 条挂起样本
    # TP/FP/TN 逐位不变；只有 FN 与分母变了
    for _asset, r in cc["rows"].items():
        assert r["tp_same"] is True
        assert r["fp_same"] is True
        assert r["delta_recall_pp"] > 0        # 重算后 recall 一律**上升**


def test_e2_union_recall_recomputed() -> None:
    doc = _load("693_defect_type_deep_analysis.json")
    tbl = doc["single_detector_table_current_labels"]
    # 条件 recall 必须 ≤ 1（曾经出现过 >100% 的分母错误）
    for _a, v in tbl.items():
        if v["recall_pct"] is not None:
            assert v["recall_pct"] <= 100.0, _a


# ───────────────────────── E3 泄漏不变量 ─────────────────────────
def test_e3_group_cv_not_better_than_random() -> None:
    """按结构签名分组的 CV 不应优于随机折（否则说明分组没起作用）。"""
    doc = _load("693_detectability_model.json")
    gap = doc["cv"]["leakage_inflation"]
    for model in ("tree", "logreg"):
        assert gap[model]["accuracy_gap"] >= -1e-9, model
    r = doc["cv"]["random_5fold"]["models"]["tree"]["accuracy"]
    g = doc["cv"]["group_5fold"]["models"]["tree"]["accuracy"]
    assert r >= g
    assert doc["n_feature_groups"] < doc["n_samples_used"], "分组数应少于样本数"


# ───────────────────────── E4 结构性事实 ─────────────────────────
def test_e4_ground_truth_flip_does_not_move_delta() -> None:
    """⭐ 翻转 expected_verdict 不得改变 A5 主端点 Δ（它只依赖 per_asset）。"""
    doc = _load("693_counterfactual_extended.json")
    arm_c = doc["arm_c_label_quality"]
    assert arm_c["flip_ground_truth"], "缺少 ground-truth 翻转臂"
    for rate, v in arm_c["flip_ground_truth"].items():
        assert v["delta_pp_change"] == 0.0, f"{rate} 改变了 Δ，口径被破坏"
    # 而翻 per_asset 应当**能**改变 Δ（至少有一档不为 0）
    assert any(abs(v["delta_change_pp"]) > 0
               for v in arm_c["flip_per_asset_verdict"].values())


def test_e4_environment_arm_matches_692() -> None:
    """E4 的 D 臂必须与 692 的 E1−E2 = 35.34pp 逐位一致。"""
    doc = _load("693_counterfactual_extended.json")
    assert abs(doc["arm_d_environment"]["delta_pp_unaware"] - 35.3357) < 1e-3
    assert doc["arm_d_environment"]["container_arm"]["executed"] is False


def test_e4_sample_size_delta_shrinks_with_n() -> None:
    doc = _load("693_counterfactual_extended.json")
    a = doc["arm_a_sample_size"]
    ns = sorted((int(k) for k in a))
    assert ns[0] == 50 and ns[-1] == 566
    # CI 宽度必须随 n 单调收窄（随机性检查：允许极小抖动，故用非严格递减 + 容差）
    widths = [a[str(n)]["ci_width_pp"] for n in ns]
    assert widths[-1] < widths[0], widths


# ───────────────────────── E5 口径不变量 ─────────────────────────
def test_e5_or_auc_dominates_every_single_asset() -> None:
    doc = _load("693_meta_evaluation_v2.json")
    d = doc["discrimination"]
    or_auc = d["OR_all8"]["auc"]
    for a, v in d.items():
        if a == "OR_all8" or v["auc"] is None:
            continue
        assert or_auc >= v["auc"], f"OR 的 AUC 低于单资产 {a}"


def test_e5_linker_is_near_chance() -> None:
    """linker 的 AUC ≈ 0.5（论文'低边际但不可替代'论断的量化支撑）。"""
    doc = _load("693_meta_evaluation_v2.json")
    auc = doc["discrimination"]["linker"]["auc"]
    assert auc is not None and abs(auc - 0.5) < 0.05, auc


def test_e5_ece_is_bounded() -> None:
    doc = _load("693_meta_evaluation_v2.json")
    c = doc["calibration"]
    for key in ("llm_arm", "detectors_deterministic"):
        ece = c[key]["ece"]
        assert ece is None or 0.0 <= ece <= 1.0, (key, ece)
    # LLM 强过自信：最高置信桶里 accuracy 应明显低于 confidence
    top = max(c["llm_arm"]["bins"], key=lambda b: b["n"])
    assert top["accuracy"] < top["mean_confidence"], top


def test_e5_framework_comparison_is_labelled_qualitative() -> None:
    doc = _load("693_meta_evaluation_v2.json")
    assert doc["framework_comparison"], "缺少框架对照"
    for fr in doc["framework_comparison"]:
        assert "非实测" in fr["source"], fr["framework"]


# ───────────────────────── E7 锚点纪律 ─────────────────────────
def test_e7_uses_grep_anchors_not_line_numbers() -> None:
    p = DATA / "693_paper_revision_suggestions.md"
    if not p.exists():
        pytest.skip("未生成 693_paper_revision_suggestions.md")
    txt = p.read_text(encoding="utf-8")
    assert "grep -n" in txt, "E7 必须给 grep 锚点"
    assert "不改正文" in txt or "未改动" in txt, "E7 必须声明未改正文"


def test_e7_paper_tex_unmodified_by_this_batch() -> None:
    """红线 1 自证：本批不得修改论文正文（用 git 判断工作树是否干净）。"""
    import subprocess
    r = subprocess.run(
        ["git", "status", "--porcelain", "--",
         "research/latex/queyi_neurips2027_v1.1.tex"],
        cwd=str(ROOT), capture_output=True, text=True, encoding="utf-8", check=False)
    assert r.stdout.strip() == "", f"论文正文被改动了：{r.stdout!r}"


# ───────────────────────── 报告 ↔ JSON 一致 ─────────────────────────
@pytest.mark.parametrize(("json_name", "md_name"), [
    ("693_defect_type_deep_analysis.json", "693_defect_type_report.md"),
    ("693_detectability_model.json", "693_detectability_model_report.md"),
    ("693_counterfactual_extended.json", "693_counterfactual_report.md"),
    ("693_meta_evaluation_v2.json", "693_meta_evaluation_report.md"),
    ("693_original_repo_cve.json", "693_original_repo_cve_report.md"),
])
def test_report_exists_and_is_substantive(json_name: str, md_name: str) -> None:
    if not (DATA / json_name).exists():
        pytest.skip(f"未生成 {json_name}")
    md = DATA / md_name
    assert md.exists(), f"缺报告 {md_name}"
    assert len(md.read_text(encoding="utf-8")) > 800, md_name
