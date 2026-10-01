#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""gate_rules_670g.py — 670g B2：六条 P0 门禁（**论文/ baseline 维度强化版**）。

⚠ 与 `tools/gate_rules_669d.py` 的关系：669d 已有**同名**六条（产物↔前端一致性那一层）。
本文件**不重复**那层，而是把同一批判据**强化到"论文 ↔ 产物 ↔ baseline"这一层**——
因为 670g 新增了 baseline 三臂与 v0.8，**最容易出错的地方从"产物↔前端"移到了"论文↔产物"**。

六条规则（670g 强化版）
======================
  G-RATE-CONSISTENCY  论文里的率必须与 `data/experiments/baseline_*.json` 现算值一致
  G-DENOMINATOR       论文里每个百分比必须同时给出 `k/n`（禁止只给 %）
  G-STATS-FROZEN      统计口径必须引用 `research/669d_统计口径.md`，禁止自造
  G-BOUNDARY-REQUIRED 实卡缺 semantic scope 时必须**显式登记** gap（不许静默）
  G-BASELINE-EXISTS   论文出现"优于/显著高于"时必须存在 baseline 产物
  G-IRR               标注类结论必须有 IRR 记录，或**显式登记**缺口

设计约定（与 669d 一致）
========================
* `check_*(root: Path) -> list[dict]`；Finding = `{rule, severity, target, message, fix_hint}`。
* severity ∈ {block, warn}；纯标准库。
* 每条规则可被 `tmp_path` 正/反例测试。

用法：
    python tools/gate_rules_670g.py --check
    python tools/gate_rules_670g.py --rule G-DENOMINATOR --json
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

PAPER = "research/paper_v0.9.md"
TEX = "research/latex/queyi_neurips2027.tex"
CALIBER_DOC = "research/669d_统计口径.md"
ABLATION_CALIBER_DOC = "research/671b_统计口径_ablation.md"
BASELINE_DIR = "data/experiments"


def finding(rule: str, severity: str, target: str, message: str, fix_hint: str = "") -> dict:
    return {"rule": rule, "severity": severity, "target": target, "message": message, "fix_hint": fix_hint}


def _read(root: Path, rel: str) -> str:
    p = root / rel
    return p.read_text(encoding="utf-8") if p.is_file() else ""


def _load_json(root: Path, rel: str) -> Any | None:
    p = root / rel
    if not p.is_file():
        return None
    try:
        return json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        return None


# ── G-RATE-CONSISTENCY（论文 ↔ baseline 产物）────────────────────────
def check_rate_consistency(root: Path) -> list[dict]:
    out = []
    paper = _read(root, PAPER)
    fd = _load_json(root, f"{BASELINE_DIR}/baseline_fd.json")
    st = _load_json(root, f"{BASELINE_DIR}/baseline_static.json")
    if not paper:
        return [finding("G-RATE-CONSISTENCY", "warn", PAPER, "论文不存在，跳过")]
    if fd is None or st is None:
        return [finding("G-RATE-CONSISTENCY", "warn", BASELINE_DIR,
                        "baseline 产物缺失（670a 未跑？）", "跑 tools/baseline_670a.py --run")]
    # 论文必须出现三臂的关键 k/n 组合（671a 扩样后：holdout 21 可测 / corpus 48 可测）
    for need in ("17/21", "1/21", "7/48", "26/48"):
        if need not in paper:
            out.append(finding("G-RATE-CONSISTENCY", "block", PAPER,
                               f"论文未出现关键计数 {need}（baseline 三臂）",
                               "从 data/experiments/baseline_*.json 现算填入"))
    return out


# ── G-DENOMINATOR（率必须带 k/n）─────────────────────────────────────
PCT_RE = re.compile(r"(\d+(?:\.\d+)?)\s*%")


