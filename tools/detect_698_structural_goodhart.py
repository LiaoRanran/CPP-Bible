#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""detect_698_structural_goodhart.py — 698-A：四型结构性 Goodhart 的统一风险评分器。

输入：一个**评估系统的原始输出 + 元数据**（JSON，格式见下），
输出：四型风险评分（0–100）+ 逐型早期预警信号。

输入格式（``--spec``，或 ``--demo-queyi`` 用仓库内冻结矩阵）
=========================================================
```json
{
  "system": "my-evaluator",
  "declared_assets": ["a1", "a2", "..."],          // 声明的资产/组件全集
  "samples": [
    {"uid": "s1", "per_asset": {"a1": "catch", "a2": "miss"}, 
     "defect_type": "t1", "source_batch": "b1"}
  ],
  "environment": {
    "reference_assets": ["a1", "a2", ...],          // 参考口径（全能力）支持的资产
    "current_assets":   ["a2", ...]                 // 当前口径实际支持的资产
  },
  "denominator_rules": ["catch_over_catch_plus_miss", "catch_over_total"],
  "aggregation_rules": ["or_any", "mean_per_asset"],
  "label_vocabularies": ["defect_type", "source_batch"]   // 可选：多词表
}
```

四型风险的定义
==============
* **Type I（分母 / 构成）**：``100 × 表观增益中可归因于"池构成"的比例``
  —— 用"掺入零产资产后随机臂覆盖率的下降"占表观增益的比例来量。
* **Type II（环境）**：``100 × 报出的负例中被污染的比例``（参考口径下其实是正例）。
* **Type III（标签）**：``100 × (高盲类占比在词表间的极差) / 最大值``。
* **Type IV（聚合）**：``100 × 掺入零产资产后最敏感可用聚合口径的相对变化``。

每型附**早期预警信号**（可在没有配对实验时就发现的征兆）。

红线：``detect_calls = 0``；只读；产出只写 ``data/698_*``。

用法
====
    python tools/detect_698_structural_goodhart.py --demo-queyi
    python tools/detect_698_structural_goodhart.py --spec my_system.json --out data/698_risk_mysys.json
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

_log = get_logger("detect_698_structural_goodhart")

MATRIX_1147: Final[str] = "blindspot_676g_detection_matrix.json"
REF_692: Final[str] = "692_environment_paired_experiment.json"
OUT_JSON: Final[Path] = ROOT / "data" / "698_structural_goodhart_risk.json"
K: Final[int] = 4

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
# 输入
# ══════════════════════════════════════════════════════════════════════════
def _verdict(cell: Any) -> str:
    if isinstance(cell, dict):
        return str(cell.get("verdict", "unknown"))
    return str(cell) if cell is not None else "unknown"


def load_spec(path: Path) -> dict[str, Any]:
    spec: dict[str, Any] = json.loads(path.read_text(encoding="utf-8"))
    spec.setdefault("environment", {})
    spec.setdefault("denominator_rules", ["catch_over_catch_plus_miss"])
    spec.setdefault("aggregation_rules", ["or_any", "mean_per_asset"])
    return spec


def demo_queyi_spec() -> dict[str, Any]:
    """把 Queyi 的冻结矩阵包装成统一输入格式（**不跑 detect**）。"""
    doc = load_json_cached(DATA / MATRIX_1147)
    ref = load_json_cached(DATA / REF_692)
    part = ref["asset_partition"]
    samples = []
    for s in doc.get("samples", []):
        pa = {a: _verdict((s.get("per_asset") or {}).get(a, "unknown")) for a in part["all_assets"]}
        samples.append({
            "uid": str(s.get("uid") or ""),
            "per_asset": pa,
            "defect_type": str(s.get("defect_type") or "unknown"),
            "source_batch": str(s.get("source_batch") or "unknown"),
        })
    return {
        "system": "Queyi (C/C++ verification apparatus, 8 declared assets)",
        "declared_assets": list(part["all_assets"]),
        "samples": samples,
        "environment": {
            "reference_assets": list(part["E1_supported"]),
            "current_assets": list(part["E2_supported"]),
        },
        "denominator_rules": ["catch_over_catch_plus_miss", "catch_over_total"],
        "aggregation_rules": ["or_any", "mean_per_asset", "at_least_2_assets"],
        "label_vocabularies": ["defect_type", "source_batch"],
    }


