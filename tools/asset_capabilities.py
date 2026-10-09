#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""asset_capabilities.py — 707-B：**资产能力声明 / 记账口径 / 聚合规则的单一事实源**。

科研依据（红线 8：每项改动标注来源）
====================================
700-F 零成本改进（权威源 ``data/700_design_simulation.json``；703 只读验证
``data/703_zero_cost_validation.json``，生成者 ``tools/compute_703_zero_cost_validation.py``）。
设计 B（aware 记账 + 6 资产声明 + 显式聚合）综合分 **0.7721** 胜过现状 A **0.6230**，
抗漂移评分 **53.05 → 66.67**，而**检出率完全相同**（59.55%）。落地的三条零成本改进：

* **P1 移除零产资产声明**：`wunsequenced` / `compile-time` 在本冻结矩阵上 catch = 0
  （``data/blindspot_676g_stats.json``：二者结构性恒 unknown，永不 catch）。把它们从
  **声明池**移除 ⇒ 构成膨胀份额 0.4602 → 0.0000，**检出率 Δ = 0**。
* **P2 aware 记账**：把「声明了但该环境不支持」的资产未测样本记 ``unknown``
  （absence of evidence）而非 ``miss``（evidence of absence）⇒ Δunknown 从
  **0.00pp 变成 75.265pp**，暴露**静默退化**。
* **P3 聚合规则显式声明**：**OR 对零产资产免疫**（加/减零产资产 OR 覆盖率不变）；
  **mean 会被稀释**（8 资产 vs 6 资产的单资产均值之比 = **1.3333**，即 mean 口径可被
  加零产资产压低）。

红线：``detect_calls = 0``；只读冻结矩阵；产出只写 ``data/707_*``。

用法
====
    python tools/asset_capabilities.py --validate     # 在冻结矩阵上复算 P1/P2/P3 并对账 703
    python tools/asset_capabilities.py --declared      # 打印声明池 / 零产资产 / 有效池
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path
from typing import Any, Final

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

from utils.data_access import DATA, load_json_cached  # noqa: E402

OUT_JSON: Final[Path] = ROOT / "data" / "707_zero_cost_landing_validation.json"

# ── P1：资产声明（科研依据 700-F P1）────────────────────────────────────────
# 声明池 = 项目**声明**支持的资产（口径签名里的 A）。
ALL_ASSETS: Final[tuple[str, ...]] = (
    "asan", "ubsan", "tsan", "compiler-warn",
    "wunsequenced", "cross-compile", "linker", "compile-time",
)
# 零产资产：在本冻结矩阵上 catch = 0（blindspot_676g_stats.json 逐型 asset_catch 全 0）。
# 700-F P1：把二者从**声明**里移除（保留其作为能力边界记录），检出率 Δ = 0。
ZERO_YIELD_ASSETS: Final[tuple[str, ...]] = ("wunsequenced", "compile-time")
# 有效声明池 = 声明池 − 零产资产（设计 B 的 6 资产）。
EFFECTIVE_ASSETS: Final[tuple[str, ...]] = tuple(
    a for a in ALL_ASSETS if a not in set(ZERO_YIELD_ASSETS))

DECLARED_CAPABILITY: Final[dict[str, str]] = {
    "asan": "address sanitizer（WSL g++ 环境门控）",
    "ubsan": "undefined sanitizer（WSL g++ 环境门控）",
    "tsan": "thread sanitizer（WSL g++ 环境门控）",
    "compiler-warn": "编译器告警（编译器无关）",
    "wunsequenced": "【零产】-Wunsequenced 静态未实现（本冻结矩阵恒 unknown）",
    "cross-compile": "交叉编译档（环境门控）",
    "linker": "链接器诊断（环境门控；低边际但不可替代）",
    "compile-time": "【零产】编译期检测器静态未实现（本冻结矩阵恒 unknown）",
}

# ── P2：记账口径（科研依据 700-F P2）────────────────────────────────────────
# 环境门控资产：声明了但**本环境可能不支持**（缺测量 ≠ 缺检出）。
ENV_GATED_ASSETS: Final[tuple[str, ...]] = (
    "asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker")
# 692 的两环境剖面（E1 = WSL 全 6 门控；E2 = native 仅 3 门控 supported）。
E1_SUPPORTED: Final[tuple[str, ...]] = ENV_GATED_ASSETS
E2_SUPPORTED: Final[tuple[str, ...]] = ("compiler-warn", "cross-compile", "linker")
ENV_GAP_E2: Final[tuple[str, ...]] = ("asan", "ubsan", "tsan")
ACCOUNTINGS: Final[tuple[str, ...]] = ("unaware", "aware")

