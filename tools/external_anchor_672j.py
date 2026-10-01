#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""external_anchor_672j.py — 672j W5：外部锚定的**检测与统计**。

判据（不另造）
==============
* sanitizer 类：`tools/external_corpus_reveal_671a.py::detect_san_double_opt`（-O0/-O2 + setarch -R）；
* 其余（compiler-warn / cross-compile）：`tools/external_corpus_662.py::detect`（-fsyntax-only / 双编译器）。
样本若带 `harness`（prelude_v1）则在编译前统一拼接（不改片段主体）——见数据集 `harness` 字段。

统计
====
* 每子集 + 总集：catch/miss/unknown + CP95（stat_bounds 单一来源）；
* 与 corpus（62.5%，n=64）/ holdout（82.9%，n=41）的**非配对**率差（Newcombe 混合区间，本工具实现）；
* 预注册 H1/H2/H3 判定（阈值见 prereg_672j.json）。

产物：`data/external_anchor_reveal_672j.json`

用法
====
    python tools/external_anchor_672j.py                 # 跑（3 回合）
    python tools/external_anchor_672j.py --runs 1 --json  # 快速/机读
    python tools/external_anchor_672j.py --selftest       # 自检（不联网不编译）
"""
from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
import math
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
DATASET = ROOT / "data" / "external_anchor" / "external_anchor_672j.json"
FETCH = HERE / "external_anchor_fetch_672j.py"
OUT = ROOT / "data" / "external_anchor_reveal_672j.json"
CORPUS_REVEAL = ROOT / "data" / "external_corpus_reveal_672h.json"
HOLDOUT_REVEAL = ROOT / "data" / "holdout_reveal_5_672h.json"
CORPUS_HIST_RATE = 54.2      # 预注册 H2 引用的 corpus 历史子集（n=48，672h 前）
N_RUNS = 3


def _load_mod(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def jload(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def prelude() -> str:
    return _load_mod("anchor_fetch", FETCH).PRELUDE


def newcombe_diff(k1: int, n1: int, k2: int, n2: int, conf: float = 0.95) -> tuple[float, float]:
    """两独立比例的 Newcombe 混合区间（本工具自实现；用于**非配对**子集比较）。"""
    sb = _load_mod("stat_bounds", HERE / "stat_bounds.py")
    z = 1.959963984540054
    p1, p2 = (k1 / n1 if n1 else 0.0), (k2 / n2 if n2 else 0.0)

    def cp(k: int, n: int) -> tuple[float, float]:
        if n <= 0:
            return (0.0, 1.0)
        r = sb.proportion(k, n, conf)
        return (r["cp_low"], r["cp_high"])

    l1, u1 = cp(k1, n1)
    l2, u2 = cp(k2, n2)
    delta = p1 - p2
    se1 = math.sqrt(p1 * (1 - p1) / n1) if n1 else 0.0
    se2 = math.sqrt(p2 * (1 - p2) / n2) if n2 else 0.0
    lo = delta - math.sqrt(max(0.0, (p1 - l1) ** 2 + (u2 - p2) ** 2))
    hi = delta + math.sqrt(max(0.0, (u1 - p1) ** 2 + (p2 - l2) ** 2))
    # 退化保护：n 太小或退化样本时用 Wald 兜底（登记在 note 里）
    if not (math.isfinite(lo) and math.isfinite(hi)) or (se1 + se2 == 0 and delta == 0):
        half = z * math.sqrt(se1 ** 2 + se2 ** 2)
        lo, hi = delta - half, delta + half
    return (lo, hi)


def measure(e671a, e662, samples: list[dict], pre: str) -> list[dict]:
    rows = []
    for s in samples:
        code = (pre + s["code"]) if s.get("harness") else s["code"]
        verdicts, notes = [], []
        for kind in s["expected_detectors"]:
            if kind in ("asan", "ubsan", "tsan"):
                v, note = e671a.detect_san_double_opt(kind, code)
            else:
                v, note = e662.detect(kind, code)
            verdicts.append(v)
            notes.append(f"{kind}:{v}({str(note)[:70]})")
        if "catch" in verdicts:
            v = "catch"
        elif all(x == "unknown" for x in verdicts):
            v = "unknown"
        else:
            v = "miss"
        rows.append({"id": s["id"], "subset": s["subset"], "label": s.get("label"),
                     "rule_id": s.get("rule_id"), "detectors": s["expected_detectors"],
                     "verdict": v, "per_detector": verdicts,
                     "note": " | ".join(notes)[:300]})
        print(f"  {s['id']:<6} {s['subset'][:18]:<18} {str(s.get('rule_id')):<8} {v:<8}"
              f" {' | '.join(notes)[:60]}", flush=True)
    return rows


def tally(rows: list[dict]) -> dict[str, Any]:
    c = m = u = 0
    for r in rows:
        if r["verdict"] == "catch":
            c += 1
        elif r["verdict"] == "miss":
            m += 1
        else:
            u += 1
    den = c + m
    sb = _load_mod("stat_bounds", HERE / "stat_bounds.py")
    cp = sb.proportion(c, den, 0.95) if den else None
    return {"total": len(rows), "catch": c, "miss": m, "unknown": u,
            "denominator": {"value": den, "meaning": "catch+miss（可测）", "excluded": {"unknown": u}},
            "rate_pct": round(c / den * 100, 1) if den else None,
            "cp95": ({"k": c, "n": den, "point": cp["point"], "cp_low": cp["cp_low"],
                      "cp_high": cp["cp_high"], "conf": 0.95} if cp else None)}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="672j W5：外部锚定检测")
    ap.add_argument("--runs", type=int, default=N_RUNS)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()

    e671a = _load_mod("ecr671a", HERE / "external_corpus_reveal_671a.py")
    e662 = _load_mod("ec662", HERE / "external_corpus_662.py")
    ds = jload(DATASET)
    pre = prelude()
    samples = ds["samples"]
    print(f"[anchor-672j] {len(samples)} 条 × {a.runs} 回合（verbatim "
          f"{ds['counts']['guideline_bad_verbatim']} + 重建 {ds['counts']['ub_reconstructed']}）")
    per_run = []
    for i in range(a.runs):
        print(f"--- round {i + 1}/{a.runs} ---", flush=True)
        per_run.append(measure(e671a, e662, samples, pre))
    # 聚合：任一回合 catch ⇒ catch（与 672h 口径一致）
    by_id: dict[str, list[dict]] = {}
    for run in per_run:
        for r in run:
            by_id.setdefault(r["id"], []).append(r)
    rows = []
    for s in samples:
        rs = by_id.get(s["id"], [])
        vs = [r["verdict"] for r in rs]
        v = ("catch" if "catch" in vs else
             ("unknown" if vs and all(x == "unknown" for x in vs) else ("miss" if vs else "unknown")))
        rows.append({**rs[0], "verdict": v, "verdicts_per_run": vs,
                     "reproducible": bool(vs) and len(set(vs)) == 1})

    sub_a = [r for r in rows if r["subset"] == "guideline_bad_verbatim"]
    sub_b = [r for r in rows if r["subset"] == "ub_reconstructed"]
    ta, tb, tt = tally(sub_a), tally(sub_b), tally(rows)

    corpus = jload(CORPUS_REVEAL)["cumulative"]
    holdout = jload(HOLDOUT_REVEAL)["cumulative"]
    cr, cn = corpus["catch"], corpus["denominator"]["value"]
    hr, hn = holdout["error_subset"]["catch"], holdout["denominator"]["value"]

    h1_delta = (None if ta["rate_pct"] is None else round(corpus["detect_rate_pct"] - ta["rate_pct"], 1))
    h1_ci = (None if ta["denominator"]["value"] == 0 else
             [round(x * 100, 1) for x in newcombe_diff(cr, cn, ta["catch"],
                                                       ta["denominator"]["value"])])
    h2_delta = (None if tb["rate_pct"] is None else round(tb["rate_pct"] - CORPUS_HIST_RATE, 1))
    rep = {
        "schema": "queyi-external-anchor-reveal/672j",
        "generated_by": "tools/external_anchor_672j.py（W5 外部锚定）",
        "generated_at": _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "prereg": "data/experiments/prereg_672j.json",
        "dataset": str(DATASET.relative_to(ROOT).as_posix()),
        "source": ds["source"], "harness": ds.get("harness"),
        "compilability_filter": ds.get("compilability_filter"),
        "runs": a.runs,
        "caliber": "可测 = catch+miss；unknown 不进分母；**两部分子集分列**（目标类不同）",
        "subset_a_guideline_verbatim": ta,
        "subset_b_ub_reconstructed": tb,
        "total": tt,
        "compare": {
            "corpus_672h": {"k": cr, "n": cn, "rate_pct": corpus["detect_rate_pct"]},
            "holdout_5_672h": {"k": hr, "n": hn, "rate_pct": holdout["error_subset"]["detect_rate_pct"]},
            "corpus_hist_reference_pct": CORPUS_HIST_RATE,
            "diff_vs_corpus_pp": h1_delta, "diff_vs_corpus_ci95_pp": h1_ci,
            "diff_vs_holdout_pp": (None if tt["rate_pct"] is None else
                                   round(holdout["error_subset"]["detect_rate_pct"] - tt["rate_pct"], 1)),
        },
        "hypothesis_verdicts": {
            "H1_corpus_minus_guideline_gt_10pp": ("成立" if (h1_delta is not None and h1_delta > 10)
                                                  else f"不成立（Δ={h1_delta}pp）"),
            "H2_recon_ub_vs_corpus_hist_lt_25pp": ("成立" if (h2_delta is not None and abs(h2_delta) < 25)
                                                   else f"不成立（Δ={h2_delta}pp）"),
            "H3_total_rate_ge_30pct": ("成立" if (tt["rate_pct"] is not None and tt["rate_pct"] >= 30)
                                       else f"不成立（{tt['rate_pct']}%）"),
        },
        "per_sample": rows,
        "unknown_samples": [{"id": r["id"], "note": r["note"][:160]} for r in rows
                            if r["verdict"] == "unknown"],
        "reproducibility": {"unstable": [{"id": r["id"], "verdicts": r["verdicts_per_run"]}
                                         for r in rows if not r["reproducible"]]},
        "honest_note": "外部锚定唯一 verbatim 源是 C++ Core Guidelines（cppref/SO 403）；"
                       "subset A 的目标类是『准则违规』而不是 UB ⇒ 其率低不代表检测器坏，"
                       "代表『仪器测不到规范问题』；subset B 才是与 corpus 可比的目标类。",
    }
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print(f"\n[total]  {tt['catch']}/{tt['denominator']['value']} = {tt['rate_pct']}%"
              f"（unknown {tt['unknown']}）")
        print(f"[subsetA guideline] {ta['catch']}/{ta['denominator']['value']} = {ta['rate_pct']}%")
        print(f"[subsetB recon UB ] {tb['catch']}/{tb['denominator']['value']} = {tb['rate_pct']}%")
        print(f"[compare] corpus {corpus['detect_rate_pct']}% (n={cn}) ｜ holdout "
              f"{holdout['error_subset']['detect_rate_pct']}% (n={hn})")
        print("[假设] " + json.dumps(rep["hypothesis_verdicts"], ensure_ascii=False))
    if not a.no_write:
        OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8", newline="\n")
        print(f"[anchor-672j] 写入 {OUT.relative_to(ROOT).as_posix()}")
    return 0


def selftest() -> int:
    ok = 0
    ds = jload(DATASET)
    assert ds["counts"]["total"] >= 50, ds["counts"]
    assert ds["counts"]["guideline_bad_verbatim"] == 35
    assert ds["counts"]["ub_reconstructed"] == 15
    ok += 3
    ids = [s["id"] for s in ds["samples"]]
    assert len(ids) == len(set(ids)) == 50
    assert all(s.get("code") and s.get("expected_detectors") for s in ds["samples"])
    ok += 2
    # verbatim 部分必须可复核（URL + code_sha256），重建部分必须标明来源类别
    va = [s for s in ds["samples"] if s["subset"] == "guideline_bad_verbatim"]
    rb = [s for s in ds["samples"] if s["subset"] == "ub_reconstructed"]
    assert all(s["source_url"] and s["code_sha256"] and s["verbatim"] is True for s in va)
    assert all(s["citation"] and s["verbatim"] is False for s in rb)
    ok += 3
    # 检测器映射合法
    legal = {"asan", "ubsan", "tsan", "compiler-warn", "cross-compile"}
    assert all(set(s["expected_detectors"]) <= legal for s in ds["samples"])
    ok += 1
    # 统计口径：unknown 不进分母
    rows = [{"id": "a", "verdict": "catch"}, {"id": "b", "verdict": "miss"},
            {"id": "c", "verdict": "unknown"}]
    t = tally(rows)
    assert t["denominator"]["value"] == 2 and t["rate_pct"] == 50.0 and t["unknown"] == 1
    ok += 2
    # Newcombe：自实现区间必须包含点差、且量级合理
    lo, hi = newcombe_diff(34, 41, 10, 35)
    d = 34 / 41 - 10 / 35
    assert lo < d < hi and -1 <= lo <= hi <= 1
    lo2, hi2 = newcombe_diff(0, 0, 5, 10)
    assert lo2 <= hi2
    ok += 2
    print(f"[anchor-672j-selftest] {ok} 项通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
