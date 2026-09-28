#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""gate_tier_check_658.py — 校验门禁两层模型声明与 CI 实际一致。

不变式（658 B 段）：
  1. 每个 gate 必须属于 L0 或 L1；
  2. mutation_score 必须是 L1（禁止据此宣称外部效度）；
  3. L1 门禁若在 CI 里出现，必须 continue-on-error: true（不阻断合并）。

用法：
    python tools/gate_tier_check_658.py --check
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TIERS = os.path.join(ROOT, "tools", "gate_tiers_658.json")
WF_DIR = os.path.join(ROOT, ".github", "workflows")


def load_tiers():
    return json.load(open(TIERS, encoding="utf-8"))


def validate(tiers):
    errors = []
    l0 = {g["id"] for g in tiers["tiers"]["L0"]["gates"]}
    l1 = {g["id"] for g in tiers["tiers"]["L1"]["gates"]}
    for gid in l0 | l1:
        pass
    if "mutation_score" not in l1:
        errors.append("不变式违反：mutation_score 必须是 L1（禁止据此宣称外部效度）")
    # 校验每个 gate 有 id/name/why
    for tier, gid_set in (("L0", l0), ("L1", l1)):
        for g in tiers["tiers"][tier]["gates"]:
            for fld in ("id", "name", "why"):
                if fld not in g:
                    errors.append(f"{tier}/{g.get('id','?')} 缺字段 {fld}")
    return errors, l0, l1


def check_ci_continues(l1, l0):
    warns = []
    if not os.path.isdir(WF_DIR):
        return warns
    for fn in os.listdir(WF_DIR):
        if not fn.endswith(".yml"):
            continue
        txt = open(os.path.join(WF_DIR, fn), encoding="utf-8").read()
        # 找每个 step 的 name 与 continue-on-error
        steps = re.findall(r"-\s*name:\s*(.+?)\n((?:\s+[^-\n].*\n)*)", txt)
        for name, body in steps:
            name = name.strip()
            has_ce = "continue-on-error: true" in body
            for gid in l1:
                if gid in name.lower() or gid.replace("_", " ") in name.lower():
                    if not has_ce:
                        warns.append(f"[{fn}] L1 门禁 '{name}' 未设 continue-on-error（应非阻断）")
            for gid in l0:
                if gid in name.lower() or gid.replace("_", " ") in name.lower():
                    if has_ce:
                        warns.append(f"[{fn}] L0 门禁 '{name}' 设了 continue-on-error（红线不应被绕过）")
    return warns


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--check", action="store_true")
    ap.parse_args()
    tiers = load_tiers()
    errors, l0, l1 = validate(tiers)
    warns = check_ci_continues(l1, l0)
    print(f"L0 gates: {len(l0)}  L1 gates: {len(l1)}")
    for w in warns:
        print("  WARN:", w)
    if errors:
        print("[GATE-TIER-ERROR]")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    print("[OK] 门禁两层模型声明合法（mutation_score∈L1；CI 非阻断一致性见 WARN）")


if __name__ == "__main__":
    main()
