#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""sample_size_671b.py — 671b D2：样本量现算器（ablation 版）。

与 669d 的分工
==============
* `research/669d_统计口径.md` §4 给的是**单比例 CI 半宽 → n** 的换算
  （"±10pp 需 n≈93–104"，纯 Clopper–Pearson 反解）。
* 本文件补的是 **ablation 真正需要的那两类量**：
  ① **独立两比例**：检出 Δ=15pp 需要每组多少 n（两臂不同样本）；
  ② **配对 McNemar**：同批 X 前后对比需要多少"对"（取决于不一致对比例 ψ）。

这两类量 `stat_bounds.py` 里没有（它只有 `n_for_upper_bound_zero` / `n_for_proportion`
这类**单比例**换算），所以必须新建——但**原语复用** `ablation_stats_671b.py`，
保证口径单一来源（669d §2.1「禁止从产物抄数」）。

为什么"现算"而不是抄表
====================
670b 设计 §2.3 的表里给了 ≈167 / ≈93 / ≈373 / ≈102–172 等数；本工具**现场重算**这些数，
并把"表里的值与现算值的差"如实登记（`drift_vs_doc`）。若哪天公式或参数变了，
本工具的输出会变，而**表格不会** —— 这正是 669d G-RATE-CONSISTENCY 要抓的形态。

用法
====
    python tools/sample_size_671b.py                 # 打印（现算）
    python tools/sample_size_671b.py --run           # 落盘 data/experiments/sample_size_671b.json
    python tools/sample_size_671b.py --check         # 自检（只读）
    python tools/sample_size_671b.py --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))

import ablation_stats_671b as AS  # noqa: E402
import stat_bounds as sb  # noqa: E402

VERSION = "1.0"
OUT = ROOT / "data" / "experiments" / "sample_size_671b.json"
DOC = "research/670b_ablation设计.md"

#: 670b §2.3 表里登记的"文档值"，用于现算 vs 文档的漂移登记（**不是**信源）
DOC_TWO_PROP = {(0.35, 0.50): 167, (0.35, 0.55): 93, (0.35, 0.45): 373, (0.50, 0.65): 167}
DOC_MCNEMAR = {(0.35, 0.50, 0.30): 102, (0.35, 0.50, 0.40): 137, (0.35, 0.50, 0.50): 172}

#: 论文主指标当前的可测 n（671a 扩样后，来自 reveal_update_671a.json；
#: 用于"当前 vs 目标"的差距登记。16/32/40 是扩样前旧值，已作废）
CURRENT_N = {"holdout_measurable": 21, "corpus_measurable": 48, "corpus_all": 60}


def two_proportion_table() -> list[dict]:
    """① 独立两比例：各目标 Δ 下所需 n/组（power=0.80, α=0.05 双侧）。"""
    rows = []
    for (p1, p2), doc_n in sorted(DOC_TWO_PROP.items()):
        r = AS.sample_size_two_proportions(p1, p2, power=0.80, alpha=0.05)
        rows.append({
            "p1": p1, "p2": p2, "delta_pp": round((p2 - p1) * 100, 1),
            "n_per_group": r["n_per_group"], "n_total": r["n_total"],
            "doc_value": doc_n, "drift_vs_doc": r["n_per_group"] - doc_n,
            "formula": r["method"],
        })
    return rows


def mcnemar_table() -> list[dict]:
    """② 配对 McNemar：Δ=15pp 下，各不一致对比例 ψ 所需的对数 n。"""
    rows = []
    for (p1, p2, psi), doc_n in sorted(DOC_MCNEMAR.items()):
        r = AS.sample_size_paired_mcnemar(p1, p2, psi, power=0.80, alpha=0.05)
        rows.append({
            "p1": p1, "p2": p2, "psi": psi, "delta_pp": round((p2 - p1) * 100, 1),
            "n_pairs": r["n_pairs"],
            "doc_value": doc_n, "drift_vs_doc": r["n_pairs"] - doc_n,
            "formula": r["method"],
        })
    return rows


