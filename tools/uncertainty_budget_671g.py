#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""uncertainty_budget_671g.py — 671g E5：检出率的 GUM 不确定度预算（统计/系统/标注三分量）。

计量学 GUM 思路（《测量不确定度表示指南》）
==========================================
报一个检出率，不确定度不只是"样本量"。本工具把它拆成三个独立分量并方和根合成：

  * u_stat：**统计**分量（抽样）——用 CP95 半宽 / 1.96 近似（小样本保守，报告同时给精确 CP）；
  * u_sys ：**系统**分量——检测器差异（FD vs 静态口径的率差，作为"仪器依赖"的系统效应上界）
    与环境差异（本机 vs 缺关键检测器导致的 unknown 比例）；
  * u_lab ：**标注**分量——由标注一致性（IRR/单人 κ，或分歧比例）折算的率不确定度。

合成：u_c = sqrt(u_stat² + u_sys² + u_lab²)（假设分量独立；相关时报告必须声明为**低估**）。
这是**预算/上界**工具，不是精确测量：目的是把"87.5% 到底多硬"变成可见数字，
防止把小样本+强仪器依赖+同源判据的率当精确值。

用法
====
    python tools/uncertainty_budget_671g.py --k 14 --n 16 --cp-low 61.65 --cp-high 98.45 \\
        --detector-gap 81.3 --unknown-frac 0.033 --kappa 1.0
"""
from __future__ import annotations

import argparse
import json
import math


def stat_component(cp_low_pct: float, cp_high_pct: float) -> float:
    """CP95 半宽（百分点）/1.96 近似标准不确定度。"""
    return (cp_high_pct - cp_low_pct) / 2.0 / 1.96


def detector_component(detector_gap_pp: float) -> float:
    """检测器/仪器依赖的系统效应：口径重分箱率差（pp）的一半作为上界分量。"""
    return abs(detector_gap_pp) / 2.0


def environment_component(unknown_frac: float, total: int, unknown: int) -> float:
    """环境依赖：unknown 比例（可测分母外的样本占总样本比，pp）——换台没检测器的机器直接掉这么多。"""
    frac = unknown_frac if unknown_frac is not None else (unknown / total if total else 0.0)
    return frac * 100.0


def labeling_component(kappa: float | None, disagreement_rate: float | None = None) -> float:
    """标注分量：κ 低 ⇒ 标注不可靠 ⇒ 率不确定；或直接给重标分歧率（pp 的一半）。"""
    if disagreement_rate is not None:
        return abs(disagreement_rate) / 2.0
    if kappa is None:
        return 0.0
    if kappa <= 0:
        return 50.0                     # κ=0 ⇒ 标注无信息，给最保守上界
    return max(0.0, (1.0 - kappa)) * 50.0 / 1.0   # κ=0→50pp，κ=1→0（线性上界）


def combine(components: dict[str, float]) -> float:
    """方和根合成（独立假设）。"""
    return math.sqrt(sum(v * v for v in components.values()))


def budget(k: int, n: int, cp_low: float, cp_high: float, *, detector_gap_pp: float = 0.0,
         unknown_frac: float = 0.0, kappa: float | None = None,
         disagreement_rate: float | None = None) -> dict:
    point = 100.0 * k / n
    u_stat = stat_component(cp_low, cp_high)
    u_det = detector_component(detector_gap_pp)
    u_env = environment_component(unknown_frac, 0, 0)
    u_lab = labeling_component(kappa, disagreement_rate)
    u_sys = math.sqrt(u_det ** 2 + u_env ** 2)
    comps = {"u_stat": round(u_stat, 3), "u_detector": round(u_det, 3),
              "u_environment": round(u_env, 3), "u_labeling": round(u_lab, 3)}
    uc = combine({"stat": u_stat, "sys": u_sys, "lab": u_lab})
    return {"point_pct": round(point, 3), "components_pp": comps,
            "u_sys_pp": round(u_sys, 3), "combined_std_pp": round(uc, 3),
            "approx95_extended_pp": round(2 * uc, 3),
            "interval_combined_pct": [round(point - 2 * uc, 3), round(point + 2 * uc, 3)],
            "independence_note": "分量按独立假设方和根；u_det 与 u_env 相关，合成偏乐观（保守上界请相加）"}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g E5：GUM 不确定度预算")
    ap.add_argument("--k", type=int, required=True)
    ap.add_argument("--n", type=int, required=True)
    ap.add_argument("--cp-low", type=float, required=True)
    ap.add_argument("--cp-high", type=float, required=True)
    ap.add_argument("--detector-gap", type=float, default=0.0, help="FD vs 静态口径率差 pp")
    ap.add_argument("--unknown-frac", type=float, default=0.0)
    ap.add_argument("--kappa", type=float, default=None)
    ap.add_argument("--disagreement-rate", type=float, default=None)
    a = ap.parse_args(argv)
    print(json.dumps(budget(a.k, a.n, a.cp_low, a.cp_high,
                         detector_gap_pp=a.detector_gap, unknown_frac=a.unknown_frac,
                         kappa=a.kappa, disagreement_rate=a.disagreement_rate),
                     ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
