#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""compute_698_composition_drift.py — 698-A：结构性 Goodhart 的口径扫描（**只读，0 次 detect**）。

覆盖四型中的 **Type I（分母/构成）**、**Type III（标签）**、**Type IV（聚合）**；
Type II（环境）复用 692/697 的配对数据（本脚本只做逐资产环境敏感度排名）。

红线
====
* 不修改论文正文 / bib（696 在改）；
* ``detect_calls = 0`` —— 只读冻结矩阵；
* 不修改检测器 / 样本 / 冻结矩阵；
* 产出只写 ``data/698_*``。

主要内容
========
1. **Type I**：把退化资产数 :math:`d` 从 0 扫到 7，量 :math:`g_{\\text{app}}(d)`。
   - 真实池：8 个资产的**全部 255 个非空子集**，按 :math:`d` 分组统计；
   - 注入外推：5 个有效资产 + :math:`j` 个零产"幽灵资产"（:math:`j=0..7`），
     **精确枚举** :math:`\\binom{5+j}{4}` 个随机组合（不用蒙特卡洛）；
   - 拟合：线性 / 二次 / 684 的 :math:`\\mathbb{E}[J]=kd/n` 模型，报 :math:`R^2`。
2. **Type II**：逐资产环境敏感度排名（692 的 E1→E2 数据）。
3. **Type III**：标签粒度阶梯（raw 70 → 34 → 家族 → 批次 → 细粒度）下的盲区曲线。
4. **Type IV**：聚合口径对比与**可操纵性**（加零产资产时哪个口径动得最多）。

用法
====
    python tools/compute_698_composition_drift.py
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from collections import Counter, defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any, Final

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA, load_json_cached  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("compute_698_composition_drift")

MATRIX_1147: Final[str] = "blindspot_676g_detection_matrix.json"
MATRIX_1137: Final[str] = "a5_676f_detection_matrix.json"
STATS_676G: Final[str] = "blindspot_676g_stats.json"
REF_692: Final[str] = "692_environment_paired_experiment.json"
OUT_JSON: Final[Path] = ROOT / "data" / "698_composition_drift.json"

ASSETS: Final[tuple[str, ...]] = (
    "asan", "ubsan", "tsan", "compiler-warn",
    "wunsequenced", "cross-compile", "linker", "compile-time",
)
PRODUCTIVE_5: Final[tuple[str, ...]] = ("asan", "ubsan", "tsan", "compiler-warn", "cross-compile")
K: Final[int] = 4                 # 论文主端点的预算
LOW_YIELD_THRESHOLD: Final[float] = 0.05   # 684 预注册的"低产"下限（5%）

FAMILY_OF: Final[dict[str, str]] = {
    "memory_safety": "memory", "use_after_free": "memory", "double_free": "memory",
    "memory_leak": "memory", "smart_pointer": "memory", "raii_violation": "memory",
    "move_semantics": "memory", "uninitialized_read": "memory",
    "out_of_bounds": "bounds", "null_pointer_deref": "bounds",
    "integer_overflow": "integer", "bit_operation": "integer",
    "type_punning": "alias_type", "strict_aliasing": "alias_type",
    "alignment": "alias_type", "endianness": "alias_type", "linker_odr": "alias_type",
    "data_race": "concurrency", "atomic_ub": "concurrency",
    "memory_order": "concurrency", "deadlock": "concurrency",
    "condition_variable": "concurrency",
    "iterator_invalidation": "stl", "stl_container_ub": "stl",
    "string_ub": "stl", "algorithm_misuse": "stl",
    "virtual_function": "language_oop", "lambda_capture": "language_oop",
    "cross_tu_ub": "language_oop", "logic_error": "language_oop", "other_ub": "language_oop",
    "volatile_misuse": "embedded", "register_ub": "embedded", "interrupt_safety": "embedded",
}


def _verdict(cell: Any) -> str:
    if isinstance(cell, dict):
        return str(cell.get("verdict", "unknown"))
    return str(cell) if cell is not None else "unknown"


