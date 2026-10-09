#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""compute_700_design_simulation.py — 700-F：反事实评估器设计（**只读**）。

如果重新设计 Queyi，基于 697/698/700 的理论，**最优设计**是什么？

三个候选设计（全部在**同一冻结矩阵**上模拟，不跑 detect）
========================================================
| 设计 | 资产池 | 记账 | 聚合 | 标签 | 说明 |
|---|---|---|---|---|---|
| **A 现状** | 8 声明（含 2 零产） | unaware | OR | 34 类隐式 | 当前 Queyi |
| **B 理论最优** | 6 声明（去 2 零产） | **aware**（三组件） | OR + **可操纵性检查** | **显式声明 λ** | 由 7 公理 + T5/T6 + 相变 + 信息论下界推出 |
| **C 极简** | 3（贪心前 3） | unaware | OR | 34 类隐式 | 最少资产 |

四个评价维度
============
* **检出率**：贪心 $k=4$ 的 OR 覆盖率（冻结矩阵实测）；
* **稳定性**：1 − 构成膨胀份额（698-A Type I 的公式）；
* **审计成本**：检出该设计下"构成漂移"所需配对样本数（700-C 的公式）；
* **抗漂移能力**：四型风险的补数（698-A 的风险评分器公式）。

红线：``detect_calls = 0``；产出只写 ``data/700_*``。

用法
====
    python tools/compute_700_design_simulation.py
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import sys
from itertools import combinations
from pathlib import Path
from typing import Any, Final

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA, load_json_cached  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("compute_700_design_simulation")

MATRIX: Final[str] = "blindspot_676g_detection_matrix.json"
OUT_JSON: Final[Path] = ROOT / "data" / "700_design_simulation.json"

ASSETS: Final[tuple[str, ...]] = (
    "asan", "ubsan", "tsan", "compiler-warn",
    "wunsequenced", "cross-compile", "linker", "compile-time",
)
K: Final[int] = 4


def _verdict(cell: Any) -> str:
    if isinstance(cell, dict):
        return str(cell.get("verdict", "unknown"))
    return str(cell) if cell is not None else "unknown"


def load_catch() -> tuple[dict[str, set[str]], int]:
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


def audit_cost_n(psi: float, eps: float, alpha: float = 0.05) -> int | None:
    """700-C 的样本复杂度（完全单向情形用精确二项判据）。"""
    if psi <= 0 or eps <= 0:
        return None
    m = math.ceil(math.log(alpha / 2.0) / math.log(0.5))
    return math.ceil(m / psi)


def evaluate_design(
    name: str, pool: tuple[str, ...], catch: dict[str, set[str]], n: int,
    aware: bool, declared: tuple[str, ...],
) -> dict[str, Any]:
    """在冻结矩阵上评价一个设计。"""
    sel = greedy(catch, pool, K)
    det = union_n(catch, sel) / n * 100.0
    rand = random_mean(catch, pool, K) / n * 100.0
    g_app = det - rand

    # 构成膨胀份额：与"去掉零产资产后的池"比较
    productive = tuple(a for a in pool if catch.get(a))
    if len(productive) >= K:
        det_c = union_n(catch, greedy(catch, productive, K)) / n * 100.0
        rand_c = random_mean(catch, productive, K) / n * 100.0
        g_clean = det_c - rand_c
    else:
        g_clean = 0.0
    comp_inflation = ((g_app - g_clean) / g_app) if g_app > 0 else 0.0

    # 聚合可操纵性（掺 3 个零产资产后最敏感可用口径的相对变化）
    padded = dict(catch)
    ph = [f"__ph{i}" for i in range(3)]
    for p in ph:
        padded[p] = set()

    def mean_rate(cs: dict[str, set[str]], pl: tuple[str, ...]) -> float:
        return sum(len(cs.get(a, set())) for a in pl) / (len(pl) * n) * 100.0

    v0 = mean_rate(catch, productive)
    v1 = mean_rate(padded, productive + tuple(ph))
    agg_manip = abs(v1 - v0) / v0 if v0 else 0.0

    # 审计成本：检出"构成漂移"（去掉池内最低产资产）所需配对样本数
    lowest = min(pool, key=lambda a: len(catch.get(a, set())))
    kept = tuple(a for a in pool if a != lowest)
    b = sum(1 for u in catch.get(lowest, set())
            if not any(u in catch.get(x, set()) for x in kept))
    c_ = sum(1 for x in kept for u in catch.get(x, set())
             if not any(u in catch.get(y, set()) for y in pool if y != x))
    psi = (b + c_) / n
    eps = abs(b - c_) / n
    cost = audit_cost_n(psi, eps)

    # 四型风险（简化版；与 698-A 的评分器同式）
    risk_i = 100.0 * max(0.0, min(1.0, comp_inflation))
    risk_iv = 100.0 * min(1.0, agg_manip)
    risk_ii = 0.0 if aware else 46.95      # 692 实测的负例污染率
    risk_iii = 12.53 if name == "A_current" else (0.0 if aware else 12.53)
    drift_resistance = 100.0 - max(risk_i, risk_ii, risk_iii, risk_iv)

    return {
        "design": name,
        "declared_assets": list(declared),
        "pool_used_for_selection": list(pool),
        "n_pool": len(pool),
        "accounting": "aware（三组件）" if aware else "unaware（单一 recall）",
        "greedy_k4_selection": list(sel),
        "detection_rate_pct": round(det, 4),
        "random_mean_k4_pct": round(rand, 4),
        "apparent_gain_g_app_pp": round(g_app, 4),
        "composition_inflation_share": round(comp_inflation, 6),
        "aggregation_manipulability": round(agg_manip, 6),
        "audit_cost_paired_samples": cost,
        "risk_scores": {"type_I": round(risk_i, 2), "type_II": round(risk_ii, 2),
                        "type_III": round(risk_iii, 2), "type_IV": round(risk_iv, 2)},
        "drift_resistance_100": round(drift_resistance, 2),
    }