CODE_FENCE_RE = re.compile(r"```.*?```", re.S)
# 这些语境里的百分比不是"检出率"，无需 k/n
SKIP_CTX = ("CP", "CI", "置信", "95%", "半宽", "目标", "阈值", "≥", "≤", "上限",
            "→", "pp", "口径", "置信度", "置信水平", "percentile")


def check_denominator(root: Path) -> list[dict]:
    paper = _read(root, PAPER)
    if not paper:
        return [finding("G-DENOMINATOR", "warn", PAPER, "论文不存在，跳过")]
    body = CODE_FENCE_RE.sub("", paper)   # 代码块里的数字（复现命令注释）不算
    out = []
    for m in PCT_RE.finditer(body):
        tail = body[m.end():m.end() + 30]
        if re.match(r"\s*[（(]?\d+\s*/\s*\d+", tail):     # 紧跟 (k/n)
            continue
        ctx = body[max(0, m.start() - 30):m.end() + 6].replace("\n", " ")
        if any(w in ctx for w in SKIP_CTX):
            continue
        out.append(finding("G-DENOMINATOR", "warn", PAPER,
                           f"百分比 {m.group(0)} 未紧随 k/n：…{ctx}…",
                           "补 (k/n) 或说明其为阈值/效应量"))
    return out


# ── G-STATS-FROZEN（引用冻结口径）────────────────────────────────────
def check_stats_frozen(root: Path) -> list[dict]:
    paper = _read(root, PAPER)
    if not paper:
        return [finding("G-STATS-FROZEN", "warn", PAPER, "论文不存在，跳过")]
    if not (root / CALIBER_DOC).is_file():
        return [finding("G-STATS-FROZEN", "warn", CALIBER_DOC, "冻结口径文件缺失")]
    if "669d_统计口径" not in paper and "Clopper" not in paper:
        return [finding("G-STATS-FROZEN", "block", PAPER,
                        "论文未引用冻结统计口径（既无 669d_统计口径 也无 Clopper-Pearson）",
                        "引用 research/669d_统计口径.md 或写明 CP 口径")]
    return []


# ── G-BOUNDARY-REQUIRED（缺口必须显式登记）───────────────────────────
def check_boundary_required(root: Path) -> list[dict]:
    paper = _read(root, PAPER)
    if not paper:
        return [finding("G-BOUNDARY-REQUIRED", "warn", PAPER, "论文不存在，跳过")]
    if "0/26" not in paper:
        return [finding("G-BOUNDARY-REQUIRED", "block", PAPER,
                        "论文未登记 semantic scope 完整度缺口（0/26）",
                        "显式写出 scope 回填缺口，不许静默")]
    return []


# ── G-BASELINE-EXISTS（claim 优于 ⇒ 必须有 baseline）─────────────────
SUPERIOR_WORDS = ("优于", "显著高于", "显著优于", "better than", "outperforms")


def check_baseline_exists(root: Path) -> list[dict]:
    paper = _read(root, PAPER)
    if not paper:
        return [finding("G-BASELINE-EXISTS", "warn", PAPER, "论文不存在，跳过")]
    has_claim = any(w in paper for w in SUPERIOR_WORDS)
    if not has_claim:
        return []
    if not any((root / BASELINE_DIR / f).is_file()
               for f in ("baseline_fd.json", "baseline_static.json", "baseline_random.json")):
        return [finding("G-BASELINE-EXISTS", "block", PAPER,
                        "论文主张'优于/显著高于'但无 baseline 产物",
                        "先跑 tools/baseline_670a.py --run")]
    return []


# ── G-IRR（标注一致性：有则查，无则登记）────────────────────────────
def check_irr(root: Path) -> list[dict]:
    paper = _read(root, PAPER)
    if not paper:
        return [finding("G-IRR", "warn", PAPER, "论文不存在，跳过")]
    has_gap_note = ("IRR" in paper) or ("κ" in paper) or ("标注" in paper and "缺口" in paper)
    if not has_gap_note:
        return [finding("G-IRR", "warn", PAPER,
                        "未见 IRR / 标注一致性登记",
                        "补 IRR 结果，或显式登记'第二标注者 0 人'的缺口")]
    return []


