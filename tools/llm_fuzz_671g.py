#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""llm_fuzz_671g.py — 671g D5：LLM 自动生成验证夹具的三姿势框架（不实际调用 LLM API）。

为什么是"框架"（671f #135）
==============================
实际 LLM 调用需要 API key 与外部网络，本批**不接 API**，只把三姿势的**协议/数据流/判定**钉死，
让任何接 LLM 的实现都必须走同一结构（便于 G-LLM-CHANNEL 与 G-POISON-DETECT 拦在数据入口）。

三姿势
========
* 姿势1（缺陷发现）：LLM 生成 C++ 代码 → **sanitizer 当 oracle**（不是 LLM 自己标！）
  → 标签来自 asan/ubsan/tsan 的 -O0/-O2 双档运行；
* 姿势2（变异杀死）：LLM 生成变异体 → 验证器检测 → killed/survived，并入变异杀死率；
* 姿势3（反事实）：LLM 生成反事实 case → 验证器判决 → **人工标注真值**（LLM 不产真值）。

共同纪律：LLM 只提供**待判材料**；真值来自 oracle/人工。LLM 输出必须过 G-LLM-CHANNEL
（输入过滤/输出校验）与 G-POISON-DETECT（canary/配对探针）才能进数据集。

用法
====
    python tools/llm_fuzz_671g.py --posture 1 --code-file x.cpp --sanitizer asan
    （无 --runner 时只做框架演练，不编译不联网）
"""
from __future__ import annotations

import argparse
import json
import time
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "queyi-llm-fuzz/671g"
POSTURES = (1, 2, 3)

#: 一个 runner：(code_text, sanitizer) -> {oracle_hit:bool, rc:int, output:str}；None=未接仪器
CodeRunner = Callable[[str, str], dict[str, Any]]
Verifier = Callable[[dict[str, Any]], str]       # case -> verdict(catch/miss/...)


def posture1_code_to_label(code: str, sanitizer: str, runner: CodeRunner | None) -> dict[str, Any]:
    """姿势1：LLM 代码 → sanitizer oracle → 缺陷标签。runner=None ⇒ 未接仪器，不臆标。"""
    if sanitizer not in ("asan", "ubsan", "tsan"):
        return {"posture": 1, "status": "rejected", "why": f"未知 sanitizer：{sanitizer}"}
    if runner is None:
        return {"posture": 1, "sanitizer": sanitizer, "oracle": "not_attached",
                "label": None, "status": "framework_only",
                "why": "未接 sanitizer runner（本批不调 LLM/不编译）；标签必须来自 oracle，禁止 LLM 自标"}
    r = runner(code, sanitizer)
    hit = bool(r.get("oracle_hit"))
    return {"posture": 1, "sanitizer": sanitizer, "oracle": "attached",
            "label": "defect" if hit else "clean", "rc": r.get("rc"),
            "status": "labeled", "evidence": str(r.get("output", ""))[:300]}


def posture2_mutant_kill(case: dict[str, Any], verify: Verifier | None) -> dict[str, Any]:
    """姿势2：LLM 变异体 → 验证器 → killed/survived。"""
    if not case.get("mutant_code"):
        return {"posture": 2, "status": "rejected", "why": "缺 mutant_code"}
    if verify is None:
        return {"posture": 2, "verifier": "not_attached", "status": "framework_only",
                "verdict": None, "why": "未接验证器；不得臆造 killed/survived"}
    v = verify(case)
    return {"posture": 2, "verdict": v, "status": "labeled",
            "killed": v == "catch", "mutation_op": case.get("mutation_op")}


def posture3_counterfactual(case: dict[str, Any], verify: Verifier | None,
                          human_label: str | None = None) -> dict[str, Any]:
    """姿势3：LLM 反事实 case → 验证器判决 → 人工真值。无人工标签 ⇒ 不得入数据集。"""
    if not case.get("fake_citation"):
        return {"posture": 3, "status": "rejected", "why": "反事实 case 必须含 fake_citation"}
    verdict = verify(case) if verify is not None else None
    if human_label is None:
        return {"posture": 3, "verdict": verdict, "human_truth": None,
                "status": "quarantined",
                "why": "无人工真值 ⇒ 隔离，不得进数据集（LLM 不产真值）"}
    if human_label not in ("original_holds", "original_falls"):
        return {"posture": 3, "status": "rejected", "why": f"非法人工标签：{human_label}"}
    return {"posture": 3, "verdict": verdict, "human_truth": human_label,
            "status": "labeled", "agree": (verdict is not None)}


def run_batch(posture: int, items: list[dict[str, Any]], *, runner: CodeRunner | None = None,
              verify: Verifier | None = None) -> dict[str, Any]:
    """一批 LLM 材料走同一姿势；产出机读批次（G-LLM-CHANNEL/POISON 在入库前再拦一道）。"""
    fn = {1: lambda c: posture1_code_to_label(c.get("code", ""), c.get("sanitizer", "asan"), runner),
          2: lambda c: posture2_mutant_kill(c, verify),
          3: lambda c: posture3_counterfactual(c, verify, c.get("human_truth"))}[posture]
    rows = [fn(c) for c in items]
    return {"schema": SCHEMA, "posture": posture, "generated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
            "llm_attached": False, "note": "本批不接 LLM API；items 视为 LLM 已产出的材料",
            "n": len(rows), "rows": rows,
            "quarantined": sum(1 for r in rows if r.get("status") in ("quarantined", "framework_only", "rejected"))}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g D5：LLM fuzz 三姿势框架")
    ap.add_argument("--posture", type=int, choices=POSTURES, required=True)
    ap.add_argument("--code-file", default=None)
    ap.add_argument("--sanitizer", default="asan")
    ap.add_argument("--items", default=None, help="JSON 文件：[{...}, ...]")
    a = ap.parse_args(argv)
    if a.items:
        items = json.loads(Path(a.items).read_text(encoding="utf-8"))
        print(json.dumps(run_batch(a.posture, items), ensure_ascii=False, indent=2))
        return 0
    code = Path(a.code_file).read_text(encoding="utf-8") if a.code_file else "// no code"
    res = {1: posture1_code_to_label(code, a.sanitizer, None),
           2: posture2_mutant_kill({"mutant_code": code}, None),
           3: posture3_counterfactual({"fake_citation": {}}, None)}[a.posture]
    print(json.dumps(res, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
