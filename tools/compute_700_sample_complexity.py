#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""compute_700_sample_complexity.py — 700-C：评估器审计的信息论下界（**只读**）。

问题
====
给定配对设计，**最少需要多少配对样本**才能以显著性 α、功效 1−β 检出幅度 ≥ ε 的漂移？

模型
====
配对二值结果：记 $\\psi = \\Pr[\\text{不一致}]$（discordance rate），
$\\pi = \\Pr[\\text{方向} \\mid \\text{不一致}]$。则边际率差
$$\\varepsilon = \\psi\\,(2\\pi - 1).$$
检验 = 对**不一致对**做符号检验（= 精确 McNemar）。所需不一致对数
$$m \\;\\ge\\; \\frac{\\bigl(z_{1-\\alpha/2}\\sqrt{\\tfrac14} + z_{1-\\beta}\\sqrt{\\pi(1-\\pi)}\\bigr)^2}{(\\pi-\\tfrac12)^2},
\\qquad n \\;=\\; m/\\psi .$$

要回答
======
1. 四型各自的样本复杂度公式与数值；
2. **哪一型最难检测**（本批的核心发现）；
3. 3 种采样策略（均匀 / 分层比例 / Neyman 最优）与下界的差距；
4. 与 698-B 的 2 策略结论对比。

红线：``detect_calls = 0``；只读冻结矩阵；产出只写 ``data/700_*``。

用法
====
    python tools/compute_700_sample_complexity.py
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import random
import sys
from collections import defaultdict
from pathlib import Path
from typing import Any, Final

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA, load_json_cached  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("compute_700_sample_complexity")

A5: Final[str] = "a5_676f_detection_matrix.json"
REF_692: Final[str] = "692_environment_paired_experiment.json"
OUT_JSON: Final[Path] = ROOT / "data" / "700_sample_complexity.json"

ASSETS: Final[tuple[str, ...]] = (
    "asan", "ubsan", "tsan", "compiler-warn",
    "wunsequenced", "cross-compile", "linker", "compile-time",
)
PRODUCTIVE_5: Final[tuple[str, ...]] = ("asan", "ubsan", "tsan", "compiler-warn", "cross-compile")
E1_SUP: Final[tuple[str, ...]] = ("asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker")
E2_SUP: Final[tuple[str, ...]] = ("compiler-warn", "cross-compile", "linker")


# ══════════════════════════════════════════════════════════════════════════
# 正态分位数（Acklam 有理逼近，精度 ~1e-9）
# ══════════════════════════════════════════════════════════════════════════
def z(p: float) -> float:
    if not 0.0 < p < 1.0:
        raise ValueError("p must be in (0,1)")
    a = (-3.969683028665376e+01, 2.209460984245205e+02, -2.759285104469687e+02,
         1.383577518672690e+02, -3.066479806614716e+01, 2.506628277459239e+00)
    b = (-5.447609879822406e+01, 1.615858368580409e+02, -1.556989798598866e+02,
         6.680131188771972e+01, -1.328068155288572e+01)
    c = (-7.784894002430293e-03, -3.223964580411365e-01, -2.400758277161838e+00,
         -2.549732539343734e+00, 4.374664141464968e+00, 2.938163982698783e+00)
    d = (7.784695709041462e-03, 3.224671290700398e-01, 2.445134137142996e+00,
         3.754408661907416e+00)
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


def kl_bernoulli(p: float, q: float) -> float:
    """KL(p‖q)（nats）；p 或 q 为 0/1 时按极限处理。"""
    out = 0.0
    if p > 0:
        out += p * math.log(p / q) if q > 0 else math.inf
    if p < 1:
        out += (1 - p) * math.log((1 - p) / (1 - q)) if q < 1 else math.inf
    return out


