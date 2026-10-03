#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""smoke_E.py — 开发期快速自检：把已登记样本的 C++ 抽出并做语法编译。

只做 -fsyntax-only（本机 MinGW），不跑 WSL。正式验证走 verify_E.py。
"""
from __future__ import annotations

import os
import subprocess
import sys
import tempfile
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from _dsl import SAMPLES  # noqa: E402

PARTS = [p for p in sorted(os.listdir(HERE))
         if p.startswith("defs_E") and p.endswith(".py")]
for m in PARTS:
    importlib.import_module(m[:-3])

print(f"已登记 {len(SAMPLES)} 个样本，来自 {len(PARTS)} 个模块")
bad = 0
with tempfile.TemporaryDirectory() as td:
    for s in SAMPLES:
        p = os.path.join(td, f"sample_{s['sid']}.cpp")
        with open(p, "w", encoding="utf-8", newline="\n") as f:
            f.write(s["code"])
        try:
            r = subprocess.run(["g++", "-std=c++17", "-O0", "-fsyntax-only", "-pthread", p],
                               capture_output=True, text=True, timeout=120)
        except Exception as e:  # noqa: BLE001
            print(f"  {s['sid']} EXC {e}")
            bad += 1
            continue
        if r.returncode != 0:
            bad += 1
            msg = (r.stdout + r.stderr).strip().replace("\n", " | ")
            print(f"  {s['sid']} FAIL  {msg[:220]}")
print(f"\n语法检查：{len(SAMPLES)-bad}/{len(SAMPLES)} 通过，失败 {bad}")
sys.exit(1 if bad else 0)
