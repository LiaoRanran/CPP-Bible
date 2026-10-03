#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""run_a5_experiment_673p.py — 673p D：A5（random-budget）实验运行器（拆仓第三 + 四层）。

它把前三层接起来：
    资产池（verifier_pool_673p） → 选择策略（selection_strategies_673p）
        → **运行层**（本文件 ReplayExecutor） → **评估层**（本文件 arm_stats / 配对检验）

⚠ 运行层是 **replay**，不是重跑（必须说清楚）
==============================================
本仓的逐样本明细（`data/holdout/reveal_5_detail_672h.json` /
`data/external_corpus/reveal_detail_672h.json`）每条记录的是：

    {id, detector, verdict, …}   —— 该样本**被哪个资产判成什么**

由此定义一个**单归属（single-attribution）**重放模型：

    给定选中资产集 S，样本 s 的重放判决 =
        unknown / not_error        （原样保留，S 无关）
        catch                      若 s 原判 catch **且** detector(s) ∈ S
        miss                       其余

**这个模型是一条假设**，不是事实：一条样本可能**同时**被多个资产抓到，而明细只记了
"被抓到时归属的那一个"。因此重放值**低估**大资产集的检出、**高估**小资产集的检出
（被截掉的资产本来可能也抓得到）。该假设的后果与缓解见产物 `honest_notes`。

**为什么不真跑**：真跑需要 WSL g++ + sanitizer + 双档 × 3 回合，单轮小时级；
本批的目标是**建立 A5 的基础设施**（可运行的拆仓 + 预注册），不是产出新的实测判决。
真跑留给后续批次（本文件已把运行层做成可替换的 `Executor` 协议）。

673r：**真跑已经做了**
======================
673r 新增 `tools/detect_for_assets.py`：对每条样本、每个资产**各调一次**
`tools/holdout_reveal_661.py::detect`，得到 N × 8 的真实判定矩阵
（`data/experiments/asset_attribution_673r.json`）。本文件因此新增第二个
Executor —— `AttributionExecutor`：

    给定选中资产集 S，样本 s 的判定 = S 中各资产真实判定的 **OR**
    （任一 catch ⇒ catch；全部 unknown ⇒ unknown；其余 miss）

与 `ReplayExecutor` 的差别是**根本性的**：重放只认"明细里记的那一个 detector"，
真实矩阵承认"同一条样本可以被多个资产抓到"。673p 的 A5 阻塞条件 3
（"FD 无选择层、预算是事后记账"）在 replay 模型下无法解除，在真实矩阵下可以。

本文件同时保留 replay 段（`primary`）与真实段（`real_attribution`）：
前者与 673p 逐位同口径，供跨批对照；后者是本批的结论来源。

A5 的**核心诚实问题**（本文件必须回答）
======================================
A5 问：「**同等预算**下，failure-driven **选择** 是否优于 random **选择**？」
但现状 FD **不做选择**——它对每个样本跑**全池**。"FD 用到的资产"（4/5 个）是
**事后从 catch 反推**的记账量，不是选择量。于是：

* 若把 FD 的预算定义成"它实际用到的资产数"⇒ FD 用的是**评测集自身**的信息 ⇒ **oracle**；
* 若把 FD 的预算定义成"全池大小 8" ⇒ Random 抽 8 个 = 全池 ⇒ Δ 恒为 0。

**两条路都不是"选择策略 vs 选择策略"的干净对照。** 故本批如实登记：

    A5 阻塞条件 3：现有架构不支持干净分离（FD 无选择层；"FD 预算"是事后记账）。

为让 A5 仍有**可读的信息**，本文件额外跑一个**探索性**（非预注册、非确认性）对照：
用**派生集**（672h 扩样前的旧样本）估 `fail_hits`，在**评测集**（672h 新样本）上评估。
这条路上 FD 是**真预测器**（不含评测集信息），因而第一次给出"选择 vs 随机"的可比信号。

产物
====
`data/experiments/a5_673p.json`

用法
====
    python tools/run_a5_experiment_673p.py            # 跑 + 落盘
    python tools/run_a5_experiment_673p.py --json     # 机读（仍落盘）
    python tools/run_a5_experiment_673p.py --no-write # 只跑不写
    python tools/run_a5_experiment_673p.py --check    # 自检（不读仓库产物）
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import statistics
import sys
import time
from collections import Counter
from pathlib import Path
from typing import Any, Protocol

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

import selection_strategies_673p as ss  # noqa: E402
import verifier_pool_673p as vp  # noqa: E402

OUT = ROOT / "data" / "experiments" / "a5_673p.json"
H_DETAIL = ROOT / "data" / "holdout" / "reveal_5_detail_672h.json"
C_DETAIL = ROOT / "data" / "external_corpus" / "reveal_detail_672h.json"

SEED = 20260930                              # 项目约定种子（预注册 673p 钉死）
MULTI_SEED_N = 2000                          # Random 臂多次运行次数（预注册钉死）
NEW_SOURCE = "measured_672h"                 # 672h 扩样新样本的来源标记（派生集切分用）

# ── 673r：真实逐资产归属 ──────────────────────────────────────────────────────
ATTRIB = ROOT / "data" / "experiments" / "asset_attribution_673r.json"
PREREG_673R = "data/673r_a5_preregistration.json"
PRIMARY_K = 4                                # 预注册 673r 钉死的主预算
SWEEP_K = (1, 2, 3, 4, 5, 6, 7)             # 探索性预算扫描
DEGENERATE_K = 8                             # k=8 ⇒ 三臂恒等于全池（退化，只报不判）
Z95 = 1.959963984540054


# ─────────────────────────────────────────────────────────────────────────────
# 运行层：Executor 协议 + replay 实现
# ─────────────────────────────────────────────────────────────────────────────
class Executor(Protocol):
    """运行层接口。真跑（subprocess + WSL 工具链）与 replay 都实现它。"""

    name: str

    def verdict(self, sample: dict, selected: tuple[str, ...]) -> str:
        """给定样本与选中资产集，返回判决 catch / miss / unknown / not_error。"""
        ...