# ══════════════════════════════════════════════════════════════════════════
# 样本复杂度公式
# ══════════════════════════════════════════════════════════════════════════
def sample_complexity(psi: float, eps: float, alpha: float = 0.05, power: float = 0.8) -> dict[str, Any]:
    """给定 (ψ, ε) 返回所需不一致对数 m 与总样本数 n（正态近似）。

    ψ = 不一致率；ε = 边际率差（|ε| ≤ ψ）。
    """
    if psi <= 0 or abs(eps) <= 0:
        return {"psi": psi, "epsilon": eps, "pi": None, "m_discordant": None,
                "n_total": None, "detectable_by_paired_design": False,
                "reason": "逐样本裁决在口径变化下**完全相同**（ψ = 0）⇒ 配对设计下功效恒为 0 ⇒ n = ∞"}
    pi = (1.0 + eps / psi) / 2.0
    if not 0.0 <= pi <= 1.0:
        return {"psi": psi, "epsilon": eps, "pi": pi, "m_discordant": None,
                "n_total": None, "detectable_by_paired_design": False,
                "reason": "|ε| > ψ 不可能（边际率差不可能超过不一致率）"}
    # ⚠ 边界情形 π = 1 或 0（**完全单向**，本数据正是如此：c = 0）**必须允许**：
    #   此时符号检验功效最大，所需不一致对最少。第一版用 0 < π < 1 把这两种情形
    #   误判为"不可检出"，导致 Type I/II 都报 n = ∞。改用**精确二项**判据。
    if pi in (0.0, 1.0):
        m_exact = math.ceil(math.log(alpha / 2.0) / math.log(0.5))
        return {
            "psi": round(psi, 6), "epsilon": round(eps, 6), "pi": round(pi, 6),
            "m_discordant": m_exact,
            "n_total": math.ceil(m_exact / psi),
            "detectable_by_paired_design": True,
            "reason": (f"完全单向（π = {pi}）⇒ 用**精确二项**判据 m ≥ log(α/2)/log(1/2) = {m_exact} "
                       "（正态近似在此退化，不用）"),
        }
    za = z(1 - alpha / 2)
    zb = z(power)
    num = (za * math.sqrt(0.25) + zb * math.sqrt(pi * (1 - pi))) ** 2
    m = num / (pi - 0.5) ** 2
    return {
        "psi": round(psi, 6), "epsilon": round(eps, 6), "pi": round(pi, 6),
        "m_discordant": math.ceil(m),
        "n_total": math.ceil(m / psi),
        "detectable_by_paired_design": True,
        "z_alpha_over_2": round(za, 6), "z_power": round(zb, 6),
        "reason": "正态近似（符号检验 / 精确 McNemar）",
    }


def kl_floor(psi: float, eps: float, beta: float = 0.2) -> dict[str, Any]:
    """信息论地板：由 Chernoff–Stein 引理，m ≥ log(1/β)/KL(π‖1/2)。"""
    if psi <= 0 or abs(eps) <= 0:
        return {"m_lower_bound": None, "n_lower_bound": None,
                "reason": "ψ = 0 ⇒ KL = 0 ⇒ 下界为 ∞"}
    pi = (1.0 + eps / psi) / 2.0
    if not 0.0 <= pi <= 1.0:
        return {"m_lower_bound": None, "n_lower_bound": None, "reason": "π 越界"}
    if pi in (0.0, 1.0):
        return {"pi": pi, "kl_nats": round(math.log(2.0), 6),
                "m_lower_bound": math.ceil(math.log(1.0 / beta) / math.log(2.0)),
                "n_lower_bound": math.ceil(math.log(1.0 / beta) / math.log(2.0) / psi),
                "note": "完全单向：KL(Bernoulli(1)‖Bernoulli(1/2)) = log 2"}
    kl = kl_bernoulli(pi, 0.5)
    m = math.log(1.0 / beta) / kl
    return {
        "pi": round(pi, 6), "kl_nats": round(kl, 6),
        "m_lower_bound": math.ceil(m), "n_lower_bound": math.ceil(m / psi),
        "note": "Chernoff–Stein：m ≥ log(1/β)/KL(π‖1/2)；这是**地板**（不含 α 的两侧修正）",
    }


# ══════════════════════════════════════════════════════════════════════════
# 从冻结矩阵量 (ψ, ε)
# ══════════════════════════════════════════════════════════════════════════
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


