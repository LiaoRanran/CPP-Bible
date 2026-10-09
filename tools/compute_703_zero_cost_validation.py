#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""compute_703_zero_cost_validation.py — 703-E：零成本改进 P1–P3 的**计算验证**（只读）。

做什么
======
700-F 提出三条"低垂果实"改进（P1 移除零产资产声明 / P2 改 aware 记账 /
P3 声明聚合规则），总成本≈0。**本脚本把这三条在同一冻结矩阵上真跑一遍**，
看 700-F 声称的效果是否成立、数字是否一致。

* **P1**：把 ``wunsequenced`` / ``compile-time`` 两个**零产资产**从声明里移除，
  重算 OR 检出率与表观增益 $g_{\\text{app}}$ ⇒ 检出率是否 Δ=0、构成膨胀是否归零。
* **P2**：在 692 的**同一环境对**（E1 ``wsl-gcc-13.3`` vs E2 ``windows-native-mingw``）
  上分别按 unaware / aware 两种记账算 catch / unknown / conditional recall。
* **P3**：在同一冻结矩阵上算 **OR / max / at-least-2 / mean** 四种聚合的检出率，
  并检验"OR 对零产资产免疫、mean 被稀释"。

红线
====
* ``detect_calls = 0``（只读冻结矩阵 ``blindspot_676g_detection_matrix.json`` 与
  ``696_transition_matrix.json``）；
* **不修改**检测器 / 样本 / 冻结矩阵；
* 产出只写 ``data/703_*``。

用法
====
    python tools/compute_703_zero_cost_validation.py
    python tools/compute_703_zero_cost_validation.py --json data/703_zero_cost_validation.json
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from itertools import combinations
from pathlib import Path
from typing import Any, Final

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA, load_json_cached  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("compute_703_zero_cost_validation")

MATRIX: Final[str] = "blindspot_676g_detection_matrix.json"
TRANSITION: Final[str] = "696_transition_matrix.json"
OUT_JSON: Final[Path] = ROOT / "data" / "703_zero_cost_validation.json"

ASSETS: Final[tuple[str, ...]] = (
    "asan", "ubsan", "tsan", "compiler-warn",
    "wunsequenced", "cross-compile", "linker", "compile-time",
)
ZERO_YIELD: Final[tuple[str, ...]] = ("wunsequenced", "compile-time")
K: Final[int] = 4


def _verdict(cell: Any) -> str:
    if isinstance(cell, dict):
        return str(cell.get("verdict", "unknown"))
    return str(cell) if cell is not None else "unknown"


def load_catch() -> tuple[dict[str, set[str]], int]:
    """返回 {asset: {uid, ...}} 与样本总数（冻结矩阵，只读）。"""
    doc = load_json_cached(DATA / MATRIX)
    catch: dict[str, set[str]] = {a: set() for a in ASSETS}
    n = 0
    for s in doc.get("samples", []):
        n += 1
        uid = str(s.get("uid") or "")
        pa = s.get("per_asset") or {}
        for a in ASSETS:
            if _verdict(pa.get(a, "unknown")) == "catch":
                catch[a].add(uid)
    return catch, n


def union_n(catch: dict[str, set[str]], pool: tuple[str, ...]) -> int:
    u: set[str] = set()
    for a in pool:
        u |= catch.get(a, set())
    return len(u)


def greedy(catch: dict[str, set[str]], pool: tuple[str, ...], k: int) -> tuple[str, ...]:
    chosen: list[str] = []
    cur: set[str] = set()
    rest = list(pool)
    while len(chosen) < min(k, len(pool)):
        best_a, best_g = None, -1
        for a in rest:
            g = len(catch.get(a, set()) - cur)
            if g > best_g:
                best_a, best_g = a, g
        if best_a is None:
            break
        chosen.append(best_a)
        cur |= catch.get(best_a, set())
        rest.remove(best_a)
    return tuple(chosen)


