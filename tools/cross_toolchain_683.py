#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""cross_toolchain_683.py — 683-B：跨工具链 / 跨平台检出对比。

设计（诚实边界全部登记）
========================
* B1 跨编译器：**WSL clang++ 18.1.3 vs WSL g++ 13.3**（同平台不同编译器，真对比）。
  基线（g++ 侧）取自 676g 冻结判定矩阵（reuse，不重跑）；clang 侧本批实测：
  asan/ubsan × -O0/-O2 双档，判定字符串与 `holdout_reveal_661.detect` 的
  SAN 分支**逐字一致**（asan: AddressSanitizer/LeakSanitizer/detected memory leaks/
  double-free；ubsan: "runtime error"）——保证 τ 可比。
* MinGW clang++ 22 的 ASan **不可用**（缺 libclang_rt.asan_dynamic 运行库）——
  尝试记录在案，不上报为任何检出数字。
* MSVC 本机不存在（诚实登记，不伪造）。
* B2 跨平台：并发类样本 ≥50 条，Windows 原生（MinGW g++ 13.1，无 sanitizer）
  实测编译/运行/挂起，对照 676g 的 WSL 行为记录（hung_flag、tsan verdict）。
* 抽样：1147 全池**分层抽样**（按 defect_type 比例 + 固定种子 6831），
  挂起样本（hung_flag）自动跳过并等量替补（原因：两编译器下都是超时→miss，
  无对比信息量；登记跳过清单）。
* 增量 checkpoint（jsonl），可断点续跑。

用法
====
    python tools/cross_toolchain_683.py --stage b1 --limit 5      # 冒烟
    python tools/cross_toolchain_683.py --stage b1                # 200 条全量（后台）
    python tools/cross_toolchain_683.py --stage b2                # 跨平台 ≥50 条
    python tools/cross_toolchain_683.py --stage report            # 一致性 + 敏感性报告
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import random
import subprocess
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "blindspot_676g_detection_matrix.json"
EXP_DIR = ROOT / "data" / "holdout_expansion"
OUT_B1 = ROOT / "data" / "683_cross_toolchain_results.json"
OUT_B2 = ROOT / "data" / "683_cross_platform_results.json"
CKPT_B1 = ROOT / "data" / "683_b1_ckpt.jsonl"
CKPT_B2 = ROOT / "data" / "683_b2_ckpt.jsonl"
REPORT = ROOT / "data" / "683_toolchain_sensitivity_report.md"

SEED = 6831
N_B1 = 200
N_B2 = 50
OPT_LEVELS = ("-O0", "-O2")
#: 与 holdout_reveal_661.detect 的 SAN 分支逐字一致的命中判据
SAN = {"asan": "address", "ubsan": "undefined"}
CONC_TYPES = {"data_race", "race_condition", "memory_order", "atomic_ub",
              "aba_problem", "lock_priority_inversion", "condition_variable",
              "false_sharing", "deadlock"}


