"""575 任务 0.3 盘点：50 条 observation 命题能不能在**命题级**指认活性锚？

输出：命题 id / 所属卡 / 引用证据卡 / 可锚形态（fixture_symbol / quantified / run_key / 无）
      + **若强制命题级锚会新增多少 warn**（这就是 warn 债务规模，先报后建字段）。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "tools"))
import atom_evidence_replay as replay   # noqa: E402
import gate_engine as ge                # noqa: E402

atoms = sorted(Path("atoms").rglob("ATOM-*.md"))
evs = sorted(Path("evidence").rglob("EV-*.md"))
ev_by_id = {}
for p in evs:
    try:
        m = replay.parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
    except ValueError:
        continue
    ev_by_id[str(m.get("id") or p.stem)] = (p, m)

rows = []
for p in atoms:
    meta = ge._meta(p)
    for prop in ge._claim_props(meta):
        ct = str(prop.get("claim_type") or "").strip()
        if ct != "observation":
            continue
        pid = str(prop.get("prop-id") or prop.get("id") or "?")
        refs = [str(x) for x in (prop.get("evidence") or []) if str(x)]
        if not refs:      # 命题没写 evidence ⇒ 退回卡级 evidence 字段
            refs = [str(x) for x in (meta.get("evidence") or []) if str(x)]
        forms = set()
        for r in refs:
            hit = ev_by_id.get(r)
            if not hit:
                continue
            _, em = hit
            if ge._has_fixture_specific_assert_symbol(em):
                forms.add("fixture_symbol")
            if ge._has_non_env_run_key(em):
                forms.add("run_key")
            fal = str(em.get("falsification") or "")
            if ge._falsification_quantified(fal):
                forms.add("quantified")
        rows.append((str(meta.get("id") or p.stem), pid, ",".join(refs) or "-",
                     ",".join(sorted(forms)) or "无", bool(prop.get("liveness"))))

print("observation 命题数:", len(rows))
print()
print(f"{'卡':24s} {'命题':8s} {'引用卡':14s} {'可锚形态':22s} 已有liveness")
for c, pid, refs, forms, has in rows:
    print(f"{c:24s} {pid:8s} {refs:14s} {forms:22s} {'是' if has else '否'}")

n_anchor = sum(1 for r in rows if r[3] != "无")
n_none = len(rows) - n_anchor
n_field = sum(1 for r in rows if r[4])
print()
print("可锚（引用卡上能定位到至少一种形态）:", n_anchor)
print("引用卡上找不到任何活性形态      :", n_none)
print("卡面已写 liveness 字段的        :", n_field)
print("⇒ 若规则=『observation 命题须显式声明 liveness』，新增 warn =", len(rows) - n_field)
print("⇒ 若规则=『缺锚 且 引用卡上确实找得到形态』才 warn，新增 warn =", n_anchor)
