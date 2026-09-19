"""528 任务1：校验一批卡回填后的解析与规则命中（用法：python _check528.py ATOM-A ...）。"""
import sys
from pathlib import Path

sys.path.insert(0, "tools")
import gate_engine as ge  # noqa: E402
import atom_evidence_replay as rp  # noqa: E402

BATCH = sys.argv[1:]
tot = 0
for p in ge._cards(ge.ATOMS, "ATOM-*.md"):
    if not any(b in p.stem for b in BATCH):
        continue
    m = rp.parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
    props = ge._claim_props(m)
    tot += len(props)
    types = [x.get("claim_type") for x in props]
    ok = all(x.get("id") and x.get("subject") and x.get("object")
             and x.get("claim_type") in ("observation", "inference")
             and x.get("extracted_by") for x in props)
    print(f"{p.stem:<26} props={len(props)} types={types} 结构合格={ok}")
print(f"本批命题总数 = {tot}")
hits = [f for f in ge.run(include_advice=True) if any(b in f.target for b in BATCH)]
if hits:
    for f in hits:
        print(f"  !! [{f.rule_id}] {f.severity} {f.target} :: {f.message[:110]}")
else:
    print("本批规则命中：无 ✓")