def _now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _log(msg: str) -> None:
    print(f"[683-B {_dt.datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def _jdump(path: Path, doc: dict) -> None:
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8", newline="\n")


def _to_wsl(path: Path) -> str:
    p = str(path).replace("\\", "/")
    if len(p) > 1 and p[1] == ":":
        p = "/mnt/" + p[0].lower() + p[2:]
    return p


def _wsl(cmd: str, timeout: int = 180) -> tuple[int, str]:
    try:
        r = subprocess.run(["wsl", "-e", "bash", "-lc", cmd], capture_output=True,
                           text=True, errors="replace", timeout=timeout)
        out = (r.stdout or "") + (r.stderr or "")
        out = "\n".join(ln for ln in out.splitlines() if "wsl:" not in ln[:6])
        return r.returncode, out
    except subprocess.TimeoutExpired:
        return -9, "TIMEOUT_EXPIRED"
    except Exception as e:  # noqa: BLE001
        return -1, f"wsl_error:{type(e).__name__}:{e}"


def sample_files(row: dict) -> list[Path]:
    """676g 样本行的磁盘文件定位（expA..expG；holdout 批不参与本抽样）。"""
    batch = row["source_batch"]
    d = EXP_DIR / batch
    out = []
    for f in row.get("files") or []:
        p = d / f
        if p.is_file():
            out.append(p)
    return out


def stratified_sample(rows: list[dict], n: int, seed: int) -> list[dict]:
    """按 defect_type 比例分层抽样；挂起样本跳过、等量替补。"""
    pool = [r for r in rows if r["source_batch"].startswith("exp")
            and not r.get("hung_flag") and r.get("files")]
    by_type: dict[str, list[dict]] = {}
    for r in pool:
        by_type.setdefault(r["defect_type"], []).append(r)
    rng = random.Random(seed)
    total = len(pool)
    picked: list[dict] = []
    for t in sorted(by_type):
        want = max(1, round(n * len(by_type[t]) / total))
        rng.shuffle(by_type[t])
        picked.extend(by_type[t][:want])
    rng.shuffle(picked)
    return picked[:n]


# ─────────────────────────────────────────────────────────────────────────────
# B1：clang 侧实测（判定与 661 SAN 分支逐字一致）
# ─────────────────────────────────────────────────────────────────────────────
def clang_detect(files: list[Path], kind: str) -> dict:
    san = SAN[kind]
    hits, tried, notes = [], [], []
    wfiles = " ".join(_to_wsl(f) for f in files)
    for opt in OPT_LEVELS:
        exe = f"/tmp/ct_{kind}_{opt.lstrip('-')}"
        rc_c, out_c = _wsl(f"clang++ -std=c++17 {opt} -g -fsanitize={san} -pthread "
                           f"{wfiles} -o {exe}", timeout=120)
        if rc_c != 0:
            notes.append(f"{opt} 编译失败:{out_c.strip()[:60]}")
            continue
        rc_r, out_r = _wsl(exe, timeout=120)
        tried.append(opt)
        low = out_r.lower()
        if kind == "asan":
            hit = ("AddressSanitizer" in out_r or "LeakSanitizer" in out_r
                   or "detected memory leaks" in low or "double-free" in low)
        else:
            hit = "runtime error" in out_r
        snip = out_r.strip().replace("\n", " ")[:160]
        if hit:
            hits.append(f"{opt}(rc={rc_r}) {snip}")
        else:
            notes.append(f"{opt}(rc={rc_r}) {snip or '无输出'}")
    if hits:
        return {"verdict": "catch", "note": "; ".join(hits)[:400], "tried": tried}
    if not tried:
        return {"verdict": "unknown", "note": "clang 不可用: " + "; ".join(notes)[:200],
                "tried": tried}
    return {"verdict": "miss", "note": "; ".join(notes)[:400], "tried": tried}


def stage_b1(limit: int | None = None) -> int:
    rows = json.loads(MATRIX.read_text(encoding="utf-8"))["samples"]
    picked = stratified_sample(rows, limit or N_B1, SEED)
    done: dict[str, dict] = {}
    if CKPT_B1.is_file():
        for ln in CKPT_B1.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                r = json.loads(ln)
                done[r["uid"]] = r
    _log(f"B1 抽样 {len(picked)} 条（分层 seed={SEED}），checkpoint {len(done)} 条")
    t0 = time.time()
    for i, row in enumerate(picked, 1):
        uid = row["uid"]
        if uid in done:
            continue
        files = sample_files(row)
        g_side = {a: {**row["per_asset"][a]} for a in ("asan", "ubsan")}
        rec = {"uid": uid, "defect_type": row["defect_type"], "files": [f.name for f in files],
               "gxx_676g": {a: g_side[a]["verdict"] for a in g_side},
               "gxx_source": "blindspot_676g_detection_matrix（WSL g++ 13.3，reuse）",
               "clang": {}}
        if not files:
            rec["skip_reason"] = "files 未找到"
            _log(f"{i}/{len(picked)} {uid} SKIP (files missing)")
            continue
        for kind in ("asan", "ubsan"):
            rec["clang"][kind] = clang_detect(files, kind)
        done[uid] = rec
        with CKPT_B1.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        a_c, u_c = rec["clang"]["asan"]["verdict"], rec["clang"]["ubsan"]["verdict"]
        _log(f"{i}/{len(picked)} {uid:<22} clang asan={a_c:<7} ubsan={u_c:<7} "
             f"[{time.time()-t0:.0f}s]")
    _log(f"B1 实测完成：{len(done)} 条")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# B2：跨平台（Windows 原生 vs WSL）
# ─────────────────────────────────────────────────────────────────────────────
def win_probe(files: list[Path]) -> dict:
    """Windows 原生 MinGW g++ 13.1：编译（-O0，无 sanitizer）→ 运行（10s 超时）。"""
    with tempfile.TemporaryDirectory() as td:
        exe = Path(td) / "wp.exe"
        cmd = ["g++", "-std=c++17", "-O0", "-g", "-pthread"] + [str(f) for f in files] + \
              ["-o", str(exe)]
        try:
            rc_c = subprocess.run(cmd, capture_output=True, text=True, errors="replace",
                                  timeout=120)
        except Exception as e:  # noqa: BLE001
            return {"compile": "error", "note": f"{type(e).__name__}"}
        if rc_c.returncode != 0:
            return {"compile": "error", "note": (rc_c.stderr or "")[:200]}
        t0 = time.perf_counter()
        try:
            rc_r = subprocess.run([str(exe)], capture_output=True, text=True,
                                  errors="replace", timeout=10)
            return {"compile": "ok",
                    "run": "normal_exit" if rc_r.returncode == 0 else f"crash_rc{rc_r.returncode}",
                    "wall_s": round(time.perf_counter() - t0, 2)}
        except subprocess.TimeoutExpired:
            return {"compile": "ok", "run": "hang_timeout10s",
                    "wall_s": round(time.perf_counter() - t0, 2)}


def stage_b2() -> int:
    rows = json.loads(MATRIX.read_text(encoding="utf-8"))["samples"]
    pool = [r for r in rows if r["source_batch"].startswith("exp")
            and r["defect_type"] in CONC_TYPES and r.get("files")]
    picked = stratified_sample(pool, N_B2, SEED + 1)
    done: dict[str, dict] = {}
    if CKPT_B2.is_file():
        for ln in CKPT_B2.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                r = json.loads(ln)
                done[r["uid"]] = r
    _log(f"B2 并发类样本 {len(picked)} 条（池 {len(pool)}，seed={SEED+1}）")
    t0 = time.time()
    for i, row in enumerate(picked, 1):
        uid = row["uid"]
        if uid in done:
            continue
        files = sample_files(row)
        rec = {"uid": uid, "defect_type": row["defect_type"],
               "hung_flag_676g": bool(row.get("hung_flag")),
               "tsan_676g": row["per_asset"].get("tsan", {}).get("verdict"),
               "windows_native": win_probe(files) if files else {"compile": "no_files"}}
        done[uid] = rec
        with CKPT_B2.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        _log(f"{i}/{len(picked)} {uid:<22} win={rec['windows_native'].get('run', '?')} "
             f"[{time.time()-t0:.0f}s]")
    _log(f"B2 完成：{len(done)} 条")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# 报告：一致性（κ）+ 工具链敏感性
# ─────────────────────────────────────────────────────────────────────────────
def cohen_kappa(pairs: list[tuple[str, str]], labels: tuple[str, ...]) -> float:
    n = len(pairs)
    if not n:
        return float("nan")
    po = sum(1 for a, b in pairs if a == b) / n
    pe = 0.0
    for lab in labels:
        pa = sum(1 for a, _ in pairs if a == lab) / n
        pb = sum(1 for _, b in pairs if b == lab) / n
        pe += pa * pb
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def stage_report() -> int:
    b1_rows = [json.loads(ln) for ln in CKPT_B1.read_text(encoding="utf-8").splitlines()
               if ln.strip()] if CKPT_B1.is_file() else []
    b2_rows = [json.loads(ln) for ln in CKPT_B2.read_text(encoding="utf-8").splitlines()
               if ln.strip()] if CKPT_B2.is_file() else []
    labels = ("catch", "miss", "unknown")
    res: dict = {"schema": "queyi-683-cross-toolchain/v1", "generated_at": _now(),
                 "environment": {
                     "clang_wsl": "Ubuntu clang 18.1.3", "gxx_wsl": "g++ 13.3.0",
                     "gxx_win": "MinGW g++ 13.1.0",
                     "mingw_clang_note": "MinGW clang 22.1 ASan 不可用（缺 libclang_rt.asan_dynamic）"
                                         "——尝试记录，不上报检出数字",
                     "msvc": "本机不存在（诚实登记）"},
                 "b1": {"n": len(b1_rows), "per_asset": {}}, "b2": {"n": len(b2_rows)}}
    for kind in ("asan", "ubsan"):
        pairs = [(r["gxx_676g"][kind], r["clang"][kind]["verdict"]) for r in b1_rows
                 if r.get("clang", {}).get(kind)]
        n = len(pairs)
        agree = sum(1 for a, b in pairs if a == b)
        g_catch = sum(1 for a, _ in pairs if a == "catch")
        c_catch = sum(1 for _, b in pairs if b == "catch")
        # 差异明细（最多 40 条）
        diffs = [{"uid": r["uid"], "defect_type": r["defect_type"],
                  "gxx": r["gxx_676g"][kind], "clang": r["clang"][kind]["verdict"],
                  "clang_note": r["clang"][kind]["note"][:150]}
                 for r in b1_rows if r.get("clang", {}).get(kind)
                 and r["gxx_676g"][kind] != r["clang"][kind]["verdict"]]
        res["b1"]["per_asset"][kind] = {
            "n": n, "agree": agree, "agree_pct": round(agree / n * 100, 2) if n else None,
            "kappa": round(cohen_kappa(pairs, labels), 4) if n else None,
            "gxx_catch": g_catch, "clang_catch": c_catch,
            "gxx_catch_pct": round(g_catch / n * 100, 2) if n else None,
            "clang_catch_pct": round(c_catch / n * 100, 2) if n else None,
            "delta_pp_clang_minus_gxx": round((c_catch - g_catch) / n * 100, 2) if n else None,
            "n_diff": len(diffs), "diffs": diffs[:40],
        }
    # B2 汇总
    if b2_rows:
        win_hang = sum(1 for r in b2_rows if r["windows_native"].get("run") == "hang_timeout10s")
        win_crash = sum(1 for r in b2_rows if str(r["windows_native"].get("run", "")).startswith("crash"))
        win_ok = sum(1 for r in b2_rows if r["windows_native"].get("run") == "normal_exit")
        win_cerr = sum(1 for r in b2_rows if r["windows_native"].get("compile") != "ok")
        tsan_catch = sum(1 for r in b2_rows if r["tsan_676g"] == "catch")
        res["b2"] = {"n": len(b2_rows), "windows_hang": win_hang, "windows_crash": win_crash,
                     "windows_normal": win_ok, "windows_compile_error": win_cerr,
                     "wsl_tsan_catch_676g": tsan_catch,
                     "note": "Windows 侧为无 sanitizer 的裸运行观测（挂起/崩溃/正常）；"
                             "WSL 侧 tsan 判定取自 676g（Linux 专属工具链）"}
    _jdump(OUT_B1, res)

    sens = res["b1"]["per_asset"]
    lines = ["# 683-B3 · 工具链敏感性报告（clang 18 vs g++ 13.3；Windows vs WSL）", "",
             "- 基线 = 676g 冻结矩阵（WSL g++ 13.3，双档 -O0/-O2，reuse 不重跑）",
             "- clang 侧 = 本批实测（Ubuntu clang 18.1.3，判定字符串与 661 SAN 分支逐字一致）", ""]
    if sens:
        lines.append("## 编译器一致性（asan / ubsan）\n")
        lines.append("| 资产 | n | 一致率 | Cohen's κ | g++ catch% | clang catch% | Δ(clang−g++) | 差异条数 |")
        lines.append("|---|---:|---:|---:|---:|---:|---:|---:|")
        for kind in ("asan", "ubsan"):
            s = sens[kind]
            lines.append(f"| {kind} | {s['n']} | {s['agree_pct']}% | {s['kappa']} | "
                         f"{s['gxx_catch_pct']} | {s['clang_catch_pct']} | "
                         f"{s['delta_pp_clang_minus_gxx']}pp | {s['n_diff']} |")
        maxdiff = max(abs(sens[k]["delta_pp_clang_minus_gxx"] or 0) for k in sens)
        lines.append(f"\n- **最大检出差异：{maxdiff}pp**；"
                     f"{'⚠️ >10pp，须在论文 limitations 强调' if maxdiff > 10 else '≤10pp，工具链敏感性有限（如实报告）'}")
    if b2_rows:
        b = res["b2"]
        lines.append(f"\n## 跨平台（Windows 原生 vs WSL，n={b['n']} 并发类样本）\n")
        lines.append(f"- Windows 原生裸运行：正常退出 {b['windows_normal']} / 崩溃 {b['windows_crash']} / "
                     f"挂起(10s 超时) {b['windows_hang']} / 编译失败 {b['windows_compile_error']}")
        lines.append(f"- 同一批样本 WSL 侧 tsan（676g）：catch {b['wsl_tsan_catch_676g']}/{b['n']}")
        lines.append(f"- 结论：{b['note']}")
    REPORT.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    _log(f"报告 → {REPORT.relative_to(ROOT).as_posix()}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=("b1", "b2", "report"), required=True)
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    if a.stage == "b1":
        return stage_b1(limit=a.limit)
    if a.stage == "b2":
        return stage_b2()
    return stage_report()


if __name__ == "__main__":
    sys.exit(main())
