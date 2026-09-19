"""582 只读侦察④：引用核验工具 + KG 写点 + 前轮结论头（避免重复）。"""
import pathlib
import re

ROOT = pathlib.Path(__file__).resolve().parents[2]


def head(path: str, n: int = 26) -> None:
    p = ROOT / path
    if not p.is_file():
        print(f"=== {path} 不存在 ===")
        return
    print(f"=== {path}（{sum(1 for _ in p.open(encoding='utf-8'))} 行）头 {n} 行 ===")
    for i, ln in enumerate(p.read_text(encoding="utf-8").splitlines()[:n], 1):
        print(f"{i:5}|{ln[:108]}")


head("tools/check_citations.py", 30)
print()
head("tools/d5_source_integrity.py", 18)
print()
head("tools/verification_audit.py", 14)

print("=== knowledge_graph 的写点 ===")
for p in (ROOT / "tools").glob("*.py"):
    for i, ln in enumerate(p.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
        if "knowledge_graph" in ln:
            print(f"  {p.name}:{i}: {ln.strip()[:100]}")

print()
for f in ("_arch_v8/00_总览.md", "_arch_v8/03_NDW三档.md"):
    head(f, 22)
    print()
