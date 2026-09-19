"""582 只读侦察③：metrics 三曲线/推翻/registry 实现 + MIS 样本 + liveness todo + 引用核验类工具。"""
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[2]
mc = (ROOT / "tools/metrics_collector.py").read_text(encoding="utf-8").splitlines()

print("=== metrics_collector 330-430 ===")
for i in range(329, min(len(mc), 430)):
    print(f"{i+1:5}|{mc[i][:110]}")

print()
print("=== 误解库 MIS 样本（前 2 个文件的关键字段）===")
misdir = ROOT / "misconceptions"
files = sorted(misdir.rglob("*.md"))
print(f"  {len(files)} 个 .md；首个: {files[0].relative_to(ROOT)}")
t = files[0].read_text(encoding="utf-8", errors="replace")
print("  ---- 头 40 行 ----")
for ln in t.splitlines()[:40]:
    print("   ", ln[:104])

print()
print("=== data/prop_liveness_todo.md 头 30 行 ===")
lt = ROOT / "data/prop_liveness_todo.md"
if lt.is_file():
    for ln in lt.read_text(encoding="utf-8").splitlines()[:30]:
        print("  ", ln[:104])

print()
print("=== 引用核验 / 溯源类工具与目录 ===")
for kw in ("reference", "citation", "source", "audit", "provenance", "trace"):
    hits = sorted({p.name for p in (ROOT / "tools").glob("*.py")
                   if kw in p.name.lower()})
    print(f"  tools/*{kw}* → {hits}")
print("  sources/:", [str(p.relative_to(ROOT)) for p in (ROOT / "sources").rglob("*")][:6])
print("  Memory/:", [str(p.relative_to(ROOT)) for p in (ROOT / "Memory").rglob("*")][:6])
print("  goldens/:", [str(p.relative_to(ROOT)) for p in (ROOT / "goldens").rglob("*")][:6])

print()
print("=== knowledge_graph.db 的表结构（只读连接）===")
import sqlite3
try:
    con = sqlite3.connect(f"file:{ROOT/'data/knowledge_graph.db'}?mode=ro", uri=True)
    for r in con.execute("SELECT name, type FROM sqlite_master WHERE type IN ('table','view')"):
        print("   ", r[0], r[1])
        try:
            cnt = con.execute(f"SELECT COUNT(*) FROM {r[0]}").fetchone()[0]
            print("      行数:", cnt)
        except Exception as e:
            print("      (计数失败:", e, ")")
    con.close()
except Exception as exc:
    print("  打开失败:", exc)
