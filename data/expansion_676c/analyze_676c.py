#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""analyze_676c.py — 汇总统计 + Task D 质量抽检（随机 20%）。
"""
import os
import json
import random
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXP = os.path.join(REPO, "data", "expansion_676c")
VOCAB = {"undefined_behavior", "memory_safety", "uninitialized_read",
         "null_pointer_deref", "out_of_bounds", "data_race",
         "integer_overflow", "type_punning", "resource_leak", "other_ub"}
CATCH_TYPES = {"memory_safety", "out_of_bounds", "null_pointer_deref", "undefined_behavior"}

res = json.load(open(os.path.join(EXP, "verify_results.json"), encoding="utf-8"))

pooled = [k for k, v in res.items() if v.get("pooled")]
failed = [k for k, v in res.items() if not v.get("pooled")]

# 类型分布 / 严重度 / planted / 耗时
pool_types = Counter()
sev = Counter()
planted_true = 0
warned = 0
times = []
for k in pooled:
    meta = json.load(open(os.path.join(EXP, f"{k}.json"), encoding="utf-8"))
    pool_types[meta["defect_type"]] += 1
    sev[meta["severity"]] += 1
    if meta.get("planted") is True:
        planted_true += 1
    if res[k].get("syntax_warnings"):
        warned += 1
    if res[k].get("elapsed_s") is not None:
        times.append(res[k]["elapsed_s"])

n = len(pooled)
avg_t = (sum(times) / len(times)) if times else 0

print("=== 汇总 ===")
print(f"入池样本数: {n}")
print(f"淘汰样本数: {len(failed)} -> {failed}")
print(f"各类型入池: {dict(pool_types)}")
print(f"严重度分布: {dict(sev)}")
print(f"planted=true: {planted_true}/{n} ({planted_true/n*100:.1f}%)")
print(f"带编译警告样本数: {warned}")
print(f"平均验证耗时: {avg_t:.2f}s/样本 (总 {sum(times):.1f}s)")

# === Task D 抽检 ===
random.seed(6761)  # 固定种子可复现
sample_ids = random.sample(pooled, max(1, round(n * 0.2)))
print(f"\n=== Task D 抽检 ({len(sample_ids)} 个 = {len(sample_ids)/n*100:.0f}%) ===")
check_fail = 0
for k in sorted(sample_ids):
    meta = json.load(open(os.path.join(EXP, f"{k}.json"), encoding="utf-8"))
    cpp = os.path.join(EXP, f"{k}.cpp")
    code = open(cpp, encoding="utf-8").read()
    lines = code.splitlines()
    dl = meta.get("defect_location", {})
    problems = []
    # 1) 字段完整性
    for fld in ("defect_type", "severity", "planted", "expected_verdict",
                "expected_detectors", "notes"):
        if not meta.get(fld) and meta.get(fld) is not False and fld != "planted":
            problems.append(f"字段空:{fld}")
    if meta.get("planted") is not True:
        problems.append("planted!=true")
    # 2) 受控词表
    if meta["defect_type"] not in VOCAB:
        problems.append("defect_type 不在词表")
    if meta["expected_verdict"] not in ("catch", "miss"):
        problems.append("expected_verdict 非法")
    if not isinstance(meta.get("expected_detectors"), list) or not meta["expected_detectors"]:
        problems.append("expected_detectors 空")
    # 3) 缺陷行真实含哨兵
    ln = dl.get("line")
    if not isinstance(ln, int) or ln < 1 or ln > len(lines):
        problems.append("defect_location.line 非法")
    elif "<<PLANTED-DEFECT>>" not in lines[ln - 1]:
        problems.append(f"第{ln}行无缺陷哨兵")
    # 4) verdict 与类型一致（catch 类应为 catch）
    v = res[k].get("detector_verdict")
    if meta["defect_type"] in CATCH_TYPES and meta["expected_verdict"] != "catch":
        problems.append("catch型却标注miss")
    if meta["defect_type"] == "uninitialized_read" and v not in ("miss", "catch"):
        problems.append("uninit 检测器非 miss/catch")
    # 5) 检测器结果与标注一致（已调和）
    if v != meta["expected_verdict"]:
        problems.append(f"检测器{v}≠标注{meta['expected_verdict']}")
    status = "OK" if not problems else "BAD:" + ";".join(problems)
    if problems:
        check_fail += 1
    print(f"  {k} [{meta['defect_type']}] line{ln} det={v} exp={meta['expected_verdict']} -> {status}")

print(f"\n抽检不合格: {check_fail}/{len(sample_ids)} "
      f"({check_fail/len(sample_ids)*100:.1f}%)  <= 阈值10%? {check_fail/len(sample_ids) <= 0.10}")

bad_rate = check_fail / len(sample_ids)
stats = {
    "pooled": n, "failed": len(failed), "failed_ids": failed,
    "by_type": dict(pool_types), "severity": dict(sev),
    "planted_true": planted_true, "planted_ratio": planted_true / n,
    "warned": warned, "avg_time_s": round(avg_t, 3),
    "spotcheck_n": len(sample_ids), "spotcheck_fail": check_fail,
    "spotcheck_rate": round(bad_rate, 4),
    "spotcheck_ids": sorted(sample_ids),
}
json.dump(stats, open(os.path.join(EXP, "stats.json"), "w", encoding="utf-8"),
          ensure_ascii=False, indent=2)
print("\nstats.json 已写。")
