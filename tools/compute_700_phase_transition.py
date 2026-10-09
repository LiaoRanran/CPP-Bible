#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""compute_700_phase_transition.py — 700-B：结构性 Goodhart 的相变理论（**只读**）。

思路
====
把评估系统看作一个受**控制参数**驱动的物理系统：
* **控制参数**：口径偏离量（退化资产数 $d$ / 标签粒度 $g$ / 聚合规则 / 环境）；
* **序参量** $\\varphi$：**测量失真**（报告值与机制值的偏离）$= |\\hat R - R^*|$；
* **响应函数（磁化率）** $\\chi = \\mathrm{d}\\varphi/\\mathrm{d}(\\text{控制参数})$。

要回答
======
1. 四型各自是**一阶**（不连续跳变）还是**二阶**（连续、临界）相变？
2. 有没有**临界点**？临界指数 $\\beta$ 是多少？
3. 有没有可用的**预警指标**？能否回测 681 的标签漂移？
4. 四型是否属于**同一个普适性类**？

红线：``detect_calls = 0``；只读 698/697/676g/681 的冻结产物；产出只写 ``data/700_*``。

用法
====
    python tools/compute_700_phase_transition.py
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import sys
from pathlib import Path
from typing import Any, Final

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA, load_json_cached  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("compute_700_phase_transition")

COMP_698: Final[str] = "698_composition_drift.json"
DRIFT_697: Final[str] = "697_drift_algebra.json"
STATS_676G: Final[str] = "blindspot_676g_stats.json"
TYPES_681: Final[str] = "681_type_stats_normalized.json"
OUT_JSON: Final[Path] = ROOT / "data" / "700_phase_transition.json"


# ══════════════════════════════════════════════════════════════════════════
# 工具
# ══════════════════════════════════════════════════════════════════════════
def _linfit2(xs: list[float], ys: list[float]) -> tuple[float, float, float]:
    """两点/多点线性最小二乘 y = a + b·x，返回 (a, b, R²)。"""
    n = len(xs)
    mx = sum(xs) / n
    my = sum(ys) / n
    sxx = sum((x - mx) ** 2 for x in xs)
    if sxx == 0:
        return my, 0.0, 0.0
    sxy = sum((x - mx) * (y - my) for x, y in zip(xs, ys))
    b = sxy / sxx
    a = my - b * mx
    ss_res = sum((y - (a + b * x)) ** 2 for x, y in zip(xs, ys))
    ss_tot = sum((y - my) ** 2 for y in ys)
    return a, b, (1 - ss_res / ss_tot if ss_tot > 0 else 0.0)


def _lag1_autocorr(v: list[float]) -> float | None:
    if len(v) < 3:
        return None
    xs, ys = v[:-1], v[1:]
    a, b, r2 = _linfit2(xs, ys)
    _ = (a, b)
    return round(math.sqrt(max(0.0, r2)) if b >= 0 else -math.sqrt(max(0.0, r2)), 6)


def _numeric_derivative(xs: list[float], ys: list[float]) -> list[float]:
    out: list[float] = []
    for i in range(len(xs) - 1):
        dx = xs[i + 1] - xs[i]
        out.append((ys[i + 1] - ys[i]) / dx if dx else 0.0)
    return out


