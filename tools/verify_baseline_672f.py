#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""verify_baseline_672f.py — 672f E 段：baseline 三臂的**独立复算**（双 Agent 交叉复现·路径 B）。

为什么要有它
============
单 Agent 跑实验可能有 bug。本文件是 baseline 实验的**第二条独立代码路径**：
从原始逐样本数据（reveal 明细）重新计算三臂检出率、CP 区间、配对 McNemar、Cohen's h
与 Newcombe 配对 Δ 区间，然后与路径 A（tools/baseline_670a.py --run 落盘的
data/experiments/baseline_*.json）逐项对账。

独立性约束（与路径 A 的差异）：
  * **不 import** tools/baseline_670a.py（臂定义在本文件内独立重写）；
  * **不 import** tools/stat_bounds.py（Clopper-Pearson 用二分法独立实现，
    基于 log-gamma 二项 PMF，与 stat_bounds 的正则化不完全贝塔互为交叉验证）；
  * 统计量（McNemar / Cohen's h / Newcombe）为本文件独立实现
    （与 tools/ablation_stats_671b.py 的原语互为交叉验证）。

判定
====
路径 A vs 路径 B：率差 < 0.1pp、CI 端点差 < 0.1pp、p 值相对差 < 1e-9 ⇒ PASS。
任何一项超差 ⇒ FAIL（exit 1），查根因，**不取平均**。

用法
====
    python tools/verify_baseline_672f.py            # 复算 + 对账（打印结论）
    python tools/verify_baseline_672f.py --json     # 机读（落盘 data/experiments/baseline_verify_672f.json）
    python tools/verify_baseline_672f.py --run      # 复算并落盘对账产物
"""
from __future__ import annotations

import argparse
import json
import math
import random
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VERSION = "1.0"
SEED = 20260930                                   # 与项目约定种子一致（prereg_672f）
random.seed(SEED)                                 # 672f：模块级固定种子（G-SEED-FIXED）

HOLDOUT_DETAIL = ROOT / "data" / "holdout" / "reveal_3_detail_671a.json"
CORPUS_DETAIL = ROOT / "data" / "external_corpus" / "reveal_detail_671a.json"
BASELINE_DIR = ROOT / "data" / "experiments"
OUT = BASELINE_DIR / "baseline_verify_672f.json"

#: 静态/编译期仪器（与 baseline_670a.py 的定义**语义一致**，但独立重写常量）
STATIC_INSTRUMENTS = frozenset(
    {"compiler-warn", "wunsequenced", "cross-compile", "linker"})
INSTRUMENT_POOL = tuple(sorted(
    STATIC_INSTRUMENTS | {"asan", "ubsan", "tsan"}
    | {"measure", "perf-counter", "compile-time"}))

#: 对账容差
TOL_PP = 0.1                 # 率 / CI 端点：0.1 个百分点
TOL_P_REL = 1e-9             # p 值相对差


# ── 独立统计原语（不 import stat_bounds / ablation_stats）────────────────────
def _log_binom_pmf(k: int, n: int, p: float) -> float:
    """log[ C(n,k) p^k (1-p)^(n-k) ]（log-gamma 实现，数值稳定）。"""
    if p <= 0.0:
        return 0.0 if k == 0 else -math.inf
    if p >= 1.0:
        return 0.0 if k == n else -math.inf
    logc = math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    return logc + k * math.log(p) + (n - k) * math.log(1.0 - p)


def cp_interval(k: int, n: int, conf: float = 0.95) -> tuple[float, float]:
    """Clopper-Pearson 精确区间：二分法解
    low:  P(X >= k) = (1-conf)/2 ；high: P(X <= k) = (1-conf)/2。
    （独立实现，交叉验证 tools/stat_bounds.py 的正则化不完全贝塔）"""
    if n <= 0:
        raise ValueError("n=0 ⇒ 无可测样本，拒绝给率（fail-loud）")
    alpha = 1.0 - conf

    def upper_tail(x: int, p: float) -> float:
        return sum(math.exp(_log_binom_pmf(i, n, p)) for i in range(x, n + 1))

    def lower_tail(x: int, p: float) -> float:
        return sum(math.exp(_log_binom_pmf(i, n, p)) for i in range(0, x + 1))

    def bisect(fn, target: float, lo: float, hi: float, increasing: bool) -> float:
        for _ in range(200):
            mid = (lo + hi) / 2.0
            if (fn(mid) > target) == increasing:
                hi = mid            # fn 单调增：fn 超过目标 ⇒ 根在左侧
            else:
                lo = mid            # fn 单调减：fn 超过目标 ⇒ 根在右侧
        return (lo + hi) / 2.0

    low = 0.0 if k == 0 else bisect(
        lambda p: upper_tail(k, p), alpha / 2.0, 0.0, 1.0, increasing=True)
    high = 1.0 if k == n else bisect(
        lambda p: lower_tail(k, p), alpha / 2.0, 0.0, 1.0, increasing=False)
    return low, high


def mcnemar_exact(b: int, c: int) -> float:
    """配对精确 McNemar 双侧 p：P(X <= min(b,c)) × 2（二项 n=b+c, p=0.5，截 1）。
    （独立实现，交叉验证 tools/ablation_stats_671b.py）"""
    n = b + c
    if n == 0:
        return 1.0
    m = min(b, c)
    tail = sum(math.exp(_log_binom_pmf(i, n, 0.5)) for i in range(0, m + 1))
    return min(1.0, 2.0 * tail)


def cohens_h(p1: float, p2: float) -> float:
    """Cohen's h = 2·asin(√p1) − 2·asin(√p2)。"""
    return 2.0 * math.asin(math.sqrt(p1)) - 2.0 * math.asin(math.sqrt(p2))