def measure_pairs() -> dict[str, Any]:
    """从 A5 的 566 条 evaluation 样本量出各型的 (ψ, ε)。"""
    doc = load_json_cached(DATA / A5)
    ref = load_json_cached(DATA / REF_692)
    ev = [s for s in doc["samples"] if s.get("split") == "evaluation"]

    def stats(v_before: list[str], v_after: list[str]) -> dict[str, Any]:
        n = len(v_before)
        b = sum(1 for i in range(n) if v_before[i] == "catch" and v_after[i] != "catch")
        c = sum(1 for i in range(n) if v_before[i] != "catch" and v_after[i] == "catch")
        disc = b + c
        eps = (b - c) / n
        return {"n": n, "b": b, "c": c, "discordant": disc,
                "psi": disc / n, "epsilon_abs": abs(eps), "epsilon_signed": eps}

    pairs: dict[str, Any] = {}
    v_full = [_or({a: _verdict((s.get("per_asset") or {}).get(a, "unknown")) for a in ASSETS}, ASSETS)
              for s in ev]
    # Type I：口径变化 = 剔除 3 个退化资产（等价于只保留 5 个有效资产）
    v_clean = [_or({a: _verdict((s.get("per_asset") or {}).get(a, "unknown")) for a in ASSETS},
                   PRODUCTIVE_5) for s in ev]
    pairs["type_I_composition_drop_degenerate"] = stats(v_full, v_clean)

    # Type II：环境变化 E1 → E2
    v_e1 = [_or({a: _verdict((s.get("per_asset") or {}).get(a, "unknown")) for a in ASSETS}, E1_SUP)
            for s in ev]
    v_e2 = [_or({a: _verdict((s.get("per_asset") or {}).get(a, "unknown")) for a in ASSETS}, E2_SUP)
            for s in ev]
    pairs["type_II_environment_E1_to_E2"] = stats(v_e1, v_e2)

    # Type III / IV：逐样本裁决**完全不变** ⇒ ψ = 0
    pairs["type_III_label_vocabulary"] = {
        "n": len(ev), "b": 0, "c": 0, "discordant": 0, "psi": 0.0,
        "epsilon_abs": 0.0, "epsilon_signed": 0.0,
        "why": "标签词表变化**不改变任何逐样本裁决** ⇒ 配对设计下 ψ = 0（698-A Type III 已证）",
    }
    pairs["type_IV_aggregation_rule"] = {
        "n": len(ev), "b": 0, "c": 0, "discordant": 0, "psi": 0.0,
        "epsilon_abs": 0.0, "epsilon_signed": 0.0,
        "why": "聚合规则变化**不改变任何逐样本裁决** ⇒ 配对设计下 ψ = 0（698-A Type IV 已证）",
    }
    return {"pairs": pairs, "n_evaluation": len(ev), "e1_supported": list(E1_SUP),
            "e2_supported": list(E2_SUP), "reference_692_e2": ref["frames"]["A5_evaluation_566"]["E2_native_unaware"]}


# ══════════════════════════════════════════════════════════════════════════
# 3 种采样策略的模拟
# ══════════════════════════════════════════════════════════════════════════
def mcnemar_exact(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(k + 1)) / (2.0 ** n)
    return min(1.0, 2.0 * tail)


def strategy_simulation(n_trials: int = 400, seed: int = 700) -> dict[str, Any]:
    """3 种策略：均匀 / 分层比例 / Neyman 最优（用**真值**层不一致率，作为上限）。"""
    doc = load_json_cached(DATA / A5)
    ev = [s for s in doc["samples"] if s.get("split") == "evaluation"]
    v1 = [_or({a: _verdict((s.get("per_asset") or {}).get(a, "unknown")) for a in ASSETS}, E1_SUP)
          for s in ev]
    v2 = [_or({a: _verdict((s.get("per_asset") or {}).get(a, "unknown")) for a in ASSETS}, E2_SUP)
          for s in ev]
    groups = [str(s.get("defect_group") or "unknown") for s in ev]
    n = len(ev)
    by_g: dict[str, list[int]] = defaultdict(list)
    for i, g in enumerate(groups):
        by_g[g].append(i)

    disc_flag = [1 if v1[i] != v2[i] else 0 for i in range(n)]
    g_rate = {g: (sum(disc_flag[i] for i in idx) / len(idx)) for g, idx in by_g.items()}

    def run(strategy: str, budget: int, rng: random.Random) -> bool:
        if strategy == "uniform":
            idx = rng.sample(range(n), budget)
        elif strategy == "stratified_proportional":
            idx = []
            for g, pool in by_g.items():
                take = int(round(budget * len(pool) / n))
                idx.extend(rng.sample(pool, min(take, len(pool))))
            idx = list(set(idx))[:budget]
        else:  # neyman_oracle
            w = {g: len(by_g[g]) * math.sqrt(max(g_rate[g], 1e-6) * (1 - g_rate[g])) for g in by_g}
            tot = sum(w.values())
            idx = []
            for g, pool in by_g.items():
                take = int(round(budget * w[g] / tot)) if tot else 0
                idx.extend(rng.sample(pool, min(take, len(pool))))
            idx = list(set(idx))[:budget]
        if not idx:
            return False
        b = sum(1 for i in idx if v1[i] == "catch" and v2[i] != "catch")
        c = sum(1 for i in idx if v1[i] != "catch" and v2[i] == "catch")
        return mcnemar_exact(b, c) < 0.05

    out: dict[str, Any] = {"n": n, "trials": n_trials, "budgets": {},
                           "stratum_discordance_rates": {g: round(g_rate[g], 4) for g in sorted(g_rate)}}
    for budget in (5, 8, 10, 12, 15, 20, 30, 50):
        row: dict[str, Any] = {}
        for si, strategy in enumerate(("uniform", "stratified_proportional", "neyman_oracle")):
            rng = random.Random(seed + budget * 10 + si)
            hits = sum(1 for _ in range(n_trials) if run(strategy, budget, rng))
            row[strategy] = round(hits / n_trials, 4)
        out["budgets"][str(budget)] = row
    return out


