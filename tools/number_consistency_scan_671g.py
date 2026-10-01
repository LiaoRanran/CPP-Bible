#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""number_consistency_scan_671g.py — 671g B1：率三元组（pct%（k/n））的全仓一致性扫描。

它抓什么 / 不抓什么（口径先讲清）
====================================
抓两类**真不一致**：
  1. **算术不自洽**：文中写 ``pct%（k/n）``，但 ``100*k/n`` 算出的率与 pct 对不上
     （容差按 pct 的小数位自适应，默认 0.15pp）——这是手抄错数字的典型形态；
  2. **同一 (k,n) 两处报不同率**：完全相同的分母分子在不同文件里被写成不同百分比
     ——同一事实两个值，必有一个错。

**刻意不抓**：盲测冻结值 87.5%(14/16) vs 扩样累计 81.0%(17/21) 这类——
(k,n) 不同就是**不同口径**，不是不一致（671g A 台账 D-01 已登记两者并列）。

扫描范围（红线隔离）
====================
* 纳入：docs/*.md（顶层当前文档）、docs/discipline/**、data/ 顶层 *报告/核查*.md、
  tools/*.py、tests/*671g*.py、data/experiments/*.json（三臂等派生产物）；
* 排除（不判红）：research/**（论文批次）、web/**（671d 在改，只单独列出）、
  _arch_*/**（架构笔记）、Book/**、data/holdout/**、data/external_corpus/**（671a 原始样本）、
  data/*baseline* / data/*acceptance_report*（历史批次冻结留痕）。

用法
====
    python tools/number_consistency_scan_671g.py            # 打印不一致清单（exit 1=有）
    python tools/number_consistency_scan_671g.py --json
    python tools/number_consistency_scan_671g.py --check     # 0 不一致才 exit 0
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "queyi-number-consistency/671g"
TOL_PP = 0.15                       # 算术容差（百分点）

#: 87.5%（14/16） / 87.5% (14/16) / 87.5% （14 / 16）
CITE_RE = re.compile(r"(\d+(?:\.\d+)?)\s*%\s*[（(]\s*(\d+)\s*/\s*(\d+)(?!\d)")
CODE_RE = re.compile(r"```.*?```", re.DOTALL)

#: 纳入扫描的 glob（相对仓库根）
INCLUDE_GLOBS = ("docs/*.md", "docs/discipline/**/*.md", "data/*核查*.md", "data/*报告*.md",
                 "tools/*_671g.py", "data/experiments/*.json")
#: 测试文件**不参与**：红路径夹具里故意写错误率（如 80%（14/16）），是测试输入不是产物声明；
#: 测试由 tests/test_number_consistency_671g.py 在 tmp 仓里验证扫描器的红/绿路径。
#: 命中也排除（历史/冻结/他人在改）
EXCLUDE_PARTS = ("research", "web", "_arch_", "Book", "Examples",
                  "data/holdout", "data/external_corpus")
EXCLUDE_NAME = ("baseline", "acceptance_report", "_665.", "_669.", "_670.", "_671.")
#: 扫描器/门禁自身的注释里含"错误示例"（如 80%（14/16）），是说明材料不是断言 ⇒ 自排除
SELF_EXCLUDE = {"tools/number_consistency_scan_671g.py", "tools/gate_rules_671g.py"}


def _in_scope(p: Path, root: Path = ROOT) -> bool:
    try:
        rel = p.relative_to(root).as_posix()
    except ValueError:
        return False
    if rel in SELF_EXCLUDE:
        return False
    # 671i E/G：原 `parts = set(rel.split("/"))` 为死赋值，已移除（行为不变）。
    # 但下一行用 `x in rel`（子串匹配）而非 `x in parts`(按路径段匹配)——疑为笔误，
    # 二者语义不同（例如 "build" 会误中 "rebuild"）；是否改为按段匹配待人工裁定。
    if any(x in rel for x in EXCLUDE_PARTS):
        return False
    name = p.name
    if any(tok in name for tok in ("baseline", "acceptance_report")):
        return False
    # 历史批次产物（数字随批次演进，属冻结留痕）——只排除 data/ 下的，不排 tools 671g
    if rel.startswith("data/") and re.search(r"_(6[0-6]\d|670|671)[a-z]?\.", name):
        return False
    return True