# ══════════════════════════════════════════════════════════════════════════
# 工具
# ══════════════════════════════════════════════════════════════════════════
def catch_sets(spec: dict[str, Any]) -> dict[str, set[str]]:
    out: dict[str, set[str]] = {a: set() for a in spec["declared_assets"]}
    for s in spec["samples"]:
        for a, v in (s.get("per_asset") or {}).items():
            if _verdict(v) == "catch":
                out.setdefault(a, set()).add(str(s["uid"]))
    return out


def union_n(catch: dict[str, set[str]], pool: tuple[str, ...]) -> int:
    u: set[str] = set()
    for a in pool:
        u |= catch.get(a, set())
    return len(u)


def greedy_pool(catch: dict[str, set[str]], pool: tuple[str, ...], k: int) -> tuple[str, ...]:
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


def random_mean(catch: dict[str, set[str]], pool: tuple[str, ...], k: int) -> float:
    tot = cnt = 0
    for sub in combinations(pool, k):
        tot += union_n(catch, sub)
        cnt += 1
    return tot / cnt if cnt else 0.0


def zero_yield(catch: dict[str, set[str]], pool: tuple[str, ...]) -> list[str]:
    return [a for a in pool if not catch.get(a, set())]


# ══════════════════════════════════════════════════════════════════════════
# 四型风险
# ══════════════════════════════════════════════════════════════════════════
def risk_type_i(spec: dict[str, Any], catch: dict[str, set[str]]) -> dict[str, Any]:
    """构成 / 分母风险：表观增益中有多少来自"池里掺了零产资产"。"""
    n = len(spec["samples"])
    pool = tuple(spec["declared_assets"])
    productive = tuple(a for a in pool if catch.get(a))
    z = zero_yield(catch, pool)
    g_now = (union_n(catch, greedy_pool(catch, pool, K)) - random_mean(catch, pool, K)) / n * 100.0
    g_clean = ((union_n(catch, greedy_pool(catch, productive, K))
                - random_mean(catch, productive, K)) / n * 100.0) if len(productive) >= K else 0.0
    share = (g_now - g_clean) / g_now if g_now > 0 else 0.0
    return {
        "risk_score": round(100.0 * max(0.0, min(1.0, share)), 2),
        "apparent_gain_now_pp": round(g_now, 4),
        "apparent_gain_after_removing_zero_yield_pp": round(g_clean, 4),
        "composition_share_of_gain": round(share, 6),
        "zero_yield_assets": z,
        "n_declared": len(pool),
        "n_productive": len(productive),
        "early_warning_signals": [
            "声明资产集中存在「恒 unknown / 零产出」组件（本项目：%s）" % (", ".join(z) or "无"),
            "随机基线臂的覆盖率对池大小高度敏感（掺资产即掉分）",
            "表观增益 > 非退化池增益的 2 倍（本项目 %.2f vs %.2f pp）" % (g_now, g_clean),
        ],
    }


def risk_type_ii(spec: dict[str, Any], catch: dict[str, set[str]]) -> dict[str, Any]:
    """环境风险：报出的负例中有多少在参考口径下其实是正例。"""
    env = spec["environment"]
    ref_assets = tuple(env.get("reference_assets") or spec["declared_assets"])
    cur_assets = tuple(env.get("current_assets") or spec["declared_assets"])
    lost = [a for a in ref_assets if a not in cur_assets]
    if not lost:
        return {"risk_score": 0.0, "poisoned_negatives": 0, "reported_negatives": 0,
                "poisoned_share": 0.0, "lost_assets": [],
                "early_warning_signals": ["当前口径与参考口径的资产集相同 ⇒ 无环境门控缺口"]}
    poisoned = 0
    reported_neg = 0
    for s in spec["samples"]:
        pa = {a: _verdict(v) for a, v in (s.get("per_asset") or {}).items()}
        cur_catch = any(pa.get(a) == "catch" for a in cur_assets)
        if cur_catch:
            continue
        reported_neg += 1
        if any(pa.get(a) == "catch" for a in lost):
            poisoned += 1
    share = poisoned / reported_neg if reported_neg else 0.0
    return {
        "risk_score": round(100.0 * share, 2),
        "poisoned_negatives": poisoned,
        "reported_negatives": reported_neg,
        "poisoned_share": round(share, 6),
        "lost_assets": lost,
        "early_warning_signals": [
            "参考口径支持但当前口径**未运行**的组件：%s" % ", ".join(lost),
            "报出的负例中有 %.2f%% 在参考口径下是正例" % (share * 100.0),
            "静默性：丢失的能力被写成 miss 而非 unknown（Δ_unknown = 0）",
        ],
    }


