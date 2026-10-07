#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""equivalence_689.py — 689-B：合成 vs 真实的等价性检验（TOST）与标准化（composition adjustment）。

背景（689 究极重构批次）
========================
外部评审指出：论文此前用 ``p=0.60`` 暗示"合成与真实无差异"，这是错误读法
（p>0.05 不等于等价）。本脚本做两件正确的事：

* **B1 TOST**：真实靶场 110 条（65/110 = 59.09%）vs 自造语料 1147 条
  （707/1147 = 61.64%），独立两比例。主分析 margin ±10pp；敏感性
  ±5/7/10/12/15pp；margin 曲线 m∈[0,15]pp（步长 0.25）。报告 90% CI
  （Wald）、双单侧 p、TOST 决策与**最小通过 margin**；另做设计效应校正的
  保守敏感性（677b 的 design effect 4.05–4.26，取上界 4.26）。
* **B2 标准化**：在家族级（``tools/repair_681_labels.py::FAMILY8``，8 家族）
  与类型级（9 个共同类型）分别做**双向标准化**：
  ``R_syn_std = Σ_f w_real,f · R_syn,f``（正向）与
  ``R_real_std = Σ_f w_syn,f · R_real,f``（反向，限制在共同支撑域并重新归一化）。
  回答"整体率相似是否由缺陷类型分布抵消造成"。

口径与红线
==========
* 只读上游产物：``data/683_real_world_detection_matrix.json``（683，只读）、
  ``data/blindspot_676g_detection_matrix.json``（676g，只读）；
* OR 判定口径两侧逐字一致：任一 catch ⇒ catch；全部 unknown ⇒ unknown；其余 miss。
  真实侧 ``or_verdict``；合成侧 ``or_verdict_all8``（两侧该口径下 unknown 均为 0）；
* 不引入 numpy/scipy；全部标准库；确定性计算（无随机），种子登记为 6891（供复算元数据）；
* 不修改任何上游文件；输出 ``data/689_equivalence_test.{json,md}`` 与
  ``data/689_standardized_analysis.{json,md}``。

用法
====
    python tools/equivalence_689.py