def iter_files(root: Path) -> list[Path]:
    files: set[Path] = set()
    for g in INCLUDE_GLOBS:
        files.update(p for p in root.glob(g) if p.is_file())
    return sorted(p for p in files if _in_scope(p, root))


def citations_in(text: str) -> list[tuple[str, float, int, int]]:
    """去掉代码块 + 豁免标记行后抽率三元组。

    豁免：行内含 ``671g:scan-ignore``（门禁清单/射程报告等**描述红路径示例**的元文档用）。
    """
    kept = []
    in_fence = False
    for line in text.splitlines():
        if line.strip().startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence or "671g:scan-ignore" in line:
            continue
        kept.append(line)
    return [(m.group(1), float(m.group(1)), int(m.group(2)), int(m.group(3)))
            for m in CITE_RE.finditer("\n".join(kept))]


def scan(root: Path = ROOT) -> dict[str, Any]:
    arithmetic: list[dict[str, Any]] = []
    sites: dict[tuple[int, int], list[dict[str, Any]]] = {}
    scanned = 0
    for p in iter_files(root):
        try:
            text = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        cits = citations_in(text)
        if not cits:
            continue
        scanned += 1
        rel = p.relative_to(root).as_posix()
        for raw_pct, pct, k, n in cits:
            sites.setdefault((k, n), []).append({"file": rel, "pct": pct})
            if n <= 0 or k > n:
                arithmetic.append({"file": rel, "pct": pct, "k": k, "n": n,
                                "expected": None,
                                "why": f"非法分母/分子：k={k} n={n}"})
                continue
            exp = round(100.0 * k / n, 4)
            # 与文中 pct 的**书写精度**对齐后再比（87.5 容 0.15，整数 87/88 容 0.6）
            decimals = len(raw_pct.split(".", 1)[1]) if "." in raw_pct else 0
            tol = TOL_PP if decimals >= 1 else 0.6
            if abs(exp - pct) > tol + 1e-9:
                arithmetic.append({"file": rel, "pct": pct, "k": k, "n": n,
                                "expected_pct": exp,
                                "why": f"{pct}% ≠ {k}/{n} 现算 {exp}%（容差 {tol}pp）"})
    conflicting: list[dict[str, Any]] = []
    for (k, n), rows in sites.items():
        pcts = sorted({r["pct"] for r in rows})
        # 同一 (k,n) 的不同书写精度（87.5 vs 87.50）不算冲突；差 >容差才算
        distinct = [pcts[0]]
        for p in pcts[1:]:
            if all(abs(p - q) > TOL_PP for q in distinct):
                distinct.append(p)
        if len(distinct) > 1:
            conflicting.append({"k": k, "n": n, "pcts": distinct, "sites": rows,
                              "why": f"同一 (k,n)=({k},{n}) 被写成不同率 {distinct}"})
    return {
        "schema": SCHEMA,
        "scanned_files": scanned,
        "arithmetic_inconsistencies": arithmetic,
        "conflicting_calibers": conflicting,
        "inconsistency_count": len(arithmetic) + len(conflicting),
        "note": "只判率三元组内部算术自洽 + 同(k,n)同率；不同(k,n)属不同口径，不判",
    }


def render(rep: dict[str, Any]) -> str:
    L = [f"[671g number consistency] 扫描文件={rep['scanned_files']} "
         f"不一致={rep['inconsistency_count']}"]
    for r in rep["arithmetic_inconsistencies"]:
        L.append(f"  [ARITH] {r['file']}: {r['why']}")
    for r in rep["conflicting_calibers"]:
        L.append(f"  [CONFLICT (k,n)=({r['k']},{r['n']})] {r['pcts']}")
        for s in r["sites"][:8]:
            L.append(f"      {s['file']}: {s['pct']}%")
    return "\n".join(L)


# ─────────────────────────────────────────────────────────────────────────────────────
# B3：G-DENOMINATOR-COMPLETE —— 结果率必须带分母（k/n）+ 口径
# ─────────────────────────────────────────────────────────────────────────────────────

