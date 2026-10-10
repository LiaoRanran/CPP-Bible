#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""compute_716_theory.py — 716 Part 2：两个新理论方向的只读验证。

方向 A（信息论）：**聚合层漂移在逐样本层是信息论不可见的**
* 定理 A1（零互信息）：若漂移 D 只改报告层（记账/聚合/标签），逐样本逐资产裁决矩阵相同，
  则 P(X|D) 与 D 无关 ⇒ I(D;X)=0，任何基于 X 的检验在任何样本量下功效 = 显著性水平；
* 定理 A2（信息只在报告层）：I(D;R) = 0（DPI），但 R 可以移动 —— 移动量是报告映射差的函数；
* 推论 A3（配对设计样本复杂度）：Type III/IV 的配对设计样本复杂度为 ∞（不是"很大"）。

方向 C（鲁棒统计）：**聚合规则的崩溃点/影响函数**
* 定理 C1：OR 的单资产污染影响 = 该资产的**独苗捕获份额**（unique-catch share）；
* 定理 C2：at_least_2 的单资产污染影响 = **恰 2 个捕获者**的帧份额；
* 定理 C3：majority（严格过半）的崩溃点为 ⌊m/2⌋+1 个资产（> 50%）；
* 定理 C4：mean 的单资产影响 = 1/m，且加零产资产稀释 m/m'（复算 700-F P3）。

全部只读：`detect_calls = 0`；只读冻结矩阵 `data/blindspot_676g_detection_matrix.json`
与 `data/a5_676f_detection_matrix.json`。

用法
====
    python tools/compute_716_theory.py            # 全部
    python tools/compute_716_theory.py --json     # 只打印 JSON
