#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""reverify_676cC.py — 单进程内重验证指定样本（避免并发写 JSON 竞态）。"""
import json, importlib.util, os

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("v", os.path.join(HERE, "verify_676cC.py"))
v = importlib.util.module_from_spec(spec); spec.loader.exec_module(v)

R = json.load(open(v.RESULTS, encoding="utf-8")) if os.path.isfile(v.RESULTS) else {}
for idx in [32, 34, 36, 122]:
    rec = v.verify_one(idx)
    R[rec["id"]] = rec
    print(f"sample_{idx:03d} pooled={rec.get('pooled')} stage={rec.get('stage')} "
          f"verdict={rec.get('detector_verdict')} "
          f"o0={rec.get('opt_O0_detector')} o2={rec.get('opt_O2_detector')}")
json.dump(R, open(v.RESULTS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print("saved")
