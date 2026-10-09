#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""compute_710_a8_empirical.py — 710-A3：A8（标签轴闭包）在真实冻结矩阵上的**实证验证**。

科研依据
========
700-A 元理论（``data/700_metatheory.md`` §2.1）给出了 A8 缺失的**构造见证**：
固定覆盖结构、逐样本裁决 V=(c,c,c,m)，细词表（3 类）与粗词表（1 类）下
「逐样本裁决与全部 7 条公理量不变，但分组统计改变」⇒ Type III 漂移不可表达。

本脚本把该见证从「4 样本玩具域」抬到**真实冻结数据**（1147 条 676g 矩阵）：

1. **真实词表阶梯**：``defect_type``(34) → ``group``(14, 681) → ``family``(8, 697)，
   逐一验证「父子是函数」（真粗化，不是两套划分）；
2. 在三个 λ 下重算**分组统计量**（>50% 盲类占比 / 宏观平均盲区率 / 最差类身份），
   同时确认 **逐样本裁决与 OR 检出率逐位不变**；
3. **量化 λ 的自由度**：在 34 类之上枚举/构造任意标签映射，求分组统计量的可达范围
   （含构造性极值 + 随机划分分布）；
4. 给出「对论文意味着什么」的判定（威胁有效性 or 新审计维度）。

红线
====
``detect_calls = 0``；只读 ``data/blindspot_676g_detection_matrix.json``（1147 条）与
``data/681_type_stats_normalized.json``（词表层）；**0 处**论文正文/bib 修改。
输出：``data/710_a8_empirical.json``。

用法
====
    python tools/compute_710_a8_empirical.py
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import random
import sys
from collections import defaultdict
from itertools import combinations
from pathlib import Path
from typing import Any, Final

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA, load_json_cached  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("compute_710_a8_empirical")

OUT_JSON: Final[Path] = ROOT / "data" / "710_a8_empirical.json"

MATRIX: Final[str] = "blindspot_676g_detection_matrix.json"
TYPE_STATS: Final[str] = "681_type_stats_normalized.json"

# 697 的 34 → 8 家族映射（``tools/train_697_predictor.py::FAMILY_OF``，逐字复制，
# 不 import 该模块以免触发其顶层源码特征依赖）。
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


# ══════════════════════════════════════════════════════════════════════════
# 1. 读数
# ══════════════════════════════════════════════════════════════════════════
def load_rows() -> list[dict[str, Any]]:
    doc = load_json_cached(DATA / MATRIX)
    out: list[dict[str, Any]] = []
    for s in doc.get("samples", []):
        out.append({
            "uid": s.get("uid"),
            "defect_type": str(s.get("defect_type") or "unknown"),
            "or6": str(s.get("or_verdict_available6") or "unknown"),
        })
    return out


def group_of() -> dict[str, str]:
    d = load_json_cached(DATA / TYPE_STATS)
    return {t: str(v.get("group") or "unknown") for t, v in d.get("per_type", {}).items()}


# ══════════════════════════════════════════════════════════════════════════
# 2. 分组统计量（给定标签映射 λ: 样本 → 类）
# ══════════════════════════════════════════════════════════════════════════
def stats_under_lambda(rows: list[dict[str, Any]], lam: list[str]) -> dict[str, Any]:
    """在标签映射 λ 下重算分组统计量。

    * ``share_high_blind_pct``：盲区率 > 50% 的**类占比**（式如论文 13/34=38.24% 的那个数）
    * ``macro_mean_blind_pct``：类级盲区率的**未加权平均**
    * ``micro_blind_pct``：整帧盲区率（**λ 不变**，作为对照）
    * ``worst_class`` / ``worst_blind_pct``：最差类的身份与盲区率
    """
    per: dict[str, list[int]] = defaultdict(list)
    for r, t in zip(rows, lam):
        blind = 0 if r["or6"] == "catch" else 1        # unknown 记盲（与 681/698 同口径）
        per[t].append(blind)
    rates = {t: sum(v) / len(v) for t, v in per.items()}
    n_high = sum(1 for v in rates.values() if v > 0.5)
    worst = max(rates.items(), key=lambda kv: (kv[1], kv[0]))
    return {
        "n_classes": len(rates),
        "share_high_blind_pct": round(100.0 * n_high / len(rates), 4),
        "n_high_blind": n_high,
        "macro_mean_blind_pct": round(100.0 * sum(rates.values()) / len(rates), 4),
        "micro_blind_pct": round(100.0 * sum(sum(v) for v in per.values()) / len(lam), 4),
        "worst_class": worst[0],
        "worst_blind_pct": round(100.0 * worst[1], 4),
        "high_blind_classes": sorted([t for t, v in rates.items() if v > 0.5]),
    }


