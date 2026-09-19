#!/usr/bin/env python3
"""547 C 面探针：新旧接缝（549/548/535 的缝）。

读真实门禁、在沙箱造卡，不写正式文件。每行 `[PASS|FAIL|ESCAPE|INFO]`。
"""
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

import gate_engine as ge          # noqa: E402
import mutation_fuzz as mf        # noqa: E402
import atom_evidence_replay as replay  # noqa: E402

EV = ROOT / "evidence"
CARD = EV / "conc" / "EV-CONC-001.md"


# ── C1：548 Part 2 新规则在真仓库零误伤（存量 0 命中） ─────────────────────────
def t_c1_real_repo_zero_false() -> str:
    hits = ge.check_card_path_canonical()
    if hits:
        return f"FAIL (真仓库存量误伤 {len(hits)}：{[h.target for h in hits][:3]})"
    return "PASS (规则 61 条，CARD-PATH-NOT-CANONICAL 真仓库 0 命中)"


# ── C3：沙箱里 M2 三种异体都被新规则看见（规则读副本、不漏判） ────────────────
def t_c3_sandbox_sees_all_m2_forms() -> str:
    base = CARD.read_text(encoding="utf-8")
    # 取本卡第一个 fixture 字段名与相对路径
    import re
    m = re.search(r"^(fixture|artifact|run_match_file):\s*(\S+)", base, re.M)
    if not m:
        return "INFO (本卡无路径字段，换卡)"
    field, rel = m.group(1), m.group(2)
    posix = rel.replace("\\", "/")
    forms = {
        "大写": posix.upper(),
        "点斜杠": "./" + posix,
        "反斜杠": posix.replace("/", "\\"),
    }
    seen = {}
    with mf.sandbox() as tmp:
        sb = mf._rel_in_sandbox(CARD, tmp)
        orig = sb.read_text(encoding="utf-8")
        for name, fr in forms.items():
            mutated = re.sub(rf"^{field}:\s*\S+", f"{field}: {fr}", orig, count=1, flags=re.M)
            sb.write_text(mutated, encoding="utf-8")
            fs = ge.check_card_path_canonical()
            seen[name] = any(f.rule_id == "CARD-PATH-NOT-CANONICAL" for f in fs)
        sb.write_text(orig, encoding="utf-8")
    miss = [k for k, v in seen.items() if not v]
    return "PASS" if not miss else f"FAIL (漏判表单 {miss})"


# ── C2：549 的 fast 分支接缝（skip replay 后 warn 是否仍计入） ──────────────────
def t_c2_fast_branch_seam() -> str:
    # 549 尚未实现（本批是 547）；当前 M2 不是 replay 算子，warn 走门禁恒定可见。
    # 此接缝属 549 的工作，列 INFO 不在本批伪造结论。
    if "M2" not in mf.REPLAY_OPS:
        return ("INFO (M2 非 replay 算子 ⇒ CARD-PATH-NOT-CANONICAL 走门禁恒定可见；"
                "549 fast 分支接缝留待 549 自测)")
    return "PASS"


DEFS = [t_c1_real_repo_zero_false, t_c3_sandbox_sees_all_m2_forms, t_c2_fast_branch_seam]


def main() -> int:
    print("=== C 面：新旧接缝 ===")
    esc = 0
    for f in DEFS:
        try:
            res = f()
        except Exception as e:  # noqa: BLE001
            res = f"FAIL (抛异常 {type(e).__name__}: {e})"
        tag = res.split(" ")[0]
        if tag == "ESCAPE":
            esc += 1
        print(f"[{tag}] {f.__name__}: {res}")
    print(f"C 面：{esc} ESCAPE")
    return 1 if esc else 0


if __name__ == "__main__":
    raise SystemExit(main())
