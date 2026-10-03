#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""blindspot_676g_runner.py — 676g：全量样本 × 8 资产判定矩阵生成器。

红线遵守
========
* 不修改 tools/holdout_reveal_661.py（仅 importlib 加载，detect() 一字未动）。
* 不修改 tools/detect_for_assets.py（仅复用其函数）。
* 不修改任何样本（data/holdout_expansion/ 只读）。
* 本文件自身放在 data/ 下，属本批自己的文件。

设计要点（为什么这样调度）
==========================
1. **复用**：原 105 样本（holdout 41 + corpus 64）复用 673r 归属矩阵
   （data/experiments/asset_attribution_673r.json，同日同环境生成），
   另抽 10 条做当日复跑一致性验证（qa 子命令）。
2. **本地资产并行**：compiler-warn / wunsequenced / cross-compile / linker
   全部走本机 MinGW g++ / clang++，各自独立临时目录，无共享状态 ⇒ 多进程安全。
3. **sanitizer 串行**：asan/ubsan/tsan 走 WSL，detect() 把二进制写到**固定路径**
   /tmp/rv_bin_O0、/tmp/rv_bin_O2 ⇒ 两个进程并发调 detect 会互相覆写二进制、
   在"编译完成→exec 启动"窗口内误执对方样本 ⇒ 非挂起样本必须串行。
4. **挂起样本专用并行池**：expE 34 个 hung=true（自旋死锁/自死锁/cv 永久等待，
   全部无堆访问）+ expG sample_G019（CVE-2022-0778 无限循环）。
   这 35 条在 sanitizer 下无论跑哪个二进制结果都是"挂起→120s 超时→无报告→miss"，
   互相误执不改变可观测量 ⇒ 可以并行（本文件头部论证 + qa 抽检兜底）。
   QA：任何非 miss 判定 ⇒ 串行独占复跑；另抽 10% miss 串行复跑对一致性。
5. **TSan 稳定性**：非挂起并发样本跑 3 次取众数；挂起样本为确定性超时，
   不烧 3×（诚实记录，不做伪装的重复）。

用法
====
    python data/blindspot_676g_runner.py manifest     # 生成样本清单
    python data/blindspot_676g_runner.py local        # 并行本地资产（后台）
    python data/blindspot_676g_runner.py san          # 串行 sanitizer（后台）
    python data/blindspot_676g_runner.py hung         # 并行挂起池（须在 san 之后）
    python data/blindspot_676g_runner.py qa           # QA 复跑 + 105 复用验证
    python data/blindspot_676g_runner.py merge        # 合并 → 判定矩阵 JSON
