#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
collect_reports.py — 门禁/审计报告归集器（T4）。

设计原则（安全优先，不改动任何门禁 writer，避免动 CI）：
  - 仅"读取 + 拷贝"散落在 仓库根 / tools/ / build/ 的各 JSON 报告，
    汇聚到 build/reports/，并生成 build/reports/INDEX.json 清单。
  - 不删除源文件；源文件若被 git 跟踪则保持跟踪，拷贝是只读副本。
  - build/ 已被 .gitignore 忽略，归集副本不会污染 git 树。
  - 不归集"配置/输入"类文件（compile_exempt.json、asm_drift_baseline.json、
    baselines/ 等），它们不是产物。

用法：
  python3 tools/collect_reports.py [--root ROOT] [--out build/reports]
"""

from __future__ import annotations
from typing import Any

import argparse
import json
import os
import shutil
import sys
import glob

# 显式列举的门禁/审计产物（相对 root）
EXPLICIT_SOURCES = [
    "tools/compile_report.json",
    "tools/exempt_audit_report.json",
    "tools/last_report.json",
    "tools/last_v4_report.json",
    "tools/learning_path.json",
    "tools/module_report_gcc15.json",
    "tools/reverify_result.json",
    "tools/v4_ranking.json",
    "tools/_prepush_asm_report.json",
    "tools/audit_cpp_defects.json",
    "tools/audit_py_tools.json",
    "tools/ci_baseline.json",
    "build/markdown_style_report.json",
    "build/asm_evidence_report.json",
    "build/asm_repro_spotcheck.json",
    "build/chapter_lint.json",
    "build/d5_appendix_audit.json",
    "build/d5_gap_report.json",
    "build/s10_audit.json",
]

# 目录 glob 补充（捕获动态命名产物）
GLOB_SOURCES = [
    "build/*_report.json",
    "build/*_audit.json",
    "build/exercise_theme*.json",
    "build/*_digest.txt",
]


def collect(root: str, out: str):
    root_abs = os.path.abspath(root)
    out_abs = os.path.abspath(out)
    os.makedirs(out_abs, exist_ok=True)

    candidates = []
    seen = set()
    for rel in EXPLICIT_SOURCES:
        p = os.path.join(root_abs, rel)
        if os.path.isfile(p):
            candidates.append((rel, p))
            seen.add(os.path.normpath(p))
    for pat in GLOB_SOURCES:
        for p in sorted(glob.glob(os.path.join(root_abs, pat))):
            np = os.path.normpath(p)
            if np in seen:
                continue
            seen.add(np)
            candidates.append((os.path.relpath(p, root_abs), p))

    index: dict[str, Any] = {"tool": "collect_reports", "out": out_abs, "reports": {}}
    copied = 0
    for rel, p in candidates:
        dest = os.path.join(out_abs, os.path.basename(p))
        try:
            shutil.copy2(p, dest)
            st = os.stat(p)
            index["reports"][os.path.basename(p)] = {
                "src": rel,
                "size": st.st_size,
                "mtime": st.st_mtime,
            }
            copied += 1
        except Exception as e:
            print(f"  ! 拷贝失败 {rel}: {e}", file=sys.stderr)

    index_path = os.path.join(out_abs, "INDEX.json")
    with open(index_path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(index, fh, ensure_ascii=False, indent=2)

    print(f"归集源: {len(candidates)} 个文件")
    print(f"成功拷贝: {copied} 个 -> {out_abs}")
    print(f"清单: {index_path}")
    return 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--out", default="build/reports")
    args = ap.parse_args()
    return collect(args.root, args.out)


if __name__ == "__main__":
    sys.exit(main())
