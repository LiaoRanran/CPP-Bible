# -*- coding: utf-8 -*-
"""
p02_confidence_sequence.py — _arch_v20 只读探针
方向 5（序贯分析/统计学习）实证：
  阙疑现状：逃逸率契约 1/1406，Clopper-Pearson 固定样本量 CI。
  问题：批次是累积的（51 批→615 批），每批都重新看上界 = 连续偷看（peeking），
        固定样本量 CP 在任停/多次查看下不成立。
  本探针（纯标准库，无外部依赖，全部 Monte Carlo 可复现，种子固定）：
    A) 精确复算 CP：双侧 95% CI、单侧 95% 上界（Beta 逆函数，bisection）
    B) Beta-混合 e-process 置信序列（Ville 不等式，任意停止时刻联合有效），
       对 n=1406,x=1 给 anytime 上界，与 CP 对比代价
    C) Monte Carlo：真实 p=0 下，CP 单侧 0.05 每 10 样本偷看一次的经验虚报率
       vs e-process 偷看的经验虚报率（理论 ≤ α）
    D) 样本节约：给定可接受上界 0.5%，在「0 逃逸」前缀上两种方法分别最早何时能宣称达标
"""
import math, random

ALPHA = 0.05
N, X = 1406, 1
SEED = 20260921


