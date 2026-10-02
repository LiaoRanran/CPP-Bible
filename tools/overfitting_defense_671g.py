#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""overfitting_defense_671g.py — 671g E3：评估过拟合防御（训练/验证/测试三分离 + 调参登记 + 多重检验校正）。

金融回测教训
============
量化策略在历史数据上反复调参 ⇒ 回测漂亮、未来失效（backtest overfitting）。规则工程
同形：在测试集上反复改规则直到检出率好看 ⇒ 数字是"挑出来的"。三道防线：

  1. **三分离**：train / validation / test 三个 id 集合两两不相交（测试集只用于最终评估一次）；
  2. **调参登记**：每条规则的每次参数调整必须登记 tuning_set（只能 train/validation，禁 test）；
  3. **多重检验校正**：同一数据集做 m 次假设检验必须控制 FWER（Holm）或 FDR（BH），
     不许只挑显著的那条报。

登记 data/671g/eval_split.json：{train_ids,validation_ids,test_ids, rule_tuning:[{rule,set}]}
门禁 G-NO-OVERFITTING：三集合不相交；调参集合不能是 test。
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "queyi-overfitting/671g"
CONFIG = Path("data/671g/eval_split.json")
TUNING_SETS = ("train", "validation")


def holm(pvals: list[float], alpha: float = 0.05) -> list[int]:
    """Holm 逐步降权：返回校正后仍拒绝 H0 的原始下标列表（FWER 控制）。"""
    order = sorted(range(len(pvals)), key=lambda i: pvals[i])
    m = len(pvals)
    rejected: list[int] = []
    for rank, idx in enumerate(order):
        threshold = alpha / (m - rank)
        if pvals[idx] <= threshold:
            rejected.append(idx)
        else:
            break                 # Holm：第一个不拒绝就停
    return rejected


def benjamini_hochberg(pvals: list[float], alpha: float = 0.05) -> list[int]:
    """BH：控制 FDR，返回拒绝下标。"""
    m = len(pvals)
    order = sorted(range(m), key=lambda i: pvals[i])
    rejected: list[int] = []
    k = 0
    for rank, idx in enumerate(order, start=1):
        if pvals[idx] <= alpha * rank / m:
            k = rank
    for rank, idx in enumerate(order[:k], start=1):
        rejected.append(idx)
    return rejected


def default_config() -> dict[str, Any]:
    return {"schema": SCHEMA, "train_ids": [], "validation_ids": [], "test_ids": [],
            "rule_tuning": [],
            "note": "671g 现状：holdout/corpus 为 reveal 盲测集（测试），调参/新规则孵化在 atoms/draft 与 669d 扩样前的训练资产；三集合映射待论文批次细化"}


def load(root: Path) -> dict[str, Any]:
    p = root / CONFIG
    if not p.is_file():
        return default_config()
    d: dict[str, Any] = json.loads(p.read_text(encoding="utf-8"))
    for k in ("train_ids", "validation_ids", "test_ids", "rule_tuning"):
        d.setdefault(k, [])
    return d


def check_split(cfg: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    tr, va, te = (set(cfg.get(x, [])) for x in ("train_ids", "validation_ids", "test_ids"))
    for a, b, na, nb in ((tr, va, "train", "validation"), (tr, te, "train", "test"),
                           (va, te, "validation", "test")):
        inter = a & b
        if inter:
            out.append({"rule": "G-NO-OVERFITTING", "severity": "block",
                       "target": f"{na}∩{nb}", "message": f"集合相交 {sorted(inter)[:5]}（评估污染）"})
    for t in cfg.get("rule_tuning", []):
        if t.get("set") not in TUNING_SETS:
            out.append({"rule": "G-NO-OVERFITTING", "severity": "block",
                       "target": f"tuning:{t.get('rule', '?')}",
                       "message": f"调参集合={t.get('set')!r}，只允许 {TUNING_SETS}（禁在 test 上改规则）"})
    return out


def check(root: Path = ROOT) -> list[dict[str, Any]]:
    cfg = load(root)
    if not (cfg["train_ids"] or cfg["validation_ids"] or cfg["test_ids"]):
        return [{"rule": "G-NO-OVERFITTING", "severity": "warn", "target": str(CONFIG),
                "message": "三集合都为空 ⇒ 未进射程（框架就位，待论文批次映射 id 集合）"}]
    return check_split(cfg)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g E3：评估过拟合防御")
    ap.add_argument("--root", default=None)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--holm", default=None, help="逗号分隔 p 值，演示 Holm 校正")
    ap.add_argument("--bh", default=None, help="逗号分隔 p 值，演示 BH 校正")
    a = ap.parse_args(argv)
    if a.holm:
        p = [float(x) for x in a.holm.split(",")]
        print(json.dumps({"method": "holm", "rejected_index": holm(p)}))
        return 0
    if a.bh:
        p = [float(x) for x in a.bh.split(",")]
        print(json.dumps({"method": "BH", "rejected_index": benjamini_hochberg(p)}))
        return 0
    root = Path(a.root).resolve() if a.root else ROOT
    f = check(root)
    print("[overfitting] " + ("unarmed（三集合未映射）" if f and f[0]["severity"] == "warn" else
          ("PASS" if not f else "")))
    for x in f:
        print(f"  [{x['severity']}] {x['target']}: {x['message']}")
    return 1 if any(x["severity"] == "block" for x in f) else 0


if __name__ == "__main__":
    raise SystemExit(main())
