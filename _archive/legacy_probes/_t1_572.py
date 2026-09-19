"""572 任务 1/2 先量：(b) 的存量命中面 + 生成 (a) 的人审断言计数基线。"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "tools"))
import atom_evidence_replay as replay   # noqa: E402
import gate_engine as ge                # noqa: E402

BASE = Path("tools/assert_count_baseline.json")
cards = sorted(Path("evidence").rglob("EV-*.md"))
rows, stock_b = {}, []
for p in cards:
    m = replay.parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
    aa = m.get("artifact_assert")
    act = m.get("actual") or {}
    keys = (act.get("run_match_keys") if isinstance(act, dict) else None) or []
    rows[p.stem] = {"artifact_assert": len(aa) if isinstance(aa, list) else 0,
                    "run_match_keys": len(keys) if isinstance(keys, list) else 0}
    # (b) 存量面：已有的断言里**本来就有**通用/样板候选的
    for r in (aa if isinstance(aa, list) else []):
        if not isinstance(r, dict):
            continue
        kind = str(r.get("kind") or "")
        texts = ([r.get("text")] if r.get("text") else []) + list(r.get("texts") or [])
        uni = [t for t in texts if t and ge._is_universal_symbol(str(t))]
        if uni:
            stock_b.append((p.stem, kind, uni, len(texts)))

print("卡数:", len(rows))
print("(b) 存量命中（已有断言含通用候选的卡）:", len(stock_b))
for s in stock_b:
    print("   ", s)
print()
if not BASE.is_file() or "--write" in sys.argv:
    BASE.write_text(json.dumps({"note": "人审断言计数基线（只增不减；gate 用它比当前计数）",
                                "updated": "2026-09-17", "cards": rows},
                               ensure_ascii=False, indent=1, sort_keys=True) + "\n",
                    encoding="utf-8")
    print("基线已写:", BASE, "| 卡数:", len(rows),
          "| 断言条目合计:", sum(v["artifact_assert"] for v in rows.values()),
          "| 键合计:", sum(v["run_match_keys"] for v in rows.values()))
else:
    old = json.loads(BASE.read_text(encoding="utf-8"))["cards"]
    print("基线已存在：卡数", len(old))