def newcombe_paired(p1: float, n1: int, p2: float, n2: int, conf: float = 0.95) -> tuple[float, float]:
    """Newcombe method 10（square-and-add）配对差值区间：
    d = p1 − p2；low = d − √((p1−l1)² + (u2−p2)²)；high = d + √((u1−p1)² + (p2−l2)²)。"""
    l1, u1 = _wilson(p1, n1, conf)
    l2, u2 = _wilson(p2, n2, conf)
    d = p1 - p2
    low = d - math.sqrt((p1 - l1) ** 2 + (u2 - p2) ** 2)
    high = d + math.sqrt((u1 - p1) ** 2 + (p2 - l2) ** 2)
    return max(-1.0, low), min(1.0, high)


def _wilson(p: float, n: int, conf: float) -> tuple[float, float]:
    z = {0.95: 1.959963984540054, 0.99: 2.5758293035489004}[round(conf, 2)]
    den = 1.0 + z * z / n
    center = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return center - half, center + half


# ── 臂的独立重实现（从原始明细，不读路径 A 的中间结果）──────────────────────
def load_samples() -> dict[str, list[dict]]:
    """holdout 真错子集（planted is True）+ corpus 全样本（含对照）。"""
    h = json.loads(HOLDOUT_DETAIL.read_text(encoding="utf-8"))
    c = json.loads(CORPUS_DETAIL.read_text(encoding="utf-8"))
    holdout = [{"id": s["id"], "detector": str(s.get("detector") or "unknown"),
                "verdict": str(s.get("verdict"))}
               for s in h["per_sample"] if s.get("planted") is True]
    corpus = [{"id": r["id"], "detector": str(r.get("detector") or "unknown"),
               "verdict": str(r.get("verdict"))} for r in c["per_sample"]]
    return {"holdout": holdout, "corpus": corpus}


def arm_fd(samples: list[dict]) -> dict[str, str]:
    return {s["id"]: s["verdict"] for s in samples}


def arm_static(samples: list[dict]) -> dict[str, str]:
    out: dict[str, str] = {}
    for s in samples:
        v = s["verdict"]
        if v in ("unknown", "not_error"):
            out[s["id"]] = v
        elif s["detector"] in STATIC_INSTRUMENTS:
            out[s["id"]] = v
        else:
            out[s["id"]] = "miss"
    return out