def risk_type_iii(spec: dict[str, Any], catch: dict[str, set[str]]) -> dict[str, Any]:
    """标签风险：高盲类占比在不同词表间的摆动幅度。"""
    caught: set[str] = set()
    for a in spec["declared_assets"]:
        caught |= catch.get(a, set())

    def _share(keyfn: Any, name: str) -> dict[str, Any]:
        grp: dict[str, list[int]] = defaultdict(list)
        for s in spec["samples"]:
            grp[str(keyfn(s))].append(0 if str(s["uid"]) in caught else 1)
        rates = {k: sum(v) / len(v) for k, v in grp.items()}
        hi = [k for k, r in rates.items() if r > 0.5]
        return {"vocabulary": name, "n_categories": len(grp),
                "n_high_blindspot": len(hi),
                "share_high_blindspot_pct": round(len(hi) / len(grp) * 100.0, 4),
                "macro_mean_blindspot_pct": round(sum(rates.values()) / len(rates) * 100.0, 4)}

    vocab: list[dict[str, Any]] = []
    for name in (spec.get("label_vocabularies") or ["defect_type"]):
        if name == "defect_type":
            vocab.append(_share(lambda s: s.get("defect_type", "unknown"), "defect_type"))
        elif name == "source_batch":
            vocab.append(_share(lambda s: s.get("source_batch", "unknown"), "source_batch"))
        elif name == "family":
            vocab.append(_share(
                lambda s: FAMILY_OF.get(str(s.get("defect_type")), "language_oop"), "family"))
    vocab.append(_share(
        lambda s: f"{s.get('defect_type')}@{s.get('source_batch')}", "defect_type_x_source_batch"))

    shares = [v["share_high_blindspot_pct"] for v in vocab]
    spread = (max(shares) - min(shares)) if shares else 0.0
    rel = spread / max(shares) if shares and max(shares) > 0 else 0.0
    return {
        "risk_score": round(100.0 * rel, 2),
        "vocabularies": vocab,
        "share_spread_pp": round(spread, 4),
        "relative_spread": round(rel, 6),
        "monotone_in_granularity": _is_monotone(vocab),
        "early_warning_signals": [
            "同一批裁决在不同词表下给出 %.2f pp 的「高盲类占比」摆动" % spread,
            "细粒度词表未必给出更高占比（本项目单调性 = %s）" % _is_monotone(vocab),
            "存在单样本类（类别数虚高，占比被稀释）",
        ],
    }


def _is_monotone(vocab: list[dict[str, Any]]) -> bool:
    ordered = sorted(vocab, key=lambda v: v["n_categories"])
    sh = [v["share_high_blindspot_pct"] for v in ordered]
    return all(sh[i] <= sh[i + 1] for i in range(len(sh) - 1)) or \
        all(sh[i] >= sh[i + 1] for i in range(len(sh) - 1))


def risk_type_iv(spec: dict[str, Any], catch: dict[str, set[str]]) -> dict[str, Any]:
    """聚合风险：不增加任何能力就能改变报告值的幅度。"""
    n = len(spec["samples"])
    pool = tuple(spec["declared_assets"])
    productive = tuple(a for a in pool if catch.get(a))
    phantoms = tuple(f"__phantom_{i}" for i in range(3))
    padded = dict(catch)
    for p in phantoms:
        padded[p] = set()

    def agg(rule: str, pool_: tuple[str, ...], cs: dict[str, set[str]]) -> float:
        if rule == "or_any":
            return union_n(cs, pool_) / n * 100.0
        if rule == "mean_per_asset":
            return sum(len(cs.get(a, set())) for a in pool_) / (len(pool_) * n) * 100.0
        if rule == "max_asset":
            return max(len(cs.get(a, set())) for a in pool_) / n * 100.0
        if rule == "at_least_2_assets":
            cnt: Counter[str] = Counter()
            for a in pool_:
                for uid in cs.get(a, set()):
                    cnt[uid] += 1
            return sum(1 for v in cnt.values() if v >= 2) / n * 100.0
        raise ValueError(rule)

    rows: list[dict[str, Any]] = []
    for rule in (spec.get("aggregation_rules") or ["or_any", "mean_per_asset"]):
        v0 = agg(rule, productive, catch)
        v1 = agg(rule, productive + phantoms, padded)
        rows.append({"rule": rule, "value_pct": round(v0, 4),
                     "value_after_padding_3_zero_yield_pct": round(v1, 4),
                     "manipulability_pp": round(abs(v1 - v0), 4),
                     "manipulability_relative": round(abs(v1 - v0) / v0, 6) if v0 else 0.0})
    worst = max(rows, key=lambda r: r["manipulability_relative"])
    return {
        "risk_score": round(100.0 * min(1.0, worst["manipulability_relative"]), 2),
        "aggregation_table": rows,
        "most_manipulable_rule": worst["rule"],
        "most_robust_rule": min(rows, key=lambda r: r["manipulability_relative"])["rule"],
        "early_warning_signals": [
            "聚合口径含**平均/求和**类运算 ⇒ 对掺入零产组件敏感（%s：%.2f%%）"
            % (worst["rule"], worst["manipulability_relative"] * 100.0),
            "若报告值可在**不增加任何有效能力**的前提下被改变 ⇒ 存在 Type IV 漂移",
            "OR / max 类口径对零产组件免疫（可操纵性 0）",
        ],
    }


