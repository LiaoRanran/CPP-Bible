#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""pap_register_671g.py — 671g D4：PAP（Pre-Analysis Plan）预注册门禁。

为什么（671f #102）
=====================
"先看结果再定分析方案" 是评估过拟合的总入口：看到 87.5% 好看就只报盲测口径、看到 p 值不显著
就换分母。PAP 要求**跑实验之前**把 14 项钉死：

  research_question / hypothesis / sample_size / statistical_method / alpha / exclusion_criteria /
  variable_definitions / analysis_pipeline / expected_results / data_source / code_version /
  rules_version / environment / registered_at

* 每个实验批次先注册 PAP 再跑（门禁 G-PAP-REGISTERED：被列入 require 清单的实验必须有有效 PAP）；
* 已完成实验允许**事后补注册**，但必须 ``registration_type="posthoc"`` + posthoc_note
  ——事后 PAP 不享受"预注册"的可信度，显式标记，不许冒充；
* PAP 与实验结果分离存放（data/671g/pap/），补注册不得回填"预期结果"去贴结果。

用法
====
    python tools/pap_register_671g.py --check                    # 校验全部 PAP + require 覆盖
    python tools/pap_register_671g.py --new BATCH --scaffold   # 生成 14 字段模板
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "queyi-pap/671g"
PAP_DIR = Path("data/671g/pap")
REGISTRY = Path("data/671g/pap/registry.json")

#: PAP 必填 14 字段（缺一不可）
REQUIRED_FIELDS = (
    "research_question", "hypothesis", "sample_size", "statistical_method", "alpha",
    "exclusion_criteria", "variable_definitions", "analysis_pipeline", "expected_results",
    "data_source", "code_version", "rules_version", "environment", "registered_at",
)
REGISTRATION_TYPES = ("preregistered", "posthoc")


def scaffold(batch: str) -> dict[str, Any]:
    return {"schema": SCHEMA, "batch_id": batch, "registration_type": "preregistered",
            "experiment_start": "", **{f: "" for f in REQUIRED_FIELDS},
            "posthoc_note": ""}


def validate(pap: dict[str, Any]) -> list[str]:
    """返回问题清单；空 = PAP 有效。字段缺失/空都算无效（fail-loud）。"""
    problems = []
    rt = pap.get("registration_type")
    if rt not in REGISTRATION_TYPES:
        problems.append(f"registration_type 必须是 {REGISTRATION_TYPES}（实际 {rt!r}）")
    for f in REQUIRED_FIELDS:
        v = pap.get(f)
        if v is None or (isinstance(v, str) and not v.strip()) or v == [] or v == {}:
            problems.append(f"缺字段或为空：{f}")
    # alpha：假设检验必须 (0,1) 数值；纯描述/只报区间的批次可显式声明"不适用"（不许留空，fail-loud）
    a = pap.get("alpha")
    if isinstance(a, str) and (a.strip() == "不适用" or a.strip().startswith("不适用")):
        meth = str(pap.get("statistical_method", ""))
        if not any(w in meth for w in ("CP", "Clopper", "区间", "描述", "不适用")):
            problems.append("alpha=不适用 要求统计方法为纯描述/区间（出现假设检验必须给数值 alpha）")
    else:
        if isinstance(a, str):
            try:
                a = float(a.rstrip("%"))
            except ValueError:
                a = None
        if not isinstance(a, (int, float)) or not (0.0 < float(a) < 1.0):
            problems.append("alpha 必须是 (0,1) 内数值，或显式写「不适用」（纯描述/区间批次）")
    if rt == "posthoc" and not str(pap.get("posthoc_note", "")).strip():
        problems.append("事后补注册必须写 posthoc_note（为什么事后、与结果是否互相影响）")
    # 时间顺序：预注册必须在实验开始之前
    if rt == "preregistered" and str(pap.get("experiment_start", "")).strip():
        if str(pap.get("registered_at", "")) > str(pap.get("experiment_start")):
            problems.append("预注册时间晚于实验开始时间（预注册必须先于跑实验）")
    return problems


def load_registry(root: Path) -> dict[str, Any]:
    p = root / REGISTRY
    if not p.is_file():
        return {"require": [], "pap_files": {}}
    d: dict[str, Any] = json.loads(p.read_text(encoding="utf-8"))
    d.setdefault("require", [])
    d.setdefault("pap_files", {})
    return d


def check(root: Path = ROOT) -> list[dict[str, Any]]:
    """G-PAP-REGISTERED：require 清单里每个实验必须有有效 PAP；所有 PAP 必须自身有效。"""
    out: list[dict[str, Any]] = []
    reg = load_registry(root)
    pap_dir = root / PAP_DIR
    pap_files = sorted(pap_dir.glob("*.json")) if pap_dir.is_dir() else []
    pap_by_batch: dict[str, dict[str, Any]] = {}
    for p in pap_files:
        if p.name == "registry.json":
            continue
        try:
            pap = json.loads(p.read_text(encoding="utf-8"))
        except ValueError as e:
            out.append({"rule": "G-PAP-REGISTERED", "severity": "block", "target": p.name,
                       "message": f"PAP JSON 解析失败：{e}"})
            continue
        probs = validate(pap)
        bid = str(pap.get("batch_id", p.stem))
        pap_by_batch[bid] = pap
        for prob in probs:
            out.append({"rule": "G-PAP-REGISTERED", "severity": "block",
                       "target": f"{p.name}::{bid}", "message": prob})
    # 显式映射优先；也允许映射值是 pap 文件名（pap_<bid>.json）或 batch_id
    mapping = reg.get("pap_files", {})
    for exp in reg.get("require", []):
        bid = mapping.get(exp, exp)
        if bid in pap_by_batch:
            continue
        if (pap_dir / f"pap_{bid}.json").is_file():
            continue
        out.append({"rule": "G-PAP-REGISTERED", "severity": "block", "target": exp,
                    "message": f"实验 {exp} 在 require 清单但无对应 PAP（{bid}）",
                    "fix_hint": "先 --new 注册，再跑实验"})
    return out


def write_scaffold(root: Path, batch: str) -> Path:
    p = root / PAP_DIR / f"pap_{batch}.json"
    p.parent.mkdir(parents=True, exist_ok=True)
    pap = scaffold(batch)
    pap["registered_at"] = time.strftime("%Y-%m-%d")
    p.write_text(json.dumps(pap, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return p


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g D4：PAP 预注册")
    ap.add_argument("--root", default=None)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--new", default=None)
    ap.add_argument("--posthoc", action="store_true")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else ROOT
    if a.new:
        p = write_scaffold(root, a.new)
        if a.posthoc:
            d = json.loads(p.read_text(encoding="utf-8"))
            d["registration_type"] = "posthoc"
            d["posthoc_note"] = "事后补注册：实验已完成，本 PAP 只冻结既有方案（不享受预注册可信度）"
            p.write_text(json.dumps(d, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"[pap] 已生成模板 {p.relative_to(root)}（{'事后补注册' if a.posthoc else '预注册'}）")
        return 0
    f = check(root)
    if a.json:
        print(json.dumps(f, ensure_ascii=False, indent=2))
    elif not f:
        print("[pap] PASS（require 清单实验均有有效 PAP）")
    for x in f:
        print(f"  [BLOCK] {x['target']}: {x['message']}")
    return 1 if f else 0


if __name__ == "__main__":
    raise SystemExit(main())