"""
from __future__ import annotations

import argparse
import datetime as _dt
import glob
import json
import multiprocessing as mp
import os
import random
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent          # .../data
ROOT = HERE.parent                              # 仓库根
TOOLS = ROOT / "tools"
sys.path.insert(0, str(TOOLS))

EXP_DIRS = {f"exp{c}": ROOT / "data" / "holdout_expansion" / f"exp{c}"
            for c in "ABCDEFG"}
MANIFEST_OUT = HERE / "blindspot_676g_sample_manifest.json"
MATRIX_OUT = HERE / "blindspot_676g_detection_matrix.json"
ATTR_673R = ROOT / "data" / "experiments" / "asset_attribution_673r.json"

CKPT = {
    "local": HERE / "blindspot_676g_ckpt_local.jsonl",
    "san": HERE / "blindspot_676g_ckpt_san.jsonl",
    "hung": HERE / "blindspot_676g_ckpt_hung.jsonl",
    "qa": HERE / "blindspot_676g_ckpt_qa.jsonl",
}

LOCAL_ASSETS = ["compiler-warn", "wunsequenced", "cross-compile", "linker"]
SAN_ASSETS = ["asan", "ubsan", "tsan"]
ALL_ASSETS = SAN_ASSETS + LOCAL_ASSETS + ["compile-time"]
CONC_TYPES = {"data_race", "race_condition", "memory_order", "atomic_ub",
              "aba_problem", "lock_priority_inversion", "condition_variable",
              "false_sharing"}
# 挂起池：expE hung=true 的 34 条 + expG 无限循环 1 条（结构论证见文件头）
HUNG_TYPES = {"infinite_loop"}

_W = None  # worker 进程内的 rv661 模块句柄


def _log(msg: str) -> None:
    print(f"[676g { _dt.datetime.now().strftime('%H:%M:%S') }] {msg}",
          flush=True)


# ─────────────────────────────────────────────────────────────────────────────
# 样本清单
# ─────────────────────────────────────────────────────────────────────────────
def _exp_files(d: Path, sid: str) -> list[str]:
    """一条扩样样本的全部源文件（多 TU / 头文件一并带上，detect 会拷进同一临时目录）。

    批次命名差异：expD/expF 的磁盘文件是 sample_<id>.cpp，其余批次直接用 <id>.cpp。
    """
    fs: list[str] = []
    for prefix in (sid, f"sample_{sid}"):
        for pat in (f"{prefix}.cpp", f"{prefix}*.cpp", f"{prefix}*.h", f"{prefix}*.hpp"):
            fs.extend(os.path.basename(p) for p in glob.glob(str(d / pat)))
        if fs:
            break
    return sorted(set(fs))


def _holdout_types() -> dict[str, str]:
    types: dict[str, str] = {}
    for rel in ("data/holdout/holdout.json", "data/holdout/holdout_extension_669d.json",
                "data/holdout/holdout_extension_672h.json"):
        p = ROOT / rel
        if not p.is_file():
            continue
        doc = json.loads(p.read_text(encoding="utf-8"))
        for s in doc.get("seeds", []):
            types.setdefault(str(s["id"]), str(s.get("category", "unknown")))
    return types


def build_manifest() -> list[dict]:
    rows: list[dict] = []
    # 1) 原 105：复用 673r 归属矩阵的样本规格
    attr = json.loads(ATTR_673R.read_text(encoding="utf-8"))
    h_types = _holdout_types()
    for ds in ("holdout", "corpus"):
        for r in attr["datasets"][ds]["samples"]:
            sid = str(r["id"])
            if ds == "holdout":
                if sid not in h_types:
                    raise KeyError(f"holdout 样本 {sid} 在 holdout.json/extensions 里找不到类型")
                dtype = h_types[sid]
            else:
                dtype = str(r.get("category", "unknown"))
            rows.append({
                "uid": f"{ds}:{sid}", "sample_id": sid,
                "source_batch": ds, "defect_type": dtype,
                "planted": True if ds == "holdout" else None,
                "expected_verdict": str(r.get("recorded_verdict", "")),
                "input_mode": str(r.get("input_mode", "")),
                "dir": str(r.get("dir", "")), "files": list(r.get("files", [])),
                "run_mode": "reuse_673r", "hung_flag": False,
            })
    # 2) 扩样 1042：各批 INDEX
    for exp in ("expA", "expB", "expC", "expD", "expE", "expF", "expG"):
        idx = json.loads((EXP_DIRS[exp] / "INDEX.json").read_text(encoding="utf-8"))
        entries = idx.get("index") or idx.get("samples") or []
        n = 0
        for e in entries:
            sid = str(e.get("id") or e.get("sample_id"))
            files = _exp_files(EXP_DIRS[exp], sid)
            if not files:
                raise FileNotFoundError(f"{exp}/{sid} 找不到任何源文件")
            notes = ""
            if exp == "expE":  # 挂起样本的缺陷说明（报告用）
                per = EXP_DIRS[exp] / f"{sid}.json"
                if per.is_file():
                    notes = str(json.loads(per.read_text(encoding="utf-8"))
                                .get("notes", ""))
            hung = bool(e.get("hung", False))
            dtype = str(e["defect_type"])
            if dtype in HUNG_TYPES:      # expG 无限循环等
                hung = True
            rows.append({
                "uid": f"{exp}:{sid}", "sample_id": sid,
                "source_batch": exp, "defect_type": dtype,
                "planted": bool(e.get("planted", True)),
                "expected_verdict": str(e.get("expected_verdict", "")),
                "input_mode": "disk_fixtures",
                "dir": f"data/holdout_expansion/{exp}", "files": files,
                "run_mode": "fresh", "hung_flag": hung,
                "notes": notes,
            })
            n += 1
        _log(f"manifest {exp}: {n} 条")
    return rows


def cmd_manifest(_limit: int | None = None) -> int:
    rows = build_manifest()
    from collections import Counter
    by_batch = Counter(r["source_batch"] for r in rows)
    hung = [r["sample_id"] for r in rows if r["hung_flag"]]
    doc = {
        "schema": "queyi-blindspot-manifest/676g",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "total": len(rows),
        "by_batch": dict(by_batch),
        "hung_pool": hung,
        "hung_pool_reason": ("expE INDEX hung=true（自旋死锁/自死锁/cv 永久等待，"
                             "结构上无堆访问）+ defect_type=infinite_loop（CVE-2022-0778）；"
                             "这些样本 sanitizer 真实判据=挂起→120s 超时→无报告→miss，"
                             "互相误执不改变可观测量，故并行安全，QA 抽检兜底"),
        "samples": rows,
    }
    MANIFEST_OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                            encoding="utf-8", newline="\n")
    _log(f"manifest 总数={len(rows)} 批次={dict(by_batch)} 挂起池={len(hung)}")
    _log(f"写入 {MANIFEST_OUT.relative_to(ROOT).as_posix()}")
    return 0


def _load_manifest() -> list[dict]:
    doc = json.loads(MANIFEST_OUT.read_text(encoding="utf-8"))
    return doc["samples"]


# ─────────────────────────────────────────────────────────────────────────────
# checkpoint 工具
# ─────────────────────────────────────────────────────────────────────────────
def _append(path: Path, obj: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(obj, ensure_ascii=False) + "\n")
        f.flush()


def _done_keys(path: Path) -> set[tuple]:
    done: set[tuple] = set()
    if not path.is_file():
        return done
    for ln in path.read_text(encoding="utf-8").splitlines():
        ln = ln.strip()
        if not ln:
            continue
        try:
            o = json.loads(ln)
        except json.JSONDecodeError:
            continue
        done.add((o["sample_id"], o["asset"], o.get("run", 1)))
    return done


def _cell(sample: dict, asset: str, verdict: str, note: str, wall: float,
          run: int = 1, extra: dict | None = None) -> dict:
    o = {"sample_id": sample["uid"], "sid": sample["sample_id"],
         "source_batch": sample["source_batch"],
         "asset": asset, "run": run, "verdict": str(verdict),
         "note": str(note)[:400], "wall_seconds": round(wall, 3),
         "ts": _dt.datetime.now().astimezone().isoformat(timespec="seconds")}
    if extra:
        o.update(extra)
    return o


# ─────────────────────────────────────────────────────────────────────────────
# 本地资产并行池
# ─────────────────────────────────────────────────────────────────────────────
def _local_worker_init() -> None:
    global _W
    from detect_for_assets import load_rv661
    _W = load_rv661()


def _local_task(task: dict) -> dict:
    from detect_for_assets import detect_one_asset, SampleSpec, ROOT
    sid, bdir, files, asset = task["sample_id"], task["dir"], task["files"], task["asset"]
    spec = SampleSpec(id=task["uid"], dataset=task["source_batch"], dir=bdir,
                      files=tuple(files))
    t0 = time.perf_counter()
    r = detect_one_asset(_W, spec, asset, atoms_root=str(ROOT / bdir))
    return _cell(task, asset, r["verdict"], r["note"],
                 time.perf_counter() - t0)


def cmd_local(limit: int | None) -> int:
    rows = [r for r in _load_manifest() if r["run_mode"] == "fresh"]
    if limit:
        rows = rows[:limit]
    done = _done_keys(CKPT["local"])
    tasks = [{"uid": r["uid"], "sample_id": r["sample_id"],
              "source_batch": r["source_batch"],
              "dir": r["dir"], "files": r["files"], "asset": a}
             for r in rows for a in LOCAL_ASSETS
             if (r["uid"], a, 1) not in done]
    _log(f"local: 待跑 {len(tasks)} / 共 {len(rows) * len(LOCAL_ASSETS)} 格")
    if not tasks:
        return 0
    t0 = time.perf_counter()
    with mp.Pool(processes=6, initializer=_local_worker_init) as pool:
        for i, cell in enumerate(pool.imap_unordered(_local_task, tasks, chunksize=4), 1):
            _append(CKPT["local"], cell)
            if i % 100 == 0 or i == len(tasks):
                el = time.perf_counter() - t0
                _log(f"local {i}/{len(tasks)} ({el:.0f}s, "
                     f"{el / i:.2f}s/格)")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# sanitizer 串行主池（非挂起扩样样本）
# ─────────────────────────────────────────────────────────────────────────────
def cmd_san(limit: int | None) -> int:
    from detect_for_assets import (decode_safety, detect_one_asset, load_rv661,
                                   SampleSpec, ROOT)
    rows = [r for r in _load_manifest()
            if r["run_mode"] == "fresh" and not r["hung_flag"]]
    if limit:
        rows = rows[:limit]
    done = _done_keys(CKPT["san"])
    rv = load_rv661()
    n_cells = sum(1 for r in rows for a in SAN_ASSETS
                  if (r["sample_id"], a, 1) not in done)
    _log(f"san: 非挂起样本 {len(rows)}，待跑约 {n_cells} 格（串行）")
    t0 = time.perf_counter()
    n_done = 0
    with decode_safety() as env_info:
        _log(f"san 适配层 L1_effect={env_info.get('L1_effect')}")
        for i, r in enumerate(rows, 1):
            spec = SampleSpec(id=r["uid"], dataset=r["source_batch"],
                              dir=r["dir"], files=tuple(r["files"]))
            for asset in SAN_ASSETS:
                if (r["uid"], asset, 1) in done:
                    continue
                t1 = time.perf_counter()
                res = detect_one_asset(rv, spec, asset,
                                       atoms_root=str(ROOT / r["dir"]))
                cell = _cell(r, asset, res["verdict"], res["note"],
                             time.perf_counter() - t1)
                _append(CKPT["san"], cell)
                n_done += 1
                # TSan 稳定性：并发类型样本再跑 2 次（众数）
                if asset == "tsan" and r["defect_type"] in CONC_TYPES:
                    for run in (2, 3):
                        t2 = time.perf_counter()
                        res2 = detect_one_asset(rv, spec, asset,
                                                atoms_root=str(ROOT / r["dir"]))
                        _append(CKPT["san"], _cell(r, asset, res2["verdict"],
                                                   res2["note"],
                                                   time.perf_counter() - t2,
                                                   run=run))
            if i % 25 == 0 or i == len(rows):
                el = time.perf_counter() - t0
                eta = el / max(n_done, 1) * (n_cells - n_done)
                _log(f"san {i}/{len(rows)} {r['uid']} "
                     f"({el:.0f}s, ETA {eta / 60:.0f}m)")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# 挂起样本并行池（论证见文件头）
# ─────────────────────────────────────────────────────────────────────────────
def _hung_worker_init() -> None:
    global _W
    from detect_for_assets import decode_safety, load_rv661
    _W = load_rv661()
    _W._ctx676g = decode_safety()          # worker 生命周期内常驻，进程退出即释放
    _W._info676g = _W._ctx676g.__enter__()


def _hung_task(task: dict) -> dict:
    from detect_for_assets import detect_one_asset, SampleSpec, ROOT
    spec = SampleSpec(id=task["uid"], dataset=task["source_batch"],
                      dir=task["dir"], files=tuple(task["files"]))
    t0 = time.perf_counter()
    r = detect_one_asset(_W, spec, task["asset"], atoms_root=str(ROOT / task["dir"]))
    return _cell(task, task["asset"], r["verdict"], r["note"],
                 time.perf_counter() - t0)


def cmd_hung(limit: int | None) -> int:
    rows = [r for r in _load_manifest()
            if r["run_mode"] == "fresh" and r["hung_flag"]]
    if limit:
        rows = rows[:limit]
    done = _done_keys(CKPT["hung"])
    tasks = [{"uid": r["uid"], "sample_id": r["sample_id"],
              "source_batch": r["source_batch"],
              "dir": r["dir"], "files": r["files"], "asset": a,
              "defect_type": r["defect_type"]}
             for r in rows for a in SAN_ASSETS
             if (r["uid"], a, 1) not in done]
    _log(f"hung: 挂起样本 {len(rows)}，待跑 {len(tasks)} 格（{mp.cpu_count() and 6} 进程并行，"
         f"每格最多 2×120s 超时）")
    if not tasks:
        return 0
    t0 = time.perf_counter()
    with mp.Pool(processes=6, initializer=_hung_worker_init) as pool:
        for i, cell in enumerate(pool.imap_unordered(_hung_task, tasks, chunksize=1), 1):
            _append(CKPT["hung"], cell)
            el = time.perf_counter() - t0
            _log(f"hung {i}/{len(tasks)} {cell['sample_id']}/{cell['asset']} "
                 f"= {cell['verdict']} ({el:.0f}s, ETA "
                 f"{el / i * (len(tasks) - i) / 60:.0f}m)")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# QA：挂起池抽检 + 复用 105 的 10% 当日复跑验证
# ─────────────────────────────────────────────────────────────────────────────
def _run_cell(rv, sample: dict, asset: str, run: int = 1) -> dict:
    from detect_for_assets import detect_one_asset, SampleSpec, ROOT
    if sample.get("input_mode") == "code_materialized":
        import tempfile
        from detect_for_assets import corpus_code_map
        code = corpus_code_map().get(sample["sample_id"], "")
        tmp = tempfile.mkdtemp(prefix=f"qa_{sample['sample_id']}_")
        (Path(tmp) / "s.cpp").write_text(code, encoding="utf-8")
        spec = SampleSpec(id=sample["uid"], dataset=sample["source_batch"],
                          dir="", files=("s.cpp",))
        t0 = time.perf_counter()
        r = detect_one_asset(rv, spec, asset, atoms_root=tmp)
        import shutil
        shutil.rmtree(tmp, ignore_errors=True)
        return _cell(sample, asset, r["verdict"], r["note"],
                     time.perf_counter() - t0, run=run, extra={"qa": True})
    spec = SampleSpec(id=sample["uid"], dataset=sample["source_batch"],
                      dir=sample["dir"], files=tuple(sample["files"]))
    t0 = time.perf_counter()
    r = detect_one_asset(rv, spec, asset, atoms_root=str(ROOT / sample["dir"]))
    return _cell(sample, asset, r["verdict"], r["note"],
                 time.perf_counter() - t0, run=run, extra={"qa": True})


def cmd_qa(_limit: int | None = None) -> int:
    from detect_for_assets import decode_safety, load_rv661
    rv = load_rv661()
    done = _done_keys(CKPT["qa"])
    manifest = {r["uid"]: r for r in _load_manifest()}
    attr = json.loads(ATTR_673R.read_text(encoding="utf-8"))
    reuse_verdicts: dict[str, dict[str, str]] = {}
    for ds in ("holdout", "corpus"):
        for r in attr["datasets"][ds]["samples"]:
            reuse_verdicts[f"{ds}:{r['id']}"] = {
                a: str(v["verdict"]) for a, v in r["per_asset"].items()}

    # 1) 挂起池 QA
    hung_cells = {}
    if CKPT["hung"].is_file():
        for ln in CKPT["hung"].read_text(encoding="utf-8").splitlines():
            if ln.strip():
                o = json.loads(ln)
                hung_cells[(o["sample_id"], o["asset"])] = o
    suspects = [(k, v) for k, v in hung_cells.items() if v["verdict"] != "miss"]
    miss_pool = sorted(k for k, v in hung_cells.items() if v["verdict"] == "miss")
    rng = random.Random(676)
    spot = rng.sample(miss_pool, max(1, round(len(miss_pool) * 0.10))) if miss_pool else []
    _log(f"qa: 挂起池 {len(hung_cells)} 格，非 miss 疑似 {len(suspects)}，"
         f"miss 抽检 {len(spot)}")
    with decode_safety() as env_info:
        _log(f"qa 适配层 L1_effect={env_info.get('L1_effect')}")
        for (uid, asset), cell in suspects:
            if (uid, asset, 2) in done:
                continue
            _log(f"qa 疑似复跑 {uid}/{asset}（并行判定={cell['verdict']}）")
            _append(CKPT["qa"], _run_cell(rv, manifest[uid], asset, run=2))
        for uid, asset in spot:
            if (uid, asset, 2) in done:
                continue
            _log(f"qa 抽检复跑 {uid}/{asset}")
            _append(CKPT["qa"], _run_cell(rv, manifest[uid], asset, run=2))

    # 2) 复用 105 的 10% 当日复跑（对照 673r 同资产判定）
    reuse = [r for r in _load_manifest() if r["run_mode"] == "reuse_673r"]
    rng2 = random.Random(67610)
    pick = sorted(rng2.sample([r["uid"] for r in reuse if r["source_batch"] == "holdout"], 5)
                  + rng2.sample([r["uid"] for r in reuse if r["source_batch"] == "corpus"], 5))
    _log(f"qa 复用验证 {len(pick)} 条: {pick}")
    agree = 0
    total = 0
    for uid in pick:
        r = manifest[uid]
        for asset in ALL_ASSETS:
            if (uid, asset, 2) in done:
                continue
            cell = _run_cell(rv, r, asset, run=2)
            _append(CKPT["qa"], cell)
            ref = reuse_verdicts.get(uid, {}).get(asset)
            if ref is not None:
                total += 1
                if cell["verdict"] == ref:
                    agree += 1
                else:
                    _log(f"qa 复用差异 {uid}/{asset}: 673r={ref} 今日={cell['verdict']}")
    _log(f"qa 复用一致性: {agree}/{total}")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# compile-time 资产（无本地检测器 ⇒ 恒 unknown；仍走真实 detect() 调用，秒级）
# ─────────────────────────────────────────────────────────────────────────────
def cmd_ct(_limit: int | None = None) -> int:
    from detect_for_assets import detect_one_asset, load_rv661, SampleSpec, ROOT
    rv = load_rv661()
    rows = [r for r in _load_manifest() if r["run_mode"] == "fresh"]
    done = _done_keys(CKPT["local"])
    n = 0
    for r in rows:
        if (r["uid"], "compile-time", 1) in done:
            continue
        spec = SampleSpec(id=r["uid"], dataset=r["source_batch"],
                          dir=r["dir"], files=tuple(r["files"]))
        t0 = time.perf_counter()
        res = detect_one_asset(rv, spec, "compile-time",
                               atoms_root=str(ROOT / r["dir"]))
        _append(CKPT["local"], _cell(r, "compile-time", res["verdict"],
                                     res["note"], time.perf_counter() - t0))
        n += 1
    _log(f"ct: 补跑 compile-time {n} 格（真实 detect 调用，无本地检测器 ⇒ unknown）")
    return 0


# ─────────────────────────────────────────────────────────────────────────────
# merge：合成判定矩阵
# ─────────────────────────────────────────────────────────────────────────────
def cmd_merge(_limit: int | None = None) -> int:
    manifest_rows = _load_manifest()
    attr = json.loads(ATTR_673R.read_text(encoding="utf-8"))
    reuse_verdicts: dict[str, dict[str, str]] = {}
    reuse_meta: dict[str, dict] = {}
    for ds in ("holdout", "corpus"):
        for r in attr["datasets"][ds]["samples"]:
            uid = f"{ds}:{r['id']}"
            reuse_verdicts[uid] = {a: str(v["verdict"])
                                   for a, v in r["per_asset"].items()}
            reuse_meta[uid] = {
                "wall_seconds": {a: v.get("wall_seconds")
                                 for a, v in r["per_asset"].items()},
                "note": {a: str(v.get("note", ""))[:300]
                         for a, v in r["per_asset"].items()},
            }

    # 收集各 checkpoint 的格子（同 key 后者覆盖前者）
    cells: dict[tuple, dict] = {}
    for name in ("local", "san", "hung", "qa"):
        p = CKPT[name]
        if not p.is_file():
            continue
        for ln in p.read_text(encoding="utf-8").splitlines():
            ln = ln.strip()
            if not ln:
                continue
            o = json.loads(ln)
            cells[(o["sample_id"], o["asset"], o.get("run", 1))] = o

    samples_out: list[dict] = []
    matrix: dict[str, dict[str, str]] = {}
    problems: list[str] = []
    for r in manifest_rows:
        uid = r["uid"]
        per: dict[str, dict] = {}
        verdicts: dict[str, str] = {}
        if r["run_mode"] == "reuse_673r":
            for a in ALL_ASSETS:
                v = reuse_verdicts.get(uid, {}).get(a, "unknown")
                verdicts[a] = v
                per[a] = {"verdict": v, "source": "reuse_673r",
                          "wall_seconds": reuse_meta.get(uid, {}).get("wall_seconds", {}).get(a),
                          "note": reuse_meta.get(uid, {}).get("note", {}).get(a, "")}
        else:
            for a in ALL_ASSETS:
                c = cells.get((uid, a, 1))
                if c is None:
                    problems.append(f"{uid}/{a}: 缺判定")
                    verdicts[a] = "MISSING"
                    per[a] = {"verdict": "MISSING", "source": "fresh"}
                else:
                    v = str(c["verdict"])
                    src = "fresh"
                    note = c.get("note", "")
                    # 挂起池 QA：独占复跑与并行判定不一致 ⇒ 以复跑为准（记录覆盖）
                    q = cells.get((uid, a, 2))
                    if q is not None and str(q["verdict"]) != v:
                        v = str(q["verdict"])
                        src = "fresh_qa_override"
                        note = (str(q.get("note", ""))[:300]
                                + " ｜[QA 覆盖] 并行首轮判定=" + str(c["verdict"])
                                + "（该样本行为跨运行不稳定，以独占复跑为准）")
                    verdicts[a] = v
                    per[a] = {"verdict": v,
                              "source": src, "run": 1,
                              "wall_seconds": c.get("wall_seconds"),
                              "note": note}
        # TSan 稳定性（3 次众数）
        stability = None
        if r["run_mode"] == "fresh" and r["defect_type"] in CONC_TYPES \
                and verdicts.get("tsan") not in (None, "MISSING"):
            runs = [cells[(uid, "tsan", k)]["verdict"] for k in (1, 2, 3)
                    if (uid, "tsan", k) in cells]
            if len(runs) >= 2:
                from statistics import multimode
                majority = sorted(multimode(runs))[0]
                stability = {"runs": runs, "majority": majority,
                             "stable": len(set(runs)) == 1}
                if r.get("hung_flag"):
                    stability["note"] = "挂起样本为确定性超时，只跑 1 次（不烧伪装的 3 次）"
        # QA 复跑记录
        qa_cells = {a: cells[(uid, a, 2)] for a in ALL_ASSETS
                    if (uid, a, 2) in cells}
        samples_out.append({
            "uid": uid, "sample_id": r["sample_id"],
            "source_batch": r["source_batch"],
            "defect_type": r["defect_type"], "planted": r["planted"],
            "expected_verdict": r["expected_verdict"],
            "hung_flag": r["hung_flag"], "run_mode": r["run_mode"],
            "files": r.get("files", []), "per_asset": per,
            "or_verdict_available6": _or6(verdicts),
            "or_verdict_all8": _or8(verdicts),
            "tsan_stability": stability, "qa_rerun": qa_cells,
        })
        matrix[uid] = verdicts
    if problems:
        _log(f"merge 警告：{len(problems)} 个缺失判定（前 5：{problems[:5]}）")

    # QA 汇总：复用复跑一致性（对照 673r 同资产判定）+ 挂起池抽检一致性
    reuse_verdicts_qa: dict[str, dict[str, str]] = {}
    for ds in ("holdout", "corpus"):
        for r in attr["datasets"][ds]["samples"]:
            reuse_verdicts_qa[f"{ds}:{r['id']}"] = {
                a: str(v["verdict"]) for a, v in r["per_asset"].items()}
    qa_agree = qa_total = 0
    hung_qa_agree = hung_qa_total = 0
    hung_uids = {r["uid"] for r in manifest_rows if r["run_mode"] == "fresh" and r["hung_flag"]}
    for (uid, asset, run), c in cells.items():
        if run != 2 or c.get("qa") is not True:
            continue
        if uid in hung_uids:
            ref = cells.get((uid, asset, 1))
            if ref is None:
                continue
            hung_qa_total += 1
            hung_qa_agree += (c["verdict"] == ref["verdict"])
        else:
            ref = reuse_verdicts_qa.get(uid, {}).get(asset)
            if ref is None:
                continue
            qa_total += 1
            qa_agree += (c["verdict"] == ref)

    env = {
        "local_gcc": _tool_version(["g++", "--version"]),
        "local_clang": _tool_version(["clang++", "--version"]),
        "wsl_gcc": _tool_version(["wsl", "-e", "bash", "-lc", "g++ --version | head -1"]),
        "os": sys.platform,
    }
    doc = {
        "schema": "queyi-blindspot-matrix/676g",
        "version": "1.0",
        "generated_by": "data/blindspot_676g_runner.py merge",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "detector_owner": "tools/holdout_reveal_661.py::detect（未修改）",
        "wrapper": "tools/detect_for_assets.py（未修改，复用其 decode_safety/detect_one_asset）",
        "reuse": {
            "source": "data/experiments/asset_attribution_673r.json",
            "generated_at": attr.get("generated_at"),
            "n_holdout": len(attr["datasets"]["holdout"]["samples"]),
            "n_corpus": len(attr["datasets"]["corpus"]["samples"]),
            "note": "673r 归属矩阵与本批同日同环境生成；10% 当日复跑验证见 qa_verify",
        },
        "assets": ALL_ASSETS,
        "asset_availability": {
            "wunsequenced": "本机 MinGW g++ 13.1 不认 -Wunsequenced ⇒ 恒 unknown（673u 判据，已如实区分）",
            "compile-time": "无本地检测器 ⇒ 恒 unknown（检测器池中的声明性资产）",
        },
        "hung_pool_note": ("35 条挂起样本（expE 34 + expG G019）sanitizer 判据=挂起→超时→miss；"
                           "并行执行的安全性论证见 runner 文件头；QA 复跑见各样本 qa_rerun"),
        "environment": env,
        "n_samples": len(manifest_rows),
        "n_problems": len(problems),
        "problems": problems[:50],
        "qa_verify": {
            "reuse_rerun_agree": qa_agree, "reuse_rerun_total": qa_total,
            "hung_pool_rerun_agree": hung_qa_agree,
            "hung_pool_rerun_total": hung_qa_total,
        },
        "samples": samples_out,
        "matrix": matrix,
    }
    MATRIX_OUT.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                          encoding="utf-8", newline="\n")
    _log(f"merge 完成：{len(manifest_rows)} 样本，缺失 {len(problems)}；"
         f"写入 {MATRIX_OUT.relative_to(ROOT).as_posix()}")
    return 0


def _or6(v: dict) -> str:
    avail = ["asan", "ubsan", "tsan", "compiler-warn", "cross-compile", "linker"]
    vs = [v.get(a) for a in avail]
    if "catch" in vs:
        return "catch"
    if vs and all(x == "unknown" for x in vs):
        return "unknown"
    if any(x == "MISSING" for x in vs):
        return "MISSING"
    return "miss"


def _or8(v: dict) -> str:
    vs = [v.get(a) for a in ALL_ASSETS]
    if "catch" in vs:
        return "catch"
    if vs and all(x == "unknown" for x in vs):
        return "unknown"
    if any(x == "MISSING" for x in vs):
        return "MISSING"
    return "miss"


def _tool_version(cmd: list) -> str:
    import subprocess
    try:
        cp = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        out = ((cp.stdout or "") + (cp.stderr or "")).strip().splitlines()
        return out[0] if out else ""
    except Exception as e:  # noqa: BLE001
        return f"error:{e}"


def main() -> int:
    if os.name == "nt":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:  # noqa: BLE001
            pass
    ap = argparse.ArgumentParser(description="676g 判定矩阵生成器")
    ap.add_argument("cmd", choices=("manifest", "local", "ct", "san", "hung", "qa",
                                    "merge"))
    ap.add_argument("--limit", type=int, default=None)
    a = ap.parse_args()
    return {"manifest": cmd_manifest, "local": cmd_local, "ct": cmd_ct,
            "san": cmd_san, "hung": cmd_hung, "qa": cmd_qa,
            "merge": cmd_merge}[a.cmd](a.limit)


if __name__ == "__main__":
    raise SystemExit(main())