"""
from __future__ import annotations

import datetime as _dt
import json
import math
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
REAL_MATRIX = ROOT / "data" / "683_real_world_detection_matrix.json"
SYN_MATRIX = ROOT / "data" / "blindspot_676g_detection_matrix.json"
OUT_TOST_JSON = ROOT / "data" / "689_equivalence_test.json"
OUT_TOST_MD = ROOT / "data" / "689_equivalence_test_report.md"
OUT_STD_JSON = ROOT / "data" / "689_standardized_analysis.json"
OUT_STD_MD = ROOT / "data" / "689_standardized_analysis_report.md"

SEED = 6891  # 本脚本确定性，无随机；种子仅登记供复算元数据
Z90 = 1.6448536269514722  # 正态 95% 分位（TOST 双单侧 α=0.05 ⇒ 90% CI）
DEFF_CONSERVATIVE = 4.26  # 677b design effect 上界（4.05–4.26），用于保守敏感性

#: 家族映射权威源：tools/repair_681_labels.py::FAMILY8（681 归一化后口径）
FAMILY8: dict[str, tuple[str, ...]] = {
    "memory": ("memory_safety", "use_after_free", "double_free", "memory_leak",
               "smart_pointer", "raii_violation", "move_semantics", "uninitialized_read"),
    "bounds": ("out_of_bounds", "null_pointer_deref"),
    "integer": ("integer_overflow", "bit_operation"),
    "alias_type": ("type_punning", "strict_aliasing", "alignment", "endianness"),
    "concurrency": ("data_race", "atomic_ub", "memory_order", "deadlock", "condition_variable"),
    "stl": ("iterator_invalidation", "stl_container_ub", "string_ub", "algorithm_misuse"),
    "language_oop": ("virtual_function", "lambda_capture", "logic_error", "cross_tu_ub", "other_ub"),
    "embedded_link": ("volatile_misuse", "register_ub", "interrupt_safety", "linker_odr"),
}
TYPE_TO_FAMILY: dict[str, str] = {t: f for f, ts in FAMILY8.items() for t in ts}


def _now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _norm_cdf(z: float) -> float:
    """标准正态 CDF（标准库实现，允许 scipy 缺失）。"""
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def _prop_diff_stats(k1: int, n1: int, k2: int, n2: int) -> dict[str, float]:
    """独立两比例之差（p1 - p2）的 Wald 统计量。"""
    p1 = k1 / n1
    p2 = k2 / n2
    se = math.sqrt(p1 * (1.0 - p1) / n1 + p2 * (1.0 - p2) / n2)
    return {"p1": p1, "p2": p2, "diff": p1 - p2, "se": se}


def _tost_once(diff: float, se: float, margin: float) -> dict[str, Any]:
    """TOST：H0_lower: diff <= -m；H0_upper: diff >= +m。p_tost = max(p_lower, p_upper)。"""
    z_lower = (diff + margin) / se
    z_upper = (diff - margin) / se
    p_lower = 1.0 - _norm_cdf(z_lower)
    p_upper = _norm_cdf(z_upper)
    p_tost = max(p_lower, p_upper)
    ci_low = diff - Z90 * se
    ci_high = diff + Z90 * se
    return {
        "margin_pp": margin * 100.0,
        "ci90_pp": [ci_low * 100.0, ci_high * 100.0],
        "p_lower": p_lower,
        "p_upper": p_upper,
        "p_tost": p_tost,
        "equivalent": p_tost < 0.05,
        "ci_within_margin": (ci_low > -margin) and (ci_high < margin),
    }


def _min_passing_margin(diff: float, se: float) -> float:
    """最小通过 margin：TOST 通过 ⟺ 90% CI ⊂ (-m, m) ⟺ m > |diff| + z90·se（当 CI 跨 0 时）。"""
    return abs(diff) + Z90 * se


def _or_catch(verdict: str) -> bool:
    return verdict == "catch"


def _real_samples() -> list[dict[str, Any]]:
    doc: dict[str, Any] = json.loads(REAL_MATRIX.read_text(encoding="utf-8"))
    return list(doc["samples"])


def _syn_samples() -> list[dict[str, Any]]:
    doc: dict[str, Any] = json.loads(SYN_MATRIX.read_text(encoding="utf-8"))
    return list(doc["samples"])


def _bucket(samples: list[dict[str, Any]], key: str, field: str) -> dict[str, list[int]]:
    """返回 {key: [n, catch]}（unknown 不计入 catch；OR 口径两侧 unknown 均为 0，此处仍显式排除）。"""
    out: dict[str, list[int]] = {}
    for s in samples:
        k = str(s[key])
        v = str(s[field])
        cell = out.setdefault(k, [0, 0])
        cell[0] += 1
        if _or_catch(v):
            cell[1] += 1
    return out


# ---------------------------------------------------------------- B1: TOST
def run_tost() -> dict[str, Any]:
    real = _real_samples()
    syn = _syn_samples()
    n_real = len(real)
    k_real = sum(1 for s in real if _or_catch(str(s["or_verdict"])))
    n_syn = len(syn)
    k_syn = sum(1 for s in syn if _or_catch(str(s["or_verdict_all8"])))

    base = _prop_diff_stats(k_real, n_real, k_syn, n_syn)
    diff, se = base["diff"], base["se"]

    main = _tost_once(diff, se, 0.10)
    sensitivity = [_tost_once(diff, se, m / 100.0) for m in (5.0, 7.0, 10.0, 12.0, 15.0)]
    curve = []
    steps = 61  # 0 .. 15 pp, step 0.25
    for i in range(steps):
        m_pp = 15.0 * i / (steps - 1)
        curve.append({"margin_pp": round(m_pp, 4),
                      "p_tost": _tost_once(diff, se, m_pp / 100.0)["p_tost"]})

    m_pass = _min_passing_margin(diff, se)

    # 设计效应保守校正：只作用于合成侧样本量（n_syn_eff = n_syn / deff）
    n_syn_eff = n_syn / DEFF_CONSERVATIVE
    p1 = k_real / n_real
    p2 = k_syn / n_syn
    se_adj = math.sqrt(p1 * (1 - p1) / n_real + DEFF_CONSERVATIVE * p2 * (1 - p2) / n_syn)
    deff = {
        "design_effect_upper": DEFF_CONSERVATIVE,
        "source": "data/677b_cluster_bootstrap.json（design effect 4.05–4.26，取上界保守）",
        "n_syn_effective": round(n_syn_eff, 2),
        "se_pp": se_adj * 100.0,
        "tost_margin10": _tost_once(diff, se_adj, 0.10),
        "min_passing_margin_pp": _min_passing_margin(diff, se_adj) * 100.0,
    }

    return {
        "schema": "queyi-689-equivalence/v1",
        "generated_by": "tools/equivalence_689.py",
        "generated_at": _now(),
        "seed": SEED,
        "sources": {
            "real": "data/683_real_world_detection_matrix.json（683，只读）",
            "syn": "data/blindspot_676g_detection_matrix.json（676g，只读）",
            "verdict_rule": "OR：任一 catch ⇒ catch；全部 unknown ⇒ unknown；其余 miss（两侧逐字一致）",
        },
        "arms": {
            "real": {"n": n_real, "catch": k_real, "rate_pct": base["p1"] * 100.0,
                     "label": "source-derived real-defect corpus（110 CVE 重构）"},
            "syn": {"n": n_syn, "catch": k_syn, "rate_pct": base["p2"] * 100.0,
                    "label": "self-authored synthetic corpus（676g 冻结矩阵）"},
        },
        "difference": {
            "diff_pp": diff * 100.0,
            "direction": "real − synthetic",
            "se_pp": se * 100.0,
            "independence_note": "两批样本独立（非配对），不能做 McNemar；此前 z=-0.52, p=0.60 为**非显著性**，不是等价性证据",
        },
        "tost_main_margin10": main,
        "tost_margin_sensitivity": sensitivity,
        "tost_margin_curve": curve,
        "min_passing_margin_pp": m_pass * 100.0,
        "deff_adjusted_sensitivity": deff,
        "conclusion": (
            "TOST（margin=±10pp）未通过：90% CI 下界 −10.61pp 略超 −10pp（p_tost≈0.064>0.05）；"
            "最小通过 margin≈10.61pp（deff 校正后≈11.67pp）。"
            "因此不能说\"合成与真实等价\"；只能说\"在本样本量与本 margin 下未能声明等价，"
            "差异点估计 −2.55pp、CI 宽约 ±8.1pp\"。"
        ),
    }


# --------------------------------------------------- B2: standardized analysis
def _family_table(real: list[dict[str, Any]], syn: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rb = _bucket(real, "defect_type", "or_verdict")
    sb = _bucket(syn, "defect_type", "or_verdict_all8")
    fam_r: dict[str, list[int]] = {}
    fam_s: dict[str, list[int]] = {}
    for t, (n, k) in rb.items():
        f = TYPE_TO_FAMILY[t]
        cell = fam_r.setdefault(f, [0, 0])
        cell[0] += n
        cell[1] += k
    for t, (n, k) in sb.items():
        f = TYPE_TO_FAMILY[t]
        cell = fam_s.setdefault(f, [0, 0])
        cell[0] += n
        cell[1] += k

    rows = []
    n_r_total, n_s_total = len(real), len(syn)
    for f in FAMILY8:
        rn, rk = fam_r.get(f, [0, 0])
        sn, sk = fam_s.get(f, [0, 0])
        rows.append({
            "family": f,
            "n_real": rn, "k_real": rk,
            "rate_real_pct": (rk / rn * 100.0) if rn else None,
            "w_real": rn / n_r_total,
            "n_syn": sn, "k_syn": sk,
            "rate_syn_pct": (sk / sn * 100.0) if sn else None,
            "w_syn": sn / n_s_total,
            "delta_real_minus_syn_pp": ((rk / rn - sk / sn) * 100.0) if (rn and sn) else None,
            "in_common_support": bool(rn and sn),
        })
    return rows


def _type_table(real: list[dict[str, Any]], syn: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rb = _bucket(real, "defect_type", "or_verdict")
    sb = _bucket(syn, "defect_type", "or_verdict_all8")
    n_r_total, n_s_total = len(real), len(syn)
    rows = []
    for t in sorted(set(rb) | set(sb)):
        rn, rk = rb.get(t, [0, 0])
        sn, sk = sb.get(t, [0, 0])
        rows.append({
            "type": t, "family": TYPE_TO_FAMILY[t],
            "n_real": rn, "k_real": rk,
            "rate_real_pct": (rk / rn * 100.0) if rn else None,
            "w_real": rn / n_r_total,
            "n_syn": sn, "k_syn": sk,
            "rate_syn_pct": (sk / sn * 100.0) if sn else None,
            "w_syn": sn / n_s_total,
            "delta_real_minus_syn_pp": ((rk / rn - sk / sn) * 100.0) if (rn and sn) else None,
            "in_common_support": bool(rn and sn),
        })
    return rows


def _standardize(rows: list[dict[str, Any]], weight_side: str, rate_side: str,
                 restrict_common: bool) -> dict[str, Any]:
    """标准化：用一侧权重加权另一侧的率。

    weight_side ∈ {real, syn}；rate_side 为被加权侧的率来源。
    restrict_common=True 时只保留共同支撑行并把权重重新归一化。
    """
    use = [r for r in rows if (r["in_common_support"] if restrict_common else r["rate_syn_pct"] is not None)]
    if restrict_common:
        use = [r for r in use if r[f"rate_{rate_side}_pct"] is not None]
    wsum = sum(float(r[f"w_{weight_side}"]) for r in use)
    acc = 0.0
    for r in use:
        w = float(r[f"w_{weight_side}"]) / wsum
        acc += w * float(r[f"rate_{rate_side}_pct"])
    return {
        "weight_side": weight_side,
        "rate_side": rate_side,
        "restrict_common_support": restrict_common,
        "rows_used": len(use),
        "weight_sum_normalized_from": wsum,
        "standardized_rate_pct": acc,
    }


def run_standardized() -> dict[str, Any]:
    real = _real_samples()
    syn = _syn_samples()
    n_real, n_syn = len(real), len(syn)
    k_real = sum(1 for s in real if _or_catch(str(s["or_verdict"])))
    k_syn = sum(1 for s in syn if _or_catch(str(s["or_verdict_all8"])))
    rate_real = k_real / n_real * 100.0
    rate_syn = k_syn / n_syn * 100.0

    fam_rows = _family_table(real, syn)
    typ_rows = _type_table(real, syn)

    fam_fwd = _standardize(fam_rows, "real", "syn", True)
    fam_rev = _standardize(fam_rows, "syn", "real", True)
    typ_fwd = _standardize(typ_rows, "real", "syn", True)
    typ_rev = _standardize(typ_rows, "syn", "real", True)

    common_fam_share_syn = sum(r["w_syn"] for r in fam_rows if r["in_common_support"])
    common_typ = [r for r in typ_rows if r["in_common_support"]]
    n_syn_common = sum(r["n_syn"] for r in common_typ)
    k_syn_common = sum(r["k_syn"] for r in common_typ)
    rate_syn_common = k_syn_common / n_syn_common * 100.0

    return {
        "schema": "queyi-689-standardized/v1",
        "generated_by": "tools/equivalence_689.py",
        "generated_at": _now(),
        "seed": SEED,
        "family_mapping_source": "tools/repair_681_labels.py::FAMILY8（681 归一化后权威口径，8 家族）",
        "headline": {
            "rate_real_pct": rate_real, "rate_syn_pct": rate_syn,
            "diff_pp": rate_real - rate_syn,
        },
        "family_table": fam_rows,
        "type_table": typ_rows,
        "family_standardization": {
            "forward_rsyn_std": fam_fwd,
            "reverse_rreal_std": fam_rev,
            "forward_diff_pp": rate_real - fam_fwd["standardized_rate_pct"],
            "reverse_diff_pp": rate_syn - fam_rev["standardized_rate_pct"],
            "common_support_share_of_syn": common_fam_share_syn,
            "note": ("正向=真实权重×合成家族率；反向=合成权重×真实家族率（仅 6 个共同家族，权重重新归一化）。"
                     "合成的 stl/embedded_link 两家族在真实侧无对应样本，反向标准化不可覆盖。"),
        },
        "type_standardization": {
            "forward_rsyn_std": typ_fwd,
            "reverse_rreal_std": typ_rev,
            "forward_diff_pp": rate_real - typ_fwd["standardized_rate_pct"],
            "reverse_diff_pp": rate_syn_common - typ_rev["standardized_rate_pct"],
            "n_syn_common_support": n_syn_common,
            "rate_syn_common_support_pct": rate_syn_common,
            "note": ("类型级只用两侧都存在的 9 类；反向标准化对比的是合成在这 9 类子集上的率"
                     f"（{k_syn_common}/{n_syn_common} = {rate_syn_common:.2f}%），不是全池 61.64%。"),
        },
        "interpretation": {
            "q1_are_overall_rates_compensated": True,
            "q1_evidence": ("正向标准化把差异从 −2.55pp 放大到 −17.92pp：在**真实缺陷构成**下，"
                            "合成数据的家族率预测 77.01%，真实只到 59.09%。"
                            "整体率相近主要由两侧家族构成差异抵消（真实 64.5% 样本落在检测器强家族"
                            "bounds/memory/integer，合成只有 36.9%）。"),
            "q2_family_level_structure": [
                "memory: real 100.00% vs syn 71.05%（+28.95pp，真实更强）",
                "bounds: real 86.36% vs syn 92.37%（−6.01pp）",
                "integer: real 71.43% vs syn 88.70%（−17.27pp）",
                "concurrency: real 75.00% vs syn 42.67%（+32.33pp，小样本 n=4）",
                "alias_type: real 0.00% vs syn 36.56%（−36.56pp，n=4）",
                "language_oop: real 3.23% vs syn 62.07%（−58.84pp，真实 logic_error n=31 为主因）",
            ],
            "q3_type_level_structure": ("类型级同向：正向标准化差异 −13.52pp；"
                                        "真实侧 use_after_free/null_pointer_deref/double_free/memory_leak 全捕获，"
                                        "logic_error 31 条只捕获 1 条（3.23% vs 合成 25.71%）、"
                                        "type_punning 4 条 0 捕获（vs 合成 52.17%）。"),
            "conclusion": ("整体检出率相似是**构成抵消**的产物，不是\"两种语料等价\"；"
                           "真实缺陷在其自身构成下比合成低约 17.9pp（家族级正向标准化），"
                           "其中 language_oop（logic/logic-like）与 alias_type 是结构性主因，"
                           "memory/bounds 方向相反。该结论支持论文把 p=0.60 改写为"
                           "\"未检测到显著差异，结构分化显著\"。"),
        },
        "caveats": [
            "真实侧仅 9 类缺陷（34 类词表子集），家族级 language_oop 在合成侧是杂项家族（含 other_ub 62/72 检出），会稀释 logic_error 效应；类型级对照是更锐利的视图。",
            "家族/类型内样本量小（如 alias_type n=4、concurrency n=4），单家族 Δ 仅为结构性指示，不做显著性声明。",
            "两侧样本非独立同分布抽样：真实 110 按 CVE 可得性采样，合成 1147 为自造语料；标准化只调整构成，不调整可观测性设计差异。",
        ],
    }


# ---------------------------------------------------------------- reports
def _write(path: Path, text: str) -> None:
    path.write_text(text, encoding="utf-8", newline="\n")


def tost_report(doc: dict[str, Any]) -> str:
    a = doc["arms"]["real"]
    b = doc["arms"]["syn"]
    d = doc["difference"]
    m = doc["tost_main_margin10"]
    lines = [
        "# 689-B1 · 等价性检验（TOST）：真实靶场 vs 自造语料",
        "",
        f"- 生成：{doc['generated_at']}｜脚本：tools/equivalence_689.py｜种子登记：{doc['seed']}（确定性计算）",
        "- 数据（只读）：`data/683_real_world_detection_matrix.json`（110 条）"
        " vs `data/blindspot_676g_detection_matrix.json`（1147 条）",
        "- 口径：OR（任一 catch ⇒ catch；全部 unknown ⇒ unknown；其余 miss），两侧逐字一致。",
        "",
        "## 1. 两臂",
        "",
        "| 臂 | n | catch | 检出率 |",
        "|---|---:|---:|---:|",
        f"| 真实（source-derived, 110 CVE 重构） | {a['n']} | {a['catch']} | {a['rate_pct']:.2f}% |",
        f"| 合成（self-authored, 676g 冻结矩阵） | {b['n']} | {b['catch']} | {b['rate_pct']:.2f}% |",
        "",
        f"- 差异（real − synthetic）：**{d['diff_pp']:+.2f}pp**，Wald SE {d['se_pp']:.2f}pp。",
        f"- {d['independence_note']}",
        "",
        "## 2. 主分析（margin = ±10pp，α=0.05 双单侧 ⇒ 90% CI）",
        "",
        f"- 90% CI：**[{m['ci90_pp'][0]:.2f}, {m['ci90_pp'][1]:.2f}]pp**"
        f"（CI 是否落入 ±10pp：{'是' if m['ci_within_margin'] else '否'}）",
        f"- p_lower = {m['p_lower']:.4f}｜p_upper = {m['p_upper']:.4f}｜**p_TOST = {m['p_tost']:.4f}**",
        f"- **判定：{'等价成立' if m['equivalent'] else '未通过（不能声明等价）'}**",
        "- 说明：落在 +10pp 一侧的上单侧检验通过（p_upper≈0.005）；未通过的是 −10pp 一侧"
        "（真实更低方向的边界），差 0.61pp 未及。",
        "",
        f"- **最小通过 margin ≈ {doc['min_passing_margin_pp']:.2f}pp**"
        "（= |diff| + z90·SE；即 margin 需 ≥ 该值 TOST 才通过）。",
        "",
        "## 3. Margin 敏感性",
        "",
        "| margin | 90% CI | p_TOST | 等价？ |",
        "|---:|---|---:|---|",
    ]
    for s in doc["tost_margin_sensitivity"]:
        lines.append(f"| ±{s['margin_pp']:.0f}pp | [{s['ci90_pp'][0]:.2f}, {s['ci90_pp'][1]:.2f}] | "
                     f"{s['p_tost']:.4f} | {'是' if s['equivalent'] else '否'} |")
    lines += [
        "",
        "## 4. Margin 曲线（m ∈ [0,15]pp，步长 0.25）",
        "",
        "曲线数据见 JSON `tost_margin_curve`。p_TOST 随 margin 单调下降；"
        f"在 m≈{doc['min_passing_margin_pp']:.2f}pp 处首次 <0.05。",
        "**纪律**：不得为了\"通过\"事后放大 margin；本报告把曲线全量公开，供审稿人检查任何 margin 下的判定。",
        "",
        "## 5. 设计效应保守敏感性（合成侧聚类）",
        "",
        f"- 合成侧样本来自模板家族（677b：design effect 4.05–4.26，本处取上界 {doc['deff_adjusted_sensitivity']['design_effect_upper']}）。",
        f"- 校正后 SE 由 {d['se_pp']:.2f}pp 放宽到 {doc['deff_adjusted_sensitivity']['se_pp']:.2f}pp；",
        f"  margin=±10pp 仍{'通过' if doc['deff_adjusted_sensitivity']['tost_margin10']['equivalent'] else '未通过'}"
        f"（p_TOST={doc['deff_adjusted_sensitivity']['tost_margin10']['p_tost']:.4f}），"
        f"最小通过 margin ≈ {doc['deff_adjusted_sensitivity']['min_passing_margin_pp']:.2f}pp。",
        "",
        "## 6. 结论（可直接引用）",
        "",
        f"> {doc['conclusion']}",
        "",
        "复算：`python tools/equivalence_689.py`（只读两个矩阵，输出本报告与 JSON）。",
        "",
    ]
    return "\n".join(lines)


def std_report(doc: dict[str, Any]) -> str:
    h = doc["headline"]
    lines = [
        "# 689-B2 · 标准化分析（composition adjustment）：整体率相似是构成抵消吗？",
        "",
        f"- 生成：{doc['generated_at']}｜脚本：tools/equivalence_689.py",
        f"- 家族映射：{doc['family_mapping_source']}",
        f"- 头条：真实 {h['rate_real_pct']:.2f}%（65/110） vs 合成 {h['rate_syn_pct']:.2f}%（707/1147），"
        f"差异 {h['diff_pp']:+.2f}pp。",
        "",
        "## 1. 家族级双向标准化",
        "",
        "| 家族 | n_real | 率_real% | w_real | n_syn | 率_syn% | w_syn | Δ(real−syn)pp |",
        "|---|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for r in doc["family_table"]:
        rr = f"{r['rate_real_pct']:.2f}" if r["rate_real_pct"] is not None else "—"
        sr = f"{r['rate_syn_pct']:.2f}" if r["rate_syn_pct"] is not None else "—"
        dd = f"{r['delta_real_minus_syn_pp']:+.2f}" if r["delta_real_minus_syn_pp"] is not None else "—"
        lines.append(f"| {r['family']} | {r['n_real']} | {rr} | {r['w_real']:.4f} | "
                     f"{r['n_syn']} | {sr} | {r['w_syn']:.4f} | {dd} |")
    fw = doc["family_standardization"]["forward_rsyn_std"]
    rv = doc["family_standardization"]["reverse_rreal_std"]
    lines += [
        "",
        f"- **正向**（真实权重 × 合成家族率）：R_syn_std = **{fw['standardized_rate_pct']:.2f}%**；"
        f"R_real − R_syn_std = **{doc['family_standardization']['forward_diff_pp']:+.2f}pp**"
        f"（{fw['rows_used']} 个共同家族，权重归一化自 {fw['weight_sum_normalized_from']:.4f}）。",
        f"- **反向**（合成权重 × 真实家族率，仅共同家族）：R_real_std = **{rv['standardized_rate_pct']:.2f}%**；"
        f"R_syn − R_real_std = **{doc['family_standardization']['reverse_diff_pp']:+.2f}pp**。",
        f"- 共同支撑覆盖：合成侧 {doc['family_standardization']['common_support_share_of_syn'] * 100:.1f}% 的样本"
        "落在与真实共有的 6 个家族；stl/embedded_link 无真实对应。",
        "",
        "## 2. 类型级双向标准化（9 个共同类型）",
        "",
        "| 类型 | 家族 | real | 率_real% | syn | 率_syn% | Δpp |",
        "|---|---|---:|---:|---:|---:|---:|",
    ]
    for r in doc["type_table"]:
        if not r["in_common_support"]:
            continue
        dd = f"{r['delta_real_minus_syn_pp']:+.2f}" if r["delta_real_minus_syn_pp"] is not None else "—"
        lines.append(f"| {r['type']} | {r['family']} | {r['k_real']}/{r['n_real']} | {r['rate_real_pct']:.2f} | "
                     f"{r['k_syn']}/{r['n_syn']} | {r['rate_syn_pct']:.2f} | {dd} |")
    tf = doc["type_standardization"]
    lines += [
        "",
        f"- 正向标准化（真实类型权重 × 合成同类型率）：R_syn_std = **{tf['forward_rsyn_std']['standardized_rate_pct']:.2f}%**；"
        f"差异 **{tf['forward_diff_pp']:+.2f}pp**。",
        f"- 反向标准化（合成类型权重 × 真实同类型率，对比合成在这 9 类子集上的率 "
        f"{tf['rate_syn_common_support_pct']:.2f}% = {tf['n_syn_common_support']} 条子集）："
        f"R_real_std = **{tf['reverse_rreal_std']['standardized_rate_pct']:.2f}%**；差异 **{tf['reverse_diff_pp']:+.2f}pp**。",
        "",
        "## 3. 解读（回答\"分布抵消\"问题）",
        "",
        f"1. **是，整体率相似是构成抵消的产物。** {doc['interpretation']['q1_evidence']}",
        "",
        "2. **家族级结构分化（真正的信息）**：",
    ]
    lines += [f"   - {x}" for x in doc["interpretation"]["q2_family_level_structure"]]
    lines += [
        "",
        f"3. **类型级同向**：{doc['interpretation']['q3_type_level_structure']}",
        "",
        "## 4. 结论（可直接引用）",
        "",
        f"> {doc['interpretation']['conclusion']}",
        "",
        "## 5. 诚实边界",
        "",
    ]
    lines += [f"- {c}" for c in doc["caveats"]]
    lines += ["", "复算：`python tools/equivalence_689.py`。", ""]
    return "\n".join(lines)


def main() -> None:
    tost = run_tost()
    std = run_standardized()
    _write(OUT_TOST_JSON, json.dumps(tost, ensure_ascii=False, indent=1) + "\n")
    _write(OUT_TOST_MD, tost_report(tost))
    _write(OUT_STD_JSON, json.dumps(std, ensure_ascii=False, indent=1) + "\n")
    _write(OUT_STD_MD, std_report(std))
    print("[689-B] TOST:", tost["tost_main_margin10"]["equivalent"],
          "p=", round(tost["tost_main_margin10"]["p_tost"], 4),
          "min_margin=", round(tost["min_passing_margin_pp"], 2))
    print("[689-B] fwd diff:", round(std["family_standardization"]["forward_diff_pp"], 2),
          "rev diff:", round(std["family_standardization"]["reverse_diff_pp"], 2),
          "type fwd:", round(std["type_standardization"]["forward_diff_pp"], 2))
    print("[689-B] wrote", OUT_TOST_JSON.name, OUT_TOST_MD.name, OUT_STD_JSON.name, OUT_STD_MD.name)


if __name__ == "__main__":
    main()
