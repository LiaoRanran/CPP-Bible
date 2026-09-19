"""575 任务 3：产出「待补命题级活性锚」清单（**只列清单，机器绝不写入卡面**）。

输出 data/prop_liveness_todo.md：卡 / 命题 / 引用卡 / 可锚形态 / **建议可锚符号（仅提示）**。
补锚是知识活 —— 交人或 576 之后的强模型知识轮。
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent / "tools"))
import gate_engine as ge                # noqa: E402
import atom_evidence_replay as replay   # noqa: E402

ev_by_id = {}
for p in sorted(Path("evidence").rglob("EV-*.md")):
    try:
        m = replay.parse_frontmatter(p.read_text(encoding="utf-8", errors="replace"))
    except ValueError:
        continue
    ev_by_id[str(m.get("id") or p.stem)] = (p, m)

rows = []
for p in sorted(Path("atoms").rglob("ATOM-*.md")):
    meta = ge._meta(p)
    for prop in ge._claim_props(meta):
        if str(prop.get("claim_type") or "").strip() != "observation":
            continue
        if isinstance(prop.get("liveness"), dict) and prop.get("liveness"):
            continue                       # 已有锚 ⇒ 不在待补清单里
        pid = str(prop.get("prop-id") or prop.get("id") or "?")
        refs = [str(r) for r in ge._as_list(prop.get("evidence")) if str(r)]
        sug, forms = "-", set()
        for r in refs:
            hit = ev_by_id.get(r)
            if not hit:
                continue
            _, em = hit
            if ge._has_fixture_specific_assert_symbol(em):
                forms.add("fixture_symbol")
                if sug == "-":
                    for rr in (em.get("artifact_assert") if isinstance(em.get("artifact_assert"), list) else []):
                        if not isinstance(rr, dict):
                            continue
                        for t in ge._assert_targets(rr)[1]:
                            t = str(t).strip()
                            if t and not ge._is_universal_symbol(t):
                                sug = t
                                break
                        if sug != "-":
                            break
            if ge._has_non_env_run_key(em):
                forms.add("run_key")
            if ge._falsification_quantified(em.get("falsification")):
                forms.add("quantified")
        rows.append((str(meta.get("id") or p.stem), pid, ",".join(refs) or "-",
                     ",".join(sorted(forms)) or "无", sug))

out = Path("data/prop_liveness_todo.md")
lines = ["# 待补命题级活性锚清单（575 任务 3）", "",
         "> 机器产出清单，**绝不自动写入卡面**：补锚是知识活，交人或 576 之后的强模型知识轮。",
         "> 判据：`claim_structured[*].liveness = {kind: fixture_symbol, symbol: <夹具特有符号>}`，",
         "> 符号须真实出现在本命题引用卡的工件断言中、且非通用符号。", "",
         f"**缺锚 observation 命题：{len(rows)} 条**", "",
         "| 卡 | 命题 | 引用卡 | 可锚形态 | 建议可锚符号（仅提示） |",
         "|---|---|---|---|---|"]
for c, pid, refs, forms, sug in rows:
    lines.append(f"| {c} | {pid} | {refs} | {forms} | `{sug}` |")
out.write_text("\n".join(lines) + "\n", encoding="utf-8")
print("待补锚命题数:", len(rows), "→", out)
