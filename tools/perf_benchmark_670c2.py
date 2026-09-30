#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""perf_benchmark_670c2.py — 性能基准固化（670c2 C4）。

测量并落盘 `data/perf_670c2.json`：
  - gate_run_ms        : L0 门禁编排耗时（阈值 ≤ 30000ms）
  - data_parse_ms.*    : 前端数据文件解析耗时（proxy；卡库筛选/星图数据加载）
  - asset_size_kb.*    : 关键 JS/CSS 体积
  - paper_gate_ms      : 论文质量门禁耗时

**诚实限定**：真正的"星图 60fps / 卡库筛选 ≤100ms"是**浏览器渲染指标**，需要 headless 浏览器；
本工具测量的是**可复现的服务端/解析代理指标**，并在报告中标注这一区别。
退出码：0 = 无超阈值；1 = 有超阈值（warn 级）。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import subprocess
import sys
import time

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "data", "perf_670c2.json")
PY = sys.executable

THRESHOLDS = {
    "gate_run_ms": 30000,
    "paper_gate_ms": 15000,
    "data_parse_ms": 500,
}


def time_subprocess(cmd: list[str]) -> float:
    t0 = time.perf_counter()
    subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return (time.perf_counter() - t0) * 1000.0


def time_json_parse(path: str) -> tuple[float, int]:
    t0 = time.perf_counter()
    with open(path, encoding="utf-8") as fh:
        data = json.load(fh)
    ms = (time.perf_counter() - t0) * 1000.0
    return ms, len(json.dumps(data))


def run() -> dict:
    res: dict = {"measurements": {}, "thresholds": THRESHOLDS, "warns": [], "notes": []}

    # 1. 门禁编排耗时
    gate = os.path.join(ROOT, "tools", "run_658_gate.py")
    if os.path.isfile(gate):
        res["measurements"]["gate_run_ms"] = round(time_subprocess([PY, gate]), 1)

    # 2. 论文质量门禁耗时
    pgate = os.path.join(ROOT, "tools", "paper_quality_gate_670c2.py")
    if os.path.isfile(pgate):
        res["measurements"]["paper_gate_ms"] = round(time_subprocess([PY, pgate]), 1)

    # 3. 前端数据解析耗时（proxy）
    parse = {}
    for p in sorted(glob.glob(os.path.join(ROOT, "web", "data", "*.json"))):
        ms, size = time_json_parse(p)
        parse[os.path.basename(p)] = {"parse_ms": round(ms, 2), "bytes": size}
    res["measurements"]["data_parse_ms"] = parse

    # 4. 资产体积
    sizes = {}
    for rel in ("web/starmap.js", "web/js/charts.js", "web/js/cards_core.js", "web/style.css"):
        p = os.path.join(ROOT, rel)
        if os.path.isfile(p):
            sizes[rel] = round(os.path.getsize(p) / 1024.0, 1)
    res["measurements"]["asset_size_kb"] = sizes

    # 阈值判定
    m = res["measurements"]
    if "gate_run_ms" in m and m["gate_run_ms"] > THRESHOLDS["gate_run_ms"]:
        res["warns"].append(f"gate_run_ms {m['gate_run_ms']} > {THRESHOLDS['gate_run_ms']}")
    if "paper_gate_ms" in m and m["paper_gate_ms"] > THRESHOLDS["paper_gate_ms"]:
        res["warns"].append(f"paper_gate_ms {m['paper_gate_ms']} > {THRESHOLDS['paper_gate_ms']}")
    for name, v in m.get("data_parse_ms", {}).items():
        if v["parse_ms"] > THRESHOLDS["data_parse_ms"]:
            res["warns"].append(f"data_parse_ms[{name}] {v['parse_ms']} > {THRESHOLDS['data_parse_ms']}")

    res["notes"].append("data_parse_ms 是 JSON 解析代理指标，非浏览器渲染/筛选延迟。")
    res["notes"].append("星图 60fps / 卡库筛选 ≤100ms 需 headless 浏览器测量，本批未做。")
    return res


def main() -> int:
    ap = argparse.ArgumentParser(description="性能基准（670c2 C4）")
    ap.add_argument("--write", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    res = run()
    if args.write:
        with open(OUT, "w", encoding="utf-8") as fh:
            json.dump(res, fh, ensure_ascii=False, indent=2)
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        for k, v in res["measurements"].items():
            print(f"  {k}: {v}")
        for w in res["warns"]:
            print("  [warn]", w)
        print("[perf] " + ("PASS" if not res["warns"] else f"{len(res['warns'])} warn"))
    return 0 if not res["warns"] else 1


if __name__ == "__main__":
    sys.exit(main())