def random_mean(catch: dict[str, set[str]], pool: tuple[str, ...], k: int) -> float:
    tot = cnt = 0
    for sub in combinations(pool, k):
        tot += union_n(catch, sub)
        cnt += 1
    return tot / cnt if cnt else 0.0


# ---------------------------------------------------------------- P1
def validate_p1(catch: dict[str, set[str]], n: int) -> dict[str, Any]:
    declared8 = ASSETS
    productive = tuple(a for a in ASSETS if catch.get(a))
    removed = tuple(a for a in ASSETS if not catch.get(a))

    # 全池 OR（所有声明资产）—— 对零产资产天然免疫
    det8 = union_n(catch, declared8) / n * 100.0
    det6 = union_n(catch, productive) / n * 100.0

    # 700-F 的口径：贪心 k=4 选中 4 个资产后的 OR 检出率
    sel8 = greedy(catch, declared8, K)
    sel6 = greedy(catch, productive, K)
    det_k4_8 = union_n(catch, sel8) / n * 100.0
    det_k4_6 = union_n(catch, sel6) / n * 100.0
    g_app8 = det_k4_8 - random_mean(catch, declared8, K) / n * 100.0
    g_app6 = det_k4_6 - random_mean(catch, productive, K) / n * 100.0
    comp8 = (g_app8 - g_app6) / g_app8 if g_app8 > 0 else 0.0

    per_asset = {a: len(catch[a]) for a in ASSETS}
    return {
        "declared_pool": list(declared8),
        "zero_yield_assets": list(removed),
        "per_asset_catch": per_asset,
        "removed_catch_total": sum(len(catch[a]) for a in removed),
        "detection_rate_8asset_pct": round(det8, 4),
        "detection_rate_6asset_pct": round(det6, 4),
        "delta_detection_pp": round(det6 - det8, 6),
        "greedy_k4_selection_8": list(sel8),
        "greedy_k4_selection_6": list(sel6),
        "detection_rate_greedy_k4_8asset_pct": round(det_k4_8, 4),
        "detection_rate_greedy_k4_6asset_pct": round(det_k4_6, 4),
        "delta_detection_greedy_k4_pp": round(det_k4_6 - det_k4_8, 6),
        "apparent_gain_8asset_pp": round(g_app8, 4),
        "apparent_gain_6asset_pp": round(g_app6, 4),
        "composition_inflation_8asset": round(comp8, 6),
        "composition_inflation_6asset": 0.0,
        "claim_p1_holds": abs(det6 - det8) < 1e-9 and abs(det_k4_6 - det_k4_8) < 1e-9,
    }


# ---------------------------------------------------------------- P2
def validate_p2(transition: dict[str, Any]) -> dict[str, Any]:
    frames = transition.get("frames", {})
    frame = frames.get("A5_evaluation_566", {})
    n = int(frame.get("n", 0))
    e1 = frame.get("E1", {})
    e2u = frame.get("E2_unaware", {})
    e2a = frame.get("E2_aware", {})

    def rates(d: dict[str, int]) -> dict[str, Any]:
        c = int(d.get("catch", 0))
        m = int(d.get("miss", 0))
        u = int(d.get("unknown", 0))
        denom = c + m
        return {
            "catch": c, "miss": m, "unknown": u, "n": c + m + u,
            "catch_rate_pct": round(c / n * 100.0, 4) if n else None,
            "unknown_rate_pct": round(u / n * 100.0, 4) if n else None,
            "conditional_recall_pct": (round(c / denom * 100.0, 4) if denom else None),
        }

    r1, r2u, r2a = rates(e1), rates(e2u), rates(e2a)
    return {
        "frame": frame.get("frame"),
        "n": n,
        "E1": r1,
        "E2_unaware": r2u,
        "E2_aware": r2a,
        "delta_catch_rate_unaware_pp": round(r2u["catch_rate_pct"] - r1["catch_rate_pct"], 4),
        "delta_unknown_unaware_pp": round(r2u["unknown_rate_pct"] - r1["unknown_rate_pct"], 4),
        "delta_catch_rate_aware_pp": round(r2a["catch_rate_pct"] - r1["catch_rate_pct"], 4),
        "delta_unknown_aware_pp": round(r2a["unknown_rate_pct"] - r1["unknown_rate_pct"], 4),
        "reclassified_miss_to_unknown": int(frame.get("reclassified_miss_to_unknown", 0)),
        "claim_p2_holds": abs(r2u["unknown_rate_pct"] - r1["unknown_rate_pct"]) < 1e-9,
    }