# ── P3：聚合规则（科研依据 700-F P3 / 700-A A5）─────────────────────────────
AGGREGATION_RULES: Final[dict[str, str]] = {
    "or": "任一资产 catch ⇒ catch（**对零产资产免疫**：加/减零产资产率不变）",
    "max": "最好单资产（max）",
    "at_least_2": "至少 2 个资产 catch",
    "mean": "单资产均值（**会被零产资产稀释**：加零产资产会压低读数）",
}
DEFAULT_AGGREGATION: Final[str] = "or"


def _verdict(cell: Any) -> str:
    if isinstance(cell, dict):
        return str(cell.get("verdict", "unknown"))
    return str(cell) if cell is not None else "unknown"


def _pct(k: int, n: int) -> float:
    return round(k / n * 100.0, 4) if n else 0.0


# ── P2 核心：OR 口径 + 记账规则（与 analyze_692_environment.or_verdict 同构）──
def or_verdict(per_asset: dict[str, Any], assets: tuple[str, ...], *,
               accounting: str = "unaware", env_gap: tuple[str, ...] = ()) -> str:
    """OR 口径 + 记账规则。

    * ``accounting="unaware"``（默认，旧行为）：任一 catch ⇒ catch；全 unknown ⇒ unknown；其余 miss。
    * ``accounting="aware"``（700-F P2 新行为）：若无 catch 且 ``env_gap`` 非空
      （声明了但本环境不支持的资产）⇒ unknown（缺测量 ≠ 缺检出），暴露静默退化。
    """
    if accounting not in ACCOUNTINGS:
        raise ValueError(f"未知 accounting={accounting!r}（应为 {ACCOUNTINGS}）")
    vs = [_verdict(per_asset.get(a, "unknown")) for a in assets]
    if "catch" in vs:
        return "catch"
    if accounting == "aware" and env_gap:
        return "unknown"
    if all(v == "unknown" for v in vs):
        return "unknown"
    return "miss"


def triple(verdicts: list[str], *, accounting: str = "unaware") -> dict[str, Any]:
    """三组件向量（P2 落地）：catch / unknown / conditional recall 分开报告。"""
    c = verdicts.count("catch")
    m = verdicts.count("miss")
    u = verdicts.count("unknown")
    n = len(verdicts)
    return {
        "accounting": accounting,
        "catch": c, "miss": m, "unknown": u, "total": n,
        "catch_rate_pct": _pct(c, n),
        "unknown_rate_pct": _pct(u, n),
        "conditional_recall_pct": _pct(c, c + m),
    }


# ── P3 核心：聚合 ─────────────────────────────────────────────────────────
def aggregate_one(per_asset: dict[str, Any], assets: tuple[str, ...], *,
                  rule: str = DEFAULT_AGGREGATION) -> str:
    if rule not in AGGREGATION_RULES:
        raise ValueError(f"未知聚合规则={rule!r}（应为 {tuple(AGGREGATION_RULES)}）")
    vs = [_verdict(per_asset.get(a, "unknown")) for a in assets]
    n_catch = vs.count("catch")
    if rule == "or":
        if n_catch:
            return "catch"
        return "unknown" if vs and all(v == "unknown" for v in vs) else "miss"
    if rule == "max":
        return "catch" if n_catch else "miss"
    if rule == "at_least_2":
        return "catch" if n_catch >= 2 else "miss"
    if rule == "mean":  # 均值口径：>0.5 视为 catch（可被零产资产稀释）
        rate = (n_catch / len(assets)) if assets else 0.0
        return "catch" if rate > 0.5 else "miss"
    raise AssertionError("unreachable")


def aggregate_rate(samples: list[dict[str, Any]], assets: tuple[str, ...], *,
                   rule: str = DEFAULT_AGGREGATION) -> float:
    """覆盖率（P3 报告量）。

    注意 ``rule="mean"`` 是**单资产均值**口径（= 各资产 catch 率的平均），与
    ``aggregate_one(rule="mean")`` 的逐样本语义不同——它正是 700-F P3 用来量化
    「mean 被零产资产稀释」的量（8 资产 13.25% vs 6 资产 17.67%，比值 **1.3333**）。
    """
    if not samples:
        return 0.0
    if rule == "mean":
        n = len(samples)
        per_asset = [sum(1 for s in samples if s["per_asset"][a] == "catch") for a in assets]
        return round(sum(_pct(k, n) for k in per_asset) / len(assets), 4) if assets else 0.0
    hits = sum(1 for s in samples if aggregate_one(s["per_asset"], assets, rule=rule) == "catch")
    return _pct(hits, len(samples))


