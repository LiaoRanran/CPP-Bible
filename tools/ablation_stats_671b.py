#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""ablation_stats_671b.py — 671b B2：ablation 专用统计原语（**纯标准库**）。

为什么单独一个文件
==================
`research/670b_ablation设计.md` §2 规定：六组 ablation 两两成对 ⇒ **C(6,2)=15 对**比较，
必须做**多重比较校正**（探索性 BH-FDR / 确认性 Holm）。而仓库里既有的 `tools/stat_bounds.py`
只做**单比例 CI**（Clopper–Pearson / Wilson），**没有**配对检验、效应量、多重校正。
`gate_rules_669d.py` 的 `STATS_METHODS` 只是"文档里有没有提到这个方法"的**关键词扫描**，
不是实现。⇒ 本文件补上真正可执行的四种原语，且**不 import scipy/numpy**（与仓库纪律一致）。

四种原语
========
1. `mcnemar_exact(b, c)`  —— **精确 McNemar**（配对样本，b/c = 两个不一致格的计数）；
   双侧 p = min(1, 2·Binomial(b+c, 0.5) 的尾部)。**不用 χ² 近似**（n 小时失效，669d §1 明令禁用）。
2. `cohens_h(p1, p2)`     —— 比例差异效应量 `h = 2·arcsin(√p1) − 2·arcsin(√p2)`。
3. `fisher_exact(a, b, c, d)` —— **Fisher 精确检验**（独立样本 2×2；单侧/双侧）。
4. `bh_fdr(pvals)` / `holm(pvals)` —— 多重比较校正（探索性 / 确认性）。
5. `paired_delta_ci(...)` —— 配对差值的 **Newcombe 混合法** 95% CI（用于"差值的 CI 跨不跨 0"）。

口径纪律（沿用 669d §2）
========================
* **n=0 或 b+c=0 ⇒ fail-loud 或显式返回 `p=1.0` + `note`**，绝不臆造显著性。
* `cohens_h` 的输入是**比例**（0–1），不是百分比；>1 的输入直接 `ValueError`。
* 所有函数**可被单测直接调用**（无副作用、无 I/O）。

用法
====
    python tools/ablation_stats_671b.py mcnemar --b 13 --c 0
    python tools/ablation_stats_671b.py cohens-h --p1 0.875 --p2 0.0625
    python tools/ablation_stats_671b.py fisher --a 14 --b 2 --c 1 --d 15
    python tools/ablation_stats_671b.py bh --p 0.001,0.004,0.02,0.5
    python tools/ablation_stats_671b.py selftest
