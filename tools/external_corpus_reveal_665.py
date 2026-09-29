#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""external_corpus_reveal_665.py — 665 D2：外部 corpus 扩到 40 后的检出率。

为什么不跑 `external_corpus_662.py`
===================================
那个脚本会把结果写进 `data/external_corpus_reveal_662.json`——那是 **662 的历史留痕**，
覆写它等于抹掉当时的测量。本工具 `import` 它的 `detect()`（**判据只有一个版本**），
但把结果写进新文件 `data/external_corpus_reveal_665.json`。

收益在哪
========
662 只敢说"检出率 33.3%，低分大概是因为缺检测器"。665 D1 把 corpus 按**检测器可用性**
分了三层（A 本机可跑 / B 跨编译器·测量 / C 本机无检测器），所以本轮能把这个"大概"
变成一张**可对照的表**：A 层检出率 vs C 层 unknown 占比。

输出：data/external_corpus_reveal_665.json
"""
from __future__ import annotations

import importlib.util
import json
import os
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HERE = os.path.dirname(os.path.abspath(__file__))
CORPUS = os.path.join(ROOT, "data", "external_corpus", "external_corpus_662.json")
OLD = os.path.join(ROOT, "data", "external_corpus_reveal_662.json")
OUT = os.path.join(ROOT, "data", "external_corpus_reveal_665.json")

#: 按 expected_detector 归类到 D1 的三层
LAYER = {**{k: "A_local" for k in ("asan", "ubsan", "tsan", "compiler-warn", "wunsequenced")},
         **{k: "B_cross_or_measure" for k in ("cross-compile", "measure")},
         "unknown": "C_no_local_detector"}


def _load_ex662():
    spec = importlib.util.spec_from_file_location("ex662", os.path.join(HERE, "external_corpus_662.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def _load_ext665():
    spec = importlib.util.spec_from_file_location("ext665", os.path.join(HERE, "external_corpus_extend_665.py"))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main() -> int:
    ex = _load_ex662()
    # 读 **canonical 合并视图**（40 条），不是 662 的产物文件（会被旧工具重写成 20 条）
    c = _load_ext665().load_merged()
    old = json.load(open(OLD, encoding="utf-8")) if os.path.isfile(OLD) else {}

    rows: list = []          # 666 A1：加注解消 var-annotated
    by_layer: dict = {}
    for s in c["samples"]:
        kind = s["expected_detector"]
        v, note = ex.detect(kind, s.get("code"))
        layer = LAYER.get(kind, "other")
        d = by_layer.setdefault(layer, {"total": 0, "catch": 0, "miss": 0, "unknown": 0,
                                        "not_error": 0, "measurable": 0})
        d["total"] += 1
        if v in ("catch", "miss", "unknown", "not_error"):
            d[v] += 1
        if v in ("catch", "miss"):
            d["measurable"] += 1
        rows.append({"id": s["id"], "category": s["category"], "verified_source": s["verified_source"],
                     "detector": kind, "layer": layer, "verdict": v, "note": note[:200]})
        print(f"  {s['id']:<6} {v.upper():<10} {kind:<14} {note[:50]}")

    catch = sum(1 for r in rows if r["verdict"] == "catch")
    miss = sum(1 for r in rows if r["verdict"] == "miss")
    unknown = sum(1 for r in rows if r["verdict"] == "unknown")
    not_error = sum(1 for r in rows if r["verdict"] == "not_error")
    denom = catch + miss
    for layer, d in by_layer.items():
        d["detect_rate_pct"] = round(d["catch"] / d["measurable"] * 100, 1) if d["measurable"] else 0.0

    rep = {
        "schema": "queyi-external-corpus-reveal/v2",
        "generated_at": time.strftime("%Y-%m-%d"),
        "generated_by": "tools/external_corpus_reveal_665.py",
        "detector_reuse": "import tools/external_corpus_662.py::detect（唯一判据），结果另存 665 文件",
        "total": len(rows),
        "catch": catch, "miss": miss, "unknown": unknown, "not_error": not_error,
        "detect_rate_pct": round(catch / denom * 100, 1) if denom else 0.0,
        "by_layer": by_layer,
        "compare_662": {
            "before_total": old.get("total"),
            "before_detect_rate_pct": old.get("detect_rate_pct"),
            "after_total": len(rows),
            "after_detect_rate_pct": round(catch / denom * 100, 1) if denom else 0.0,
            "note": ("分母仍是 catch+miss（可测且非测量类）；两轮的对比对象是**不同样本集合**，"
                     "所以数字差异只能描样本构成，不能断言验证器变好变坏。"),
        },
        "honest_note": ("source 只写类别级出处；`verified_source=false` 的条目**未**被本机验证过。"
                        "C 层（本机无检测器）样本若全是 unknown，这才算 662 那条猜测的证据；反过来，"
                        "若 A 层检出率也不高，就说明问题不在『缺检测器』。"),
        "results": rows,
    }
    json.dump(rep, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n总 {len(rows)}：catch={catch} miss={miss} unknown={unknown} not_error={not_error} "
          f"→ 检出率={rep['detect_rate_pct']}%（662 为 {old.get('detect_rate_pct')}%）")
    for layer, d in sorted(by_layer.items()):
        print(f"  {layer:<22} 可测 {d['measurable']}/{d['total']}  检出率={d['detect_rate_pct']}%")
    print(f"已写 {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
