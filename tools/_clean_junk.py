import re, shutil
from pathlib import Path

ROOT = Path("Book")
BAK_SUFFIX = ".preclean.bak"

# 灌水签名（真实章绝不会用这些标题命名节）
JUNK_RE = re.compile(
    r"^##\s+"
    r"(附录\s*Z\b"          # 附录 Z
    r"|附录\s*Z\+"          # 附录 Z+
    r"|附录\s*ZZ"           # 附录 ZZ / ZZZ
    r"|附录\s*FINAL"        # 附录 FINAL
    r"|维度增强\d*"         # 维度增强 / 维度增强2
    r")",
    re.IGNORECASE,
)

def clean_file(path: Path):
    lines = path.read_text(encoding="utf-8").split("\n")
    h2 = [(i, l) for i, l in enumerate(lines) if l.startswith("## ")]
    delete = set()
    junk_sections = []
    for k, (i, h) in enumerate(h2):
        if JUNK_RE.match(h):
            nxt = h2[k + 1][0] if k + 1 < len(h2) else len(lines)
            for j in range(i, nxt):
                delete.add(j)
            junk_sections.append(h.strip())
    if not delete:
        return None
    new_lines = [l for j, l in enumerate(lines) if j not in delete]
    # 备份
    bak = path.with_suffix(path.suffix + BAK_SUFFIX)
    if not bak.exists():
        shutil.copy(path, bak)
    path.write_text("\n".join(new_lines), encoding="utf-8")
    return {"file": str(path.relative_to(ROOT)), "removed": len(delete),
            "sections": junk_sections}

# 跑全部章（不含 .bak / .preclean.bak）
total_removed = 0
changed = []
for p in sorted(ROOT.glob("**/*.md")):
    if p.name.endswith(".bak") or p.name.endswith(BAK_SUFFIX):
        continue
    r = clean_file(p)
    if r:
        changed.append(r)
        total_removed += r["removed"]

print(f"清理章数: {len(changed)}")
print(f"删除总行数: {total_removed}")
print("\n=== 明细 ===")
for r in changed:
    print(f"  -{r['removed']:>4}行  {r['file']}")
    for s in r["sections"]:
        print(f"        · {s}")