# ---------------------------------------------------------------- P3
def validate_p3(catch: dict[str, set[str]], n: int) -> dict[str, Any]:
    declared8 = ASSETS
    productive = tuple(a for a in ASSETS if catch.get(a))

    def aggregates(pool: tuple[str, ...]) -> dict[str, Any]:
        or_cov = union_n(catch, pool) / n * 100.0
        max_single = max((len(catch[a]) for a in pool), default=0) / n * 100.0
        at_least_2 = 0
        for uid in {u for a in pool for u in catch[a]}:
            if sum(1 for a in pool if uid in catch[a]) >= 2:
                at_least_2 += 1
        at_least_2 = at_least_2 / n * 100.0
        mean_single = sum(len(catch[a]) for a in pool) / (len(pool) * n) * 100.0
        return {
            "n_assets": len(pool),
            "or_pct": round(or_cov, 4),
            "max_single_pct": round(max_single, 4),
            "at_least_2_pct": round(at_least_2, 4),
            "mean_single_pct": round(mean_single, 4),
        }

    a8 = aggregates(declared8)
    a6 = aggregates(productive)
    sel8 = greedy(catch, declared8, K)
    sel6 = greedy(catch, productive, K)
    return {
        "pool_8asset": a8,
        "pool_6asset": a6,
        "greedy_k4_8asset": aggregates(sel8),
        "greedy_k4_6asset": aggregates(sel6),
        "delta_or_pp": round(a6["or_pct"] - a8["or_pct"], 6),
        "delta_max_single_pp": round(a6["max_single_pct"] - a8["max_single_pct"], 6),
        "delta_at_least_2_pp": round(a6["at_least_2_pct"] - a8["at_least_2_pct"], 6),
        "delta_mean_single_pp": round(a6["mean_single_pct"] - a8["mean_single_pct"], 6),
        "mean_dilution_factor": round(a6["mean_single_pct"] / a8["mean_single_pct"], 6)
        if a8["mean_single_pct"] else None,
        "or_is_zero_yield_immune": abs(a6["or_pct"] - a8["or_pct"]) < 1e-9,
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="703-E 零成本改进 P1–P3 计算验证（只读）")
    ap.add_argument("--json", type=Path, default=OUT_JSON)
    args = ap.parse_args(argv)

    catch, n = load_catch()
    transition = load_json_cached(DATA / TRANSITION)
    _log.info("冻结矩阵 %d 条；转移矩阵帧 %s", n, list(transition.get("frames", {})))

    p1 = validate_p1(catch, n)
    p2 = validate_p2(transition)
    p3 = validate_p3(catch, n)

    doc: dict[str, Any] = {
        "schema": "queyi-703/zero-cost-validation/v1",
        "generated_by": "tools/compute_703_zero_cost_validation.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "sources": {
            "matrix": f"data/{MATRIX}",
            "transition": f"data/{TRANSITION}",
            "upstream_700F": "data/700_design_simulation.json",
        },
        "n_samples": n,
        "P1_remove_zero_yield_declarations": p1,
        "P2_aware_accounting": p2,
        "P3_aggregation_rules": p3,
        "cross_check_with_700F": {
            "700F_detection_rate_A_pct": 59.55,
            "700F_detection_rate_B_pct": 59.55,
            "700F_composition_inflation_A": 0.4602,
            "700F_composition_inflation_B": 0.0,
            "this_batch_detection_rate_8asset_pct": p1["detection_rate_8asset_pct"],
            "this_batch_detection_rate_6asset_pct": p1["detection_rate_6asset_pct"],
            "this_batch_composition_inflation_8asset": p1["composition_inflation_8asset"],
        },
        "honest_limits": [
            "全部为**只读复算**：冻结矩阵 + 692 转移矩阵，detect_calls = 0。",
            "P2 的 aware 读数基于**单一环境对**（n_env=1，E1 vs E2）⇒ 不声称普适。",
            "P3 的四种聚合都在**同一批逐样本裁决**上算 ⇒ 只反映聚合规则差异，不含真实能力变化。",
            "检出率是 1147 条（92.9% 人工植入）冻结矩阵上的 OR 覆盖率 ⇒ 不代表真实缺陷分布。",
            "P1 的『零产』是**在本冻结矩阵上**零 catch；换语料可能不再零产。",
        ],
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    _log.info("已写出 %s", args.json)

    print("== 703-E 零成本改进 P1–P3 计算验证（只读）==")
    print(f"  冻结矩阵 n={n}")
    print("\n  P1 移除零产资产声明：")
    print(f"    零产资产 = {p1['zero_yield_assets']}（catch 合计 {p1['removed_catch_total']}）")
    print(f"    全池 OR 检出率 8资产={p1['detection_rate_8asset_pct']:.4f}%  "
          f"6资产={p1['detection_rate_6asset_pct']:.4f}%  Δ={p1['delta_detection_pp']:.6f}pp")
    print(f"    贪心 k=4 检出率 8资产={p1['detection_rate_greedy_k4_8asset_pct']:.4f}%  "
          f"6资产={p1['detection_rate_greedy_k4_6asset_pct']:.4f}%  "
          f"Δ={p1['delta_detection_greedy_k4_pp']:.6f}pp")
    print(f"    表观增益 8={p1['apparent_gain_8asset_pp']:.4f}pp → 6={p1['apparent_gain_6asset_pp']:.4f}pp  "
          f"构成膨胀 {p1['composition_inflation_8asset']:.4f} → 0.0000")
    print(f"    结论 P1 成立 = {p1['claim_p1_holds']}")
    print("\n  P2 aware 记账（A5 评估 566）：")
    print(f"    E1            catch={p2['E1']['catch']}  catch率={p2['E1']['catch_rate_pct']}%  "
          f"unknown率={p2['E1']['unknown_rate_pct']}%")
    print(f"    E2 unaware    catch={p2['E2_unaware']['catch']}  catch率={p2['E2_unaware']['catch_rate_pct']}%  "
          f"unknown率={p2['E2_unaware']['unknown_rate_pct']}%  cond.recall={p2['E2_unaware']['conditional_recall_pct']}%")
    print(f"    E2 aware      catch={p2['E2_aware']['catch']}  catch率={p2['E2_aware']['catch_rate_pct']}%  "
          f"unknown率={p2['E2_aware']['unknown_rate_pct']}%  cond.recall={p2['E2_aware']['conditional_recall_pct']}%")
    print(f"    Δunknown：unaware {p2['delta_unknown_unaware_pp']}pp vs aware {p2['delta_unknown_aware_pp']}pp")
    print("\n  P3 聚合规则：")
    for name, key in (("8 资产池", "pool_8asset"), ("6 资产池", "pool_6asset")):
        a = p3[key]
        print(f"    {name}: OR={a['or_pct']:.4f}%  max={a['max_single_pct']:.4f}%  "
              f"at-least-2={a['at_least_2_pct']:.4f}%  mean={a['mean_single_pct']:.4f}%")
    print(f"    ΔOR={p3['delta_or_pp']:.6f}pp（OR 免疫={p3['or_is_zero_yield_immune']}）  "
          f"Δmean={p3['delta_mean_single_pp']:.4f}pp  稀释因子={p3['mean_dilution_factor']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
