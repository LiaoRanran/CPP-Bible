#!/usr/bin/env python3
"""565 Part 1 · 把形容词算成数字的**统计原语库**（纯标准库；无 scipy/numpy）。

来历：563 调研（`_arch_v6/probe_bounds.py`）已把 C-P 精确区间 / rule-of-three / 样本量亲算复现；
本文件把它**正规化**为正式工具——函数名与算法保持不变（与探针**逐值一致**），补
docstring / 类型标注 / 边界 fail-loud / CLI。

为什么不用 scipy：本仓核心依赖只有 pyyaml（`.venv` 里 scipy/numpy **实测未安装**），且
"为对拍把 scipy 加进核心依赖"是反向依赖。正确性由 `tests/test_stat_bounds.py` 的**四重锚点**
自证：① k=0/k=n 解析解闭式；② 独立第二实现（数值积分 CDF + 二分）交叉；③ 公开锚点
（56 卡 0 误伤 95% 上界 ≈0.05209 / rule-of-three 3/56≈0.05357 / n=100,k=0 ≈0.0295）；
④ 样本量闭式（5%@95% ⇒ n=59；2% ⇒ n=149）。

口径纪律（Part 2 依赖本库）：**比率必须带分子/分母**；分母为 0 ⇒ **拒答**（ValueError），
不许静默返回 0 或 1——"不可判"与"率为零"是两件事（563 N9 误报的教训就是口径不自洽）。

用法：
  python tools/stat_bounds.py cp --k 0 --n 56            # C-P 精确区间 + 点估计
  python tools/stat_bounds.py wilson --k 0 --n 56        # Wilson 区间（闭式近似）
  python tools/stat_bounds.py n-needed --eps 0.05        # 零失效样本量
  （任意子命令都可加 --json 取机器可读输出）
"""
from __future__ import annotations

import argparse
import json
import math
import sys

VERSION = "v1.0"


# ── 边界校验（fail-loud；565 明确要求禁止静默返回）─────────────────────────────
def _check_k_n(k: int, n: int, conf: float) -> None:
    """参数合法性：n≥1、0≤k≤n、conf ∈ (0,1)。任一条不满足 ⇒ ValueError。

    为什么必须抛而不是钳：`n=0`（无样本）与"率为 0"在报告里长得一样但含义相反
    （前者是"不可判"，后者是"确实没发生"）——静默钳值会把"没测"伪装成"没问题"。
    """
    if not isinstance(n, int) or not isinstance(k, int):
        raise ValueError(f"k/n 必须是整数：k={k!r} n={n!r}")
    if n < 1:
        raise ValueError(f"n 必须 ≥1（n={n}）：无样本 ⇒ 不可判，拒绝给率")
    if k < 0:
        raise ValueError(f"k 必须 ≥0（k={k}）")
    if k > n:
        raise ValueError(f"k 不得 > n（k={k} > n={n}）")
    if not (0.0 < conf < 1.0):
        raise ValueError(f"conf 必须在 (0,1) 内（conf={conf}）")


def normal_quantile(p: float) -> float:
    """标准正态分位数（二分反解 `erf`，p ∈ (0,1)）。精度 ~1e-12，避免引入 scipy。"""
    if not (0.0 < p < 1.0):
        raise ValueError(f"p 必须在 (0,1) 内（p={p}）")
    lo, hi = -40.0, 40.0
    root2 = math.sqrt(2.0)
    for _ in range(200):
        mid = (lo + hi) / 2
        cdf = 0.5 * (1.0 + math.erf(mid / root2))
        if cdf < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def beta_quantile(p: float, a: float, b: float) -> float:
    """Beta(a,b) 的 p 分位数：二分反解 regularized incomplete beta（Lentz 连分式）。

    算法与 563 探针**逐字一致**（连分式 MAXIT=200 / EPS=3e-12 / 二分 80 轮），
    以保证"与 `_arch_v6/probe_bounds.py` 输出逐值一致"这条验收。
    """
    if not (0.0 < p < 1.0):
        raise ValueError(f"p 必须在 (0,1) 内（p={p}）")
    if a <= 0 or b <= 0:
        raise ValueError(f"a,b 必须 > 0（a={a} b={b}）")
    logbet = math.lgamma(a) + math.lgamma(b) - math.lgamma(a + b)

    def betacf(x: float, aa: float, bb: float) -> float:
        MAXIT, EPS = 200, 3e-12
        qab, qap, qam = aa + bb, aa + 1, aa - 1
        c = 1.0
        d = 1.0 - qab * x / qap
        if abs(d) < 1e-30:
            d = 1e-30
        d = 1 / d
        h = d
        for m in range(1, MAXIT + 1):
            m2 = 2 * m
            num = m * (bb - m) * x / ((qam + m2) * (aa + m2))
            d = 1 + num * d
            if abs(d) < 1e-30:
                d = 1e-30
            c = 1 + num / c
            if abs(c) < 1e-30:
                c = 1e-30
            d = 1 / d
            h *= d * c
            num = -(aa + m) * (qab + m) * x / ((aa + m2) * (qap + m2))
            d = 1 + num * d
            if abs(d) < 1e-30:
                d = 1e-30
            c = 1 + num / c
            if abs(c) < 1e-30:
                c = 1e-30
            d = 1 / d
            delta = d * c
            h *= delta
            if abs(delta - 1) < EPS:
                break
        return h

    def ibf(x: float, aa: float, bb: float) -> float:
        if x <= 0:
            return 0.0
        if x >= 1:
            return 1.0
        bt = math.exp(aa * math.log(x) + bb * math.log(1 - x) - logbet)
        if x < (aa + 1) / (aa + bb + 2):
            return bt * betacf(x, aa, bb) / aa
        return 1 - bt * betacf(1 - x, bb, aa) / bb

    lo, hi = 0.0, 1.0
    for _ in range(80):
        mid = (lo + hi) / 2
        if ibf(mid, a, b) < p:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


