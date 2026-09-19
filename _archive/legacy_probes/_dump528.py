"""528 任务1：批量导出资子的 claim + 证据读数（写命题须逐字准确，不靠印象）。

用法：python _dump528.py ATOM-A ATOM-B ...
"""
import sys
from pathlib import Path

sys.path.insert(0, "tools")
import gate_engine as ge  # noqa: E402
import atom_evidence_replay as rp  # noqa: E402

idx = ge._ev_index()
for aid in sys.argv[1:]:
    hits = [q for q in ge._cards(ge.ATOMS, "ATOM-*.md") if q.stem == aid]
    if not hits:
        print("!! 找不到卡:", aid)
        continue
    m = rp.parse_frontmatter(hits[0].read_text(encoding="utf-8", errors="replace"))
    print("=" * 74)
    print(aid, "| status=", m.get("status"), "| 人签=", ge._has_human_signoff(m))
    print("title:", m.get("title"))
    print("claim:", str(m.get("claim") or "").replace("\n", " ")[:620])
    srcs = [s for s in (m.get("sources") or []) if isinstance(s, dict)]
    print(f"sources({len(srcs)}):")
    for s in srcs:
        print("   indep=", s.get("independent"), "|", str(s.get("kind")), "|",
              str(s.get("ref"))[:88])
    for eid in [str(r).strip() for r in ge._as_list(m.get("evidence")) if str(r).strip()]:
        em = idx.get(eid) or {}
        print(f"  -- {eid}: artifact={str(em.get('artifact'))[:58]}")
        for r in (em.get("artifact_assert") or [])[:3]:
            print("       assert:", str(r)[:100])
        for k, v in (em.get("actual") or {}).items():
            print(f"       {k}: {str(v)[:220]}")
