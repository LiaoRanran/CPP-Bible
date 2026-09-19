"""571 任务 1 侦察：M3 为何只有 7 个可判变体 —— 全库卡的门禁读取面形状分布。"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "tools"))
import mutation_fuzz as mf   # noqa: E402

cards = sorted(set(Path("evidence").rglob("EV-*.md")) | set(Path("atoms").rglob("ATOM-*.md")))
rows = []
for p in cards:
    if "README" in p.name:
        continue
    t = p.read_text(encoding="utf-8")
    spans = mf._gate_read_spans(t)
    def in_gate(needle: str) -> bool:
        s = t.find(needle)
        while s != -1:
            if any(a <= s < b for a, b in spans):
                return True
            s = t.find(needle, s + 1)
        return False
    rows.append({
        "card": p.stem,
        "contains_in": in_gate("contains_in"),
        "absent_in": in_gate("absent_in"),
        "Werror": in_gate("-Werror"),
        "count": in_gate("count:"),
        "contains_any": in_gate("contains_any"),
        "kind_absent": in_gate("kind: absent"),
        "run_keys": in_gate("run_match_keys"),
        "Wflag": in_gate("-Wall") or in_gate("-Wextra"),
    })

print("卡总数", len(rows))
keys = ("contains_in", "absent_in", "Werror", "count", "contains_any", "kind_absent",
        "run_keys", "Wflag")
for k in keys:
    n = sum(1 for r in rows if r[k])
    print(f"  {k:12s} {n:3d} 卡")
unlock = {
    "删一条 artifact_assert 条目（任意卡）": len(rows),
    "删一个 run_match_keys（有声明的卡）": sum(1 for r in rows if r["run_keys"]),
}
print()
for k, v in unlock.items():
    print(f"  候选新变体可解锁：{k} -> {v} 卡")
print()
# M3 现状可判（含 _in / -Werror / count 任一）
now = [r["card"] for r in rows if r["contains_in"] or r["absent_in"] or r["Werror"] or r["count"]]
print("M3 现状可覆盖卡数（含 _in/-Werror/count 任一）:", len(now), now[:12])
