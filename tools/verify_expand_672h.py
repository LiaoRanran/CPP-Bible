#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""verify_expand_672h.py — 672h W3：扩样结果的**独立复算**（双路径交叉复现）。

为什么需要它
============
预注册 672h 写明：`tools/holdout_reveal_5_672h.py` / `external_corpus_reveal_672h.py`
与 `baseline_670a.py` 的产物必须由**独立重实现**复算，率与 CI 差 <0.1pp 才算 PASS。

独立性约束（本文件的纪律）
==========================
* **不 import**：`stat_bounds` / `ablation_stats_671b` / `holdout_reveal_*` / `baseline_670a`
  ——CP 区间用**二分法 + lgamma** 自实现；McNemar 用精确二项（自实现 log 组合数）；
  Cohen's h / Newcombe 差值 CI 同样自实现。
* 事实源只有**逐样本明细**（`reveal_5_detail_672h.json` / `reveal_detail_672h.json`），
  不读任何汇总数字。
* Static 臂的**重分箱规则**独立重抄一遍（只认编译期仪器的语义），再与 baseline_670a 的落盘比对。

产物
====
`data/experiments/verify_expand_672h.json`：双路径对账 + H1/H2 配对检验 + 与
`ablation_stats_671b`（仓库规范实现）的第三路对账（若可用）。

用法
====
    python tools/verify_expand_672h.py            # 复算 + 落盘
    python tools/verify_expand_672h.py --json     # 机读
    python tools/verify_expand_672h.py --selftest # 自检（不读仓库产物）