def load_catch_sets(name: str) -> tuple[dict[str, set[str]], dict[str, dict[str, Any]]]:
    """返回 ``{asset: 该资产 catch 的样本 uid 集合}`` 与样本元信息。"""
    doc = load_json_cached(DATA / name)
    catch: dict[str, set[str]] = {a: set() for a in ASSETS}
    meta: dict[str, dict[str, Any]] = {}
    for s in doc.get("samples", []):
        uid = str(s.get("uid") or s.get("sample_id") or "")
        pa = s.get("per_asset") or {}
        for a in ASSETS:
            if _verdict(pa.get(a, "unknown")) == "catch":
                catch[a].add(uid)
        meta[uid] = {
            "defect_type": str(s.get("defect_type") or "unknown"),
            "source_batch": str(s.get("source_batch") or "unknown"),
        }
    return catch, meta


def union_count(catch: dict[str, set[str]], pool: tuple[str, ...]) -> int:
    u: set[str] = set()
    for a in pool:
        u |= catch.get(a, set())
    return len(u)


def greedy_pool(catch: dict[str, set[str]], pool: tuple[str, ...], k: int) -> tuple[str, ...]:
    """标准贪心：每步取边际覆盖增量最大的资产（并列取资产表顺序，确定性）。"""
    chosen: list[str] = []
    cur: set[str] = set()
    remaining = list(pool)
    while len(chosen) < min(k, len(pool)):
        best_a, best_gain = None, -1
        for a in remaining:
            gain = len(catch.get(a, set()) - cur)
            if gain > best_gain:
                best_a, best_gain = a, gain
        if best_a is None:
            break
        chosen.append(best_a)
        cur |= catch.get(best_a, set())
        remaining.remove(best_a)
    return tuple(chosen)


def random_mean_exact(catch: dict[str, set[str]], pool: tuple[str, ...], k: int) -> float:
    """随机臂的**精确**期望覆盖率（枚举全部 C(|pool|, k) 子集，不用蒙特卡洛）。"""
    tot = 0
    cnt = 0
    for sub in combinations(pool, k):
        tot += union_count(catch, sub)
        cnt += 1
    return tot / cnt if cnt else 0.0


def degeneracy(catch: dict[str, set[str]], pool: tuple[str, ...], n: int) -> dict[str, int]:
    """池内退化资产计数（两种定义，都报）。"""
    d_abs = 0   # 零产：C_a = ∅
    d_low = 0   # 低产：|C_a|/n < 5%（684 预注册下限；含 linker 的 0.88%）
    for a in pool:
        ca = catch.get(a, set())
        if not ca:
            d_abs += 1
        if len(ca) / n < LOW_YIELD_THRESHOLD:
            d_low += 1
    return {"d_abs_zero_yield": d_abs, "d_low_yield": d_low}


# ══════════════════════════════════════════════════════════════════════════
# 最小二乘拟合（纯标准库：正规方程 + 高斯消元）
# ══════════════════════════════════════════════════════════════════════════
def polyfit(xs: list[float], ys: list[float], degree: int) -> dict[str, Any]:
    """多项式最小二乘 + R²。 degree ∈ {1, 2}。"""
    n = len(xs)
    p = degree + 1
    # 正规方程 A^T A β = A^T y
    ata = [[sum(xs[i] ** (r + c) for i in range(n)) for c in range(p)] for r in range(p)]
    aty = [sum((xs[i] ** r) * ys[i] for i in range(n)) for r in range(p)]
    # 高斯消元
    m = [row[:] + [aty[r]] for r, row in enumerate(ata)]
    for col in range(p):
        piv = max(range(col, p), key=lambda r: abs(m[r][col]))
        m[col], m[piv] = m[piv], m[col]
        if abs(m[col][col]) < 1e-12:
            return {"degree": degree, "coefficients": None, "r2": None, "note": "奇异矩阵"}
        for r in range(p):
            if r != col:
                f = m[r][col] / m[col][col]
                for c in range(col, p + 1):
                    m[r][c] -= f * m[col][c]
    beta = [m[r][p] / m[r][r] for r in range(p)]
    pred = [sum(beta[r] * xs[i] ** r for r in range(p)) for i in range(n)]
    ybar = sum(ys) / n
    ss_res = sum((ys[i] - pred[i]) ** 2 for i in range(n))
    ss_tot = sum((y - ybar) ** 2 for y in ys)
    r2 = 1.0 - ss_res / ss_tot if ss_tot > 0 else None
    return {
        "degree": degree,
        "coefficients": [round(b, 6) for b in beta],
        "r2": round(r2, 6) if r2 is not None else None,
        "ss_res": round(ss_res, 6),
    }


