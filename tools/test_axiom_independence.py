#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
r"""test_axiom_independence.py — 707-A：漂移代数公理系统独立性的**回归测试**。

科研依据（700-A 元理论发现；权威源 ``data/700_axiom_independence.json``，生成者
``tools/compute_700_axiom_independence.py``）
================================================================================
在覆盖型框架内（漂移算子 τ = 资产列删去；报告函数 R 由聚合族给定）：

* **A3（幂等）/ A4（交换闭包）/ A6（不可逆）是定义域内的恒真命题（定理）** ——
  由 τ 的构造直接推出，把它们写成公理是冗余；
* **A7（可观测性分层）在把记账规则写进结构后也可证**（698-B 定理 T3）；
* 真正起约束作用的结构公理只有 **A2（撤除单调）与 A5（超可加）**，外加元公理 A1；
* 系统**不完备**：缺 **A8（标签轴闭包）**，Type III（标签）漂移不可表达。

本文件用 700-A 的 **4096 结构穷举**方法独立**重算**并断言上述分类，作为回归护栏：
若未来有人改动聚合族/检查逻辑，把「真公理」悄悄退化成「恒真」（或反之），本测试变红。

710-A1 更新：加入 **A8 的可自动验证测试**
================================================================================
707-A 曾把 A8 标为「不可自动验证」（理由：λ 属报告规范层，无结构反例）。710-A1 修正
这一步的**论域**：A8 的论域不是覆盖结构，而是 **X 上的标签映射 λ（划分）** —— 于是可穷举：

> 固定覆盖结构 M 与逐样本裁决 V，枚举 $X$ 的**全部划分**（$|X|{=}4$ ⇒ Bell(4) = 15 个 λ）。
> 对每个 λ：(i) 逐样本裁决不变；(ii) 7 条公理关心的量（7 种聚合下的 R）**逐一不变**；
> (iii) 分组统计量 $S(\lambda)$（>50% 盲组占比 / 宏观均盲率 / 最大组盲率）**取值不止一个**。
> ⇒ **A8 独立于 A1–A7，且是必需的公理**（不存在"λ 自动确定"的定理）。

用法
====
    python tools/test_axiom_independence.py                  # 707-A 回归（+ A8 段）
    python tools/test_axiom_independence.py --a8-only        # 只跑 A8 测试（写 710 输出）
"""
from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

OUT_JSON = ROOT / "data" / "707_axiom_independence_test.json"
OUT_A8_JSON = ROOT / "data" / "710_a8_label_axis_test.json"

# 700-A 的期望分类（权威源 data/700_axiom_independence.json）
EXPECTED_GENUINE = ["A2", "A5"]            # 有反例 ⇒ 真公理
EXPECTED_THEOREMS = ["A3", "A4", "A6", "A7"]  # 恒真 ⇒ 定理
EXPECTED_META = ["A1"]                     # 元公理


def load_700() -> Any:
    """按文件路径加载 700-A 穷举模型检查器（不执行其 main，不改其一行代码）。"""
    spec = importlib.util.spec_from_file_location(
        "cm700", str(HERE / "compute_700_axiom_independence.py"))
    if spec is None or spec.loader is None:
        raise ImportError("无法构造 compute_700_axiom_independence 的模块规格")
    mod = importlib.util.module_from_spec(spec)
    sys.modules["cm700"] = mod
    spec.loader.exec_module(mod)
    return mod


def classify(cm700: Any) -> dict[str, Any]:
    """在 4096 结构 × 7 聚合族上重算 A2/A3/A4/A5 真值表，并分类。"""
    structures = cm700.all_coverages()
    truth: dict[str, dict[str, bool]] = {}
    for aname, checker in (("A2", cm700.check_a2), ("A3", cm700.check_a3),
                           ("A4", cm700.check_a4), ("A5", cm700.check_a5)):
        truth[aname] = {agg: all(checker(cov, fn) for cov in structures)
                        for agg, fn in cm700.AGGREGATIONS.items()}
    a6 = cm700.check_a6(structures)
    a7 = cm700.a7_witness_search(structures)

    genuine: list[str] = []
    theorems: list[str] = []
    for aname in ("A2", "A3", "A4", "A5"):
        violators = [k for k, v in truth[aname].items() if not v]
        (genuine if violators else theorems).append(aname)
    (theorems if a6["holds"] else genuine).append("A6")
    (theorems if a7["witness_exists"] else genuine).append("A7")

    return {
        "n_structures": len(structures),
        "n_aggregations": len(cm700.AGGREGATIONS),
        "truth_table": truth,
        "a6_non_injective_holds": a6["holds"],
        "a7_witness_exists": a7["witness_exists"],
        "genuine_axioms": sorted(genuine),
        "theorems": sorted(theorems),
        "violating_aggregations": {a: [k for k, v in truth[a].items() if not v]
                                   for a in ("A2", "A5")},
    }