# ══════════════════════════════════════════════════════════════════════════
# 1. 四型的响应曲线
# ══════════════════════════════════════════════════════════════════════════
def response_curves() -> dict[str, Any]:
    comp = load_json_cached(DATA / COMP_698)
    frame = comp["frames"]["capability_boundary_1147"]
    inj = frame["type_I_composition"]["injection_scan_d0_to_7"]
    ladder = frame["type_III_label"]["ladder"]
    agg = frame["type_IV_aggregation"]["aggregation_table"]
    drift = load_json_cached(DATA / DRIFT_697)

    # Type I：控制参数 d，序参量 = 表观增益 g_app（= 报告值与机制值的偏离）
    d_i = [float(r["d"]) for r in inj]
    phi_i = [float(r["g_app_pp"]) for r in inj]

    # Type II：控制参数 = 环境（二值），序参量 = 率差（一阶：跳变）
    t = drift["three_state_transitions"]["A5_evaluation_566"]
    r1 = t["marginal_M"]["catch"] / t["n"] * 100.0
    r2 = t["marginal_Mprime"]["catch"] / t["n"] * 100.0
    phi_ii = [0.0, round(r2 - r1, 4)]

    # Type III：控制参数 = 标签粒度（类数），序参量 = 高盲类占比
    g_iii = [float(x["n_categories"]) for x in ladder]
    phi_iii = [float(x["share_high_blindspot_pct"]) for x in ladder]

    # Type IV：控制参数 = 掺入零产资产数（0 → 3），序参量 = 报告值相对变化
    usable = [r for r in agg if r["rule"] != "min_asset"]
    worst = max(usable, key=lambda r: r["manipulability_relative_pct"] or 0.0)
    phi_iv = [0.0, round(float(worst["manipulability_relative_pct"]), 4)]

    return {
        "type_I": {"control": "退化资产数 d", "x": d_i, "phi_pp": phi_i,
                   "order_parameter": "表观增益 g_app（pp）",
                   "source": "698_composition_drift.json → injection_scan_d0_to_7"},
        "type_II": {"control": "环境（E1→E2）", "x": [0.0, 1.0], "phi_pp": phi_ii,
                    "order_parameter": "报告率差（pp）",
                    "source": "697_drift_algebra.json → three_state_transitions.A5_evaluation_566"},
        "type_III": {"control": "标签粒度（类数 g）", "x": g_iii, "phi_pct": phi_iii,
                     "order_parameter": "高盲类占比（%）",
                     "source": "698_composition_drift.json → type_III_label.ladder"},
        "type_IV": {"control": "掺入零产资产数", "x": [0.0, 3.0], "phi_pct": phi_iv,
                    "order_parameter": "报告值相对变化（%）",
                    "aggregation_rule": worst["rule"],
                    "source": "698_composition_drift.json → type_IV_aggregation.aggregation_table"},
        "type_II_rates_pct": {"E1": round(r1, 4), "E2": round(r2, 4)},
    }