# ── 区间估计（Clopper-Pearson 精确 / Wilson 闭式）──────────────────────────────
def cp_upper(k: int, n: int, conf: float = 0.95) -> float:
    """Clopper-Pearson **精确上界**（k 次"失败/逃逸"，n 次试验）。

    k=0 走解析解 `1 - (1-conf)^(1/n)`（"零失效"场景的精确解，即 rule-of-three 的精确版，
    也是"56 卡 0 误伤 ⇒ 误伤率 ≤0.05209 @95%"那个数）；k=n ⇒ 1.0。

    ⚠️ **口径警告（565 实测发现，Part 2 必须知道）**：本函数是 563 探针的**原样语义**——
      * `k == 0` 分支是**单侧**上界（alpha 全给一侧）；
      * `k > 0` 分支走 `beta_quantile(1-alpha/2, …)`，是**双侧**上界。
    两侧混用是探针既有的形态（本库为"与探针逐值一致"这条验收保持不动）。**要口径统一**：
      * 双侧区间 ⇒ 用 `cp_interval()`（lo/hi 同为 alpha/2，自洽）；
      * 单侧上界 ⇒ 用 `cp_upper_one_sided()`（k=0 与本节一致，k>0 用 alpha 而非 alpha/2）。
    直接把 `cp_upper` 当"统一上界"用会在 k=0↔k>0 之间偷偷换口径——这正是 565 Part 2 要防的失真。
    """
    _check_k_n(k, n, conf)
    alpha = 1 - conf
    if k == 0:
        return 1 - alpha ** (1 / n)
    if k == n:
        return 1.0
    return beta_quantile(1 - alpha / 2, k + 1, n - k)


def cp_upper_one_sided(k: int, n: int, conf: float = 0.95) -> float:
    """Clopper-Pearson **单侧**精确上界（口径统一版）：k=0 时与 `cp_upper` 相同。

    `P(X ≤ k; n, U) = 1-conf` 解出的 U：k>0 用 `beta_quantile(1-alpha, k+1, n-k)`，
    k=0 用解析解 `1-(1-conf)^(1/n)`（二者在 k=0 处**同值**，可作自洽性回归）。
    """
    _check_k_n(k, n, conf)
    alpha = 1 - conf
    if k == 0:
        return 1 - alpha ** (1 / n)
    if k == n:
        return 1.0
    return beta_quantile(1 - alpha, k + 1, n - k)


def cp_interval(k: int, n: int, conf: float = 0.95) -> tuple[float, float]:
    """Clopper-Pearson 双侧精确区间 `(lo, hi)`（k=0 ⇒ lo=0；k=n ⇒ hi=1）。"""
    _check_k_n(k, n, conf)
    alpha = 1 - conf
    lo = 0.0 if k == 0 else beta_quantile(alpha / 2, k, n - k + 1)
    hi = 1.0 if k == n else beta_quantile(1 - alpha / 2, k + 1, n - k)
    return lo, hi


def wilson(k: int, n: int, conf: float = 0.95) -> tuple[float, float]:
    """Wilson score 区间（闭式，小样本比 Wald 稳）。

    注：563 探针里 `z` 只在 conf==0.95 时给值（其它 conf 会 TypeError）；本版按 conf
    实算 z（`normal_quantile`），语义不变、边界不再炸。
    """
    _check_k_n(k, n, conf)
    z = normal_quantile(1 - (1 - conf) / 2)
    ph = k / n
    d = 1 + z * z / n
    c = ph + z * z / (2 * n)
    m = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n))
    return (c - m) / d, (c + m) / d


