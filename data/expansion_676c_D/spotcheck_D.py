#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# 676c-D 任务D：质量抽检（固定种子 6761，抽 20%）
# 对每个抽检样本检查：字段齐全、行号指向标记行、planted/severity 合法、
# expected==actual、缺陷行确实含 <<PLANTED-DEFECT>>。输出抽检记录。
import os
import json
import random

HERE = os.path.dirname(os.path.abspath(__file__))
MARK = "<<PLANTED-DEFECT>>"
REQUIRED_TOP = ["sample_id", "defect_type", "defect_location", "severity",
                "planted", "expected_verdict", "expected_detectors",
                "trigger_condition", "notes"]

def check(sid):
    fails = []
    cp = os.path.join(HERE, f"sample_{sid}.cpp")
    jp = os.path.join(HERE, f"sample_{sid}.json")
    obj = json.load(open(jp, encoding="utf-8"))
    for k in REQUIRED_TOP:
        if k not in obj or obj[k] in (None, "", [], {}):
            fails.append(f"字段缺失/为空:{k}")
    if obj.get("planted") is not True:
        fails.append("planted!=true")
    if obj.get("severity") not in ("low", "medium", "high"):
        fails.append("severity非法")
    lines = open(cp, encoding="utf-8").read().splitlines()
    dl = obj["defect_location"]["line"]
    if not isinstance(dl, int) or dl < 1 or dl > len(lines):
        fails.append("行号越界")
    elif MARK not in lines[dl - 1]:
        fails.append("行号未指向缺陷标记")
    v = obj.get("verification", {})
    if v.get("actual_verdict") not in ("catch", "miss"):
        fails.append("actual_verdict非catch/miss")
    if obj.get("expected_verdict") != v.get("actual_verdict"):
        fails.append("expected!=actual")
    return obj, fails

def main():
    random.seed(6761)
    all_ids = [f"D{i:03d}" for i in range(1, 201)]
    sample = sorted(random.sample(all_ids, 40))  # 20%
    passed, failed = [], []
    for sid in sample:
        obj, fails = check(sid)
        rec = {"sample_id": sid, "defect_type": obj["defect_type"],
               "expected_verdict": obj["expected_verdict"],
               "detectors": obj["expected_detectors"],
               "defect_line": obj["defect_location"]["line"]}
        if fails:
            rec["fail_reasons"] = fails
            failed.append(rec)
        else:
            passed.append(rec)
    out = {"seed": 6761, "sample_rate": 0.20, "sampled": len(sample),
           "passed": len(passed), "failed": len(failed),
           "fail_rate": round(len(failed) / len(sample), 4),
           "records": {"passed": passed, "failed": failed}}
    with open(os.path.join(HERE, "spotcheck_6761.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"抽检 {len(sample)} 个：合格 {len(passed)}，不合格 {len(failed)}，不合格率 {out['fail_rate']:.2%}")
    if failed:
        print("不合格样本：")
        for r in failed:
            print("  ", r["sample_id"], r["fail_reasons"])

if __name__ == "__main__":
    main()
