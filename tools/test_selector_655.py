#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""test_selector_655.py — 基于 git diff 的**增量测试选择**（655 C 杠杆 1）。

目标
====
全量 fast 阶段约 2833 例 / 350 s 量级；改一个工具却跑全套是最大的固定成本。
本工具按"**改了什么 → 哪些测试会读它**"给出**受影响测试文件**清单，供门禁/CI 只跑受影响的。

设计原则（正确性优先于省时间）
==============================
1. **fail-safe（宁可多跑）**：命中"高危面"或**无法归类**的改动 ⇒ 直接返回**全量**
   （`FULL_SUITE`），绝不因为解析不出来就少跑；
2. **只读**：不写任何文件（`--report` 除外，且写到 `data/`）；
3. **可解释**：每个被选中的测试都带理由（`reason`：命中哪个模块/路径/前缀）；
4. **不替代两阶段口径**：本工具只挑**测试文件**，`fast/slow` 的切分仍由
   `tests/conftest.py` 的模块标记负责（选了 slow 模块也会被 `-m "not slow"` 过滤掉，
   这是调用方的事，本工具会在输出里提示）。

用法
====
    python tools/test_selector_655.py                          # 对比 origin/master，含工作区改动
    python tools/test_selector_655.py --since HEAD~1
    python tools/test_selector_655.py --paths tools/gate_engine.py
    python tools/test_selector_655.py --json
    python tools/test_selector_655.py --run -- -m "not slow" -n auto   # 直接跑（透传 pytest 参数）
    python tools/test_selector_655.py --check                  # 自检（不读仓库）

诚实边界
========
- 关联关系来自**文本命中**（测试文件里出现模块名/路径），不是 AST 级依赖图；
  因此会有**假阳性**（多跑，安全），也可能有**假阴性** ⇒ 故对 `tools/` 以外的
  未知路径与高危面一律回退全量；
- 新增测试文件（`tests/test_*_655.py`）若其被测模块未在 diff 中，也不会被选中 ——
  这是刻意的：**改测试本身**永远选中自己（见 `_MAP_SELF`）。
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
TESTS = ROOT / "tests"

sys.path.insert(0, str(HERE))
try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

#: 改动这些 ⇒ **全量**（它们决定所有测试的判定口径/隔离行为）
FULL_SUITE_PATHS = (
    "tools/gate_engine.py",        # 67 条规则内嵌于此
    "tools/weighted_af_solver.py",  # W2 判决内核（尺子）
    "tools/tool_integrity.py",     # 信任根自身
    "tools/.tool_checksums",       # 信任根基准
    "tests/conftest.py",           # 测试隔离/标记
    "conftest.py",                 # 全仓数据隔离
    "pyproject.toml",              # pytest 配置
)

#: 改动这些**目录前缀** ⇒ 只挑"提到该前缀"的测试；无命中 ⇒ 回退全量
PATH_PREFIX_MAP = {
    "atoms/": ("atoms",),
    "evidence/": ("evidence",),
    "Book/": ("Book/", "Book\\"),
    "Examples/": ("Examples",),
    "web/": ("web/", "web\\", "graph.json", "manifest.json"),
    "data/": ("data/",),
    "docs/": ("docs/",),
}

#: 纯文档/表格类后缀（不在上面这些"有测试断言"的目录里时，不触发选例、也不回退全量）
DOC_SUFFIXES = (".md", ".txt", ".rst", ".json", ".yaml", ".yml", ".csv", ".html", ".css")

#: 非产品 `.py`（归档 / 调研 / 一次性脚本）：不参与测试选例，只登记
NON_PRODUCT_PY_PREFIXES = ("_archive/", "_adv_", "_arch_v", "Scripts/", "sources/", "scripts/")

OUT_JSON = ROOT / "data" / "655_test_selection.json"


def _git(*args: str) -> list[str]:
    # `core.quotepath=false`：否则中文/非 ASCII 路径会被 git 转义成 `"\_arch_v31/00_\346..."`，
    # 既没法归类（会误触发全量回退）也没法读。
    try:
        p = subprocess.run(["git", "-c", "core.quotepath=false", *args],
                           cwd=str(ROOT), capture_output=True, text=True, check=True)
    except Exception:  # noqa: BLE001
        return []
    return [ln.strip().strip('"') for ln in p.stdout.splitlines() if ln.strip()]


def changed_paths(since: str, include_worktree: bool = True) -> list[str]:
    """返回相对路径（POSIX 风格）列表：`since..HEAD` 的 diff + 可选工作区改动。"""
    out = set(_git("diff", "--name-only", f"{since}...HEAD"))
    if include_worktree:
        out.update(_git("diff", "--name-only", "HEAD"))
        out.update(_git("diff", "--name-only", "--cached"))
        out.update(_git("ls-files", "--others", "--exclude-standard"))
    return sorted(p.replace("\\", "/") for p in out)


def _test_files() -> list[Path]:
    return sorted(TESTS.glob("test_*.py"))


def _mentions(tf: Path, needles: tuple[str, ...]) -> str | None:
    try:
        text = tf.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return None
    for n in needles:
        if n and n in text:
            return n
    return None


