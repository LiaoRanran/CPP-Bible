"""582 只读侦察①：资产层文件清点 + 关键 jsonl/json 头几行（**纯读，不写正式目录**）。"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]   # _arch_v9/probes → 仓库根

print("=== data/ 递归清点（顶层 + 一级子目录） ===")
d = ROOT / "data"
for p in sorted(d.iterdir()):
    if p.is_file():
        print(f"  {p.name:34s} {p.stat().st_size/1024:8.1f} KB")
    elif p.is_dir():
        n = sum(1 for _ in p.rglob("*") if _.is_file())
        tot = sum(_.stat().st_size for _ in p.rglob("*") if _.is_file())
        print(f"  {p.name + '/':34s} {n:5d} 文件 {tot/1024/1024:8.2f} MB")

print()
print("=== metrics.jsonl（最后 2 条） ===")
m = d / "metrics.jsonl"
if m.is_file():
    lines = [ln for ln in m.read_text(encoding="utf-8").splitlines() if ln.strip()]
    print(f"  条数={len(lines)}")
    for ln in lines[-2:]:
        o = json.loads(ln)
        print("  keys:", list(o)[:10])
        print("  ", json.dumps({k: o[k] for k in list(o)[:6]}, ensure_ascii=False)[:400])

print()
print("=== oracle_registry.json ===")
o = d / "oracle_registry.json"
if o.is_file():
    print("  ", o.read_text(encoding="utf-8")[:900].replace("\n", " "))

print()
print("=== 推翻事件 / golden_state / knowledge_graph 位置核对 ===")
for name in ("overturned_events.jsonl", "golden_state.json", "knowledge_graph.db",
             "claim_structured_staging.txt", "prop_liveness_todo.md"):
    hits = list(ROOT.rglob(name))
    print(f"  {name:32s} → {[str(h.relative_to(ROOT)) for h in hits][:3]}")

print()
print("=== 顶层目录一览 ===")
for p in sorted(ROOT.iterdir()):
    if p.is_dir() and not p.name.startswith((".", "_")):
        n = sum(1 for _ in p.rglob("*") if _.is_file())
        print(f"  {p.name:24s} {n:5d} 文件")
