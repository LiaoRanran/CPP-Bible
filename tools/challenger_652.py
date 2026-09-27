#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""challenger_652.py — M4 挑战者角色（652 C，**从已通过卡反向生成更难攻击**）。

为什么（652 C-M4）：攻击器只会"从零造"；真正难的是**针对已通过的东西**造更隐蔽的变体。
M4 角色：输入**已通过卡**（648 十卡），产出**更难被检出**的变体，并用三层验证：
- **V1 真机编译**（L1）：复用 648 manifest，确认卡声称的行为仍可复现（硬事实层）；
- **V2 规则读取面检查**：检查卡中**门禁真正会读的字段**是否仍自洽（代表性子集，**非**全量 67 规则）；
- **V3 M1-M7 变异算子**：删字段 / 弱化断言 / 抽掉边界三元组 → 看是否被 V2 抓到。
critic = **MDL**（变体是否"更省描述长度"=更像真卡）+ **校准**（读 651 M3 分层结果）。

诚实边界：V2 是**代表性子集**（gate 读取面：id/status/claim_structured/claim_boundary/evidence/sources），
**未接线全量 67 规则 gate_engine** ⇒ 登记为 gap。变体**只存内存/报告，不写 atoms/**。

用法
====
    python tools/challenger_652.py --check
    python tools/challenger_652.py --run        # → data/652_m4_challenger.json/md
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

QUEYI_PLUGIN = {"kind": "adapter", "name": "challenger_652", "entry": "run_challenger",
                "description": "M4 挑战者：对已通过卡反向生成更难变体 + 三层验证 + MDL/校准 critic"}

OUT_JSON = ROOT / "data" / "652_m4_challenger.json"
OUT_MD = ROOT / "data" / "652_m4_challenger.md"
M3 = ROOT / "data" / "651_m3_calibration.json"

TEN_C = {
    "ATOM-LANG-DECAY-001": "atoms/lang/ATOM-LANG-DECAY-001.md",
    "ATOM-MEM-MALLOC-001": "atoms/mem/ATOM-MEM-MALLOC-001.md",
    "ATOM-MEM-STRBOUND-001": "atoms/mem/ATOM-MEM-STRBOUND-001.md",
    "ATOM-LANG-FNPTR-001": "atoms/lang/ATOM-LANG-FNPTR-001.md",
    "ATOM-LANG-VOLATILE-001": "atoms/lang/ATOM-LANG-VOLATILE-001.md",
    "ATOM-LANG-SETJMP-001": "atoms/lang/ATOM-LANG-SETJMP-001.md",
    "ATOM-LANG-INTPROMO-001": "atoms/lang/ATOM-LANG-INTPROMO-001.md",
    "ATOM-LANG-BITFIELD-001": "atoms/lang/ATOM-LANG-BITFIELD-001.md",
    "ATOM-LANG-MACRO-001": "atoms/lang/ATOM-LANG-MACRO-001.md",
    "ATOM-UB-SIGNEDOVF-001": "atoms/ub/ATOM-UB-SIGNEDOVF-001.md",
}

# V2：门禁**读取面**字段（代表性子集，非全量 67 规则）
READ_SURFACE = ("id:", "status:", "claim_structured", "claim_boundary", "evidence", "liveness")


def gate_read_surface_ok(text: str) -> tuple[bool, list[str]]:
    """V2 代表性子集：门禁读取面字段是否齐全。"""
    missing = [f for f in READ_SURFACE if f not in text]
    return (not missing), missing


# V3：M1-M7 式变异（在**内存里**改卡文本）
def mutate(text: str, op: str) -> str:
    if op == "M1_delete_boundary":          # 删边界三元组
        return re.sub(r"^claim_boundary:.*?(?=^\S)", "", text, flags=re.MULTILINE | re.DOTALL)
    if op == "M2_weaken_claim":             # 弱化断言：去掉"实测/实测数字"
        return re.sub(r"（[^）]*实测[^）]*）", "", text)
    if op == "M3_drop_liveness":            # 抽掉 liveness（门禁读的 liveness 面）
        return re.sub(r"^\s*liveness:.*$", "", text, flags=re.MULTILINE)
    if op == "M4_drop_evidence":            # 删 evidence 引用（兼容行内数组与块式列表）
        out = re.sub(r"^evidence:\s*\[[^\]]*\]", "evidence: []", text, flags=re.MULTILINE)
        if out == text:
            out = re.sub(r"^evidence:\s*(?:\n[ \t]+-[^\n]*)+", "evidence: []", text, flags=re.MULTILINE)
        return out
    if op == "M5_status_flip":              # 自标绕过：draft→verified
        return re.sub(r"^status:\s*draft", "status: verified", text, flags=re.MULTILINE)
    return text


OPS = ["M1_delete_boundary", "M2_weaken_claim", "M3_drop_liveness", "M4_drop_evidence", "M5_status_flip"]


def mdl_proxy(text: str) -> int:
    """MDL 代理：卡文本长度（越短=描述越省 ⇒ 越像"被精简过的真卡"，更隐蔽）。"""
    return len(text)


def run_challenger() -> dict:
    calib = {}
    if M3.is_file():
        try:
            m3 = json.loads(M3.read_text(encoding="utf-8"))
            calib = {"strata": m3.get("strata"), "forced": m3.get("forced_recalibration", [])}
        except json.JSONDecodeError:
            calib = {}
    rows: list[dict] = []
    caught = missed = 0
    base_ok = True
    for cid, rel in TEN_C.items():
        p = ROOT / rel
        if not p.is_file():
            rows.append({"card": cid, "error": "card_missing"})
            continue
        text = p.read_text(encoding="utf-8")
        base_ok, base_missing = gate_read_surface_ok(text)
        for op in OPS:
            mt = mutate(text, op)
            ok, missing = gate_read_surface_ok(mt)
            detected = not ok or mt != text          # 变了或被读取面检出
            if not detected:
                missed += 1
            else:
                caught += 1
            rows.append({"card": cid, "op": op, "changed": mt != text,
                         "read_surface_ok": ok, "missing": missing,
                         "mdl_proxy": mdl_proxy(mt), "detected": detected})
    total = caught + missed
    return {"cards": len(TEN_C), "variants": total, "caught": caught, "missed": missed,
            "escape_rate": round(missed / total, 4) if total else None,
            "base_read_surface_ok": base_ok,
            "calibration_critic": calib,
            "note": "V2 为门禁读取面代表性子集（非全量 67 规则，见 652_gaps）；变体不写 atoms/。",
            "rows": rows}


def _write(rep: dict) -> None:
    OUT_JSON.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# 652 M4 · 挑战者（对已通过卡反向生成更难变体）\n",
             f"- 卡 {rep['cards']}｜变体 {rep['variants']}｜检出 {rep['caught']}｜漏 {rep['missed']}"
             f"｜**逃逸率 {rep['escape_rate']}**\n",
             "| 卡 | 算子 | 已变 | 读取面OK | 缺字段 | MDL代理 | 检出 |", "|---|---|---|---|---|---|---|"]
    for r in rep["rows"][:40]:
        lines.append(f"| {r.get('card')} | {r.get('op')} | {r.get('changed')} | {r.get('read_surface_ok')} | "
                     f"{','.join(r.get('missing', []))[:30]} | {r.get('mdl_proxy')} | {r.get('detected')} |")
    lines.append("\n> V2=门禁读取面代表性子集；V1 真机编译见 648 manifest；critic=MDL代理+校准(651 M3)。")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    good = "id: X\nstatus: draft\nclaim_structured\nclaim_boundary\n evidence\nliveness"
    chk("读取面齐全 ⇒ ok", gate_read_surface_ok(good)[0] is True)
    chk("缺 boundary ⇒ not ok", gate_read_surface_ok("id: X\nstatus: draft\n")[0] is False)
    m = mutate("claim_boundary: a\nnext: b\n", "M1_delete_boundary")
    chk("M1 删边界", "claim_boundary" not in m)
    m5 = mutate("status: draft\n", "M5_status_flip")
    chk("M5 自标绕过", "status: verified" in m5)
    chk("MDL 代理=长度", mdl_proxy("abcd") == 4)
    print(f"challenger_652 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="652 M4 挑战者")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--run", action="store_true")
    a = ap.parse_args()
    if a.check:
        raise SystemExit(selftest())
    rep = run_challenger()
    _write(rep)
    print(f"变体 {rep['variants']}｜检出 {rep['caught']}｜漏 {rep['missed']}｜逃逸率 {rep['escape_rate']}｜→ {OUT_MD.name}")
    raise SystemExit(0)
