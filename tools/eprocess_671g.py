#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""eprocess_671g.py — 671g D2：e-process 序贯检验（天然支持 peeking/任意期中分析）。

为什么需要它（671c #44）
==========================
固定样本量检验（Neyman–Pearson）**不能边收数据边看**：每 peek 一次都要校正 α
（α-spending / O'Brien–Fleming），否则一类错误膨胀。e-process 换一个框架：

  * 零假设 H0：每个样本 Bernoulli(μ0)（μ0 = 零假设下的检出率，事先钉死）；
  * 备择 H1：Bernoulli(μ1)，μ1≠μ0。为支持**复合备择**，对一条 μ1 网格做混合
    （先验权重的似然比混合）⇒ e-process（非负上鞅，H0 下期望恒为 1）；
  * 累积 e-value = Σ_j w_j Π_i L_ij，每个新样本**乘**一个似然比（见 :func:`log_lr`）；
  * 停止规则：sup e_t ≥ 1/α（如 α=0.05 ⇒ 20）。Ville 不等式保证：
    H0 下**任意时刻、任意次数 peek** 越过阈值的概率 ≤ α——扩样不需要校正。

与 452 账本的关系：每个新判决样本追加一行（:func:`append_event`，append-only），
e-value 随之更新；该账本的哈希链由 D6 的 G-LEDGER-INVARIANTS 守。

用法
====
    python tools/eprocess_671g.py --mu0 0.5 --seq 1 0 1 1 0
    python tools/eprocess_671g.py --sim-type1 --n 200 --reps 5000 --alpha 0.05
    python tools/eprocess_671g.py --ledger data/671g/eprocess_ledger.jsonl --mu0 0.5 --x 1
