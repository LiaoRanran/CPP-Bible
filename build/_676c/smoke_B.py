#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""冒烟测试：覆盖每种缺陷类型各一个（catch / miss 变体），确认 pipeline 正常。"""
import os
import sys
import json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import validate_B as V  # noqa: E402  (sets WSL_UTF8 + monkeypatch ATOMS on import)

SAMPLE_DIR = V.SAMPLE_DIR

TESTS = ["sample_B001", "sample_B021", "sample_B041", "sample_B061",
         "sample_B071", "sample_B081", "sample_B099"]

for sid in TESTS:
    jp = os.path.join(SAMPLE_DIR, sid + ".json")
    ann = json.load(open(jp, encoding="utf-8"))
    rc, warns = V.task_b_compile(jp)
    dets = V.task_c_detect(ann)
    print(f"\n=== {sid} [{ann['defect_type']}] exp={ann['expected_verdict']} "
          f"det={ann['expected_detectors']} ===")
    print(f"  compile rc={rc}  warnings={len(warns.splitlines())}")
    for d, (v, note) in dets.items():
        print(f"  detect({d}) -> {v}")
        print(f"     note: {note[:160]}")
