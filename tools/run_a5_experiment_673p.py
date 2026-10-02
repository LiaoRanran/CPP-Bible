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

    print(f"run_a5_experiment_673p selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
