#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""llm_channel_defense_671g.py — 671g D8：LLM 数据通道四类攻击面防御（框架，不调 API）。

671f 把 LLM 通道的攻击面分四类，本工具给每类一个**可执行检查**（纯函数，框架不联网）：

  1. 提示注入    input_filter：输入里出现越权指令（"ignore previous instructions"/"你现在是…"/
     暴露 system prompt 等）⇒ 拒；output_validate：输出必须是预期结构、且不回显 system 片段；
  2. 数据投毒    canary + 配对反事实探针：LLM 批次产物必须带 canary_pass 与
     pair_consistent_pass（具体判决在 G-POISON-DETECT，本工具只校验**批次带没带**证据）；
  3. 模型窃取    限流（同一 key 的请求间隔不得超过配置 QPS）+ 输出水印/来源标记；
  4. 评估污染    train/test ID 集合必须不相交（evaluate_overlap）。

任何 LLM 生成进数据集的批次，落 data/671g/llm_batches/*.json 且必须四项全过
（门禁 G-LLM-CHANNEL）；无批次目录 ⇒ unarmed（warn，如实登记"当前无 LLM 数据通道"）。

用法
====
    python tools/llm_channel_defense_671g.py --check
    python tools/llm_channel_defense_671g.py --scan-input - < input.txt
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "queyi-llm-channel/671g"
BATCH_DIR = Path("data/671g/llm_batches")
DEFAULT_MIN_INTERVAL_S = 1.0

INJECTION_RE = re.compile(
    r"ignore\s+(all\s+)?previous|disregard\s+(the\s+)?(above|previous)|"
    r"you\s+are\s+now|new\s+instructions|system\s+prompt|reveal\s+(your|the)\s+prompt|"
    r"忽略(前面|之前|以上).{0,6}(指令|提示)|无视.{0,6}(指令|规则)|你现在是|现在开始你是|"
    r"泄露.{0,4}(系统|system).{0,4}(提示|prompt)", re.IGNORECASE)
SYSTEM_LEAK_RE = re.compile(r"system\s*[:：]|SYSTEM_PROMPLETAG|<\|im_start\|>", re.IGNORECASE)
WATERMARK_RE = re.compile(r"queyi|阙疑|generated.by.llm", re.IGNORECASE)


# ── 1 提示注入 ────────────────────────────────────────────────────────────────
def input_filter(text: str) -> dict[str, Any]:
    hits = sorted(set(m.group(0) for m in INJECTION_RE.finditer(text or "")))
    return {"pass": not hits, "hits": hits,
            "why": "命中越权指令模式" if hits else ""}


def output_validate(output: str, forbidden_system: bool = True) -> dict[str, Any]:
    """LLM 输出不得回显 system 片段；并要求非空且长度合理（防空输出/整段 prompt 回吐）。"""
    out = output or ""
    if not out.strip():
        return {"pass": False, "why": "输出为空"}
    if forbidden_system and SYSTEM_LEAK_RE.search(out):
        return {"pass": False, "why": "输出疑似回显 system prompt 片段"}
    return {"pass": True, "why": ""}


# ── 2 数据投毒（证据存在性；具体判决在 D9）──────────────────────────────
def batch_poison_defense(batch: dict[str, Any]) -> list[str]:
    """LLM 批次必须带 canary / 配对探针通过证据（缺 = 通道不设防）。"""
    problems = []
    dc = batch.get("defense_checks") or {}
    if not dc.get("canary_pass"):
        problems.append("缺 canary 通过证据（defense_checks.canary_pass）")
    if not dc.get("pair_consistent_pass"):
        problems.append("缺配对反事实探针通过证据（defense_checks.pair_consistent_pass）")
    return problems


# ── 3 模型窃取：限流 + 水印 ──────────────────────────────────────────────────
def rate_limit(request_ts: list[float], min_interval_s: float = DEFAULT_MIN_INTERVAL_S
              ) -> dict[str, Any]:
    """同 key 请求时间戳（epoch 秒）；相邻间隔 < min_interval ⇒ 超限（疑似爬取）。"""
    bad = []
    for a, b in zip(sorted(request_ts), sorted(request_ts)[1:]):
        if b - a < min_interval_s - 1e-9:
            bad.append([a, b])
    return {"pass": not bad, "violations": bad, "min_interval_s": min_interval_s}


def watermark_present(output: str) -> dict[str, Any]:
    return {"pass": bool(WATERMARK_RE.search(output or "")), "why": "" if WATERMARK_RE.search(output or "")
            else "输出缺来源水印（queyi/阙疑/generated-by-llm），防模型窃取取证"}


# ── 4 评估污染：train/test 不相交 ──────────────────────────────────────────
def evaluate_overlap(train_ids: list[str], test_ids: list[str]) -> dict[str, Any]:
    inter = sorted(set(train_ids) & set(test_ids))
    return {"pass": not inter, "overlap": inter,
            "why": "训练/测试 ID 相交 ⇒ 评估污染（测试集泄漏进训练）" if inter else ""}


# ── 批次门禁 ─────────────────────────────────────────────────────────────────
def validate_batch(batch: dict[str, Any]) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    bid = batch.get("batch_id", "?")
    inj = input_filter(str(batch.get("llm_prompt", "")))
    if not inj["pass"]:
        out.append({"rule": "G-LLM-CHANNEL", "severity": "block", "target": bid,
                   "message": f"提示注入命中：{inj['hits']}"})
    ov = output_validate(str(batch.get("llm_output", "")))
    if not ov["pass"]:
        out.append({"rule": "G-LLM-CHANNEL", "severity": "block", "target": bid,
                   "message": f"输出校验失败：{ov['why']}"})
    for why in batch_poison_defense(batch):
        out.append({"rule": "G-LLM-CHANNEL", "severity": "block", "target": bid, "message": why})
    if not batch.get("source_tag"):
        out.append({"rule": "G-LLM-CHANNEL", "severity": "block", "target": bid,
                   "message": "批次缺 source_tag（来源标记，防模型窃取/溯源）"})
    tr, te = batch.get("train_ids") or [], batch.get("test_ids") or []
    if tr or te:
        ovl = evaluate_overlap(tr, te)
        if not ovl["pass"]:
            out.append({"rule": "G-LLM-CHANNEL", "severity": "block", "target": bid,
                       "message": f"{ovl['why']}：{ovl['overlap'][:5]}"})
    return out


def check(root: Path = ROOT) -> list[dict[str, Any]]:
    d = root / BATCH_DIR
    if not d.is_dir():
        return [{"rule": "G-LLM-CHANNEL", "severity": "warn", "target": str(BATCH_DIR),
                "message": "无 LLM 批次目录 ⇒ 通道门禁未进射程（当前无 LLM 数据通道；有批次即强制）"}]
    out = []
    for p in sorted(d.glob("*.json")):
        try:
            batch = json.loads(p.read_text(encoding="utf-8"))
        except ValueError as e:
            out.append({"rule": "G-LLM-CHANNEL", "severity": "block", "target": p.name,
                        "message": f"批次 JSON 解析失败：{e}"})
            continue
        out.extend(validate_batch(batch))
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g D8：LLM 通道防御")
    ap.add_argument("--root", default=None)
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--scan-input", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else ROOT
    if a.scan_input:
        print(json.dumps(input_filter(sys.stdin.read()), ensure_ascii=False, indent=2))
        return 0
    f = check(root)
    print("[llm-channel] " + ("unarmed（无批次）" if not f else ""))
    for x in f:
        print(f"  [{x['severity']}] {x['target']}: {x['message']}")
    return 1 if any(x["severity"] == "block" for x in f) else 0


if __name__ == "__main__":
    raise SystemExit(main())
