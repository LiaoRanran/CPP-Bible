#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""verify_baseline_672g.py — 672g 双路径交叉复现（路径 B：独立重实现）。

独立性约束（与路径 A `tools/baseline_672g.py` 的差异）
====================================================
* **不 import** tools/baseline_672g.py（臂定义在本文件内独立重写）；
* **不 import** tools/stat_bounds.py（Clopper–Pearson 用二分法 + log-gamma 独立实现）；
* **不 import** tools/ablation_stats_671b.py（McNemar / Cohen's h / Wald Δ CI 独立实现）；
* 随机臂：**直接**用 `random.Random(seed).sample(pool, n)` 复算（不调 select_assets 的
  `--n` 分支）⇒ 独立验证"拆仓接口的选中集合 == 规范抽样"。

判定：率差 < 0.1pp、CI 端点差 < 0.1pp、k/n 完全一致 ⇒ PASS；任何一项超差 ⇒ FAIL。

用法
====
    python tools/verify_baseline_672g.py            # 复算 + 对账（打印结论）
    python tools/verify_baseline_672g.py --run      # 落盘 data/experiments/baseline_verify_672g.json
"""
from __future__ import annotations

import argparse
import json
import math
import os
import random
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

VERSION = "1.0"
SEED = 20260930
random.seed(SEED)

HOLDOUT_DETAIL = ROOT / "data" / "holdout" / "reveal_3_detail_671a.json"
CORPUS_DETAIL = ROOT / "data" / "external_corpus" / "reveal_detail_671a.json"
BASELINE_DIR = ROOT / "data" / "experiments"
OUT = BASELINE_DIR / "baseline_verify_672g.json"
PATH_A = BASELINE_DIR / "b3_real_672g.json"

QUEYI_VERIFIER = Path(os.environ.get("QUEYI_VERIFIER", r"C:/CodeLearnling/queyi-verifier"))
SELECTOR = QUEYI_VERIFIER / "tools" / "select_assets_672g.py"

#: 静态/编译期资产（语义与 baseline_670a 一致，但独立重写常量）
STATIC_ASSETS = frozenset({"compiler-warn", "wunsequenced", "cross-compile", "linker"})

TOL_PP = 0.1


# ── 池：从拆仓查询（池产权在拆仓）────────────────────────────────────────────
def fetch_pool() -> list[str]:
    proc = subprocess.run([sys.executable, str(SELECTOR), "--print-pool", "--json"],
                          capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError(f"取拆仓池失败：{proc.stderr.strip()}")
    return list(json.loads(proc.stdout)["pool"])


# ── 独立统计原语 ─────────────────────────────────────────────────────────────
def _log_binom_pmf(k: int, n: int, p: float) -> float:
    if p <= 0.0:
        return 0.0 if k == 0 else -math.inf
    if p >= 1.0:
        return 0.0 if k == n else -math.inf
    logc = math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1)
    return logc + k * math.log(p) + (n - k) * math.log(1.0 - p)


def cp_interval(k: int, n: int, conf: float = 0.95) -> tuple[float, float]:
    if n <= 0:
        raise ValueError("n=0 ⇒ 拒绝给率（fail-loud）")
    alpha = 1.0 - conf

    def upper_tail(x: int, p: float) -> float:
        return sum(math.exp(_log_binom_pmf(i, n, p)) for i in range(x, n + 1))

    def lower_tail(x: int, p: float) -> float:
        return sum(math.exp(_log_binom_pmf(i, n, p)) for i in range(0, x + 1))

    def bisect(fn, target: float, increasing: bool) -> float:
        lo, hi = 0.0, 1.0
        for _ in range(200):
            mid = (lo + hi) / 2.0
            if (fn(mid) > target) == increasing:
                hi = mid
            else:
                lo = mid
        return (lo + hi) / 2.0

    low = 0.0 if k == 0 else bisect(lambda p: upper_tail(k, p), alpha / 2.0, True)
    high = 1.0 if k == n else bisect(lambda p: lower_tail(k, p), alpha / 2.0, False)
    return low, high


def mcnemar_exact(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    m = min(b, c)
    tail = sum(math.exp(_log_binom_pmf(i, n, 0.5)) for i in range(0, m + 1))
    return min(1.0, 2.0 * tail)


def cohens_h(p1: float, p2: float) -> float:
    return 2.0 * math.asin(math.sqrt(p1)) - 2.0 * math.asin(math.sqrt(p2))


def delta_ci_wald(b: int, c: int, n: int) -> tuple[float, float]:
    d = (b - c) / n
    var = (b + c - (b - c) ** 2 / n) / (n * n)
    se = math.sqrt(max(0.0, var))
    z = 1.959963984540054
    return d - z * se, d + z * se


# ── 臂的独立重实现 ───────────────────────────────────────────────────────────
def load_samples() -> dict[str, list[dict]]:
    h = json.loads(HOLDOUT_DETAIL.read_text(encoding="utf-8"))
    c = json.loads(CORPUS_DETAIL.read_text(encoding="utf-8"))
    return {
        "holdout": [{"id": s["id"], "detector": str(s.get("detector") or "unknown"),
                     "verdict": str(s.get("verdict"))}
                    for s in h["per_sample"] if s.get("planted") is True],
        "corpus": [{"id": r["id"], "detector": str(r.get("detector") or "unknown"),
                    "verdict": str(r.get("verdict"))} for r in c["per_sample"]],
    }


def arm_fd(samples):
    return {s["id"]: s["verdict"] for s in samples}


def arm_static(samples):
    out = {}
    for s in samples:
        v = s["verdict"]
        if v in ("unknown", "not_error"):
            out[s["id"]] = v
        elif s["detector"] in STATIC_ASSETS:
            out[s["id"]] = v
        else:
            out[s["id"]] = "miss"
    return out


def arm_random(samples, fd, pool, seed=SEED):
    """独立重实现：直接 random.sample（不调拆仓的 --n 分支）⇒ 交叉验证接口选中集合。"""
    used = sorted({s["detector"] for s in samples
                   if fd.get(s["id"]) == "catch" and s["detector"] in set(pool)})
    picked = set(random.Random(seed).sample(list(pool), len(used))) if used else set()
    out = {}
    for s in samples:
        v = s["verdict"]
        if v in ("unknown", "not_error"):
            out[s["id"]] = v
        elif s["detector"] in picked and fd.get(s["id"]) == "catch":
            out[s["id"]] = "catch"
        else:
            out[s["id"]] = "miss"
    return out, sorted(picked), used


def rate(v):
    c = sum(1 for x in v.values() if x == "catch")
    m = sum(1 for x in v.values() if x == "miss")
    n = c + m
    if n <= 0:
        return {"k": c, "n": 0, "rate_pct": None, "cp_low": None, "cp_high": None}
    lo, hi = cp_interval(c, n)
    return {"k": c, "n": n, "rate_pct": round(c / n * 100, 4),
            "cp_low": round(lo * 100, 6), "cp_high": round(hi * 100, 6)}


def paired(a, b):
    ids = [i for i in a if a[i] in ("catch", "miss") and b[i] in ("catch", "miss")]
    ka = sum(1 for i in ids if a[i] == "catch")
    kb = sum(1 for i in ids if b[i] == "catch")
    n = len(ids)
    bb = sum(1 for i in ids if a[i] == "catch" and b[i] != "catch")
    cc = sum(1 for i in ids if a[i] != "catch" and b[i] == "catch")
    lo, hi = delta_ci_wald(bb, cc, n)
    return {"n_pairs": n, "delta_pp": round((ka - kb) / n * 100, 4),
            "ci_paired_wald_pp": [round(lo * 100, 4), round(hi * 100, 4)],
            "mcnemar_p": mcnemar_exact(bb, cc),
            "cohens_h": round(cohens_h(ka / n, kb / n), 4)}


def recompute() -> dict:
    pool = fetch_pool()
    samples = load_samples()
    out = {"schema": "queyi-baseline-verify/672g", "version": VERSION, "seed": SEED,
           "asset_pool": pool,
           "independence": "不 import baseline_672g / stat_bounds / ablation_stats；"
                           "CP=二分法；McNemar/h/Wald 独立实现；random 直接 sample"}
    for name in ("holdout", "corpus"):
        ss = samples[name]
        fd = arm_fd(ss)
        st = arm_static(ss)
        rn, picked, used = arm_random(ss, fd, pool)
        out[name] = {"n_samples": len(ss), "fd": rate(fd), "static": rate(st),
                     "random": rate(rn), "random_picked": picked, "random_fd_used": used,
                     "fd_vs_static": paired(fd, st), "fd_vs_random": paired(fd, rn)}
    return out


def compare(rec: dict) -> tuple[bool, list[str]]:
    problems: list[str] = []
    a = json.loads(PATH_A.read_text(encoding="utf-8"))

    def from_a(set_, arm):
        blk = a[set_][arm]["measurable"]
        return {"k": blk["k"], "n": blk["n"], "rate_pct": blk["point"] * 100,
                "cp_low": blk["cp_low"] * 100, "cp_high": blk["cp_high"] * 100}

    for set_ in ("holdout", "corpus"):
        for arm in ("fd", "static", "random"):
            x = from_a(set_, arm)
            y = rec[set_][arm]
            for key in ("rate_pct", "cp_low", "cp_high"):
                if abs(x[key] - y[key]) > TOL_PP:
                    problems.append(f"{set_}.{arm}.{key}: A={x[key]:.4f} B={y[key]:.4f}")
            if (x["k"], x["n"]) != (y["k"], y["n"]):
                problems.append(f"{set_}.{arm}.k/n: A={x['k']}/{x['n']} B={y['k']}/{y['n']}")
        # 统计量对账
        for cmp_ in ("fd_vs_static", "fd_vs_random"):
            pa, pb = a[set_][cmp_], rec[set_][cmp_]
            if abs(pa["delta_pp"] - pb["delta_pp"]) > TOL_PP:
                problems.append(f"{set_}.{cmp_}.delta_pp: A={pa['delta_pp']} B={pb['delta_pp']}")
            if abs(pa["mcnemar_p"] - pb["mcnemar_p"]) > 1e-12:
                problems.append(f"{set_}.{cmp_}.mcnemar_p: A={pa['mcnemar_p']} B={pb['mcnemar_p']}")
            if abs(pa["cohens_h"] - pb["cohens_h"]) > 1e-4:
                problems.append(f"{set_}.{cmp_}.cohens_h: A={pa['cohens_h']} B={pb['cohens_h']}")
        # 选中集合一致
        sel = a[set_]["random_selection"]
        if set(sel["picked"]) != set(rec[set_]["random_picked"]):
            problems.append(f"{set_}.random.picked: A={sel['picked']} B={rec[set_]['random_picked']}")
        if sorted(sel["fd_used"]) != sorted(rec[set_]["random_fd_used"]):
            problems.append(f"{set_}.random.fd_used 不一致")
    return not problems, problems


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="672g 双路径交叉复现（路径 B）")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--json", action="store_true")
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
                      f"CP95[{r['cp_low']:.1f}, {r['cp_high']:.1f}]")
            for cmp_ in ("fd_vs_static", "fd_vs_random"):
                p = b[cmp_]
                print(f"  {cmp_}: Δ={p['delta_pp']:+.1f}pp "
                      f"CI[{p['ci_paired_wald_pp'][0]:.1f},{p['ci_paired_wald_pp'][1]:.1f}] "
                      f"p={p['mcnemar_p']:.2e} h={p['cohens_h']:.2f}")
        print(f"\n路径 A vs 路径 B：{'PASS（差 < 0.1pp）' if ok else 'FAIL'}")
        for p in problems:
            print(f"  [差] {p}")
        if a.run:
            OUT.write_text(json.dumps(rec, ensure_ascii=False, indent=2) + "\n",
                           encoding="utf-8", newline="\n")
            print(f"[672g] 已写 {OUT.relative_to(ROOT).as_posix()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
