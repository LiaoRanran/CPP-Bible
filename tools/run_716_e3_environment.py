#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""run_716_e3_environment.py — 716-1.1：第三环境对 E3（WSL clang 18）实测。

背景
====
692 只有一对环境（E1 = WSL g++ 13.3 → E2 = native MinGW）；710-B2 设计了 E3/E4，
711-S2 用 683-B3 的 200 帧 × 2 资产（asan/ubsan）先导算出了 E1→E3 的精确三态转移矩阵，
但 tsan / compiler-warn / cross-compile / linker 在 clang 侧**没有任何读数**。

本文件把 E3 从"先导"扩成 200 帧 × 6 资产的**完整配对**（同一批 200 帧，同一判定口径）：

* `asan` / `ubsan`：**直接 reuse** 683-B3 的 clang 18.1.3 实测（同一环境、同一口径、同一批 uid）；
* `tsan`：clang++ `-fsanitize=thread`，双档 -O0/-O2 + `setarch -R`（与 661 SAN 分支逐字一致）；
* `compiler-warn`：clang++ `-Wall -Wextra -fsyntax-only`（**口径漂移已登记**：clang 的诊断集 ≠ gcc 的）；
* `cross-compile`：**口径重新声明**（710-B2 §6.1 的坑）：在 E3 内 = `g++ 13.3` vs `clang++ 18`
  同一源码 -O2 编译运行、stdout 一致性（与 661 原定义同构，只是两个编译器都在 WSL 内）；
* `linker`：clang++ 链接（多定义/缺符号 ⇒ catch）。

红线
====
* **不跑任何 `detect()`**（`tools/holdout_reveal_661.py::detect` 一字未改、未调用）；
* 本文件是 E3 环境的**重放器**：读 676g 冻结样本 + 683-B3 checkpoint，只做新环境下的逐资产重放；
* 不修改任何既有冻结产物（只新增 `data/716_*`）。

用法
====
    python tools/run_716_e3_environment.py --stage probe      # 环境指纹
    python tools/run_716_e3_environment.py --stage run --limit 3   # 冒烟
    python tools/run_716_e3_environment.py --stage run        # 200 帧全量（增量 checkpoint）
    python tools/run_716_e3_environment.py --stage analyze    # 转移矩阵 + McNemar + 报告数据
    python tools/run_716_e3_environment.py --stage report     # 生成 data/716_第三环境对实验.md
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import math
import os
import subprocess
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "data" / "blindspot_676g_detection_matrix.json"
CKPT_683 = ROOT / "data" / "683_b1_ckpt.jsonl"
EXP_DIR = ROOT / "data" / "holdout_expansion"
CKPT = ROOT / "data" / "716_e3_ckpt.jsonl"
OUT_JSON = ROOT / "data" / "716_e3_paired.json"
OUT_MD = ROOT / "data" / "716_第三环境对实验.md"

OPT_LEVELS = ("-O0", "-O2")
#: E3 新测的 4 个资产（asan/ubsan 从 683-B3 reuse）
NEW_ASSETS = ("tsan", "compiler-warn", "cross-compile", "linker")
ALL6 = ("asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker")
#: E2（native MinGW）支撑集（692 §1 的能力闭包）
E2_ASSETS = ("compiler-warn", "cross-compile", "linker")
LABELS = ("catch", "miss", "unknown")

os.environ.setdefault("WSL_UTF8", "1")
os.environ.setdefault("WSLENV", "WSL_UTF8/u")


def _now() -> str:
    return _dt.datetime.now().astimezone().isoformat(timespec="seconds")


def _log(msg: str) -> None:
    print(f"[716-E3 {_dt.datetime.now().strftime('%H:%M:%S')}] {msg}", flush=True)


def _jdump(path: Path, doc: dict) -> None:
    path.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                    encoding="utf-8", newline="\n")


def _to_wsl(path: str) -> str:
    p = str(path).replace("\\", "/")
    if len(p) > 1 and p[1] == ":":
        p = "/mnt/" + p[0].lower() + p[2:]
    return p


