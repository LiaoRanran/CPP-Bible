#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""563 · 把形容词算成数字：零误伤上界 / 拦截率置信区间 / 样本量公式。
纯标准库（beta 分布精确分位用数值反解），数据全来自本仓真实文件。
输出 _arch_v6/bounds_report.json + 控制台。
"""
import json
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent            # _arch_v6/ -> repo root


def beta_quantile(p, a, b, tol=1e-9):
    """Beta(a,b) 分位数（对整数/半整数 a,b 的二项后验等价物）：二分反解 regularized incomplete beta。"""
    from math import lgamma, exp, log

    def logbet(x):
        return lgamma(a) + lgamma(b) - lgamma(a + b)

    def ibf(x):
        # 连分式（Lentz）求 I_x(a,b)
        if x <= 0:
            return 0.0
        if x >= 1:
            return 1.0
        bt = exp(a * math.log(x) + b * math.log(1 - x) - logbet(x))
        if x < (a + 1) / (a + b + 2):
            return bt * betacf(a, b, x) / a
        return 1 - bt * betacf(b, a, 1 - x) / b

    def betacf(a, b, x):
        MAXIT = 200
        EPS = 3e-12
        qab, qap, qam = a + b, a + 1, a - 1
        c = 1.0
        d = 1.0 - qab * x / qap
        if abs(d) < 1e-30:
            d = 1e-30
        d = 1 / d
        h = d
        for m in range(1, MAXIT + 1):
            m2 = 2 * m
            aa = m * (b - m) * x / ((qam + m2) * (a + m2))
            d = 1 + aa * d
            if abs(d) < 1e-30:
                d = 1e-30
            c = 1 + aa / c
            if abs(c) < 1e-30:
                c = 1e-30
            d = 1 / d
            h *= d * c
            aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
            d = 1 + aa * d
            if abs(d) < 1e-30:
                d = 1e-30
            c = 1 + aa / c
            if abs(c) < 1e-30:
                c = 1e-30
            d = 1 / d
            delta = d * c
            h *= delta
            if abs(delta - 1) < EPS:
                break
        return h

    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if ibf(mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def cp_upper(k, n, conf=0.95):
    """Clopper-Pearson 精确上界（k 次失败/逃逸，n 次试验）。k=0 走解析解。"""
    alpha = 1 - conf
    if k == 0:
        return 1 - alpha ** (1 / n)            # (1-alpha)^(1/n)
    if k == n:
        return 1.0
    return beta_quantile(1 - alpha / 2, k + 1, n - k)


def cp_interval(k, n, conf=0.95):
    alpha = 1 - conf
    lo = 0.0 if k == 0 else beta_quantile(alpha / 2, k, n - k + 1)
    hi = 1.0 if k == n else beta_quantile(1 - alpha / 2, k + 1, n - k)
    return lo, hi


def wilson(k, n, conf=0.95):
    z = 1.959963984540054 if conf == 0.95 else None
    ph = k / n
    d = 1 + z * z / n
    c = ph + z * z / (2 * n)
    m = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n))
    return (c - m) / d, (c + m) / d


def n_for_upper_bound_zero(eps, conf=0.95):
    """0 失效时，要让上界 ≤ eps，需要的最小样本量：n ≥ ln(1-conf)/ln(1-eps)。"""
    return math.ceil(math.log(1 - conf) / math.log(1 - eps))


def n_for_proportion(k0, n0, eps, conf=0.95):
    """已知率 p0，要半宽 ≤ eps 的近似 n（正态/Wald 保守式）。"""
    z = 1.96
    p = k0 / n0
    return math.ceil(z * z * p * (1 - p) / (eps * eps))


def main():
    out = {"at": "2026-09-17", "source_data": []}

    # --- Q1: 56 卡 0 误伤（规则存量 warn 观察期对存量卡不 block） ---
    n_cards = 56
    q1 = {
        "n": n_cards, "failures": 0, "conf": 0.95,
        "rule_of_three_point": 3 / n_cards,
        "clopper_pearson_upper_95": cp_upper(0, n_cards, 0.95),
        "clopper_pearson_upper_90": cp_upper(0, n_cards, 0.90),
        "clopper_pearson_upper_99": cp_upper(0, n_cards, 0.99),
    }
    out["q1_zero_falsepositive_56cards"] = q1
    out["source_data"].append("56 卡 replay confirm=56；61 规则 block=0（投喂词与 ledger §4 口径）")

    # --- Q2: mutation 拦截率/逃逸率置信区间（真实 full_baseline_v1） ---
    d = json.loads((ROOT / "data/mutation/full_baseline_v1.json").read_text(encoding="utf-8"))
    total, blocked, escaped, n_a = d["variants"], d["blocked"], d["escaped"], d["n_a"]
    treated = blocked + escaped                      # 可判（非 N/A、非 malformed）
    strict_rate = blocked / total
    treated_rate = blocked / treated
    out["q2_mutation"] = {
        "variants": total, "blocked": blocked, "escaped": escaped, "n_a": n_a,
        "strict_blocked_rate": round(strict_rate, 4),
        "strict_rate_cp95": [round(x, 4) for x in cp_interval(blocked, total)],
        "strict_rate_wilson95": [round(x, 4) for x in wilson(blocked, total)],
        "treated_denominator": treated,
        "treated_blocked_rate": round(treated_rate, 4),
        "treated_rate_cp95": [round(x, 4) for x in cp_interval(blocked, treated)],
        "escape_rate_on_treated_cp95": [round(x, 4) for x in cp_interval(escaped, treated)],
    }
    out["source_data"].append("data/mutation/full_baseline_v1.json (1188=729+227+232)")

    # --- Q3: 要宣称逃逸率 ≤5% @95%，需要多少样本（0 逃逸 与 按现逃逸率 两口径） ---
    q3 = {
        "claim_escape_le_5pct_conf95": {
            "if_zero_escapes_n": n_for_upper_bound_zero(0.05, 0.95),
            "note": "0 逃逸时 rule-of-three/C-P 精确解 n>=ln(.05)/ln(.95)",
        },
        "wald_n_for_pm5pct_at_current_treated_rate":
            n_for_proportion(blocked, treated, 0.05, 0.95),
        "wald_n_for_pm5pct_near_boundary_p0.5":
            n_for_proportion(1, 2, 0.05, 0.95),
        "wald_n_for_pm2pct_p0.5": n_for_proportion(1, 2, 0.02, 0.95),
    }
    out["q3_sample_size"] = q3

    # --- Q4: 各算子单独看（M2 几乎全逃逸 207/221 是活雷，给它的逃逸率上界） ---
    ops = {}
    for op, v in d["by_operator"].items():
        n_op = v["blocked"] + v["escaped"]
        ops[op] = {
            "treated": n_op, "escaped": v["escaped"],
            "escape_rate_cp95": [round(x, 3) for x in cp_interval(v["escaped"], n_op)]
            if n_op else None,
        }
    out["q4_by_operator"] = ops

    # --- Q5: 零误伤样本量反查表（给 G-iso 开门需要的卡数） ---
    out["q5_n_needed_for_upper_bounds"] = {
        "upper_10pct_95_n": n_for_upper_bound_zero(0.10, 0.95),
        "upper_5pct_95_n": n_for_upper_bound_zero(0.05, 0.95),
        "upper_2pct_95_n": n_for_upper_bound_zero(0.02, 0.95),
        "upper_5pct_99_n": n_for_upper_bound_zero(0.05, 0.99),
    }

    (HERE / "bounds_report.json").write_text(
        json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