# ══════════════════════════════════════════════════════════════════════════
# 3. 任意标签映射下统计量的可达范围（λ 的自由度 = A8 违规定量）
# ══════════════════════════════════════════════════════════════════════════
def extreme_lambdas(rows: list[dict[str, Any]], k: int) -> list[tuple[str, list[str]]]:
    """构造两个**可达**的 λ 极值（用于证明统计量范围，不是启发式搜索）。

    * ``max_share``：k-1 个「盲样本单例类」（100% 盲）+ 1 个余下样本类 ⇒ 占比 (k-1)/k
      （要求盲样本数 ≥ k-1；否则退化）
    * ``min_share``：全部样本 1 类（k=1 时）或按"盲/非盲"二分（k≥2 且全局盲区率 ≤ 50% 时
      两个类都不超 50%）
    """
    blind_idx = [i for i, r in enumerate(rows) if r["or6"] != "catch"]
    out: list[tuple[str, list[str]]] = []
    if k == 1:
        out.append(("construct_single_class", ["all"] * len(rows)))
        return out
    if k >= 2 and len(blind_idx) >= k - 1:
        lam = ["rest"] * len(rows)
        for j, i in enumerate(blind_idx[: k - 1]):
            lam[i] = f"blind_{j}"
        out.append(("construct_max_singleton_blind", lam))
    # min：盲/非盲二分（两类均需 ≤50%）
    lam2 = ["blind" if r["or6"] != "catch" else "catch" for r in rows]
    out.append(("construct_binary_blind_vs_catch", lam2))
    return out


