#!/usr/bin/env python3
"""616 A1 · 置信序列 / e-process（**修复统计偷看**）。纯标准库，无 scipy/numpy。

背景（`_arch_v20/05` + 探针 `p02`）：逃逸率口径历史上用**固定样本 Clopper-Pearson 上界**，
但项目是**批次累积、每批复算并对外报告**（v1→v7 + 各批报告 ≈9 次）——这在序贯分析里就是
**连续偷看（peeking）**：固定样本 CI 在任意停止/多次查看下**不成立**。探针实测：名义 95% 在连续偷看下
经验虚报膨胀到 **13.80%**。本工具用 **Beta-混合 e-process 置信序列**（Ville 不等式，任意停止时刻联合有效）
给出 **anytime 上界**，把口径从"看一次"升级为"随时看都合法"。

数学（H1 取 p1~Beta(a,b) 混合，H0: p=p0）：
    E_n(p0) = B(s+a, n-s+b) / [B(a,b) · p0^s (1-p0)^(n-s)]
  E_n 在 p0→小 且 s>0 时发散、在 MLE 处最小、向右单调增；CS = { p0 : E_n(p0) < 1/alpha }（Ville）。
  单侧上界 = 使 E_n(p0)=1/alpha 的**右根**（二分）。

CLI：`--check`（对历史参考值自验证）/ `--demo`（CP vs CS 差异演示）/ 默认打印当前口径。
参考值（历史记录 `_arch_v20/probes/output/p02_output.txt`，**不重跑 gate**）：
  n=1406,x=1：CP 单侧 95% 上界 **0.3370%**，CS anytime 上界 **0.9062%**（2.69×）。
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys

ALPHA = 0.05
PRIOR_A = 1.0
PRIOR_B = 1.0

#: 历史参考（_arch_v20 p02；仅用于 --check 对照，不重跑任何监工门禁）
REF_N = 1406
REF_X = 1
REF_CP_UPPER = 0.003370
REF_CS_UPPER = 0.009062


# ── 正则化不完全 Beta（Numerical Recipes 连分式）─────────────────────────────
def _betacf(a: float, b: float, x: float, itmax: int = 300, eps: float = 3e-14) -> float:
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < 1e-30:
        d = 1e-30
    d = 1.0 / d
    h = d
    for m in range(1, itmax + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30:
            d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30:
            c = 1e-30
        d = 1.0 / d
        de = d * c
        h *= de
        if abs(de - 1.0) < eps:
            break
    return h


def betai(a: float, b: float, x: float) -> float:
    """正则化不完全 Beta I_x(a,b)。"""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    bt = math.exp(lbeta + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1) / (a + b + 2):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1 - x) / b


def beta_quantile(p: float, a: float, b: float, iters: int = 70) -> float:
    """Beta(a,b) 的 p 分位数（二分为主，纯标准库）。"""
    lo, hi = 1e-12, 1 - 1e-12
    for _ in range(iters):
        mid = (lo + hi) / 2
        if betai(a, b, mid) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def cp_upper(n: int, x: int, alpha: float = ALPHA, sided: int = 1) -> float:
    """Clopper-Pearson 上界（sided=1 单侧 1-alpha；sided=2 双侧 95% 上界）。"""
    if n <= 0:
        return 1.0
    a = x + 1
    b = max(n - x, 0)
    if b == 0:
        return 1.0
    return beta_quantile(1 - alpha / sided, a, b)


def cp_lower(n: int, x: int, alpha: float = ALPHA) -> float:
    """Clopper-Pearson 下界（双侧 alpha）。"""
    if x == 0:
        return 0.0
    return beta_quantile(alpha / 2, x, n - x + 1)


# ── Beta-混合 e-process / 置信序列 ───────────────────────────────────────────
def log_beta(a: float, b: float) -> float:
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)


def log_eprocess(p0: float, x: int, n: int, a: float = PRIOR_A, b: float = PRIOR_B) -> float:
    """log E_n(p0)：H0: p=p0 的 Beta(a,b)-混合 e-process 的对数。"""
    if n < 0 or x < 0 or x > n:
        raise ValueError("需 0 ≤ x ≤ n")
    if p0 <= 0.0:
        return log_beta(x + a, n - x + b) - log_beta(a, b) if x == 0 else float("inf")
    if p0 >= 1.0:
        return 0.0 if x == n else float("inf")
    return (log_beta(x + a, n - x + b) - log_beta(a, b)
            - x * math.log(p0) - (n - x) * math.log1p(-p0))


def eprocess(p0: float, x: int, n: int, a: float = PRIOR_A, b: float = PRIOR_B) -> float:
    """E_n(p0)（可能溢出为 inf；调用方按需用 log 版）。"""
    e = log_eprocess(p0, x, n, a, b)
    if e == float("inf"):
        return float("inf")
    return math.exp(min(e, 700.0))


def _root(x: int, n: int, alpha: float, a: float, b: float,
          lo: float, hi: float, want_gt: bool) -> float:
    """在 [lo,hi] 上二分求 log E_n = log(1/alpha) 的根。

    want_gt=True 求右根（上界）：E 在右单调增；want_gt=False 求左根（下界）。
    """
    target = math.log(1.0 / alpha)
    for _ in range(90):
        mid = (lo + hi) / 2
        e = log_eprocess(mid, x, n, a, b)
        if want_gt:
            if e < target:
                lo = mid
            else:
                hi = mid
        else:
            if e < target:
                hi = mid
            else:
                lo = mid
    return (lo + hi) / 2


def cs_interval(n: int, x: int, alpha: float = ALPHA,
                a: float = PRIOR_A, b: float = PRIOR_B) -> tuple[float, float]:
    """anytime 置信区间（Ville；{p0 : E_n(p0) < 1/alpha}）。"""
    if n <= 0:
        return (0.0, 1.0)
    p_hat = x / n
    upper = _root(x, n, alpha, a, b, max(p_hat, 1e-12), 1 - 1e-12, want_gt=True)
    if x == 0:
        lower = 0.0
    else:
        lower = _root(x, n, alpha, a, b, 1e-12, min(p_hat, 1 - 1e-12), want_gt=False)
    return (lower, upper)


def cs_upper(n: int, x: int, alpha: float = ALPHA,
             a: float = PRIOR_A, b: float = PRIOR_B) -> float:
    """anytime 单侧上界（项目最关心的指标）。"""
    return cs_interval(n, x, alpha, a, b)[1]


class ConfidenceSequence:
    """累积观测下的 anytime-valid 逃逸率置信序列。

    口径：`update(successes, failures)`；`failures`（逃逸）为被界定比率的事件，
    `successes`（非逃逸）只增加分母 n。CS 界定 **逃逸率 = failures / (successes+failures)**。
    """

    def __init__(self, alpha: float = ALPHA, prior_a: float = PRIOR_A,
                 prior_b: float = PRIOR_B, null_rate: float | None = None) -> None:
        self.alpha = float(alpha)
        self.a = float(prior_a)
        self.b = float(prior_b)
        self.null_rate = null_rate
        self.successes = 0
        self.failures = 0

    @property
    def n(self) -> int:
        return self.successes + self.failures

    @property
    def x(self) -> int:
        return self.failures

    def update(self, successes: int = 0, failures: int = 0) -> "ConfidenceSequence":
        if successes < 0 or failures < 0:
            raise ValueError("观测数不得为负")
        self.successes += int(successes)
        self.failures += int(failures)
        return self

    def get_ci(self) -> tuple[float, float]:
        """anytime 置信区间 (lower, upper)。"""
        return cs_interval(self.n, self.x, self.alpha, self.a, self.b)

    def get_upper_bound(self) -> float:
        return cs_upper(self.n, self.x, self.alpha, self.a, self.b)

    def get_lower_bound(self) -> float:
        return self.get_ci()[0]

    def get_e_process(self, p0: float | None = None) -> float:
        """E_n(p0)：对 H0 逃逸率=p0 的证据。p0 缺省用 `self.null_rate`（须已设）。"""
        rate = self.null_rate if p0 is None else p0
        if rate is None:
            raise ValueError("get_e_process 需要 p0 或实例 null_rate")
        return eprocess(float(rate), self.x, self.n, self.a, self.b)

    def point_estimate(self) -> float:
        return self.x / self.n if self.n else 0.0


def monte_carlo_peek(reps: int = 300, nmax: int = 400, step: int = 20,
                     p_true: float = 0.01, seed: int = 20260921) -> dict:
    """连续偷看下两种口径的**经验虚报率**（事件=错误宣称 'p < p_true'）。

    参数较小以便 `--demo` 快跑；`_arch_v20 p02` 用 reps=3000,nmax=1406 得 13.80% vs 0.00%。
    """
    rnd = random.Random(seed)
    cp_fire = ep_fire = 0
    for _ in range(reps):
        s = 0
        cp_hit = ep_hit = False
        for n in range(1, nmax + 1):
            if rnd.random() < p_true:
                s += 1
            if n % step == 0:
                if beta_quantile(0.95, s + 1, max(n - s, 1e-9)) < p_true:
                    cp_hit = True
                if s < n * p_true and log_eprocess(p_true, s, n) > math.log(1 / ALPHA):
                    ep_hit = True
        cp_fire += cp_hit
        ep_fire += ep_hit
    return {"reps": reps, "nmax": nmax, "step": step, "p_true": p_true,
            "cp_false_alarm": cp_fire / reps, "cs_false_alarm": ep_fire / reps}


def check() -> list[str]:
    problems: list[str] = []
    cs = cs_upper(REF_N, REF_X)
    cp = cp_upper(REF_N, REF_X)
    if abs(cs - REF_CS_UPPER) > 5e-5:
        problems.append(f"CS 上界 n=1406,x=1 应≈{REF_CS_UPPER:.6f}（实测 {cs:.6f}）")
    if abs(cp - REF_CP_UPPER) > 5e-5:
        problems.append(f"CP 单侧上界 应≈{REF_CP_UPPER:.6f}（实测 {cp:.6f}）")
    if not (cs > cp):
        problems.append("anytime CS 上界应 > 固定样本 CP（保守代价）")
    lo, hi = cs_interval(REF_N, REF_X)
    if not (0.0 <= lo <= REF_X / REF_N <= hi <= 1.0):
        problems.append(f"区间序错误：{lo} <= {REF_X / REF_N} <= {hi}")
    # 上界定义自洽：E_n(上界) ≈ 1/alpha
    e = log_eprocess(cs, REF_X, REF_N)
    if abs(e - math.log(1 / ALPHA)) > 1e-3:
        problems.append(f"上界处 log E 应≈{math.log(1 / ALPHA):.4f}（实测 {e:.4f}）")
    # 单调：0 逃逸时上界随 n 递减
    prev = 1.0
    for n in (50, 200, 1000, 1406):
        u = cs_upper(n, 0)
        if u > prev:
            problems.append(f"0 逃逸上界应随 n 单调不增（n={n}）")
            break
        prev = u
    # 类接口
    c = ConfidenceSequence()
    c.update(5, 1)
    if (c.n, c.x) != (6, 1):
        problems.append("update 计数错误")
    if not (c.get_lower_bound() <= c.point_estimate() <= c.get_upper_bound()):
        problems.append("类接口区间序错误")
    return problems


def demo() -> str:
    mc = monte_carlo_peek()
    L = ["# 616 A1 · demo：固定样本 CP vs anytime 置信序列", "",
         f"- 连续偷看 MC（reps={mc['reps']}, nmax={mc['nmax']}, step={mc['step']}, 真实 p={mc['p_true']}）：",
         f"  - 固定样本 CP 经验虚报率 = **{mc['cp_false_alarm'] * 100:.2f}%**（名义 5%）",
         f"  - 置信序列经验虚报率 = **{mc['cs_false_alarm'] * 100:.2f}%**（理论 ≤5%）", "",
         "| n | x | CP 单侧 95% | CS anytime 95% |", "|---|---|---|---|"]
    for n, x in ((50, 0), (100, 0), (200, 0), (500, 0), (1000, 0), (1406, 1)):
        L.append(f"| {n} | {x} | {cp_upper(n, x) * 100:.4f}% | {cs_upper(n, x) * 100:.4f}% |")
    L += ["", f"- n=1406,x=1：CP {cp_upper(REF_N, REF_X) * 100:.4f}% vs CS "
          f"{cs_upper(REF_N, REF_X) * 100:.4f}%（{cs_upper(REF_N, REF_X) / cp_upper(REF_N, REF_X):.2f}×）"]
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(prog="confidence_sequence",
                                 description="616 A1 置信序列/e-process（修复统计偷看，纯标准库）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--demo", action="store_true")
    ap.add_argument("--n", type=int, default=REF_N)
    ap.add_argument("--x", type=int, default=REF_X)
    a = ap.parse_args(argv)
    if a.check:
        problems = check()
        if problems:
            for p in problems:
                print(f"[A1] ❌ {p}", file=sys.stderr)
            return 1
        print(f"[A1] ✅ 自验证通过：n=1406,x=1 CS={cs_upper(REF_N, REF_X) * 100:.4f}% "
              f"CP={cp_upper(REF_N, REF_X) * 100:.4f}%（与历史参考一致）")
        return 0
    if a.demo:
        print(demo())
        return 0
    c = ConfidenceSequence()
    c.update(a.n - a.x, a.x)
    print(json.dumps({"n": c.n, "x": c.x, "point": round(c.point_estimate(), 6),
                      "cs_lower": round(c.get_lower_bound(), 6),
                      "cs_upper": round(c.get_upper_bound(), 6),
                      "cp_upper_95": round(cp_upper(c.n, c.x), 6),
                      "alpha": c.alpha}, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