class ReplayExecutor:
    """**单归属重放**：用已落盘的 detector 归属复算"若只跑 S，这条样本会怎样"。

    假设见模块 docstring。`selected` 为 None ⇒ 视为全池（= 现状 FD 的行为）。
    """

    name = "replay_single_attribution"

    def verdict(self, sample: dict, selected: tuple[str, ...]) -> str:
        v = str(sample.get("verdict"))
        if v in ("unknown", "not_error"):
            return v
        if v == "catch":
            det = str(sample.get("detector"))
            return "catch" if det in set(selected) else "miss"
        return "miss"


# ─────────────────────────────────────────────────────────────────────────────
# 统计原语（本文件自持，避免与论文线统计库耦合；口径与 verify_expand_672h 一致）
# ─────────────────────────────────────────────────────────────────────────────
def mcnemar_exact_p(b: int, c: int) -> float:
    """精确 McNemar（双侧）：2 × P(Binom(b+c, 0.5) ≤ min(b,c))，用 lgamma 算组合数。"""
    n = b + c
    if n == 0:
        return 1.0
    m = min(b, c)

    def log_cnk(n_: int, k_: int) -> float:
        return math.lgamma(n_ + 1) - math.lgamma(k_ + 1) - math.lgamma(n_ - k_ + 1)

    tail = sum(math.exp(log_cnk(n, i) - n * math.log(2)) for i in range(0, m + 1))
    return min(1.0, 2.0 * tail)


def cohens_h(p1: float, p2: float) -> float:
    return 2 * math.asin(math.sqrt(p1)) - 2 * math.asin(math.sqrt(p2))


def cp_interval(k: int, n: int, conf: float = 0.95) -> tuple[float | None, float | None]:
    """Clopper–Pearson 95%（优先用仓库唯一实现 `tools/stat_bounds.py`）。"""
    if n <= 0:
        return None, None
    try:
        import stat_bounds

        return stat_bounds.cp_interval(k, n, conf)
    except Exception:  # noqa: BLE001  兜底：正态近似的 Wilson（只在本仓工具缺失时）
        if n == 0:
            return None, None
        z = 1.959963984540054
        p = k / n
        den = 1 + z * z / n
        cen = (p + z * z / (2 * n)) / den
        half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
        return max(0.0, cen - half), min(1.0, cen + half)


# ─────────────────────────────────────────────────────────────────────────────
# 装载 + 评估层
# ─────────────────────────────────────────────────────────────────────────────
def _jload(p: Path) -> dict:
    return dict(json.loads(p.read_text(encoding="utf-8")))


def measurable_rows(detail: Path, *, planted_only: bool) -> list[dict]:
    """可测口径 = catch+miss（unknown / not_error 不进分母）。holdout 另加 planted=true。"""
    rows = _jload(detail)["per_sample"]
    if planted_only:
        rows = [r for r in rows if r.get("planted") is True]
    return [r for r in rows if r.get("verdict") in ("catch", "miss")]


def arm_stats(rows: list[dict], selected: tuple[str, ...], ex: Executor) -> dict[str, Any]:
    """一个臂在给定样本上的检出率 + CP95。"""
    n = len(rows)
    k = sum(1 for r in rows if ex.verdict(r, selected) == "catch")
    lo, hi = cp_interval(k, n)
    return {"k": k, "n": n, "point": (k / n) if n else None,
            "rate_pct": round(k / n * 100, 4) if n else None,
            "cp95": [round(lo * 100, 4) if lo is not None else None,
                     round(hi * 100, 4) if hi is not None else None]}


def paired_fd_vs(other_rows: list[dict], fd_sel: tuple[str, ...], other_sel: tuple[str, ...],
                 ex: Executor) -> dict[str, Any]:
    """FD vs 另一臂的**配对**对照（同一批样本；b/c 为不一致对）。"""
    n = len(other_rows)
    b = c = 0
    for r in other_rows:
        f = ex.verdict(r, fd_sel) == "catch"
        o = ex.verdict(r, other_sel) == "catch"
        if f and not o:
            b += 1
        elif o and not f:
            c += 1
    k_fd = sum(1 for r in other_rows if ex.verdict(r, fd_sel) == "catch")
    k_ot = sum(1 for r in other_rows if ex.verdict(r, other_sel) == "catch")
    p1, p2 = (k_fd / n if n else 0.0), (k_ot / n if n else 0.0)
    return {"n_pairs": n, "fd_catch": k_fd, "other_catch": k_ot,
            "discordant_fd_only": b, "discordant_other_only": c,
            "delta_pp": round((p1 - p2) * 100, 4),
            "mcnemar_p": mcnemar_exact_p(b, c),
            "cohens_h": round(abs(cohens_h(p1, p2)), 4) if n else None}


def fail_hits_of(rows: list[dict], pool: tuple[vp.AssetSpec, ...]) -> dict[str, int]:
    """按资产统计历史失败命中数（= 该资产被判 catch 的样本数）。"""
    cnt = Counter(str(r.get("detector")) for r in rows if r.get("verdict") == "catch")
    return {a: int(cnt.get(a, 0)) for a in vp.selectable_ids(pool)}


def _budget_anchor(rows: list[dict], pool: tuple[vp.AssetSpec, ...]) -> list[str]:
    """FD 预算锚 = FD 在 **catch** 样本上实际用到的资产（事后记账，见 A5 阻塞登记）。

    只数 catch：miss 样本的 detector 是"被谁判成没抓到"，不是产出判决的资产
    （与 672g `select_assets_671b.budget()` 同义）。
    """
    return ss.fd_budget_anchor(
        [str(r.get("detector")) for r in rows if r.get("verdict") == "catch"], pool)


def _sel_cost(sel: ss.Selection) -> int:
    return sel.cost_units


def _static_budget(pool: tuple[vp.AssetSpec, ...], k_budget: int) -> int:
    """Static 臂预算 = min(FD 预算, 池中静态资产数)。

    Static 臂**不得**用运行时资产补齐（否则口径就不是 Static 臂）；池里只有 4 个静态资产，
    当 FD 预算 k=5（corpus）时 Static 只能跑 4 个 ⇒ 这里显式降级并如实标注，不静默。
    """
    return min(k_budget, len([a for a in vp.selectable_ids(pool) if a in vp.STATIC_ASSETS]))