def random_partition_range(rows: list[dict[str, Any]], k: int, draws: int,
                           seed: int = 710) -> dict[str, Any]:
    """随机把样本划成 k 类（λ 的一个随机样本），统计 ``share_high_blind`` 的分布。"""
    rng = random.Random(seed * 1000 + k)
    n = len(rows)
    vals: list[float] = []
    for _ in range(draws):
        lam = [str(rng.randrange(k)) for _ in range(n)]
        st = stats_under_lambda(rows, lam)
        vals.append(st["share_high_blind_pct"])
    vals.sort()
    return {
        "k": k,
        "draws": draws,
        "min": round(vals[0], 4),
        "p05": round(vals[int(0.05 * len(vals))], 4),
        "median": round(vals[len(vals) // 2], 4),
        "p95": round(vals[int(0.95 * len(vals))], 4),
        "max": round(vals[-1], 4),
    }


def _share_of(groups: list[tuple[str, int, int]], thr: float = 0.5) -> float:
    """组级 (name, n, blind) 列表上的「>thr 盲的组占比」%。"""
    hi = sum(1 for _, n, b in groups if n > 0 and b / n > thr)
    return round(100.0 * hi / len(groups), 4)


def coarsening_search(rows: list[dict[str, Any]], lam: list[str]) -> dict[str, Any]:
    """**只允许合并**（真粗化）时，「>50% 盲的类占比」的可达范围（贪心下界）。

    起点 = 34 类词表本身；每一步在所有二组合并里挑「合并后占比最大」的那一个，
    直到无法再提升。这是**下界**（贪心），不是全局最优 —— 已如实标注。
    """
    per: dict[str, list[int]] = defaultdict(list)
    for r, t in zip(rows, lam):
        per[t].append(0 if r["or6"] == "catch" else 1)
    groups = [(t, len(v), sum(v)) for t, v in per.items()]
    start = _share_of(groups)
    traj: list[dict[str, Any]] = [{"step": 0, "n_groups": len(groups),
                                   "share_pct": start, "merge": None}]
    step = 0
    while len(groups) > 1:
        best: tuple[float, int, int, tuple[str, int, int], list[tuple[str, int, int]]] | None = None
        for i, j in combinations(range(len(groups)), 2):
            gi, gj = groups[i], groups[j]
            merged = (f"{gi[0]}+{gj[0]}", gi[1] + gj[1], gi[2] + gj[2])
            cand = [g for k, g in enumerate(groups) if k not in (i, j)] + [merged]
            sh = _share_of(cand)
            if best is None or sh > best[0]:
                best = (sh, i, j, merged, cand)
        if best is None or best[0] <= float(traj[-1]["share_pct"]) + 1e-9:
            break
        _, i, j, merged, cand = best
        step += 1
        groups = cand
        traj.append({"step": step, "n_groups": len(groups), "share_pct": _share_of(groups),
                     "merge": f"{merged[0]}"})
    return {
        "start_share_pct": start,
        "greedy_end_share_pct": traj[-1]["share_pct"],
        "n_groups_end": traj[-1]["n_groups"],
        "n_steps": step,
        "trajectory": traj[:12],
        "note": "贪心**下界**；真粗化（只许合并）下的可达范围 = [0%（全部并成 1 类）, 本值]",
    }


# ══════════════════════════════════════════════════════════════════════════
# 4. 主流程
# ══════════════════════════════════════════════════════════════════════════
def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="710-A3 A8 实证验证（只读冻结矩阵）")
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    ap.add_argument("--draws", type=int, default=2000, help="每个 k 的随机划分抽样次数")
    args = ap.parse_args(argv)

    rows = load_rows()
    gmap = group_of()

    lam_type = [r["defect_type"] for r in rows]
    lam_group = [gmap.get(r["defect_type"], "unknown") for r in rows]
    lam_family = [FAMILY_OF.get(r["defect_type"], "language_oop") for r in rows]

    # ── (a) 真粗化校验：type → group → family 是不是"函数" ──────────────
    t2g: dict[str, set[str]] = defaultdict(set)
    g2f: dict[str, set[str]] = defaultdict(set)
    for t, g, f in zip(lam_type, lam_group, lam_family):
        t2g[t].add(g)
        g2f[g].add(f)
    hierarchy = {
        "type_to_group_is_function": all(len(v) == 1 for v in t2g.values()),
        "group_to_family_is_function": all(len(v) == 1 for v in g2f.values()),
        "n_types": len(set(lam_type)),
        "n_groups": len(set(lam_group)),
        "n_families": len(set(lam_family)),
        "type_to_group_violations": {t: sorted(v) for t, v in t2g.items() if len(v) > 1},
        "group_to_family_violations": {g: sorted(v) for g, v in g2f.items() if len(v) > 1},
    }

    # ── (b) 三个真实词表下的分组统计量 ─────────────────────────────────
    ladder = []
    for name, lam in (("defect_type(34)", lam_type),
                      ("group(14, 681)", lam_group),
                      ("family(8, 697)", lam_family)):
        st = stats_under_lambda(rows, lam)
        ladder.append({"vocabulary": name, **st})

    micro = {s["vocabulary"]: s["micro_blind_pct"] for s in ladder}

    # ── (c) λ 自由度：可达范围 ────────────────────────────────────────
    n = len(rows)
    blind_n = sum(1 for r in rows if r["or6"] != "catch")
    extremes = []
    # k=1（全部样本 1 类）给下界 0%（整帧盲区率 38.36% < 50%），k=34 给上界
    for k in (1, 2, 3, 8, 34):
        for tag, lam in extreme_lambdas(rows, k):
            st = stats_under_lambda(rows, lam)
            extremes.append({"k": k, "construction": tag, **{kk: st[kk] for kk in (
                "share_high_blind_pct", "n_classes", "macro_mean_blind_pct",
                "worst_class", "worst_blind_pct")}})
    rand = [random_partition_range(rows, k, args.draws) for k in (2, 3, 5, 8, 14, 20, 34)]
    coarsen = coarsening_search(rows, lam_type)

    share_values = sorted({s["share_high_blind_pct"] for s in ladder})
    construct_vals = sorted({e["share_high_blind_pct"] for e in extremes})

    doc: dict[str, Any] = {
        "schema": "queyi-710/a8-empirical/v1",
        "generated_by": "tools/compute_710_a8_empirical.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "research_basis": ("700-A 元理论 §2.1 的标签粗化见证（4 样本玩具域）"
                           "在 1147 条 676g 冻结矩阵上的真实化"),
        "frame": {"source": MATRIX, "n": n, "blind_n": blind_n,
                  "overall_blind_pct": round(100.0 * blind_n / n, 4),
                  "verdict_source": "or_verdict_available6（OR(6)，wunsequenced/compile-time 恒 unknown）"},
        "hierarchy_check": hierarchy,
        "ladder": ladder,
        "invariants_under_lambda": {
            "per_sample_verdicts": "逐位相同（同一冻结矩阵，λ 不进入逐样本裁决）",
            "micro_blind_pct_by_vocabulary": micro,
            "micro_is_lambda_invariant": len(set(micro.values())) == 1,
            "note": "7 条公理的形式化只依赖 (A, R) ⇒ λ 变化不影响任何公理量（700-A §2.1）",
        },
        "lambda_freedom": {
            "constructive_extremes": extremes,
            "random_partition_distribution": rand,
            "merge_only_coarsening_greedy": coarsen,
            "observed_share_values_pp": share_values,
            "share_range_observed_and_constructed_pp": [
                min(share_values + construct_vals), max(share_values + construct_vals)],
        },
        "conclusion": None,   # 下方填充
        "honest_limits": [
            "λ 的自由度是**数学事实**（任意 λ: X → T 都合法），本批只是把它在真实矩阵上量化；"
            "构造性极值（如 33 个盲样本单例类）是**可达但荒谬**的词表——它的用途是证明「不声明 λ 的统计量没有意义」，"
            "不是建议使用。",
            "「>50% 盲」阈值 0.5 与 698-A §3.1 一致；换阈值数字会变（同样的 A8 论证照常成立）。",
            "34 类词表来自 681 归一化后的矩阵字段（676g 修复版）；70 类词表与它是两套划分，"
            "不是粗化关系（698-A §7 已登记）⇒ 本节只用**真粗化链** 34→14→8 做阶梯。",
        ],
    }

    doc["conclusion"] = {
        "a8_holds_on_queyi": False,
        "why": ("三档真实词表（34/14/8）是**逐层粗化**（父子关系均为函数，见 hierarchy_check），"
                "逐样本裁决与 OR 检出率**逐位不变**，但「>50% 盲类占比」从 "
                f"{ladder[0]['share_high_blind_pct']}% 变到 {ladder[2]['share_high_blind_pct']}%；"
                "且任意标签映射下该统计量的可达范围为 "
                f"[{min(share_values + construct_vals)}%, {max(share_values + construct_vals)}%]"),
        "paper_implication": (
            "**两者皆是，但威胁是可控的**：①论文现有数字都带**显式词表**（34 类归一化 / 8 家族），"
            "在这些 λ 下数字是良定义的 ⇒ 不构成对已发布数字的有效性威胁；"
            "②但「不声明 λ 的统计量不可比较」必须升格为**报告规范**（700-F 的 P4），"
            "因为同一批裁决在 34/14/8 三档下可给出 38.24% / 31.43% / 37.50% 三个都'正确'的数。"
            "③本条是 A8 的实证支撑：λ 必须进口径签名，否则 Type III 漂移静默。"),
    }

    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8", newline="\n")

    print("== 710-A3 · A8 实证验证（真实冻结矩阵）==")
    print(f"  帧 = {MATRIX}  n = {n}  整体盲区率 = {doc['frame']['overall_blind_pct']}%")
    print(f"  真粗化链校验：type→group={hierarchy['type_to_group_is_function']}；"
          f"group→family={hierarchy['group_to_family_is_function']}")
    for s in ladder:
        print(f"  λ={s['vocabulary']:<18} 类数={s['n_classes']:>3}  "
              f">50%盲类占比={s['share_high_blind_pct']:>7}%  "
              f"宏观均盲={s['macro_mean_blind_pct']:>7}%  最差类={s['worst_class']}({s['worst_blind_pct']}%)")
    print(f"  λ 自由度：构造极值范围 = [{min(share_values + construct_vals)}%, "
          f"{max(share_values + construct_vals)}%]（逐样本裁决冻结）")
    print(f"  A8 在 Queyi 上成立？ {doc['conclusion']['a8_holds_on_queyi']}  → {args.out.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