def ci_halfwidth_table() -> list[dict]:
    """③ 单比例 CI 半宽 → n（与 669d §4 同口径，用 stat_bounds 现算，作交叉核对）。"""
    rows = []
    for n in (21, 30, 40, 48, 60, 93, 104, 150, 200):
        lo, hi = sb.cp_interval(n // 2, n)          # p=0.5 最坏情形
        rows.append({"n": abs(n), "p_assumed": 0.5,
                     "halfwidth_pp": round((hi - lo) / 2 * 100, 1)})
    return rows


def current_gap(target_halfwidth_pp: float = 10.0) -> dict:
    """④ 当前样本量 vs 目标的差距（诚实登记，不粉饰）。"""
    # 目标：p≈0.5 时 CP 半宽 ≤ 10pp ⇒ 反解最小 n
    n = 1
    while n < 5000:
        lo, hi = sb.cp_interval(n // 2, n)
        if (hi - lo) / 2 * 100 <= target_halfwidth_pp:
            break
        n += 1
    return {
        "target_halfwidth_pp": target_halfwidth_pp,
        "n_needed_for_target": n,
        "current": dict(CURRENT_N),
        "gap": {k: n - v for k, v in CURRENT_N.items()},
        "verdict": f"当前可测 n={min(CURRENT_N.values())} ⇒ 远不足以支撑 ±{target_halfwidth_pp}pp 结论",
    }


def power_curve() -> list[dict]:
    """⑤ 效力曲线：给定 n，能检出的最小 Δ（两比例，power=0.80）。"""
    rows = []
    for n in (21, 48, 64, 96, 128, 172, 256, 392):
        # 二分反解：找最小 Δ 使 sample_size ≤ n
        lo, hi = 0.005, 0.5
        for _ in range(60):
            mid = (lo + hi) / 2
            try:
                need = AS.sample_size_two_proportions(0.35, 0.35 + mid)["n_per_group"]
            except ValueError:
                need = 10 ** 9
            if need <= n:
                hi = mid
            else:
                lo = mid
        rows.append({"n_per_group": n, "min_detectable_delta_pp": round(hi * 100, 1)})
    return rows


def run() -> dict:
    return {
        "schema": "queyi-sample-size/671b",
        "version": VERSION,
        "design_doc": DOC,
        "params": {"power": 0.80, "alpha": 0.05, "sided": "two-sided"},
        "two_proportions": two_proportion_table(),
        "paired_mcnemar": mcnemar_table(),
        "ci_halfwidth": ci_halfwidth_table(),
        "current_gap": current_gap(),
        "power_curve": power_curve(),
        "note": "所有数字**现算**（原语复用 tools/ablation_stats_671b.py + tools/stat_bounds.py）；"
                "doc_value 只是 670b §2.3 表里的登记值，用于登记漂移，**不是信源**。",
        "red_lines": [
            "样本量达标前，ablation 结果只能作**方向性读法**，不得写『显著优于』（670b §2.3）",
            "当前可测 n=21/48 仍远低于 ±10pp 所需 n ⇒ 本批仍不作任何幅度 Claim",
        ],
    }


def summary(r: dict) -> str:
    L = ["=== 671b 样本量现算（power=0.80, α=0.05 双侧）===", ""]
    L.append("① 独立两比例（需要 n/组）")
    for x in r["two_proportions"]:
        L.append(f"   Δ={x['delta_pp']:>4}pp  {x['p1']:.2f}→{x['p2']:.2f}  "
                 f"n/组={x['n_per_group']:>4}  (文档 {x['doc_value']}, 漂移 {x['drift_vs_doc']:+d})")
    L.append("")
    L.append("② 配对 McNemar（Δ=15pp；ψ=不一致对比例）")
    for x in r["paired_mcnemar"]:
        L.append(f"   ψ={x['psi']:.2f}  n 对={x['n_pairs']:>4}  "
                 f"(文档 {x['doc_value']}, 漂移 {x['drift_vs_doc']:+d})")
    L.append("")
    g = r["current_gap"]
    L.append(f"④ 目标 ±{g['target_halfwidth_pp']}pp ⇒ n≈{g['n_needed_for_target']}；"
             f"当前 holdout={g['current']['holdout_measurable']} / "
             f"corpus={g['current']['corpus_measurable']} ⇒ 缺口 {g['gap']}")
    return "\n".join(L)


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    r = run()
    chk("四张表非空", all(r[k] for k in
                          ("two_proportions", "paired_mcnemar", "ci_halfwidth", "power_curve")))
    # 独立两比例：Δ 越小 n 越大
    tp = sorted(r["two_proportions"], key=lambda x: x["delta_pp"])
    ns = [x["n_per_group"] for x in tp]
    chk("独立：Δ 越小所需 n 越大", ns == sorted(ns, reverse=True), f"({ns})")
    # 文档漂移应在合理范围（±15%）
    for x in r["two_proportions"]:
        rel = abs(x["drift_vs_doc"]) / max(1, x["doc_value"])
        chk(f"独立 Δ={x['delta_pp']}pp 与文档漂移 <15%", rel < 0.15,
            f"({x['drift_vs_doc']:+d}, {rel:.1%})")
    # 配对：ψ 越大 n 越大
    pm = sorted(r["paired_mcnemar"], key=lambda x: x["psi"])
    nps = [x["n_pairs"] for x in pm]
    chk("配对：ψ 越大所需 n 越大", nps == sorted(nps), f"({nps})")
    for x in r["paired_mcnemar"]:
        rel = abs(x["drift_vs_doc"]) / max(1, x["doc_value"])
        chk(f"配对 ψ={x['psi']} 与文档漂移 <15%", rel < 0.15,
            f"({x['drift_vs_doc']:+d}, {rel:.1%})")
    # CI 半宽：n 越大半宽越小
    hw = [x["halfwidth_pp"] for x in r["ci_halfwidth"]]
    chk("CI 半宽随 n 单调下降", hw == sorted(hw, reverse=True), f"({hw})")
    # 目标 n 与 669d 的 93–104 一致
    n_t = r["current_gap"]["n_needed_for_target"]
    chk("±10pp 目标 n ∈ [90,110]（与 669d §4 一致）", 90 <= n_t <= 110, f"({n_t})")
    # 当前缺口为正
    chk("当前样本量低于目标（缺口为正）",
        all(v > 0 for v in r["current_gap"]["gap"].values()),
        f"({r['current_gap']['gap']})")
    # 效力曲线：n 越大，可检出 Δ 越小
    md = [x["min_detectable_delta_pp"] for x in r["power_curve"]]
    chk("效力曲线：n 越大可检出 Δ 越小", md == sorted(md, reverse=True), f"({md})")
    # 红线
    chk("红线含『不得写显著优于』", any("显著优于" in x for x in r["red_lines"]))
    chk("schema 正确", r["schema"] == "queyi-sample-size/671b")
    print(f"sample_size_671b selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671b 样本量现算器（ablation 版）")
    ap.add_argument("--run", action="store_true", help="落盘 data/experiments/sample_size_671b.json")
    ap.add_argument("--check", action="store_true", help="自检（只读）")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    r = run()
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=2))
    else:
        print(summary(r))
    if a.run:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(r, ensure_ascii=False, indent=2) + "\n",
                       encoding="utf-8", newline="\n")
        print(f"[671b] 已写 {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