# ─────────────────────────────────────────────────────────────────────────────
# 673r：真实逐资产归属层（AttributionExecutor + 派生集真选择 + 预算扫描）
# ─────────────────────────────────────────────────────────────────────────────
class AttributionExecutor:
    """**真实逐资产 OR**：判定矩阵来自 `detect_for_assets` 的实测，不是重放。

    `selected` 中任一资产真实 catch ⇒ catch；全部 unknown ⇒ unknown；其余 miss。
    样本不在矩阵里 ⇒ **KeyError（fail-loud）**，绝不静默记 miss。
    """

    name = "real_per_asset_or"

    def __init__(self, index: dict[str, dict[str, str]]):
        self.index = index

    def verdict(self, sample: dict, selected: tuple[str, ...]) -> str:
        sid = str(sample.get("id"))
        if sid not in self.index:
            raise KeyError(f"样本 {sid!r} 不在真实归属矩阵中（fail-loud，不得静默记 miss）")
        row = self.index[sid]
        vs = [row.get(a) for a in selected]
        vs = [v for v in vs if v is not None]
        if not vs:
            return "unknown"
        if any(v == "catch" for v in vs):
            return "catch"
        if all(v == "unknown" for v in vs):
            return "unknown"
        return "miss"


def load_attribution(path: Path = ATTRIB) -> dict[str, Any] | None:
    """读真实归属矩阵；不存在 ⇒ None（本段整体 skip，不伪造）。"""
    if not path.is_file():
        return None
    return dict(json.loads(path.read_text(encoding="utf-8")))


def attribution_index(doc: dict[str, Any], dataset: str) -> dict[str, dict[str, str]]:
    """dataset → {sample_id: {asset_id: verdict}}。"""
    out: dict[str, dict[str, str]] = {}
    for r in doc["datasets"][dataset]["samples"]:
        out[str(r["id"])] = {a: str(v.get("verdict")) for a, v in r["per_asset"].items()}
    return out


def rows_with_attribution(detail: Path, *, planted_only: bool,
                          index: dict[str, dict[str, str]]) -> tuple[list[dict], list[str]]:
    """可测样本 ∩ 有真实归属的样本；返回 (rows, 缺失 id)。"""
    rows = measurable_rows(detail, planted_only=planted_only)
    have: list[dict] = []
    missing: list[str] = []
    for r in rows:
        sid = str(r.get("id"))
        if sid in index:
            have.append(r)
        else:
            missing.append(sid)
    return have, missing


def fail_hits_real(rows: list[dict], assets: list[str],
                   index: dict[str, dict[str, str]]) -> dict[str, int]:
    """资产在 rows 上**真实**抓到的条数（真实矩阵 ⇒ 一条样本可同时计给多个资产）。"""
    cnt = {a: 0 for a in assets}
    for r in rows:
        row = index.get(str(r.get("id")), {})
        for a in assets:
            if row.get(a) == "catch":
                cnt[a] += 1
    return cnt


def degenerate_assets(rows: list[dict], assets: list[str],
                      index: dict[str, dict[str, str]]) -> dict[str, dict[str, Any]]:
    """预注册 673r 的退化判定：在 rows 上 catch 率 == 100% 或 == 0% ⇒ degenerate_constant。"""
    n = len(rows)
    out: dict[str, dict[str, Any]] = {}
    for a in assets:
        k = sum(1 for r in rows if index.get(str(r.get("id")), {}).get(a) == "catch")
        unk = sum(1 for r in rows if index.get(str(r.get("id")), {}).get(a) == "unknown")
        rate = (k / n) if n else None
        if n and (k == n or k == 0):
            out[a] = {"catch": k, "unknown": unk, "n": n,
                      "catch_rate_pct": round(rate * 100, 4) if rate is not None else None,
                      "flag": "degenerate_constant",
                      "why": ("抓到每一条 ⇒ 常量 catch" if k == n else "一条都没抓到 ⇒ 零信息")}
    return out


def paired_test(rows: list[dict], sel_a: tuple[str, ...], sel_b: tuple[str, ...], ex: Executor,
                *, label_a: str = "fd", label_b: str = "other") -> dict[str, Any]:
    """配对对照：Δ(pp) + **95% CI** + exact McNemar p + Cohen's h。

    Δ 的 CI 用**不一致对**的标准误（McNemar 口径）：
        SE = sqrt(b + c − (b−c)²/n) / n
    """
    n = len(rows)
    b = c = 0
    ka = kb = 0
    for r in rows:
        a = ex.verdict(r, sel_a) == "catch"
        o = ex.verdict(r, sel_b) == "catch"
        ka += int(a)
        kb += int(o)
        if a and not o:
            b += 1
        elif o and not a:
            c += 1
    p1, p2 = (ka / n if n else 0.0), (kb / n if n else 0.0)
    delta = (p1 - p2) * 100
    if n:
        se = math.sqrt(max(0.0, b + c - (b - c) ** 2 / n)) / n
        lo, hi = delta - Z95 * se * 100, delta + Z95 * se * 100
    else:
        se, lo, hi = 0.0, None, None
    return {"n_pairs": n, f"{label_a}_catch": ka, f"{label_b}_catch": kb,
            "discordant_a_only": b, "discordant_b_only": c,
            "delta_pp": round(delta, 4),
            "delta_ci95_pp": [round(lo, 4) if lo is not None else None,
                              round(hi, 4) if hi is not None else None],
            "delta_se_pp": round(se * 100, 4),
            "mcnemar_p": mcnemar_exact_p(b, c),
            "cohens_h": round(abs(cohens_h(p1, p2)), 4) if n else None,
            "ci_crosses_zero": (lo is not None and hi is not None and lo < 0 < hi)}


def _arm_block(sel: ss.Selection, rows: list[dict], ex: Executor, pool: tuple[vp.AssetSpec, ...],
               *, extra: dict[str, Any] | None = None) -> dict[str, Any]:
    return {"assets": list(sel.assets), "budget_k": len(sel.assets),
            "cost_units": sel.cost_units,
            "allocation_table": [dict(r) for r in sel.allocation_table],
            **arm_stats(rows, sel.assets, ex), **(extra or {})}