# ══════════════════════════════════════════════════════════════════════════
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="700-C 信息论下界与样本复杂度（只读）")
    ap.add_argument("--trials", type=int, default=400)
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    args = ap.parse_args(argv)

    meas = measure_pairs()
    comp: dict[str, Any] = {}
    for name, st in meas["pairs"].items():
        comp[name] = {
            "measured": st,
            "required": sample_complexity(st["psi"], st["epsilon_abs"]),
            "kl_floor": kl_floor(st["psi"], st["epsilon_abs"]),
        }

    # 一般公式表：ε 与 ψ 的网格
    grid: list[dict[str, Any]] = []
    for psi in (0.05, 0.1, 0.2, 0.35, 0.5):
        for frac in (0.25, 0.5, 0.9, 1.0):
            eps = psi * frac
            r = sample_complexity(psi, eps)
            grid.append({"psi": psi, "epsilon": round(eps, 4), "epsilon_over_psi": frac,
                         "m_discordant": r["m_discordant"], "n_total": r["n_total"]})

    sim = strategy_simulation(n_trials=args.trials)

    doc: dict[str, Any] = {
        "schema": "queyi-700/sample-complexity/v1",
        "generated_by": "tools/compute_700_sample_complexity.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "formulation": {
            "H0": "无漂移（两个口径的边际率相同）",
            "H1": "有漂移，|边际率差| ≥ ε",
            "design": "配对（同一样本两个口径）⇒ 对不一致对做符号检验（= 精确 McNemar）",
            "psi": "不一致率 Pr[两口径裁决不同]",
            "pi": "方向概率 Pr[方向 | 不一致]",
            "identity": "ε = ψ·(2π − 1)",
            "formula": ("m ≥ (z_{1−α/2}·√(1/4) + z_{1−β}·√(π(1−π)))² / (π−1/2)²；n = m/ψ"
                        "（α = 0.05, power = 0.8）"),
            "kl_floor": "Chernoff–Stein：m ≥ log(1/β)/KL(π‖1/2)",
        },
        "measured_pairs": meas,
        "sample_complexity_by_type": comp,
        "general_grid": grid,
        "strategy_simulation": sim,
        "comparison_with_698B": {
            "698B_finding": "B=15 时均匀 0.505 vs 两阶段自适应 0.280；B≥60 全部饱和",
            "本批新增": "加入分层比例与 Neyman（真值）两种策略；Neyman 是**可达到的上限**",
            "gap_to_lower_bound": "见 strategy_simulation 与 sample_complexity_by_type 的 kl_floor 列",
        },
        "honest_limits": [
            "样本复杂度用**正态近似**（符号检验）；ψ 小时近似变差。",
            "KL 地板不含 α 的两侧修正 ⇒ 比实际所需小（是**地板**不是估计）。",
            "Type III/IV 的 ψ = 0 是**结构性**结论（698-A 已证逐样本裁决不变），不是测量噪声。",
            "Neyman 用**真值**层不一致率 ⇒ 是**上界**（现实中需试点估计，698-B 已示其代价）。",
            "策略模拟只在 Queyi 的 566 条 + 一个环境对上做；不声称对其他漂移幅度成立。",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    _log.info("已写出 %s", args.out)

    print("== 700-C 样本复杂度与信息论下界（只读）==")
    for name, c in comp.items():
        st = c["measured"]
        r = c["required"]
        if r["detectable_by_paired_design"]:
            print(f"  {name:<38} ψ={st['psi']:.4f} ε={st['epsilon_abs']:.4f} "
                  f"⇒ m={r['m_discordant']} n={r['n_total']}（KL 地板 n={c['kl_floor']['n_lower_bound']}）")
        else:
            print(f"  {name:<38} ψ={st['psi']:.4f} ε={st['epsilon_abs']:.4f} ⇒ **配对设计不可检出（n=∞）**")
    print("\n  策略模拟（检出概率）：")
    for b, row in sim["budgets"].items():
        print(f"    B={b:<3} 均匀={row['uniform']:.3f}  分层比例={row['stratified_proportional']:.3f}  "
              f"Neyman(真值)={row['neyman_oracle']:.3f}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
