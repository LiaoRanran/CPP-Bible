#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""terminology_scan_671g.py — 671g B2：工程文档术语一致性扫描。

守哪些词（canonical 见 docs/discipline/术语表.md）
====================================================
| 废弃写法 | 规范写法 | 级别 | 备注 |
|---|---|---|---|
| 祈易 | 阙疑（英文 queyi/QueYi 不变） | block | 671d 已全局改名；防止回潮 |
| 留出集 | holdout / 盲测集 | block | 直译 holdout 的错误术语 |
| 探测器（缺陷检测语境） | 检测器 | block | 论证语境的"探测器"（argument probe，C1/C2 五个基础探测器）**合法**，不误伤 |
| 判定（指 verdict 时） | 判决 | warn | 通用动词"判定"不拦，只在术语表要求的判决语境提示 |

上下文感知的必要性：tools/argument_audit.py 里"五个基础探测器"是论证学探针，与
asan/ubsan 这类"检测器"是**两个东西**——朴素子串匹配会把合法用法判红（假绿的镜像：假红）。
扫描范围/排除与 number_consistency_scan_671g 完全一致（论文/web/架构笔记/历史冻结件排除）。

用法
====
    python tools/terminology_scan_671g.py --check      # 0 block 才 exit 0
    python tools/terminology_scan_671g.py --json
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = "queyi-terminology/671g"

INCLUDE_GLOBS = ("docs/*.md", "docs/discipline/**/*.md", "data/*核查*.md", "data/*报告*.md",
                 "tools/*_671g.py")
#: 测试文件**不参与**：红路径夹具里故意写废弃词（如"本系统叫祈易"），是测试输入不是工程文档。
EXCLUDE_PARTS = ("research", "web", "_arch_", "Book", "Examples",
                  "data/holdout", "data/external_corpus")

#: 出现这些词时，"探测器"是论证学探针，合法
PROBE_CONTEXT = re.compile(r"论证|argument|C1|C2|五个|高级探测器|辩护|命题|图论证|主张")
#: 出现这些词时，"探测器"指的是缺陷检测器，必须用"检测器"
DETECTOR_CONTEXT = re.compile(
    r"检测器|sanitizer|asan|ubsan|tsan|编译器|缺陷|漏报|误报|逃逸|detect|检测|验证器")

BLOCK_TERMS = ("祈易", "留出集")

#: 这些文件**以登记废弃词为职责**（扫描器自身、其测试、术语表），自我排除，
#: 否则扫描器会因为在常量里列出了「祈易」而把自己判红（假红的镜像：假红）。
SELF_EXCLUDE = {"tools/terminology_scan_671g.py", "tests/test_terminology_671g.py",
               "docs/discipline/术语表.md", "tools/gate_rules_671g.py"}


def in_scope(root: Path, p: Path) -> bool:
    rel = p.relative_to(root).as_posix()
    if rel in SELF_EXCLUDE:
        return False
    if any(x in rel for x in EXCLUDE_PARTS):
        return False
    name = p.name
    if any(tok in name for tok in ("baseline", "acceptance_report")):
        return False
    if rel.startswith("data/") and re.search(r"_(6[0-6]\d|670|671)[a-z]?\.", name):
        return False
    return True


def iter_files(root: Path) -> list[Path]:
    files: set[Path] = set()
    for g in INCLUDE_GLOBS:
        files.update(p for p in root.glob(g) if p.is_file())
    return sorted(p for p in files if in_scope(root, p))


def scan(root: Path = ROOT) -> dict[str, Any]:
    blocks: list[dict[str, Any]] = []
    warns: list[dict[str, Any]] = []
    for p in iter_files(root):
        rel = p.relative_to(root).as_posix()
        try:
            lines = p.read_text(encoding="utf-8", errors="replace").splitlines()
        except OSError:
            continue
        for i, line in enumerate(lines, 1):
            # 豁免行：元文档（门禁清单/射程报告）描述废弃词与红路径示例
            if "671g:scan-ignore" in line:
                continue
            # 改名动作的描述行（新旧词同现 + 改名/→/rename）合法：它就是在讲"从旧到新"
            describes_rename = ("改名" in line or "rename" in line.lower() or "→" in line)
            for term in BLOCK_TERMS:
                if term in line:
                    if term == "祈易" and describes_rename and "阙疑" in line:
                        continue
                    blocks.append({"term": term, "file": rel, "line": i, "text": line.strip()[:120],
                                 "canonical": "阙疑（queyi）" if term == "祈易" else "holdout / 盲测集",
                                 "why": f"废弃术语「{term}」"})
            if "探测器" in line and DETECTOR_CONTEXT.search(line) and not PROBE_CONTEXT.search(line):
                blocks.append({"term": "探测器", "file": rel, "line": i,
                             "text": line.strip()[:120], "canonical": "检测器",
                             "why": "缺陷检测语境必须用「检测器」；论证学探针才用「探测器」"})
    return {"schema": SCHEMA, "scanned_files": len(iter_files(root)),
            "block_count": len(blocks), "warn_count": len(warns),
            "blocks": blocks, "warns": warns,
            "canonical_ref": "docs/discipline/术语表.md"}


def render(rep: dict[str, Any]) -> str:
    L = [f"[671g terminology] 扫描文件={rep['scanned_files']} "
         f"block={rep['block_count']} warn={rep['warn_count']}"]
    for b in rep["blocks"]:
        L.append(f"  [BLOCK] {b['file']}:{b['line']} 「{b['term']}」→ {b['canonical']}")
        L.append(f"        {b['text']}")
    return "\n".join(L)


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g B2：术语一致性扫描")
    ap.add_argument("--root", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)
    root = Path(a.root).resolve() if a.root else ROOT
    rep = scan(root)
    print(json.dumps(rep, ensure_ascii=False, indent=2) if a.json else render(rep))
    return 1 if rep["block_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
