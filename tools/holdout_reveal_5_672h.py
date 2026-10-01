#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""holdout_reveal_5_672h.py — 672h W3：holdout 第 5 轮 reveal（扩样 21 → 41 可测）。

与第 4 轮（`holdout_reveal_4_671a.py`）的关系
=============================================
**判据完全复用** `tools/holdout_reveal_661.py::detect`（-O0/-O2 双档 + setarch -R 关 ASLR；
任一档报出即 catch；两档都不可用才 unknown）。本工具只做三件新事：

1. 新样本的夹具**分散在不同目录**（Appendix/ub、Examples/_ch14_*、Examples/_ch147_*、
   Examples/atoms），所以按样本切换 `rv.ATOMS` 到该样本所在目录（不再只切一个 FIXTURES）；
2. h1-h40 的结论**复用**第 4 轮（`data/holdout/reveal_3_detail_671a.json`），不重跑；
3. 聚合口径按 `data/experiments/prereg_672h.json`：**任一回合一档报出 ⇒ catch**
   （同时保留首回合口径与逐回合明细，供读者在两种口径下自查）。

产物
====
* `data/holdout_reveal_5_672h.json`（轮次报告，schema `queyi-holdout-reveal/v5`）
* `data/holdout/reveal_5_detail_672h.json`（逐样本明细，schema `queyi-holdout-reveal-detail/v3`）

用法
====
    python tools/holdout_reveal_5_672h.py                 # 跑 h41-h60，3 回合
    python tools/holdout_reveal_5_672h.py --runs 1        # 快速
    python tools/holdout_reveal_5_672h.py --no-write       # 只测不落盘
    python tools/holdout_reveal_5_672h.py --selftest       # 自检（不碰 WSL）