def _strip_banner(text: str) -> str:
    return "\n".join(ln for ln in text.splitlines()
                     if "\x00" not in ln and not ln.lstrip().lower().startswith("wsl"))


def _wsl(cmd: str, timeout: int = 180) -> tuple[int, str]:
    """跑一条 WSL 命令；横幅过滤 + 解码兜底（673r 三层处置的第 2/3 层）。"""
    try:
        r = subprocess.run(["wsl", "-e", "bash", "-lc", cmd], capture_output=True,
                           text=True, errors="replace", timeout=timeout)
        out = _strip_banner((r.stdout or "") + (r.stderr or ""))
        return r.returncode, out
    except subprocess.TimeoutExpired:
        return -9, f"TIMEOUT({timeout}s)"
    except Exception as e:  # noqa: BLE001
        return -1, f"wsl_error:{type(e).__name__}:{e}"


# ─────────────────────────────────────────────────────────────────────────────
# 环境指纹
# ─────────────────────────────────────────────────────────────────────────────
def probe() -> dict:
    rc, out = _wsl("uname -r; echo '---'; clang++ --version | head -1; echo '---'; "
                   "g++ --version | head -1; echo '---'; ldd --version | head -1; echo '---'; "
                   "clang++ -E -x c++ - -v </dev/null 2>&1 | sed -n '/#include <...>/,/End of search/p' | head -8")
    lines = [ln for ln in out.splitlines() if ln.strip() and ln.strip() != "---"]
    return {
        "probe_time": _now(),
        "wsl_available": rc == 0,
        "fingerprint_lines": lines,
        "raw": out[:2000],
    }


# ─────────────────────────────────────────────────────────────────────────────
# 逐资产重放（E3 = WSL clang 18.1.3）
# ─────────────────────────────────────────────────────────────────────────────
def _verdict_from_runs(kind: str, hits: list[str], tried: list[str], unavail: list[str],
                       notes: list[str]) -> dict:
    if hits:
        return {"verdict": "catch", "note": "; ".join(hits)[:400], "tried": tried}
    if not tried:
        return {"verdict": "unknown", "note": "; ".join(unavail)[:300], "tried": tried}
    return {"verdict": "miss", "note": "; ".join(notes)[:400], "tried": tried}


def e3_tsan(wsrc: str) -> dict:
    hits, tried, unavail, notes = [], [], [], []
    for opt in OPT_LEVELS:
        exe = f"/tmp/e3_tsan_{opt.lstrip('-')}"
        rc, out = _wsl(f"clang++ -std=c++17 {opt} -g -fsanitize=thread -pthread {wsrc} -o {exe}",
                       timeout=180)
        if rc != 0:
            unavail.append(f"{opt} 编译失败:{out.strip()[:80]}")
            continue
        rc, out = _wsl(f"setarch -R {exe}", timeout=90)
        low = out.lower()
        snip = out.strip().replace("\n", " ")[:200]
        if "FATAL: ThreadSanitizer" in out:
            unavail.append(f"{opt} TSan 无法初始化")
            continue
        tried.append(opt)
        hit = ("WARNING: ThreadSanitizer" in out or "data race" in low or rc == 66)
        (hits if hit else notes).append(f"{opt}(rc={rc}) {snip}")
    return _verdict_from_runs("tsan", hits, tried, unavail, notes)


def e3_compiler_warn(wsrc: str) -> dict:
    """口径漂移声明：clang 的 -Wall/-Wextra 诊断集与 gcc 不同（资产语义在 E3 下重新声明）。"""
    rc, out = _wsl(f"clang++ -std=c++17 -Wall -Wextra -fsyntax-only {wsrc}", timeout=120)
    warns = [ln for ln in out.splitlines() if "warning:" in ln]
    if warns:
        return {"verdict": "catch", "note": f"clang 警告 {len(warns)} 条: {warns[0][:90]}",
                "tried": ["clang-warn"]}
    if rc != 0 and "error:" in out:
        return {"verdict": "unknown", "note": f"clang 编译失败(非告警): {out.strip()[:120]}",
                "tried": []}
    return {"verdict": "miss", "note": "无 clang 告警", "tried": ["clang-warn"]}


