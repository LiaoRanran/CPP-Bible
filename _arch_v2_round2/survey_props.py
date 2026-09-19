#!/usr/bin/env python3
"""533 勘察补充：observation/inference 命题计数与 observation 用证据结构。"""
import sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT / "tools"))
import atom_evidence_replay as R  # noqa: E402

obs = inf = 0
obs_ids: list[str] = []
ev_kind: dict[str, str] = {}
for p in sorted((ROOT / "evidence").rglob("EV-*.md")):
    m = R.parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
    ev_kind[str(m.get("id") or p.stem)] = str(m.get("kind"))

for p in sorted((ROOT / "atoms").rglob("ATOM-*.md")):
    m = R.parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
    aid = str(m.get("id") or p.stem)
    for pr in (m.get("claim_structured") or []):
        if not isinstance(pr, dict):
            continue
        ct = pr.get("claim_type")
        if ct == "observation":
            obs += 1
            evs = [str(e) for e in (pr.get("evidence") or [])]
            kinds = ",".join(sorted({ev_kind.get(e, "?") for e in evs}))
            obs_ids.append(f"{aid}/{pr.get('id')} [{kinds}] ev={'+'.join(evs)}")
        elif ct == "inference":
            inf += 1

print(f"observation={obs} inference={inf}")
for x in obs_ids:
    print(x)
print("\n按原子归并：")
for k, v in sorted(Counter(x.split("/")[0] for x in obs_ids).items()):
    print(k, v)
