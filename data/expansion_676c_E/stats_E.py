#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""stats_E.py — 验收报告用的精确数字汇总（只读，不改任何池文件）。"""
import glob
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "verify_results.json"), encoding="utf-8"))
M = {}
for f in glob.glob(os.path.join(HERE, "sample_E*.json")):
    sid = os.path.basename(f)[len("sample_"):-len(".json")]
    M[sid] = json.load(open(f, encoding="utf-8"))

dl = [s for s in sorted(R) if M[s]["defect_type"] == "deadlock"]
tot = hit = perfect = 0
for s in dl:
    fl = R[s].get("flakiness") or {}
    vs = fl.get("verdicts") or [R[s]["primary_verdict"]]
    tot += len(vs)
    hit += sum(1 for v in vs if v == "catch")
    if all(v == "catch" for v in vs):
        perfect += 1
print(f"deadlock 样本 {len(dl)}；复跑轮次合计 {tot}；catch 次数 {hit}；"
      f"每轮触发率 {hit/tot:.1%}；全轮次都触发的样本 {perfect}/{len(dl)}")
loi = [s for s in dl if "lock-order-inversion" in R[s].get("primary_note", "")]
print("TSan 自身报出 lock-order-inversion 的样本:", loi)

hung = [s for s in sorted(R) if R[s].get("hung")]
byt = {}
for s in hung:
    byt.setdefault(M[s]["defect_type"], []).append(s)
print("\n全池因挂起(timeout rc=124)被判定 catch 的样本:", len(hung))
for t, ss in sorted(byt.items()):
    print(f"  {t:<26} {len(ss):<3} {ss if len(ss) <= 6 else str(ss[:6]) + ' ...'}")

print("\n=== 调和清单 ===")
for tag in ("downgraded_to_miss_real_blindspot", "updated_to_catch"):
    ss = [s for s in sorted(R) if R[s].get("reconcile") == tag]
    print(f"{tag} ({len(ss)}):")
    print("   " + ", ".join(f"{s}[{M[s]['defect_type']}]" for s in ss))

print("\n=== 复跑非确定样本（全池）===")
flaky = []
for s in sorted(R):
    for key in ("flakiness", "stability"):
        f = R[s].get(key)
        if f and not f.get("stable", True):
            flaky.append((s, key, f["verdicts"]))
for s, key, vs in flaky:
    print(f"  {s} {M[s]['defect_type']:<24} {vs}")
print("合计", len(flaky), "个非确定样本")

print("\n=== atomic_ub 中ubsan/asan/tsan 全部 miss 的（无对应检测器）===")
ub = [s for s in sorted(R) if M[s]["defect_type"] == "atomic_ub"
      and R[s].get("primary_verdict") == "miss"]
print(len(ub), ub)

print("\n=== 各类型 -> 主资产 -> 命中 ===")
import collections
agg = collections.Counter()
for s in sorted(R):
    agg[(M[s]["defect_type"], R[s].get("primary_kind"),
         R[s].get("primary_verdict"))] += 1
for (t, k, v), c in sorted(agg.items()):
    print(f"  {t:<26} {k:<6} {v:<6} {c}")