def real_budget_comparison(rows: list[dict], ex: AttributionExecutor,
                           index: dict[str, dict[str, str]], pool: tuple[vp.AssetSpec, ...],
                           *, candidates: list[str], k: int, seed: int = SEED,
                           multi_seed_n: int = MULTI_SEED_N,
                           fail_hits: dict[str, int] | None = None,
                           eval_rows: list[dict] | None = None) -> dict[str, Any]:
    """同预算 k 的三臂对照。**FD 的 fail_hits 只来自派生集** ⇒ FD 是真预测器。

    参数
    ----
    rows        : 全部可测样本（用于 full-pool 对照臂）。
    eval_rows   : 评估集（FD/Random/Static 三臂在它上面比）。None ⇒ 用 rows。
    fail_hits   : 派生集上估的 fail_hits（**必须**来自评估集之外）。
    """
    ev = eval_rows if eval_rows is not None else rows
    fh = fail_hits if fail_hits is not None else fail_hits_real(ev, candidates, index)
    k_eff = min(k, len(candidates))

    fd_sel = ss.select("failure_driven", pool, max_assets=k_eff, fail_hits=fh,
                       candidates=candidates)
    rnd_sel = ss.select("random", pool, max_assets=k_eff, seed=seed, candidates=candidates)
    n_static = len([a for a in candidates if a in vp.STATIC_ASSETS])
    st_sel = ss.select("static", pool, max_assets=min(k_eff, n_static), candidates=candidates)
    full_sel = ss.select("failure_driven", pool, max_assets=len(candidates), fail_hits=fh,
                         candidates=candidates)

    fd_catch = sum(1 for r in ev if ex.verdict(r, fd_sel.assets) == "catch")
    rates: list[float] = []
    for i in range(multi_seed_n):
        s = ss.select("random", pool, max_assets=k_eff, seed=seed + i, candidates=candidates)
        rates.append(sum(1 for r in ev if ex.verdict(r, s.assets) == "catch") / len(ev))
    rs = sorted(rates)

    return {
        "budget_k": k_eff,
        "is_primary_k": k_eff == PRIMARY_K,
        "is_degenerate_k": k_eff >= len(candidates),
        "candidates": list(candidates),
        "eval_n": len(ev),
        "arms": {
            "fd": _arm_block(fd_sel, ev, ex, pool, extra={"fail_hits_rank": fh}),
            "random": _arm_block(rnd_sel, ev, ex, pool, extra={"seed": seed}),
            "static": _arm_block(st_sel, ev, ex, pool),
            "fd_full_pool": _arm_block(full_sel, ev, ex, pool),
        },
        "paired_tests": {
            "fd_vs_random": paired_test(ev, fd_sel.assets, rnd_sel.assets, ex,
                                       label_a="fd", label_b="random"),
            "fd_vs_static": paired_test(ev, fd_sel.assets, st_sel.assets, ex,
                                       label_a="fd", label_b="static"),
        },
        "random_multi_seed": {
            "runs": multi_seed_n,
            "mean_rate_pct": round(statistics.fmean(rates) * 100, 4),
            "sd_pp": round(statistics.pstdev(rates) * 100, 4),
            "min_rate_pct": round(min(rates) * 100, 4),
            "max_rate_pct": round(max(rates) * 100, 4),
            "percentile_2.5_pct": round(rs[int(0.025 * (multi_seed_n - 1))] * 100, 4),
            "percentile_97.5_pct": round(rs[int(0.975 * (multi_seed_n - 1))] * 100, 4),
            # FD 在随机分布中的位置：多少次抽样里 FD 严格更好 / 更好或持平 / 更差
            "fd_strictly_better_frac": round(sum(1 for x in rates if x * len(ev) < fd_catch)
                                             / multi_seed_n, 4),
            "fd_better_or_tie_frac": round(sum(1 for x in rates if x * len(ev) <= fd_catch)
                                           / multi_seed_n, 4),
            "random_strictly_better_frac": round(sum(1 for x in rates if x * len(ev) > fd_catch)
                                                 / multi_seed_n, 4),
            "fd_catch": fd_catch,
            "note": "单点 seed 只用于配对检验；分布才说明 Random 臂的期望位置。",
        },
    }