# ---------- 正则化不完全 Beta（Numerical Recipes 风格连分式） ----------
def _betacf(a, b, x, itmax=300, eps=3e-14):
    qab, qap, qam = a + b, a + 1.0, a - 1.0
    c = 1.0
    d = 1.0 - qab * x / qap
    if abs(d) < 1e-30: d = 1e-30
    d = 1.0 / d
    h = d
    for m in range(1, itmax + 1):
        m2 = 2 * m
        aa = m * (b - m) * x / ((qam + m2) * (a + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30: d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30: c = 1e-30
        d = 1.0 / d; h *= d * c
        aa = -(a + m) * (qab + m) * x / ((a + m2) * (qap + m2))
        d = 1.0 + aa * d
        if abs(d) < 1e-30: d = 1e-30
        c = 1.0 + aa / c
        if abs(c) < 1e-30: c = 1e-30
        d = 1.0 / d
        de = d * c; h *= de
        if abs(de - 1.0) < eps: break
    return h


def betai(a, b, x):
    """I_x(a,b) 正则化不完全 beta"""
    if x <= 0: return 0.0
    if x >= 1: return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    bt = math.exp(lbeta + a * math.log(x) + b * math.log1p(-x))
    if x < (a + 1) / (a + b + 2):
        return bt * _betacf(a, b, x) / a
    return 1.0 - bt * _betacf(b, a, 1 - x) / b


def beta_q(p, a, b):
    """Beta(a,b) 的 p 分位数（bisection）"""
    lo, hi = 1e-12, 1 - 1e-12
    for _ in range(70):
        mid = (lo + hi) / 2
        if betai(a, b, mid) < p: lo = mid
        else: hi = mid
    return (lo + hi) / 2


def cp_upper(n, x, alpha=ALPHA, sided=1):
    """单侧 1-alpha 上界；sided=2 时为双侧 95% 上界"""
    a = x + 1
    b = max(n - x, 0)
    p = 1 - (alpha / sided)
    if b == 0: return 1.0
    return beta_q(p, a, b)


def cp_lower(n, x, alpha=ALPHA):
    if x == 0: return 0.0
    return beta_q(alpha / 2, x, n - x + 1)


# ---------- Beta(1,1) 混合 e-process ----------
def log_beta(a, b):
    return math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)


def log_eprocess(p0, s, n):
    """H1 取 p1~Beta(1,1) 混合的对数 e-process：
    E_n = B(s+1,n-s+1) / p0^s (1-p0)^(n-s)"""
    if p0 <= 0.0:
        return log_beta(s + 1, n - s + 1) if s == 0 else float('-inf')
    if p0 >= 1.0:
        return 0.0 if s == n else float('inf')
    return log_beta(s + 1, n - s + 1) - s * math.log(p0) - (n - s) * math.log1p(-p0)


def cs_upper(n, x, alpha=ALPHA):
    """反转 e-process 求置信区间的【上根】：
    E_n(p0) 关于 p0 在 MLE 处最小，右侧单调递增，
    在 [x/n, 1) 上二分使 log E = log(1/alpha) 的点。"""
    target = math.log(1 / alpha)
    lo, hi = x / n, 1 - 1e-12
    for _ in range(80):
        mid = (lo + hi) / 2
        if log_eprocess(mid, x, n) < target: lo = mid
        else: hi = mid
    return (lo + hi) / 2


def monte_carlo_peek():
    rnd = random.Random(SEED)
    NMAX, STEP, REPS, P = 1406, 20, 3000, 0.01
    cp_fire, ep_fire = 0, 0
    for _ in range(REPS):
        s = 0
        cp_hit = ep_hit = False
        for n in range(1, NMAX + 1):
            s += 1 if rnd.random() < P else 0
            if n % STEP == 0:
                # 错误事件 = 在真实 p=P 下宣称「p 的上界 < P」（偷看诱导的过度自信）
                u = beta_q(0.95, s + 1, max(n - s, 1e-9))
                if u < P: cp_hit = True
                # 同向（向下）宣称才计入：p0 被拒绝且经验频率在 p0 下方
                if s < n * P and log_eprocess(P, s, n) > math.log(1 / ALPHA):
                    ep_hit = True
        cp_fire += cp_hit; ep_fire += ep_hit
    return cp_fire / REPS, ep_fire / REPS


def earliest_threshold(threshold=0.005, nmax=4000):
    """在 0 逃逸前缀上：两种方法最早在 n 多大时上界 ≤ threshold"""
    cp_n = ep_n = None
    for n in range(1, nmax + 1):
        if cp_n is None and cp_upper(n, 0) <= threshold: cp_n = n
        if ep_n is None and cs_upper(n, 0) <= threshold: ep_n = n
        if cp_n and ep_n: break
    return cp_n, ep_n


def main():
    print("# 探针 p02：置信序列（anytime）vs 固定样本 CP — 逃逸率口径")
    print(f"输入：n={N}, x={X}, alpha={ALPHA}, 契约逃逸率 1/{N}={1/N:.6f}\n")

    lo = cp_lower(N, X); hi2 = cp_upper(N, X, sided=2); hi1 = cp_upper(N, X, sided=1)
    print("## A. Clopper-Pearson 精确区间复算")
    print(f"  双侧 95% CI        = [{lo*100:.4f}%, {hi2*100:.4f}%]")
    print(f"  单侧 95% 上界      = {hi1*100:.4f}%   （v19 G13 称 0.337%，此处复算）")
    print(f"  点估计             = {X/N*100:.4f}%")

    cs = cs_upper(N, X)
    print("\n## B. Beta-混合 e-process 置信序列（任意停止时刻联合 95% 覆盖）")
    print(f"  n={N},x={X} 的 anytime 上界 = {cs*100:.4f}%")
    print(f"  相对单侧 CP 上界放宽倍数     = {cs/hi1:.2f}x  （anytime 的诚实代价）")
    print("  轨迹（累积观测 0 逃逸时的上界，%）:")
    for n in (50, 100, 200, 500, 1000, 1406):
        x = 1 if n == 1406 else 0
        print(f"    n={n:5d} x={x}  CP单侧={cp_upper(n,x)*100:7.4f}%  CS={cs_upper(n,x)*100:7.4f}%")

    print("\n## C. 连续偷看的虚报率（真实 p=0.01，每 20 样本看一次，看到 n=1406）")
    print("    事件=错误宣称『p < 0.01』；3000 次 Monte Carlo，种子 %d" % SEED)
    cp_rate, ep_rate = monte_carlo_peek()
    print(f"    CP 单侧 0.05 反复偷看经验虚报率 = {cp_rate*100:.2f}%  (名义 5%)")
    print(f"    e-process/置信序列经验虚报率    = {ep_rate*100:.2f}%  (理论 ≤ 5%)")

    print("\n## D. 0 逃逸前缀上达到 0.5% 上界所需样本量")
    cn, en = earliest_threshold(0.005)
    print(f"    CP 固定口径: n={cn}   CS anytime 口径: n={en}   代价 {en/cn:.2f}x")
    print("    含义：CS 用更多样本换来「每批都能合法看仪表盘」的权力。")


if __name__ == "__main__":
    main()
