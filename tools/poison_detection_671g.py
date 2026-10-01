#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""poison_detection_671g.py — 671g D9：小样本投毒检测（canary + 配对反事实探针）。

两道独立探针（671f 深化）
==========================
1. **Canary（金丝雀样本）**：在数据集中预先埋入**真值已知、判决稳定**的样本（本批用
   reveal 明细里已 3 轮复现的稳定样本作 canary，**不新增/不改原始样本**）。
   canary 被错判 ⇒ 数据集或判据可能被投毒/被改动 ⇒ block。
2. **配对反事实探针**：一对只有微小差异、按机制**应当同判**的样本（如同为 asan SEGV 的
   h22/h23、同为 double-free 的 h27/h32）。配对判决不一致 ⇒ 判据不稳定/被污染 ⇒ block。

配置 data/671g/poison_canaries.json：
  {canaries:[{id, expected_verdict, detector}], pairs:[{a,b}]}
判决从 671a reveal 明细**只读**取（data/holdout/reveal_3_detail_671a.json），
不碰 data/holdout/ 原始样本。门禁 G-POISON-DETECT。

用法
====
    python tools/poison_detection_671g.py --check
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "queyi-poison/671g"
CONFIG = Path("data/671g/poison_canaries.json")
DETAIL = Path("data/holdout/reveal_3_detail_671a.json")


def default_config() -> dict[str, Any]:
    """canary/配对都选自 reveal 明细里 3 轮复现、机制明确的稳定样本（只读，不新增样本）。"""
    return {"schema": SCHEMA,
            "canaries": [
                {"id": "h21", "expected_verdict": "catch", "detector": "ubsan",
                 "why": "有符号溢出，ubsan 3 轮 catch（CP 明确）"},
                {"id": "h24", "expected_verdict": "catch", "detector": "ubsan",
                 "why": "除零，ubsan 3 轮 catch"},
                {"id": "h26", "expected_verdict": "catch", "detector": "asan",
                 "why": "heap-use-after-free，asan catch"},
                {"id": "h32", "expected_verdict": "catch", "detector": "asan",
                 "why": "double-free（新样本，3 轮稳定）"},
                {"id": "h33", "expected_verdict": "miss", "detector": "ubsan",
                 "why": "strict-alias，ubsan 两档不报（稳定 miss，双向 canary）"}],
            "pairs": [
                {"a": "h22", "b": "h23", "expect": "same",
                 "why": "同为 asan SEGV 空指针解引用"},
                {"a": "h27", "b": "h32", "expect": "same",
                 "why": "同为 asan double-free"},
                {"a": "h25", "b": "h30", "expect": "same",
                 "why": "同为 asan 内存类命中（mismatch / leak）⇒ catch/catch"},
            ]}


def load_config(root: Path) -> dict[str, Any]:
    p = root / CONFIG
    if not p.is_file():
        return default_config()
    d = json.loads(p.read_text(encoding="utf-8"))
    return {**default_config(), **d}


def verdict_index(detail: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(r.get("id")): r for r in detail.get("per_sample", [])}


def check_canaries(cfg: dict[str, Any], rows: dict[str, dict[str, Any]]
                ) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for c in cfg.get("canaries", []):
        cid = str(c["id"])
        row = rows.get(cid)
        if row is None:
            out.append({"kind": "canary_missing", "id": cid, "severity": "block",
                       "message": f"canary {cid} 在判决明细中缺失"})
            continue
        v = row.get("verdict")
        if v != c["expected_verdict"]:
            out.append({"kind": "canary_flipped", "id": cid, "severity": "block",
                       "message": f"canary {cid} 期望 {c['expected_verdict']} 实测 {v}（疑似投毒/判据被改）"})
        det = c.get("detector")
        if det and row.get("detector") != det:
            out.append({"kind": "canary_detector_changed", "id": cid, "severity": "warn",
                       "message": f"canary {cid} 检测器 {row.get('detector')} ≠ 登记 {det}"})
    return out


def check_pairs(cfg: dict[str, Any], rows: dict[str, dict[str, Any]]
               ) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for pr in cfg.get("pairs", []):
        a, b = rows.get(str(pr["a"])), rows.get(str(pr["b"]))
        if a is None or b is None:
            out.append({"kind": "pair_missing", "id": f"{pr['a']}/{pr['b']}", "severity": "block",
                       "message": f"配对样本缺失：{pr['a']}={a is not None} {pr['b']}={b is not None}"})
            continue
        if pr.get("expect", "same") == "same" and a.get("verdict") != b.get("verdict"):
            out.append({"kind": "pair_inconsistent", "id": f"{pr['a']}/{pr['b']}",
                       "severity": "block",
                       "message": f"配对探针不一致：{pr['a']}={a.get('verdict')} "
                                  f"{pr['b']}={b.get('verdict')}（{pr.get('why', '')}）"})
    return out


def evaluate(root: Path = ROOT, cfg: dict[str, Any] | None = None,
           detail: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = cfg or load_config(root)
    detail = detail if detail is not None else json.loads(
        (root / DETAIL).read_text(encoding="utf-8")) if (root / DETAIL).is_file() else {}
    rows = verdict_index(detail)
    if not rows:
        return {"schema": SCHEMA, "status": "unarmed", "severity": "warn",
                "findings": [], "why": f"判决明细缺失：{DETAIL}"}
    findings = check_canaries(cfg, rows) + check_pairs(cfg, rows)
    status = "block" if any(f["severity"] == "block" for f in findings) else "pass"
    return {"schema": SCHEMA, "status": status, "severity": status,
            "n_canaries": len(cfg.get("canaries", [])), "n_pairs": len(cfg.get("pairs", [])),
            "findings": findings}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g D9：投毒检测（canary + 配对探针）")
    ap.add_argument("--root", default=None)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else ROOT
    rep = evaluate(root)
    print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json
          else f"[poison] {rep['status']} canary={rep.get('n_canaries')} pairs={rep.get('n_pairs')}"
                + "\n" + "\n".join(f"  [{x['severity']}] {x['kind']} {x['id']}: {x['message']}"
                                     for x in rep.get("findings", [])))
    return 1 if rep.get("status") == "block" else 0


if __name__ == "__main__":
    raise SystemExit(main())