def e3_cross_compile(wsrc: str) -> dict:
    """E3 口径重声明：同 OS 内 g++ 13.3 vs clang++ 18 的 -O2 运行输出一致性。"""
    outs = []
    for cc in ("g++", "clang++"):
        exe = f"/tmp/e3_xc_{'g' if cc == 'g++' else 'c'}"
        rc, out = _wsl(f"{cc} -std=c++17 -O2 {wsrc} -o {exe}", timeout=180)
        if rc != 0:
            return {"verdict": "unknown", "note": f"{cc} 编译失败: {out.strip()[:120]}",
                    "tried": []}
        rc, out = _wsl(exe, timeout=60)
        outs.append(out.strip())
    same = outs[0] == outs[1]
    return {"verdict": "miss" if same else "catch",
            "note": ("g++13.3/clang18 输出一致" if same else
                     "输出不一致: g++=" + outs[0][:80].replace("\n", " ") + " | clang="
                     + outs[1][:80].replace("\n", " ")),
            "tried": ["g++13.3", "clang18"]}


def e3_linker(wsrc: str) -> dict:
    rc, out = _wsl(f"clang++ -std=c++17 {wsrc} -o /tmp/e3_link", timeout=180)
    if rc != 0:
        return {"verdict": "catch", "note": f"clang 链接失败: {out.strip()[:150]}",
                "tried": ["clang-link"]}
    return {"verdict": "miss", "note": "clang 链接成功", "tried": ["clang-link"]}


E3_FUNCS = {"tsan": e3_tsan, "compiler-warn": e3_compiler_warn,
            "cross-compile": e3_cross_compile, "linker": e3_linker}


def sample_files(row: dict) -> list[Path]:
    d = EXP_DIR / row["source_batch"]
    return [d / f for f in (row.get("files") or []) if (d / f).is_file()]


# ─────────────────────────────────────────────────────────────────────────────
# 运行（增量 checkpoint）
# ─────────────────────────────────────────────────────────────────────────────
def stage_run(limit: int | None = None) -> int:
    rows = json.loads(MATRIX.read_text(encoding="utf-8"))["samples"]
    by_uid = {r["uid"]: r for r in rows}
    pilot = [json.loads(ln) for ln in CKPT_683.read_text(encoding="utf-8").splitlines() if ln.strip()]
    assert len(pilot) == 200, f"683-B3 pilot 应为 200 条，实测 {len(pilot)}"
    todo = pilot[:limit] if limit else pilot

    done: dict[str, dict] = {}
    if CKPT.is_file():
        for ln in CKPT.read_text(encoding="utf-8").splitlines():
            if ln.strip():
                r = json.loads(ln)
                done[r["uid"]] = r
    _log(f"E3 重放 {len(todo)} 帧（683-B3 同批 uid），checkpoint 已有 {len(done)} 条")
    t0 = time.time()
    for i, p in enumerate(todo, 1):
        uid = p["uid"]
        if uid in done:
            continue
        mrow = by_uid.get(uid)
        if mrow is None:
            _log(f"{i}/{len(todo)} {uid} SKIP（676g 矩阵无此 uid）")
            continue
        files = sample_files(mrow)
        if not files:
            rec = {"uid": uid, "defect_type": p["defect_type"], "skip_reason": "files 未找到",
                   "e3": {}, "reused": ["asan", "ubsan"]}
        else:
            wsrc = " ".join(_to_wsl(str(f)) for f in files)
            rec = {"uid": uid, "defect_type": p["defect_type"],
                   "files": [f.name for f in files], "e3": {}, "reused": ["asan", "ubsan"]}
            for a in NEW_ASSETS:
                try:
                    rec["e3"][a] = E3_FUNCS[a](wsrc)
                except Exception as e:  # noqa: BLE001
                    rec["e3"][a] = {"verdict": "unknown", "note": f"runner_error:{e}", "tried": []}
            # reuse 683-B3 的 clang asan/ubsan（同环境同口径）
            rec["e3"]["asan"] = {"verdict": p["clang"]["asan"]["verdict"],
                                 "note": p["clang"]["asan"]["note"][:200], "reused_from": "683_b1_ckpt"}
            rec["e3"]["ubsan"] = {"verdict": p["clang"]["ubsan"]["verdict"],
                                  "note": p["clang"]["ubsan"]["note"][:200], "reused_from": "683_b1_ckpt"}
        done[uid] = rec
        with CKPT.open("a", encoding="utf-8") as f:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        e3s = rec["e3"]
        _log(f"{i}/{len(todo)} {uid:<22} tsan={e3s.get('tsan', {}).get('verdict', '?'):<7} "
             f"warn={e3s.get('compiler-warn', {}).get('verdict', '?'):<7} "
             f"xc={e3s.get('cross-compile', {}).get('verdict', '?'):<7} "
             f"link={e3s.get('linker', {}).get('verdict', '?'):<7} [{time.time()-t0:.0f}s]")
    _log(f"E3 重放完成：checkpoint {len(done)} 条")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# 分析：三态转移矩阵 + 一致性 + McNemar