def composite(d: dict[str, Any]) -> float:
    """综合分 = 检出率(0.35) + 稳定性(0.25) + 抗漂移(0.25) + 成本效益(0.15)。"""
    det = float(d["detection_rate_pct"]) / 100.0
    stab = 1.0 - float(d["composition_inflation_share"])
    resist = float(d["drift_resistance_100"]) / 100.0
    cost = int(d["audit_cost_paired_samples"] or 0)
    # 成本效益：成本越低越好；以 900 个样本为 0 分、0 个样本为 1 分
    cost_score = 1.0 if not cost else max(0.0, 1.0 - min(1.0, cost / 900.0))
    return round(0.35 * det + 0.25 * stab + 0.25 * resist + 0.15 * cost_score, 6)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="700-F 反事实评估器设计（只读）")
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    args = ap.parse_args(argv)

    catch, n = load_catch()
    _log.info("冻结矩阵 %d 条", n)

    designs = {
        "A_current": evaluate_design(
            "A_current", ASSETS, catch, n, aware=False, declared=ASSETS),
        "B_theory_optimal": evaluate_design(
            "B_theory_optimal",
            tuple(a for a in ASSETS if catch.get(a)), catch, n, aware=True,
            declared=tuple(a for a in ASSETS if catch.get(a))),
        "C_minimal": evaluate_design(
            "C_minimal", ("asan", "ubsan", "tsan"), catch, n, aware=False,
            declared=("asan", "ubsan", "tsan")),
    }
    for k, v in designs.items():
        v["composite_score"] = composite(v)

    ranked: list[dict[str, Any]] = sorted(
        designs.values(), key=lambda d: -float(d["composite_score"]))
    best = str(ranked[0]["design"])

    recommendations: list[dict[str, Any]] = [
        {"priority": 1, "change": "把 2 个**零产资产**从「声明」里移除（保留其作为能力边界记录）",
         "effect": f"构成膨胀份额从 {designs['A_current']['composition_inflation_share']:.4f} "
                   f"降到 {designs['B_theory_optimal']['composition_inflation_share']:.4f}",
         "cost": "极低（改声明，不动代码）", "type": "低垂果实"},
        {"priority": 2, "change": "记账口径从 unaware 改为 **aware（三组件向量）**",
         "effect": f"Type II 风险从 {designs['A_current']['risk_scores']['type_II']} 降到 0"
                   "（负例污染率不再被隐藏）",
         "cost": "低（692 已有 aware 实现）", "type": "低垂果实"},
        {"priority": 3, "change": "在报告里**显式声明聚合规则**并附可操纵性检查",
         "effect": f"Type IV 风险从 {designs['A_current']['risk_scores']['type_IV']} "
                   "被暴露（不再静默）",
         "cost": "低（698-A 的评分器已实现）", "type": "低垂果实"},
        {"priority": 4, "change": "把标签词表 λ 写进口径签名（6 元组），所有分组统计附词表",
         "effect": "Type III 风险从静默变为可检出（698-A Type III 的实测）",
         "cost": "中（需改报告规范）", "type": "中等改动"},
        {"priority": 5, "change": "补齐第 3 个环境 profile（容器化）",
         "effect": "环境轴从 2 个控制点升到 3 个；H-D4 从「一个环境对」升到「两个」",
         "cost": "高（需新实测，受红线限制）", "type": "大改"},
        {"priority": 6, "change": "引入等边际替换设计以分离 g_comp 与 g_mech",
         "effect": "把「不可识别」变成「可识别」（697 定理 A2 推论）",
         "cost": "中（只读重排，不需新 detect）", "type": "中等改动"},
        {"priority": 7, "change": "**不要**减少资产数以求简洁（设计 C 的反面教材）",
         "effect": f"设计 C 检出率 {designs['C_minimal']['detection_rate_pct']:.2f}% vs "
                   f"设计 A {designs['A_current']['detection_rate_pct']:.2f}%",
         "cost": "—", "type": "设计原则"},
    ]

    doc: dict[str, Any] = {
        "schema": "queyi-700/design-simulation/v1",
        "generated_by": "tools/compute_700_design_simulation.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "n_samples": n,
        "design_principles_from_theory": {
            "从 7 公理": [
                "A1（口径可枚举）⇒ 口径签名必须显式且有限 ⇒ 设计 B 把 λ 写进签名",
                "A2（单调）⇒ 撤除组件只能降率 ⇒ 报告必须区分「降率」与「丢测量」",
                "A5（超可加）⇒ 多口径变化同时发生时**不能线性相加** ⇒ 报告必须逐口径分别声明",
                "A6/A7（不可逆 / 可观测分层）⇒ 必须 aware 记账，否则丢失不可见",
            ],
            "从 T5/T6": [
                "T5（链式 CK 条件）⇒ 跨多步漂移**不能**靠矩阵相乘推断 ⇒ 每步都要配对重测",
                "T6（可纠错边界）⇒ 获取层漂移不可事后纠正 ⇒ 组件不可随意撤除；"
                "后处理层（聚合/标签/记账）可纠正 ⇒ 保留原始 per-asset 矩阵是**硬要求**",
            ],
            "从相变理论（700-B）": [
                "Type II/IV 是一阶相变（不连续跳变）⇒ 一旦发生就**已经**跳完，无法提前干预 ⇒ "
                "设计上要**避免不连续的口径切换**（如换环境），改为可平滑过渡的口径",
                "Type I 无临界点（平滑退化）⇒ 可用**结构性预警指标**（零产组件数）监测",
            ],
            "从信息论下界（700-C）": [
                "Type III/IV 在配对设计下 ψ = 0 ⇒ **配对设计对它们无效** ⇒ "
                "设计必须包含**非配对的口径对比**（设计级对照）",
                "Type I 需 n ≈ 849 个配对样本（ψ = 0.0071）⇒ 审计成本由**不一致率**而非效应量主导 ⇒ "
                "应优先提高不一致率（如撤除高独有贡献的组件）",
            ],
        },
        "designs": designs,
        "ranking": [{"design": d["design"], "composite_score": d["composite_score"]}
                    for d in ranked],
        "best_design": best,
        "recommendations": recommendations,
        "honest_limits": [
            "三个设计都在**同一冻结矩阵**上模拟 ⇒ 只反映「资产池 / 记账 / 聚合 / 标签」四轴，"
            "不含真实环境变化（那需要新实测）。",
            "综合分的四个权重（0.35/0.25/0.25/0.15）与本批自定的成本标定（900 样本 = 0 分）"
            "都**无外部标定**。",
            "设计 B 的「理论最优」是**相对本批的四轴**而言，不是全局最优；"
            "**不声称全局最优**（资产池只有 8 个可选，搜索空间极小）。",
            "设计 C（3 资产）的检出率下降幅度取决于**贪心序**；换序会变。",
            "所有数字来自 1147 条（92.9% 人工植入）的冻结矩阵 ⇒ 不代表真实缺陷分布。",
        ],
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    _log.info("已写出 %s", args.out)

    print("== 700-F 反事实评估器设计（只读）==")
    print(f"  冻结矩阵 n={n}")
    for k, d in designs.items():
        print(f"  [{d['design']}]")
        print(f"    池={d['n_pool']} 资产  贪心选择={d['greedy_k4_selection']}")
        print(f"    检出率={d['detection_rate_pct']:.2f}%  表观增益={d['apparent_gain_g_app_pp']:.2f}pp  "
              f"构成膨胀={d['composition_inflation_share']:.4f}")
        print(f"    审计成本={d['audit_cost_paired_samples']} 配对样本  "
              f"抗漂移={d['drift_resistance_100']:.2f}/100  综合={d['composite_score']:.4f}")
    ranking_str = " > ".join(f"{d['design']}({d['composite_score']:.4f})" for d in ranked)
    print(f"\n  排名：{ranking_str}")
    print(f"  ⇒ 最优设计 = {best}")
    print("\n  改进建议（按优先级）：")
    for r in recommendations:
        print(f"    P{r['priority']} [{r['type']}] {r['change'][:44]}…")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
