#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""external_corpus_reveal_672h.py — 672h W3：external corpus 第 4 轮 reveal（d3f-01..d3f-16）。

设计：**薄壳**。判据与统计原语全部 `import` 第 3 轮（`external_corpus_reveal_671a.py`）：
    * `detect_671a(kind, code)`（sanitizer 双档 + setarch -R；其余委托 662 原实现）
    * `tally` / `by_layer` / `cp`（CP95 走 stat_bounds）
本工具只做三件新事：
    1. 从 `data/external_corpus/external_corpus_672h.json` 读 16 条新样本；
    2. 3 回合测量，按预注册口径**任一回合 catch ⇒ catch** 聚合（同时留首回合口径）；
    3. 复用 `data/external_corpus/reveal_detail_671a.json` 的历史 60 条，拼 cumulative。

产物
====
* `data/external_corpus_reveal_672h.json`（schema `queyi-external-corpus-reveal/672h`）
* `data/external_corpus/reveal_detail_672h.json`（schema `queyi-external-corpus-reveal-detail/672h`）
"""
from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXT = ROOT / "data" / "external_corpus" / "external_corpus_672h.json"
PREV_DETAIL = ROOT / "data" / "external_corpus" / "reveal_detail_671a.json"
PREV_ROUND = ROOT / "data" / "external_corpus_reveal_671a.json"
OUT = ROOT / "data" / "external_corpus_reveal_672h.json"
DETAIL = ROOT / "data" / "external_corpus" / "reveal_detail_672h.json"
N_RUNS = 3


def _load_mod(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"无法从 {path} 构造模块规格（{name}）")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def prev_mod():
    return _load_mod("ecr671a", HERE / "external_corpus_reveal_671a.py")


def jload(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def aggregate_runs(ids: list[str], runs: list[list[dict]]) -> list[dict]:
    """预注册口径：任一回合 catch ⇒ catch；全 unknown ⇒ unknown；否则 miss。"""
    by_id: dict[str, list[dict]] = {}
    for run in runs:
        for r in run:
            by_id.setdefault(r["id"], []).append(r)
    out = []
    for sid in ids:
        rs = by_id.get(sid, [])
        vs = [r["verdict"] for r in rs]
        first = rs[0] if rs else {"detector": "unknown", "layer": "other",
                                  "category": None, "note": "未跑"}
        verdict = ("catch" if "catch" in vs else
                   ("unknown" if vs and all(v == "unknown" for v in vs) else
                    ("miss" if vs else "unknown")))
        out.append({**first, "id": sid, "verdict": verdict, "verdicts_per_run": vs,
                    "first_run_verdict": vs[0] if vs else "unknown",
                    "reproducible": bool(vs) and len(set(vs)) == 1})
    return out


def build(new_rows: list[dict], hist_rows: list[dict], runs: int) -> dict[str, Any]:
    e = prev_mod()
    all_rows = new_rows + hist_rows
    cum = e.tally(all_rows)
    cum["cp95"] = e.cp(cum["catch"], cum["denominator"]["value"])
    cum["by_layer"] = e.by_layer(all_rows)
    r5 = e.tally(new_rows)
    r5["cp95"] = e.cp(r5["catch"], r5["denominator"]["value"])
    hist = e.tally(hist_rows)
    hist["cp95"] = e.cp(hist["catch"], hist["denominator"]["value"])

    prev = jload(PREV_ROUND) if PREV_ROUND.is_file() else {}
    pc = prev.get("cumulative") or {}
    pcv = cprv = None
    try:
        pcv = cprv = None
        prv = (pc.get("cp95") or {})
        pcv = [round(prv["cp_low"] * 100, 1), round(prv["cp_high"] * 100, 1)] if prv else None
        cprv = prv.get("k")
    except Exception:  # noqa: BLE001
        pass

    alt_rows = [{**r, "verdict": r.get("first_run_verdict", r["verdict"])
                 if r.get("verdicts_per_run") else r["verdict"]} for r in all_rows]
    alt = e.tally(alt_rows)
    alt["cp95"] = e.cp(alt["catch"], alt["denominator"]["value"])

    nr = r5["detect_rate_pct"]
    hr = hist["detect_rate_pct"]
    h4 = None if (nr is None or hr is None) else round(nr - hr, 1)

    report = {
        "schema": "queyi-external-corpus-reveal/672h",
        "reveal_index": 4,
        "generated_by": "tools/external_corpus_reveal_672h.py（W3 扩样：可测 48 → %d）"
                        % cum["denominator"]["value"],
        "generated_at": _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "round_label": "第 4 轮（672h）：扩样 d3f-01..d3f-16 + 历史 60 条复用",
        "runs": runs,
        "prereg": "data/experiments/prereg_672h.json",
        "detector_reuse": "sanitizer 双档 + setarch -R（671a 实现）；其余委托 external_corpus_662.detect",
        "caliber": "可测 = catch+miss（非测量类）；unknown / not_error 不进分母；六层禁合并",
        "historical_reuse": {"n": len(hist_rows), "ids": [r["id"] for r in hist_rows],
                             "source": str(PREV_DETAIL.relative_to(ROOT).as_posix())},
        "env": e.env_probe(),
        "round_new": r5,
        "cumulative": cum,
        "compare_reveal_671a": {
            "before": {"denominator": (pc.get("denominator") or {}).get("value"),
                       "k": cprv, "detect_rate_pct": pc.get("detect_rate_pct"),
                       "cp95": pcv},
            "after": {"denominator": cum["denominator"]["value"], "k": cum["catch"],
                      "detect_rate_pct": cum["detect_rate_pct"],
                      "cp95": [round(cum["cp95"]["cp_low"] * 100, 1),
                               round(cum["cp95"]["cp_high"] * 100, 1)]},
            "why_changed": "分母 48 → %d（新增 d3f-* 16 条，全部本机有判据）"
                           % cum["denominator"]["value"],
        },
        "H4_exploratory": {
            "question": "新增子集（d3f-*）与历史子集检出率差是否 <20pp",
            "new_subset": {"k": r5["catch"], "n": r5["denominator"]["value"], "rate_pct": nr},
            "historical_subset": {"k": hist["catch"], "n": hist["denominator"]["value"],
                                  "rate_pct": hr},
            "delta_pp": h4,
            "verdict": ("未判定（缺数据）" if h4 is None else
                        ("与预注册一致（<20pp）" if abs(h4) < 20 else
                         "超出预注册范围（≥20pp）⇒ 子集构成差异显著，如实登记")),
        },
        "reproducibility": {
            "runs_per_new_sample": runs,
            "unstable": [{"id": r["id"], "verdicts": r["verdicts_per_run"]}
                         for r in new_rows if not r["reproducible"]],
        },
        "new_sample_unknown": [{"id": r["id"], "detector": r["detector"], "note": r["note"][:160]}
                               for r in new_rows if r["verdict"] == "unknown"],
        "honest_note": "d3f-* 是本仓自撰的可编译片段（缺陷类别据公开清单），verified_source=false；"
                       "cross-compile 两条依赖 g++/clang++ 差异，实测可能 miss——如实记录。",
        "detail": str(DETAIL.relative_to(ROOT).as_posix()),
    }
    detail = {
        "schema": "queyi-external-corpus-reveal-detail/672h",
        "generated_by": "tools/external_corpus_reveal_672h.py",
        "generated_at": report["generated_at"],
        "summary_for": "data/external_corpus_reveal_672h.json",
        "runs": runs,
        "verdict_rule": "任一回合 catch ⇒ catch（预注册 672h）；first_run_verdict 一并落盘",
        "env": report["env"],
        "per_sample": all_rows,
        "round_new_summary": r5,
        "cumulative_summary": cum,
        "sensitivity_first_run_rule": alt,
        "note": "历史 60 条为 671a 落盘值（首回合口径）；d3f-* 为 3 回合『任一 catch』口径。",
    }
    return {"report": report, "detail": detail}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="672h W3：corpus 第 4 轮 reveal（d3f-*）")
    ap.add_argument("--runs", type=int, default=N_RUNS)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest()

    e = prev_mod()
    ext = jload(EXT)
    samples = ext["samples"]
    ids = [s["id"] for s in samples]
    print(f"[ec-reveal-672h] 新样本 {len(ids)} 条 × {a.runs} 回合；判据 e671a.detect_671a")
    runs = []
    for i in range(a.runs):
        print(f"--- round {i + 1}/{a.runs} ---", flush=True)
        runs.append(e.measure_once(samples))
    new_rows = aggregate_runs(ids, runs)

    prev = jload(PREV_DETAIL)
    hist_rows = []
    for r in prev["per_sample"]:
        hist_rows.append({**r, "verdicts_per_run": [r["verdict"]],
                          "first_run_verdict": r["verdict"],
                          "reproducible": bool(r.get("reproducible", True)),
                          "source": "reused_reveal_671a"})
    for r in new_rows:
        r["source"] = "measured_672h"

    built = build(new_rows, hist_rows, a.runs)
    rep, det = built["report"], built["detail"]
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        c = rep["cumulative"]
        print(f"\n[cumulative] 分母 {c['denominator']['value']} catch {c['catch']} miss {c['miss']}"
              f" unknown {c['unknown']} not_error {c['not_error']} rate {c['detect_rate_pct']}%"
              f" CP95 [{c['cp95']['cp_low']*100:.1f}, {c['cp95']['cp_high']*100:.1f}]")
        print("[by_layer]  ", {k: (v["catch"], v["miss"], v["detect_rate_pct"])
                               for k, v in c["by_layer"].items()})
        print("[H4]        ", rep["H4_exploratory"]["delta_pp"], rep["H4_exploratory"]["verdict"])
        if rep["new_sample_unknown"]:
            print("[unknown]   ", rep["new_sample_unknown"])
    if not a.no_write:
        OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8", newline="\n")
        DETAIL.write_text(json.dumps(det, ensure_ascii=False, indent=1) + "\n",
                          encoding="utf-8", newline="\n")
        print(f"[ec-reveal-672h] 写入 {OUT.name} + {DETAIL.name}")
    return 0


def selftest() -> int:
    e = prev_mod()
    ok = 0
    # 聚合口径
    runs = [[{"id": "x", "detector": "asan", "layer": "sanitizer", "category": "UB",
              "verdict": v, "note": ""}] for v in ("miss", "catch", "unknown")]
    a = aggregate_runs(["x"], runs)[0]
    assert a["verdict"] == "catch" and a["first_run_verdict"] == "miss", a
    ok += 2
    assert aggregate_runs(["x"], [[{"id": "x", "detector": "asan", "layer": "sanitizer",
                                    "category": "UB", "verdict": "unknown", "note": ""}]] * 2)[0][
        "verdict"] == "unknown"
    ok += 1
    # tally：not_error / unknown 都不进分母
    rows = [{"id": "1", "verdict": "catch", "detector": "asan", "layer": "sanitizer"},
            {"id": "2", "verdict": "miss", "detector": "tsan", "layer": "sanitizer"},
            {"id": "3", "verdict": "not_error", "detector": "measure", "layer": "other"},
            {"id": "4", "verdict": "unknown", "detector": "perf-counter", "layer": "perf"}]
    t = e.tally(rows)
    assert t["denominator"]["value"] == 2 and t["detect_rate_pct"] == 50.0, t
    assert t["not_error"] == 1 and t["unknown"] == 1 and t["total"] == 4
    ok += 3
    # 六层：perf 层 n=0 ⇒ 拒答
    ly = e.by_layer(rows)
    assert set(ly) == {"sanitizer", "perf", "other"}, ly
    assert ly["perf"]["detect_rate_pct"] is None and ly["perf"]["cp95"]["cp_low"] is None
    ok += 2
    # 样本定义自洽：id 不重复、都有 code 与 expected_detector、detector 在本机判据集内
    samples = jload(EXT)["samples"]
    ids = [s["id"] for s in samples]
    assert len(ids) == len(set(ids)) == 16, len(ids)
    ok += 1
    assert all(s.get("code") and s.get("expected_detector") for s in samples)
    ok += 1
    assert {s["expected_detector"] for s in samples} <= {"asan", "ubsan", "tsan",
                                                        "compiler-warn", "cross-compile"}, \
        sorted({s["expected_detector"] for s in samples})
    ok += 1
    assert all(s.get("verified_source") is False for s in samples), "自撰片段必须 verified_source=false"
    ok += 1
    print(f"[ec-reveal-selftest] {ok} 项通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