def real_dataset_section(dataset: str, doc: dict[str, Any], pool: tuple[vp.AssetSpec, ...],
                         multi_seed_n: int = MULTI_SEED_N) -> dict[str, Any]:
    """一个数据集的完整真实分析：派生集切分 + 退化诊断 + 预算扫描 + 并列分析。"""
    detail = H_DETAIL if dataset == "holdout" else C_DETAIL
    planted_only = dataset == "holdout"
    index = attribution_index(doc, dataset)
    rows, missing = rows_with_attribution(detail, planted_only=planted_only, index=index)
    ex = AttributionExecutor(index)

    assets = [a for a in vp.selectable_ids(pool) if a in set(doc["datasets"][dataset]["asset_ids"])]
    deriv = [r for r in rows if r.get("source") != NEW_SOURCE]
    evalset = [r for r in rows if r.get("source") == NEW_SOURCE]

    fh_deriv = fail_hits_real(deriv, assets, index)
    degen = degenerate_assets(deriv, assets, index)

    def scan(cands: list[str]) -> list[dict[str, Any]]:
        """k=1..8 扫描。预算被候选数钳制时同一个有效 k 会出现多次 ⇒ 折叠成一行并登记。"""
        out: list[dict[str, Any]] = []
        by_k: dict[int, dict[str, Any]] = {}
        for k in (*SWEEP_K, DEGENERATE_K):
            row = real_budget_comparison(rows, ex, index, pool, candidates=cands, k=k,
                                         multi_seed_n=multi_seed_n,
                                         fail_hits={a: fh_deriv.get(a, 0) for a in cands},
                                         eval_rows=evalset)
            if row["budget_k"] in by_k:
                by_k[row["budget_k"]]["k_requested"].append(k)
                continue
            row["k_requested"] = [k]
            by_k[row["budget_k"]] = row
            out.append(row)
        return out

    co_cands = [a for a in assets if a not in degen]
    # 事后敏感性视角：只剔除**恒 catch**（100%）资产，保留派生集上 0 命中的资产。
    const_catch = [a for a, v in degen.items() if v.get("catch_rate_pct") == 100.0]
    sens_cands = [a for a in assets if a not in const_catch]
    # 全集（含评估集）对照：fail_hits 用**全集** ⇒ oracle，明确标为不可用于确认性结论
    fullset = real_budget_comparison(rows, ex, index, pool, candidates=assets, k=PRIMARY_K,
                                     multi_seed_n=multi_seed_n,
                                     fail_hits=fail_hits_real(rows, assets, index))
    fullset["oracle_note"] = ("fail_hits 与评估集来自同一批样本 ⇒ FD 在此是 oracle，"
                              "**不得**用于 H0/H1 判定；仅为与 673p 同口径的连续性对照。")

    return {
        "dataset": dataset,
        "n_measurable_with_attribution": len(rows),
        "missing_attribution_ids": missing,
        "derivation": {"n": len(deriv), "rule": "source != measured_672h",
                       "fail_hits": {a: v for a, v in fh_deriv.items() if v},
                       "fail_hits_all": fh_deriv},
        "evaluation": {"n": len(evalset), "rule": "source == measured_672h"},
        "asset_diagnostics": {
            "assets": assets,
            "degenerate_on_derivation": degen,
            "per_asset_on_measurable": {
                a: {"catch": sum(1 for r in rows if index.get(str(r["id"]), {}).get(a) == "catch"),
                    "miss": sum(1 for r in rows if index.get(str(r["id"]), {}).get(a) == "miss"),
                    "unknown": sum(1 for r in rows if index.get(str(r["id"]), {}).get(a) == "unknown")}
                for a in assets},
        },
        "primary": {"candidates": assets, "note": "预注册主分析：全 8 项资产池，不剔除。",
                    "by_k": scan(assets)},
        "co_primary_excluding_degenerate": {
            "candidates": co_cands,
            "note": "并列分析：剔除在派生集上 catch 率 100%/0% 的常量资产（预注册预指定）。",
            "by_k": scan(co_cands)} if len(co_cands) < len(assets) else
            {"status": "skip", "why": "没有资产被标记为退化"},
        "sensitivity_exploratory": {
            "candidates": sens_cands,
            "note": "**事后增设**的敏感性视角：只剔除恒 catch（100%）资产，保留派生集上 0 命中的资产。"
                    "**不参与**通过/不通过判定，只用来看预注册『0% 也算子退化』这条规则有多保守。",
            "by_k": scan(sens_cands)} if len(sens_cands) < len(assets) else
            {"status": "skip", "why": "没有恒 catch 资产"},
        "fullset_exploratory": fullset,
    }


def real_attribution_section(pool: tuple[vp.AssetSpec, ...],
                             multi_seed_n: int = MULTI_SEED_N) -> dict[str, Any]:
    doc = load_attribution()
    if doc is None:
        return {"status": "skip", "why": f"缺少真实归属矩阵 {ATTRIB.relative_to(ROOT).as_posix()}"
                                         f"（先跑 `python tools/detect_for_assets.py --dataset both`）"}
    return {
        "status": "ok",
        "prereg": PREREG_673R,
        "generated_by": "tools/detect_for_assets.py + tools/run_a5_experiment_673p.py",
        "execution_model": {
            "name": "real_per_asset_or",
            "is_real_execution": True,
            "owner": "tools/detect_for_assets.py（复用 661.detect，未改动）",
            "aggregation": "OR：任一资产真实 catch ⇒ catch；全部 unknown ⇒ unknown；其余 miss",
            "rounds": 1,
            "rounds_note": "672h 冻结记录为 3 回合口径；本批 1 回合 ⇒ 与 82.9%/62.5% 不同口径，不得相减。",
        },
        "primary_k": PRIMARY_K,
        "sweep_k": list(SWEEP_K),
        "degenerate_k": DEGENERATE_K,
        "seed": SEED,
        "attribution_source": ATTRIB.relative_to(ROOT).as_posix(),
        "datasets": {d: real_dataset_section(d, doc, pool, multi_seed_n=multi_seed_n)
                     for d in ("holdout", "corpus") if d in doc["datasets"]},
        "honest_notes": [
            "FD 的 fail_hits **只**来自派生集（672h 扩样前的旧样本），评估只在扩样新样本上做 ⇒ FD 是真预测器，不是 oracle。",
            "Random 臂报 %d 次重采样分布；单点 seed=%d 只用于配对检验。" % (multi_seed_n, SEED),
            "k=8 时三臂选中集合恒等于全池 ⇒ Δ 恒 0、p 恒 1（退化），只报不作证据。",
            "Δ 的 95% CI 用不一致对标准误（McNemar 口径）；各臂检出率区间用 Clopper–Pearson 95%。",
        ],
    }