# ── 样本量 ────────────────────────────────────────────────────────────────────
def n_for_upper_bound_zero(eps: float, conf: float = 0.95) -> int:
    """**零失效**时要把上界压到 ≤ eps 所需的最小样本量：`n ≥ ln(1-conf)/ln(1-eps)`。

    这就是"要敢说'误伤率 ≤5%@95%'得先跑多少张卡"的答案（59 张）；也是 rule-of-three 的逆用。
    """
    if not (0.0 < eps < 1.0):
        raise ValueError(f"eps 必须在 (0,1) 内（eps={eps}）")
    if not (0.0 < conf < 1.0):
        raise ValueError(f"conf 必须在 (0,1) 内（conf={conf}）")
    return math.ceil(math.log(1 - conf) / math.log(1 - eps))


def n_for_proportion(k0: int, n0: int, eps: float, conf: float = 0.95) -> int:
    """已知观测率 p0=k0/n0，要**半宽 ≤ eps** 所需的近似样本量（Wald 保守式）。

    近似式（正态近似）——只用于"还要补多少样本"的量级估计，不得当作精确保证；
    精确保证请用 `n_for_upper_bound_zero`（零失效闭式）。
    """
    _check_k_n(k0, n0, conf)
    if not (0.0 < eps < 1.0):
        raise ValueError(f"eps 必须在 (0,1) 内（eps={eps}）")
    z = normal_quantile(1 - (1 - conf) / 2)
    p = k0 / n0
    return math.ceil(z * z * p * (1 - p) / (eps * eps))


# ── 报告载体（Part 2 直接复用：比率必须带分子分母，缺失分母拒答）────────────────
def proportion(k: int, n: int, conf: float = 0.95) -> dict:
    """把"k/n"打包成**自洽口径**的报告块：分子/分母/点估计/C-P 区间。

    Part 2 的硬要求就是"比率禁止无分母单独出现"——统一走这个函数，口径不可能漏。
    """
    _check_k_n(k, n, conf)
    lo, hi = cp_interval(k, n, conf)
    return {"numerator": k, "denominator": n, "point": k / n,
            "cp_low": lo, "cp_high": hi, "conf": conf}


# ── CLI ──────────────────────────────────────────────────────────────────────
def _fmt(p: dict) -> str:
    return (f"{p['numerator']}/{p['denominator']} = {p['point']:.4f}"
            f"  · C-P {p['conf']:.0%} 区间 [{p['cp_low']:.4f}, {p['cp_high']:.4f}]")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="统计原语：精确区间 / 样本量（纯标准库）")
    sub = ap.add_subparsers(dest="cmd", required=True)
    for name in ("cp", "wilson"):
        sp = sub.add_parser(name, help="k/n 的区间与点估计")
        sp.add_argument("--k", type=int, required=True)
        sp.add_argument("--n", type=int, required=True)
        sp.add_argument("--conf", type=float, default=0.95)
        sp.add_argument("--json", action="store_true")
    sn = sub.add_parser("n-needed", help="零失效时压制上界 ≤ eps 所需样本量")
    sn.add_argument("--eps", type=float, required=True)
    sn.add_argument("--conf", type=float, default=0.95)
    sn.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)

    try:
        if a.cmd in ("cp", "wilson"):
            blk = proportion(a.k, a.n, a.conf)
            if a.cmd == "wilson":
                wlo, whi = wilson(a.k, a.n, a.conf)
                blk["wilson_low"], blk["wilson_high"] = wlo, whi
            if a.json:
                print(json.dumps({"tool": "stat_bounds", "version": VERSION,
                                  "kind": a.cmd, **blk}, ensure_ascii=False, indent=1))
            else:
                print(f"[stat] {a.cmd}: {_fmt(blk)}")
                # 口径显形：单侧上界与双侧区间是**两个口径**，分别打标签（防混用）
                if a.cmd == "cp":
                    print(f"[stat] 单侧上界 {a.conf:.0%}："
                          f"{cp_upper_one_sided(a.k, a.n, a.conf):.5f}"
                          "（k=0 时与双侧上界不同，见 cp_upper 的口径警告）")
                if a.cmd == "wilson":
                    print(f"[stat] wilson {a.conf:.0%} 区间 "
                          f"[{blk['wilson_low']:.4f}, {blk['wilson_high']:.4f}]")
            return 0
        nn = n_for_upper_bound_zero(a.eps, a.conf)
        if a.json:
            print(json.dumps({"tool": "stat_bounds", "version": VERSION,
                              "kind": "n-needed", "eps": a.eps, "conf": a.conf,
                              "n": nn}, ensure_ascii=False, indent=1))
        else:
            print(f"[stat] n-needed: eps={a.eps:.2%} @ {a.conf:.0%} ⇒ n ≥ {nn}"
                  f"（零失效时上界 ≤ {a.eps:.2%}）")
        return 0
    except ValueError as exc:
        print(f"[stat] ❌ 参数非法：{exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    main()