"""
from __future__ import annotations

import argparse
import json
import math
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "data" / "experiments" / "verify_expand_672h.json"
H_DETAIL = ROOT / "data" / "holdout" / "reveal_5_detail_672h.json"
C_DETAIL = ROOT / "data" / "external_corpus" / "reveal_detail_672h.json"
H_ROUND = ROOT / "data" / "holdout_reveal_5_672h.json"
C_ROUND = ROOT / "data" / "external_corpus_reveal_672h.json"
B_FD = ROOT / "data" / "experiments" / "baseline_fd.json"
B_S = ROOT / "data" / "experiments" / "baseline_static.json"
TOL_PP = 0.1                       # 预注册：两路径差必须 < 0.1pp

#: Static 臂规则（独立重抄：只认编译期/静态仪器；sanitizer 样本记 miss）
STATIC_INSTR = {"compiler-warn", "wunsequenced", "cross-compile", "linker"}


def jload(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


# ── 独立统计实现（不使用仓库任何统计库）────────────────────────────────────────

def _betainc_reg(a: float, b: float, x: float) -> float:
    """正则化不完全 Beta 函数 I_x(a,b)（连分式 + 二分，Numerical Recipes 式）。"""
    if x <= 0:
        return 0.0
    if x >= 1:
        return 1.0
    lbeta = math.lgamma(a + b) - math.lgamma(a) - math.lgamma(b)
    front = math.exp(lbeta + a * math.log(x) + b * math.log(1 - x))

    def cf(a_: float, b_: float, x_: float) -> float:
        tiny = 1e-30
        c_, d_ = 1.0, 1.0 - (a_ + b_) * x_ / (a_ + 1)
        d_ = tiny if abs(d_) < tiny else d_
        d_ = 1.0 / d_
        h_ = d_
        for m in range(1, 300):
            m2 = 2 * m
            aa = m * (b_ - m) * x_ / ((a_ + m2 - 1) * (a_ + m2))
            d_ = 1.0 + aa * d_
            d_ = tiny if abs(d_) < tiny else d_
            c_ = 1.0 + aa / c_
            c_ = tiny if abs(c_) < tiny else c_
            d_ = 1.0 / d_
            h_ *= d_ * c_
            aa = -(a_ + m) * (a_ + b_ + m) * x_ / ((a_ + m2) * (a_ + m2 + 1))
            d_ = 1.0 + aa * d_
            d_ = tiny if abs(d_) < tiny else d_
            c_ = 1.0 + aa / c_
            c_ = tiny if abs(c_) < tiny else c_
            d_ = 1.0 / d_
            de = d_ * c_
            h_ *= de
            if abs(de - 1.0) < 1e-15:
                break
        return h_

    if x < (a + 1) / (a + b + 2):
        return front * cf(a, b, x) / a
    return 1.0 - front * cf(b, a, 1 - x) / b


def cp_interval(k: int, n: int, conf: float = 0.95) -> tuple[float | None, float | None]:
    """Clopper–Pearson 双侧区间（beta 分位数 + 二分；与 stat_bounds 的 beta 实现独立）。

    下界 = Beta^{-1}(α/2; k, n-k+1)：解 I_p(k, n-k+1) = α/2（I 关于 p 单调增）；
    上界 = Beta^{-1}(1-α/2; k+1, n-k)：解 I_p(k+1, n-k) = 1-α/2。
    k=0 ⇒ 下界 0；k=n ⇒ 上界 1（定义域端点，非近似）。
    """
    if n <= 0:
        return None, None
    alpha = 1 - conf

    def solve(a: float, b: float, target: float) -> float:
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2
            if _betainc_reg(a, b, mid) < target:
                lo = mid
            else:
                hi = mid
            if hi - lo < 1e-15:
                break
        return (lo + hi) / 2

    low = 0.0 if k == 0 else solve(float(k), float(n - k + 1), alpha / 2)
    high = 1.0 if k == n else solve(float(k + 1), float(n - k), 1 - alpha / 2)
    return low, high


def mcnemar_exact_p(b: int, c: int) -> float:
    """精确 McNemar（双侧）：2×P(Binom(b+c, 0.5) ≤ min(b,c))，用 lgamma 算组合数。"""
    n = b + c
    if n == 0:
        return 1.0
    m = min(b, c)

    def log_cnk(n_: int, k_: int) -> float:
        return (math.lgamma(n_ + 1) - math.lgamma(k_ + 1) - math.lgamma(n_ - k_ + 1))

    tail = sum(math.exp(log_cnk(n, i) - n * math.log(2)) for i in range(0, m + 1))
    return min(1.0, 2.0 * tail)


def cohens_h(p1: float, p2: float) -> float:
    return 2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2))


def wald_delta_ci(b: int, c: int, n: int, conf: float = 0.95) -> tuple[float, float]:
    """配对差值的 Wald CI（p1-p2 = (b-c)/n；方差 = (b+c)/n² - (b-c)²/n³）。"""
    if n <= 0:
        return (float("nan"), float("nan"))
    z = 1.959963984540054 if abs(conf - 0.95) < 1e-9 else 1.959963984540054
    d = (b - c) / n
    var = (b + c) / (n * n) - (b - c) ** 2 / (n ** 3)
    var = max(var, 0.0)
    half = z * math.sqrt(var)
    return (d - half, d + half)


# ── 逐样本装载（事实源＝明细文件）─────────────────────────────────────────────

def holdout_samples() -> list[dict]:
    d = jload(H_DETAIL)
    return [r for r in d["per_sample"] if r.get("planted") is True]


def corpus_samples() -> list[dict]:
    d = jload(C_DETAIL)
    return list(d["per_sample"])


def fd_verdicts(rows: list[dict]) -> dict[str, str]:
    return {r["id"]: r["verdict"] for r in rows}


def static_verdicts(rows: list[dict]) -> dict[str, str]:
    """Static 臂独立重实现（只认编译期仪器）。"""
    out = {}
    for r in rows:
        v = r["verdict"]
        if v in ("unknown", "not_error"):
            out[r["id"]] = v
        elif str(r.get("detector")) in STATIC_INSTR:
            out[r["id"]] = v
        else:
            out[r["id"]] = "miss"
    return out


def pair_stats(fd: dict[str, str], st: dict[str, str]) -> dict[str, Any]:
    """配对检验：只在 FD 可测（catch/miss）的样本上配对。"""
    ids = [i for i, v in fd.items() if v in ("catch", "miss")]
    n = len(ids)
    k_fd = sum(1 for i in ids if fd[i] == "catch")
    k_st = sum(1 for i in ids if st[i] == "catch")
    b = sum(1 for i in ids if fd[i] == "catch" and st[i] == "miss")
    c = sum(1 for i in ids if fd[i] == "miss" and st[i] == "catch")
    p1, p2 = k_fd / n, k_st / n
    lo, hi = wald_delta_ci(b, c, n)
    return {
        "n": n, "fd_k": k_fd, "static_k": k_st,
        "fd_rate_pct": round(p1 * 100, 4), "static_rate_pct": round(p2 * 100, 4),
        "delta_pp": round((p1 - p2) * 100, 4),
        "discordant": {"b_fd_only": b, "c_static_only": c},
        "mcnemar_p": mcnemar_exact_p(b, c),
        "cohens_h": round(cohens_h(p1, p2) if n else float("nan"), 4),
        "delta_ci95_pct": [round(lo * 100, 4), round(hi * 100, 4)],
        "cp95_fd": [round(x * 100, 4) if x is not None else None
                    for x in cp_interval(k_fd, n)],
    }


def _near(a: float | None, b: float | None, tol: float = TOL_PP) -> bool:
    if a is None or b is None:
        return a is None and b is None
    return abs(a - b) < tol


def cross_check(label: str, mine: dict[str, Any], theirs: dict[str, Any],
                problems: list[str]) -> dict[str, Any]:
    """对账：k/n 必须全等；三个比例（point/cp_low/cp_high）与 rate_pct 差 <0.1pp。"""
    diffs: dict[str, Any] = {}
    for key in ("k", "n"):
        a, b = mine.get(key), theirs.get(key)
        if a != b:
            problems.append(f"{label}:{key} 不一致 {a} ≠ {b}")
        diffs[key] = [a, b]
    # 比例统一到**百分比**再比（容差 0.1pp）；对方产物没有的键跳过（不静默：记 skipped）
    for key in ("point", "cp_low", "cp_high", "rate_pct"):
        if key not in theirs:
            diffs[key] = "（对方产物无此键，跳过）"
            continue
        a, b = mine.get(key), theirs.get(key)
        if isinstance(a, float) and a <= 1.5:
            a = a * 100
        if isinstance(b, float) and b <= 1.5:
            b = b * 100
        if not _near(a, b, TOL_PP):
            problems.append(f"{label}:{key} 差 >{TOL_PP}pp：{a} ≠ {b}")
        diffs[key] = [a, b]
    return diffs


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="672h 扩样结果独立复算")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()

    problems: list[str] = []
    hs, cs = holdout_samples(), corpus_samples()
    fd_h, st_h = fd_verdicts(hs), static_verdicts(hs)
    fd_c, st_c = fd_verdicts(cs), static_verdicts(cs)

    def rate(fd: dict[str, str]) -> dict[str, Any]:
        ids = [i for i, v in fd.items() if v in ("catch", "miss")]
        k, n = sum(1 for i in ids if fd[i] == "catch"), len(ids)
        lo, hi = cp_interval(k, n)
        return {"k": k, "n": n,
                "point": (k / n) if n else None,          # 比例（0-1）
                "cp_low": lo, "cp_high": hi,              # 比例（0-1）
                "rate_pct": round(k / n * 100, 4) if n else None}

    mh, mc = rate(fd_h), rate(fd_c)
    pair_h, pair_c = pair_stats(fd_h, st_h), pair_stats(fd_c, st_c)

    # 路径对账 1：与 reveal 轮次产物
    r5 = jload(H_ROUND)["cumulative"]
    rc = jload(C_ROUND)["cumulative"]
    diffs = {
        "holdout_vs_reveal5": cross_check("holdout", mh, {
            "k": r5["error_subset"]["catch"], "n": r5["denominator"]["value"],
            "point": r5["cp95"]["point"], "cp_low": r5["cp95"]["cp_low"],
            "cp_high": r5["cp95"]["cp_high"],
            "rate_pct": r5["error_subset"]["detect_rate_pct"]}, problems),
        "corpus_vs_reveal672h": cross_check("corpus", mc, {
            "k": rc["catch"], "n": rc["denominator"]["value"],
            "point": rc["cp95"]["point"], "cp_low": rc["cp95"]["cp_low"],
            "cp_high": rc["cp95"]["cp_high"],
            "rate_pct": rc["detect_rate_pct"]}, problems),
    }
    # 路径对账 2：与 baseline_670a 落盘（三口径里的 measurable）
    if B_FD.is_file():
        bfd = jload(B_FD)
        diffs["holdout_vs_baseline670a"] = cross_check("holdout-baseline", mh, {
            "k": bfd["holdout"]["measurable"]["k"], "n": bfd["holdout"]["measurable"]["n"],
            "point": bfd["holdout"]["measurable"]["point"],
            "cp_low": bfd["holdout"]["measurable"]["cp_low"],
            "cp_high": bfd["holdout"]["measurable"]["cp_high"]}, problems)
        diffs["corpus_vs_baseline670a"] = cross_check("corpus-baseline", mc, {
            "k": bfd["corpus"]["measurable"]["k"], "n": bfd["corpus"]["measurable"]["n"],
            "point": bfd["corpus"]["measurable"]["point"],
            "cp_low": bfd["corpus"]["measurable"]["cp_low"],
            "cp_high": bfd["corpus"]["measurable"]["cp_high"]}, problems)
    if B_S.is_file():
        bs = jload(B_S)
        if bs["holdout"]["measurable"]["k"] != pair_h["static_k"]:
            problems.append("static 臂 holdout 不一致：%s ≠ %s"
                            % (bs["holdout"]["measurable"]["k"], pair_h["static_k"]))
        if bs["corpus"]["measurable"]["k"] != pair_c["static_k"]:
            problems.append("static 臂 corpus 不一致：%s ≠ %s"
                            % (bs["corpus"]["measurable"]["k"], pair_c["static_k"]))

    # 路径对账 3（可选）：与 ablation_stats_671b（仓库规范实现）比对同一配对
    third: dict[str, Any] = {}
    try:
        sys.path.insert(0, str(ROOT / "tools"))
        import ablation_stats_671b as A  # type: ignore  # noqa: PLC0415

        for name, pair, fd, st in (("holdout", pair_h, fd_h, st_h),
                                   ("corpus", pair_c, fd_c, st_c)):
            ids = [i for i, v in fd.items() if v in ("catch", "miss")]
            n = len(ids)
            b, c = pair["discordant"]["b_fd_only"], pair["discordant"]["c_static_only"]
            # 规范实现的**配对** WALD 版本（持有 b/c 时用它，与我的自实现同法）
            d = A.delta_ci_paired(b, c, n)
            h = A.cohens_h(pair["fd_k"] / n, pair["static_k"] / n)
            pm = A.mcnemar_exact(b, c)["p_value"]
            third[name] = {
                "method": d.get("method"),
                "ablation_stats_delta_ci_pct": [round(d["ci_low"] * 100, 4),
                                                round(d["ci_high"] * 100, 4)],
                "mine_delta_ci_pct": pair["delta_ci95_pct"],
                "ablation_stats_h": round(abs(h["h"]), 4), "mine_h": abs(pair["cohens_h"]),
                "ablation_stats_p": pm, "mine_p": pair["mcnemar_p"],
            }
            if abs(d["ci_low"] * 100 - pair["delta_ci95_pct"][0]) > TOL_PP or \
               abs(d["ci_high"] * 100 - pair["delta_ci95_pct"][1]) > TOL_PP:
                problems.append(f"{name}: 与 ablation_stats 的 ΔCI 差 >{TOL_PP}pp"
                                f"（{[round(d['ci_low']*100,4), round(d['ci_high']*100,4)]}"
                                f" ≠ {pair['delta_ci95_pct']}）")
            if abs(abs(h["h"]) - abs(pair["cohens_h"])) > 1e-4:
                problems.append(f"{name}: 与 ablation_stats 的 Cohen's h 不一致")
            if abs(pm - pair["mcnemar_p"]) > 1e-9:
                problems.append(f"{name}: 与 ablation_stats 的 McNemar p 不一致"
                                f"（{pm:.3e} ≠ {pair['mcnemar_p']:.3e}）")
    except Exception as e:  # noqa: BLE001
        third = {"status": f"跳过（{type(e).__name__}: {e}）"}

    rep = {
        "schema": "queyi-verify-expand/672h",
        "generated_by": "tools/verify_expand_672h.py（独立重实现；不 import 判据/统计库）",
        "tolerance_pp": TOL_PP,
        "sources": {"holdout_detail": H_DETAIL.relative_to(ROOT).as_posix(),
                    "corpus_detail": C_DETAIL.relative_to(ROOT).as_posix()},
        "holdout_fd": mh, "corpus_fd": mc,
        "paired_fd_vs_static": {"holdout": pair_h, "corpus": pair_c},
        "third_path_ablation_stats": third,
        "cross_path": diffs,
        "problems": problems,
        "verdict": "PASS" if not problems else "FAIL",
    }
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print(f"[verify-672h] holdout FD {mh['k']}/{mh['n']} = {mh['rate_pct']}% "
              f"CP95[{mh['cp_low']}, {mh['cp_high']}]")
        print(f"[verify-672h] corpus  FD {mc['k']}/{mc['n']} = {mc['rate_pct']}% "
              f"CP95[{mc['cp_low']}, {mc['cp_high']}]")
        for name, p in (("holdout", pair_h), ("corpus", pair_c)):
            ci_lo, ci_hi = p["delta_ci95_pct"]
            print(f"[verify-672h] {name} FD-Static: Δ{p['delta_pp']:+.2f}pp "
                  f"CI[{ci_lo:.2f}, {ci_hi:.2f}] "
                  f"p={p['mcnemar_p']:.2e} h={p['cohens_h']:.3f} "
                  f"(b={p['discordant']['b_fd_only']}, c={p['discordant']['c_static_only']})")
        print(f"[verify-672h] 双路径问题：{problems or '无（<0.1pp）'}")
        print(f"[verify-672h] verdict: {rep['verdict']}")
    if not a.no_write:
        OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8", newline="\n")
        print(f"[verify-672h] 写入 {OUT.relative_to(ROOT).as_posix()}")
    return 0 if not problems else 1


def selftest() -> int:
    ok = 0
    # CP 区间：与已知值对齐（17/21 → 58.1/94.6；110/114 → 91.3/99.0）
    lo, hi = cp_interval(17, 21)
    assert lo is not None and hi is not None
    assert abs(lo * 100 - 58.1) < 0.2 and abs(hi * 100 - 94.6) < 0.2, (lo, hi)
    ok += 1
    lo, hi = cp_interval(110, 114)
    assert lo is not None and hi is not None
    assert abs(lo * 100 - 91.3) < 0.2 and abs(hi * 100 - 99.0) < 0.2, (lo, hi)
    ok += 1
    assert cp_interval(0, 0) == (None, None)
    ok += 1
    # 端点：0/n 与 n/n
    lo, hi = cp_interval(0, 20)
    assert lo == 0.0 and hi is not None and 16.0 < hi * 100 < 17.5, (lo, hi)
    ok += 1
    lo, hi = cp_interval(20, 20)
    assert hi == 1.0 and lo is not None and 82.5 < lo * 100 < 84.5, (lo, hi)
    ok += 1
    # McNemar 精确：b=13,c=0 → 2/2^13
    assert abs(mcnemar_exact_p(13, 0) - 2 / 2 ** 13) < 1e-12
    ok += 1
    assert abs(mcnemar_exact_p(16, 0) - 2 / 2 ** 16) < 1e-12
    ok += 1
    assert mcnemar_exact_p(0, 0) == 1.0
    ok += 1
    # Cohen's h：已知量级
    assert abs(cohens_h(0.81, 0.048) - 1.798) < 0.01
    ok += 1
    # Wald Δ CI：b=16,c=0,n=21 → 点值 76.19pp（端点自洽）
    lo, hi = wald_delta_ci(16, 0, 21)
    assert lo < 16 / 21 < hi and abs((16 / 21 - lo) - (hi - 16 / 21)) < 1e-12
    ok += 1
    # Static 重分箱：sanitizer 样本记 miss、编译期仪器保持
    rows = [{"id": "a", "detector": "asan", "verdict": "catch"},
            {"id": "b", "detector": "compiler-warn", "verdict": "catch"},
            {"id": "c", "detector": "asan", "verdict": "unknown"}]
    st = static_verdicts(rows)
    assert st == {"a": "miss", "b": "catch", "c": "unknown"}, st
    ok += 1
    print(f"[verify-672h-selftest] {ok} 项通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