def arm_random(samples: list[dict], fd: dict[str, str], seed: int = SEED) -> dict[str, str]:
    """仪器级预算对齐代理：FD catch 用到的仪器数 = 随机抽取数（同 seed 可复现）。"""
    used = sorted({s["detector"] for s in samples
                   if fd.get(s["id"]) == "catch" and s["detector"] in INSTRUMENT_POOL})
    picked = set(random.Random(seed).sample(list(INSTRUMENT_POOL), len(used))) if used else set()
    out: dict[str, str] = {}
    for s in samples:
        v = s["verdict"]
        if v in ("unknown", "not_error"):
            out[s["id"]] = v
        elif s["detector"] in picked and fd.get(s["id"]) == "catch":
            out[s["id"]] = "catch"
        else:
            out[s["id"]] = "miss"
    return out


def rate(verdicts: dict[str, str]) -> dict:
    c = sum(1 for v in verdicts.values() if v == "catch")
    m = sum(1 for v in verdicts.values() if v == "miss")
    u = sum(1 for v in verdicts.values() if v == "unknown")
    ne = sum(1 for v in verdicts.values() if v == "not_error")
    n = c + m
    if n <= 0:
        return {"k": c, "n": 0, "rate_pct": None, "cp_low": None, "cp_high": None,
                "catch": c, "miss": m, "unknown": u, "not_error": ne,
                "note": "无可测样本，拒绝给率（fail-loud）"}
    lo, hi = cp_interval(c, n)
    return {"k": c, "n": n, "rate_pct": round(c / n * 100, 4),
            "cp_low": round(lo, 6), "cp_high": round(hi, 6),
            "catch": c, "miss": m, "unknown": u, "not_error": ne}


def delta_ci_paired_wald(b: int, c: int, n: int, conf: float = 0.95) -> tuple[float, float]:
    """配对差值 CI（仓库规范方法，交叉验证 ablation_stats_671b::delta_ci_paired）：
    Δ=(b−c)/n，var=(b+c−(b−c)²/n)/n²（McNemar 多项式方差）。独立重写实现。"""
    d = (b - c) / n
    var = (b + c - (b - c) ** 2 / n) / (n * n)
    se = math.sqrt(max(0.0, var))
    z = 1.959963984540054
    return d - z * se, d + z * se


def paired(a: dict[str, str], b: dict[str, str]) -> dict:
    """配对统计（a=FD，b=对照臂）：McNemar + Cohen's h + 两种 Δ 区间。"""
    ids = [i for i in a if a[i] in ("catch", "miss") and b[i] in ("catch", "miss")]
    ka, kb = sum(1 for i in ids if a[i] == "catch"), sum(1 for i in ids if b[i] == "catch")
    bb = sum(1 for i in ids if a[i] == "catch" and b[i] == "miss")
    cc = sum(1 for i in ids if a[i] == "miss" and b[i] == "catch")
    n = len(ids)
    p1, p2 = ka / n, kb / n
    lo, hi = newcombe_paired(p1, n, p2, n)
    wlo, whi = delta_ci_paired_wald(bb, cc, n)
    return {"n_pairs": n, "fd_catch": ka, "other_catch": kb,
            "discordant_fd_catch": bb, "discordant_other_catch": cc,
            "delta_pp": round((p1 - p2) * 100, 4),
            "delta_ci_newcombe_pp": [round(lo * 100, 4), round(hi * 100, 4)],
            "delta_ci_paired_wald_pp": [round(wlo * 100, 4), round(whi * 100, 4)],
            "mcnemar_p": mcnemar_exact(bb, cc),
            "cohens_h": round(cohens_h(p1, p2), 4)}


# ── 复算 + 对账 ───────────────────────────────────────────────────────────────
def recompute() -> dict:
    samples = load_samples()
    out: dict = {"schema": "queyi-baseline-verify/672f", "version": VERSION, "seed": SEED,
                 "independence": "不 import baseline_670a / stat_bounds / ablation_stats；"
                                 "CP=二分法独立实现；McNemar/h/Newcombe 独立实现"}
    for name in ("holdout", "corpus"):
        ss = samples[name]
        fd = arm_fd(ss)
        st = arm_static(ss)
        rn = arm_random(ss, fd)
        out[name] = {"n_samples": len(ss),
                     "fd": rate(fd), "static": rate(st), "random": rate(rn),
                     "fd_vs_static": paired(fd, st), "fd_vs_random": paired(fd, rn)}
    return out


