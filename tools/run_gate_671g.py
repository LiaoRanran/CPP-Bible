#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""run_gate_671g.py — 671g 纪律门禁独立入口（14 条规则统一执行 + 退出码）。

与主门禁关系
============
* 14 条规则已在**工作树**挂进 `tools/run_master_gate_670c.py`（`gates_671g`，L0）；
  该共享文件同时承载 671a 在飞改动，671g 不整文件提交，最终批次合并点统一提交，避免混入在飞批次。
* 本文件是 **671g 自己拥有**的独立入口，行为与主门禁里的 671g 段一致：复用
  `gate_rules_671g.run_all`，额外先跑数字复算自检（collect 自洽），输出分层 finding。

用法
====
    python tools/run_gate_671g.py             # 0=无 block（warn 不阻断）；1=有 block
    python tools/run_gate_671g.py --json
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


def collect(root: Path) -> dict:
    import gate_rules_671g as G
    import numbers_671g as N
    findings = G.run_all(root)
    nums = N.collect(root)
    return {
        "schema": "queyi-gate-671g/v1",
        "rule_count": len(G.RULES),
        "numbers_self_inconsistent": nums.get("self_inconsistent", []),
        "findings": findings,
        "blocks": [f for f in findings if f.get("severity") == "block"],
        "warns": [f for f in findings if f.get("severity") == "warn"],
    }


def render(rep: dict) -> str:
    L = [f"[671g gate] 规则 {rep['rule_count']} 条 "
         f"block={len(rep['blocks'])} warn={len(rep['warns'])} "
         f"数字不自洽={rep['numbers_self_inconsistent']}"]
    for f in rep["findings"]:
        L.append(f"  [{f['severity'].upper()}] {f['rule']} {f['target']}: {f['message']}")
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g 纪律门禁独立入口")
    ap.add_argument("--root", default=None)
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else ROOT
    rep = collect(root)
    print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json else render(rep))
    return 1 if rep["blocks"] or rep["numbers_self_inconsistent"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