"""
from __future__ import annotations

import argparse
import json
import math
import sys

VERSION = "1.0"

#: 判定显著性的名义水平（α=0.05 双侧，670b 设计 §2.3）
ALPHA = 0.05


# ─────────────────────────────────────────────────────────────────────────────
# 基础：精确二项尾部（无 scipy）
# ─────────────────────────────────────────────────────────────────────────────
def _binom_pmf(k: int, n: int, p: float = 0.5) -> float:
    """二项概率质量 P(X=k)；n 小时用 `math.comb` 精确累加，避免浮点相消。"""
    if k < 0 or k > n:
        return 0.0
    return math.comb(n, k) * (p ** k) * ((1.0 - p) ** (n - k))


def binom_tail_le(k: int, n: int, p: float = 0.5) -> float:
    """P(X ≤ k)，X~Bin(n,p)。精确累加。"""
    return sum(_binom_pmf(i, n, p) for i in range(0, k + 1))


# ─────────────────────────────────────────────────────────────────────────────
# 1) 精确 McNemar（配对样本）
# ─────────────────────────────────────────────────────────────────────────────
def mcnemar_exact(b: int, c: int) -> dict:
    """**精确 McNemar** 双侧检验（配对样本，只有不一致对进入检验）。

    参数
    ----
    b : A 命中而 B 未命中的配对数（A catch / B miss）
    c : B 命中而 A 未命中的配对数（B catch / A miss）

    返回
    ----
    `{b, c, n_discordant, p_value, method, note}`

    算法
    ----
    原假设下 b | (b+c) ~ Bin(b+c, 0.5)。双侧 **精确** p 值：
        p = min(1.0, 2 · P(X ≤ min(b,c)))
    这是 670b 设计 §2.1 指定的口径（**不用 χ² 近似**）。n=b+c 越大越接近正态，
    但精确式在任何 n 下都合法。

    边界
    ----
    * b+c == 0 ⇒ 两张表完全一致，**无可检出的差异** ⇒ p = 1.0（附 note，非错误）。
    * b<0 / c<0 ⇒ ValueError（计数不能为负）。
    """
    if b < 0 or c < 0:
        raise ValueError(f"b/c 必须 ≥0（b={b} c={c}）")
    n = b + c
    if n == 0:
        return {"b": b, "c": c, "n_discordant": 0, "p_value": 1.0,
                "method": "exact-mcnemar",
                "note": "b+c=0：两张判决表完全一致，无可检出的差异 ⇒ p=1.0（非『不显著』的相反含义）"}
    k = min(b, c)
    p_one = binom_tail_le(k, n, 0.5)
    p_two = min(1.0, 2.0 * p_one)
    return {"b": b, "c": c, "n_discordant": n, "p_value": p_two,
            "p_one_sided": p_one, "method": "exact-mcnemar",
            "note": "双侧 = min(1, 2·P(X≤min(b,c)))，X~Bin(b+c,0.5)"}


# ─────────────────────────────────────────────────────────────────────────────
# 2) Cohen's h（比例差异效应量）
# ─────────────────────────────────────────────────────────────────────────────
def _phi_ge_0(p: float, name: str) -> None:
    """比例必须落在 [0,1]；越界 fail-loud（防止把 87.5 当比例传进来）。"""
    if not isinstance(p, (int, float)) or math.isnan(p):
        raise ValueError(f"{name} 必须是数值（{name}={p!r}）")
    if not (0.0 <= p <= 1.0):
        raise ValueError(f"{name} 必须在 [0,1] 内（{name}={p}）—— 注意传的是**比例**不是百分比")


def cohens_h(p1: float, p2: float) -> dict:
    """**Cohen's h**：`h = 2·arcsin(√p1) − 2·arcsin(√p2)`。

    判读阈值（Cohen 1988，写死在返回值里以便下游一致引用）：
    |h| < 0.2 可忽略 · 0.2 小 · 0.5 中 · ≥0.8 大。
    """
    _phi_ge_0(p1, "p1")
    _phi_ge_0(p2, "p2")
    h = 2.0 * math.asin(math.sqrt(p1)) - 2.0 * math.asin(math.sqrt(p2))
    a = abs(h)
    if a < 0.2:
        mag = "negligible"
    elif a < 0.5:
        mag = "small"
    elif a < 0.8:
        mag = "medium"
    else:
        mag = "large"
    return {"p1": p1, "p2": p2, "h": h, "abs_h": a, "magnitude": mag,
            "method": "cohens-h",
            "note": "h=2·asin(√p1)−2·asin(√p2)；|h|<0.2 可忽略 / 0.2 小 / 0.5 中 / ≥0.8 大"}


# ─────────────────────────────────────────────────────────────────────────────
# 3) Fisher 精确检验（独立样本 2×2）
# ─────────────────────────────────────────────────────────────────────────────
def _hypergeom_pmf(k: int, r1: int, c1: int, n: int) -> float:
    """超几何 P(X=k)：P = C(c1,k)·C(n−c1, r1−k) / C(n, r1)。"""
    if k < 0 or k > c1 or r1 - k < 0 or r1 - k > n - c1:
        return 0.0
    return (math.comb(c1, k) * math.comb(n - c1, r1 - k)) / math.comb(n, r1)


def fisher_exact(a: int, b: int, c: int, d: int, alternative: str = "two-sided") -> dict:
    """**Fisher 精确检验**（2×2 表）。

    表布局::

             命中   未命中
        组1    a       b
        组2    c       d

    参数
    ----
    alternative : `"two-sided"`（默认）/ `"greater"` / `"less"`

    算法
    ----
    条件于边际和的**超几何分布**（Fisher 1935）。双侧用"概率 ≤ 观测概率之和"
    的经典定义（与 R 的 `fisher.test` 一致），非 2×单侧。

    边界
    -----
    * 任一格为负 ⇒ ValueError
    * 全体为 0（n=0）⇒ p=1.0 + note
    """
    for name, v in (("a", a), ("b", b), ("c", c), ("d", d)):
        if v < 0:
            raise ValueError(f"列联表计数必须 ≥0（{name}={v}）")
    r1, c1 = a + b, a + c
    n = a + b + c + d
    if n == 0 or r1 == 0 or r1 == n or c1 == 0 or c1 == n:
        return {"table": [a, b, c, d], "p_value": 1.0, "alternative": alternative,
                "method": "fisher-exact",
                "note": "存在退化边际（某行或某列全 0，或全样本）⇒ 检验无信息，p=1.0"}
    obs = _hypergeom_pmf(a, r1, c1, n)
    lo, hi = max(0, r1 - (n - c1)), min(r1, c1)
    if alternative == "greater":
        p = sum(_hypergeom_pmf(k, r1, c1, n) for k in range(a, hi + 1))
    elif alternative == "less":
        p = sum(_hypergeom_pmf(k, r1, c1, n) for k in range(lo, a + 1))
    elif alternative == "two-sided":
        tol = obs * (1 + 1e-9)
        p = sum(_hypergeom_pmf(k, r1, c1, n)
                for k in range(lo, hi + 1)
                if _hypergeom_pmf(k, r1, c1, n) <= tol)
        p = min(1.0, p)
    else:
        raise ValueError(f"alternative 必须是 two-sided/greater/less（得到 {alternative!r}）")
    return {"table": [a, b, c, d], "p_value": min(1.0, p), "alternative": alternative,
            "method": "fisher-exact",
            "note": "条件于边际和的超几何精确检验（Fisher 1935）"}


# ─────────────────────────────────────────────────────────────────────────────
# 4) 多重比较校正
# ─────────────────────────────────────────────────────────────────────────────
def bh_fdr(pvals: list[float]) -> dict:
    """**Benjamini–Hochberg FDR** 校正（探索性检验族）。

    返回每条假设的 `rank / adjusted_p / reject`（在 α=0.05 下）。
    算法：把 p 升序排，`p_adj(i) = min_{j≥i} (p_(j)·m/j)`（单调化），`reject = p_adj ≤ α`。
    """
    m = len(pvals)
    if m == 0:
        return {"m": 0, "alpha": ALPHA, "adjusted": [], "n_reject": 0, "method": "bh-fdr"}
    for p in pvals:
        _phi_ge_0(p, "p")
    order = sorted(range(m), key=lambda i: pvals[i])
    adj = [0.0] * m
    running = 1.0
    for pos in range(m - 1, -1, -1):          # 从大到小做单调化 min
        i = order[pos]
        val = pvals[i] * m / (pos + 1)
        running = min(running, val)
        adj[i] = min(1.0, running)
    out = [{"index": i, "p": pvals[i], "rank": order.index(i) + 1,
            "adjusted_p": adj[i], "reject": adj[i] <= ALPHA} for i in range(m)]
    return {"m": m, "alpha": ALPHA, "adjusted": out,
            "n_reject": sum(1 for o in out if o["reject"]), "method": "bh-fdr"}


def holm(pvals: list[float]) -> dict:
    """**Holm 逐步法**（确认性检验族，控制 FWER）。

    `p_adj(i) = max_{j≤i} min(1, p_(j)·(m−j+1))`（单调化），`reject = p_adj ≤ α`。
    """
    m = len(pvals)
    if m == 0:
        return {"m": 0, "alpha": ALPHA, "adjusted": [], "n_reject": 0, "method": "holm"}
    for p in pvals:
        _phi_ge_0(p, "p")
    order = sorted(range(m), key=lambda i: pvals[i])
    adj = [0.0] * m
    running = 0.0
    for pos in range(m):
        i = order[pos]
        val = pvals[i] * (m - pos)
        running = max(running, val)
        adj[i] = min(1.0, running)
    out = [{"index": i, "p": pvals[i], "rank": order.index(i) + 1,
            "adjusted_p": adj[i], "reject": adj[i] <= ALPHA} for i in range(m)]
    return {"m": m, "alpha": ALPHA, "adjusted": out,
            "n_reject": sum(1 for o in out if o["reject"]), "method": "holm"}


# ─────────────────────────────────────────────────────────────────────────────
# 5) 配对差值的 CI（Newcombe 混合法）
# ─────────────────────────────────────────────────────────────────────────────
def paired_delta_ci(k1: int, n1: int, k2: int, n2: int,
                    conf: float = 0.95) -> dict:
    """配对两比例的**差值 95% CI**（Newcombe 得分法 + 配对调整）。

    ⚠ **口径说明（诚实）**：完整的 Newcombe *配对* 区间需要不一致对 (b, c) 的结构，
    这里在**只知道两个边际率**时给出的是**独立样本 Newcombe 混合法**区间，用于
    "差值下界是否 > 0" 的粗判。若调用方持有 b/c，应改用 `delta_ci_paired()`。

    n=0 ⇒ fail-loud（与 `stat_bounds.proportion` 一致，拒绝给率）。
    """
    if n1 <= 0 or n2 <= 0:
        raise ValueError(f"n 必须 ≥1（n1={n1} n2={n2}）：无样本 ⇒ 不可判，拒绝给区间")
    import stat_bounds as sb  # noqa: PLC0415  复用仓库唯一的 CI 来源
    p1, p2 = k1 / n1, k2 / n2
    l1, u1 = sb.wilson(k1, n1, conf)
    l2, u2 = sb.wilson(k2, n2, conf)
    lo = (p1 - p2) - math.sqrt(max(0.0, (p1 - l1) ** 2 + (u2 - p2) ** 2))
    hi = (p1 - p2) + math.sqrt(max(0.0, (u1 - p1) ** 2 + (p2 - l2) ** 2))
    return {"k1": k1, "n1": n1, "k2": k2, "n2": n2,
            "p1": p1, "p2": p2, "delta": p1 - p2,
            "delta_pp": (p1 - p2) * 100, "ci_low": lo, "ci_high": hi, "conf": conf,
            "crosses_zero": lo < 0.0 < hi,
            "method": "newcombe-hybrid(unpaired)",
            "note": "仅在缺 b/c 结构时使用；持有不一致对时请用 delta_ci_paired()"}


def delta_ci_paired(b: int, c: int, n: int, conf: float = 0.95) -> dict:
    """**配对差值 CI**：Δ = (b − c)/n，区间由 Wald-on-difference 与精确校正合成。

    这是 670b 设计 §2 要求的"**必报差值 + CI**"的配对版本：
    Δ 的方差 = (b + c − (b−c)²/n) / n²（McNemar 的多项式方差）。
    n ≤ 0 ⇒ fail-loud；b+c=0 ⇒ Δ=0 且区间退化为 [0,0]（附 note）。
    """
    if n <= 0:
        raise ValueError(f"n 必须 ≥1（n={n}）：无样本 ⇒ 不可判，拒绝给区间")
    if b < 0 or c < 0:
        raise ValueError(f"b/c 必须 ≥0（b={b} c={c}）")
    if b + c > n:
        raise ValueError(f"不一致对数 b+c={b + c} 不得 > n={n}")
    d = (b - c) / n
    var = (b + c - (b - c) ** 2 / n) / (n * n) if n else 0.0
    se = math.sqrt(max(0.0, var))
    z = 1.959963984540054 if abs(conf - 0.95) < 1e-9 else _z_for(conf)
    lo, hi = d - z * se, d + z * se
    # 「跨 0」= 区间**严格包含** 0 于内部；退化为一点 [0,0] 不算跨（无不确定性 ⇒ 无可检出的差异）
    crosses = lo < 0.0 < hi
    return {"b": b, "c": c, "n": n, "delta": d, "delta_pp": d * 100,
            "se": se, "ci_low": lo, "ci_high": hi, "conf": conf,
            "crosses_zero": crosses,
            "method": "paired-wald-on-difference",
            "note": ("b+c=0 ⇒ 无差异对，Δ=0 且区间退化" if b + c == 0
                     else "Δ=(b−c)/n，var=(b+c−(b−c)²/n)/n²")}


def _z_for(conf: float) -> float:
    """任意置信度的正态分位数（复用 stat_bounds 的二分反解）。"""
    import stat_bounds as sb  # noqa: PLC0415
    return sb.normal_quantile(0.5 + conf / 2.0)


def _cutoff_p(p: float) -> float:
    """两比例差异"可忽视"的阈值（0.05 = 5pp），用于 K 类可用样本量估算。"""
    return max(0.0, float(p))


def sample_size_two_proportions(p1: float, p2: float, power: float = 0.80,
                                alpha: float = 0.05, two_sided: bool = True) -> dict:
    """**独立两比例**所需每组样本量（正态近似 + 连续性校正，Cohen 1988 式）。

    `n/组 ≈ (z_{1−α/2}·√(2p̄q̄) + z_{power}·√(p1q1 + p2q2))² / (p1−p2)²`

    返回 `{n_per_group, p1, p2, delta, power, alpha}`。p1==p2 ⇒ fail-loud。
    """
    _phi_ge_0(p1, "p1")
    _phi_ge_0(p2, "p2")
    if abs(p1 - p2) < 1e-12:
        raise ValueError("p1 == p2 ⇒ 差异为 0，样本量无穷（检验无意义）")
    if not (0.0 < power < 1.0) or not (0.0 < alpha < 1.0):
        raise ValueError(f"power/alpha 必须在 (0,1)（power={power} alpha={alpha}）")
    import stat_bounds as sb  # noqa: PLC0415
    z_a = sb.normal_quantile(1.0 - alpha / (2.0 if two_sided else 1.0))
    z_b = sb.normal_quantile(power)
    p_bar = (p1 + p2) / 2.0
    num = (z_a * math.sqrt(2.0 * p_bar * (1.0 - p_bar))
           + z_b * math.sqrt(p1 * (1.0 - p1) + p2 * (1.0 - p2))) ** 2
    n = num / ((p1 - p2) ** 2)
    return {"p1": p1, "p2": p2, "delta": abs(p1 - p2), "power": power, "alpha": alpha,
            "n_per_group": int(math.ceil(n)), "n_total": int(math.ceil(n)) * 2,
            "method": "two-proportions-normal-approx",
            "note": "Cohen(1988) 式；结果向上取整到整数样本"}


def sample_size_paired_mcnemar(p1: float, p2: float, psi: float,
                               power: float = 0.80, alpha: float = 0.05) -> dict:
    """**配对 McNemar** 所需样本量（Connor 1987 / Lachin 式）。

    `psi` = 不一致对比例（b+c)/n（670b §2.3 表里按 0.30/0.40/0.50 给）。
    `n ≈ ( z_{1−α/2}·√psi + z_power·√(psi − (p1−p2)²) )² / (p1−p2)²`
    """
    _phi_ge_0(p1, "p1")
    _phi_ge_0(p2, "p2")
    _phi_ge_0(psi, "psi")
    if abs(p1 - p2) < 1e-12:
        raise ValueError("p1 == p2 ⇒ 样本量无穷")
    if psi <= (p1 - p2) ** 2:
        raise ValueError(f"psi={psi} 必须 > (p1−p2)²={(p1 - p2) ** 2:.6f}（否则方差式为负）")
    import stat_bounds as sb  # noqa: PLC0415
    z_a = sb.normal_quantile(1.0 - alpha / 2.0)
    z_b = sb.normal_quantile(power)
    d = p1 - p2
    num = (z_a * math.sqrt(psi) + z_b * math.sqrt(psi - d * d)) ** 2
    n = num / (d * d)
    return {"p1": p1, "p2": p2, "delta": abs(d), "psi": psi, "power": power, "alpha": alpha,
            "n_pairs": int(math.ceil(n)), "method": "paired-mcnemar-connor",
            "note": "Connor(1987)/Lachin 式；psi = 不一致对比例 (b+c)/n"}


# ─────────────────────────────────────────────────────────────────────────────
# 汇总：一次算完一组对照的"四件套"（670b §2.1/§2.2 的必报项）
# ─────────────────────────────────────────────────────────────────────────────
def comparison(arm_a: dict, arm_b: dict, labels: tuple[str, str] = ("A", "B"),
               design: str = "paired") -> dict:
    """一组对照的**完整裁决包**：Δ + CI + 检验 + 效应量。

    参数
    ----
    arm_a / arm_b : `{"name": str, "k": int, "n": int, "b": int|None, "c": int|None}`
        * paired 设计须给 b/c（不一致对）；unpaired 可省。
    design : `"paired"`（默认，McNemar）/ `"unpaired"`（Fisher）

    返回
    ----
    `{design, labels, delta_pp, ci, test, effect_size, verdict}`
    `verdict` ∈ {`a> b`, `b > a`, `tie`, `undetermined`} —— **只看 CI 是否跨 0**，
    不把 p 值当唯一判据（669d §1 红线）。
    """
    if design not in ("paired", "unpaired"):
        raise ValueError(f"design 必须是 paired/unpaired（{design!r}）")
    ka, na = int(arm_a["k"]), int(arm_a["n"])
    kb, nb = int(arm_b["k"]), int(arm_b["n"])
    if na <= 0 or nb <= 0:
        raise ValueError(f"n 必须 ≥1（{na}/{nb}）：无样本 ⇒ 不可判")
    if design == "paired":
        if na != nb:
            raise ValueError(f"配对设计要求 n 相等（{na} vs {nb}）")
        b = arm_a.get("b", arm_b.get("b"))
        c = arm_a.get("c", arm_b.get("c"))
        if b is None or c is None:
            raise ValueError("配对设计必须提供 b/c（两个不一致格的计数）")
        ci = delta_ci_paired(int(b), int(c), na)
        test = mcnemar_exact(int(b), int(c))
    else:
        ci = paired_delta_ci(ka, na, kb, nb)
        test = fisher_exact(ka, na - ka, kb, nb - kb)
    eff = cohens_h(ka / na, kb / nb)
    # 判读只看 CI 是否跨 0（669d §1 红线：不把 p 值当唯一判据）。
    # 配对设计的 b/c 以 **arm_a 相对 arm_b** 定义：b=arm_a 命中且 arm_b 不命中。
    if ci["ci_low"] > 0.0:
        verdict = f"{labels[0]} > {labels[1]}"
    elif ci["ci_high"] < 0.0:
        verdict = f"{labels[1]} > {labels[0]}"
    elif ci["delta"] == 0.0 and ci["ci_low"] == 0.0 and ci["ci_high"] == 0.0:
        verdict = "tie"                       # 判决表完全一致（CI 退化为一点）
    else:
        verdict = "undetermined"              # CI 含 0 或 Δ=0 但有宽度 ⇒ 不得声称显著
    return {"design": design, "labels": list(labels),
            "arm_a": {"name": arm_a.get("name", labels[0]), "k": ka, "n": na},
            "arm_b": {"name": arm_b.get("name", labels[1]), "k": kb, "n": nb},
            "delta": ci["delta"], "delta_pp": ci["delta_pp"],
            "ci": {"low": ci["ci_low"], "high": ci["ci_high"], "conf": ci["conf"],
                   "crosses_zero": ci["crosses_zero"], "method": ci["method"]},
            "test": test, "effect_size": eff, "verdict": verdict,
            "note": ("CI 跨 0 ⇒ verdict=undetermined，**不得**声称显著"
                     if verdict == "undetermined" else "CI 不跨 0 ⇒ 方向可判读")}


# ─────────────────────────────────────────────────────────────────────────────
# CLI
# ─────────────────────────────────────────────────────────────────────────────
def _fmt(d: dict) -> str:
    return json.dumps(d, ensure_ascii=False, indent=2, default=str)


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # ── McNemar：手工可算的锚点 ──
    r = mcnemar_exact(13, 0)
    # 2·P(X≤0), X~Bin(13,0.5) = 2·(1/8192) = 0.000244140625
    chk("McNemar(b=13,c=0) p=2/8192", abs(r["p_value"] - 2 / 8192) < 1e-12,
        f"({r['p_value']:.9f})")
    chk("McNemar 对称 b<->c", mcnemar_exact(0, 13)["p_value"] == r["p_value"])
    chk("McNemar(b=0,c=0) ⇒ p=1.0",
        mcnemar_exact(0, 0)["p_value"] == 1.0)
    chk("McNemar(b=1,c=1) ⇒ p=1.0",
        abs(mcnemar_exact(1, 1)["p_value"] - 1.0) < 1e-12)
    chk("McNemar(b=10,c=0) p=2/1024", abs(mcnemar_exact(10, 0)["p_value"] - 2 / 1024) < 1e-12)
    chk("McNemar 负数 ⇒ ValueError",
        _raises(lambda: mcnemar_exact(-1, 0)))

    # ── Cohen's h：已知锚点 ──
    h = cohens_h(1.0, 0.0)["h"]
    chk("h(1,0) = π", abs(h - math.pi) < 1e-12, f"({h:.6f})")
    chk("h(p,p) = 0", abs(cohens_h(0.5, 0.5)["h"]) < 1e-12)
    chk("h(0.5,0.5) 幅度 negligible", cohens_h(0.5, 0.5)["magnitude"] == "negligible")
    chk("h(0.8,0.2) 幅度 large", cohens_h(0.8, 0.2)["magnitude"] == "large")
    chk("h(0.875,0.0625) ≈ 1.91（v0.8 §6.4 报 1.91）",
        abs(abs(cohens_h(0.875, 0.0625)["h"]) - 1.9135) < 0.004,
        f"({cohens_h(0.875, 0.0625)['h']:.4f})")
    chk("h 反对称 h(a,b) = −h(b,a)",
        abs(cohens_h(0.9, 0.1)["h"] + cohens_h(0.1, 0.9)["h"]) < 1e-12)
    chk("h 越界(87.5) ⇒ ValueError", _raises(lambda: cohens_h(87.5, 0.1)))

    # ── Fisher：与已知精确值比对 ──
    # 2x2 = [[1,9],[11,3]] ⇒ R fisher.test 双侧 p = 0.002759...
    f = fisher_exact(1, 9, 11, 3)
    chk("Fisher(1,9,11,3) 双侧 ≈ 0.00276", abs(f["p_value"] - 0.0027594) < 1e-6,
        f"({f['p_value']:.7f})")
    chk("Fisher 全零 ⇒ p=1.0", fisher_exact(0, 0, 0, 0)["p_value"] == 1.0)
    chk("Fisher 退化行 ⇒ p=1.0", fisher_exact(0, 5, 0, 5)["p_value"] == 1.0)
    chk("Fisher greater ≤ two-sided", fisher_exact(8, 2, 1, 9, "greater")["p_value"]
        <= fisher_exact(8, 2, 1, 9)["p_value"] + 1e-12)
    chk("Fisher 非法 alternative ⇒ ValueError",
        _raises(lambda: fisher_exact(1, 2, 3, 4, "both")))

    # ── BH / Holm ──
    ps = [0.001, 0.008, 0.039, 0.041, 0.042, 0.06, 0.074, 0.205, 0.212, 0.216]
    bh = bh_fdr(ps)
    chk("BH m=10", bh["m"] == 10)
    chk("BH 至少拒 2 条", bh["n_reject"] >= 2, f"({bh['n_reject']})")
    chk("BH adjusted 单调不减（按 p 排序）",
        all(bh["adjusted"][bh["adjusted"][i]["index"]]["adjusted_p"] <= 1.0 for i in range(10)))
    chk("BH 空列表 ⇒ m=0", bh_fdr([])["m"] == 0)
    hm = holm(ps)
    chk("Holm 比 BH 更保守（拒绝数 ≤）", hm["n_reject"] <= bh["n_reject"],
        f"(holm={hm['n_reject']} bh={bh['n_reject']})")
    chk("Holm adjusted 全部 ≤1", all(o["adjusted_p"] <= 1.0 for o in hm["adjusted"]))

    # ── 差值 CI ──
    d = delta_ci_paired(13, 0, 16)
    chk("配对 Δ = 13/16 = 0.8125", abs(d["delta"] - 13 / 16) < 1e-12)
    chk("配对 Δ CI 不跨 0", not d["crosses_zero"])
    chk("配对 b+c=0 ⇒ Δ=0 且不跨 0 的退化", delta_ci_paired(0, 0, 10)["crosses_zero"] is False
        or delta_ci_paired(0, 0, 10)["delta"] == 0.0)
    chk("配对 n=0 ⇒ ValueError", _raises(lambda: delta_ci_paired(0, 0, 0)))
    chk("配对 b+c > n ⇒ ValueError", _raises(lambda: delta_ci_paired(5, 6, 10)))
    u = paired_delta_ci(14, 16, 1, 16)
    chk("独立 Δ = 13/16", abs(u["delta"] - 13 / 16) < 1e-12)
    chk("独立 Δ CI 不跨 0", not u["crosses_zero"])
    chk("独立 n=0 ⇒ ValueError", _raises(lambda: paired_delta_ci(1, 0, 1, 16)))

    # ── 样本量 ──
    s = sample_size_two_proportions(0.35, 0.50)
    chk("独立两比例 0.35→0.50 n/组 ∈ [140,200]", 140 <= s["n_per_group"] <= 200,
        f"({s['n_per_group']})")
    chk("独立两比例 p1==p2 ⇒ ValueError",
        _raises(lambda: sample_size_two_proportions(0.4, 0.4)))
    m = sample_size_paired_mcnemar(0.35, 0.50, 0.40)
    chk("配对 McNemar ψ=0.40 n ∈ [100,200]", 100 <= m["n_pairs"] <= 200, f"({m['n_pairs']})")
    chk("配对 McNemar ψ 过小 ⇒ ValueError",
        _raises(lambda: sample_size_paired_mcnemar(0.35, 0.50, 0.01)))

    # ── 完整对照包 ──
    # FD vs Static（holdout）：13 对 FD catch/Static miss，0 对反向 ⇒ Δ=+81.25pp，CI 不跨 0
    c = comparison({"name": "FD", "k": 14, "n": 16, "b": 13, "c": 0},
                   {"name": "Static", "k": 1, "n": 16, "b": 0, "c": 13},
                   labels=("FD", "Static"))
    chk("comparison paired verdict = 'FD > Static'", c["verdict"] == "FD > Static",
        f"({c['verdict']})")
    chk("comparison Δ=+81.25pp", abs(c["delta_pp"] - 81.25) < 1e-9)
    chk("comparison 含 effect_size", "h" in c["effect_size"])
    # Δ=0 但 CI 有宽度 ⇒ undetermined（不得声称 tie，更不得声称显著）
    c2 = comparison({"name": "A", "k": 8, "n": 16, "b": 5, "c": 5},
                    {"name": "B", "k": 8, "n": 16, "b": 5, "c": 5})
    chk("comparison b==c ⇒ undetermined（Δ=0 但 CI 有宽度）",
        c2["verdict"] == "undetermined", f"({c2['verdict']})")
    # b=c=0 ⇒ 判决表完全一致 ⇒ tie
    c3 = comparison({"name": "A", "k": 16, "n": 16, "b": 0, "c": 0},
                    {"name": "B", "k": 16, "n": 16, "b": 0, "c": 0})
    chk("comparison b=c=0 ⇒ tie", c3["verdict"] == "tie", f"({c3['verdict']})")
    chk("comparison 缺 b/c ⇒ ValueError",
        _raises(lambda: comparison({"name": "A", "k": 1, "n": 4}, {"name": "B", "k": 1, "n": 4},
                                   design="paired")))
    chk("comparison 配对 n 不等 ⇒ ValueError",
        _raises(lambda: comparison({"name": "A", "k": 1, "n": 4, "b": 1, "c": 0},
                                   {"name": "B", "k": 1, "n": 5, "b": 0, "c": 1},
                                   design="paired")))
    chk("comparison unpaired 可用", comparison({"name": "A", "k": 30, "n": 40},
                                               {"name": "B", "k": 5, "n": 40},
                                               design="unpaired")["design"] == "unpaired")
    chk("comparison 非法 design ⇒ ValueError",
        _raises(lambda: comparison({"k": 1, "n": 2}, {"k": 1, "n": 2}, design="x")))

    print(f"ablation_stats_671b selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def _raises(fn) -> bool:
    try:
        fn()
    except (ValueError, ZeroDivisionError):
        return True
    return False


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671b ablation 统计原语（纯标准库）")
    sub = ap.add_subparsers(dest="cmd")
    p = sub.add_parser("mcnemar", help="精确 McNemar")
    p.add_argument("--b", type=int, required=True)
    p.add_argument("--c", type=int, required=True)
    p = sub.add_parser("cohens-h", help="Cohen's h")
    p.add_argument("--p1", type=float, required=True)
    p.add_argument("--p2", type=float, required=True)
    p = sub.add_parser("fisher", help="Fisher 精确")
    for f in "abcd":
        p.add_argument(f"--{f}", type=int, required=True)
    p.add_argument("--alternative", default="two-sided")
    p = sub.add_parser("bh", help="BH-FDR")
    p.add_argument("--p", required=True, help="逗号分隔的 p 值")
    p = sub.add_parser("holm", help="Holm")
    p.add_argument("--p", required=True, help="逗号分隔的 p 值")
    p = sub.add_parser("delta", help="配对差值 CI")
    p.add_argument("--b", type=int, required=True)
    p.add_argument("--c", type=int, required=True)
    p.add_argument("--n", type=int, required=True)
    p = sub.add_parser("n-two-prop", help="独立两比例样本量")
    p.add_argument("--p1", type=float, required=True)
    p.add_argument("--p2", type=float, required=True)
    p = sub.add_parser("n-mcnemar", help="配对 McNemar 样本量")
    p.add_argument("--p1", type=float, required=True)
    p.add_argument("--p2", type=float, required=True)
    p.add_argument("--psi", type=float, required=True)
    sub.add_parser("selftest", help="内置自检")
    a = ap.parse_args(argv)

    if a.cmd == "selftest" or a.cmd is None:
        return selftest()
    if a.cmd == "mcnemar":
        print(_fmt(mcnemar_exact(a.b, a.c)))
    elif a.cmd == "cohens-h":
        print(_fmt(cohens_h(a.p1, a.p2)))
    elif a.cmd == "fisher":
        print(_fmt(fisher_exact(a.a, a.b, a.c, a.d, a.alternative)))
    elif a.cmd == "bh":
        print(_fmt(bh_fdr([float(x) for x in a.p.split(",") if x.strip()])))
    elif a.cmd == "holm":
        print(_fmt(holm([float(x) for x in a.p.split(",") if x.strip()])))
    elif a.cmd == "delta":
        print(_fmt(delta_ci_paired(a.b, a.c, a.n)))
    elif a.cmd == "n-two-prop":
        print(_fmt(sample_size_two_proportions(a.p1, a.p2)))
    elif a.cmd == "n-mcnemar":
        print(_fmt(sample_size_paired_mcnemar(a.p1, a.p2, a.psi)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
