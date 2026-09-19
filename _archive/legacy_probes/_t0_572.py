"""572 任务 0：把 571 v2 里 M3 的 52 条逃逸逐条打印并三分类（a/b/c）。

- (a) 条目变少可对基线：删条目 / 删 run_match_keys ⇒ 变异后计数 < 变异前计数；
- (b) 恒真样板可识别：追加的候选符号被判为通用符号（复用 553 `_is_universal_symbol`）；
- (c) 结构性堵不住：现存断言本身就平凡（不是变异造成的）⇒ 登记不硬堵。
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "tools"))
import atom_evidence_replay as replay   # noqa: E402
import gate_engine as ge                # noqa: E402
import mutation_fuzz as mf              # noqa: E402

d = json.load(open("data/mutation/full_baseline_v2.json", encoding="utf-8"))
esc = [r for r in d["results"] if r["verdict"] == "escaped" and r["op"] == "M3"]
print("M3 逃逸总数:", len(esc))


def counts(text: str) -> tuple[int, int]:
    """(artifact_assert 条目数, run_match_keys 键数)——两种写法都能数。"""
    try:
        m = replay.parse_frontmatter(text)
    except ValueError:
        return (-1, -1)
    aa = m.get("artifact_assert")
    act = m.get("actual") or {}
    keys = (act.get("run_match_keys") if isinstance(act, dict) else None) or []
    return (len(aa) if isinstance(aa, list) else 0, len(keys) if isinstance(keys, list) else 0)


rows, cls = [], {"a": 0, "b": 0, "c": 0}
for r in esc:
    p = Path(r["card"])
    t = p.read_text(encoding="utf-8")
    b4 = counts(t)
    # 重新推导该变异点对应的变体文本
    vt, appended = None, []
    for point, vtext in mf.MUTATORS["M3"](t):
        if point == r["point"] and vtext is not None:
            vt = vtext
            break
    af = counts(vt) if vt else b4
    kind = "(?)"
    if vt and (af[0] < b4[0] or af[1] < b4[1]):
        kind = "a"
    elif vt and "contains_any" in vt[: vt.find("artifact_assert") + 2000] and af == b4:
        # 追加样板候选：从变体里摘出新增的候选符号（形如 texts: [..., ".file"]）
        seg = re.search(r"texts:\s*\[([^\]]*)\]", vt)
        if seg:
            cands = [x.strip().strip('"') for x in seg.group(1).split(",") if x.strip()]
            appended = [c for c in cands if ge._is_universal_symbol(c)]
        kind = "b" if appended else "c"
    else:
        kind = "c"
    cls[kind] = cls.get(kind, 0) + 1
    rows.append((p.stem, kind, r["point"][:38], b4, af, appended))

print()
print("三分类计数：", cls)
print()
print(f"{'卡':22s} {'类':2s} {'变异点':40s} {'前(aa,keys)':>12s} {'后':>10s} 通用符号")
for card, k, point, b4, af, app in rows:
    print(f"{card:22s} {k:2s} {point:40s} {str(b4):>12s} {str(af):>10s} {app}")

print()
print("== (c) 明细（结构性堵不住，登记不硬堵）==")
for card, k, point, b4, af, app in rows:
    if k == "c":
        print("  ", card, "|", point, "|", b4, "->", af)
