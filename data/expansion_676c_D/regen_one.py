#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# 676c-D: 定点重生成单个样本（避免整批重生成抹掉其它样本的 verification）
# 用法: python regen_one.py D191
import os
import sys
import json
import importlib

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import generate_D as G

# 全局配额顺序（与 generate_D.main 一致）
QUOTA = [("iterator_invalidation", 35), ("stl_container_ub", 35), ("string_ub", 35),
         ("algorithm_misuse", 35), ("smart_pointer", 30), ("lambda_capture", 30)]
BUILDERS = {
    "iterator_invalidation": G.gen_iterator,
    "stl_container_ub": G.gen_container,
    "string_ub": G.gen_string,
    "algorithm_misuse": G.gen_algorithm,
    "smart_pointer": G.gen_smart,
    "lambda_capture": G.gen_lambda,
}

def all_specs():
    specs = []
    for t, n in QUOTA:
        specs += BUILDERS[t](n)
    return specs

def write_spec(sid, sp):
    code_lines = sp["code"]
    dline = None
    for li, ln in enumerate(code_lines, start=1):
        if G.MARK in ln:
            dline = li
            break
    assert dline is not None, "缺少缺陷标记行"
    cpp = "\n".join(code_lines) + "\n"
    cpp = ("// 676c-D: planted C++ standard-library defect candidate (generated)\n"
           "// SPDX-License-Identifier: Apache-2.0\n" + cpp)
    dline += 2
    obj = {
        "sample_id": sid,
        "defect_type": sp["defect_type"],
        "defect_location": {"line": dline, "function": sp["func"], "description": sp["desc"]},
        "severity": sp["sev"],
        "planted": True,
        "expected_verdict": sp["exp_verdict"],
        "expected_detectors": sp["exp_detectors"],
        "trigger_condition": sp["trigger"],
        "notes": sp["notes"],
        "generator": "676c-expD-generate_D",
    }
    with open(os.path.join(HERE, f"sample_{sid}.cpp"), "w", encoding="utf-8") as f:
        f.write(cpp)
    with open(os.path.join(HERE, f"sample_{sid}.json"), "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    print(f"重生成 {sid} ({sp['defect_type']}) 缺陷行={dline}")

if __name__ == "__main__":
    sid = sys.argv[1]
    specs = all_specs()
    idx = int(sid[1:]) - 1
    write_spec(sid, specs[idx])
