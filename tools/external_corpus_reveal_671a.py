#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""external_corpus_reveal_671a.py — 671a C2：d3e-* 扩样（20 条）的 reveal。

为什么要单起一轮
================
669d 把 20 条 d3e-* 并入 canonical corpus（`external_corpus_665.json` 60 条），
但**没有重跑 reveal** ⇒ 现有 `data/external_corpus_reveal_665.json` 的分母只覆盖并入前的 40 条。
直接重跑 `external_corpus_reveal_665.py` 会把 20 条不知情的样本按"没检出"记账（重演 665 的静默掉分），
所以本工具**另起一轮**、只测新样本，并把历史 40 条的落盘结论**复用**（逐行标 `source`）。

判据（"只有一个版本"原则）
========================
* 非 sanitizer 类（compiler-warn / wunsequenced / cross-compile / measure / unknown）
  **委托** `tools/external_corpus_662.py::detect` 原实现 —— 不另造"命中"定义；
* sanitizer 类（asan/ubsan/tsan）：662 的旧实现只跑单档 `-O1`，与 holdout 侧
  （`rv661`：`-O0`+`-O2` 双档 + `setarch -R` 关 ASLR）**不同口径**。本轮按 671a 受理单
  把新样本统一到**双档 + setarch -R**，命中字符串仍逐字沿用 662 的判据
  （ASan/LeakSanitizer/`double-free`/TSan/`rc==66`）。
  口径改了 ⇒ 与 665 的数字**不可直接比大小**，报告里单列 `caliber_change` 说明。

分层（669d `env_dependency.declared`：**禁止合并成一个数**）
=========================================================
按 `expected_detector` 分六层：`sanitizer` / `compiler-warn` / `cross-compile` /
`perf` / `compile-time` / `other`；每层单独给 (k/n, CP 95%)。
665 的 A/B/C 分层与本次六层**不是同一口径**，映射表写在产物 `layer_mapping` 里。

用法
====
    python tools/external_corpus_reveal_671a.py                 # 跑 d3e-*，连跑 3 次
    python tools/external_corpus_reveal_671a.py --samples d3e-01,d3e-02 --runs 1
    python tools/external_corpus_reveal_671a.py --selftest

已知限制（诚实登记）
====================
* d3e-* 是 669d 在 reveal 之后并入的 ⇒ **不具备盲态**；只用于增大样本量。
* `perf` / `compile-time` 两类本机无检测器 ⇒ 记 `unknown`（不是 miss，不进分母）。
  "本机无检测器"与"检测器报不出"在报告里必须可区分（这正是 662 那条猜测的判据）。
* 历史 40 条不重测（复用 reveal_665 落盘）；判据一旦变，`tools/guard_rerun_671a.py` 会要求重跑。
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import os
import subprocess
import tempfile
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
HERE = Path(__file__).resolve().parent
CORPUS_665 = ROOT / "data" / "external_corpus" / "external_corpus_665.json"
CORPUS_669D = ROOT / "data" / "external_corpus" / "external_corpus_669d.json"
R665 = ROOT / "data" / "external_corpus_reveal_665.json"
OUT = ROOT / "data" / "external_corpus_reveal_671a.json"
DETAIL = ROOT / "data" / "external_corpus" / "reveal_detail_671a.json"
DEFAULT_SAMPLES = "d3e-01-d3e-20"
N_RUNS = 3

#: 本轮六层口径（受理单指定）；665 的 A/B/C 映射见 660→671a 的 `layer_mapping`
LAYERS = ("sanitizer", "compiler-warn", "cross-compile", "perf", "compile-time", "other")
DETECTOR_LAYER = {
    "asan": "sanitizer", "ubsan": "sanitizer", "tsan": "sanitizer",
    "compiler-warn": "compiler-warn", "wunsequenced": "compiler-warn",
    "cross-compile": "cross-compile",
    "perf-counter": "perf",
    "compile-time": "compile-time",
}
SAN = {"tsan": "thread", "asan": "address", "ubsan": "undefined"}
#: 665 A/B/C → 671a 六层（**不是同一口径**，只为给人看对照，不用于合并统计）
LAYER_MAPPING = {
    "A_local": ["sanitizer", "compiler-warn"],
    "B_cross_or_measure": ["cross-compile", "other（measure/unknown）"],
    "C_no_local_detector": ["other（unknown）"],
}


