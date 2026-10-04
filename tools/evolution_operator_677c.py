#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""evolution_operator_677c.py — 677c C：failure-driven evolution operator 的**算法化**定义。

背景
====
国外大模型评审指出：论文里的 evolution operator E "不够像算法，更像 governance
framework + heuristic selection"。本模块把 E 钉成**可执行、可比较、可证伪**的算法：

    输入 : 当前资产集 C_t，失败集 F_t（派生集上未被 C_t 抓到的样本），候选集 A_candidate
    输出 : 下一个资产 a* = argmax_j score(a_j | F_t, C_t)

    score(a_j | F_t, C_t) = w1*failure_coverage + w2*novel_coverage
                            - w3*cost - w4*redundancy

四个分量（全部只用**派生集**信息 ⇒ 不是 oracle）
==================================================
* failure_coverage(a_j) = |{s ∈ F_t : a_j catches s}| / |F_t|
* novel_coverage(a_j)   — 两种模式：
    - ``literal``（默认，规格原文）：|{s ∈ F_t : a_j catches s 且 C_t 无资产抓 s}| / |F_t|。
      **数学事实**：F_t 的定义就是 "C_t 没抓到的样本"，于是第二个条件恒真，
      novel_coverage ≡ failure_coverage（一行证明见 ``novel_coverage`` docstring）。
      本批如实实现并**记录**这个坍缩——它解释了为什么消融里 ``fd_novel`` 与
      ``fd_only`` 选择完全一致（见 677c_operator_design_report.md）。
    - ``unique``（探索性修复）：|{s ∈ F_t : a_j catches s 且**其他候选**都抓不到 s}| / |F_t|，
      即"不可替代的残余覆盖"。这是让 novelty 成为独立信号的最小改动之一
      （不需要标签，不碰评测集），在消融里作为第 5 个探索性配置。
* cost(a_j) = wall_seconds(a_j) / max_wall（矩阵实测墙钟归一化；诚实边界：
  这是全量跑 1137 样本的墙钟，不是单样本成本，只做同口径相对比较）
* redundancy(a_j) = mean_{c ∈ C_t} Jaccard(catch(a_j), catch(c))（派生集 catch 集合）

与既有方法的关系（重要，写进了报告）
====================================
* 676f 的 FD = 派生集 catch 频率 top-k（**全局排序**，不迭代）；
* E 取 w1=1（fd_only）= **迭代式残余覆盖贪心** ≡ set-cover greedy（任务 B 的
  greedy 基线）；二者不是同一个算法，消融会给出选择与检出的双重对比。
* E 是确定性算法：给定 (index, deriv_ids, candidates, k, weights, novel_mode)，
  输出唯一（同分按资产 id 升序打破）。

用法
====
    python tools/evolution_operator_677c.py --check        # 自检（合成数据，只读）