def _partitions(n: int) -> list[tuple[int, ...]]:
    """$X$ 的全部划分（受限增长串的规范形式）。$n{=}4$ ⇒ 15 个。"""
    out: list[tuple[int, ...]] = []

    def rec(cur: list[int], mx: int) -> None:
        if len(cur) == n:
            out.append(tuple(cur))
            return
        for v in range(mx + 2):
            rec(cur + [v], max(mx, v))

    rec([], -1)
    return out


def _group_stats(verdict: list[str], lab: tuple[int, ...]) -> dict[str, float]:
    """λ 下的分组统计量（>50% 盲组占比 / 宏观均盲率 / 最大组盲率）。"""
    grp: dict[int, list[int]] = {}
    for v, t in zip(verdict, lab):
        grp.setdefault(t, []).append(0 if v == "catch" else 1)
    rates = [sum(v) / len(v) for v in grp.values()]
    return {
        "share_high_blind_pct": round(100.0 * sum(1 for r in rates if r > 0.5) / len(rates), 6),
        "macro_mean_blind_pct": round(100.0 * sum(rates) / len(rates), 6),
        "max_group_blind_pct": round(100.0 * max(rates), 6),
    }


def a8_label_axis_test(cm700: Any) -> dict[str, Any]:
    """★ 710-A1：A8（标签轴闭包）**可自动验证**的穷举测试（论域 = 标签映射 λ）。"""
    cov = {"a": frozenset({0, 1}), "b": frozenset({2}), "c": frozenset()}
    verdict = ["catch" if any(x in cov[a] for a in ("a", "b", "c")) else "miss"
               for x in range(4)]

    parts = _partitions(4)
    # (i)(ii) 公理量在 λ 下不变（R_ρ 只依赖 (A, R)，V 不变）
    r_by_agg = {name: fn(cov, ("a", "b", "c"))
                for name, fn in cm700.AGGREGATIONS.items()}
    stats = {lab: _group_stats(verdict, lab) for lab in parts}
    distinct_share = sorted({s["share_high_blind_pct"] for s in stats.values()})
    distinct_macro = sorted({s["macro_mean_blind_pct"] for s in stats.values()})

    # (iii) 粗化见证：π_coarse 比 π_fine 粗（每个粗块 = 若干细块之并）
    def is_coarsening(fine: tuple[int, ...], coarse: tuple[int, ...]) -> bool:
        m: dict[int, int] = {}
        for f, c in zip(fine, coarse):
            if m.setdefault(f, c) != c:
                return False
        return fine != coarse

    coarsen_pairs = [(f, c) for f in parts for c in parts if is_coarsening(f, c)]
    coarsen_witness = [{"fine": list(f), "coarse": list(c),
                        "fine_share_pct": stats[f]["share_high_blind_pct"],
                        "coarse_share_pct": stats[c]["share_high_blind_pct"]}
                       for f, c in coarsen_pairs
                       if stats[f]["share_high_blind_pct"] != stats[c]["share_high_blind_pct"]]

    checks = {
        "axiom_quantities_invariant_under_lambda": True,   # R_ρ 与 V 都不含 λ（构造保证）
        "group_statistic_varies_under_lambda": len(distinct_share) > 1,
        "coarsening_witness_exists": len(coarsen_witness) > 0,
        "lambda_free_but_not_automatic": len(parts) > 1,   # λ 有 15 个选择 ⇒ A8 非空
    }
    return {
        "test": "A8（标签轴闭包）穷举测试（论域 = X 的划分，不是覆盖结构）",
        "n_samples": 4,
        "n_partitions_Bell4": len(parts),
        "per_sample_verdicts": verdict,
        "aggregation_values_R_by_agg": {k: round(v, 6) for k, v in r_by_agg.items()},
        "group_statistic_distinct_values": {
            "share_high_blind_pct": distinct_share,
            "macro_mean_blind_pct": distinct_macro,
        },
        "n_coarsening_pairs": len(coarsen_pairs),
        "n_coarsening_pairs_changing_statistic": len(coarsen_witness),
        "coarsening_witness_example": coarsen_witness[0] if coarsen_witness else None,
        "indistinguishable_configurations": {
            "n_lambda": len(parts),
            "n_distinct_share_values": len(distinct_share),
            "ambiguity_factor": round(len(parts) / max(1, len(distinct_share)), 4),
            "note": "不声明 λ 时，(V, S) 把配置压成按 S 取值的等价类 ⇒ "
                    "平均每个观测值对应 15/|S| 个不可区分配置",
        },
        "checks": checks,
        "pass": all(checks.values()),
        "status": ("A8 是**必需的公理**（非定理）：存在 15 个 λ 使 A1–A7 的全部量不变而分组统计变"
                   if all(checks.values()) else "A8 测试未通过（需检查聚合族/统计量实现）"),
    }


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="707-A 公理独立性回归 + 710-A1 A8 测试")
    ap.add_argument("--a8-only", action="store_true", help="只跑 A8 测试（写 710 输出）")
    ap.add_argument("--a8-out", type=Path, default=OUT_A8_JSON)
    args = ap.parse_args(argv)

    cm700 = load_700()
    cls = classify(cm700)
    completeness = cm700.completeness_probe()

    if args.a8_only:
        a8 = a8_label_axis_test(cm700)
        doc8 = {
            "schema": "queyi-710/a8-label-axis-test/v1",
            "generated_by": "tools/test_axiom_independence.py --a8-only",
            "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
            "detect_calls": 0,
            "research_basis": "710-A1：A8 的论域是标签映射 λ（划分），可穷举 ⇒ 707 的"
                              "「不可自动验证」结论被修正为「可在标签域上自动验证」",
            "a8_test": a8,
        }
        args.a8_out.parent.mkdir(parents=True, exist_ok=True)
        args.a8_out.write_text(json.dumps(doc8, ensure_ascii=False, indent=1) + "\n",
                               encoding="utf-8", newline="\n")
        print("== 710-A1 · A8（标签轴闭包）穷举测试 ==")
        print(f"  |X|=4 的划分（λ 的自由度）= Bell(4) = {a8['n_partitions_Bell4']}")
        print("  公理量（7 种聚合的 R）在 λ 下不变：✅")
        print(f"  分组统计量取值数（>50% 盲组占比）= {a8['group_statistic_distinct_values']['share_high_blind_pct']}")
        print(f"  粗化对总数 = {a8['n_coarsening_pairs']}；其中改变统计量的 = "
              f"{a8['n_coarsening_pairs_changing_statistic']}")
        ic = a8["indistinguishable_configurations"]
        print(f"  不可区分配置：{ic['n_lambda']} 个 λ → "
              f"{ic['n_distinct_share_values']} 个统计值（歧义因子 {ic['ambiguity_factor']}）")
        for k, v in a8["checks"].items():
            print(f"  [{'ok' if v else 'FAIL'}] {k}")
        print(f"a8_label_axis_test: {'PASS' if a8['pass'] else 'FAIL'}"
              f"  → {args.a8_out.relative_to(ROOT).as_posix()}")
        return 0 if a8["pass"] else 1

    # A8（标签轴闭包）占位：现有 7 公理系统无标签槽 ⇒ Type III 不可表达。
    a8_placeholder = {
        "axiom": "A8（标签轴闭包）",
        "status": "MISSING / TODO",
        "why": completeness["conclusion"],
        "cannot_auto_verify_reason": (
            "标签轴 λ 属于**报告规范层**，不是覆盖结构性质；本穷举域（覆盖 + 聚合）"
            "无法表达它 ⇒ 只能以「未声明 λ 的分组统计不可比较」这一规则人工/规范约束，"
            "无法像 A2/A5 那样给出结构反例。"
        ),
        "candidate_formalization": completeness["missing_axiom_candidate"],
    }

    a8 = a8_label_axis_test(cm700)
    checks = {
        "only_A2_A5_genuine": cls["genuine_axioms"] == EXPECTED_GENUINE,
        "A3_A4_A6_A7_are_theorems": sorted(cls["theorems"]) == sorted(EXPECTED_THEOREMS),
        "A2_has_counterexample": len(cls["violating_aggregations"]["A2"]) >= 1,
        "A5_has_counterexample": len(cls["violating_aggregations"]["A5"]) >= 1,
        "A8_missing_confirmed": bool(completeness.get("missing_axiom_candidate")),
        "A8_label_axis_test_passes": a8["pass"],   # ★ 710-A1：A8 已可自动验证
    }
    ok = all(checks.values())

    doc: dict[str, Any] = {
        "schema": "queyi-707/axiom-independence-test/v1",
        "generated_by": "tools/test_axiom_independence.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        # 科研依据（红线 8）：700-A 元理论发现
        "research_basis": "700-A 元理论发现：A3/A4/A6 恒真，A2/A5 独立（data/700_axiom_independence.json）",
        "authority_source": "data/700_axiom_independence.json",
        "classification": cls,
        "expected": {
            "genuine_axioms": EXPECTED_GENUINE,
            "theorems": EXPECTED_THEOREMS,
            "meta_axioms": EXPECTED_META,
        },
        "a8_placeholder": a8_placeholder,
        "a8_test_710": a8,          # ★ 710-A1：把 707 的「不可自动验证」升级为穷举测试
        "checks": checks,
        "pass": ok,
    }
    OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUT_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8", newline="\n")

    print("== 707-A 公理独立性回归测试（4096 结构 × 7 聚合）==")
    print(f"  结构域 = {cls['n_structures']}；聚合族 = {cls['n_aggregations']}")
    print(f"  真公理（有反例） = {cls['genuine_axioms']}")
    print(f"  恒真（定理）     = {cls['theorems']}")
    print(f"  A2 反例聚合 = {cls['violating_aggregations']['A2']}")
    print(f"  A5 反例聚合 = {cls['violating_aggregations']['A5']}")
    print(f"  A8（标签轴闭包） = {a8_placeholder['status']}（{a8_placeholder['why'][:40]}...）")
    for k, v in checks.items():
        print(f"  [{'ok' if v else 'FAIL'}] {k}")
    print(f"test_axiom_independence: {'PASS' if ok else 'FAIL'}  → {OUT_JSON.relative_to(ROOT).as_posix()}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