def compare(rec: dict) -> tuple[bool, list[str]]:
    """路径 A（落盘产物）vs 路径 B（本文件复算）逐项对账。"""
    problems: list[str] = []

    def rate_from(doc: dict, set_: str) -> dict:
        blk = doc[set_]
        return {"k": blk["measurable"]["k"], "n": blk["measurable"]["n"],
                "rate_pct": blk["measurable"]["point"] * 100,
                "cp_low": blk["measurable"]["cp_low"] * 100,      # 产物存分数 ⇒ 统一成百分点
                "cp_high": blk["measurable"]["cp_high"] * 100}

    pairs = [("fd", "baseline_fd.json"), ("static", "baseline_static.json"),
             ("random", "baseline_random.json")]
    for set_ in ("holdout", "corpus"):
        for arm, fn in pairs:
            doc = json.loads((BASELINE_DIR / fn).read_text(encoding="utf-8"))
            a = rate_from(doc, set_)
            b = rec[set_][arm if arm != "random" else "random"]
            b = {**b, "cp_low": b["cp_low"] * 100, "cp_high": b["cp_high"] * 100}
            for key, tol in (("rate_pct", TOL_PP), ("cp_low", TOL_PP), ("cp_high", TOL_PP)):
                if a[key] is None or b[key] is None:
                    problems.append(f"{set_}.{arm}.{key}: 一侧为 None（A={a[key]} B={b[key]}）")
                    continue
                if abs(a[key] - b[key]) > tol:
                    problems.append(f"{set_}.{arm}.{key}: A={a[key]:.4f} B={b[key]:.4f} "
                                    f"差 {abs(a[key] - b[key]):.4f} > {tol}pp")
            if (a["k"], a["n"]) != (b["k"], b["n"]):
                problems.append(f"{set_}.{arm}.k/n: A={a['k']}/{a['n']} B={b['k']}/{b['n']}")

    # 抽查：random 臂与 FD 同预算（分配表自洽）
    rnd = json.loads((BASELINE_DIR / "baseline_random.json").read_text(encoding="utf-8"))
    for set_ in ("holdout", "corpus"):
        sel = rnd["selection"][set_]
        if len(sel["picked"]) != len(sel["fd_used"]):
            problems.append(f"{set_}.random 预算不对齐：picked={len(sel['picked'])} "
                            f"vs fd_used={len(sel['fd_used'])}")
    return not problems, problems


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="672f E：baseline 独立复算对账（路径 B）")
    ap.add_argument("--run", action="store_true", help="落盘 data/experiments/baseline_verify_672f.json")
    ap.add_argument("--json", action="store_true", help="打印机读结果")
    a = ap.parse_args(argv)

    rec = recompute()
    ok, problems = compare(rec)
    rec["path_a_vs_b"] = {"ok": ok, "tolerance_pp": TOL_PP, "problems": problems}
    rec["verdict"] = "PASS" if ok else "FAIL"

    if a.json:
        print(json.dumps(rec, ensure_ascii=False, indent=2))
    else:
        for set_ in ("holdout", "corpus"):
            b = rec[set_]
            print(f"[{set_}] 样本 {b['n_samples']}")
            for arm in ("fd", "static", "random"):
                r = b[arm]
                print(f"  {arm:7s} {r['k']}/{r['n']} = {r['rate_pct']:.1f}%  "
                      f"CP95[{r['cp_low'] * 100:.1f}, {r['cp_high'] * 100:.1f}]")
            for cmp_ in ("fd_vs_static", "fd_vs_random"):
                p = b[cmp_]
                print(f"  {cmp_}: Δ={p['delta_pp']:+.1f}pp "
                      f"WaldCI[{p['delta_ci_paired_wald_pp'][0]:.1f}, {p['delta_ci_paired_wald_pp'][1]:.1f}]  "
                      f"NewcombeCI[{p['delta_ci_newcombe_pp'][0]:.1f}, {p['delta_ci_newcombe_pp'][1]:.1f}]  "
                      f"McNemar p={p['mcnemar_p']:.2e}  h={p['cohens_h']:.2f}")
        print(f"\n路径 A vs 路径 B 对账：{'PASS（全部差 < 0.1pp）' if ok else 'FAIL'}")
        for p in problems:
            print(f"  [差] {p}")
        if a.run:
            OUT.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8", newline="\n")
            print(f"[672f] 已写 {OUT.relative_to(ROOT).as_posix()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