# ─────────────────────────────────────────────────────────────────────────────
# 主实验
# ─────────────────────────────────────────────────────────────────────────────
def run_dataset(label: str, rows: list[dict], ex: Executor, pool: tuple[vp.AssetSpec, ...],
                *, multi_seed_n: int = MULTI_SEED_N) -> dict[str, Any]:
    """在一个数据集上跑三臂 + 多次随机 + 配对检验。"""
    anchor = _budget_anchor(rows, pool)
    k_budget = len(anchor)
    fh_full = fail_hits_of(rows, pool)          # ⚠ 用评测集自身 ⇒ oracle，仅用于预算锚

    fd_full = tuple(vp.selectable_ids(pool))    # 现状 FD：跑全池
    fd_sel = ss.select("failure_driven", pool, max_assets=k_budget, fail_hits=fh_full)
    rnd_sel = ss.select("random", pool, max_assets=k_budget, seed=SEED)
    st_sel = ss.select("static", pool, max_assets=_static_budget(pool, k_budget))

    t0 = time.perf_counter()
    arms = {
        "fd_full_pool": {"assets": list(fd_full), "budget_k": len(fd_full),
                         "cost_units": vp.total_cost(fd_full, pool),
                         **arm_stats(rows, fd_full, ex)},
        "fd_budget_matched": {"assets": list(fd_sel.assets), "budget_k": k_budget,
                              "cost_units": _sel_cost(fd_sel),
                              "allocation_table": [dict(r) for r in fd_sel.allocation_table],
                              **arm_stats(rows, fd_sel.assets, ex)},
        "random": {"assets": list(rnd_sel.assets), "budget_k": k_budget,
                   "cost_units": _sel_cost(rnd_sel), "seed": SEED,
                   "allocation_table": [dict(r) for r in rnd_sel.allocation_table],
                   **arm_stats(rows, rnd_sel.assets, ex)},
        "static": {"assets": list(st_sel.assets), "budget_k": len(st_sel.assets),
                   "cost_units": _sel_cost(st_sel),
                   "allocation_table": [dict(r) for r in st_sel.allocation_table],
                   **arm_stats(rows, st_sel.assets, ex)},
    }
    replay_wall = time.perf_counter() - t0

    # Random 臂多次运行（同预算；随机性 ⇒ 报分布而非单点）
    rates: list[float] = []
    for i in range(multi_seed_n):
        s = ss.select("random", pool, max_assets=k_budget, seed=SEED + i)
        rates.append(sum(1 for r in rows if ex.verdict(r, s.assets) == "catch") / len(rows))
    rates_sorted = sorted(rates)
    lo_q = rates_sorted[int(0.025 * (multi_seed_n - 1))]
    hi_q = rates_sorted[int(0.975 * (multi_seed_n - 1))]
    random_multi = {
        "runs": multi_seed_n,
        "mean_rate_pct": round(statistics.fmean(rates) * 100, 4),
        "sd_pp": round(statistics.pstdev(rates) * 100, 4),
        "min_rate_pct": round(min(rates) * 100, 4),
        "max_rate_pct": round(max(rates) * 100, 4),
        "percentile_2.5_pct": round(lo_q * 100, 4),
        "percentile_97.5_pct": round(hi_q * 100, 4),
        "note": "同预算随机子集的检出率**分布**（非单点）；单点 seed=20260930 用于配对检验。",
    }

    return {
        "n_measurable": len(rows),
        "budget": {
            "k_assets": k_budget,
            "anchor": anchor,
            "anchor_note": "FD 在 catch 上实际用到的资产（**事后记账**，非选择）；"
                           "Random/Static 必须与它同预算。",
            "cost_units_fd_full": vp.total_cost(fd_full, pool),
            "cost_units_matched": _sel_cost(rnd_sel),
        },
        "arms": arms,
        "paired_tests": {
            "fd_vs_random": paired_fd_vs(rows, fd_full, rnd_sel.assets, ex),
            "fd_vs_static": paired_fd_vs(rows, fd_full, st_sel.assets, ex),
        },
        "random_multi_seed": random_multi,
        "replay_wall_seconds": round(replay_wall, 6),
        "fail_hits_used": {a: v for a, v in fh_full.items() if v},
    }


def exploratory_derivation_split(label: str, rows: list[dict], ex: Executor,
                                 pool: tuple[vp.AssetSpec, ...],
                                 *, multi_seed_n: int = MULTI_SEED_N) -> dict[str, Any]:
    """**探索性**：派生集（旧样本）估 fail_hits → 评测集（新样本）评估。

    这是本批**唯一**让 FD 成为"真预测器"（不含评测集信息）的对照。
    非预注册、非确认性 ⇒ 只报方向 + CI，不得写成确认性结论。
    """
    deriv = [r for r in rows if r.get("source") != NEW_SOURCE]
    evalset = [r for r in rows if r.get("source") == NEW_SOURCE]
    if not deriv or not evalset:
        return {"status": "skip", "why": f"派生集 {len(deriv)} / 评测集 {len(evalset)} 有空集"}

    fh_deriv = fail_hits_of(deriv, pool)
    k = len([a for a, v in fh_deriv.items() if v > 0])
    fd_sel = ss.select("failure_driven", pool, max_assets=k, fail_hits=fh_deriv)
    rnd_sel = ss.select("random", pool, max_assets=k, seed=SEED)
    st_sel = ss.select("static", pool, max_assets=_static_budget(pool, k))

    rates: list[float] = []
    for i in range(multi_seed_n):
        s = ss.select("random", pool, max_assets=k, seed=SEED + i)
        rates.append(sum(1 for r in evalset if ex.verdict(r, s.assets) == "catch") / len(evalset))
    rates_sorted = sorted(rates)

    return {
        "status": "exploratory",
        "derivation": {"n": len(deriv), "source": "672h 扩样前旧样本（source != measured_672h）",
                       "fail_hits": {a: v for a, v in fh_deriv.items() if v}},
        "evaluation": {"n": len(evalset), "source": "672h 扩样新样本（source == measured_672h）"},
        "budget_k": k,
        "arms": {
            "fd_derived": {"assets": list(fd_sel.assets), **arm_stats(evalset, fd_sel.assets, ex)},
            "random": {"assets": list(rnd_sel.assets), "seed": SEED,
                       **arm_stats(evalset, rnd_sel.assets, ex)},
            "static": {"assets": list(st_sel.assets), **arm_stats(evalset, st_sel.assets, ex)},
        },
        "paired_tests": {
            "fd_vs_random": paired_fd_vs(evalset, fd_sel.assets, rnd_sel.assets, ex),
            "fd_vs_static": paired_fd_vs(evalset, fd_sel.assets, st_sel.assets, ex),
        },
        "random_multi_seed": {
            "runs": multi_seed_n,
            "mean_rate_pct": round(statistics.fmean(rates) * 100, 4),
            "sd_pp": round(statistics.pstdev(rates) * 100, 4),
            "percentile_2.5_pct": round(rates_sorted[int(0.025 * (multi_seed_n - 1))] * 100, 4),
            "percentile_97.5_pct": round(rates_sorted[int(0.975 * (multi_seed_n - 1))] * 100, 4),
        },
        "honest_note": "派生集与评测集是**时间切分**（旧→新），但两者出自同一批夹具政策 ⇒ "
                       "分布漂移已由 672h H4 登记（corpus 新子集检出率显著更高）。"
                       "本条为探索性，不进确认性结论。",
    }