"""
from __future__ import annotations

import argparse
import json
import math
import random
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "queyi-eprocess/671g"
DEFAULT_ALPHA = 0.05


def log_lr(x: int, mu0: float, mu1: float) -> float:
    """单样本对数似然比 log [P(x|μ1)/P(x|μ0)]（Bernoulli）。"""
    if not (0.0 < mu0 < 1.0 and 0.0 < mu1 < 1.0):
        raise ValueError("μ0/μ1 必须在 (0,1) 内（边界请换精确检验）")
    if x == 1:
        return math.log(mu1 / mu0)
    if x == 0:
        return math.log((1.0 - mu1) / (1.0 - mu0))
    raise ValueError("Bernoulli 样本只接受 0/1")


def default_mu1_grid(mu0: float, step: float = 0.05) -> list[float]:
    """复合备择的混合网格：(0,1) 上等距，剔除 μ0 本身。"""
    grid = [round(step * i, 4) for i in range(1, int(round(1.0 / step)))]
    return [m for m in grid if abs(m - mu0) > 1e-9]


def _logsumexp(a: list[float]) -> float:
    m = max(a)
    return m + math.log(sum(math.exp(v - m) for v in a))


def e_value_sequence(outcomes: list[int], mu0: float,
                    mu1_grid: list[float] | None = None,
                    weights: list[float] | None = None) -> list[float]:
    """逐样本累积 e-value 序列（复合备择混合；H0 下是 e-process）。

    返回长度 = len(outcomes)+1，首项恒为 1（空序列）。
    """
    grid = mu1_grid or default_mu1_grid(mu0)
    if not grid:
        raise ValueError("μ1 网格为空")
    if weights is None:
        w = [1.0 / len(grid)] * len(grid)
    else:
        if len(weights) != len(grid):
            raise ValueError("weights 长度与网格不一致")
        s = sum(weights)
        w = [x / s for x in weights]
    logw = [math.log(x) for x in w]
    cum = [0.0] * len(grid)          # 每个 μ1 的累积对数似然比
    series = [1.0]
    for x in outcomes:
        for j, mu1 in enumerate(grid):
            cum[j] += log_lr(x, mu0, mu1)
        series.append(math.exp(_logsumexp([logw[j] + cum[j] for j in range(len(grid))])))
    return series


def stop_at(series: list[float], alpha: float = DEFAULT_ALPHA) -> int | None:
    """首次越过 1/α 的下标（0-based，对应越过前已看样本数）；未越过返回 None。"""
    th = 1.0 / alpha
    for i, e in enumerate(series):
        if e >= th - 1e-12:
            return i
    return None


def append_event(ledger_path: Path, x: int, mu0: float,
               mu1_grid: list[float] | None = None,
               prior: list[dict[str, Any]] | None = None,
               alpha: float = DEFAULT_ALPHA) -> dict[str, Any]:
    """追加一行 e-process 事件（append-only；不修改历史）。返回追加的事件。"""
    prior = prior if prior is not None else read_ledger(ledger_path)
    outcomes = [int(rec["x"]) for rec in prior] + [int(x)]
    e = e_value_sequence(outcomes, mu0, mu1_grid)
    event = {"schema": SCHEMA, "ts": time.strftime("%Y-%m-%d %H:%M:%S"),
             "seq_index": len(prior), "x": int(x), "mu0": mu0,
             "e_value_after": e[-1], "alpha": alpha,
             "stop": e[-1] >= 1.0 / alpha - 1e-12}
    with ledger_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")
    return event


def read_ledger(ledger_path: Path) -> list[dict[str, Any]]:
    if not ledger_path.is_file():
        return []
    out = []
    for line in ledger_path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            out.append(json.loads(line))
    return out


def type1_simulation(mu0: float, n: int = 200, reps: int = 5000,
                      alpha: float = DEFAULT_ALPHA, seed: int = 20261001) -> dict[str, Any]:
    """H0 仿真：估 Ville 一类错误率，应 ≤ alpha（带 Monte Carlo 噪声）。"""
    rng = random.Random(seed)
    grid = default_mu1_grid(mu0)
    th = 1.0 / alpha
    reject = 0
    stop_times: list[int] = []
    for _ in range(reps):
        cum = [0.0] * len(grid)
        logw = [-math.log(len(grid))] * len(grid)
        stopped = False
        for t in range(1, n + 1):
            x = 1 if rng.random() < mu0 else 0
            for j, mu1 in enumerate(grid):
                cum[j] += log_lr(x, mu0, mu1)
            e = math.exp(_logsumexp([logw[j] + cum[j] for j in range(len(grid))]))
            if e >= th - 1e-12 and not stopped:
                reject += 1
                stop_times.append(t)
                stopped = True
    return {"mu0": mu0, "n": n, "reps": reps, "alpha": alpha, "threshold": th,
            "rejections": reject, "type1_rate": reject / reps,
            "bound_ok": reject / reps <= alpha + 2.0 * math.sqrt(alpha / reps) + 1e-12}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g D2：e-process 序贯检验")
    ap.add_argument("--mu0", type=float, default=0.5)
    ap.add_argument("--seq", nargs="*", type=int, default=None)
    ap.add_argument("--alpha", type=float, default=DEFAULT_ALPHA)
    ap.add_argument("--sim-type1", action="store_true")
    ap.add_argument("--n", type=int, default=200)
    ap.add_argument("--reps", type=int, default=5000)
    ap.add_argument("--ledger", default=None)
    ap.add_argument("--x", type=int, default=None)
    a = ap.parse_args(argv)
    if a.sim_type1:
        print(json.dumps(type1_simulation(a.mu0, a.n, a.reps, a.alpha), indent=2))
        return 0
    if a.ledger is not None and a.x is not None:
        ev = append_event(Path(a.ledger), a.x, a.mu0, alpha=a.alpha)
        print(json.dumps(ev, ensure_ascii=False, indent=2))
        return 1 if ev["stop"] else 0
    seq = a.seq or []
    s = e_value_sequence(seq, a.mu0)
    stop = stop_at(s, a.alpha)
    print(json.dumps({"mu0": a.mu0, "outcomes": seq, "e_series": [round(v, 6) for v in s],
                     "threshold": 1 / a.alpha, "stop_index": stop,
                     "reject": stop is not None}, ensure_ascii=False, indent=2))
    return 1 if stop is not None else 0


if __name__ == "__main__":
    raise SystemExit(main())
