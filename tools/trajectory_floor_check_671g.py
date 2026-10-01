#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""trajectory_floor_check_671g.py — 671g D10：标注质量地板检查（floor-check）。

教训（671f）
==============
8B 评委 400 条标错 397 条：低质量标注会**系统性毁掉**下游一切（训练/评估/论文）。
本工具给每个标注批次一道地板：

  * 每批**随机抽 ≥10 条**（带 seed，可复现）人工复核；
  * 复核错误率 **>20% ⇒ 整批全部重标**（block，不许挑错的重标——错率说明整批不可信）；
  * 0 复核记录 / 样本不足 ⇒ inconclusive（warn，不许放行当合格）。

批次产物格式 data/671g/labels/<batch>.json：
  {batch_id, n_items, labels:[{id, label}], review:{seed, reviewed:[{id, label, truth, error}]}}
review 必须独立（复核真值不来自标注者自己）。

用法
====
    python tools/trajectory_floor_check_671g.py --check
"""
from __future__ import annotations

import argparse
import json
import random
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "queyi-floor-check/671g"
LABEL_DIR = Path("data/671g/labels")
REVIEW_SIZE = 10
ERROR_THRESHOLD = 0.20


def pick_sample(n_items: int, size: int = REVIEW_SIZE, seed: int = 20261001) -> list[int]:
    """确定性随机抽样（seed 可复现）；n<size 时全抽。"""
    rng = random.Random(seed)
    idx = list(range(n_items))
    rng.shuffle(idx)
    return sorted(idx[:min(size, n_items)])


def evaluate(batch: dict[str, Any]) -> dict[str, Any]:
    bid = batch.get("batch_id", "?")
    labels = batch.get("labels") or []
    n = len(labels)
    rev = batch.get("review") or {}
    reviewed = rev.get("reviewed") or []
    if n < REVIEW_SIZE and not reviewed:
        return {"batch_id": bid, "status": "inconclusive", "severity": "warn",
                "error_rate": None, "why": f"批次仅 {n} 条且无复核记录，不足以做地板检查"}
    if not reviewed:
        return {"batch_id": bid, "status": "inconclusive", "severity": "warn",
                "error_rate": None, "why": "缺独立人工复核 review（每批至少抽 10 条）"}
    errs = sum(1 for r in reviewed if bool(r.get("error")))
    k = len(reviewed)
    rate = errs / k if k else 1.0
    status = "block" if rate > ERROR_THRESHOLD + 1e-12 else "pass"
    return {"batch_id": bid, "n_items": n, "reviewed": k, "errors": errs,
            "error_rate": round(rate, 6), "threshold": ERROR_THRESHOLD,
            "action": "整批全部重标" if status == "block" else "通过地板",
            "status": status, "severity": status}


def check(root: Path = ROOT) -> list[dict[str, Any]]:
    d = root / LABEL_DIR
    if not d.is_dir():
        return [{"rule": "G-TRAJECTORY-FLOOR", "severity": "warn", "target": str(LABEL_DIR),
                "message": "无标注批次目录 ⇒ 地板检查未进射程（有 LLM/人工标注批次时必须建）"}]
    out: list[dict[str, Any]] = []
    for p in sorted(d.glob("*.json")):
        try:
            batch = json.loads(p.read_text(encoding="utf-8"))
        except ValueError as e:
            out.append({"rule": "G-TRAJECTORY-FLOOR", "severity": "block", "target": p.name,
                        "message": f"批次 JSON 解析失败：{e}"})
            continue
        r = evaluate(batch)
        if r["status"] in ("block", "warn"):
            out.append({"rule": "G-TRAJECTORY-FLOOR", "severity": r["severity"],
                       "target": f"{p.name}::{bid(r)}", "message": r["why"] if r["status"] == "warn"
                       else f"复核错误率 {r['error_rate']} > {ERROR_THRESHOLD} ⇒ {r['action']}"})
    return out


def bid(r: dict[str, Any]) -> str:
    return str(r.get("batch_id", "?"))


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g D10：标注地板检查")
    ap.add_argument("--root", default=None)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--n", type=int, default=50)
    ap.add_argument("--seed", type=int, default=20261001)
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else ROOT
    if a.n and not a.check:
        print(json.dumps({"sample_index": pick_sample(a.n, REVIEW_SIZE, a.seed)}, indent=2))
        return 0
    f = check(root)
    print("[floor] " + ("无批次（unarmed）" if not f else ""))
    for x in f:
        print(f"  [{x['severity']}] {x['target']}: {x['message']}")
    return 1 if any(x["severity"] == "block" for x in f) else 0


if __name__ == "__main__":
    raise SystemExit(main())