def _payload(ex: Executor, pool: tuple[vp.AssetSpec, ...],
             multi_seed_n: int = MULTI_SEED_N) -> dict[str, Any]:
    h_rows = measurable_rows(H_DETAIL, planted_only=True)
    c_rows = measurable_rows(C_DETAIL, planted_only=False)
    return {
        "schema": "queyi-a5-experiment/673p",
        "version": "1.0",
        "generated_by": "tools/run_a5_experiment_673p.py",
        "prereg": "data/673p_a5_preregistration.json",
        "seed": SEED,
        "multi_seed_runs": multi_seed_n,
        "asset_pool_owner": "tools/verifier_pool_673p.py::ASSET_POOL",
        "selection_owner": "tools/selection_strategies_673p.py::select",
        "execution_model": {
            "name": ex.name,
            "is_real_execution": False,
            "assumption": "单归属：一条样本的 catch 只归属到明细里记的 detector；"
                          "其它资产的判决未知，一律记 miss。",
            "direction_of_bias": "对大资产集**低估**检出、对小资产集**高估**检出。",
            "why_not_real": "真跑需 WSL g++ + sanitizer 双档 × 3 回合（小时级）；本批只建基础设施。",
        },
        "sources": {
            "holdout": "data/holdout/reveal_5_detail_672h.json（planted=true，可测 41）",
            "corpus": "data/external_corpus/reveal_detail_672h.json（可测 64）",
        },
        "primary": {
            "holdout": run_dataset("holdout", h_rows, ex, pool, multi_seed_n=multi_seed_n),
            "corpus": run_dataset("corpus", c_rows, ex, pool, multi_seed_n=multi_seed_n),
        },
        "exploratory_derivation_split": {
            "holdout": exploratory_derivation_split("holdout", h_rows, ex, pool, multi_seed_n=multi_seed_n),
            "corpus": exploratory_derivation_split("corpus", c_rows, ex, pool, multi_seed_n=multi_seed_n),
        },
        "real_attribution": real_attribution_section(pool, multi_seed_n=multi_seed_n),
        "blockers": [
            {
                "id": "A5-B3",
                "title": "A5 阻塞条件 3：现有架构不支持干净分离",
                "detail": "FD 对每个样本跑**全池**，没有'在预算下选子集'这一层。"
                          "现状 'FD 用到的资产数' 是从 catch 反推的**事后记账**，不是选择量。"
                          "把它当 FD 的选择 ⇒ oracle（用了评测集自身信息）；"
                          "把预算设成全池 ⇒ Random 抽满池，Δ 恒 0。两条路都不是选择-vs-选择对照。",
                "consequence": "预注册的 FD-vs-Random 主对照**不得**被读作"
                               "'failure-driven selection 优于 random selection'。",
                "mitigation": "新增探索性派生集对照（exploratory_derivation_split）："
                              "在旧样本上估 fail_hits、在新样本上评估 ⇒ FD 成为真预测器。",
            },
        ],
        "honest_notes": [
            "所有数字由逐样本明细现算；区间用 Clopper–Pearson 95%（tools/stat_bounds.py）。",
            "运行层是 replay 不是重跑 ⇒ '运行时间' 只报 replay 墙钟 + 声明式序数成本，"
            "**不报**真实执行耗时（未实测，不得编造）。",
            "Random 臂有随机性 ⇒ 报 N=%d 次运行的分布（均值/标准差/2.5–97.5 分位），"
            "单点 seed=%d 只用于配对检验。" % (multi_seed_n, SEED),
            "资产池的 cost_units 是**声明式序数**（未实测墙钟）；把它当秒数是错的。",
            "exploratory_derivation_split 非预注册、非确认性 ⇒ 只读方向 + CI。",
        ],
    }


