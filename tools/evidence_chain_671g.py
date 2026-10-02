#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""evidence_chain_671g.py — 671g E4：证据保管链 / 毒树之果（数据污染溯源）。

法学隐喻
========
证据法要求每份呈堂证据有**来源链**（chain of custody）；非法取得的证据派生的一切都是
"毒树之果"（fruit of the poisonous tree），必须排除。本工具对**派生产物**做同样的事：

  * 每个派生产物登记 parents：直接来源文件列表 + 登记时的 sha256；
  * 校验：parents 必须存在、当前哈希必须等于登记哈希（来源被改而产物没重跑 ⇒ 断链）；
  * 传播：任一 parent（递归向上）被标记 poisoned ⇒ 该产物标记 **poisoned_fruit**，
    不得用于结论；
  * 登记册 data/671g/evidence_chain.json，门禁 G-EVIDENCE-CHAIN。

用法
====
    python tools/evidence_chain_671g.py --check
    python tools/evidence_chain_671g.py --add data/x.json --parent data/y.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "queyi-evidence-chain/671g"
REGISTRY = Path("data/671g/evidence_chain.json")


def sha256_file(root: Path, rel: str) -> str | None:
    p = root / rel
    if not p.is_file():
        return None
    return hashlib.sha256(p.read_bytes()).hexdigest()


def default_registry() -> dict[str, Any]:
    return {"schema": SCHEMA, "artifacts": {}, "poisoned": []}


def load_registry(root: Path) -> dict[str, Any]:
    p = root / REGISTRY
    if not p.is_file():
        return default_registry()
    d: dict[str, Any] = json.loads(p.read_text(encoding="utf-8"))
    d.setdefault("artifacts", {})
    d.setdefault("poisoned", [])
    return d


def add_artifact(root: Path, artifact: str, parents: list[str]) -> dict[str, Any]:
    reg = load_registry(root)
    reg["artifacts"][artifact] = {
        "parents": [{"path": q, "sha256": sha256_file(root, q)} for q in parents],
        "self_sha256": sha256_file(root, artifact)}
    save(root, reg)
    entry: dict[str, Any] = reg["artifacts"][artifact]
    return entry


def save(root: Path, reg: dict[str, Any]) -> None:
    p = root / REGISTRY
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(reg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def ancestors_of(artifact: str, reg: dict[str, Any]) -> set[str]:
    out: set[str] = set()
    stack = [artifact]
    while stack:
        cur = stack.pop()
        for par in (reg["artifacts"].get(cur) or {}).get("parents", []):
            q = par["path"]
            if q not in out:
                out.add(q)
                stack.append(q)
    return out


def check(root: Path = ROOT) -> list[dict[str, Any]]:
    reg = load_registry(root)
    out: list[dict[str, Any]] = []
    poisoned = set(reg.get("poisoned", []))
    for art, spec in reg["artifacts"].items():
        if not (root / art).is_file():
            out.append({"rule": "G-EVIDENCE-CHAIN", "severity": "block", "target": art,
                       "message": "登记的派生产物自身缺失"})
            # 仍继续查 parents（可能同时缺失）
        cur_self = sha256_file(root, art)
        if spec.get("self_sha256") and cur_self != spec["self_sha256"]:
            out.append({"rule": "G-EVIDENCE-CHAIN", "severity": "warn", "target": art,
                       "message": "产物已更新但链未刷新（跑 --add 重登记）"})
        for par in spec.get("parents", []):
            q = par["path"]
            h = sha256_file(root, q)
            if h is None:
                out.append({"rule": "G-EVIDENCE-CHAIN", "severity": "block", "target": f"{art}←{q}",
                           "message": "来源文件缺失，证据链断裂"})
            elif par.get("sha256") and h != par["sha256"]:
                out.append({"rule": "G-EVIDENCE-CHAIN", "severity": "block", "target": f"{art}←{q}",
                           "message": "来源哈希变了而产物未重跑（来源被改/污染）"})
        if poisoned & ancestors_of(art, reg):
            out.append({"rule": "G-EVIDENCE-CHAIN", "severity": "block", "target": art,
                       "message": f"上游含毒 {sorted(poisoned & ancestors_of(art, reg))} ⇒ 毒树之果，不得用于结论"})
    # 被标毒的来源必须存在登记（悬空标记也要显形）
    for q in poisoned:
        if q not in reg["artifacts"] and not (root / q).is_file():
            out.append({"rule": "G-EVIDENCE-CHAIN", "severity": "warn", "target": q,
                       "message": "poisoned 标记指向不存在的文件"})
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g E4：证据保管链/毒树之果")
    ap.add_argument("--root", default=None)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--add", default=None)
    ap.add_argument("--parent", action="append", default=[])
    ap.add_argument("--mark-poison", default=None)
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else ROOT
    if a.add:
        print(json.dumps(add_artifact(root, a.add, a.parent), ensure_ascii=False, indent=2))
        return 0
    if a.mark_poison:
        reg = load_registry(root)
        if a.mark_poison not in reg["poisoned"]:
            reg["poisoned"].append(a.mark_poison)
        save(root, reg)
        print(f"已标记 {a.mark_poison} 为污染来源")
        return 0
    f = check(root)
    if not f:
        print("[evidence-chain] PASS（登记产物链完整、无毒树之果）")
    for x in f:
        print(f"  [{x['severity']}] {x['target']}: {x['message']}")
    return 1 if any(x["severity"] == "block" for x in f) else 0


if __name__ == "__main__":
    raise SystemExit(main())
