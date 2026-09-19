"""571 任务 1：v2 全量基线摘要（等它落盘，然后逐算子对比 v1 + 贴 C-P 区间）。"""
import json
import time
from pathlib import Path

V2 = Path("data/mutation/full_baseline_v2.json")
V1 = Path("data/mutation/full_baseline_v1.json")

t0 = time.time()
while not V2.is_file() and time.time() - t0 < 420:
    time.sleep(10)

if not V2.is_file():
    print("v2 未落盘（超时）—— 见 _v2_571.err 尾部")
    raise SystemExit(0)

d = json.load(open(V2, encoding="utf-8"))
v1 = json.load(open(V1, encoding="utf-8"))
print("v2 elapsed_s:", d.get("elapsed_s"), "| variants:", d.get("variants"),
      "| cards:", len(d.get("cards") or []))
print()
hdr = f"{'算子':4s} | {'v1 b/e/na':>12s} | {'v2 b/e/na':>12s} | {'可判':>4s} | 逃逸率 (95% C-P)"
print(hdr)
for op in d.get("operators", []):
    a = (v1.get("by_operator") or {}).get(op, {})
    b = (d.get("by_operator") or {}).get(op, {})
    r = (d.get("by_operator_rates") or {}).get(op, {})
    esc = r.get("escape") or {}
    a1 = f"{a.get('blocked')}/{a.get('escaped')}/{a.get('n_a')}"
    b1 = f"{b.get('blocked')}/{b.get('escaped')}/{b.get('n_a')}"
    er = f"{esc.get('numerator')}/{esc.get('denominator')} = {esc.get('point')} " \
         f"[{esc.get('cp_low')}, {esc.get('cp_high')}]"
    print(f"{op:4s} | {a1:>12s} | {b1:>12s} | {r.get('judged'):>4} | {er}")
print()
m3 = (d.get("by_operator_rates") or {}).get("M3") or {}
print("M3 全量：judged =", m3.get("judged"), "| n_a =", m3.get("n_a"),
      "| strict =", json.dumps(m3.get("strict"), ensure_ascii=False))
print("M3 escape =", json.dumps(m3.get("escape"), ensure_ascii=False))
print("rate_flags:", json.dumps(d.get("rate_flags"), ensure_ascii=False))
from collections import Counter   # noqa: E402
res = d.get("results") or []
print()
print("按变异点（M3）：")
for k, v in Counter(r["point"][:40] for r in res if r["op"] == "M3").most_common():
    print(f"  {v:3d}  {k}")
esc = [r for r in res if r["verdict"] == "escaped"]
print()
print("逃逸总数:", len(esc), "| 按算子:", dict(Counter(r["op"] for r in esc)))
print("M3 逃逸按点:")
for k, v in Counter(r["point"][:40] for r in esc if r["op"] == "M3").most_common():
    print(f"  {v:3d}  {k}")
