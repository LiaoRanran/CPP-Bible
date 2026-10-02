#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""itt_discipline_671g.py — 671g E2：ITT（意向治疗）口径纪律。

医学 ITT
==========
临床试验 ITT：**所有随机入组样本都计入分析**，不能因为"药没吃上/检测器不支持"就剔除——
否则剔除与结局相关时偏差巨大。本项目对应：**所有入检测集的样本必须计入某一口径**，
unknown（检测器不支持）可以**不进主分母**，但必须：

  1. 显式登记（哪些 id、为什么 unknown）；
  2. 排除理由**在实验前/预注册（PAP）中声明**，不能看到结果后再剔；
  3. 报告全样本口径（unknown 记 miss 的保守率），不允许只报可测率。

登记 data/671g/itt_exclusions.json：{experiment: {pap_id, exclusions:[{id,reason,preregistered}]}}
门禁 G-ITT-DISCIPLINE：每条排除必须有预注册 PAP 引用 + 非空理由；detect 集未知排除需声明。
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
SCHEMA = "queyi-itt/671g"
REGISTRY = Path("data/671g/itt_exclusions.json")
VALID_REASONS = ("detector_unavailable", "measure_class_not_error", "sample_corrupt")


def default_registry() -> dict[str, Any]:
    return {"schema": SCHEMA, "experiments": {}}


def load(root: Path) -> dict[str, Any]:
    p = root / REGISTRY
    if not p.is_file():
        return default_registry()
    d: dict[str, Any] = json.loads(p.read_text(encoding="utf-8"))
    d.setdefault("experiments", {})
    return d


def validate_entry(exp_id: str, entry: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    if not str(entry.get("pap_id", "")).strip():
        out.append({"rule": "G-ITT-DISCIPLINE", "severity": "block", "target": exp_id,
                   "message": "排除集合缺 pap_id（排除必须预注册，不许看结果后剔）"})
    excl = entry.get("exclusions") or []
    ids = [x.get("id") for x in excl]
    if len(ids) != len(set(ids)):
        out.append({"rule": "G-ITT-DISCIPLINE", "severity": "block", "target": exp_id,
                   "message": "排除 id 重复"})
    for x in excl:
        xid = x.get("id", "?")
        if not str(x.get("reason", "")).strip() or x.get("reason") not in VALID_REASONS:
            out.append({"rule": "G-ITT-DISCIPLINE", "severity": "block",
                       "target": f"{exp_id}:{xid}",
                       "message": f"排除理由缺失/非法（{x.get('reason')!r}），允许 {VALID_REASONS}"})
        if not x.get("preregistered", False):
            out.append({"rule": "G-ITT-DISCIPLINE", "severity": "block",
                       "target": f"{exp_id}:{xid}",
                       "message": "preregistered=false：事后排除违反 ITT（必须在 PAP 预注册）"})
    return out


def check(root: Path = ROOT) -> list[dict[str, Any]]:
    reg = load(root)
    out: list[dict[str, Any]] = []
    if not reg["experiments"]:
        return [{"rule": "G-ITT-DISCIPLINE", "severity": "warn", "target": str(REGISTRY),
                "message": "无排除登记 ⇒ 门禁未进射程（有 unknown 排除时必须登记）"}]
    for exp_id, entry in reg["experiments"].items():
        out.extend(validate_entry(exp_id, entry))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g E2：ITT 口径纪律")
    ap.add_argument("--root", default=None)
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else ROOT
    f = check(root)
    if not f:
        print("[itt] PASS")
    for x in f:
        print(f"  [{x['severity']}] {x['target']}: {x['message']}")
    return 1 if any(x["severity"] == "block" for x in f) else 0


if __name__ == "__main__":
    raise SystemExit(main())
