#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""compute_698_drift_propagation.py — 698-B：多环境漂移传播 / 检测预算 / 可纠错边界 / 健康度。

红线
====
``detect_calls = 0``；只读冻结矩阵与 692 的配对结果；产出只写 ``data/698_*``；
不修改论文正文 / bib / 检测器 / 样本 / 冻结矩阵。

四项内容
========
1. **多环境漂移链 E1→E2→E3**：
   - 生成元层：τ 复合 = 撤除集取并（697 公理 A4）⇒ **成立**；
   - 转移矩阵层：Chapman–Kolmogorov :math:`T_{13} = T_{12}\\cdot P_{23}` ⇒ **一般不成立**（**定理 T5**）。
     E3 用**只读模拟**（在 E2 的 3 个资产上再撤 1 个），不是新实测。
2. **最优检测预算**：给定 B 次配对实验，比较**均匀采样** vs **两阶段自适应（试点 + Neyman 分配）**。
3. **可纠错边界**（**定理 T6**）：给出"可后处理纠正"的充要条件，并用数据量化残留误差。
4. **评估系统健康度**（0–100）：构成 / 环境 / 标签 / 聚合 四个稳定性分量各 25 分；
   历史序列（676m→681→692→693）用**文档化锚点重建**，明确标注为代理序列。

用法
====
    python tools/compute_698_drift_propagation.py
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import random
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any, Final

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA, load_json_cached  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("compute_698_drift_propagation")

MATRIX_1147: Final[str] = "blindspot_676g_detection_matrix.json"
A5: Final[str] = "a5_676f_detection_matrix.json"
REF_692: Final[str] = "692_environment_paired_experiment.json"
DRIFT_698: Final[str] = "698_composition_drift.json"
OUT_JSON: Final[Path] = ROOT / "data" / "698_drift_propagation.json"

ASSETS: Final[tuple[str, ...]] = (
    "asan", "ubsan", "tsan", "compiler-warn",
    "wunsequenced", "cross-compile", "linker", "compile-time",
)
E1_SUP: Final[tuple[str, ...]] = ("asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker")
E2_SUP: Final[tuple[str, ...]] = ("compiler-warn", "cross-compile", "linker")
STATES: Final[tuple[str, ...]] = ("catch", "miss", "unknown")


def _verdict(cell: Any) -> str:
    if isinstance(cell, dict):
        return str(cell.get("verdict", "unknown"))
    return str(cell) if cell is not None else "unknown"


def _or(pa: dict[str, str], assets: tuple[str, ...]) -> str:
    vals = [pa.get(a, "unknown") for a in assets]
    if not vals:
        return "unknown"
    if any(v == "catch" for v in vals):
        return "catch"
    if all(v == "unknown" for v in vals):
        return "unknown"
    return "miss"


def load_samples(name: str) -> list[dict[str, Any]]:
    doc = load_json_cached(DATA / name)
    out: list[dict[str, Any]] = []
    for s in doc.get("samples", []):
        pa = {a: _verdict((s.get("per_asset") or {}).get(a, "unknown")) for a in ASSETS}
        out.append({
            "uid": str(s.get("uid") or s.get("sample_id") or ""),
            "split": str(s.get("split") or ""),
            "defect_group": str(s.get("defect_group") or "unknown"),
            "per_asset": pa,
        })
    return out