"""
from __future__ import annotations

import argparse
from typing import Any

VERSION = "1.0"

#: 默认权重（卡片指定；**不是学习得到的**——消融实验展示权重敏感性）。
DEFAULT_WEIGHTS: dict[str, float] = {
    "w_failure": 0.3, "w_novel": 0.4, "w_cost": 0.1, "w_redundancy": 0.2,
}

#: 消融配置（卡片指定 4 个 + 本批加 1 个探索性 novel 修复变体）。
ABLATION_CONFIGS: dict[str, dict[str, Any]] = {
    "fd_only": {"weights": {"w_failure": 1.0, "w_novel": 0.0, "w_cost": 0.0, "w_redundancy": 0.0},
                "novel_mode": "literal", "note": "w1=1 其余=0 = 当前方法（纯 failure coverage）"},
    "fd_novel": {"weights": {"w_failure": 0.5, "w_novel": 0.5, "w_cost": 0.0, "w_redundancy": 0.0},
                 "novel_mode": "literal", "note": "FD+novel（literal 模式下 novel≡failure）"},
    "fd_novel_redundancy": {"weights": {"w_failure": 0.3, "w_novel": 0.4, "w_cost": 0.0,
                                        "w_redundancy": 0.3},
                            "novel_mode": "literal", "note": "FD+novel+redundancy"},
    "full": {"weights": dict(DEFAULT_WEIGHTS), "novel_mode": "literal",
             "note": "完整 4 分量（默认权重）"},
    "full_unique_novel": {"weights": dict(DEFAULT_WEIGHTS), "novel_mode": "unique",
                          "note": "探索性：novel 改为'其他候选都抓不到'的不可替代残余覆盖"},
}

Index = dict[str, dict[str, str]]


# ─────────────────────────────────────────────────────────────────────────────
# 基础量（纯函数）
# ─────────────────────────────────────────────────────────────────────────────
def catch_set(asset: str, index: Index, ids: list[str]) -> set[str]:
    """资产在 ids 上抓到的样本 id 集合。"""
    return {s for s in ids if index[s].get(asset) == "catch"}


def or_coverage(assets: list[str], index: Index, ids: list[str]) -> set[str]:
    """资产集合的 OR 覆盖（任一 catch ⇒ 覆盖）。与 AttributionExecutor 口径一致。"""
    out: set[str] = set()
    for a in assets:
        out |= catch_set(a, index, ids)
    return out


def failure_set(current: list[str], index: Index, ids: list[str]) -> set[str]:
    """F_t = 派生集上未被当前资产集 C_t 抓到的样本。"""
    return set(ids) - or_coverage(current, index, ids)


def jaccard(s1: set[str], s2: set[str]) -> float:
    """Jaccard 相似度；两个空集定义为 0（空资产间不判冗余）。"""
    if not s1 and not s2:
        return 0.0
    union = s1 | s2
    return len(s1 & s2) / len(union) if union else 0.0


def novel_coverage(asset: str, failures: set[str], current: list[str], candidates: list[str],
                   index: Index, ids: list[str], *, mode: str) -> float:
    """novel_coverage(a_j | F_t, C_t)。

    literal 模式（规格原文）
    -----------------------
    |{s ∈ F_t : a_j catches s 且 C_t 中没有资产抓到 s}| / |F_t|。
    由 F_t 的定义（C_t 无资产抓到 s 对**一切** s ∈ F_t 成立），第二个条件恒真，因此
    ``novel_coverage(literal) ≡ failure_coverage``。这不是实现偷懒，是规格本身的
    数学性质；本模块如实实现并在设计报告里披露（消融 fd_novel ≡ fd_only 即由此来）。

    unique 模式（探索性修复）
    -----------------------
    |{s ∈ F_t : a_j catches s 且**其他候选资产**都抓不到 s}| / |F_t|——
    不可替代的残余覆盖。C_t 之外的候选之间也在竞争，这个模式奖励"只有我能抓"的资产。
    """
    if not failures:
        return 0.0
    mine = catch_set(asset, index, ids) & failures
    if mode == "literal":
        return len(mine) / len(failures)
    if mode == "unique":
        others: set[str] = set()
        for c in candidates:
            if c != asset:
                others |= catch_set(c, index, ids)
        return len(mine - others) / len(failures)
    raise ValueError(f"未知 novel_mode={mode!r}（应为 'literal' / 'unique'）")


def score_components(asset: str, current: list[str], candidates: list[str], index: Index,
                     ids: list[str], *, wall_seconds: dict[str, float],
                     novel_mode: str = "literal") -> dict[str, float]:
    """单步打分的 4 个分量（全部只用派生集信息）。"""
    failures = failure_set(current, index, ids)
    n_f = len(failures)
    mine = catch_set(asset, index, ids) & failures
    fc = len(mine) / n_f if n_f else 0.0
    nc = novel_coverage(asset, failures, current, candidates, index, ids, mode=novel_mode)
    max_wall = max(wall_seconds[c] for c in candidates) if candidates else 1.0
    cost_n = wall_seconds[asset] / max_wall if max_wall > 0 else 0.0
    if current:
        red = sum(jaccard(catch_set(asset, index, ids), catch_set(c, index, ids))
                  for c in current) / len(current)
    else:
        red = 0.0
    return {"failure_coverage": fc, "novel_coverage": nc,
            "cost_norm": cost_n, "redundancy": red, "n_failures": float(n_f)}


def select_portfolio(candidates: list[str], k: int, index: Index, ids: list[str], *,
                     wall_seconds: dict[str, float],
                     weights: dict[str, float] | None = None,
                     novel_mode: str = "literal") -> dict[str, Any]:
    """迭代式 E：从空集出发，每步 argmax score，直到选满 k 个（或候选耗尽）。

    确定性：同分按资产 id 升序（浮点分先 round(12) 消噪声）。
    返回 selection + 逐步 trace（每步的 F_t 大小与入选资产的 4 分量），可审计。
    """
    w = dict(weights or DEFAULT_WEIGHTS)
    for key in ("w_failure", "w_novel", "w_cost", "w_redundancy"):
        if key not in w:
            raise ValueError(f"weights 缺 {key}")
    cands = sorted(set(candidates))
    for c in cands:
        if c not in wall_seconds:
            raise KeyError(f"wall_seconds 缺候选 {c!r}（成本分量需要每个候选的实测墙钟）")
    current: list[str] = []
    trace: list[dict[str, Any]] = []
    while len(current) < min(k, len(cands)):
        remaining = [c for c in cands if c not in current]
        best: str | None = None
        best_score = -float("inf")
        best_comp: dict[str, float] = {}
        for a in remaining:  # remaining 已按 id 升序 ⇒ 同分保留 id 最小者
            comp = score_components(a, current, remaining, index, ids,
                                    wall_seconds=wall_seconds, novel_mode=novel_mode)
            score = (w["w_failure"] * comp["failure_coverage"] + w["w_novel"] * comp["novel_coverage"]
                     - w["w_cost"] * comp["cost_norm"] - w["w_redundancy"] * comp["redundancy"])
            if round(score, 12) > round(best_score, 12):
                best, best_score, best_comp = a, score, comp
        if best is None:  # 理论不可达（remaining 非空），防御
            break
        current.append(best)
        trace.append({"step": len(current), "picked": best, "score": round(best_score, 6),
                      "n_failures_before": int(best_comp["n_failures"]),
                      "failure_coverage": round(best_comp["failure_coverage"], 6),
                      "novel_coverage": round(best_comp["novel_coverage"], 6),
                      "cost_norm": round(best_comp["cost_norm"], 6),
                      "redundancy": round(best_comp["redundancy"], 6)})
    return {"selection": list(current), "trace": trace, "weights": w, "novel_mode": novel_mode}


# ─────────────────────────────────────────────────────────────────────────────
# 自检（合成数据，不碰仓库数据）
# ─────────────────────────────────────────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    # 合成矩阵：3 样本 × 3 资产
    #   a1 抓 {s1, s2}；a2 抓 {s2, s3}；a3 抓 {s1}（a3 ⊂ a1 ⇒ 高冗余、低 unique-novelty）
    index: Index = {
        "s1": {"a1": "catch", "a2": "miss", "a3": "catch"},
        "s2": {"a1": "catch", "a2": "catch", "a3": "miss"},
        "s3": {"a1": "miss", "a2": "catch", "a3": "miss"},
    }
    ids = ["s1", "s2", "s3"]
    cands = ["a1", "a2", "a3"]
    wall = {"a1": 100.0, "a2": 100.0, "a3": 10.0}

    # literal 模式：novel ≡ failure（规格坍缩的数学证明）
    f = failure_set([], index, ids)
    for a in cands:
        comp = score_components(a, [], cands, index, ids, wall_seconds=wall, novel_mode="literal")
        chk(f"literal: novel≡failure ({a})", comp["novel_coverage"] == comp["failure_coverage"])
    chk("F_0 = 全集", f == {"s1", "s2", "s3"})

    # unique 模式：a3 的残余覆盖 {s1} 都被 a1 覆盖 ⇒ unique-novelty = 0
    comp3u = score_components("a3", [], cands, index, ids, wall_seconds=wall, novel_mode="unique")
    chk("unique: a3 不可替代覆盖 = 0", comp3u["novel_coverage"] == 0.0, f"({comp3u})")
    # a1 抓 {s1,s2} 但 a3 抓 s1、a2 抓 s2 ⇒ a1 也无独占；a2 抓 {s2,s3}，s3 无他选 ⇒ 1/3
    comp1u = score_components("a1", [], cands, index, ids, wall_seconds=wall, novel_mode="unique")
    comp2u = score_components("a2", [], cands, index, ids, wall_seconds=wall, novel_mode="unique")
    chk("unique: a1 无独占残余", comp1u["novel_coverage"] == 0.0, f"({comp1u['novel_coverage']:.4f})")
    chk("unique: a2 独占 s3 = 1/3", abs(comp2u["novel_coverage"] - 1 / 3) < 1e-12,
        f"({comp2u['novel_coverage']:.4f})")

    # fd_only 权重 = 残余覆盖贪心：第一步应选抓得最多的 a1（同 2 个的 a2 靠 id 排序输了并列？不——
    # a1 抓 2、a2 抓 2 ⇒ 同分，id 升序 ⇒ a1 先）。
    r = select_portfolio(cands, 2, index, ids, wall_seconds=wall,
                         weights={"w_failure": 1.0, "w_novel": 0.0, "w_cost": 0.0,
                                  "w_redundancy": 0.0})
    chk("fd_only 第一步 = a1（同分 id 升序）", r["selection"][0] == "a1", f"({r['selection']})")
    # 第二步：F_1 = {s3}，只有 a2 抓 s3 ⇒ a2
    chk("fd_only 第二步 = a2（残余覆盖）", r["selection"][1] == "a2", f"({r['selection']})")

    # 确定性 + 权重缺字段 fail-loud
    r2 = select_portfolio(cands, 2, index, ids, wall_seconds=wall,
                          weights={"w_failure": 1.0, "w_novel": 0.0, "w_cost": 0.0,
                                   "w_redundancy": 0.0})
    chk("确定性", r["selection"] == r2["selection"])
    try:
        select_portfolio(cands, 1, index, ids, wall_seconds=wall, weights={"w_failure": 1.0})
        chk("缺权重字段 ⇒ ValueError", False)
    except ValueError:
        chk("缺权重字段 ⇒ ValueError", True)
    try:
        select_portfolio(cands, 1, index, ids, wall_seconds={"a1": 1.0}, weights=None)
        chk("缺墙钟 ⇒ KeyError", False)
    except KeyError:
        chk("缺墙钟 ⇒ KeyError", True)

    # cost 分量把选择推向便宜的资产：全覆盖信号相同（a3 对残余 F 无覆盖）时，
    # w_cost>0 会让 a3（便宜）排在 a2（贵）前面——构造 F_1={s1} 场景验证。
    r3 = select_portfolio(["a1", "a3"], 2, index, ids, wall_seconds=wall,
                          weights={"w_failure": 0.0, "w_novel": 0.0, "w_cost": 1.0,
                                   "w_redundancy": 0.0})
    chk("cost 主导 ⇒ 先选便宜的 a3", r3["selection"][0] == "a3", f"({r3['selection']})")

    # 消融配置齐全
    chk("消融配置 = 5 个", len(ABLATION_CONFIGS) == 5, f"({sorted(ABLATION_CONFIGS)})")

    print(f"evolution_operator_677c selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="677c C：evolution operator 算法化定义")
    ap.add_argument("--check", action="store_true", help="自检（合成数据，只读）")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    ap.print_help()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