#: 句中出现这些词且带百分比，视为"结果率声明"，必须带 k/n
RATE_KEYWORD_RE = re.compile(r"(检出率|检测率|逃逸率|击杀率|kill[ _]?rate|误报率|重注入)")
BARE_PCT_RE = re.compile(r"(\d+(?:\.\d+)?)\s*%")
KN_RE = re.compile(r"\d+\s*/\s*\d+")
#: 这些语境的百分比不是结果率（区间端点/阈值/效应量/历史值显式标注），豁免
SKIP_CTX = re.compile(r"CP\s?95|CI\b|置信|区间|阈值|阈值|阈值|pp\b|百分点|效应量|power|阈值|显著性|p\s*=|历史值|冻结|口径变")
CALIBER_RE = re.compile(r"口径|可测|全样本|盲|cumulative|blind|分母|k\s*/\s*n|catch\+miss|denominator")
DENOM_GLOBS = ("docs/discipline/**/*.md", "data/671g_*.md", "docs/671g_工程反哺总结.md")


def check_denominator_complete(root: Path = ROOT) -> list[dict[str, Any]]:
    """G-DENOMINATOR-COMPLETE：结果率声明必须**同行**带 (k/n) 或显式口径锚点。

    刻意只扫**新纪律文档 + 671g 产物**（历史批次文档已在各自批次声明分母，且属冻结留痕；
    论文/web 由各自批次门禁守）。三臂 baseline JSON 的率块另做结构化分母校验。
    """
    findings: list[dict[str, Any]] = []
    files: set[Path] = set()
    for g in DENOM_GLOBS:
        files.update(p for p in root.glob(g) if p.is_file())
    for p in sorted(files):
        rel = p.relative_to(root).as_posix()
        raw = p.read_text(encoding="utf-8", errors="replace").splitlines()
        # 跳过 ``` 代码块（里面的率是测试/命令样例，不是文档断言）
        lines: list[str] = []
        in_fence = False
        for line in raw:
            if line.strip().startswith("```"):
                in_fence = not in_fence
                continue
            if not in_fence:
                lines.append(line)
        for i, line in enumerate(lines, 1):
            if not RATE_KEYWORD_RE.search(line):
                continue
            for m in BARE_PCT_RE.finditer(line):
                ctx = line[max(0, m.start() - 24):m.end() + 24]
                if SKIP_CTX.search(ctx):
                    continue
                # 形如 <5% / ≤5% / ≥10% 是阈值，不是结果率
                before = line[:m.start()].rstrip()
                if before and before[-1] in "<≤≥>":
                    continue
                if KN_RE.search(line) or CALIBER_RE.search(line):
                    continue
                findings.append({"rule": "G-DENOMINATOR-COMPLETE", "severity": "block",
                               "target": f"{rel}:{i}",
                               "message": f"结果率「{m.group(0)}」缺分母(k/n)或口径声明：…{line.strip()[:90]}…",
                               "fix_hint": "在同行补 (k/n) 与口径（可测/全样本/盲测累计）+ CP95"})
    # baseline 三臂 JSON：measurable 率块必须有 numerator + denominator（结构化分母校验）
    for arm in ("fd", "static", "random"):
        p = root / "data" / "experiments" / f"baseline_{arm}.json"
        if not p.is_file():
            continue
        d = json.loads(p.read_text(encoding="utf-8"))
        for name in ("holdout", "corpus"):
            meas = (d.get(name) or {}).get("measurable") or {}
            if not isinstance(meas, dict):
                continue
            if meas.get("point") is not None and (
                    meas.get("numerator", meas.get("k")) is None
                    or meas.get("denominator", meas.get("n")) is None):
                findings.append({"rule": "G-DENOMINATOR-COMPLETE", "severity": "block",
                             "target": f"{p.relative_to(root).as_posix()}::{name}.measurable",
                             "message": "率有点估计但缺 numerator/denominator", "fix_hint": "补 k/n"})
    return findings


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g B1：率三元组全仓一致性扫描")
    ap.add_argument("--root", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else ROOT
    rep = scan(root)
    print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json else render(rep))
    return 1 if rep["inconsistency_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