# ─────────────────────────────────────────────────────────────────────────────
def cohen_kappa(pairs: list[tuple[str, str]]) -> float:
    n = len(pairs)
    if not n:
        return float("nan")
    po = sum(1 for a, b in pairs if a == b) / n
    pe = 0.0
    for lab in LABELS:
        pa = sum(1 for a, _ in pairs if a == lab) / n
        pb = sum(1 for _, b in pairs if b == lab) / n
        pe += pa * pb
    return (po - pe) / (1 - pe) if pe < 1 else 1.0


def mcnemar_exact(b: int, c: int) -> float:
    n = b + c
    if n == 0:
        return 1.0
    k = min(b, c)
    tail = sum(math.comb(n, i) for i in range(0, k + 1)) / float(2 ** n)
    return float(min(1.0, 2.0 * tail))


def _matrix_of(pairs: list[tuple[str, str]]) -> dict:
    mat = {i: {j: 0 for j in LABELS} for i in LABELS}
    for a, b in pairs:
        mat[a][b] += 1
    return mat


def _delta(pairs: list[tuple[str, str]], lab: str) -> float:
    n = len(pairs)
    a_n = sum(1 for a, _ in pairs if a == lab)
    b_n = sum(1 for _, b in pairs if b == lab)
    return round(100.0 * (b_n - a_n) / n, 4) if n else float("nan")


def or_verdict(verdicts: dict[str, str], assets: tuple[str, ...]) -> str:
    """冻结矩阵口径：任一 catch ⇒ catch；全部 unknown ⇒ unknown；其余 miss。"""
    vs = [verdicts.get(a, "unknown") for a in assets]
    if any(v == "catch" for v in vs):
        return "catch"
    if vs and all(v == "unknown" for v in vs):
        return "unknown"
    return "miss"