# ══════════════════════════════════════════════════════════════════════════
# Type I · 构成 / 分母漂移
# ══════════════════════════════════════════════════════════════════════════
def type_i_composition(catch: dict[str, set[str]], n: int, frame: str) -> dict[str, Any]:
    """真实池（8 资产的全部非空子集）+ 注入外推（d = 0..7）。"""
    # ── 真实池扫描 ────────────────────────────────────────────────────
    real_rows: list[dict[str, Any]] = []
    for r in range(K, len(ASSETS) + 1):
        for pool in combinations(ASSETS, r):
            g = union_count(catch, greedy_pool(catch, pool, K)) / n * 100.0
            rm = random_mean_exact(catch, pool, K) / n * 100.0
            deg = degeneracy(catch, pool, n)
            real_rows.append({
                "pool": list(pool), "n_assets": r, "d_low_yield": deg["d_low_yield"],
                "d_abs_zero_yield": deg["d_abs_zero_yield"],
                "greedy_k4_pct": round(g, 4), "random_mean_k4_pct": round(rm, 4),
                "g_app_pp": round(g - rm, 4),
            })
    by_d: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in real_rows:
        by_d[str(row["d_low_yield"])].append(row)
    grouped: dict[str, Any] = {}
    for d in sorted(by_d, key=lambda x: int(x)):
        rows = by_d[d]
        gs = [r["g_app_pp"] for r in rows]
        grouped[d] = {
            "n_pools": len(rows),
            "g_app_mean_pp": round(sum(gs) / len(gs), 4),
            "g_app_min_pp": round(min(gs), 4),
            "g_app_max_pp": round(max(gs), 4),
            "d_range_observed": sorted({r["d_abs_zero_yield"] for r in rows}),
        }

    # ── 三个规范池（复现 684/677c）────────────────────────────────────
    canonical = {
        "full_8": ASSETS,
        "pool_B_C_6": ("asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker"),
        "pool_A_5": PRODUCTIVE_5,
    }
    canonical_rows: dict[str, Any] = {}
    for label, pool in canonical.items():
        g = union_count(catch, greedy_pool(catch, pool, K)) / n * 100.0
        rm = random_mean_exact(catch, pool, K) / n * 100.0
        deg = degeneracy(catch, pool, n)
        canonical_rows[label] = {
            "pool": list(pool),
            "d_low_yield": deg["d_low_yield"],
            "greedy_k4_pct": round(g, 4),
            "random_mean_k4_pct": round(rm, 4),
            "g_app_pp": round(g - rm, 4),
        }

    # ── 注入外推：5 个有效资产 + j 个零产幽灵资产 ─────────────────────
    inj_rows: list[dict[str, Any]] = []
    base = {a: catch.get(a, set()) for a in PRODUCTIVE_5}
    for j in range(0, 8):
        pool_map = dict(base)
        for i in range(j):
            pool_map[f"phantom_{i}"] = set()          # 零产资产：C_a = ∅
        pool = tuple(pool_map)
        g = union_count(pool_map, greedy_pool(pool_map, pool, K)) / n * 100.0
        rm = random_mean_exact(pool_map, pool, K) / n * 100.0
        nn = len(pool)
        e_j = K * j / nn                              # 684 的 E[J] = k·d/n
        inj_rows.append({
            "d": j, "n_assets": nn, "greedy_k4_pct": round(g, 4),
            "random_mean_k4_pct": round(rm, 4), "g_app_pp": round(g - rm, 4),
            "E_J_wasted_slots": round(e_j, 6),
        })

    ds = [float(r["d"]) for r in inj_rows]
    gs = [r["g_app_pp"] for r in inj_rows]
    ejs = [r["E_J_wasted_slots"] for r in inj_rows]
    fits = {
        "linear_in_d": polyfit(ds, gs, 1),
        "quadratic_in_d": polyfit(ds, gs, 2),
        "linear_in_E_J_684_model": polyfit(ejs, gs, 1),
    }
    best = max(fits.items(), key=lambda kv: (kv[1]["r2"] if kv[1]["r2"] is not None else -1.0))
    return {
        "frame": frame, "n": n, "k": K,
        "degeneracy_definitions": {
            "d_low_yield": f"|C_a|/n < {LOW_YIELD_THRESHOLD:.0%}（684 预注册下限；全池 d=3，Pool A d=0，Pool B/C d=1）",
            "d_abs_zero_yield": "C_a = ∅（恒 unknown 资产）",
        },
        "canonical_pools": canonical_rows,
        "real_pool_scan": {
            "n_subsets_scanned": len(real_rows),
            "grouped_by_d_low_yield": grouped,
            "note": "8 资产的全部 255 个非空子集中 |P|≥4 的部分；随机臂用**精确枚举**期望，非蒙特卡洛。",
        },
        "injection_scan_d0_to_7": inj_rows,
        "curve_fits": fits,
        "best_fit": best[0],
        "interpretation": (
            "g_app 随 d 单调上升；684 的 E[J]=k·d/n 模型与线性-in-d 模型的 R² 比较"
            "用于判断「表观增益」到底由**退化资产数量**还是**浪费槽位期望**解释得更好。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
# Type II · 环境敏感度排名
# ══════════════════════════════════════════════════════════════════════════
def type_ii_environment(catch: dict[str, set[str]], n: int, frame: str) -> dict[str, Any]:
    """逐资产环境敏感度：该资产在 E1→E2 中丢了多少、其中多少是**独有**捕获。"""
    ref = load_json_cached(DATA / REF_692)
    part = ref["asset_partition"]
    env_gated = set(part["env_gated_assets"])
    e2_sup = set(part["E2_supported"])
    e2_gap = set(part["E2_environment_gap"])

    rows: list[dict[str, Any]] = []
    for a in ASSETS:
        ca = catch.get(a, set())
        others = set().union(*[catch.get(b, set()) for b in ASSETS if b != a]) if ASSETS else set()
        sole = len(ca - others)
        rows.append({
            "asset": a,
            "n_catch": len(ca),
            "catch_rate_pct": round(len(ca) / n * 100.0, 4),
            "sole_catch": sole,
            "sole_catch_pct_of_n": round(sole / n * 100.0, 4),
            "env_gated": a in env_gated,
            "in_E2_supported": a in e2_sup,
            "in_E2_gap_lost": a in e2_gap,
            "sensitivity": ("HIGH" if a in e2_gap else "none"),
            "loss_when_moving_to_E2": len(ca) if a in e2_gap else 0,
        })
    rows.sort(key=lambda r: (-r["sole_catch"], -r["n_catch"]))

    fr = ref["frames"]["A5_evaluation_566"]
    return {
        "frame": frame, "n": n,
        "per_asset_sensitivity": rows,
        "environment_gap_assets": sorted(e2_gap),
        "from_692": {
            "lost_e1_catches_by_asset_sole": fr["silent_false_miss"]["lost_e1_catches_by_asset_sole"],
            "lost_e1_catches": fr["silent_false_miss"]["lost_e1_catches"],
            "e2_reported_negatives": fr["silent_false_miss"]["e2_reported_negatives"],
            "poisoned_share_of_e2_negatives_pct": fr["silent_false_miss"]["poisoned_share_of_e2_negatives_pct"],
        },
        "interpretation": (
            "环境敏感度 = 该资产的捕获在换环境时被静默写成 miss 的量。"
            "**独有捕获数**是关键：被别的资产也覆盖的样本丢了也不影响 OR，"
            "只有独有捕获才真正造成不可信负例。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
# Type III · 标签粒度阶梯
# ══════════════════════════════════════════════════════════════════════════
def type_iii_label(meta: dict[str, dict[str, Any]], catch: dict[str, set[str]], n: int) -> dict[str, Any]:
    """不同标签粒度下「盲区类占比」的曲线。"""
    caught: set[str] = set()
    for a in ASSETS:
        caught |= catch.get(a, set())

    def _ladder(name: str, keyfn: Any) -> dict[str, Any]:
        """按 keyfn 分组，统计每组的**盲区率**（1 = 盲，即未被任何资产捕获）。

        ⚠ 指示变量方向：``1`` 必须是**盲**（not caught）。写反会得到「高检出类占比」，
        与 681 的 13/34 对不上（本批第一版就是这里写反，得 19/34）。
        """
        grp: dict[str, list[int]] = defaultdict(list)
        for uid, m in meta.items():
            grp[str(keyfn(m))].append(0 if uid in caught else 1)
        rates = {k: sum(v) / len(v) for k, v in grp.items()}
        blind = [k for k, r in rates.items() if r > 0.5]
        macro = sum(rates.values()) / len(rates)
        return {
            "granularity": name,
            "n_categories": len(grp),
            "n_high_blindspot_gt50": len(blind),
            "share_high_blindspot_pct": round(len(blind) / len(grp) * 100.0, 4),
            "macro_mean_blindspot_pct": round(macro * 100.0, 4),
            "n_singleton_categories": sum(1 for v in grp.values() if len(v) == 1),
        }

    ladders = [
        _ladder("family_8", lambda m: FAMILY_OF.get(m["defect_type"], "language_oop")),
        _ladder("defect_type_34_normalized", lambda m: m["defect_type"]),
        _ladder("source_batch_9", lambda m: m["source_batch"]),
        _ladder("type_x_batch_fine", lambda m: f"{m['defect_type']}@{m['source_batch']}"),
    ]
    # 70 粒度取自 676g 的 by_type（**原始混合词表**：同时含 MEM/UB/CONC 等粗码与 heap_overflow 等细名）
    stats = load_json_cached(DATA / STATS_676G)
    bt = stats["by_type"]
    hi70 = [x for x in bt if x.get("blindspot_ratio", 0) > 0.5]
    ladders.append({
        "granularity": "raw_70_vocabulary_from_676g_by_type",
        "n_categories": len(bt),
        "n_high_blindspot_gt50": len(hi70),
        "share_high_blindspot_pct": round(len(hi70) / len(bt) * 100.0, 4),
        "macro_mean_blindspot_pct": round(sum(x["blindspot_ratio"] for x in bt) / len(bt) * 100.0, 4),
        "n_singleton_categories": sum(1 for x in bt if x["n"] == 1),
        "note": "原始混合词表（粗码 + 细名 + 元标签混杂），与 34 粒度是**两套不同的划分**，不可互相校验。",
    })
    ladders.sort(key=lambda d: d["n_categories"])
    return {
        "n": n,
        "ladder": ladders,
        "headline": {
            "raw_70": "18 / 70 = 25.71% 的类 >50% 盲（676g by_type）",
            "normalized_34": "13 / 34 = 38.24% 的类 >50% 盲（681 归一化词表）",
            "delta_pp": round(38.2353 - 25.7143, 4),
        },
        "interpretation": (
            "「盲区类占比」是**标签粒度**的函数：粒度越粗，类越少，高盲类的**占比**越高（分子被合并进去了）。"
            "⇒ 任何形如「X/Y 的类 >50% 盲」的表述**必须附带词表**，否则不可比较。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
# Type IV · 聚合口径与可操纵性
# ══════════════════════════════════════════════════════════════════════════
def type_iv_aggregation(catch: dict[str, set[str]], n: int, frame: str) -> dict[str, Any]:
    """比较多种聚合规则；用「掺入零产资产后各口径的变化」量可操纵性。"""
    total_catches = sum(len(catch.get(a, set())) for a in ASSETS)

    def agg(name: str, pool: tuple[str, ...]) -> float:
        if name == "or_any":
            return union_count(catch, pool) / n * 100.0
        if name == "mean_per_asset":
            return (sum(len(catch.get(a, set())) for a in pool) / (len(pool) * n)) * 100.0
        if name == "max_asset":
            return (max(len(catch.get(a, set())) for a in pool) / n) * 100.0
        if name == "min_asset":
            return (min(len(catch.get(a, set())) for a in pool) / n) * 100.0
        if name == "at_least_2_assets":
            cnt: Counter[str] = Counter()
            for a in pool:
                for uid in catch.get(a, set()):
                    cnt[uid] += 1
            return (sum(1 for v in cnt.values() if v >= 2) / n) * 100.0
        raise ValueError(name)

    rules = ("or_any", "mean_per_asset", "max_asset", "min_asset", "at_least_2_assets")
    full = ASSETS
    productive = tuple(a for a in ASSETS if catch.get(a, set()))
    padded = productive + ("phantom_A", "phantom_B", "phantom_C")   # 掺 3 个零产资产

    catch_padded = dict(catch)
    for a in ("phantom_A", "phantom_B", "phantom_C"):
        catch_padded[a] = set()

    rows: list[dict[str, Any]] = []
    for r in rules:
        v_prod = agg(r, productive)
        v_pad = agg(r, padded)
        # 可操纵性 = 掺入 3 个零产资产后报告值的绝对变化
        rows.append({
            "rule": r,
            "value_on_productive_pool_pct": round(v_prod, 4),
            "value_after_padding_3_zero_yield_pct": round(v_pad, 4),
            "manipulability_pp": round(abs(v_pad - v_prod), 4),
            "manipulability_relative_pct": (
                round(abs(v_pad - v_prod) / v_prod * 100.0, 4) if v_prod else None
            ),
        })
    rows.sort(key=lambda d: d["manipulability_pp"])

    return {
        "frame": frame, "n": n,
        "total_asset_catch_events": total_catches,
        "or_rate_pct": round(union_count(catch, full) / n * 100.0, 4),
        "mean_rate_over_8_pct": round(total_catches / (8 * n) * 100.0, 4),
        "mean_rate_over_productive_pct": round(total_catches / (len(productive) * n) * 100.0, 4),
        "aggregation_table": rows,
        "most_robust_rule": rows[0]["rule"],
        "most_manipulable_rule": rows[-1]["rule"],
        "interpretation": (
            "**OR 口径对掺入零产资产完全免疫**（可操纵性 0）——因为 OR 只看并集；"
            "**均值口径最容易被操纵**——往池里塞任意多零产资产就能把报告值拉低。"
            "⇒ 若一个评估系统的分数可以被**不增加任何有效能力**的操作改变，它就存在 Type IV 结构性漂移。"
        ),
    }


# ══════════════════════════════════════════════════════════════════════════
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="698-A 结构性 Goodhart 的口径扫描（只读）")
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    args = ap.parse_args(argv)

    out: dict[str, Any] = {
        "schema": "queyi-698/composition-drift/v1",
        "generated_by": "tools/compute_698_composition_drift.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "frames": {},
    }
    for name, label in ((MATRIX_1147, "capability_boundary_1147"), (MATRIX_1137, "A5_1137")):
        catch, meta = load_catch_sets(name)
        n = len(meta)
        _log.info("%s：n=%d", label, n)
        out["frames"][label] = {
            "n": n,
            "type_I_composition": type_i_composition(catch, n, label),
            "type_II_environment": type_ii_environment(catch, n, label),
            "type_IV_aggregation": type_iv_aggregation(catch, n, label),
        }
        if label == "capability_boundary_1147":
            out["frames"][label]["type_III_label"] = type_iii_label(meta, catch, n)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")
    _log.info("已写出 %s", args.out)

    print("== 698-A 口径扫描（只读）==")
    for label, fr in out["frames"].items():
        ti = fr["type_I_composition"]
        print(f"\n  [{label}] n={fr['n']}")
        for k2, v in ti["canonical_pools"].items():
            print(f"    {k2:<12} d={v['d_low_yield']}  greedy={v['greedy_k4_pct']:.2f}%  "
                  f"rand_mean={v['random_mean_k4_pct']:.2f}%  g_app={v['g_app_pp']:.2f}pp")
        print("    注入扫描 g_app(d)：" +
              "  ".join(f"d={r['d']}:{r['g_app_pp']:.2f}" for r in ti["injection_scan_d0_to_7"]))
        print(f"    最佳拟合 = {ti['best_fit']}；R²: " +
              ", ".join(f"{k}={v['r2']}" for k, v in ti["curve_fits"].items()))
        tv = fr["type_IV_aggregation"]
        print(f"    最稳健聚合 = {tv['most_robust_rule']}（可操纵性 {tv['aggregation_table'][0]['manipulability_pp']}pp）；"
              f"最易操纵 = {tv['most_manipulable_rule']}（{tv['aggregation_table'][-1]['manipulability_pp']}pp）")
    t3 = out["frames"]["capability_boundary_1147"]["type_III_label"]
    print("\n  标签粒度阶梯：" +
          "  ".join(f"{d['n_categories']}类→{d['n_high_blindspot_gt50']}高盲({d['share_high_blindspot_pct']:.1f}%)"
                    for d in t3["ladder"]))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