def _sha256(doc: dict) -> str:
    """内容哈希（**剔除计时字段**：replay_wall_seconds 每次不同，不该进复现性判定）。"""
    clean = json.loads(json.dumps(doc, ensure_ascii=False))

    def _strip(o: Any) -> None:
        if isinstance(o, dict):
            o.pop("replay_wall_seconds", None)
            for v in o.values():
                _strip(v)
        elif isinstance(o, list):
            for v in o:
                _strip(v)

    _strip(clean)
    return hashlib.sha256(json.dumps(clean, ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="673p D：A5（random-budget）实验运行器")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--multi-seed", type=int, default=MULTI_SEED_N)
    a = ap.parse_args(argv)
    if a.check:
        return selftest()

    ex: Executor = ReplayExecutor()
    pool = vp.ASSET_POOL
    doc = _payload(ex, pool, multi_seed_n=a.multi_seed)

    # 复现性：同进程内连跑两次，内容哈希必须一致（与 672g b3_real 同法）
    h1 = _sha256(doc)
    h2 = _sha256(_payload(ex, pool, multi_seed_n=a.multi_seed))
    doc["reproducibility"] = {"run1_sha256": h1, "run2_sha256": h2, "identical": h1 == h2}

    if a.json:
        print(json.dumps(doc, ensure_ascii=False, indent=2))
    else:
        for name in ("holdout", "corpus"):
            p = doc["primary"][name]
            arms = p["arms"]
            print(f"[a5-673p] {name}: FD(full) {arms['fd_full_pool']['rate_pct']}% "
                  f"({arms['fd_full_pool']['k']}/{arms['fd_full_pool']['n']}) | "
                  f"Random {arms['random']['rate_pct']}% | Static {arms['static']['rate_pct']}% "
                  f"| budget k={p['budget']['k_assets']}")
            t = p["paired_tests"]["fd_vs_random"]
            print(f"           FD-vs-Random Δ{t['delta_pp']:+.2f}pp p={t['mcnemar_p']:.3e} "
                  f"(b={t['discordant_fd_only']}, c={t['discordant_other_only']})")
            e = doc["exploratory_derivation_split"][name]
            if e.get("status") == "exploratory":
                print(f"           [explor] FD {e['arms']['fd_derived']['k']}/{e['evaluation']['n']} vs "
                      f"Random {e['arms']['random']['k']}/{e['evaluation']['n']} vs "
                      f"Static {e['arms']['static']['k']}/{e['evaluation']['n']}")
        print(f"[a5-673p] 复现一致：{doc['reproducibility']['identical']}")
        print(f"[a5-673p] A5 阻塞：{doc['blockers'][0]['title']}")

        ra = doc.get("real_attribution", {})
        if ra.get("status") == "ok":
            print("\n[a5-673r] 真实逐资产实测（prereg 673r，FD 的 fail_hits 只来自派生集）")
            for name, d in ra["datasets"].items():
                prim = next(x for x in d["primary"]["by_k"] if x["is_primary_k"])
                p = prim["paired_tests"]["fd_vs_random"]
                ar = prim["arms"]
                print(f"  {name}: 派生 n={d['derivation']['n']} → 评估 n={d['evaluation']['n']} | k={prim['budget_k']}")
                print(f"    FD {ar['fd']['rate_pct']}% | Random {ar['random']['rate_pct']}% "
                      f"| Static {ar['static']['rate_pct']}% | 全池 {ar['fd_full_pool']['rate_pct']}%")
                print(f"    FD−Random Δ{p['delta_pp']:+.2f}pp CI[{p['delta_ci95_pp'][0]:+.2f},"
                      f"{p['delta_ci95_pp'][1]:+.2f}] p={p['mcnemar_p']:.4f} "
                      f"(b={p['discordant_a_only']}, c={p['discordant_b_only']})")
                dg = d["asset_diagnostics"]["degenerate_on_derivation"]
                if dg:
                    print(f"    退化资产（派生集上常量）：{sorted(dg)}")
        else:
            print(f"\n[a5-673r] 真实段跳过：{ra.get('why', '未知原因')}")

    if not a.no_write:
        OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8", newline="\n")
        print(f"[a5-673p] 写入 {OUT.relative_to(ROOT).as_posix()}")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# 自检（不读仓库产物）
# ─────────────────────────────────────────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    ex = ReplayExecutor()
    s_catch = {"id": "s1", "detector": "asan", "verdict": "catch"}
    s_unk = {"id": "s2", "detector": "unknown", "verdict": "unknown"}
    s_miss = {"id": "s3", "detector": "asan", "verdict": "miss"}
    chk("选中 asan ⇒ catch", ex.verdict(s_catch, ("asan",)) == "catch")
    chk("未选中 asan ⇒ miss", ex.verdict(s_catch, ("ubsan",)) == "miss")
    chk("unknown 与选中集无关", ex.verdict(s_unk, ("asan",)) == "unknown")
    chk("原判 miss 保持 miss", ex.verdict(s_miss, ("asan",)) == "miss")

    chk("McNemar b=13,c=0", abs(mcnemar_exact_p(13, 0) - 2 / 2 ** 13) < 1e-12)
    chk("McNemar 无不一致 ⇒ p=1", mcnemar_exact_p(0, 0) == 1.0)
    lo, hi = cp_interval(17, 21)
    chk("CP95(17/21) ≈ [58.1, 94.6]",
        lo is not None and hi is not None and abs(lo * 100 - 58.1) < 0.3 and abs(hi * 100 - 94.6) < 0.3,
        f"({lo}, {hi})")
    chk("Cohen's h 符号", cohens_h(0.8, 0.2) > 0)

    # ── 673r：真实逐资产层（合成矩阵，不读仓库产物）
    def _raises2(fn) -> bool:
        try:
            fn()
            return False
        except (KeyError, ValueError, TypeError):
            return True

    idx = {"s1": {"asan": "catch", "ubsan": "miss", "compile-time": "unknown"},
           "s2": {"asan": "miss", "ubsan": "miss", "compile-time": "unknown"}}
    aex = AttributionExecutor(idx)
    chk("真实 OR：命中资产在选中集 ⇒ catch", aex.verdict({"id": "s1"}, ("asan",)) == "catch")
    chk("真实 OR：多资产同时命中也算 catch", aex.verdict({"id": "s1"}, ("asan", "ubsan")) == "catch")
    chk("真实 OR：未命中 ⇒ miss", aex.verdict({"id": "s1"}, ("ubsan",)) == "miss")
    chk("真实 OR：只选恒 unknown ⇒ unknown", aex.verdict({"id": "s1"}, ("compile-time",)) == "unknown")
    chk("真实 OR：unknown+miss ⇒ miss", aex.verdict({"id": "s1"}, ("compile-time", "ubsan")) == "miss")
    chk("样本不在矩阵 ⇒ KeyError（fail-loud）",
        _raises2(lambda: aex.verdict({"id": "zzz"}, ("asan",))))
    rows2 = [{"id": "s1"}, {"id": "s2"}]
    chk("fail_hits_real 逐资产计数",
        fail_hits_real(rows2, ["asan", "ubsan", "compile-time"], idx)
        == {"asan": 1, "ubsan": 0, "compile-time": 0})
    dg = degenerate_assets(rows2, ["asan", "ubsan", "compile-time"], idx)
    chk("退化判定：0% catch 被标记", "ubsan" in dg and "compile-time" in dg)
    chk("退化判定：非恒定资产不标记", "asan" not in dg)
    cidx = {"s1": {"w": "catch"}, "s2": {"w": "catch"}}
    chk("退化判定：100% catch 被标记", "w" in degenerate_assets(rows2, ["w"], cidx))
    t1 = paired_test(rows2, ("asan",), ("ubsan",), aex, label_a="fd", label_b="random")
    chk("paired_test 给出 Δ 与 CI", t1["delta_pp"] == 50.0 and t1["delta_ci95_pp"][0] is not None)
    chk("Δ CI 在 n 很小时会跨 0（如实暴露）", t1["ci_crosses_zero"] is True)
    t2 = paired_test([{"id": "s2"}], ("asan",), ("ubsan",), aex)
    chk("无不一致对 ⇒ Δ=0 且 p=1", t2["delta_pp"] == 0.0 and t2["mcnemar_p"] == 1.0)
    chk("缺少归属矩阵 ⇒ 真实段 skip（不伪造）",
        load_attribution(ROOT / "data" / "experiments" / "__none__.json") is None)

    print(f"run_a5_experiment_673p selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
