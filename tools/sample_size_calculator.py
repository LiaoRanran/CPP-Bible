#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""sample_size_calculator.py — 707-D：配对审计的**样本量 / 信息论下界**计算器（700-C）。

科研依据（700-C 信息论下界；权威源 ``data/700_sample_complexity.json``）
========================================================================
配对设计（同一样本在两个口径下各判一次）对**不一致对**做符号检验（= 精确 McNemar）：

* ``psi`` = 不一致率 Pr[两口径裁决不同]；``pi`` = 方向概率 Pr[方向 | 不一致]；
* 恒等式 ``epsilon = psi · (2·pi − 1)``；
* 正态近似：``m ≥ (z_{1−α/2}·√(1/4) + z_{1−β}·√(π(1−π)))² / (π − 1/2)²``；``n = m / psi``；
* 完全单向（``π = 1``）：正态近似退化，改用**精确二项** ``m ≥ log(α/2)/log(1/2) = 6``；
* **Type III/IV（标签/聚合）逐样本裁决不变 ⇒ psi = 0 ⇒ 配对设计功效恒 0 ⇒ n = ∞**
  ⇒ 这类漂移**不能**靠配对设计检出，必须用设计级对照（见 `tools/audit_protocol.py` 的双设计）。

已实测（700-C）：Type I n = **849**（psi=0.00707）、Type II n = **17**（psi=0.3534）、Type III/IV = **∞**。

红线：纯计算，``detect_calls = 0``。

用法
====
    python tools/sample_size_calculator.py --type I
    python tools/sample_size_calculator.py --type III
    python tools/sample_size_calculator.py --psi 0.1 --epsilon 0.05
    python tools/sample_size_calculator.py --grid
"""
from __future__ import annotations

import argparse
import json
import math
from typing import Any, Final

# 700-C 实测锚点（data/700_sample_complexity.json::measured_pairs）
MEASURED: Final[dict[str, dict[str, float]]] = {
    "I": {"psi": 0.007067137809187279, "epsilon": 0.007067137809187279},
    "II": {"psi": 0.35335689045936397, "epsilon": 0.35335689045936397},
    "III": {"psi": 0.0, "epsilon": 0.0},
    "IV": {"psi": 0.0, "epsilon": 0.0},
}
EXPECTED_N: Final[dict[str, Any]] = {"I": 849, "II": 17, "III": float("inf"), "IV": float("inf")}


def norm_ppf(p: float) -> float:
    """标准正态分位数（Acklam 有理近似，绝对误差 < 1.15e-9）。"""
    if not 0.0 < p < 1.0:
        raise ValueError("p 必须落在 (0,1)")
    a = [-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00]
    b = [-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01]
    c = [-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00]
    d = [7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00]
    plow, phigh = 0.02425, 1 - 0.02425
    if p < plow:
        q = math.sqrt(-2 * math.log(p))
        return (((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
               ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    if p > phigh:
        q = math.sqrt(-2 * math.log(1 - p))
        return -(((((c[0] * q + c[1]) * q + c[2]) * q + c[3]) * q + c[4]) * q + c[5]) / \
               ((((d[0] * q + d[1]) * q + d[2]) * q + d[3]) * q + 1)
    q = p - 0.5
    r = q * q
    return (((((a[0] * r + a[1]) * r + a[2]) * r + a[3]) * r + a[4]) * r + a[5]) * q / \
           (((((b[0] * r + b[1]) * r + b[2]) * r + b[3]) * r + b[4]) * r + 1)


def required_discordant(pi: float, alpha: float = 0.05, power: float = 0.8) -> int:
    """所需**不一致对**数 m。π = 1 时用精确二项；否则用正态近似（700-C 公式）。"""
    z_a = norm_ppf(1 - alpha / 2)
    z_b = norm_ppf(power)
    if pi >= 1.0:
        # 完全单向：m ≥ log(α/2)/log(1/2)（精确二项，700-C）
        return math.ceil(math.log(alpha / 2) / math.log(0.5))
    num = z_a * math.sqrt(0.25) + z_b * math.sqrt(pi * (1 - pi))
    return math.ceil((num / (pi - 0.5)) ** 2)


def required_n(psi: float, epsilon: float, alpha: float = 0.05, power: float = 0.8) -> dict[str, Any]:
    """由 psi / epsilon 求所需总样本量 n（配对设计）。

    psi = 0 ⇒ 逐样本裁决不变 ⇒ 配对功效 0 ⇒ **n = ∞**（Type III/IV）。
    """
    if psi <= 0:
        return {"psi": psi, "epsilon": epsilon, "pi": None, "m_discordant": None,
                "n_total": float("inf"), "detectable_by_paired_design": False,
                "reason": "psi=0（逐样本裁决不变）⇒ 配对设计功效恒 0 ⇒ n = ∞（Type III/IV 必须用设计级对照）"}
    pi = (1.0 + epsilon / psi) / 2.0
    if not 0.0 < pi <= 1.0:
        raise ValueError(f"非法 (psi,epsilon)：pi={pi} 越界（需 0<eps/psi<=1）")
    m = required_discordant(pi, alpha, power)
    n = math.ceil(m / psi)
    reason = ("完全单向（π=1.0）⇒ 精确二项判据 m ≥ log(α/2)/log(1/2)=6（正态近似退化）"
              if pi >= 1.0 else "正态近似（700-C 公式）")
    return {"psi": psi, "epsilon": epsilon, "pi": round(pi, 6), "m_discordant": m,
            "n_total": n, "detectable_by_paired_design": True, "reason": reason}


def by_type(t: str) -> dict[str, Any]:
    m = MEASURED[t]
    out = required_n(m["psi"], m["epsilon"])
    out["type"] = t
    out["expected_n"] = EXPECTED_N[t]
    out["matches_700C"] = (out["n_total"] == EXPECTED_N[t])
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="707-D：配对审计样本量计算器（700-C 信息论下界）")
    ap.add_argument("--type", choices=("I", "II", "III", "IV"), default=None)
    ap.add_argument("--psi", type=float, default=None)
    ap.add_argument("--epsilon", type=float, default=None)
    ap.add_argument("--alpha", type=float, default=0.05)
    ap.add_argument("--power", type=float, default=0.8)
    ap.add_argument("--grid", action="store_true", help="打印 psi × eps/psi 网格")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    if a.grid:
        grid = []
        for psi in (0.05, 0.1, 0.2, 0.35, 0.5):
            for ratio in (0.25, 0.5, 0.9, 1.0):
                r = required_n(psi, psi * ratio, a.alpha, a.power)
                grid.append({"psi": psi, "epsilon_over_psi": ratio, **r})
        print(json.dumps(grid, ensure_ascii=False, indent=1))
        return 0

    if a.type:
        out = by_type(a.type)
    elif a.psi is not None and a.epsilon is not None:
        out = required_n(a.psi, a.epsilon, a.alpha, a.power)
    else:
        ap.print_help()
        return 0

    if a.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
        return 0
    print("== 707-D 配对样本量（700-C）==")
    print(f"  psi={out['psi']}  eps={out['epsilon']}  pi={out['pi']}")
    print(f"  所需不一致对 m={out['m_discordant']}  所需样本 n={out['n_total']}")
    print(f"  可由配对设计检出={out['detectable_by_paired_design']}  （{out['reason']}）")
    if "matches_700C" in out:
        print(f"  与 700-C 一致（期望 {out['expected_n']}）= {out['matches_700C']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