"""
from __future__ import annotations

import argparse
import datetime as _dt
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
EXT = ROOT / "data" / "holdout" / "holdout_extension_672h.json"
HOLDOUT = ROOT / "data" / "holdout" / "holdout.json"
PREV_DETAIL = ROOT / "data" / "holdout" / "reveal_3_detail_671a.json"
PREV_ROUND = ROOT / "data" / "holdout_reveal_4_671a.json"
OUT = ROOT / "data" / "holdout_reveal_5_672h.json"
OUT_DETAIL = ROOT / "data" / "holdout" / "reveal_5_detail_672h.json"

N_RUNS = 3
DEFAULT_SAMPLES = "h41-h60"

KIND_ALIAS = {"-wunsequenced": "wunsequenced", "wunsequenced": "wunsequenced"}

#: 六层纪律（669d）：检测器 → 层映射。禁把层合并成一个数。
DETECTOR_LAYER = {
    "asan": "sanitizer", "ubsan": "sanitizer", "tsan": "sanitizer",
    "compiler-warn": "compiler-warn", "wunsequenced": "compiler-warn",
    "cross-compile": "cross-compile", "linker": "linker",
    "perf-counter": "perf", "compile-time": "compile-time", "measure": "other",
}


def _load_mod(name: str, path: Path):
    spec = importlib.util.spec_from_file_location(name, str(path))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def load_rv661():
    return _load_mod("rv661", HERE / "holdout_reveal_661.py")


def load_stat_bounds():
    return _load_mod("stat_bounds", HERE / "stat_bounds.py")


def norm_kind(kind: str | None) -> str:
    k = str(kind or "").strip()
    return KIND_ALIAS.get(k.lower(), k)


def _load(p: Path) -> dict:
    return json.loads(p.read_text(encoding="utf-8"))


# ─────────────────────────────────────────────────────────────────────────────
# 计划：从扩展文件现推导（不手抄，避免第二事实源）
# ─────────────────────────────────────────────────────────────────────────────

def plan_from_extension(ext_seeds: list[dict]) -> dict[str, tuple[str, str, list[str]]]:
    """`{id: (kind, 目录(相对仓库), [文件名])}`。

    目录 = atom_ref/第一个 files 的父目录；同一样本的所有文件必须同目录
    （detect() 只接受一个 ATOMS 根 + 文件名列表）。
    """
    plan: dict[str, tuple[str, str, list[str]]] = {}
    for s in ext_seeds:
        sid = str(s.get("id"))
        refs = [str(x).replace("\\", "/") for x in (s.get("files") or [s.get("atom_ref")])]
        dirs = {os.path.dirname(r) for r in refs if r}
        if len(dirs) != 1:
            raise ValueError(f"{sid}: 文件跨目录（{sorted(dirs)}）⇒ detect() 无法编译，需改样本定义")
        d = dirs.pop()
        plan[sid] = (norm_kind(s.get("detector")), d, [os.path.basename(r) for r in refs])
    return plan


def parse_ids(spec: str, all_ids: list[str]) -> list[str]:
    """"h41-h60" / "h41,h43" / "h41-h45,h60" → id 列表（与 671a 同款区间语法）。"""
    if spec.strip().lower() in ("all", ""):
        return list(all_ids)
    out: list[str] = []
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part[1:]:
            a, b = part.split("-", 1)
            lo, hi = int(a.lstrip("hH")), int(b.lstrip("hH"))
            out += [f"h{i}" for i in range(lo, hi + 1)]
        else:
            out.append(part)
    return [i for i in out if i in set(all_ids)]


# ─────────────────────────────────────────────────────────────────────────────
# 测量
# ─────────────────────────────────────────────────────────────────────────────

def measure_round(rv, plan: dict[str, tuple[str, str, list[str]]],
                  ids: list[str]) -> list[dict]:
    """跑一遍：逐样本把 rv.ATOMS 切到该样本目录，再走 rv661.detect（唯一判据）。"""
    rows: list[dict] = []
    for sid in ids:
        kind, d, files = plan.get(sid, ("unknown", "", []))
        old = rv.ATOMS
        if d:
            rv.ATOMS = str(ROOT / d)
        try:
            verdict, note = rv.detect(kind, files)
        finally:
            rv.ATOMS = old
        rows.append({"id": sid, "detector": kind, "dir": d, "files": files,
                     "verdict": verdict, "note": str(note)[:300]})
        print(f"  {sid:<4} {kind:<14} {verdict:<8} {str(note)[:70]}", flush=True)
    return rows


def aggregate_runs(id_list: list[str], runs: list[list[dict]]) -> list[dict]:
    """合并多回合（预注册口径）：**任一回合 catch ⇒ catch**；全 unknown ⇒ unknown；否则 miss。

    同时保留首回合结论与逐回合序列 ⇒ 读者可在『首回合口径』下自查（672h 报告 §敏感）。
    """
    by_id: dict[str, list[dict]] = {}
    for run in runs:
        for r in run:
            by_id.setdefault(r["id"], []).append(r)
    out: list[dict] = []
    for sid in id_list:
        rs = by_id.get(sid, [])
        vs = [r["verdict"] for r in rs]
        first = rs[0] if rs else {"detector": "unknown", "dir": "", "files": [], "note": "未跑"}
        if "catch" in vs:
            verdict = "catch"
        elif vs and all(v == "unknown" for v in vs):
            verdict = "unknown"
        elif vs:
            verdict = "miss"
        else:
            verdict = "unknown"
        out.append({
            "id": sid, "detector": first["detector"], "dir": first.get("dir", ""),
            "files": first["files"], "verdict": verdict,
            "verdicts_per_run": vs,
            "first_run_verdict": vs[0] if vs else "unknown",
            "reproducible": bool(vs) and len(set(vs)) == 1,
            "note": first["note"],
        })
    return out


def tally(rows: list[dict], labels: dict[str, Any]) -> dict[str, Any]:
    """按标签统计（口径与第 4 轮一致：可测真错 = catch+miss）。"""
    ec = em = eu = 0
    ct = cf = 0
    lu = 0
    for r in rows:
        lab = labels.get(r["id"])
        v = r["verdict"]
        if lab is True:
            if v == "catch":
                ec += 1
            elif v == "miss":
                em += 1
            else:
                eu += 1
        elif lab is False:
            ct += 1
            if v == "catch":
                cf += 1
        else:
            lu += 1
    denom = ec + em
    return {
        "labels": {"error": ec + em + eu, "control": ct, "unknown": lu},
        "error_subset": {
            "total": ec + em + eu, "catch": ec, "miss": em, "unknown": eu,
            "detect_rate_pct": round(ec / denom * 100, 1) if denom else None,
        },
        "control_subset": {"total": ct, "false_positive": cf},
        "denominator": {"value": denom, "meaning": "catch+miss（可测真错样本）",
                        "excluded": {"detector_unknown": eu, "label_unknown": lu}},
    }


def by_layer(rows: list[dict], labels: dict[str, Any]) -> dict[str, Any]:
    """六层分层（669d 纪律：禁合并成一个数）。只统计 planted=true 的样本。"""
    out: dict[str, Any] = {}
    for r in rows:
        if labels.get(r["id"]) is not True:
            continue
        layer = DETECTOR_LAYER.get(r["detector"], "other")
        b = out.setdefault(layer, {"total": 0, "catch": 0, "miss": 0, "unknown": 0,
                                   "detectors": set()})
        b["total"] += 1
        b[r["verdict"]] = b.get(r["verdict"], 0) + 1
        b["detectors"].add(r["detector"])
    for layer, b in out.items():
        denom = b["catch"] + b["miss"]
        b["detectors"] = sorted(b["detectors"])
        b["denominator"] = {"value": denom, "meaning": "catch+miss（可测且非测量类）"}
        b["detect_rate_pct"] = round(b["catch"] / denom * 100, 1) if denom else None
        b["cp95"] = cp_interval(b["catch"], denom)
    return out


def cp_interval(k: int, n: int, conf: float = 0.95) -> dict[str, Any]:
    if n <= 0:
        return {"k": k, "n": n, "point": None, "cp_low": None, "cp_high": None,
                "conf": conf, "note": "n=0 ⇒ 拒绝给率（fail-loud）"}
    p = load_stat_bounds().proportion(k, n, conf)
    return {"k": k, "n": n, "point": p["point"], "cp_low": p["cp_low"],
            "cp_high": p["cp_high"], "conf": conf}


def env_probe() -> dict[str, Any]:
    import subprocess

    def run(cmd: list[str], timeout: int = 60) -> str:
        try:
            r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
            return ((r.stdout or "") + (r.stderr or "")).strip().splitlines()[0] if \
                ((r.stdout or "") + (r.stderr or "")).strip() else "(空)"
        except Exception as e:  # noqa: BLE001
            return f"(不可用: {type(e).__name__})"

    return {
        "wsl_gpp": run(["wsl", "-e", "bash", "-lc", "g++ --version | head -1"]),
        "local_gpp": run(["g++", "--version"]),
        "local_clang": run(["clang++", "--version"]),
        "host": sys.platform,
        "python": sys.version.split()[0],
        "roll": "asan/ubsan/tsan 走 WSL（-O0/-O2 双档 + setarch -R）；"
                "wunsequenced/compiler-warn/cross-compile/linker 走本机编译器",
    }


# ─────────────────────────────────────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────────────────────────────────────

def build_report(new_rows: list[dict], hist_rows: list[dict], labels: dict[str, Any],
                 runs: int, samples: list[str]) -> dict[str, Any]:
    """拼轮次报告 + 明细（cumulative 口径与第 4 轮同构，外加六层分层与 H4 子集对比）。"""
    all_rows = new_rows + hist_rows
    cum = tally(all_rows, labels)
    cum["cp95"] = cp_interval(cum["error_subset"]["catch"], cum["denominator"]["value"])
    cum["by_layer"] = by_layer(all_rows, labels)

    r5 = tally(new_rows, labels)
    r5["cp95"] = cp_interval(r5["error_subset"]["catch"], r5["denominator"]["value"])

    hist = tally(hist_rows, labels)
    hist["cp95"] = cp_interval(hist["error_subset"]["catch"], hist["denominator"]["value"])

    def _d(blk: dict) -> float | None:
        a, b = blk["error_subset"]["detect_rate_pct"], None
        return a

    new_rate = r5["error_subset"]["detect_rate_pct"]
    old_rate = hist["error_subset"]["detect_rate_pct"]
    h4_delta = (None if (new_rate is None or old_rate is None)
                else round(new_rate - old_rate, 1))

    prev = _load(PREV_ROUND) if PREV_ROUND.is_file() else {}
    prev_cum = (prev.get("cumulative") or {})
    prv = prev_cum.get("cp95") or {}

    # 首回合口径（敏感性）：全部样本按 first_run_verdict 重算
    alt_rows = []
    for r in all_rows:
        r2 = dict(r)
        r2["verdict"] = r.get("first_run_verdict", r["verdict"]) if r.get("verdicts_per_run") \
            else r["verdict"]
        alt_rows.append(r2)
    alt = tally(alt_rows, labels)
    alt["cp95"] = cp_interval(alt["error_subset"]["catch"], alt["denominator"]["value"])

    detail = {
        "schema": "queyi-holdout-reveal-detail/v3",
        "reveal_index": 5,
        "generated_by": "tools/holdout_reveal_5_672h.py",
        "generated_at": _dt.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "summary_for": "data/holdout_reveal_5_672h.json",
        "naming_note": "672h 第 5 轮：h41-h60 实测；h1-h40 复用第 4 轮（not 重跑）",
        "samples_requested": samples,
        "runs": runs,
        "detector_reuse": "tools/holdout_reveal_661.py::detect（唯一判据；-O0/-O2 双档 + setarch -R）",
        "verdict_rule": "任一回合任一档报出 ⇒ catch（预注册 672h 口径）；first_run_verdict 一并落盘",
        "caliber": "可测真错 = catch+miss；unknown（检测器不可用/编译失败）不进分母；对照单列",
        "env": env_probe(),
        "per_sample": all_rows,
        "round5_summary": r5,
        "historical_reuse": {"n": len(hist_rows), "ids": [r["id"] for r in hist_rows],
                             "source": str(PREV_DETAIL.relative_to(ROOT).as_posix())},
        "cumulative_summary": cum,
        "sensitivity_first_run_rule": alt,
        "note": "h1-h40 的 verdict 为 671a 第 4 轮落盘值（首回合口径，单回合）；"
                "h41-h60 为 3 回合『任一 catch』口径。两种口径的差别见 sensitivity_first_run_rule。",
    }
    report = {
        "schema": "queyi-holdout-reveal/v5",
        "reveal_index": 5,
        "generated_by": "tools/holdout_reveal_5_672h.py（W3 扩样：holdout 可测 21 → %d）"
                        % cum["denominator"]["value"],
        "generated_at": detail["generated_at"],
        "round_label": "第 5 轮（672h）：扩样 h41-h60（存量缺陷夹具）+ h1-h40 复用",
        "runs": runs,
        "samples_requested": samples,
        "prereg": "data/experiments/prereg_672h.json",
        "detector_reuse": detail["detector_reuse"],
        "caliber": detail["caliber"],
        "historical_reuse": detail["historical_reuse"],
        "env": detail["env"],
        "round5": r5,
        "cumulative": cum,
        "compare_reveal_4": {
            "before": {"denominator": prev_cum.get("denominator", {}).get("value"),
                       "k": prv.get("k"), "detect_rate_pct":
                       (prev_cum.get("error_subset") or {}).get("detect_rate_pct"),
                       "cp95": [round(prv["cp_low"] * 100, 1),
                                round(prv["cp_high"] * 100, 1)] if prv else None},
            "after": {"denominator": cum["denominator"]["value"],
                      "k": cum["error_subset"]["catch"],
                      "detect_rate_pct": cum["error_subset"]["detect_rate_pct"],
                      "cp95": [round(cum["cp95"]["cp_low"] * 100, 1),
                               round(cum["cp95"]["cp_high"] * 100, 1)]},
            "why_changed": "分母 21 → %d（新增 h41-h60 全部为 planted=true 的存量缺陷夹具）"
                           % cum["denominator"]["value"],
        },
        "H4_exploratory": {
            "question": "新增子集（h41-h60）与历史子集（h1-h40）的检出率差是否 <20pp",
            "new_subset": {"k": r5["error_subset"]["catch"], "n": r5["denominator"]["value"],
                           "rate_pct": new_rate},
            "historical_subset": {"k": hist["error_subset"]["catch"],
                                  "n": hist["denominator"]["value"], "rate_pct": old_rate},
            "delta_pp": h4_delta,
            "verdict": ("未判定（缺数据）" if h4_delta is None else
                        ("与预注册一致（<20pp）" if abs(h4_delta) < 20 else
                         "超出预注册范围（≥20pp）⇒ 说明子集构成差异显著，按预注册如实登记")),
            "caveat": "新子集 14/20 为 asan 类，检测器构成与历史子集不同；"
                      "该对比是**构成差异**的显式承认，不是检测能力差异的因果证据。",
        },
        "reproducibility": {
            "runs_per_new_sample": runs,
            "unstable": [{"id": r["id"], "verdicts": r["verdicts_per_run"]}
                         for r in new_rows if not r["reproducible"]],
        },
        "new_sample_unknown": [{"id": r["id"], "detector": r["detector"], "note": r["note"][:160]}
                               for r in new_rows if r["verdict"] == "unknown"],
        "honest_note": "扩样样本全部取自本仓既有故意缺陷夹具（不新写代码）；"
                       "新增子集 asan 占比高 ⇒ 汇总率为加权平均，必须与 by_layer 一起读；"
                       "双口径（任一回合 / 首回合）结果并列落盘。",
        "detail": str(OUT_DETAIL.relative_to(ROOT).as_posix()),
    }
    return {"report": report, "detail": detail}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="672h W3：holdout 第 5 轮 reveal（h41-h60）")
    ap.add_argument("--samples", default=DEFAULT_SAMPLES)
    ap.add_argument("--runs", type=int, default=N_RUNS)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()

    rv = load_rv661()
    ext = _load(EXT)
    plan = plan_from_extension(ext["seeds"])
    h = _load(HOLDOUT)
    labels = {s["id"]: s.get("planted") for s in h["seeds"]}
    ids = parse_ids(a.samples, sorted(plan))
    print(f"[reveal5] 新样本 {len(ids)} 条 × {a.runs} 回合；判据 rv661.detect")

    runs = [measure_round(rv, plan, ids) for _ in range(a.runs)]
    new_rows = aggregate_runs(ids, runs)

    # 历史复用
    prev = _load(PREV_DETAIL)
    prev_map = {r["id"]: r for r in prev["per_sample"]}
    hist_rows = []
    for s in h["seeds"]:
        if s["id"] in plan or s["id"] not in prev_map:
            continue
        p = prev_map[s["id"]]
        hist_rows.append({
            "id": s["id"], "detector": str(p.get("detector") or "unknown"),
            "dir": os.path.dirname(str(s.get("atom_ref") or "")).replace("\\", "/"),
            "files": [os.path.basename(str(s.get("atom_ref") or ""))],
            "verdict": str(p.get("verdict")), "verdicts_per_run": [str(p.get("verdict"))],
            "first_run_verdict": str(p.get("verdict")),
            "reproducible": bool(p.get("reproducible", True)),
            "note": "复用第 4 轮（671a）：" + str(p.get("note", ""))[:200],
            "source": "reused_reveal_4",
            "planted": s.get("planted"),          # 供 baseline_670a 现读（planted is True 才是真错）
            "layer": DETECTOR_LAYER.get(str(p.get("detector") or ""), "other"),
        })
    for r in new_rows:
        r["source"] = "measured_672h"
        r["planted"] = labels.get(r["id"])
        r["layer"] = DETECTOR_LAYER.get(r["detector"], "other")

    built = build_report(new_rows, hist_rows, labels, a.runs, ids)
    rep, det = built["report"], built["detail"]
    rep["detect_rate_pct"] = rep["cumulative"]["error_subset"]["detect_rate_pct"]
    rep["denominator"] = rep["cumulative"]["denominator"]["value"]

    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        c = rep["cumulative"]
        print(f"\n[cumulative] 分母 {c['denominator']['value']}  catch {c['error_subset']['catch']}"
              f"  miss {c['error_subset']['miss']}  unknown {c['error_subset']['unknown']}"
              f"  rate {c['error_subset']['detect_rate_pct']}%"
              f"  CP95 [{c['cp95']['cp_low']*100:.1f}, {c['cp95']['cp_high']*100:.1f}]")
        print(f"[round5]     k={rep['round5']['error_subset']['catch']}"
              f"/{rep['round5']['denominator']['value']}"
              f"  rate={rep['round5']['error_subset']['detect_rate_pct']}%")
        print("[by_layer]  ", {k: (v["catch"], v["miss"], v["detect_rate_pct"])
                               for k, v in c["by_layer"].items()})
        if rep["new_sample_unknown"]:
            print("[unknown]   ", rep["new_sample_unknown"])
    if not a.no_write:
        OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=1) + "\n",
                       encoding="utf-8", newline="\n")
        OUT_DETAIL.write_text(json.dumps(det, ensure_ascii=False, indent=1) + "\n",
                              encoding="utf-8", newline="\n")
        print(f"[reveal5] 写入 {OUT.name} + {OUT_DETAIL.name}")
    return 0


def selftest() -> int:
    """自检（不碰 WSL/编译器）：计划推导 + 区间语法 + 聚合/统计口径。"""
    ok = 0
    ext = _load(EXT)
    plan = plan_from_extension(ext["seeds"])
    assert len(plan) == len(ext["seeds"]), "计划数 ≠ 样本数"
    ok += 1
    kind, d, files = plan["h41"]
    assert kind == "asan" and d == "Appendix/ub" and files == ["ub_use_after_free.cpp"], (d, files)
    ok += 1
    ids = parse_ids("h41-h43,h60", sorted(plan))
    assert ids == ["h41", "h42", "h43", "h60"], ids
    ok += 1
    # 多回合聚合：任一 catch ⇒ catch；全 unknown ⇒ unknown；否则 miss
    runs = [[{"id": "x", "detector": "asan", "dir": "", "files": [], "verdict": v, "note": ""}]
            for v in ("miss", "catch", "miss")]
    agg = aggregate_runs(["x"], runs)[0]
    assert agg["verdict"] == "catch" and agg["first_run_verdict"] == "miss"
    assert agg["verdicts_per_run"] == ["miss", "catch", "miss"] and not agg["reproducible"]
    ok += 2
    runs_u = [[{"id": "x", "detector": "asan", "dir": "", "files": [], "verdict": "unknown",
                "note": ""}]]
    assert aggregate_runs(["x"], runs_u)[0]["verdict"] == "unknown"
    ok += 1
    # 统计口径：unknown 标签 / unknown 判定都不进分母
    rows = [{"id": "a", "verdict": "catch", "detector": "asan"},
            {"id": "b", "verdict": "miss", "detector": "tsan"},
            {"id": "c", "verdict": "unknown", "detector": "asan"},
            {"id": "d", "verdict": "catch", "detector": "compiler-warn"},
            {"id": "e", "verdict": "miss", "detector": "asan"}]
    labels = {"a": True, "b": True, "c": True, "d": True, "e": None}
    t = tally(rows, labels)
    assert t["denominator"]["value"] == 3 and t["error_subset"]["catch"] == 2
    assert t["control_subset"] == {"total": 0, "false_positive": 0}
    assert t["labels"] == {"error": 4, "control": 0, "unknown": 1}
    ok += 3
    # 六层分层：compiler-warn 层独立成层，不与 sanitizer 合并（且只统计 planted=true）
    ly = by_layer(rows, labels)
    assert set(ly) == {"sanitizer", "compiler-warn"}, ly
    assert ly["sanitizer"]["catch"] == 1 and ly["sanitizer"]["miss"] == 1
    assert ly["sanitizer"]["unknown"] == 1 and ly["sanitizer"]["detect_rate_pct"] == 50.0
    assert ly["compiler-warn"]["detect_rate_pct"] == 100.0
    ok += 3
    # CP 区间：与 stat_bounds 一致（17/21 → 58.1/94.6）
    cp = cp_interval(17, 21)
    assert abs(cp["cp_low"] * 100 - 58.1) < 0.2 and abs(cp["cp_high"] * 100 - 94.6) < 0.2, cp
    ok += 1
    assert cp_interval(0, 0)["cp_low"] is None, "n=0 必须拒答"
    ok += 1
    # 目录一致性检查：跨目录样本必须抛错（防 detect() 静默用错根）
    try:
        plan_from_extension([{"id": "z", "detector": "asan",
                              "files": ["a/x.cpp", "b/y.cpp"]}])
        raise AssertionError("跨目录未被拦截")
    except ValueError:
        ok += 1
    print(f"[reveal5-selftest] {ok} 项通过")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
