#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""retest_reliability_671g.py — 671g D7：单人隔周重标法（零合作者的 IRR 替代）。

问题（671f v44/16）
======================
标准 IRR 要≥2 个标注者；单人项目没有合作者。替代方案：**同一标注者隔一周**
对同一批样本独立重标（不看上轮标注），计算 test-retest 的 Cohen κ：
  * κ ≥ 0.8：标注稳定（可进数据集，仍不证明对，只证明自洽）；
  * 0.6 ≤ κ < 0.8：warn，需人审不一致项；
  * κ < 0.6 或样本 < 10：block / 不可判（样本太少不发布可靠性结论）。

**关键纪律**：重标必须**盲**（不看第一次答案，且间隔≥7 天）；否则测的是记忆不是稳定性。
这是 8B 评委"400 条标错 397 条"教训的地板之一（另一条见 D10 floor-check）。

用法
====
    python tools/retest_reliability_671g.py --round1 a,b,a --round2 a,b,b --labels a,b
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "queyi-retest/671g"
KAPPA_PASS = 0.8
KAPPA_WARN = 0.6
MIN_SAMPLES = 10
MIN_GAP_DAYS = 7


def cohen_kappa(r1: list[Any], r2: list[Any]) -> float:
    """Cohen κ（含完全一致=1、无方差标签集退化=0.0 但 observed<1 的边界）。"""
    if len(r1) != len(r2) or not r1:
        raise ValueError("两轮标注长度必须一致且非空")
    labels = sorted(set(r1) | set(r2))
    n = len(r1)
    po = sum(1 for a, b in zip(r1, r2) if a == b) / n
    pe = sum((r1.count(lab) / n) * (r2.count(lab) / n) for lab in labels)
    if pe >= 1.0 - 1e-12:
        return 1.0 if po >= 1.0 - 1e-12 else 0.0
    return (po - pe) / (1.0 - pe)


def disagreements(r1: list[Any], r2: list[Any], ids: list[Any] | None = None
               ) -> list[dict[str, Any]]:
    ids = ids or list(range(len(r1)))
    return [{"id": ids[i], "round1": r1[i], "round2": r2[i]}
            for i in range(len(r1)) if r1[i] != r2[i]]


def evaluate(r1: list[Any], r2: list[Any], *, ids: list[Any] | None = None,
            gap_days: float = MIN_GAP_DAYS, labels: list[Any] | None = None,
            min_samples: int = MIN_SAMPLES) -> dict[str, Any]:
    out: dict[str, Any] = {"schema": SCHEMA, "n": len(r1), "kappa": None, "status": "unknown"}
    if len(r1) != len(r2):
        return {**out, "status": "rejected", "why": "两轮长度不一致"}
    if len(r1) < min_samples:
        return {**out, "status": "inconclusive",
                "why": f"样本 {len(r1)}<{min_samples}，不足以发布可靠性结论"}
    if gap_days < MIN_GAP_DAYS:
        return {**out, "status": "rejected",
                "why": f"重标间隔 {gap_days}<{MIN_GAP_DAYS} 天（须盲隔一周，测的是稳定性不是记忆）"}
    k = cohen_kappa(r1, r2)
    dis = disagreements(r1, r2, ids)
    out.update(kappa=round(k, 6), disagreement_rate=round(len(dis) / len(r1), 6),
              disagreements=dis)
    if k >= KAPPA_PASS:
        out["status"] = "pass"
    elif k >= KAPPA_WARN:
        out["status"] = "warn"
    else:
        out["status"] = "block"
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g D7：单人隔周重标 κ")
    ap.add_argument("--round1", required=True)
    ap.add_argument("--round2", required=True)
    ap.add_argument("--ids", default=None)
    ap.add_argument("--gap-days", type=float, default=MIN_GAP_DAYS)
    a = ap.parse_args(argv)
    r1 = a.round1.split(",")
    r2 = a.round2.split(",")
    ids = a.ids.split(",") if a.ids else None
    rep = evaluate(r1, r2, ids=ids, gap_days=a.gap_days)
    print(json.dumps(rep, ensure_ascii=False, indent=2))
    return 1 if rep.get("status") in ("block", "rejected") else 0


if __name__ == "__main__":
    raise SystemExit(main())