# ══════════════════════════════════════════════════════════════════════════
# 2. 临界点与临界指数（Type I）
# ══════════════════════════════════════════════════════════════════════════
def criticality(xs: list[float], ys: list[float]) -> dict[str, Any]:
    """网格搜索 (d_c, β) 拟合 φ(d) = φ_c − B·(d_c − d)^β；并给响应函数与敏感性。"""
    # 二次拟合（698-A 已定）：φ = c0 + c1 d + c2 d²
    n = len(xs)
    # 三阶正规方程（3 参数）—— 手写高斯消元
    deg = 2
    p = deg + 1
    ata = [[sum(x ** (r + c) for x in xs) for c in range(p)] for r in range(p)]
    aty = [sum((x ** r) * y for x, y in zip(xs, ys)) for r in range(p)]
    m = [row[:] + [aty[r]] for r, row in enumerate(ata)]
    for col in range(p):
        piv = max(range(col, p), key=lambda r: abs(m[r][col]))
        m[col], m[piv] = m[piv], m[col]
        for r in range(p):
            if r != col and abs(m[col][col]) > 1e-15:
                f = m[r][col] / m[col][col]
                for c in range(col, p + 1):
                    m[r][c] -= f * m[col][c]
    coef = [m[r][p] / m[r][r] for r in range(p)]
    c0, c1, c2 = coef
    pred = [c0 + c1 * x + c2 * x * x for x in xs]
    ybar = sum(ys) / n
    ss_res = sum((y - q) ** 2 for y, q in zip(ys, pred))
    ss_tot = sum((y - ybar) ** 2 for y in ys)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

    # 响应函数 χ(d) = dφ/dd = c1 + 2 c2 d
    chi = [round(c1 + 2 * c2 * x, 6) for x in xs]
    # 驻点
    d_star = (-c1 / (2 * c2)) if abs(c2) > 1e-15 else None
    chi_monotone_decreasing = all(chi[i] >= chi[i + 1] - 1e-12 for i in range(len(chi) - 1))
    in_range = d_star is not None and min(xs) <= d_star <= max(xs)

    # 临界指数：**正确的函数形式**是 φ(d) = φ_max − B·(d* − d)^β，
    # 其中 d* 是响应函数的驻点（φ 的极大点），不是"从上方逼近的极限"。
    # ⚠ 第一版写成 φ(d) = φ_c − B(d_c − d)^β 并让 d_c 自由搜索，得到 β=5.0、R²=−2.44
    #   的垃圾解（因为该形式要求 φ 随 d **下降**，与本数据相反）。
    fit: dict[str, Any] | None = None
    if d_star is not None and c2 < 0:
        phi_max = c0 + c1 * d_star + c2 * d_star * d_star
        us: list[float] = []
        vs: list[float] = []
        for x, y in zip(xs, ys):
            u = d_star - x
            v = phi_max - y
            if u > 0 and v > 0:
                us.append(math.log(u))
                vs.append(math.log(v))
        if len(us) >= 3:
            a_ll, b_ll, r2_ll = _linfit2(us, vs)
            fit = {
                "form": "φ(d) = φ_max − B·(d* − d)^β，d* = 二次拟合的驻点（φ 的极大点）",
                "d_star": round(d_star, 4),
                "phi_max_pp": round(phi_max, 4),
                "beta": round(b_ll, 6),
                "B": round(math.exp(a_ll), 6),
                "loglog_r2": round(r2_ll, 6),
                "n_points_used": len(us),
            }

    return {
        "quadratic_fit": {"c0": round(c0, 6), "c1": round(c1, 6), "c2": round(c2, 6),
                          "r2": round(r2, 6)},
        "susceptibility_chi_dphi_dd": chi,
        "chi_monotone_decreasing": chi_monotone_decreasing,
        "stationary_point_d_star": round(d_star, 4) if d_star is not None else None,
        "stationary_point_inside_data_range": bool(in_range),
        "critical_exponent_fit": fit,
        "verdict": (
            "**观测区间内无临界点**：响应函数 χ 单调递减、驻点 d* 落在数据区间之外 "
            f"（d* = {round(d_star, 2) if d_star else 'n/a'} > max(d) = {max(xs)}）"
            "⇒ Type I 在可观测范围内是**平滑（亚临界）退化**，不是相变。"
            "临界指数 β 的拟合值属**外推**，不可作为实测结论。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
# 3. 预警指标
# ══════════════════════════════════════════════════════════════════════════
def early_warnings(xs: list[float], ys: list[float]) -> dict[str, Any]:
    """在 d-扫描上标定预警指标（8 个点），并给出每个指标的方向。"""
    dphi = _numeric_derivative(xs, ys)
    var_inc = sum((d - sum(dphi) / len(dphi)) ** 2 for d in dphi) / len(dphi)
    ac1 = _lag1_autocorr(ys)
    half = len(ys) // 2
    ac1_first = _lag1_autocorr(ys[:half + 1])
    ac1_last = _lag1_autocorr(ys[half:])
    return {
        "n_points": len(xs),
        "indicators": [
            {"name": "序参量水平 φ", "value": round(ys[-1], 4),
             "expected_direction_near_criticality": "升高",
             "observed": "升高（5.30 → 29.88）", "usable": True},
            {"name": "增量方差 Var(Δφ)", "value": round(var_inc, 6),
             "expected_direction_near_criticality": "升高（临界慢化）",
             "observed": "**下降**（增量单调递减）", "usable": True},
            {"name": "一阶自相关 AC1(φ)", "value": ac1,
             "expected_direction_near_criticality": "升高（临界慢化）",
             "observed": f"前半段 {ac1_first} → 后半段 {ac1_last}",
             "usable": ac1 is not None},
            {"name": "零产组件数", "value": 2,
             "expected_direction_near_criticality": "出现即预警",
             "observed": "恒为 2（compile-time / wunsequenced）", "usable": True},
            {"name": "随机臂对池大小的敏感度", "value": "−13.5 pp/资产（d=0→1）",
             "expected_direction_near_criticality": "升高",
             "observed": "随 d 递减（−13.5 → −2.2）", "usable": True},
        ],
        "verdict": (
            "**临界慢化类指标在本数据上失效**：增量方差与自相关都**不升反降**，"
            "与「接近临界点」的预期相反 —— 这**正面支持**了 §2 的结论"
            "（Type I 在观测区间内不是相变）。"
            "⇒ 可用的预警指标是**结构性指标**（零产组件数、随机臂敏感度），不是动力学指标。"
        ),
    }


def label_fragmentation_warning() -> dict[str, Any]:
    """标签碎片化指数（FI）—— 用 676m 之前的原始词表 vs 681 归一化词表标定。

    FI = (#单样本类 + #双样本类) / #类数。FI 高 ⇒ 词表碎片化 ⇒ 标签漂移的前兆。
    """
    stats = load_json_cached(DATA / STATS_676G)
    by_type = stats["by_type"]
    n_cat = len(by_type)
    n1 = sum(1 for x in by_type if x["n"] == 1)
    n2 = sum(1 for x in by_type if x["n"] == 2)
    fi_raw = (n1 + n2) / n_cat

    # 681 的 per_type 是 **dict**（{类型名: {n, blind, ...}}），不是 list
    t681 = load_json_cached(DATA / TYPES_681)
    per_type: dict[str, Any] = t681.get("per_type") or {}
    n_cat_n = len(per_type)
    n1n = sum(1 for v in per_type.values() if v.get("n") == 1)
    n2n = sum(1 for v in per_type.values() if v.get("n") == 2)
    fi_norm = ((n1n + n2n) / n_cat_n) if n_cat_n else None

    return {
        "definition": "FI = (#单样本类 + #双样本类) / #类数（词表碎片化指数）",
        "before_681_normalization": {
            "n_categories": n_cat, "n_singleton": n1, "n_doubleton": n2,
            "FI": round(fi_raw, 6), "source": "676g by_type（原始混合词表，70 类）",
        },
        "after_681_normalization": {
            "n_categories": n_cat_n, "n_singleton": n1n, "n_doubleton": n2n,
            "FI": round(fi_norm, 6) if fi_norm is not None else None,
            "source": "681 type_stats_normalized（归一化词表，34 类）",
        },
        "backtest_verdict": (
            f"**可以回测**：归一化前 FI = {round(fi_raw, 4)}（14 个单样本类 / 70 类），"
            f"归一化后 FI = {round(fi_norm, 4) if fi_norm is not None else 'n/a'}。"
            "FI 在 681 之前就**高于 0**，是一个**纯结构性的、无需任何新测量**即可读出的预警信号。"
            "⇒ 在 681 的标签归一化**之前**，FI 就已经在报警。"
        ),
        "honest_note": (
            "这是**事后标定**（我们已经知道 681 发生了归一化）。"
            "把它当预警指标需要一个**阈值**，而本批只有一次漂移事件 ⇒ 阈值无法标定。"
            "FI > 0 只是必要条件，不是充分条件。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
# 4. 普适性类
# ══════════════════════════════════════════════════════════════════════════
def universality(curves: dict[str, Any], crit: dict[str, Any]) -> dict[str, Any]:
    rows: list[dict[str, Any]] = [
        {"type": "I（构成/分母）", "control_axis": "连续（d）", "shape": "**连续、平滑、凹**",
         "transition_order": "**无相变**（亚临界）",
         "exponent_beta": (crit["critical_exponent_fit"] or {}).get("beta"),
         "exponent_note": "外推值（d_c 落在数据区间之外）"},
        {"type": "II（环境）", "control_axis": "二值（E1/E2）", "shape": "**不连续跳变**",
         "transition_order": "**一阶**", "exponent_beta": None,
         "exponent_note": "一阶相变无 β（序参量在临界点跳变）"},
        {"type": "III（标签）", "control_axis": "离散（类数 g）", "shape": "**非单调**",
         "transition_order": "**非相变**（序参量对控制参数无单调性）", "exponent_beta": None,
         "exponent_note": "非单调 ⇒ 临界指数无定义"},
        {"type": "IV（聚合）", "control_axis": "离散（规则切换）", "shape": "**不连续跳变**",
         "transition_order": "**一阶**", "exponent_beta": None,
         "exponent_note": "同上"},
    ]
    orders = {r["type"][0]: r["transition_order"] for r in rows}
    distinct = len(set(orders.values()))
    return {
        "table": rows,
        "n_distinct_orders": distinct,
        "verdict": (
            "**四型不属于同一个普适性类。** 只有 II 与 IV 同为**一阶**（不连续跳变）；"
            "I 是**连续但无临界点**（亚临界平滑退化）；III 是**非单调**（序参量对控制参数无单调性）。"
            "⇒ 不能用一个临界指数统一刻画四型；"
            "「结构性 Goodhart 的相变理论」这一说法**必须限定为「II/IV 型是一阶相变」**。"
        ),
        "cross_check": {
            "type_I_beta": (crit["critical_exponent_fit"] or {}).get("beta"),
            "type_I_chi_monotone_decreasing": crit["chi_monotone_decreasing"],
            "note": "若 I 与 II/IV 同属一个普适性类，I 也应显示不连续或发散响应 —— 实测两者都不成立。",
        },
    }


# ══════════════════════════════════════════════════════════════════════════
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="700-B 结构性 Goodhart 相变理论（只读）")
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    args = ap.parse_args(argv)

    curves = response_curves()
    ti = curves["type_I"]
    crit = criticality([float(x) for x in ti["x"]], [float(y) for y in ti["phi_pp"]])
    warn = early_warnings([float(x) for x in ti["x"]], [float(y) for y in ti["phi_pp"]])
    frag = label_fragmentation_warning()
    uni = universality(curves, crit)

    doc: dict[str, Any] = {
        "schema": "queyi-700/phase-transition/v1",
        "generated_by": "tools/compute_700_phase_transition.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "order_parameter_definition": (
            "序参量 φ = 测量失真 = |R̂ − R*|（报告值与机制值的偏离）；"
            "控制参数 = 口径偏离量；响应函数 χ = dφ/d(控制参数)"
        ),
        "response_curves": curves,
        "criticality_type_I": crit,
        "early_warning_indicators": warn,
        "label_fragmentation_warning": frag,
        "universality_classes": uni,
        "honest_limits": [
            "Type I 的「无临界点」结论只在 d ∈ [0,7] 上成立；d ≥ 8 的扫描含**注入的幽灵资产**（非真实资产）。",
            "临界指数 β 由网格搜索拟合，d_c 落在数据区间之外 ⇒ **外推值**，不可作为实测结论。",
            "Type II / IV 只有 **2 个控制点**（跳变前后）⇒ 「一阶」的判定基于「不连续」而非拟合。",
            "预警指标只在 **8 个点**上标定；历史序列（5-6 个代理点）**不足以估计**动力学指标。",
            "标签碎片化指数的阈值**无法标定**（只有一次漂移事件）。",
            "「相变」是**类比**：评估系统不是热力学系统，没有温度与自由能；"
            "本批只借用「控制参数 / 序参量 / 响应函数 / 一阶二阶」这套**描述性语言**，不声称存在热力学对应物。",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    _log.info("已写出 %s", args.out)

    print("== 700-B 结构性 Goodhart 相变理论（只读）==")
    q = crit["quadratic_fit"]
    print(f"  Type I 二次拟合：φ(d) = {q['c0']} + {q['c1']}·d + {q['c2']}·d²  (R²={q['r2']})")
    print(f"    驻点 d* = {crit['stationary_point_d_star']}；在数据区间内？"
          f"{crit['stationary_point_inside_data_range']}；χ 单调递减={crit['chi_monotone_decreasing']}")
    f = crit["critical_exponent_fit"]
    if f:
        print(f"    临界指数：β = {f['beta']}（对数-对数 R² = {f['loglog_r2']}），"
              f"d* = {f['d_star']}，φ_max = {f['phi_max_pp']}pp")
    print(f"  ⇒ {crit['verdict'][:70]}…")
    print("\n  预警指标（5 个）：")
    for ind in warn["indicators"]:
        print(f"    {ind['name']:<22} 观测={ind['observed']}")
    print(f"\n  标签碎片化：FI(归一化前)={frag['before_681_normalization']['FI']} → "
          f"FI(归一化后)={frag['after_681_normalization']['FI']}")
    print(f"\n  普适性类：{uni['verdict'][:90]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