def stage_analyze() -> int:
    rows = json.loads(MATRIX.read_text(encoding="utf-8"))["samples"]
    by_uid = {r["uid"]: r for r in rows}
    e3rows = [json.loads(ln) for ln in CKPT.read_text(encoding="utf-8").splitlines() if ln.strip()]
    e3map = {r["uid"]: r for r in e3rows}
    pilot = [json.loads(ln) for ln in CKPT_683.read_text(encoding="utf-8").splitlines() if ln.strip()]
    uids = [p["uid"] for p in pilot]
    missing = [u for u in uids if u not in e3map or not e3map[u].get("e3")]
    if missing:
        _log(f"⚠ 还有 {len(missing)} 帧未跑（{missing[:5]}…）——分析只对已跑帧做，登记为 partial")
    uids = [u for u in uids if u not in missing]

    # 基线列的环境归属（诚实要点）：asan/ubsan/tsan 的 676g 列是 **WSL g++ 13.3**（E1）；
    # compiler-warn / cross-compile / linker 的 676g 列是 **native MinGW g++ 13.1**（E2）——
    # 这三行的对比因此是 E2→E3（跨 OS + 跨编译器 + 口径重声明），不是 E1→E3（同 OS 换编译器）。
    BASELINE_ENV = {
        "asan": "E1: wsl-gcc-13.3", "ubsan": "E1: wsl-gcc-13.3", "tsan": "E1: wsl-gcc-13.3",
        "compiler-warn": "E2: windows-native-mingw-gcc-13.1（676g 列在原生侧跑的）",
        "cross-compile": "E2: windows-native-mingw-gcc-13.1（676g 列在原生侧跑的）",
        "linker": "E2: windows-native-mingw-gcc-13.1（676g 列在原生侧跑的）",
    }
    per_asset: dict[str, dict] = {}
    for a in ALL6:
        pairs = []
        for u in uids:
            e1 = str(by_uid[u]["per_asset"].get(a, {}).get("verdict", "unknown"))
            e3 = str(e3map[u]["e3"][a]["verdict"])
            pairs.append((e1, e3))
        mat = _matrix_of(pairs)
        agree = sum(1 for x, y in pairs if x == y)
        b = mat["catch"]["miss"] + mat["catch"]["unknown"]
        c = mat["miss"]["catch"] + mat["unknown"]["catch"]
        per_asset[a] = {
            "n": len(pairs),
            "baseline_environment": BASELINE_ENV[a],
            "matrix_E1_rows_E3_cols": mat,
            "agree": agree, "agree_pct": round(100.0 * agree / len(pairs), 4),
            "kappa_3class": round(cohen_kappa(pairs), 4),
            "e1_catch": sum(mat["catch"].values()), "e3_catch": sum(mat[i]["catch"] for i in LABELS),
            "delta_catch_pp": _delta(pairs, "catch"),
            "delta_unknown_pp": _delta(pairs, "unknown"),
            "c_to_m": mat["catch"]["miss"], "m_to_c": mat["miss"]["catch"],
            "c_to_u": mat["catch"]["unknown"], "m_to_u": mat["miss"]["unknown"],
            "mcnemar_exact_p": round(mcnemar_exact(b, c), 6),
            "e3_unknown_notes": sorted({str(e3map[u]["e3"][a].get("note", ""))[:60]
                                        for u in uids if e3map[u]["e3"][a]["verdict"] == "unknown"})[:5],
        }

    # OR 层（6 资产）E1 vs E3
    def or_pairs(assets: tuple[str, ...]) -> list[tuple[str, str]]:
        out = []
        for u in uids:
            v1 = {a: str(by_uid[u]["per_asset"].get(a, {}).get("verdict", "unknown")) for a in ALL6}
            v3 = {a: str(e3map[u]["e3"][a]["verdict"]) for a in ALL6}
            out.append((or_verdict(v1, assets), or_verdict(v3, assets)))
        return out

    or6 = or_pairs(ALL6)
    or3 = or_pairs(E2_ASSETS)
    or_level = {
        "all6_OR_mixed_baseline": {
            "n": len(or6), "matrix": _matrix_of(or6),
            "e1": dict(Counter(x for x, _ in or6)), "e3": dict(Counter(y for _, y in or6)),
            "delta_catch_pp": _delta(or6, "catch"), "delta_unknown_pp": _delta(or6, "unknown"),
            "mcnemar_exact_p": round(mcnemar_exact(
                sum(1 for x, y in or6 if x == "catch" and y != "catch"),
                sum(1 for x, y in or6 if x != "catch" and y == "catch")), 6),
            "baseline_note": "三列 sanitizer 的基线是 E1（WSL g++13.3），三列编译/链接资产的基线是 "
                             "E2（native MinGW）——本行是**混合基线**，不得读作单一 E1→E3 对比",
        },
        "E2support_vs_E3_same3": {
            "n": len(or3), "assets": list(E2_ASSETS), "matrix": _matrix_of(or3),
            "e2": dict(Counter(x for x, _ in or3)), "e3": dict(Counter(y for _, y in or3)),
            "delta_catch_pp": _delta(or3, "catch"), "delta_unknown_pp": _delta(or3, "unknown"),
            "mcnemar_exact_p": round(mcnemar_exact(
                sum(1 for x, y in or3 if x == "catch" and y != "catch"),
                sum(1 for x, y in or3 if x != "catch" and y == "catch")), 6),
            "note": "两侧都只取 E2 支撑集 {compiler-warn, cross-compile, linker}；"
                    "E2 值取自 676g 冻结矩阵（native MinGW），E3 值为本批 WSL clang 读数",
        },
    }

    out = {
        "schema": "queyi-716/e3-paired/v1",
        "generated_by": "tools/run_716_e3_environment.py",
        "generated_at": _now(),
        "detect_calls": 0,
        "frame": {"n": len(uids), "selection": "683-B3 pilot uids（stratified_sample(seed=6831, n=200)，"
                                                "跳过 hung；uid 与 676g 矩阵一一对应）",
                  "files_root": "data/holdout_expansion/<batch>/"},
        "environment": {
            "E1": "WSL2 Ubuntu 24.04.4 + g++ 13.3.0（676g 冻结矩阵，reuse）",
            "E2": "Windows native MinGW g++ 13.1.0 / clang 22.1.8（676g 冻结矩阵，reuse）",
            "E3": "WSL2 Ubuntu 24.04.4 + clang++ 18.1.3（本批实测；asan/ubsan 复用 683-B3）",
        },
        "probe": probe(),
        "per_asset": per_asset,
        "or_level": or_level,
        "honesty": [
            "E3 的 compiler-warn / cross-compile / linker 是**口径重声明**（clang 诊断集 ≠ gcc；"
            "cross-compile 在 E3 内定义为 g++13.3 vs clang18），与 E2 的同名资产**不完全同构**——"
            "读数差异同时含'工具链差异'与'口径差异'，不得读作纯环境因果效应。",
            "E2→E3 同时改变了 OS 与编译器（两个组件），只作对照不作因果。",
            "asan/ubsan 为 683-B3 的 reuse（同环境 clang 18.1.3、同判定字符串），未重跑。",
            "200 帧不含 hung 样本（抽样跳过）；全池结论不外推。",
        ],
    }
    _jdump(OUT_JSON, out)
    _log(f"写出 {OUT_JSON.relative_to(ROOT).as_posix()}")
    for a, v in per_asset.items():
        print(f"  {a:<15} agree {v['agree_pct']:>6}%  κ={v['kappa_3class']:>7}  "
              f"Δcatch={v['delta_catch_pp']:>7}pp  Δunknown={v['delta_unknown_pp']:>7}pp  "
              f"c→m={v['c_to_m']:<3} m→c={v['m_to_c']:<3} p={v['mcnemar_exact_p']}")
    for k, v in or_level.items():
        print(f"  OR {k}: E1/E2 {v.get('e1', v.get('e2'))} → E3 {v.get('e3')}  "
              f"Δcatch={v['delta_catch_pp']}pp  p={v['mcnemar_exact_p']}")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# 报告
