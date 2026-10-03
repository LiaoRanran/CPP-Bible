#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""blindspot_676g_analysis.py — 676g 任务 B：盲区比例统计。

输入  data/blindspot_676g_detection_matrix.json（merge 产物）
输出  data/blindspot_676g_stats.json

口径（与规格对齐 + 常见坑规避）
================================
* catch（样本级）= 8 资产中任一 catch。wunsequenced/compile-time 结构性恒 unknown
  （MinGW 不认 -Wunsequenced / 无本地检测器），永不 catch，故 8 资产 OR 与
  6 可用资产 OR 的 catch/miss/unknown 完全一致；per-asset 统计仍列出这两项并注明。
* miss（样本级）= 无任何 catch 且 ≥1 个可用资产给出确定 miss。
* unknown（样本级）= 可用 6 资产全部 unknown。
* 盲区比例 = (miss + unknown) / n，并单列 miss / unknown 以便区分"确定漏报"与"无法判定"。
* 批次层级、planted 分组、资产互补性（两两并集覆盖率）一并列出。
* planted=false（n=74）给 Wilson 95% CI；corpus(64) planted 字段缺失单列为 null 组。
"""
from __future__ import annotations

import datetime as _dt
import json
import math
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
MATRIX = HERE / "blindspot_676g_detection_matrix.json"
OUT = HERE / "blindspot_676g_stats.json"

AVAILABLE = ["asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker"]
ALL_ASSETS = AVAILABLE + ["wunsequenced", "compile-time"]

#: 缺陷类型 → 报告用家族（仅分组用，细粒度类型保留原始字符串）
FAMILY: dict[str, str] = {}
for t in ("memory_safety", "out_of_bounds", "null_pointer_deref", "uninitialized_read",
          "resource_leak", "heap_overread", "heap_overflow", "heap_underflow",
          "global_overflow", "stack_overflow", "stack_overflow_write", "stack_overread",
          "use_after_free", "double_free", "null_deref", "memory_leak", "type_confusion"):
    FAMILY[t] = "memory"
for t in ("MEM", "leak", "boundary", "memory"):
    FAMILY[t] = "memory"
for t in ("undefined_behavior", "integer_overflow", "type_punning", "other_ub",
          "division_by_zero", "pointer_overflow", "bit_operation", "optimization_dependent"):
    FAMILY[t] = "ub"
for t in ("UB",):
    FAMILY[t] = "ub"
for t in ("data_race", "race_condition", "memory_order", "atomic_ub", "aba_problem",
          "lock_priority_inversion", "condition_variable", "false_sharing",
          "CONC", "memory-order"):
    FAMILY[t] = "concurrency"
for t in ("iterator_invalidation", "stl_container_ub", "string_ub", "algorithm_misuse",
          "smart_pointer"):
    FAMILY[t] = "stl"
for t in ("alignment", "endianness", "volatile_misuse", "interrupt_safety",
          "register_ub", "timing_side_channel"):
    FAMILY[t] = "embedded_platform"
for t in ("move_semantics", "virtual_function", "lambda_capture", "raii_violation",
          "RAII/UB"):
    FAMILY[t] = "language_raii"
for t in ("cross_tu_ub", "ODR"):
    FAMILY[t] = "link_odr"
for t in ("logic_error", "state_machine", "infinite_loop", "resource_exhaustion",
          "info_leak", "conditional_trigger"):
    FAMILY[t] = "logic_semantic"
for t in ("API", "api"):
    FAMILY[t] = "api_misuse"
for t in ("historical", "unspecified", "perf", "control", "well-defined", "demo",
          "compiler-diff", "ambiguity", "compiler-bug", "compiler_warning"):
    FAMILY[t] = "other"


def wilson(p: float, n: int, z: float = 1.96) -> tuple[float, float]:
    if n == 0:
        return (None, None)
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return (round(max(0.0, c - h), 4), round(min(1.0, c + h), 4))


def main() -> int:
    doc = json.loads(MATRIX.read_text(encoding="utf-8"))
    samples = doc["samples"]
    n_total = len(samples)

    # ── 每样本聚合口径 ────────────────────────────────────────────────
    def sample_class(s: dict) -> str:
        vs = [s["per_asset"].get(a, {}).get("verdict") for a in AVAILABLE]
        if "catch" in vs:
            return "catch"
        if all(v == "unknown" for v in vs):
            return "unknown"
        if any(v == "MISSING" for v in vs):
            return "MISSING"
        return "miss"

    for s in samples:
        s["_class"] = sample_class(s)

    classes = [s["_class"] for s in samples]
    overall = {c: classes.count(c) for c in ("catch", "miss", "unknown", "MISSING")}

    # ── 1) 按缺陷类型 ────────────────────────────────────────────────
    by_type: dict[str, dict] = {}
    for s in samples:
        t = s["defect_type"]
        d = by_type.setdefault(t, {"n": 0, "catch": 0, "miss": 0, "unknown": 0,
                                   "batches": defaultdict(int),
                                   "asset_catch": defaultdict(int),
                                   "asset_miss": defaultdict(int),
                                   "evidence_miss": [], "evidence_catch": []})
        d["n"] += 1
        d["batches"][s["source_batch"]] += 1
        if s["_class"] in ("miss", "unknown"):
            d[s["_class"]] += 1
        elif s["_class"] == "catch":
            d["catch"] += 1
        for a in ALL_ASSETS:
            v = s["per_asset"].get(a, {}).get("verdict")
            if v == "catch":
                d["asset_catch"][a] += 1
            elif v == "miss":
                d["asset_miss"][a] += 1
        if s["_class"] in ("miss", "unknown") and len(d["evidence_miss"]) < 4:
            notes = {a: s["per_asset"].get(a, {}).get("note", "")[:120]
                     for a in AVAILABLE if s["per_asset"].get(a, {}).get("verdict") == "miss"}
            d["evidence_miss"].append({"uid": s["uid"], "batch": s["source_batch"],
                                       "class": s["_class"], "miss_notes": notes})
        if s["_class"] == "catch" and len(d["evidence_catch"]) < 2:
            caught = sorted(a for a in AVAILABLE
                            if s["per_asset"].get(a, {}).get("verdict") == "catch")
            d["evidence_catch"].append({"uid": s["uid"], "caught_by": caught})

    type_rows = []
    for t, d in by_type.items():
        blind = d["miss"] + d["unknown"]
        type_rows.append({
            "defect_type": t, "family": FAMILY.get(t, "other"),
            "n": d["n"], "catch": d["catch"], "miss": d["miss"],
            "unknown": d["unknown"],
            "blindspot_ratio": round(blind / d["n"], 4),
            "miss_ratio": round(d["miss"] / d["n"], 4),
            "unknown_ratio": round(d["unknown"] / d["n"], 4),
            "batches": dict(d["batches"]),
            "asset_catch": {a: d["asset_catch"].get(a, 0) for a in ALL_ASSETS},
            "asset_miss": {a: d["asset_miss"].get(a, 0) for a in AVAILABLE},
            "asset_catch_rate": {a: round(d["asset_catch"].get(a, 0) / d["n"], 4)
                                 for a in ALL_ASSETS},
            "evidence_miss": d["evidence_miss"], "evidence_catch": d["evidence_catch"],
        })
    type_rows.sort(key=lambda r: (-r["blindspot_ratio"], -r["n"]))
    for i, r in enumerate(type_rows, 1):
        r["rank"] = i
        if r["blindspot_ratio"] > 0.5:
            r["band"] = "high_blindspot(>50%)"
        elif r["blindspot_ratio"] >= 0.2:
            r["band"] = "partial_visibility(20-50%)"
        else:
            r["band"] = "low_blindspot(<20%)"

    # ── 2) 按资产 ────────────────────────────────────────────────────
    by_asset = {}
    for a in ALL_ASSETS:
        c = m = u = 0
        for s in samples:
            v = s["per_asset"].get(a, {}).get("verdict")
            if v == "catch":
                c += 1
            elif v == "miss":
                m += 1
            elif v == "unknown":
                u += 1
        by_asset[a] = {"n": n_total, "catch": c, "miss": m, "unknown": u,
                       "other": n_total - c - m - u,
                       "coverage_catch_rate": round(c / n_total, 4),
                       "note": doc.get("asset_availability", {}).get(a, "")}
    asset_rank = sorted(((a, v["coverage_catch_rate"]) for a, v in by_asset.items()),
                        key=lambda kv: -kv[1])

    # ── 3) 按批次 ────────────────────────────────────────────────────
    by_batch = {}
    for s in samples:
        b = s["source_batch"]
        d = by_batch.setdefault(b, {"n": 0, "catch": 0, "miss": 0, "unknown": 0,
                                    "asset_catch": defaultdict(int)})
        d["n"] += 1
        if s["_class"] in ("catch", "miss", "unknown"):
            d[s["_class"]] += 1
        for a in AVAILABLE:
            if s["per_asset"].get(a, {}).get("verdict") == "catch":
                d["asset_catch"][a] += 1
    for b, d in by_batch.items():
        d["blindspot_ratio"] = round((d["miss"] + d["unknown"]) / d["n"], 4)
        d["asset_catch"] = dict(d["asset_catch"])
        d["asset_catch_rate"] = {a: round(d["asset_catch"].get(a, 0) / d["n"], 4)
                                 for a in AVAILABLE}
        d.pop("asset_catch")

    # ── 4) 按 planted ────────────────────────────────────────────────
    def planted_key(s: dict) -> str:
        if s["planted"] is None:
            return "null"
        return "true" if s["planted"] else "false"

    by_planted = {}
    for key in ("true", "false", "null"):
        rows = [s for s in samples if planted_key(s) == key]
        if not rows:
            continue
        c = sum(1 for s in rows if s["_class"] == "catch")
        m = sum(1 for s in rows if s["_class"] == "miss")
        u = sum(1 for s in rows if s["_class"] == "unknown")
        blind = m + u
        n = len(rows)
        entry = {"n": n, "catch": c, "miss": m, "unknown": u,
                 "blindspot_ratio": round(blind / n, 4),
                 "blindspot_wilson95": wilson(blind / n, n)}
        if key == "false":
            entry["note"] = ("planted=false 仅 74 条（expG 真实 CVE 衍生）；n 小，"
                             "比例不稳，务必看 Wilson 区间")
        if key == "null":
            entry["note"] = ("corpus 64 条为外部真实语料，无 planted 字段；"
                             "其中 53 条源码来自历史真实缺陷/规范差异，不能与 planted=true 混同")
        by_planted[key] = entry

    # ── 5) 资产互补性（两两并集 + 单资产边际贡献）─────────────────────
    pairs = []
    for i, a in enumerate(AVAILABLE):
        for b in AVAILABLE[i + 1:]:
            uni = sum(1 for s in samples
                      if s["per_asset"].get(a, {}).get("verdict") == "catch"
                      or s["per_asset"].get(b, {}).get("verdict") == "catch")
            pairs.append({"pair": [a, b], "union_catch": uni,
                          "union_rate": round(uni / n_total, 4)})
    pairs.sort(key=lambda p: -p["union_rate"])
    solo = {a: by_asset[a]["catch"] for a in AVAILABLE}
    all6 = sum(1 for s in samples if s["_class"] == "catch")

    # ── 6) TSan 稳定性 ──────────────────────────────────────────────
    stab = {"n_with_runs": 0, "stable": 0, "unstable": 0, "unstable_list": []}
    for s in samples:
        st = s.get("tsan_stability")
        if st and st.get("runs"):
            stab["n_with_runs"] += 1
            if st.get("stable"):
                stab["stable"] += 1
            else:
                stab["unstable"] += 1
                stab["unstable_list"].append({"uid": s["uid"], "runs": st["runs"]})

    # ── 7) 盲区带汇总 ────────────────────────────────────────────────
    bands = {
        "high_blindspot(>50%)": [r["defect_type"] for r in type_rows if r["band"].startswith("high")],
        "partial_visibility(20-50%)": [r["defect_type"] for r in type_rows if r["band"].startswith("partial")],
        "low_blindspot(<20%)": [r["defect_type"] for r in type_rows if r["band"].startswith("low")],
    }

    out = {
        "schema": "queyi-blindspot-stats/676g",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "source": MATRIX.relative_to(ROOT).as_posix(),
        "caliber": {
            "sample_catch": "8 资产任一 catch（wunsequenced/compile-time 结构性恒 unknown，永不 catch，OR 口径等价于 6 可用资产）",
            "sample_miss": "无 catch 且 ≥1 可用资产确定 miss",
            "sample_unknown": "可用 6 资产全部 unknown",
            "blindspot_ratio": "(miss + unknown) / n；miss 与 unknown 单列，不混同",
            "types_note": "细粒度类型沿用各批次 INDEX 的 defect_type 原字符串；family 为报告分组（附录口径）",
            "hierarchy_note": "corpus/holdout 用粗粒度 category（MEM/UB/CONC/...），扩样批次用细粒度类型；两层不合并计数，避免层级重复",
        },
        "total": {"n": n_total, **{k: overall.get(k, 0) for k in ("catch", "miss", "unknown", "MISSING")},
                  "blindspot_ratio": round((overall.get("miss", 0) + overall.get("unknown", 0)) / n_total, 4)},
        "by_type": type_rows,
        "by_asset": {a: by_asset[a] for a, _ in asset_rank},
        "asset_rank_by_coverage": [a for a, _ in asset_rank],
        "by_batch": by_batch,
        "by_planted": by_planted,
        "complementarity": {
            "solo_catch": solo,
            "all6_union_catch": all6,
            "all6_union_rate": round(all6 / n_total, 4),
            "pairwise_union": pairs,
            "marginal_gain_of_adding_asset_to_rest": {
                # 把资产 a 加进"其余 5 个资产"的池子，新增的检出 = 只被 a 抓到的样本
                a: round((sum(1 for s in samples
                              if s["per_asset"].get(a, {}).get("verdict") == "catch"
                              and all(s["per_asset"].get(b, {}).get("verdict") != "catch"
                                      for b in AVAILABLE if b != a))) / n_total, 4)
                for a in AVAILABLE},
        },
        "tsan_stability": stab,
        "blindspot_bands": bands,
        "n_types": len(type_rows),
    }
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n",
                   encoding="utf-8", newline="\n")
    print(f"[676g] stats: {n_total} 样本 / {len(type_rows)} 类型；"
          f"总盲区 {out['total']['blindspot_ratio']:.1%}；"
          f"高盲区 {len(bands['high_blindspot(>50%)'])} 类型 / "
          f"部分可见 {len(bands['partial_visibility(20-50%)'])} / "
          f"低盲区 {len(bands['low_blindspot(<20%)'])}")
    print(f"[676g] 写入 {OUT.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