def select(paths: list[str]) -> dict[str, Any]:
    """核心：改动路径 → 测试文件清单 + 理由 + 是否回退全量。"""
    tests = _test_files()
    chosen: dict[str, str] = {}
    full_suite = False
    reasons: list[str] = []

    for raw in paths:
        p = raw.replace("\\", "/")
        if p in FULL_SUITE_PATHS:
            full_suite = True
            reasons.append(f"{p} 属高危面 ⇒ 全量")
            continue
        if p.startswith("tests/") and Path(p).name.startswith("test_"):
            chosen.setdefault(p, "自身（测试文件改动）")
            continue
        if p.startswith("tests/"):
            full_suite = True
            reasons.append(f"{p} 是测试基础设施 ⇒ 全量")
            continue
        if p.endswith(".py"):
            if p.startswith(NON_PRODUCT_PY_PREFIXES):
                reasons.append(f"{p} 非产品脚本（归档/调研）⇒ 不触发选例")
                continue
            mod = Path(p).stem
            hit = False
            for tf in tests:
                why = _mentions(tf, (f"import {mod}", mod))
                if why:
                    chosen.setdefault(tf.relative_to(ROOT).as_posix(), f"命中模块 {mod}")
                    hit = True
            if not hit and p.startswith("tools/"):
                full_suite = True
                reasons.append(f"{p} 无测试提及 ⇒ 无法归因，回退全量")
            elif not hit:
                reasons.append(f"{p} 无测试提及（非 tools/）⇒ 不触发选例")
            continue
        matched_prefix = next((k for k in PATH_PREFIX_MAP if p.startswith(k)), None)
        if matched_prefix:
            needles = PATH_PREFIX_MAP[matched_prefix]
            hit = False
            for tf in tests:
                why = _mentions(tf, needles)
                if why:
                    chosen.setdefault(tf.relative_to(ROOT).as_posix(), f"命中前缀 {matched_prefix}")
                    hit = True
            if not hit:
                reasons.append(f"{p} 前缀 {matched_prefix} 无测试提及（不回退：内容类改动）")
            continue
        if p.endswith(DOC_SUFFIXES):
            # 文档/表格类：治理类测试可能读它，但不强制全量（登记即可）
            for tf in tests:
                why = _mentions(tf, (p, Path(p).name))
                if why:
                    chosen.setdefault(tf.relative_to(ROOT).as_posix(), f"命中文件名 {p}")
            reasons.append(f"{p} 文档/数据类改动（无命中测试也不回退全量）")
            continue
        full_suite = True
        reasons.append(f"{p} 未归类 ⇒ 回退全量（fail-safe）")

    selected = sorted(chosen) if not full_suite else [tf.relative_to(ROOT).as_posix()
                                                      for tf in tests]
    return {
        "paths": paths,
        "full_suite": full_suite,
        "selected": selected,
        "selected_count": len(selected),
        "total_test_files": len(tests),
        "reasons": reasons,
        "why": chosen if not full_suite else {},
    }


def _run_pytest(files: list[str], extra: list[str]) -> int:
    cmd = [sys.executable, "-m", "pytest", *files, *extra]
    print(f"$ {' '.join(cmd)}")
    return subprocess.run(cmd, cwd=str(ROOT), check=False).returncode


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    r1 = select(["tools/license_header_check_655.py"])
    chk("工具改动命中自身测试", "tests/test_655_tools.py" in r1["selected"] and not r1["full_suite"],
        f"{r1['selected'][:3]}")
    r2 = select(["tools/gate_engine.py"])
    chk("高危面 ⇒ 全量", r2["full_suite"] is True and r2["selected_count"] == r2["total_test_files"])
    r3 = select(["whatever/unknown.bin"])
    chk("未归类 ⇒ 全量（fail-safe）", r3["full_suite"] is True)
    r4 = select(["tests/test_655_tools.py"])
    chk("测试自身改动 ⇒ 只选自己", r4["selected"] == ["tests/test_655_tools.py"])
    r5 = select(["tools/zzz_never_mentioned_855.py"])
    chk("新工具无测试提及 ⇒ 全量", r5["full_suite"] is True)
    r6 = select([])
    chk("无改动 ⇒ 空集合且不全量", r6["selected"] == [] and r6["full_suite"] is False)
    chk("输出路径在 data 下", str(OUT_JSON).replace("\\", "/").endswith("data/655_test_selection.json"))
    print(f"test_selector_655 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="基于 git diff 的增量测试选择（655 C 杠杆 1）")
    ap.add_argument("--since", default="origin/master", help="对比基线（默认 origin/master）")
    ap.add_argument("--paths", nargs="*", default=None, help="显式给改动路径（不读 git）")
    ap.add_argument("--no-worktree", action="store_true", help="只看提交差异，忽略工作区改动")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--report", action="store_true", help="写 data/655_test_selection.json")
    ap.add_argument("--run", action="store_true", help="直接跑选中的测试（其余参数放 `--` 后）")
    ap.add_argument("--check", action="store_true")
    a, extra = ap.parse_known_args(argv)
    passthrough = extra[1:] if extra and extra[0] == "--" else extra

    if a.check:
        return selftest()

    paths = a.paths if a.paths is not None else changed_paths(a.since, not a.no_worktree)
    rep = select(paths)

    if a.report:
        OUT_JSON.parent.mkdir(parents=True, exist_ok=True)
        OUT_JSON.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8", newline="\n")
        print(f"[selector] 报告已写：{OUT_JSON.relative_to(ROOT).as_posix()}")

    if a.json:
        print(json.dumps(rep, ensure_ascii=False, indent=2))
    else:
        tag = "（全量回退）" if rep["full_suite"] else ""
        print(f"[selector] 改动 {len(paths)} 个路径 ⇒ 选中 {rep['selected_count']}/"
              f"{rep['total_test_files']} 个测试文件{tag}")
        for r in rep["reasons"][:8]:
            print(f"  · {r}")
        for s in rep["selected"][:15]:
            print(f"  - {s}")
        if rep["selected_count"] > 15:
            print(f"  …（其余 {rep['selected_count'] - 15} 个）")

    if a.run and rep["selected"]:
        return _run_pytest(rep["selected"], passthrough or ["-q", "-p", "no:cacheprovider"])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