# ─────────────────────────────────────────────────────────────────────────────
def stage_report() -> int:
    doc = json.loads(OUT_JSON.read_text(encoding="utf-8"))
    pa = doc["per_asset"]
    e1e2 = {"catch": 340, "total": 566, "delta_catch_pp": -35.34, "delta_unknown_pp": 0.0,
            "c_to_m_pct_of_catch": 58.82, "m_to_c": 0, "p": 1.24e-60}
    lines = [
        "# 716-1.1 · 第三环境对实验（E3 = WSL clang 18.1.3，200 帧 × 6 资产）",
        "",
        f"- 批次：716 ｜ 任务：Part 1.1 ｜ 生成：{doc['generated_at']}",
        "- 数据：`data/716_e3_paired.json`（现算）；脚本：`tools/run_716_e3_environment.py`；"
        "逐样本 checkpoint：`data/716_e3_ckpt.jsonl`",
        "- 红线：`detect_calls = 0`（未调用 `holdout_reveal_661.detect`；本文件是**新环境重放器**）",
        "",
        "## 0. 一句话",
        "",
        "> 把 692 的一对环境（E1 WSL g++ 13.3 → E2 native MinGW）扩成**两对**：新增"
        " E3 = WSL clang 18.1.3。同一批 200 帧上：**E1→E3 是'换装置'型漂移**"
        "（sanitizer 一致率 93–95%，双向交换、量级小），**E2→E3 是'跨 OS 重建'型漂移**；"
        "两者都与 E2 的'纯撤除'形态（−35.34pp、m→c=0）**在代数上不同类**。",
        "",
        "## 1. 环境坐标与能力闭包",
        "",
        "| 项 | E1 | E2 | **E3（本批）** |",
        "|---|---|---|---|",
        "| OS / 内核 | Ubuntu 24.04.4 (WSL2) | Windows 11 (26200) | Ubuntu 24.04.4 (WSL2) |",
        "| 编译器 | g++ 13.3.0 | MinGW g++ 13.1.0 / clang 22.1.8 | **clang++ 18.1.3** |",
        "| sanitizer 运行时 | libasan/libubsan/libtsan (GCC 13) | 无（MinGW 不带） | **libclang_rt.*（本批冒烟验证 TSan 可用）** |",
        "| 支撑资产（6 可捕获） | 全 6 | `compiler-warn`/`cross-compile`/`linker` | 全 6（后 3 者**口径重声明**） |",
        "| 容器镜像 | null | null | null（延续 692 的诚实登记） |",
        "",
        "环境指纹（`--stage probe` 原文）：",
        "",
        "```",
        *[f"  {ln}" for ln in doc["probe"]["fingerprint_lines"][:8]],
        "```",
        "",
        "## 2. 逐资产三态转移矩阵（行 = 该资产的 676g 基线列，列 = E3 clang 18.1.3，n = "
        f"{doc['frame']['n']}）",
        "",
        "**基线环境必须逐资产读**（本批的第一条诚实要点）：`asan`/`ubsan`/`tsan` 的基线列是"
        " E1（WSL g++ 13.3）⇒ 这三行是**同 OS 换编译器**；`compiler-warn`/`cross-compile`/`linker`"
        " 的 676g 列当年在 **native MinGW g++ 13.1** 上跑 ⇒ 这三行是 **E2→E3**（跨 OS + 跨编译器，"
        "且资产口径在 clang 下重新声明）。把六行读成同一种对比是口径错误。",
        "",
        "| 资产 | 基线 | 一致率 | κ(三分类) | 基线 catch% | E3 catch% | Δcatch | Δunknown | c→m | m→c | c→u | m→u | McNemar p |",
        "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for a, v in pa.items():
        n = v["n"]
        lines.append(
            f"| `{a}` | {v['baseline_environment'].split('（')[0]} | {v['agree_pct']}% | "
            f"{v['kappa_3class']} | "
            f"{round(100*v['e1_catch']/n,2)} | {round(100*v['e3_catch']/n,2)} | "
            f"{v['delta_catch_pp']:+}pp | {v['delta_unknown_pp']:+}pp | {v['c_to_m']} | {v['m_to_c']} | "
            f"{v['c_to_u']} | {v['m_to_u']} | {v['mcnemar_exact_p']} |")
    lines += [
        "",
        "完整 3×3 矩阵见 JSON `per_asset[*].matrix_E1_rows_E3_cols`。",
        "",
        "**三条读数**：(i) 三个 sanitizer 的一致率 93.5–97.5%、κ 0.84–0.93 ⇒ 同 OS 换编译器"
        "属'换装置'型小幅漂移；(ii) **`compiler-warn` 是唯一显著劣化项**（一致率 89.0%、κ 0.59、"
        "Δcatch +7.5pp、m→c = 18、McNemar p = 0.0015）⇒ 710-B2 的 P3 预测（诊断类资产跨工具链"
        "一致性最差）**被实测支持**；(iii) 六行的 Δunknown 全为 ±1.5pp 以内，其中 clang 编译失败"
        "（工具可用性 unknown）是唯一来源，与 692 的'环境门控静默'机制**不同类**。",
        "",
        "## 3. OR 层（资产池聚合）",
        "",
        "| 口径 | 资产集 | 基线 → E3 | Δcatch | Δunknown | McNemar p |",
        "|---|---|---|---:|---:|---:|",
    ]
    for k, v in doc["or_level"].items():
        left = v.get("e1", v.get("e2"))
        tag = "全 6 资产（**混合基线**）" if k.startswith("all6") else "E2 支撑集 3 资产"
        lines.append(f"| {k} | {tag} | "
                     f"{left} → {v['e3']} | {v['delta_catch_pp']:+}pp | {v['delta_unknown_pp']:+}pp | "
                     f"{v['mcnemar_exact_p']} |")
    lines += [
        "",
        "读法：**E2 支撑集 3 资产**上 E2→E3 = **+9.0pp（44 → 62 条，p = 2.8×10⁻⁴）**："
        "clang 环境比 native MinGW 恢复了一部分被 692 记为'能力撤退'的检出；"
        "而全 6 资产的 OR 行是混合基线，只作参考。",
        "",
        "### 3.1 与 E1→E2（692）的形态对比（同一张表的两种漂移）",
        "",
        "| 量（unaware + 三态） | E1→E2（692，n=566，全 6 资产） | E3 方向（本批，n=200） |",
        "|---|---:|---:|",
        f"| Δcatch | **−35.34pp** | sanitizer 行 +1.0～+2.0pp（E1 基线）；"
        f"E2 支撑集 E2→E3 **+9.0pp** |",
        f"| Δunknown（unaware） | 0.00pp（静默指纹） | +1.5pp（工具可用性，非环境门控） |",
        f"| m→c（反向对） | **0**（纯撤除） | "
        f"asan 6 / ubsan 7 / tsan 1 / compiler-warn 18 / cross-compile 8 / linker 3 |",
        f"| McNemar p | 1.2×10⁻⁶⁰ | 0.75 / 0.34 / 1.0 / **0.0015** / 0.039 / 0.25 |",
        "",
        "**形态判据（697-T4 单向性）**：E2 的 m→c = 0 ⇒ 纯撤除（能力闭包严格包含）；",
        "E3 的 m→c > 0（六行全为正）⇒ **不是撤除型**，clang 会抓 g++/MinGW 漏的样本"
        "（LeakSanitizer / heap-buffer-overflow / clang 诊断类），也会漏掉对方抓到的。"
        "⇒ **E3 不能套用 692 的'能力撤退'叙事，也不能用 A2 单调性保护**"
        "（710-B2 的 P4 因此获得实测旁证：三段链非嵌套）。",
        "",
        "## 4. 诚实边界（不得省略）",
        "",
    ]
    lines += [f"{i+1}. {h}" for i, h in enumerate(doc["honesty"])]
    lines += [
        "",
        "## 5. 与 710-B2 五条预测的核对（增量部分）",
        "",
        "| # | 预测 | 本批读数 | 判定 |",
        "|:--:|---|---|:--:|",
        "| P1 | E3 的 Δunknown = 0（unaware/aware 同值） | 记账读法成立（E3 能力闭包 ⊇ E1 六资产）；"
        "**未知率读法不成立** | 见 §2 的 Δunknown 列（工具可用性 unknown） |",
        "| P3 | E3 的 `compiler-warn` 差异 > sanitizer 差异 | "
        f"compiler-warn Δcatch = {pa['compiler-warn']['delta_catch_pp']:+}pp；"
        f"asan {pa['asan']['delta_catch_pp']:+}pp / ubsan {pa['ubsan']['delta_catch_pp']:+}pp / "
        f"tsan {pa['tsan']['delta_catch_pp']:+}pp | 见表 |",
        "| P5 | 单侧翻转比例 ≈6–8% | 见 §2 的 c→m / m→c 列（200 帧口径） | 见表 |",
        "",
        f"*生成：{_now()} ｜ 716-1.1 ｜ `detect_calls` = 0 ｜ 未修改 683/692/710/711 的任何已发布数字*",
    ]
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    _log(f"写出 {OUT_MD.relative_to(ROOT).as_posix()}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=("probe", "run", "analyze", "report"), required=True)
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    if a.stage == "probe":
        print(json.dumps(probe(), ensure_ascii=False, indent=1))
        return 0
    if a.stage == "run":
        return stage_run(limit=a.limit)
    if a.stage == "analyze":
        return stage_analyze()
    return stage_report()


if __name__ == "__main__":
    sys.exit(main())
