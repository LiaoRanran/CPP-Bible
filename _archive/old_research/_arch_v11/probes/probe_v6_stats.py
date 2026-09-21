#!/usr/bin/env python3
"""只读探针：解析 data/mutation/full_baseline_v6.json，输出全量口径统计。
不写任何文件（除 stdout）。用法：.venv\\Scripts\\python.exe _arch_v11\\probes\\probe_v6_stats.py
"""
from __future__ import annotations
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
p = ROOT / "data" / "mutation" / "full_baseline_v6.json"
rep = json.loads(p.read_text(encoding="utf-8"))

print("== top-level keys ==")
print(sorted(rep.keys()))
for k in ("variants", "blocked", "escaped", "n_a", "malformed", "out_of_scope",
          "equivalent", "equivalent_invalid", "strict_blocked", "strict_rate",
          "treated_rate", "jobs", "parallel", "elapsed_s", "ge_runs", "replay_runs",
          "replay_skipped", "root_fingerprint_ok"):
    if k in rep:
        print(f"{k} = {rep[k]}")
if "rates" in rep:
    print("rates =", json.dumps(rep["rates"], ensure_ascii=False))
print("n cards =", len(rep.get("cards", [])), " operators =", rep.get("operators"))

res = rep["results"]
print("\n== verdict x op (all variants) ==")
ops = sorted({r["op"] for r in res})
print("op      total  blocked escaped n_a    malformed out_of_scope equivalent")
for op in ops:
    rows = [r for r in res if r["op"] == op]
    c = Counter(r["verdict"] for r in rows)
    print("{op:7} {tot:6} {b:6} {e:7} {n:6} {m:9} {o:11} {q:10}".format(
        op=op, tot=len(rows), b=c.get("blocked", 0), e=c.get("escaped", 0),
        n=c.get("n_a", 0), m=sum(1 for r in rows if r.get("malformed")),
        o=sum(1 for r in rows if r.get("out_of_scope")),
        q=sum(1 for r in rows if r.get("equivalent"))))

print("\n== escaped_list (full) ==")
for r in rep.get("escaped_list", []):
    print(f"{r['card']} | {r['op']} | {r['point']}")
    print("   detail:", json.dumps({k: r.get(k) for k in
          ("new_block", "new_warn", "why", "kind")}, ensure_ascii=False))

print("\n== equivalent variants (grouped) ==")
eqs = [r for r in res if r.get("equivalent")]
print("total equivalent =", len(eqs))
by = Counter((r["op"], r["verdict"]) for r in eqs)
for k, v in sorted(by.items()):
    print(k, v)
for r in eqs:
    print(f"  {r['card']} | {r['op']} | {r['point'][:80]}")

print("\n== n_a why categories ==")
na = Counter()
for r in res:
    if r["verdict"] == "n_a":
        w = (r.get("why") or "")[:30]
        na[w] += 1
for k, v in na.most_common():
    print(v, k)

print("\n== cards per variant count top10 ==")
cc = Counter(r["card"] for r in res)
for k, v in cc.most_common(10):
    print(v, k)
print("distinct cards =", len(cc))