# ── 读冻结矩阵 ────────────────────────────────────────────────────────────
def _samples(matrix_rel: str) -> list[dict[str, Any]]:
    doc = load_json_cached(DATA / matrix_rel)
    out: list[dict[str, Any]] = []
    for s in doc.get("samples", []):
        out.append({
            "uid": str(s.get("uid") or s.get("sample_id") or ""),
            "split": str(s.get("split") or ""),
            "per_asset": {a: _verdict((s.get("per_asset") or {}).get(a, "unknown"))
                          for a in ALL_ASSETS},
        })
    return out


def declared_report() -> dict[str, Any]:
    """P1 声明报告（无矩阵依赖）。"""
    return {
        "declared_pool": list(ALL_ASSETS),
        "zero_yield_assets": list(ZERO_YIELD_ASSETS),
        "effective_pool": list(EFFECTIVE_ASSETS),
        "capability_notes": DECLARED_CAPABILITY,
    }


# ── 验证：在冻结矩阵上复算 P1/P2/P3 并对账 703 ────────────────────────────
def _near(a: float, b: float, tol: float = 1e-3) -> bool:
    return abs(a - b) <= tol


def validate() -> dict[str, Any]:
    g = _samples("blindspot_676g_detection_matrix.json")   # 1147
    a5 = _samples("a5_676f_detection_matrix.json")          # 1137/566
    eval566 = [s for s in a5 if s["split"] == "evaluation"]

    # P1：逐资产 catch；OR(声明 8) vs OR(有效 6) ⇒ Δ = 0；零产资产 catch = 0
    per_asset_catch = {a: sum(1 for s in g if s["per_asset"][a] == "catch") for a in ALL_ASSETS}
    rate8 = aggregate_rate(g, ALL_ASSETS, rule="or")
    rate6 = aggregate_rate(g, EFFECTIVE_ASSETS, rule="or")
    p1 = {
        "per_asset_catch": per_asset_catch,
        "zero_yield_catch_total": sum(per_asset_catch[a] for a in ZERO_YIELD_ASSETS),
        "detection_rate_declared8_pct": rate8,
        "detection_rate_effective6_pct": rate6,
        "delta_detection_pp": round(rate8 - rate6, 4),
        "claim_p1_holds": (sum(per_asset_catch[a] for a in ZERO_YIELD_ASSETS) == 0
                           and _near(rate8, rate6)),
    }

    # P2：E1 vs E2 在 unaware / aware 两口径下的 Δunknown
    v1 = [or_verdict(s["per_asset"], E1_SUPPORTED, accounting="unaware") for s in eval566]
    v2_un = [or_verdict(s["per_asset"], E2_SUPPORTED, accounting="unaware") for s in eval566]
    v2_aw = [or_verdict(s["per_asset"], E2_SUPPORTED, accounting="aware",
                        env_gap=ENV_GAP_E2) for s in eval566]
    t1, t2un, t2aw = triple(v1), triple(v2_un), triple(v2_aw)
    p2 = {
        "n": len(eval566),
        "E1": t1, "E2_unaware": t2un, "E2_aware": t2aw,
        "delta_unknown_unaware_pp": round(t2un["unknown_rate_pct"] - t1["unknown_rate_pct"], 4),
        "delta_unknown_aware_pp": round(t2aw["unknown_rate_pct"] - t1["unknown_rate_pct"], 4),
        "claim_p2_holds": (_near(t2un["unknown_rate_pct"] - t1["unknown_rate_pct"], 0.0)
                           and _near(t2aw["unknown_rate_pct"] - t1["unknown_rate_pct"], 75.265, 0.01)),
    }

    # P3：OR 对零产免疫；mean 被稀释（6/8 比值 = 1.3333）
    r = {}
    for rule in ("or", "max", "at_least_2", "mean"):
        r[rule] = {"declared8_pct": aggregate_rate(g, ALL_ASSETS, rule=rule),
                   "effective6_pct": aggregate_rate(g, EFFECTIVE_ASSETS, rule=rule)}
    dilution = (round(r["mean"]["effective6_pct"] / r["mean"]["declared8_pct"], 6)
                if r["mean"]["declared8_pct"] else None)
    p3 = {
        "rates": r,
        "delta_or_pp": round(r["or"]["effective6_pct"] - r["or"]["declared8_pct"], 4),
        "delta_mean_pp": round(r["mean"]["effective6_pct"] - r["mean"]["declared8_pct"], 4),
        "mean_dilution_factor": dilution,
        "or_is_zero_yield_immune": _near(r["or"]["effective6_pct"], r["or"]["declared8_pct"]),
        "claim_p3_holds": (_near(r["or"]["effective6_pct"], r["or"]["declared8_pct"])
                           and dilution is not None and _near(dilution, 1.333331, 1e-3)),
    }

    return {
        "schema": "queyi-707/zero-cost-landing-validation/v1",
        "generated_by": "tools/asset_capabilities.py --validate",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "research_basis": ("700-F 零成本改进（data/700_design_simulation.json）；"
                           "对账 703 只读验证（data/703_zero_cost_validation.json）"),
        "cross_check_703": {
            "703_P1_delta_detection_pp": 0.0,
            "703_P1_composition_inflation_8": 0.460241,
            "703_P2_delta_unknown_aware_pp": 75.265,
            "703_P3_mean_dilution_factor": 1.333331,
        },
        "P1": p1, "P2": p2, "P3": p3,
        "anti_drift_score": {                       # 科研依据 700-D（设计 A → B）
            "A_current": 53.05, "B_theory_optimal": 66.67,
            "note": "700-D 设计模拟：落地 P1/P2/P3 后抗漂移评分 53.05 → 66.67（检出率不变）。",
        },
        "all_claims_hold": bool(p1["claim_p1_holds"] and p2["claim_p2_holds"] and p3["claim_p3_holds"]),
        "honest_limits": [
            "全部为只读复算（冻结矩阵 + 692 剖面）；detect_calls = 0。",
            "P1「零产」是**在本冻结矩阵上**零 catch；换语料可能不再零产。",
            "P2 aware 读数基于**单一环境对**（E1 vs E2）⇒ 不声称普适。",
            "检出率是 1147 条（92.9% 人工植入）冻结矩阵上的 OR 覆盖率 ⇒ 不代表真实缺陷分布。",
            "抗漂移评分 53.05/66.67 来自 700-D 设计模拟（同冻结矩阵，四轴模拟），非新实测。",
        ],
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="707-B：资产能力声明 / 记账 / 聚合单一事实源")
    ap.add_argument("--validate", action="store_true", help="在冻结矩阵上复算 P1/P2/P3 并对账 703")
    ap.add_argument("--declared", action="store_true", help="打印声明池 / 零产资产 / 有效池")
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    args = ap.parse_args(argv)

    if args.declared:
        print(json.dumps(declared_report(), ensure_ascii=False, indent=1))
        return 0
    if not args.validate:
        ap.print_help()
        return 0

    doc = validate()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8", newline="\n")
    p1, p2, p3 = doc["P1"], doc["P2"], doc["P3"]
    print("== 707-B 零成本改进落地验证（只读，detect_calls=0）==")
    print(f"  P1 零产资产 catch 合计={p1['zero_yield_catch_total']}；"
          f"OR 8 资产={p1['detection_rate_declared8_pct']}% vs 6 资产={p1['detection_rate_effective6_pct']}%"
          f" ⇒ Δ={p1['delta_detection_pp']}pp  hold={p1['claim_p1_holds']}")
    print(f"  P2 Δunknown：unaware={p2['delta_unknown_unaware_pp']}pp "
          f"vs aware={p2['delta_unknown_aware_pp']}pp  hold={p2['claim_p2_holds']}")
    print(f"  P3 OR Δ={p3['delta_or_pp']}pp（免疫）；mean 稀释因子={p3['mean_dilution_factor']} "
          f"hold={p3['claim_p3_holds']}")
    print(f"  抗漂移评分（700-D）：{doc['anti_drift_score']['A_current']} → "
          f"{doc['anti_drift_score']['B_theory_optimal']}")
    print(f"  ALL_CLAIMS_HOLD = {doc['all_claims_hold']}  → {args.out.relative_to(ROOT).as_posix()}")
    return 0 if doc["all_claims_hold"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
