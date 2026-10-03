#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""_dsl.py — 676c-E 样本登记 DSL（被 generate_E.py 与各 defs_*.py 共享）。"""
from __future__ import annotations

#: 全局登记表（各 defs 模块 import 后往里追加）
SAMPLES: list[dict] = []


def S(sid, dtype, sev, verdict, dets, nthreads, timeout, func, desc,
      code, trig, notes):
    """登记一个候选样本。code 为完整 C++ 源码（含 main），不含文件头注释。"""
    SAMPLES.append(dict(
        sid=sid, dtype=dtype, sev=sev, verdict=verdict, dets=dets,
        nthreads=nthreads, timeout=timeout, func=func, desc=desc,
        code=code.strip("\n") + "\n", trig=trig, notes=notes,
    ))