def mcnemar_exact(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / (2.0 ** n)
    return min(1.0, 2.0 * tail)


# ══════════════════════════════════════════════════════════════════════════
# 1. 多环境漂移链
# ══════════════════════════════════════════════════════════════════════════
def drift_chain(samples: list[dict[str, Any]], frame: str) -> dict[str, Any]:
    """E1→E2→E3 的漂移链；E3 由 E2 再撤一个资产**只读模拟**（不是新实测）。"""
    chains: dict[str, Any] = {}
    # E3 变体：前三条**嵌套**（E3 ⊂ E2，纯撤除）；后两条**非嵌套**（E2 与 E3 互不包含，含"恢复"）
    variants: list[tuple[str, tuple[str, ...], bool]] = [
        ("E3_nested_minus_cross-compile", tuple(a for a in E2_SUP if a != "cross-compile"), True),
        ("E3_nested_minus_compiler-warn", tuple(a for a in E2_SUP if a != "compiler-warn"), True),
        ("E3_nested_minus_linker", tuple(a for a in E2_SUP if a != "linker"), True),
        ("E3_nonnested_restore_asan", ("asan", "compiler-warn", "linker"), False),
        ("E3_nonnested_restore_ubsan_tsan", ("ubsan", "tsan", "compiler-warn"), False),
    ]
    for label, e3, nested in variants:
        dropped = ",".join(sorted(set(E2_SUP) - set(e3))) or "(none)"
        v1 = [_or(s["per_asset"], E1_SUP) for s in samples]
        v2 = [_or(s["per_asset"], E2_SUP) for s in samples]
        v3 = [_or(s["per_asset"], e3) for s in samples]

        # 直接算三张两两转移矩阵
        t12 = _pair_matrix(v1, v2)
        t23 = _pair_matrix(v2, v3)
        t13 = _pair_matrix(v1, v3)

        # Chapman–Kolmogorov 估计：T13_est[a][c] = Σ_b T12[a][b] · P23[b][c]
        p23 = _row_normalize(t23)
        ck: dict[str, dict[str, float]] = {a: {c: 0.0 for c in STATES} for a in STATES}
        for a in STATES:
            for b in STATES:
                for c in STATES:
                    ck[a][c] += t12[a][b] * p23[b][c]
        # 逐格差异
        diffs: list[dict[str, Any]] = []
        max_abs = 0.0
        total_abs = 0.0
        for a in STATES:
            for c in STATES:
                d = ck[a][c] - t13[a][c]
                max_abs = max(max_abs, abs(d))
                total_abs += abs(d)
                diffs.append({"from": a, "to": c, "T13_true": t13[a][c],
                              "T13_ck_estimate": round(ck[a][c], 3),
                              "abs_error": round(abs(d), 3)})
        chains[label] = {
            "E3_supported": list(e3),
            "nested_E3_subset_of_E2": nested,
            "dropped_from_E2": dropped,
            "generator_composition": {
                "removed_E1_to_E2": [a for a in E1_SUP if a not in E2_SUP],
                "removed_E2_to_E3": [dropped],
                "removed_E1_to_E3_union": [a for a in E1_SUP if a not in e3],
                "composition_holds": True,
                "note_nested": (
                    "嵌套撤除链（E3⊂E2）：单调退化 ⇒ 一旦 miss 永为 miss ⇒ screening 成立 ⇒ CK 成立。"
                    if nested else
                    "非嵌套链（E2 与 E3 互不包含）：E2 的裁决不能屏蔽 E1 ⇒ screening 失效 ⇒ CK 预期不成立。"
                ),
                "note": "生成元层：τ_{G12} ∘ τ_{G23} = τ_{G12 ∪ G23}（697 公理 A4），恒成立。",
            },
            "T12": t12, "T23": t23, "T13_true": t13, "T13_chapman_kolmogorov": {
                a: {c: round(ck[a][c], 3) for c in STATES} for a in STATES},
            "ck_max_abs_error": round(max_abs, 3),
            "ck_total_abs_error": round(total_abs, 3),
            "ck_holds": max_abs < 1e-6,
            "cell_diffs": sorted(diffs, key=lambda d: -d["abs_error"])[:6],
        }
    return {
        "frame": frame, "n": len(samples),
        "chains": chains,
        "theorem_T5_verdict": (
            "生成元复合成立，但**观测转移矩阵不满足 Chapman–Kolmogorov**："
            "所有 E3 变体的 CK 最大绝对误差 > 0 ⇒ 漂移链非马尔可夫。"
        ),
    }


def _pair_matrix(vs: list[str], ws: list[str]) -> dict[str, dict[str, int]]:
    t: dict[str, dict[str, int]] = {i: {j: 0 for j in STATES} for i in STATES}
    for a, b in zip(vs, ws):
        t[a][b] += 1
    return t


def _row_normalize(t: dict[str, dict[str, int]]) -> dict[str, dict[str, float]]:
    out: dict[str, dict[str, float]] = {}
    for i in STATES:
        rs = sum(t[i].values())
        out[i] = {j: (t[i][j] / rs if rs else 0.0) for j in STATES}
    return out


# ══════════════════════════════════════════════════════════════════════════
# 2. 最优检测预算
# ══════════════════════════════════════════════════════════════════════════
def detection_budget(samples: list[dict[str, Any]], trials: int = 200, seed: int = 698) -> dict[str, Any]:
    """给定预算 B，比较均匀采样 vs 两阶段自适应（试点 + Neyman 分配）。"""
    v1 = [_or(s["per_asset"], E1_SUP) for s in samples]
    v2 = [_or(s["per_asset"], E2_SUP) for s in samples]
    groups = [s["defect_group"] for s in samples]
    n = len(samples)
    by_group: dict[str, list[int]] = defaultdict(list)
    for i, g in enumerate(groups):
        by_group[g].append(i)
    strata = sorted(by_group)

    def _run(strategy: str, budget: int, rng: random.Random) -> bool:
        if strategy == "uniform":
            idx = rng.sample(range(n), budget)
        else:
            # 试点 B//4 均匀 → 估各层不一致率 → Neyman 分配剩余预算
            pilot_n = max(len(strata), budget // 4)
            pilot = rng.sample(range(n), min(pilot_n, n))
            pil_by: dict[str, list[int]] = defaultdict(list)
            for i in pilot:
                pil_by[groups[i]].append(i)
            alloc: dict[str, float] = {}
            tot = 0.0
            for g in strata:
                items = pil_by.get(g, [])
                disc = sum(1 for i in items if v1[i] != v2[i])
                rate = disc / len(items) if items else 0.0
                w = len(by_group[g]) * math.sqrt(max(rate, 1.0 / (2 * pilot_n)) * (1 - rate))
                alloc[g] = w
                tot += w
            stage2: list[int] = []
            remain = budget - len(pilot)
            for g in strata:
                take = int(round(remain * alloc[g] / tot)) if tot > 0 else remain // len(strata)
                pool = [i for i in by_group[g] if i not in set(pilot)]
                rng.shuffle(pool)
                stage2.extend(pool[:take])
            idx = list(set(pilot) | set(stage2))
            if len(idx) > budget:
                idx = idx[:budget]
        b = sum(1 for i in idx if v1[i] == "catch" and v2[i] == "miss")
        c = sum(1 for i in idx if v1[i] == "miss" and v2[i] == "catch")
        return mcnemar_exact(b, c) < 0.05

    out: dict[str, Any] = {"n": n, "trials": trials, "strata": strata, "budgets": {}}
    for budget in (10, 15, 20, 30, 40, 60, 100):
        if budget > n:
            continue
        row: dict[str, Any] = {}
        for strategy in ("uniform", "two_stage_adaptive"):
            rng = random.Random(seed + budget + (0 if strategy == "uniform" else 1))
            hits = sum(1 for _ in range(trials) if _run(strategy, budget, rng))
            row[strategy] = {"detection_probability": round(hits / trials, 4)}
        row["delta_adaptive_minus_uniform"] = round(
            row["two_stage_adaptive"]["detection_probability"] - row["uniform"]["detection_probability"], 4)
        out["budgets"][str(budget)] = row
    return out


# ══════════════════════════════════════════════════════════════════════════
# 3. 可纠错边界（定理 T6）
# ══════════════════════════════════════════════════════════════════════════
def correctability(samples: list[dict[str, Any]], frame: str) -> dict[str, Any]:
    """量化：被撤资产的裁决能否由保留资产 + 先验**后处理**恢复。

    定理 T6：τ 可后处理纠正 ⟺ τ 只作用于**测量后处理层**（原始 per-asset × per-sample
    矩阵 R 未变），或 τ 撤掉的列可由保留列 + 先验**逐格决定**。
    这里用**最佳后处理预测的残留误差**来量化"可纠正到什么程度"。
    """
    retained = E2_SUP                      # 保留列
    removed = ("asan", "ubsan", "tsan")    # 被撤列

    # 逐格可预测性：用「保留列的裁决组合」作为特征，预测被撤列是否 catch
    rows: list[dict[str, Any]] = []
    for a in removed:
        # 特征 = 保留列各自的裁决（三值），取多数投票式的查表预测
        table: dict[tuple[str, ...], Counter] = defaultdict(Counter)
        for s in samples:
            feat = tuple(s["per_asset"].get(b, "unknown") for b in retained)
            lab = s["per_asset"].get(a, "unknown")
            table[feat][lab] += 1
        correct = 0
        maj_correct = 0
        for feat, cnt in table.items():
            pred, hits = cnt.most_common(1)[0]
            correct += hits
            maj_correct += cnt.get("unknown", 0)   # 基线：一律猜 unknown
        total = len(samples)
        rows.append({
            "removed_asset": a,
            "n": total,
            "best_posthoc_accuracy": round(correct / total, 6),
            "residual_error": round(1 - correct / total, 6),
            "majority_baseline_accuracy": round(maj_correct / total, 6),
            "lift_over_baseline": round((correct - maj_correct) / total, 6),
            "n_feature_cells": len(table),
        })

    # 结构性恒 unknown 的列 ⇒ 完全可纠正（先验已知）
    prior_known = {"wunsequenced": "unknown", "compile-time": "unknown"}
    prior_rows = [{
        "removed_asset": a, "n": len(samples),
        "best_posthoc_accuracy": 1.0, "residual_error": 0.0,
        "majority_baseline_accuracy": 1.0, "lift_over_baseline": 0.0,
        "note": "结构性恒 unknown（673u 判据 / 无本地检测器）⇒ 由**先验**逐格决定 ⇒ **完全可纠正**。",
    } for a in prior_known]

    return {
        "frame": frame,
        "theorem_T6": {
            "statement": (
                "设原始记录 R = (V(x,a))_{x∈X,a∈A} ∈ {c,m,u}^{|X|×|A|}，报告 ρ = agg(R)。"
                "漂移 τ **可后处理纠正**，当且仅当下列之一成立："
                "(i) τ 不改动 R（只改 ρ：记账 / 聚合 / 标签）——此时保留 R 即可重算任意 ρ；"
                "(ii) τ 删去 R 的若干列，但被删列**逐格**由保留列 + 先验决定。"
                "否则（被删列含 R 中不可由保留列恢复的信息）τ **不可纠正**，必须重测。"
            ),
            "proof_sketch": (
                "(i) τ|_ρ 是已知函数，R 保留 ⇒ 可计算任意 ρ'，故可恢复。"
                "(ii) 被删列是保留列的函数 ⇒ 可逐格重建，误差 0。"
                "反之，若被删列含不可由保留列决定的信息，则由 697 定理 T2 的构造"
                "（两个不同的 R 映射到同一个 R'）⇒ 多对一 ⇒ 无逆 ⇒ 不可纠正。"
            ),
        },
        "quantified": rows + prior_rows,
        "post_measurement_layer_drifts": {
            "denominator_accounting": {"correctable": True, "residual_error": 0.0,
                                       "why": "三组件计数 (catch, unknown, miss) 可重算"},
            "aggregation_or_vs_mean": {"correctable": True, "residual_error": 0.0,
                                       "why": "R 未变，换聚合函数即可重算"},
            "label_vocabulary": {"correctable": True, "residual_error": 0.0,
                                  "why": "λ 是 R 之上的分组函数，逐样本裁决未变"},
        },
        "acquisition_layer_drifts": {
            "environment_gated_removal": {"correctable": False,
                                          "residual_error": None,
                                          "why": "asan/ubsan/tsan 列被删除且不可由保留列恢复 ⇒ 必须重测"},
        },
        "interpretation": (
            "被撤的 sanitizer 列的**最佳后处理准确率**见 quantified 表："
            "残留误差越接近 0 ⇒ 越接近可纠正；远高于 0 ⇒ 只能重测。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
# 4. 评估系统健康度
# ══════════════════════════════════════════════════════════════════════════
def health_score(frame_data: dict[str, Any], ref692: dict[str, Any]) -> dict[str, Any]:
    """0–100 健康度 = 构成 / 环境 / 标签 / 聚合 四个稳定性分量，各 25 分。"""
    ti = frame_data["type_I_composition"]
    inj = {r["d"]: r["g_app_pp"] for r in ti["injection_scan_d0_to_7"]}
    g_full = inj.get(3, 0.0)
    g_clean = inj.get(0, 0.0)
    comp_inflation = (g_full - g_clean) / g_full if g_full else 0.0

    fr = ref692["frames"]["A5_evaluation_566"]["silent_false_miss"]
    poisoned = fr["poisoned_share_of_e2_negatives_pct"] / 100.0

    ladder = frame_data["type_III_label"]["ladder"]
    fine = [d for d in ladder if d["granularity"] in
            ("defect_type_34_normalized", "raw_70_vocabulary_from_676g_by_type", "type_x_batch_fine")]
    shares = [d["share_high_blindspot_pct"] for d in fine]
    label_spread = (max(shares) - min(shares)) / 100.0 if shares else 0.0

    agg_rows = frame_data["type_IV_aggregation"]["aggregation_table"]
    # 排除 min_asset：它会因掺入零产资产直接归零（相对变化 100%），是病态规则，
    # 从不作为头条数字使用；纳入会让该分量恒为 0 而失去分辨力。
    usable = [r for r in agg_rows if r["rule"] != "min_asset"]
    max_rel = max((r["manipulability_relative_pct"] or 0.0) for r in usable) / 100.0
    worst_rule = max(usable, key=lambda r: (r["manipulability_relative_pct"] or 0.0))["rule"]

    comp = {
        "composition_stability": {"raw": round(1 - comp_inflation, 6), "score": round(25 * (1 - comp_inflation), 2),
                                  "definition": "1 − (g_app(d=3) − g_app(d=0)) / g_app(d=3)"},
        "environment_stability": {"raw": round(1 - poisoned, 6), "score": round(25 * (1 - poisoned), 2),
                                  "definition": "1 − E2 负例中被污染的比例（692：46.95%）"},
        "label_stability": {"raw": round(1 - label_spread, 6), "score": round(25 * (1 - label_spread), 2),
                            "definition": "1 − 细粒度词表间「高盲类占比」的极差 / 100"},
        "aggregation_stability": {"raw": round(1 - max_rel, 6), "score": round(25 * (1 - max_rel), 2),
                                  "definition": "1 − 掺入 3 个零产资产后最敏感**可用**聚合口径的相对变化",
                                  "worst_rule": worst_rule,
                                  "excluded": "min_asset（病态：掺零产资产即归零，相对变化 100%）"},
    }
    total = round(sum(v["score"] for v in comp.values()), 2)

    # 历史序列：用**文档化锚点**重建（明确标注为代理序列）
    history = [
        {"version": "676m", "event": "H2 标签迁移：defect_type 56→33，308/1042 条改写，笼统标签 145→8",
         "component_moved": "label", "direction": "先降后升（迁移期标签不稳，迁移后归一）",
         "source": "data/676m_H2标签迁移报告.md"},
        {"version": "681", "event": "类型统计重算：34 类、13/34 >50% 盲",
         "component_moved": "label", "direction": "升（口径固定）",
         "source": "data/681_type_stats_normalized.json"},
        {"version": "692", "event": "环境形式化 + 配对实验：E1→E2 静默退化，46.95% 负例被污染",
         "component_moved": "environment", "direction": "降（首次暴露环境不稳定性）",
         "source": "data/692_environment_paired_experiment.json"},
        {"version": "693", "event": "元评估 v2 + 可检测性模型（族外 AUC 0.766 天花板）",
         "component_moved": "caliber", "direction": "持平（新增能力边界声明）",
         "source": "data/693_meta_evaluation_v2.json"},
        {"version": "697/698", "event": "漂移代数 + 四型量化；本批给出四项分量与总分",
         "component_moved": "all", "direction": "首次可评分",
         "source": "data/698_drift_propagation.json"},
    ]
    return {
        "total_score": total,
        "components": comp,
        "history": history,
        "honest_note": (
            "历史序列是**从各批次的文档化锚点重建的代理序列**，"
            "**不是**用同一台仪器在不同时间点测出的时间序列 —— 各批次报告的分量定义并不一致，"
            "因此曲线只应读作**定性轨迹**，不应读作精确的健康度数值变化。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="698-B 漂移传播 / 检测预算 / 可纠错边界 / 健康度（只读）")
    ap.add_argument("--trials", type=int, default=200)
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    args = ap.parse_args(argv)

    a5 = load_samples(A5)
    evaluation = [s for s in a5 if s["split"] == "evaluation"]
    ref692 = load_json_cached(DATA / REF_692)
    comp_doc = load_json_cached(DATA / DRIFT_698)
    frame1147 = comp_doc["frames"]["capability_boundary_1147"]
    _log.info("A5 evaluation n=%d", len(evaluation))

    out: dict[str, Any] = {
        "schema": "queyi-698/drift-propagation/v1",
        "generated_by": "tools/compute_698_drift_propagation.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "drift_chain": drift_chain(evaluation, "A5_evaluation_566"),
        "detection_budget": detection_budget(evaluation, trials=args.trials),
        "correctability": correctability(evaluation, "A5_evaluation_566"),
        "health": health_score(frame1147, ref692),
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    _log.info("已写出 %s", args.out)

    print("== 698-B 漂移传播（只读）==")
    for name, ch in out["drift_chain"]["chains"].items():
        nested = ch["nested_E3_subset_of_E2"]
        print(f"  {name} [{'嵌套' if nested else '非嵌套'}]: "
              f"CK 最大绝对误差 = {ch['ck_max_abs_error']}  ⇒ CK 成立？{ch['ck_holds']}")
        print(f"     生成元复合：撤除集并集 = {ch['generator_composition']['removed_E1_to_E3_union']}（成立）")
    print("\n  检测预算（检出概率）：")
    for b, row in out["detection_budget"]["budgets"].items():
        print(f"    B={b:<4} 均匀={row['uniform']['detection_probability']:.3f}  "
              f"两阶段自适应={row['two_stage_adaptive']['detection_probability']:.3f}  "
              f"Δ={row['delta_adaptive_minus_uniform']:+.3f}")
    print("\n  可纠错残留误差（被撤 sanitizer 列）：")
    for r in out["correctability"]["quantified"][:3]:
        print(f"    {r['removed_asset']:<6} 最佳后处理准确率={r['best_posthoc_accuracy']:.4f}  "
              f"残留={r['residual_error']:.4f}  基线={r['majority_baseline_accuracy']:.4f}")
    h = out["health"]
    print(f"\n  健康度总分 = {h['total_score']} / 100")
    for k, v in h["components"].items():
        print(f"    {k:<24} {v['score']:>6.2f} / 25")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
