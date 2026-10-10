#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
r"""compute_715_equal_marginal_factorial.py — 715 Part 4：F1 增益的**实验性**（2^4 全因子）分解。

背景
====
710-C 把 F1 的头条 $+24.03$pp 观测性地分解为四步：
    $+24.03 \to +14.48\;(\text{期望口径},-9.55) \to +6.21\;(\text{去两个零产资产},-8.27)
     \to +1.55\;(\text{去 linker},-4.65) \to +12.30\;(k{=}4{\to}1,+10.74)$
但这条链是**观测性的**：一次只动一个旋钮、顺序固定、且四个旋钮不独立（710-C 自己登记了
"order-dependent"）。评审的问题很直接：**你怎么证明这些分量是因果的，而不是相关的？**

本脚本用**等边际替换设计（equal-marginal substitution design）**在**同一冻结矩阵**上做
$2^{4}=16$ 全因子实验：四个二元因子同时取值，每个格子测量同一标量（选择增益 $\Delta$），
于是**主效应与交互效应都可以被分离**（而不是像序贯分解那样把交互项全塞进最后一步）。

四个因子（任务卡定义）
======================
| 记号 | 因子 | 取值 |
|---|---|---|
| $A$ | 记账口径 accounting | `naive`（分母 = 全部样本，unknown 当 miss） vs `aware`（分母 = catch+miss，unknown 剔出） |
| $B$ | 资产池 pool | `full8`（8 资产） vs `noZ`（去掉两个结构上不可用的零产资产：wunsequenced、compile-time） |
| $C$ | linker（**控制槽位规模**） | `with` vs `without_slotctrl`（把 linker 换成一个**全 miss 的合成零产列**，$|\text{pool}|$ 与 $k$ 都不变，只移走 linker 的覆盖能力） |
| $D$ | 预算档位 $k$ | $k{=}1$ vs $k{=}4$ |

响应变量：$\Delta = R(S_{\text{sel}}) - \mathbb{E}[R(S_{\text{rand}})]$，
其中 $S_{\text{sel}}$ 是贪心（边际增益最大）选出的 $k$ 个资产，随机臂取
$\binom{|\text{pool}|}{k}$ 的**精确期望**（枚举，非抽样）。

红线
====
`detect_calls = 0`：只读 `data/a5_676f_detection_matrix.json`，不跑任何新检测，
不改冻结矩阵，不改论文。

用法
====
    python tools/compute_715_equal_marginal_factorial.py [--boot 400] [--out data/715_...json]
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import random
import statistics
import sys
from itertools import combinations
from pathlib import Path
from typing import Any, Final

ROOT = Path(__file__).resolve().parents[1]
A5: Final[Path] = ROOT / "data" / "a5_676f_detection_matrix.json"
OUT_JSON: Final[Path] = ROOT / "data" / "715_等边际替换_16组合结果.json"

POOL8: Final[tuple[str, ...]] = (
    "asan", "ubsan", "tsan", "compiler-warn", "wunsequenced", "cross-compile",
    "linker", "compile-time",
)
ZERO_YIELD: Final[tuple[str, ...]] = ("wunsequenced", "compile-time")
POOL6: Final[tuple[str, ...]] = tuple(a for a in POOL8 if a not in ZERO_YIELD)
ZERO_COL: Final[str] = "ZERO_cell"   # 合成零产列：全 miss，用于**控制槽位规模**

FACTORS: Final[tuple[tuple[str, tuple[str, ...]], ...]] = (
    ("accounting", ("naive", "aware")),
    ("pool", ("full8", "noZ")),
    ("linker", ("with", "without_slotctrl")),
    ("k", ("k1", "k4")),
)


# --------------------------------------------------------------------------
# 载入
# --------------------------------------------------------------------------
def load_rows(split: str | None) -> list[dict[str, Any]]:
    doc = json.loads(A5.read_text(encoding="utf-8"))
    out = []
    for s in doc["samples"]:
        if split is not None and s.get("split") != split:
            continue
        pa = s.get("per_asset") or {}
        out.append({a: (pa.get(a) if isinstance(pa.get(a), str) else "unknown") for a in POOL8}
                   | {ZERO_COL: "miss"})
    return out


# --------------------------------------------------------------------------
# 读数：OR 池化 + 两种记账
# --------------------------------------------------------------------------
def pooled(rows: list[dict[str, Any]], subset: tuple[str, ...]) -> list[str]:
    """每个样本在给定资产集下的 OR 池化裁决（catch / miss / unknown）。"""
    out = []
    for r in rows:
        v = "miss"
        for a in subset:
            x = r.get(a, "unknown")
            if x == "catch":
                v = "catch"
                break
            if x == "unknown":
                v = "unknown"
        out.append(v)
    return out


def rate(rows: list[dict[str, Any]], subset: tuple[str, ...], accounting: str) -> float:
    v = pooled(rows, subset)
    c = sum(1 for x in v if x == "catch")
    if accounting == "naive":
        return c / len(v) if v else 0.0
    den = c + sum(1 for x in v if x == "miss")
    return c / den if den else 0.0


def exact_random_mean(rows: list[dict[str, Any]], pool: tuple[str, ...], k: int,
                      accounting: str) -> float:
    subs = list(combinations(pool, k))
    if not subs:
        return 0.0
    return sum(rate(rows, s, accounting) for s in subs) / len(subs)


def greedy(rows: list[dict[str, Any]], pool: tuple[str, ...], k: int,
           accounting: str) -> tuple[str, ...]:
    """贪心（边际增益最大）= 684/698 的 FD 口径；目标函数与响应一致（同记账）。"""
    chosen: list[str] = []
    for _ in range(min(k, len(pool))):
        best, best_gain = None, -1.0
        for a in pool:
            if a in chosen:
                continue
            g = rate(rows, tuple(chosen) + (a,), accounting)
            if g > best_gain + 1e-15:
                best, best_gain = a, g
        if best is None:
            break
        chosen.append(best)
    return tuple(chosen)


def delta(rows: list[dict[str, Any]], pool: tuple[str, ...], k: int,
          accounting: str) -> dict[str, Any]:
    sel = greedy(rows, pool, k, accounting)
    r_sel = rate(rows, sel, accounting)
    r_rand = exact_random_mean(rows, pool, k, accounting)
    return {
        "selected": list(sel),
        "rate_selected_pct": round(100.0 * r_sel, 4),
        "rate_random_pct": round(100.0 * r_rand, 4),
        "delta_pp": round(100.0 * (r_sel - r_rand), 4),
    }


def cell(rows: list[dict[str, Any]], accounting: str, pool_name: str, linker: str,
         k_name: str) -> dict[str, Any]:
    pool = list(POOL8 if pool_name == "full8" else POOL6)
    if linker == "without_slotctrl":
        pool = [ZERO_COL if a == "linker" else a for a in pool]
    pool_t = tuple(pool)
    k = 1 if k_name == "k1" else 4
    d = delta(rows, pool_t, k, accounting)
    d.update({"pool_effective": list(pool_t), "k": k})
    return d


# --------------------------------------------------------------------------
# 2^4 因子分析（单次重复 ⇒ 用最高阶交互作误差项；另用 bootstrap 给效应区间）
# --------------------------------------------------------------------------
def yates_effects(values: list[float]) -> tuple[dict[str, float], float]:
    """返回 {效应名: 效应值} 与 4 阶交互（作误差项的 SS）。键按因子顺序排序。"""
    names = ["accounting", "pool", "linker", "k"]
    labels = []
    for mask in range(1, 16):
        lab = "+".join(names[i] for i in range(4) if mask & (1 << i))
        labels.append(lab)
    # 输入顺序：因子按 (accounting, pool, linker, k) 二进制展开，0 = 第一个取值
    y = list(values)
    assert len(y) == 16
    # Yates 算法
    work = list(y)
    n = 16
    step = 1
    while step < n:
        for i in range(0, n, step * 2):
            for j in range(i, i + step):
                a, b = work[j], work[j + step]
                work[j], work[j + step] = a + b, b - a
        step *= 2
    total = work[0]
    # work[1..15] 的顺序 = 二进制位序（第一位 = accounting）
    effects: dict[str, float] = {}
    for idx, lab in enumerate(labels, start=1):
        effects[lab] = round(work[idx] / 8.0, 4)   # 2^(4-1) = 8
    return effects, total


def ss_from_effect(eff: float, n_rep: int = 1) -> float:
    """单次重复：SS = contrast^2 / 2^4 = (effect * 2^3)^2 / 16 = effect^2 * 4。"""
    return (eff ** 2) * 4.0 / n_rep


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="715 等边际替换 2^4 全因子实验")
    ap.add_argument("--split", default="evaluation",
                    help="帧（evaluation = 566 帧，与 710-C/677c 同一帧；all = 1137）")
    ap.add_argument("--boot", type=int, default=300, help="bootstrap 重采样次数")
    ap.add_argument("--seed", type=int, default=7150)
    args = ap.parse_args(argv)

    rows_all = load_rows(None if args.split == "all" else args.split)
    n = len(rows_all)

    # ---- 16 组合（点估计）-------------------------------------------------
    order = [("naive", "full8", "with", "k4"), ("aware", "full8", "with", "k4"),
             ("naive", "noZ", "with", "k4"), ("aware", "noZ", "with", "k4"),
             ("naive", "full8", "without_slotctrl", "k4"),
             ("aware", "full8", "without_slotctrl", "k4"),
             ("naive", "noZ", "without_slotctrl", "k4"),
             ("aware", "noZ", "without_slotctrl", "k4"),
             ("naive", "full8", "with", "k1"), ("aware", "full8", "with", "k1"),
             ("naive", "noZ", "with", "k1"), ("aware", "noZ", "with", "k1"),
             ("naive", "full8", "without_slotctrl", "k1"),
             ("aware", "full8", "without_slotctrl", "k1"),
             ("naive", "noZ", "without_slotctrl", "k1"),
             ("aware", "noZ", "without_slotctrl", "k1")]
    # 上面的顺序即 Yates 需要的二进制顺序（accounting 最快、其次 pool、linker、k）

    cells = {}
    ys = []
    for acc, pool_name, link, kn in order:
        c = cell(rows_all, acc, pool_name, link, kn)
        c.update({"accounting": acc, "pool": pool_name, "linker": link, "k_level": kn})
        cells[f"{acc}|{pool_name}|{link}|{kn}"] = c
        ys.append(c["delta_pp"])

    effects, total = yates_effects(ys)

    # ★ 次级响应：同 16 格的**原始检出率**（选中集），用于与 710-C 的"linker 自身覆盖
    #   −0.4711pp"对账——Δ 上两臂同时失去 linker 覆盖，效应会部分抵消，只看 Δ 会低估。
    ys_sel = [cells[f"{a}|{p}|{lk}|{kn}"]["rate_selected_pct"] for a, p, lk, kn in order]
    effects_rate, _ = yates_effects(ys_sel)

    # ★ 退化格标记：aware 记账 + 含全 unknown 资产的完整池 ⇒ 分母塌缩（第 692 批的
    #   "反向分母病理"）。这类格的 rate 是构造性的 100%，必须在报告中单列。
    degenerate = [key for key, c in cells.items()
                  if c["accounting"] == "aware" and c["pool"] == "full8"]

    ss = {k: round(ss_from_effect(v), 4) for k, v in effects.items()}
    ss_total = round(sum(ss.values()), 4)
    err_key = "accounting+pool+linker+k"
    ss_err = ss[err_key]
    # 以 4 阶交互为误差（df=1）——单次重复下的惯用处置
    anova_rows = []
    for lab, v in effects.items():
        s = ss[lab]
        anova_rows.append({
            "term": lab,
            "effect_pp": v,
            "SS": s,
            "SS_share_pct": round(100.0 * s / ss_total, 2) if ss_total else 0.0,
            "F_vs_4way": round(s / ss_err, 3) if ss_err > 0 else None,
        })
    anova_rows.sort(key=lambda r: -r["SS"])

    # ---- bootstrap：重采样样本，重算 16 格，得到每个效应的分布 ------------
    rng = random.Random(args.seed)
    boot_eff: dict[str, list[float]] = {k: [] for k in effects}
    for _ in range(args.boot):
        idx = [rng.randrange(n) for _ in range(n)]
        sub = [rows_all[i] for i in idx]
        yy = []
        for acc, pool_name, link, kn in order:
            pool = list(POOL8 if pool_name == "full8" else POOL6)
            if link == "without_slotctrl":
                pool = [ZERO_COL if a == "linker" else a for a in pool]
            k = 1 if kn == "k1" else 4
            yy.append(delta(sub, tuple(pool), k, acc)["delta_pp"])
        e, _ = yates_effects(yy)
        for kk, vv in e.items():
            boot_eff[kk].append(vv)

    boot_summary = {}
    for kk, vals in boot_eff.items():
        vals = sorted(vals)
        lo = vals[int(0.025 * len(vals))]
        hi = vals[int(0.975 * len(vals)) - 1] if len(vals) > 1 else vals[0]
        boot_summary[kk] = {
            "mean_pp": round(statistics.fmean(vals), 4),
            "sd_pp": round(statistics.pstdev(vals), 4),
            "ci95_pp": [round(lo, 4), round(hi, 4)],
            "crosses_zero": bool(lo <= 0.0 <= hi),
        }

    # ---- 一个附加臂：期望口径效应（对应观测分解的第一步 −9.55pp）----------
    aux_rows = load_rows("evaluation") if args.split == "evaluation" else rows_all
    sel4 = greedy(aux_rows, POOL8, 4, "naive")
    r_sel = rate(aux_rows, sel4, "naive")
    r_rand_mean = exact_random_mean(aux_rows, POOL8, 4, "naive")
    # 单点随机抽取的期望值 = 精确期望（无偏），单点实现值随抽样波动 ⇒ 用 2000 次抽样给实现分布
    rng2 = random.Random(args.seed + 1)
    draws = []
    for _ in range(2000):
        s = tuple(rng2.sample(POOL8, 4))
        draws.append(100.0 * (r_sel - rate(aux_rows, s, "naive")))
    aux = {
        "frame": args.split,
        "n": len(aux_rows),
        "delta_vs_expectation_pp": round(100.0 * (r_sel - r_rand_mean), 4),
        "delta_single_draw_mean_pp": round(statistics.fmean(draws), 4),
        "delta_single_draw_p05_pp": round(sorted(draws)[int(0.05 * len(draws))], 4),
        "delta_single_draw_p95_pp": round(sorted(draws)[int(0.95 * len(draws)) - 1], 4),
        "delta_single_draw_max_pp": round(max(draws), 4),
        "gap_single_minus_expectation_pp": round(
            statistics.fmean(draws) - 100.0 * (r_sel - r_rand_mean), 4),
    }

    # ---- 敏感性：只用 naive 记账的 2^3（去掉退化格的影响）-----------------
    order_naive = [o for o in order if o[0] == "naive"]
    ys3 = [cells[f"{a}|{p}|{lk}|{kn}"]["delta_pp"] for a, p, lk, kn in order_naive]
    # 2^3 ≤ 用前 3 个因子做 Yates（去 accounting）
    names3 = ["pool", "linker", "k"]
    work = list(ys3)
    step = 1
    while step < 8:
        for i in range(0, 8, step * 2):
            for j in range(i, i + step):
                a_, b_ = work[j], work[j + step]
                work[j], work[j + step] = a_ + b_, b_ - a_
        step *= 2
    labels3 = ["+".join(names3[i] for i in range(3) if mask & (1 << i)) for mask in range(1, 8)]
    eff3 = {lab: round(work[i] / 4.0, 4) for i, lab in enumerate(labels3, start=1)}

    doc = {
        "schema": "queyi-715/equal-marginal-factorial/v1",
        "generated_by": "tools/compute_715_equal_marginal_factorial.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "source_matrix": "data/a5_676f_detection_matrix.json",
        "frame": {"split": args.split, "n": n},
        "design": {
            "type": "2^4 full factorial, equal-marginal substitution",
            "factors": {k: list(v) for k, v in FACTORS},
            "response": "Delta = rate(selected) - exact_expectation[rate(random)] (pp)",
            "slot_control": "removing linker substitutes an all-miss synthetic column (ZERO_cell) "
                            "so that |pool| and k are unchanged",
        },
        "cells": cells,
        "degenerate_cells": degenerate,
        "degeneracy_note": (
            "aware 记账 + full8 池：未捕获样本的池化裁决为 unknown（两个资产全 unknown）⇒ "
            "分母 catch+miss 塌缩为 catch ⇒ rate 构造性地 =100%。这是 692 批登记的"
            "『反向分母病理』，不是数值错误；该 4 格在解读 accounting 主效应时必须单列。"
        ),
        "yates_effects_pp": effects,
        "yates_effects_on_selected_rate_pp": effects_rate,
        "anova": {
            "note": "单次重复：效应 = contrast/8；SS = effect^2*4；F 以 4 阶交互为误差（df=1）",
            "SS_total": ss_total,
            "SS_error_term": err_key,
            "SS_error": ss_err,
            "rows": anova_rows,
        },
        "bootstrap": {"B": args.boot, "seed": args.seed, "by_term": boot_summary},
        "sensitivity_naive_only_2x2x2": {
            "note": "只取 naive 记账的 8 格（排除退化格），去 accounting 后的 2^3 效应",
            "effects_pp": eff3,
        },
        "aux_expectation_caliber": aux,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8", newline="\n")

    print(f"== 715 等边际替换 2^4 全因子（帧={args.split}, n={n}）==")
    for key, c in cells.items():
        print(f"  {key:46s} sel={c['rate_selected_pct']:7.3f}%  "
              f"rand={c['rate_random_pct']:7.3f}%  Δ={c['delta_pp']:+7.3f}pp")
    print("\n== 效应（Yates，pp）==")
    for lab, v in sorted(effects.items(), key=lambda kv: -abs(kv[1])):
        bs = boot_summary[lab]
        print(f"  {lab:34s} {v:+8.3f}  CI95 [{bs['ci95_pp'][0]:+.3f}, {bs['ci95_pp'][1]:+.3f}] "
              f"{'(跨零)' if bs['crosses_zero'] else ''}")
    print("\n== 原始检出率（选中集）的效应，pp（与 710-C 的 linker −0.4711pp 对账用）==")
    for lab, v in sorted(effects_rate.items(), key=lambda kv: -abs(kv[1])):
        print(f"  {lab:34s} {v:+8.3f}")
    print("\n== 敏感性：naive-only 2^3 效应，pp ==")
    for lab, v in sorted(eff3.items(), key=lambda kv: -abs(kv[1])):
        print(f"  {lab:20s} {v:+8.3f}")
    print(f"\n退化格（aware|full8）: {degenerate}")
    print(f"\n结果 → {OUT_JSON.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