def _to_wsl(p: str) -> str:
    q = p.replace("\\", "/")
    return ("/mnt/" + q[0].lower() + q[2:]) if len(q) > 1 and q[1] == ":" else q


def _sh(cmd: list[str], timeout: int = 180) -> tuple[int, str]:
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:  # noqa: BLE001
        return -1, f"EXC: {type(e).__name__}: {e}"


def _wsl(cmd: str, timeout: int = 180) -> tuple[int, str]:
    return _sh(["wsl", "-e", "bash", "-lc", cmd], timeout)


_SETARCH: str | None = None


def setarch_prefix() -> str:
    """`setarch -R`（关 ASLR）：668 起 TSan 在高熵 ASLR 下会 `FATAL: unexpected memory mapping`，
    同一夹具时而 catch、时而 unknown。关 ASLR 是把**测量**变成可复现的测量（不是让检测器更容易报）。"""
    global _SETARCH
    if _SETARCH is None:
        rc, _ = _wsl("command -v setarch")
        _SETARCH = "setarch -R " if rc == 0 else ""
    return _SETARCH


def load_ex662():
    spec = importlib.util.spec_from_file_location("ex662", HERE / "external_corpus_662.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def load_stat_bounds():
    spec = importlib.util.spec_from_file_location("stat_bounds", HERE / "stat_bounds.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def jload(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


# ─────────────────────────────────────────────────────────────────────────────
# 判据：sanitizer 双档（新口径），其余委托 662
# ─────────────────────────────────────────────────────────────────────────────

def detect_san_double_opt(kind: str, code: str, opt_levels: tuple[str, ...] = ("-O0", "-O2")) -> tuple[str, str]:
    """双档 sanitizer：任一档报出即 catch；两档都不可用 ⇒ unknown（不误记 miss）。"""
    d = tempfile.mkdtemp(prefix="d3e_")
    try:
        src = os.path.join(d, "s.cpp")
        Path(src).write_text(code, encoding="utf-8")
        w = _to_wsl(src)
        tried: list[str] = []
        hits: list[str] = []
        notes: list[str] = []
        unavail: list[str] = []
        for opt in opt_levels:
            exe = f"/tmp/d3e_{kind}_{opt.lstrip('-')}"
            cmd = f"g++ -std=c++17 {opt} -g -fsanitize={SAN[kind]} -pthread {w} -o {exe}"
            rc, out = _wsl(cmd)
            if rc != 0:
                unavail.append(f"{opt} 编译失败: {out.strip()[:80]}")
                continue
            rc, out = _wsl(setarch_prefix() + exe, timeout=120)
            low = out.lower()
            if kind == "tsan" and "FATAL: ThreadSanitizer" in out:
                unavail.append(f"{opt} TSan 无法初始化（已试 setarch -R）")
                continue
            tried.append(opt)
            # 命中字符串逐字沿用 ex662.detect（判据不另造）
            hit = (("ThreadSanitizer" in out or "data race" in low or rc == 66) if kind == "tsan"
                   else any(s in out for s in ("AddressSanitizer", "LeakSanitizer", "runtime error")))
            if hit:
                hits.append(f"{opt}(rc={rc}) {out.strip()[:80]}")
            else:
                notes.append(f"{opt}(rc={rc})")
        if hits:
            return ("catch", f"{kind} 命中[{'; '.join(hits)}]（档位 {','.join(tried)}）")
        if not tried:
            return ("unknown", f"检测器不可用({kind})：{'; '.join(unavail)[:140]}")
        return ("miss", f"{kind} 两档均无报告[{'; '.join(notes)}]")
    finally:
        import shutil
        shutil.rmtree(d, ignore_errors=True)


def detect_671a(kind: str, code: str | None) -> tuple[str, str]:
    """统一入口：sanitizer 走双档；其余**委托** ex662.detect（同一个"命中"定义）。"""
    if kind in SAN:
        if not code:
            return ("unknown", "无代码片段")
        return detect_san_double_opt(kind, code)
    return load_ex662().detect(kind, code)


def layer_of(kind: str | None) -> str:
    return DETECTOR_LAYER.get(str(kind or ""), "other")


def measure_once(samples: list[dict]) -> list[dict]:
    rows: list[dict] = []
    for s in samples:
        k = str(s.get("expected_detector"))
        v, note = detect_671a(k, s.get("code"))
        rows.append({"id": s["id"], "category": s.get("category"),
                     "detector": k, "layer": layer_of(k), "verdict": v,
                     "note": str(note)[:200]})
        print(f"  {s['id']:<8} {v.upper():<10} {k:<14} {str(note)[:56]}")
    return rows


def merge_runs(ids: list[str], runs: list[list[dict]]) -> list[dict]:
    by_id: dict[str, list[dict]] = {}
    for run in runs:
        for r in run:
            by_id.setdefault(r["id"], []).append(r)
    out: list[dict] = []
    for sid in ids:
        rs = by_id.get(sid, [])
        vs = [r["verdict"] for r in rs]
        first = rs[0] if rs else {"detector": "unknown", "layer": "other", "note": "未跑",
                                  "category": None}
        out.append({**first, "id": sid, "verdict": vs[0] if vs else "unknown",
                    "verdicts_per_run": vs,
                    "reproducible": bool(vs) and len(set(vs)) == 1})
    return out


# ─────────────────────────────────────────────────────────────────────────────
# 统计
# ─────────────────────────────────────────────────────────────────────────────

def tally(rows: list[dict]) -> dict[str, Any]:
    c = m = u = ne = 0
    for r in rows:
        v = r["verdict"]
        if v == "catch":
            c += 1
        elif v == "miss":
            m += 1
        elif v == "not_error":
            ne += 1
        else:
            u += 1
    den = c + m
    return {"total": len(rows), "catch": c, "miss": m, "unknown": u, "not_error": ne,
            "denominator": {"value": den, "meaning": "catch+miss（可测且非测量类）",
                            "excluded": {"unknown": u, "not_error": ne},
                            "all_samples": len(rows)},
            "detect_rate_pct": round(c / den * 100, 1) if den else None}


def cp(k: int, n: int, conf: float = 0.95) -> dict[str, Any]:
    if n <= 0:
        return {"k": k, "n": n, "point": None, "cp_low": None, "cp_high": None,
                "conf": conf, "note": "n=0 ⇒ 拒绝给率（fail-loud）"}
    p = load_stat_bounds().proportion(k, n, conf)
    return {"k": k, "n": n, "point": p["point"], "cp_low": p["cp_low"],
            "cp_high": p["cp_high"], "conf": conf}


def by_layer(rows: list[dict]) -> dict[str, Any]:
    out: dict[str, Any] = {}
    for lay in LAYERS:
        sub = [r for r in rows if r["layer"] == lay]
        if not sub:
            continue
        t = tally(sub)
        t["cp95"] = cp(t["catch"], t["denominator"]["value"])
        t["detectors"] = sorted({r["detector"] for r in sub})
        out[lay] = t
    return out


def env_probe() -> dict[str, Any]:
    import sys

    rc, wsl_gpp = _wsl("g++ --version | head -1")
    _, local_gpp = _sh(["g++", "--version"])
    _, local_clang = _sh(["clang++", "--version"])
    wsl_ok = rc == 0 and "g++" in wsl_gpp
    return {
        "wsl_available": wsl_ok,
        "wsl_gpp": (wsl_gpp.strip().splitlines() or ["(不可用)"])[0],
        "local_gpp": (local_gpp.strip().splitlines() or ["(不可用)"])[0],
        "local_clang": (local_clang.strip().splitlines() or ["(不可用)"])[0],
        "host": sys.platform,
        "python": sys.version.split()[0],
        "setarch": setarch_prefix().strip() or "(不可用)",
        "caliber_warning": ("WSL 不可用 ⇒ sanitizer 层会整层降级为 unknown（669d env_dependency 警告的形态）"
                            if not wsl_ok else ""),
    }


# ─────────────────────────────────────────────────────────────────────────────
# 主流程
# ─────────────────────────────────────────────────────────────────────────────

def split_range(part: str, all_ids: list[str]) -> tuple[str, str] | None:
    """把 `d3e-01-d3e-20` 拆成 (lo, hi)；不是范围（单个 id）⇒ None。

    不能用 `partition("-")`：corpus 的 id 自身带 `-`（`d3e-01`），
    必须在每个 `-` 位置试探、只接受两半都是已知 id 的切法。
    """
    if part in all_ids:
        return None
    for i, ch in enumerate(part):
        if ch != "-" or i == 0 or i == len(part) - 1:
            continue
        lo, hi = part[:i].strip(), part[i + 1:].strip()
        if lo in all_ids and hi in all_ids:
            return lo, hi
    raise SystemExit(f"--samples 无法解析（既不是已知 id，也不是「id-id」范围）：{part}")


def parse_samples(spec: str, all_ids: list[str]) -> list[str]:
    spec = (spec or "").strip()
    if spec in ("", "all"):
        return list(all_ids)
    want: set[str] = set()
    for part in spec.split(","):
        part = part.strip()
        if not part:
            continue
        rng = split_range(part, all_ids)
        if rng is None:
            want.add(part)
            continue
        i, j = all_ids.index(rng[0]), all_ids.index(rng[1])
        if i > j:
            raise SystemExit(f"--samples 范围反序：{part}")
        want.update(all_ids[i:j + 1])
    return [s for s in all_ids if s in want]


def run(ids: list[str], runs_n: int, write: bool = True) -> dict[str, Any]:
    c = jload(CORPUS_665)
    samples = {str(s["id"]): s for s in c["samples"]}
    missing = [i for i in ids if i not in samples]
    if missing:
        raise SystemExit(f"corpus 里没有这些样本：{missing}")
    # 669d 声明的 20 条必须与本轮请求一致（否则是"换了样本却没换口径"）
    declared = [str(x) for x in (c.get("extend_669d") or {}).get("added_ids", [])]
    undeclared = [i for i in ids if i not in declared]
    if undeclared:
        raise SystemExit(f"这些样本不在 extend_669d.added_ids 里（拒绝把历史样本算成本轮扩样）：{undeclared}")

    env = env_probe()
    all_runs: list[list[dict]] = []
    for i in range(max(1, runs_n)):
        print(f"[run {i + 1}/{max(1, runs_n)}] d3e-* {len(ids)} 条")
        all_runs.append(measure_once([samples[i2] for i2 in ids]))
    rows = merge_runs(ids, all_runs)

    r665 = jload(R665) if R665.is_file() else {}
    r665_map = {str(x["id"]): x for x in r665.get("results", [])}
    hist = [{"id": sid, "detector": str(r665_map[sid].get("detector")),
             "layer": layer_of(r665_map[sid].get("detector")),
             "verdict": str(r665_map[sid].get("verdict")),
             "note": str(r665_map[sid].get("note", ""))[:200],
             "category": r665_map[sid].get("category"),
             "verdicts_per_run": [r665_map[sid].get("verdict")], "reproducible": None,
             "source": "reused_reveal_665"}
            for sid in samples if sid not in set(ids) and sid in r665_map]
    for r in rows:
        r["source"] = "measured_671a"
    cand = rows + hist
    cum_ids = ids + [h["id"] for h in hist]

    new_t, cum_t = tally(rows), tally(cand)
    new_l, cum_l = by_layer(rows), by_layer(cand)
    cum_t["cp95"] = cp(cum_t["catch"], cum_t["denominator"]["value"])
    new_t["cp95"] = cp(new_t["catch"], new_t["denominator"]["value"])
    unstable = [r["id"] for r in rows if not r["reproducible"]]

    rep: dict[str, Any] = {
        "schema": "queyi-external-corpus-reveal/671a",
        "generated_by": "tools/external_corpus_reveal_671a.py",
        "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
        "round_label": f"{ids[0]}–{ids[-1]}（{len(ids)} 条，669d 扩样补充样本）",
        "runs": max(1, runs_n),
        "samples_requested": ids,
        "detector_reuse": ("非 sanitizer 类委托 tools/external_corpus_662.py::detect（同一命中定义）；"
                           "sanitizer 类用双档 -O0/-O2 + setarch -R，命中字符串逐字沿用 662 的判据"),
        "caliber": ("真错分母 = catch+miss（可测且非测量类）；unknown（本机无检测器）与 not_error"
                    "（测量类，本就不是缺陷）均不进分母；禁止把六层合并成一个数（669d declared）"),
        "layers": list(LAYERS),
        "layer_mapping": LAYER_MAPPING,
        "caliber_change": {
            "what": ("665 的 sanitizer 判据是**单档 -O1 且未关 ASLR**；本轮新样本改用"
                     "-O0/-O2 双档 + setarch -R（与 holdout rv661 对齐）"),
            "why": "单档会把『被优化掉整段内存操作』的夹具记成假 miss；ASLR 抖动会把同一夹具记成 unknown",
            "consequence": "本轮与 665 的数字**不可直接比大小**（口径变了），只能描样本构成",
        },
        "historical_reuse": {
            "from": R665.relative_to(ROOT).as_posix(),
            "ids": [h["id"] for h in hist],
            "why": "判据未变 ⇒ 历史结论复用；本轮不重跑、不覆盖 reveal_665 的落盘",
        },
        "env": env,
        "new_samples": new_t,
        "new_by_layer": new_l,
        "cumulative": cum_t,
        "cumulative_by_layer": cum_l,
        "compare_reveal_665": {
            "before_total": (r665.get("total")),
            "before_denominator": (r665.get("denominator") or {}).get("value"),
            "before_rate_pct": r665.get("detect_rate_pct"),
            "after_total": cum_t["total"],
            "after_denominator": cum_t["denominator"]["value"],
            "after_rate_pct": cum_t["detect_rate_pct"],
            "note": "分母扩大且口径变更 ⇒ 两轮数字不可直接比大小（见 caliber_change）",
        },
        "reproducibility": {"runs": max(1, runs_n), "unstable_samples": unstable,
                            "all_reproducible": not unstable},
        "honest_note": ("d3e-* 是 669d 在 reveal 之后并入的 ⇒ **不具备盲态**，只用于增大样本量；"
                        "`perf` / `compile-time` 两层本机无检测器 ⇒ 记 unknown（不是 miss）。"
                        "率必须**分层**引用（669d env_dependency.declared）。"),
        "detail": DETAIL.relative_to(ROOT).as_posix(),
    }
    detail = {
        "schema": "queyi-external-corpus-reveal-detail/671a",
        "generated_by": "tools/external_corpus_reveal_671a.py",
        "generated_at": rep["generated_at"],
        "summary_for": OUT.relative_to(ROOT).as_posix(),
        "samples_requested": ids,
        "runs": max(1, runs_n),
        "caliber": rep["caliber"],
        "env": env,
        "per_sample": [{**r, "is_669d_new": r["id"] in set(ids),
                        "verified_source": samples.get(r["id"], {}).get("verified_source")}
                       for r in cand],
        "order": cum_ids,
        "new_summary": new_t, "cumulative_summary": cum_t,
        "unstable_samples": unstable,
        "note": ("`verdicts_per_run` 是每轮原始结论；`reproducible=false` 说明结论随环境抖动。"
                 "`source` 标明该行是**本轮实测**还是**复用 reveal_665**。"),
    }
    if write:
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(rep, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        DETAIL.parent.mkdir(parents=True, exist_ok=True)
        DETAIL.write_text(json.dumps(detail, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return rep


def render(rep: dict[str, Any]) -> str:
    n, cu = rep["new_samples"], rep["cumulative"]
    L = [f"[corpus reveal 671a] {rep['round_label']}  连跑 {rep['runs']} 次  "
         f"WSL={'可用' if rep['env']['wsl_available'] else '不可用'}  {rep['env']['setarch']}",
         f"  新样本 catch={n['catch']} miss={n['miss']} unknown={n['unknown']} "
         f"not_error={n['not_error']} ⇒ 可测 {n['denominator']['value']}，率={n['detect_rate_pct']}%",
         f"  累计   catch={cu['catch']} miss={cu['miss']} unknown={cu['unknown']} "
         f"not_error={cu['not_error']} ⇒ 可测 {cu['denominator']['value']}，率={cu['detect_rate_pct']}%"]
    for lay, d in sorted(rep["cumulative_by_layer"].items()):
        L.append(f"    {lay:<16} 可测 {d['denominator']['value']}/{d['total']}  "
                 f"率={d['detect_rate_pct']}%")
    if rep["reproducibility"]["unstable_samples"]:
        L.append(f"  [警告] 结论不稳：{rep['reproducibility']['unstable_samples']}")
    if rep["env"]["caliber_warning"]:
        L.append(f"  [警告] {rep['env']['caliber_warning']}")
    return "\n".join(L)


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    ids = ["d3e-01", "d3e-02", "d3e-03"]
    chk("parse_samples 逗号", parse_samples("d3e-01,d3e-03", ids) == ["d3e-01", "d3e-03"])
    chk("parse_samples 区间", parse_samples("d3e-01-d3e-02", ids) == ["d3e-01", "d3e-02"])
    chk("layer_of 六层映射", layer_of("asan") == "sanitizer" and layer_of("perf-counter") == "perf"
        and layer_of("compile-time") == "compile-time" and layer_of("measure") == "other"
        and layer_of("unknown") == "other")
    t = tally([{"verdict": "catch"}, {"verdict": "miss"}, {"verdict": "unknown"},
               {"verdict": "not_error"}])
    chk("tally 分母 = catch+miss", t["denominator"]["value"] == 2)
    chk("tally not_error 不进分母", t["not_error"] == 1 and t["unknown"] == 1)
    c = jload(CORPUS_665)
    d = jload(CORPUS_669D)
    declared = set((c.get("extend_669d") or {}).get("added_ids") or [])
    chk("669d 声明的 20 条与扩展文件条数一致",
        len(declared) == 20 and len(d["samples"]) == 20)
    chk("扩展样本都在 canonical corpus 里",
        all(str(s["id"]) in {str(x["id"]) for x in c["samples"]} for s in d["samples"]))
    chk("每层都有归属（无 None）", all(layer_of(s.get("expected_detector")) in LAYERS
                                        for s in d["samples"]))
    chk("n=0 拒绝给率", cp(0, 0)["point"] is None)
    print(f"external_corpus_reveal_671a selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671a C2：d3e-* 扩样的 reveal")
    ap.add_argument("--samples", default=DEFAULT_SAMPLES, help=f"默认 {DEFAULT_SAMPLES}")
    ap.add_argument("--runs", type=int, default=N_RUNS, help=f"连跑次数（默认 {N_RUNS}）")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--no-write", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)

    if a.selftest:
        return selftest()

    c = jload(CORPUS_665)
    all_ids = [str(s["id"]) for s in c["samples"]]
    ids = parse_samples(a.samples, all_ids)
    rep = run(ids, a.runs, write=not a.no_write)
    print()
    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        print(render(rep))
    if not a.no_write:
        print(f"已写 {OUT.relative_to(ROOT).as_posix()}")
        print(f"已写 {DETAIL.relative_to(ROOT).as_posix()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
