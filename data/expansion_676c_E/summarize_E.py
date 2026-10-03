#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""summarize_E.py — 汇总 verify_results.json，产出验收报告要用的全部统计量。"""
from __future__ import annotations

import collections
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
R = json.load(open(os.path.join(HERE, "verify_results.json"), encoding="utf-8"))


def meta(sid):
    return json.load(open(os.path.join(HERE, f"sample_{sid}.json"), encoding="utf-8"))


ids = sorted(R.keys())
rows = []
for sid in ids:
    m = meta(sid)
    v = R[sid]
    rows.append(dict(
        sid=sid, dtype=m["defect_type"], sev=m["severity"],
        planted=m["planted"], exp=m["expected_verdict"],
        kind=v.get("primary_kind"), verdict=v.get("primary_verdict"),
        hung=bool(v.get("hung")), pooled=bool(v.get("pooled")),
        reconcile=v.get("reconcile"), syn=v.get("syntax_rc"),
        sec=v.get("secondary_verdict"), note=v.get("primary_note", ""),
        raw_rc=v.get("raw_rc", []), stab=v.get("stability"),
    ))

n = len(rows)
print(f"=== 总览 (n={n}) ===")
print("语法通过:", sum(1 for r in rows if r["syn"] == 0), "/", n)
print("入池:", sum(1 for r in rows if r["pooled"]), "/", n)
print("判定分布:", dict(collections.Counter(r["verdict"] for r in rows)))
print("调和分布:", dict(collections.Counter(r["reconcile"] for r in rows)))
print(f"实测 catch 率 = {sum(1 for r in rows if r['verdict']=='catch')/n:.1%}")
print(f"实测 盲区(miss)率 = {sum(1 for r in rows if r['verdict']=='miss')/n:.1%}")
print(f"标注与实测一致率 = "
      f"{sum(1 for r in rows if r['reconcile'] in ('consistent','consistent_blindspot'))/n:.1%}")

print("\n=== 类型分布 ===")
for t in ["memory_order", "atomic_ub", "deadlock", "aba_problem",
          "lock_priority_inversion", "condition_variable"]:
    sub = [r for r in rows if r["dtype"] == t]
    c = sum(1 for r in sub if r["verdict"] == "catch")
    p = sum(1 for r in sub if r["pooled"])
    print(f"{t:<26} n={len(sub):<4} catch={c:<4} miss={len(sub)-c:<4} 入池={p}")

print("\n=== 严重度 ===", dict(collections.Counter(r["sev"] for r in rows)))
print("=== planted 全为 true:", all(r["planted"] for r in rows))

print("\n=== 死锁/阻塞触发统计 ===")
dl = [r for r in rows if r["dtype"] == "deadlock"]
hung = [r for r in dl if r["hung"]]
print(f"deadlock 样本 {len(dl)}，运行超时(挂起) {len(hung)}，"
      f"触发率 {len(hung)/len(dl):.1%}")
print("  其中 TSan 自身报出 lock-order-inversion 的:",
      sum(1 for r in dl if "lock-order-inversion" in r["note"]), "个")
print("  死锁样本中判定为 catch 的:",
      sum(1 for r in dl if r["verdict"] == "catch"), "/", len(dl))
cv = [r for r in rows if r["dtype"] == "condition_variable"]
print(f"condition_variable 中因通知丢失而挂起的: "
      f"{sum(1 for r in cv if r['hung'])}/{len(cv)}")

print("\n=== 检测资产命中 ===")
for k, c in collections.Counter(r["kind"] for r in rows).items():
    sub = [r for r in rows if r["kind"] == k]
    print(f"{k:<8} n={c:<4} catch={sum(1 for r in sub if r['verdict']=='catch')}")

print("\n=== 降级样本（预期 catch -> 实测 miss，真实盲区）===")
dg = [r for r in rows if r["reconcile"] == "downgraded_to_miss_real_blindspot"]
print(f"共 {len(dg)} 个:", ", ".join(r["sid"] for r in dg))
print("\n=== 升级样本（预期 miss -> 实测 catch）===")
up = [r for r in rows if r["reconcile"] == "updated_to_catch"]
print(f"共 {len(up)} 个:", ", ".join(r["sid"] for r in up))

print("\n=== 盲区类型分布（哪些类型完全没有检测器）===")
bl = collections.Counter(r["dtype"] for r in rows if r["verdict"] == "miss")
for t, c in bl.most_common():
    tot = sum(1 for r in rows if r["dtype"] == t)
    print(f"  {t:<26} miss {c}/{tot} = {c/tot:.0%}")

if any(r["stab"] for r in rows):
    print("\n=== TSan 稳定性（复跑一致性）===")
    st = [r for r in rows if r["stab"]]
    ok = sum(1 for r in st if r["stab"]["stable"])
    print(f"抽检 {len(st)} 个，每个复跑 {len(st[0]['stab']['verdicts'])} 轮，"
          f"一致 {ok}/{len(st)} = {ok/len(st):.1%}")
    for r in st:
        if not r["stab"]["stable"]:
            print(f"  不稳定: {r['sid']} {r['stab']['verdicts']}")

print("\n=== raw rc 分布（124 = timeout 挂起）===")
print(dict(collections.Counter(x for r in rows for x in r["raw_rc"])))
