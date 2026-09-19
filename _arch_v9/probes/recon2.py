"""582 只读侦察②：prop_graph / stat_bounds / metrics / impact_analysis 的结构面（纯读）。"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]


def sigs(path: str, pat: str = r"^(def |class |SCHEMA|VERSION|_?[A-Z_]+ = )") -> None:
    p = ROOT / path
    print(f"=== {path}（{sum(1 for _ in p.open(encoding='utf-8'))} 行）===")
    for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
        if re.match(pat, ln):
            print(f"{i:5}|{ln[:104]}")


sigs("tools/prop_graph.py")
print()
sigs("tools/stat_bounds.py")
print()
sigs("tools/impact_analysis.py")

print()
print("=== prop_graph 的 SCHEMA 全文 ===")
t = (ROOT / "tools/prop_graph.py").read_text(encoding="utf-8")
m = re.search(r'SCHEMA = """(.*?)"""', t, re.S)
print(m.group(1)[:1400] if m else "（未按 SCHEMA = \"\"\" 形式书写）")

print()
print("=== 关键词定位 ===")
for kw in ("overturned", "verified_by_oracle", "valid_at", "asserted_at", "SYSTEM_TIME",
           "temporal", "bitemporal", "PROV"):
    hits = []
    for p in (ROOT / "tools").glob("*.py"):
        for i, ln in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if kw.lower() in ln.lower():
                hits.append(f"{p.name}:{i}")
    print(f"  {kw:18s} → {hits[:6] if hits else '（无）'}")
