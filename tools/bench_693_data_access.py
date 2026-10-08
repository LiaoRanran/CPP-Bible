#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""bench_693_data_access.py — 693-D4：数据访问性能实测（数字现算，不写死）。

测什么
======
1. ``json.load`` 冷读 vs ``utils.data_access.load_json_cached`` 缓存命中；
2. 流式 sha256 vs 一次性读入后 hash（**峰值内存**差异）；
3. 复现流水线里"同一文件被解析 N 次"的真实代价。

为什么不直接写数字
==================
性能数字**随机器、磁盘、Python 版本漂移**。写死在文档里第二次读就是谎言。
本脚本每次运行现算，并把结果写进 ``data/693_perf_bench.json``，
文档（``tools/README.md`` / 验收报告）引用该 JSON 的字段而不是抄数字。

用法
====
    python tools/bench_693_data_access.py
    python tools/bench_693_data_access.py --repeat 7
"""
from __future__ import annotations

import argparse
import datetime as _dt
import gc
import hashlib
import json
import statistics
import sys
import time
import tracemalloc
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from utils.data_access import DATA, load_json_cached, sha256_file  # noqa: E402
from utils.logging_setup import get_logger  # noqa: E402

_log = get_logger("bench_693")
OUT_JSON = ROOT / "data" / "693_perf_bench.json"

TARGETS = (
    ("blindspot_676g_detection_matrix.json", "冻结检测矩阵 1147×8"),
    ("683_real_world_detection_matrix.json", "真实靶场矩阵 110×8"),
    ("676m_a5_matrix_corrected.json", "A5 修正矩阵"),
)


def _time_it(fn, repeat: int) -> dict[str, float]:
    """执行 ``fn`` ``repeat`` 次，返回 first / median / min（毫秒）。"""
    ts: list[float] = []
    for _ in range(repeat):
        gc.collect()
        t0 = time.perf_counter()
        fn()
        ts.append((time.perf_counter() - t0) * 1000.0)
    return {"first_ms": round(ts[0], 2),
            "median_ms": round(statistics.median(ts), 2),
            "min_ms": round(min(ts), 2)}


def _peak_mem(fn) -> int:
    """返回 ``fn`` 的峰值内存（字节）。"""
    gc.collect()
    tracemalloc.start()
    fn()
    _cur, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    return peak


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repeat", type=int, default=5, help="每项重复次数（默认 5）")
    args = ap.parse_args()

    doc: dict[str, Any] = {
        "schema": "queyi-693-perf-bench/v1",
        "generated_by": "tools/bench_693_data_access.py",
        "generated_at": _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "python": sys.version.split()[0],
        "repeat": args.repeat,
        "targets": {},
    }

    for name, desc in TARGETS:
        p = DATA / name
        if not p.exists():
            _log.warning("跳过（不存在）：%s", name)
            continue
        size_kb = round(p.stat().st_size / 1024, 1)

        # ── 冷读（每次强制重解析）──
        cold = _time_it(lambda: load_json_cached(p, use_cache=False), args.repeat)
        # ── 缓存命中（先填一次，再计时）──
        load_json_cached(p)  # warm
        warm = _time_it(lambda: load_json_cached(p), args.repeat)

        # ── 内存：流式 vs 一次性 ──
        peak_stream = _peak_mem(lambda: sha256_file(p))
        peak_whole = _peak_mem(lambda: hashlib.sha256(p.read_bytes()).hexdigest())

        speedup = round(cold["median_ms"] / warm["median_ms"], 1) if warm["median_ms"] else None
        doc["targets"][name] = {
            "desc": desc,
            "size_kb": size_kb,
            "cold": cold,
            "cached": warm,
            "cache_speedup_x": speedup,
            "peak_bytes_stream_sha256": peak_stream,
            "peak_bytes_whole_file_sha256": peak_whole,
            "peak_memory_saved_bytes": peak_whole - peak_stream,
        }
        _log.info("%-42s 冷读 %7.2f ms → 缓存 %6.2f ms（×%s）｜sha256 峰值 %d→%d B",
                  name, cold["median_ms"], warm["median_ms"], speedup,
                  peak_whole, peak_stream)

    # ── 复现流水线的真实代价：同一文件被解析 N 次 ──
    p = DATA / TARGETS[0][0]
    if p.exists():
        n_times = 4  # 693-E 的四个分析各自读一次
        t0 = time.perf_counter()
        for _ in range(n_times):
            load_json_cached(p, use_cache=False)
        naive_ms = (time.perf_counter() - t0) * 1000.0
        load_json_cached(p)  # warm once
        t0 = time.perf_counter()
        for _ in range(n_times):
            load_json_cached(p)
        cached_ms = (time.perf_counter() - t0) * 1000.0
        doc["pipeline_simulation"] = {
            "file": TARGETS[0][0],
            "n_reads": n_times,
            "naive_total_ms": round(naive_ms, 2),
            "cached_total_ms": round(cached_ms, 2),
            "saved_ms": round(naive_ms - cached_ms, 2),
            "saved_pct": round((naive_ms - cached_ms) / naive_ms * 100.0, 1) if naive_ms else None,
        }
        _log.info("流水线模拟（同文件读 %d 次）：%.1f ms → %.1f ms，省 %.1f%%",
                  n_times, naive_ms, cached_ms, doc["pipeline_simulation"]["saved_pct"])

    OUT_JSON.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n",
                        encoding="utf-8", newline="\n")
    print(f"[693-D4] 实测结果 → {OUT_JSON}")


if __name__ == "__main__":
    main()