# ══════════════════════════════════════════════════════════════════════════
def score(spec: dict[str, Any]) -> dict[str, Any]:
    catch = catch_sets(spec)
    t1 = risk_type_i(spec, catch)
    t2 = risk_type_ii(spec, catch)
    t3 = risk_type_iii(spec, catch)
    t4 = risk_type_iv(spec, catch)
    scores = {"type_I_composition": t1["risk_score"], "type_II_environment": t2["risk_score"],
              "type_III_label": t3["risk_score"], "type_IV_aggregation": t4["risk_score"]}
    return {
        "schema": "queyi-698/structural-goodhart-risk/v1",
        "generated_by": "tools/detect_698_structural_goodhart.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detect_calls": 0,
        "system": spec.get("system", "unnamed"),
        "n_samples": len(spec["samples"]),
        "risk_scores": scores,
        "overall_max_risk": max(scores.values()),
        "overall_mean_risk": round(sum(scores.values()) / len(scores), 2),
        "overall_verdict": _verdict_of(max(scores.values())),
        "details": {"type_I_composition": t1, "type_II_environment": t2,
                    "type_III_label": t3, "type_IV_aggregation": t4},
        "honest_note": (
            "四型风险分是**启发式**指标（0–100），不是统计检验。"
            "它们回答「这个评估系统的报告值有多少可被口径操作改变」，"
            "不回答「报告值是否正确」——后者需要参考口径的实测（697 定理 A1）。"
        ),
    }


def _verdict_of(score: float) -> str:
    if score >= 50:
        return "HIGH：报告值的一半以上可被口径操作改变，必须补齐口径声明与配对重测"
    if score >= 25:
        return "MEDIUM：存在实质性口径敏感性，建议做配对实验并随数字声明口径"
    if score > 0:
        return "LOW：口径敏感性有限，但需登记到报告规范里"
    return "NONE：四型口径敏感性均为 0（罕见，需复核输入是否完整）"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="698-A 四型结构性 Goodhart 风险评分")
    ap.add_argument("--spec", type=Path, help="输入评估系统描述 JSON")
    ap.add_argument("--demo-queyi", action="store_true", help="用仓库内 Queyi 冻结矩阵演示")
    ap.add_argument("--out", type=Path, default=OUT_JSON)
    args = ap.parse_args(argv)

    if args.demo_queyi or args.spec is None:
        spec = demo_queyi_spec()
        _log.info("使用 Queyi 演示输入（%d 样本）", len(spec["samples"]))
    else:
        spec = load_spec(args.spec)
        _log.info("载入 %s（%d 样本）", args.spec, len(spec["samples"]))

    doc = score(spec)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
    _log.info("已写出 %s", args.out)

    print(f"== 四型结构性 Goodhart 风险评分：{doc['system']} ==")
    for k, v in doc["risk_scores"].items():
        print(f"  {k:<24} {v:>6.2f} / 100")
    print(f"  {'总体（取最大）':<24} {doc['overall_max_risk']:>6.2f} / 100   "
          f"均值 {doc['overall_mean_risk']}")
    print(f"  ⇒ {doc['overall_verdict']}")
    print("\n  早期预警信号：")
    for k, v in doc["details"].items():
        for s in v["early_warning_signals"][:2]:
            print(f"    [{k}] {s}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