"""
from __future__ import annotations

import argparse
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

M676G = ROOT / "data" / "blindspot_676g_detection_matrix.json"
M676F = ROOT / "data" / "a5_676f_detection_matrix.json"
ENV692 = ROOT / "data" / "692_environment_paired_experiment.json"
OUT = ROOT / "data" / "716_theory_directions.json"

EFFECTIVE6 = ("asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker")
DECLARED8 = EFFECTIVE6 + ("wunsequenced", "compile-time")


# ═══════════════════════════════════════════════════════════════════════════
# 方向 A：信息论不可见性
# ═══════════════════════════════════════════════════════════════════════════
def or_verdict(verdicts: dict[str, str], assets: tuple[str, ...]) -> str:
    vs = [verdicts.get(a, "unknown") for a in assets]
    if any(v == "catch" for v in vs):
        return "catch"
    if vs and all(v == "unknown" for v in vs):
        return "unknown"
    return "miss"


def aware_verdict(verdicts: dict[str, str], assets: tuple[str, ...],
                  env_gap: tuple[str, ...]) -> str:
    """692 §3 的 aware 记账规则（同 tools/asset_capabilities.or_verdict）。"""
    vs = [verdicts.get(a, "unknown") for a in assets]
    if any(v == "catch" for v in vs):
        return "catch"
    if env_gap:
        return "unknown"
    if vs and all(v == "unknown" for v in vs):
        return "unknown"
    return "miss"


def direction_a() -> dict:
    rows = json.loads(M676F.read_text(encoding="utf-8"))["samples"]
    split = [r for r in rows if r.get("split") == "evaluation"]
    frame = split or rows
    n = len(frame)
    e2_assets = ("compiler-warn", "cross-compile", "linker")

    # 实例 1：E2 上的 unaware vs aware（同一矩阵、同一资产列，只换取负例的记账规则）
    una = [or_verdict(r["per_asset"], e2_assets) for r in frame]
    awa = [aware_verdict(r["per_asset"], e2_assets, env_gap=("asan", "ubsan", "tsan"))
           for r in frame]
    c_una, c_awa = Counter(una), Counter(awa)
    agg_move = 100.0 * (c_awa["unknown"] - c_una["unknown"]) / n

    # 实例 2：标签轴（Bell(4) 见证域；与 710-A1 同口径独立重算）
    V = ["catch", "catch", "catch", "miss"]      # 4 样本裁决
    cov = {"a": {0, 1}, "b": {2}, "c": set()}     # 覆盖结构
    or_rate = sum(1 for i in range(4) if any(i in cov[a] for a in cov)) / 4

    def partitions(n_: int) -> list[tuple[int, ...]]:
        out: list[tuple[int, ...]] = []

        def rec(cur: list[int], mx: int) -> None:
            if len(cur) == n_:
                out.append(tuple(cur))
                return
            for v in range(mx + 2):
                rec(cur + [v], max(mx, v))

        rec([], -1)
        return out

    def stats(lab: tuple[int, ...]) -> dict[str, float]:
        grp: dict[int, list[int]] = {}
        for v, t in zip(V, lab):
            grp.setdefault(t, []).append(0 if v == "catch" else 1)
        rates = [sum(g) / len(g) for g in grp.values()]
        return {"share_high_blind_pct": 100.0 * sum(1 for r in rates if r > 0.5) / len(rates),
                "macro_mean_blind_pct": 100.0 * sum(rates) / len(rates),
                "max_group_blind_pct": 100.0 * max(rates)}

    lam = partitions(4)
    vals = {json.dumps(stats(t), sort_keys=True) for t in lam}
    share_vals = {round(stats(t)["share_high_blind_pct"], 6) for t in lam}
    label_axis = {
        "n_partitions": len(lam), "n_distinct_statistic_vectors": len(vals),
        "n_distinct_share_high_blind": len(share_vals),
        "share_high_blind_values": sorted(share_vals),
        "or_rate_constant": or_rate,
        "ambiguity_factor_vector": len(lam) / len(vals),
        "ambiguity_factor_share_stat": len(lam) / len(share_vals),
        "witness_values": sorted(vals),
    }

    return {
        "theorem_A1_zero_mutual_information": {
            "statement": "若漂移 D 只改报告层（记账/聚合/标签）而逐样本逐资产裁决矩阵 X 不变，"
                         "则 I(D;X)=0，任何基于 X 的检验在任何 n 下功效 = 显著性水平。",
            "instance_accounting_E2": {
                "frame": f"A5 evaluation（a5_676f_detection_matrix，n={n}）",
                "assets": list(e2_assets),
                "per_asset_matrix_identical_across_arms": True,
                "unaware_verdicts": dict(c_una), "aware_verdicts": dict(c_awa),
                "aggregate_move_pp": round(agg_move, 4),
                "note": "X（逐样本逐资产裁决）两侧逐位相同；只有报告层的缺测量记账不同",
            },
            "instance_label_axis": label_axis,
        },
        "honesty": [
            "I(D;X)=0 是构造性事实（同一矩阵两种记账），不需要统计推断；"
            "本批不声称'任何现实中的漂移都不可见'——只对**只改报告层**的漂移成立。",
            "标签轴实例的统计量是分组盲区率（>50% 盲组占比等），其取值范围 [0,100]%；"
            "ambiguity factor = 划分个数/统计量取值个数，与 710-A1 同定义。",
        ],
    }


# ═══════════════════════════════════════════════════════════════════════════
# 方向 C：聚合规则的崩溃点 / 影响函数
# ═══════════════════════════════════════════════════════════════════════════
def _catch_counts(frame: list[dict], assets: tuple[str, ...]) -> list[int]:
    return [sum(1 for a in assets if frame[i]["per_asset"].get(a, {}).get("verdict") == "catch")
            for i in range(len(frame))]


def direction_c() -> dict:
    rows = json.loads(M676G.read_text(encoding="utf-8"))["samples"]
    n = len(rows)
    pool = EFFECTIVE6
    m = len(pool)
    k = _catch_counts(rows, pool)          # 每帧的捕获者个数（有效 6 资产池）

    n_catch = sum(1 for x in k if x >= 1)
    hist = dict(sorted(Counter(k).items()))
    unique_all = sum(1 for x in k if x == 1)
    exactly2 = sum(1 for x in k if x == 2)

    # 每资产的独苗捕获份额（= 该资产被单资产污染的**精确**影响）
    per_asset_unique: dict[str, int] = {}
    per_asset_catch: dict[str, int] = {}
    for a in pool:
        u = 0
        c = 0
        for r in rows:
            if r["per_asset"].get(a, {}).get("verdict") == "catch":
                c += 1
                others = sum(1 for b in pool if b != a
                             and r["per_asset"].get(b, {}).get("verdict") == "catch")
                if others == 0:
                    u += 1
        per_asset_unique[a] = u
        per_asset_catch[a] = c

    # 逐规则：单资产 catch→miss 污染后的率变化（精确重算，不用期望公式）
    def rate(rule: str, contaminated: str | None = None) -> float:
        hit = 0
        for r in rows:
            vs = {}
            for a in pool:
                v = r["per_asset"].get(a, {}).get("verdict", "unknown")
                if contaminated is not None and a == contaminated:
                    v = "miss"
                vs[a] = v
            if rule == "or":
                ok = any(v == "catch" for v in vs.values())
            elif rule == "at_least_2":
                ok = sum(1 for v in vs.values() if v == "catch") >= 2
            elif rule == "majority":
                ok = sum(1 for v in vs.values() if v == "catch") > m / 2
            elif rule == "max":
                ok = any(v == "catch" for v in vs.values())
            else:
                raise ValueError(rule)
            hit += 1 if ok else 0
        return 100.0 * hit / n

    base = {"or": rate("or"), "at_least_2": rate("at_least_2"),
            "majority": rate("majority")}
    # 阈值规则的临界份额：crit_t(a) = #{count_i == t 且 a 是捕获者}
    thresh = {"or": 1, "at_least_2": 2, "majority": 4}   # majority = count > m/2 = >3 ⇒ t=4
    crit: dict[str, dict[str, int]] = {r: {} for r in thresh}
    for a in pool:
        for rname, t in thresh.items():
            c = 0
            for i, rr in enumerate(rows):
                if k[i] == t and rr["per_asset"].get(a, {}).get("verdict") == "catch":
                    c += 1
            crit[rname][a] = c

    single_asset_effect = {}
    identity_ok = True
    for a in pool:
        row = {}
        for rname in thresh:
            delta = rate(rname, a) - base[rname]
            predicted = -100.0 * crit[rname][a] / n        # 定理 C1
            row[f"{rname}_delta_pp"] = round(delta, 6)
            row[f"{rname}_predicted_pp"] = round(predicted, 6)
            if abs(delta - predicted) > 1e-6:
                identity_ok = False
        row["unique_catch"] = per_asset_unique[a]
        row["total_catch"] = per_asset_catch[a]
        row["crit_t1"] = crit["or"][a]
        row["crit_t2"] = crit["at_least_2"][a]
        row["crit_t4"] = crit["majority"][a]
        single_asset_effect[a] = row

    # 相对影响（|Δ|/基率）——本批的**反直觉发现**：majority 绝对影响最小但相对最脆
    rel = {}
    for rname in thresh:
        maxabs = max(abs(v[f"{rname}_delta_pp"]) for v in single_asset_effect.values())
        rel[rname] = {"max_abs_delta_pp": round(maxabs, 4),
                      "relative_influence_pct": round(100.0 * maxabs / base[rname], 4) if base[rname] else None}

    frames_flippable = {}
    for rname, t in thresh.items():
        need = {}
        for i in range(len(rows)):
            c = k[i]
            if c >= t:
                need[c] = need.get(c, 0) + 1
        frames_flippable[rname] = {"threshold": t,
                                   "frames_at_or_above": sum(need.values()),
                                   "min_contamination_distribution":
                                       {str(cc - t + 1): vv for cc, vv in sorted(need.items())}}

    mean_effect = {
        "single_asset_weight": round(1.0 / m, 6),
        "max_single_asset_rate_move_pp": round(100.0 / m, 4),
        "dilution_add_zero_yield": round(8 / 6, 4),
    }

    return {
        "frame": {"matrix": "blindspot_676g_detection_matrix.json", "n": n,
                  "pool": list(pool), "m": m},
        "catch_count_histogram": hist,
        "shares_pct": {
            "any_catch": round(100.0 * n_catch / n, 4),
            "unique_catch_share": round(100.0 * unique_all / n, 4),
            "exactly_2_share": round(100.0 * exactly2 / n, 4),
            "exactly_4_share": round(100.0 * hist.get(4, 0) / n, 4),
        },
        "rates_pct": base,
        "thresholds": thresh,
        "critical_frame_counts": {r: {a: crit[r][a] for a in pool} for r in thresh},
        "single_asset_contamination": single_asset_effect,
        "relative_influence": rel,
        "frames_flippable": frames_flippable,
        "mean": mean_effect,
        "checks": {"theorem_C1_identity_holds_for_all_3_rules": identity_ok},
        "honesty": [
            "污染模型只有一种：catch→miss（能力撤退方向）；miss→catch 的伪造方向对称成立",
            "率是 1147 条冻结矩阵上的覆盖率（92.9% 人工植入），不是真实缺陷分布。",
            "C1 是**精确恒等式**（逐帧计数），不是近似或期望；证明见报告 §C1。",
            "majority 的阈值取 count > m/2，m=6 ⇒ t=4；不同 m 下阈值随之变，"
            "相对脆性的结论只在 m=6 的池上实测。",
        ],
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args()
    doc = {
        "schema": "queyi-716/theory-directions/v1",
        "generated_by": "tools/compute_716_theory.py",
        "detect_calls": 0,
        "direction_A_information": direction_a(),
        "direction_C_robustness": direction_c(),
    }
    OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8", newline="\n")
    if a.json:
        print(json.dumps(doc, ensure_ascii=False, indent=1))
        return 0
    A = doc["direction_A_information"]["theorem_A1_zero_mutual_information"]
    C = doc["direction_C_robustness"]
    print("== 方向 A：聚合层漂移的信息论不可见性 ==")
    inst = A["instance_accounting_E2"]
    print(f"  E2 记账漂移：X 相同、聚合移动 {inst['aggregate_move_pp']}pp "
          f"（unaware {inst['unaware_verdicts']} → aware {inst['aware_verdicts']}）")
    la = A["instance_label_axis"]
    print(f"  标签轴：{la['n_partitions']} 个划分 → {la['n_distinct_share_high_blind']} 个不同"
          f"「>50% 盲组占比」值，ambiguity factor {round(la['ambiguity_factor_share_stat'],4)}"
          f"（与论文的 15/4=3.75 同口径）")
    print("== 方向 C：崩溃点/影响函数 ==")
    print(f"  捕获者个数直方图（0..6）：{C['catch_count_histogram']}")
    print(f"  独苗份额 {C['shares_pct']['unique_catch_share']}%；"
          f"恰 2 捕获份额 {C['shares_pct']['exactly_2_share']}%；"
          f"恰 4 捕获份额 {C['shares_pct']['exactly_4_share']}%")
    print(f"  基率 {C['rates_pct']}")
    print(f"  定理 C1 恒等式（Δ = −crit_t(a)/n，三条规则 × 6 资产全部精确成立）："
          f"{C['checks']['theorem_C1_identity_holds_for_all_3_rules']}")
    for rname, v in C["relative_influence"].items():
        print(f"  {rname:<12} 最大单资产绝对影响 {v['max_abs_delta_pp']:+}pp，"
              f"相对影响 {v['relative_influence_pct']}%")
    print(f"  mean 单资产权重 1/m = {C['mean']['single_asset_weight']}；"
          f"加零产资产稀释 8/6 = {C['mean']['dilution_add_zero_yield']}")
    print(f"wrote {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