# ── G-ABLATION-CONSISTENCY（论文 ablation 主张 ↔ ablation 计划产物）──
ABLATION_PLAN = "data/experiments/ablation_plan_671b.json"
ABLATION_RESULT_KEYS = ("detection_rate", "recall", "result", "delta", "verdict")  # 禁止的"实验结果"键


def check_ablation_consistency(root: Path) -> list[dict]:
    """论文里的 A0--A5 必须与 ablation 计划产物一致，且**不得出现编造的实验结果**。"""
    out: list[dict] = []
    paper = _read(root, PAPER)
    plan = _load_json(root, ABLATION_PLAN)
    if not paper:
        return [finding("G-ABLATION-CONSISTENCY", "warn", PAPER, "论文不存在，跳过")]
    if plan is None:
        return [finding("G-ABLATION-CONSISTENCY", "block", ABLATION_PLAN,
                        "论文写了 ablation 框架但无计划产物",
                        "先跑 tools/ablation_671b.py --dry-run")]
    # 论文必须出现关键对照字面量
    if "A0 - A5" not in paper.replace("−", "-"):
        out.append(finding("G-ABLATION-CONSISTENCY", "block", PAPER,
                           "论文未出现关键对照 A0 - A5",
                           "在 §6.2/§7.6 明确写出 A0 - A5 的证伪条件"))
    # ablation 计划里不得有实验结果字段（本批只写设计，不跑实验）
    text = json.dumps(plan, ensure_ascii=False)
    for key in ("\"p_value\"", "\"ci_low\"", "\"ci_high\""):
        if key in text:
            out.append(finding("G-ABLATION-CONSISTENCY", "block", ABLATION_PLAN,
                               f"ablation 计划含实验结果字段 {key}（本批不得跑实验）",
                               "把结果清空为 {{TODO_ablation_*}} 占位"))
    # 计划里必须有占位符
    if "{{TODO_ablation_A0}}" not in text:
        out.append(finding("G-ABLATION-CONSISTENCY", "warn", ABLATION_PLAN,
                           "ablation 计划缺少 {{TODO_ablation_A0}} 占位",
                           "为每组登记 result_placeholder"))
    return out


RULES: list[tuple[str, Any]] = [
    ("G-RATE-CONSISTENCY", check_rate_consistency),
    ("G-DENOMINATOR", check_denominator),
    ("G-STATS-FROZEN", check_stats_frozen),
    ("G-BOUNDARY-REQUIRED", check_boundary_required),
    ("G-BASELINE-EXISTS", check_baseline_exists),
    ("G-IRR", check_irr),
    ("G-ABLATION-CONSISTENCY", check_ablation_consistency),
]


def run_all(root: Path) -> list[dict]:
    out: list[dict] = []
    for _name, fn in RULES:
        out.extend(fn(root))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description="670g 六条 P0 门禁（论文/baseline 维度）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--rule", default=None)
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    root = Path(__file__).resolve().parent.parent

    if args.rule:
        fn = dict(RULES).get(args.rule)
        if not fn:
            print(f"未知规则：{args.rule}", file=sys.stderr)
            return 2
        findings = fn(root)
    else:
        findings = run_all(root)

    blocks = [f for f in findings if f["severity"] == "block"]
    if args.json:
        print(json.dumps({"findings": findings, "blocks": len(blocks)}, ensure_ascii=False, indent=2))
    else:
        print(f"[gate-670g] findings={len(findings)}  block={len(blocks)}")
        for f in findings:
            print(f"  [{f['severity'].upper()}] {f['rule']}: {f['message']}")
        print("[gate-670g] " + ("PASS" if not blocks else "FAIL"))
    return 0 if not blocks else 1


if __name__ == "__main__":
    sys.exit(main())
