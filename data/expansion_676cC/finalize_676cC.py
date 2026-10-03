#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""finalize_676cC.py — 统计 + 入池 + INDEX + 20% 抽检（Task D/E/F 准备）。

读取 verify_results.json 与各 sample_NNN.json，计算：
  - 生成/淘汰/入池数，各类型分布，severity，planted 比例
  - 盲区比例（expected_verdict=miss 或 实测 miss）
  - 优化敏感比例（optimization_dependent 中 O0/O2 行为不同者）
  - 平均验证耗时
  - 入池样本复制到 data/holdout_expansion/expC/ + 写 INDEX.json
  - 20% 固定种子抽检（字段完整/哨兵/缺陷真实/判定一致）
"""
import os, json, random, shutil
from collections import Counter

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
EXP = os.path.join(REPO, "data", "expansion_676cC")
POOL = os.path.join(REPO, "data", "holdout_expansion", "expC")
VOCAB = {"move_semantics", "raii_violation", "virtual_function", "cross_tu_ub",
         "optimization_dependent", "conditional_trigger"}
os.makedirs(POOL, exist_ok=True)

res = json.load(open(os.path.join(EXP, "verify_results.json"), encoding="utf-8"))

pooled = [k for k, v in res.items() if v.get("pooled")]
failed = [k for k, v in res.items() if not v.get("pooled")]

by_type = Counter()
sev = Counter()
planted_true = 0
miss_count = 0
opt_total = 0
opt_sensitive = 0
times = []
for k in pooled:
    meta = json.load(open(os.path.join(EXP, k + ".json"), encoding="utf-8"))
    by_type[meta["defect_type"]] += 1
    sev[meta["severity"]] += 1
    if meta.get("planted") is True:
        planted_true += 1
    if res[k].get("detector_verdict") == "miss" or meta.get("expected_verdict") == "miss":
        miss_count += 1
    v = meta.get("verification", {})
    if meta["defect_type"] == "optimization_dependent":
        opt_total += 1
        if v.get("opt_output_differs") or (v.get("opt_O0_detector") != v.get("opt_O2_detector")):
            opt_sensitive += 1
    if res[k].get("elapsed_s") is not None:
        times.append(res[k]["elapsed_s"])

n = len(pooled)
avg_t = (sum(times) / len(times)) if times else 0
blind_ratio = miss_count / n if n else 0
opt_ratio = (opt_sensitive / opt_total) if opt_total else 0

# ---------- 入池复制 ----------
copied = 0
for k in pooled:
    meta = json.load(open(os.path.join(EXP, k + ".json"), encoding="utf-8"))
    for f in meta.get("source_files", [k + ".cpp"]):
        shutil.copy2(os.path.join(EXP, f), os.path.join(POOL, f))
    shutil.copy2(os.path.join(EXP, k + ".json"), os.path.join(POOL, k + ".json"))
    copied += 1

# ---------- INDEX.json ----------
index = {
    "agent": "676c-expC", "category": "C", "pooled": n, "failed": len(failed),
    "failed_ids": failed, "by_type": dict(by_type), "severity": dict(sev),
    "blind_spot_ratio": round(blind_ratio, 4),
    "optimization_sensitive_ratio": round(opt_ratio, 4),
    "avg_time_s": round(avg_t, 3),
    "index": [{"id": k, "defect_type": json.load(open(os.path.join(EXP, k + ".json"), encoding="utf-8"))["defect_type"],
               "severity": json.load(open(os.path.join(EXP, k + ".json"), encoding="utf-8"))["severity"],
               "expected_verdict": json.load(open(os.path.join(EXP, k + ".json"), encoding="utf-8"))["expected_verdict"],
               "detector": (json.load(open(os.path.join(EXP, k + ".json"), encoding="utf-8")).get("expected_detectors") or ["asan"])[0],
               "defect_line": json.load(open(os.path.join(EXP, k + ".json"), encoding="utf-8"))["defect_location"]["line"],
               "planted": True} for k in pooled],
}
json.dump(index, open(os.path.join(POOL, "INDEX.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)

# ---------- Task D 抽检 ----------
random.seed(6762)
spot_ids = sorted(random.sample(pooled, max(1, round(n * 0.2))))
bad = 0
for k in spot_ids:
    meta = json.load(open(os.path.join(EXP, k + ".json"), encoding="utf-8"))
    problems = []
    for fld in ("defect_type", "severity", "planted", "expected_verdict",
                "expected_detectors", "trigger_condition", "notes"):
        if not meta.get(fld) and meta.get(fld) is not False and fld != "planted":
            problems.append("empty:" + fld)
    if meta.get("planted") is not True:
        problems.append("planted!=true")
    if meta["defect_type"] not in VOCAB:
        problems.append("type oov")
    if meta["expected_verdict"] not in ("catch", "miss"):
        problems.append("verdict bad")
    if not isinstance(meta.get("expected_detectors"), list) or not meta["expected_detectors"]:
        problems.append("detectors bad")
    if meta["defect_type"] == "optimization_dependent" and not meta.get("optimization_sensitivity"):
        problems.append("opt_sens missing")
    dl = meta.get("defect_location", {})
    ln = dl.get("line")
    # 跨文件样本 source_files[0] 可能是 .h，而哨兵在 .cpp；扫描所有源文件定位缺陷行。
    sent_ok = False
    if isinstance(ln, int) and ln >= 1:
        for sf in meta.get("source_files", [k + ".cpp"]):
            fp = os.path.join(EXP, sf)
            if os.path.isfile(fp):
                fl = open(fp, encoding="utf-8").read().splitlines()
                if ln <= len(fl) and "<<PLANTED-DEFECT>>" in fl[ln - 1]:
                    sent_ok = True; break
    if not sent_ok:
        problems.append("defect line bad")
    if res[k].get("detector_verdict") != meta["expected_verdict"]:
        problems.append("verdict mismatch")
    if problems:
        bad += 1
        print("  SPOT-BAD", k, problems)
print(f"spotcheck {len(spot_ids)} sampled, bad={bad} ({bad/len(spot_ids)*100:.1f}%)")

stats = {
    "generated": n + len(failed), "pooled": n, "failed": len(failed), "failed_ids": failed,
    "by_type": dict(by_type), "severity": dict(sev), "planted_true": planted_true,
    "planted_ratio": planted_true / n, "blind_spot_ratio": round(blind_ratio, 4),
    "opt_total": opt_total, "opt_sensitive": opt_sensitive, "opt_ratio": round(opt_ratio, 4),
    "avg_time_s": round(avg_t, 3), "spotcheck_n": len(spot_ids), "spotcheck_bad": bad,
    "spotcheck_rate": round(bad / len(spot_ids), 4), "spotcheck_ids": spot_ids,
}
json.dump(stats, open(os.path.join(EXP, "stats.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
print(f"\nPOOLED={n} FAILED={len(failed)} blind={blind_ratio*100:.1f}% opt_sens={opt_ratio*100:.1f}% avg={avg_t:.2f}s")
print(f"by_type={dict(by_type)}")
print(f"copied {copied} samples to {POOL}")
