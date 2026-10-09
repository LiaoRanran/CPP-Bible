#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""gen_tool_manifest_696.py — 696 批次：扫描 ``tools/*.py`` 生成分类清单。

用途
====
``tools/`` 下有 700+ 个脚本，命名规则多样。本脚本用**文件名启发式**把它们归入
五个功能类，产出一份机器可读清单 ``tools/manifest.json``，回答"哪个功能的脚本在哪一类"。

分类（判据 = **文件名子串/前缀**，按下列顺序**首个命中即归类**）
================================================================
1. ``utils``         —— 共用基础设施（``util`` / ``common`` / ``helper`` /
   ``path_config`` / ``utf8_console`` / ``toolchain`` / ``console`` / ``config``）；
2. ``verification``  —— 门禁与校验（``verify`` / ``gate`` / ``check`` / ``audit`` /
   ``guard`` / ``integrity`` / ``lint`` / ``validate`` / ``consistency`` / ``assert`` /
   ``poison`` / ``drill`` / ``preflight`` / ``prepush`` / ``replay`` / ``invariant`` /
   ``triage`` / ``exempt`` / ``fail_closed``）；
3. ``visualization`` —— 可视化/前端数据（``visual`` / ``plot`` / ``chart`` / ``graph`` /
   ``dashboard`` / ``render`` / ``svg`` / ``figure`` / ``site_`` / ``web_data`` /
   ``mermaid`` / ``star_h2`` / ``html``）；
4. ``batch``         —— 批次一次性脚本（文件名**以 3 位批次号开头**如 ``612_baseline.py``，
   或含 ``batch`` / ``acceptance``）；
5. ``analysis``      —— **兜底桶**：以上都不命中者（研究/实验/统计/生成类脚本）一律归此。

**为什么把 analysis 设为兜底**：本仓 ``tools/`` 的主体就是研究/实验脚本，给它们逐条穷举
关键词只会过拟合命名；而 infra（utils）、门禁（verification）、可视化（visualization）、
批次一次性（batch）四类的**命名信号清晰**，用精确 token 先判，剩余即"分析/实验/其它"。

**这是启发式、不是真理**：它只用于**索引**，不做任何门禁判决（不参与 pass/fail）。
判据若调整，改本文件的 token 元组即可，清单可重生成。

确定性
======
输出前对文件名与分类键**双重排序**；``generated_at`` 是唯一的时间戳字段（非确定性），
其余内容（``count`` / ``categories`` / ``counts``）在给定目录下**逐次一致**，便于单测断言。

用法
====
    python tools/gen_tool_manifest_696.py                 # 写 tools/manifest.json
    python tools/gen_tool_manifest_696.py --out X.json    # 写到指定路径
    python tools/gen_tool_manifest_696.py --stdout        # 打印到 stdout，不落盘
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TOOLS_DIR = ROOT / "tools"
DEFAULT_OUT = DEFAULT_TOOLS_DIR / "manifest.json"

#: 五类分类键（顺序即报告展示顺序）
CATEGORY_ORDER: tuple[str, ...] = (
    "analysis",
    "verification",
    "visualization",
    "utils",
    "batch",
)

#: 判据表：按元组顺序首个命中即归类（最后一类 ``utils`` 同时是兜底）
_UTILS_TOKENS: tuple[str, ...] = (
    "util", "common", "helper", "path_config", "utf8_console",
    "toolchain", "console", "config",
)
_VERIFICATION_TOKENS: tuple[str, ...] = (
    "verify", "gate", "check", "audit", "guard", "integrity", "lint", "validate",
    "consistency", "assert", "poison", "drill", "preflight", "prepush", "replay",
    "invariant", "triage", "exempt", "fail_closed", "failclosed",
)
_VISUALIZATION_TOKENS: tuple[str, ...] = (
    "visual", "plot", "chart", "graph", "dashboard", "render", "svg", "figure",
    "site_", "web_data", "mermaid", "star_h2", "html",
)

#: 批次一次性脚本：文件名以 3 位批次号开头（如 ``612_baseline.py``）
_BATCH_PREFIX_RE = re.compile(r"^\d{3}")
_BATCH_TOKENS: tuple[str, ...] = ("batch", "acceptance")


def classify(filename: str) -> str:
    """按文件名启发式判定分类。

    Args:
        filename: 脚本文件名（含 ``.py`` 亦可，仅取 stem 语义）。

    Returns:
        五个分类键之一（见 :data:`CATEGORY_ORDER`）。
    """
    name = filename.lower()
    stem = name[:-3] if name.endswith(".py") else name

    if any(tok in stem for tok in _UTILS_TOKENS):
        return "utils"
    if any(tok in stem for tok in _VERIFICATION_TOKENS):
        return "verification"
    if any(tok in stem for tok in _VISUALIZATION_TOKENS):
        return "visualization"
    if _BATCH_PREFIX_RE.match(stem) or any(tok in stem for tok in _BATCH_TOKENS):
        return "batch"
    return "analysis"


def scan_tools(tools_dir: Path) -> dict[str, list[str]]:
    """扫描 ``tools_dir/*.py``（**仅顶层**），返回分类 → 排序文件名列表。

    Args:
        tools_dir: 待扫描目录。

    Returns:
        ``{分类键: [文件名...]}``；五个分类键**始终存在**（无成员则为空列表）。
    """
    categories: dict[str, list[str]] = {key: [] for key in CATEGORY_ORDER}
    for path in sorted(tools_dir.glob("*.py")):
        categories[classify(path.name)].append(path.name)
    for key in categories:
        categories[key].sort()
    return categories


def build_manifest(
    tools_dir: Path | None = None,
    generated_at: str | None = None,
) -> dict[str, Any]:
    """构造 manifest 字典（除 ``generated_at`` 外确定性）。

    Args:
        tools_dir: 待扫描目录，默认仓库 ``tools/``。
        generated_at: 覆盖时间戳（测试用）；为 ``None`` 时取当前本地时间。

    Returns:
        含 ``generated_by`` / ``generated_at`` / ``count`` / ``counts`` / ``categories`` 的字典。
    """
    d = tools_dir or DEFAULT_TOOLS_DIR
    categories = scan_tools(d)
    count = sum(len(v) for v in categories.values())
    return {
        "generated_by": "tools/gen_tool_manifest_696.py",
        "generated_at": generated_at or _dt.datetime.now().astimezone().isoformat(timespec="seconds"),
        "count": count,
        "counts": {key: len(categories[key]) for key in CATEGORY_ORDER},
        "categories": categories,
    }


def main(argv: list[str] | None = None) -> int:
    """CLI 入口：生成清单并落盘/打印。"""
    ap = argparse.ArgumentParser(description="扫描 tools/*.py 生成分类清单（696 批次）")
    ap.add_argument("--tools-dir", type=Path, default=None,
                    help="待扫描目录（默认仓库 tools/）")
    ap.add_argument("--out", type=Path, default=None,
                    help=f"输出路径（默认 {DEFAULT_OUT}）")
    ap.add_argument("--stdout", action="store_true",
                    help="只打印 JSON 到 stdout，不写文件")
    args = ap.parse_args(argv)

    manifest = build_manifest(args.tools_dir)
    text = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"

    if args.stdout:
        sys.stdout.write(text)
        return 0

    out = args.out or DEFAULT_OUT
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8", newline="\n")
    counts = manifest["counts"]
    summary = " ".join(f"{k}={counts[k]}" for k in CATEGORY_ORDER)
    print(f"[696-manifest] 已写入 {out}（count={manifest['count']}；{summary}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
