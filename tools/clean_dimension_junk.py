#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""clean_dimension_junk.py — 残留污染节清理（#18）

背景
====
Phase 3 清理签名=『附录 Z/Z+/ZZ/ZZZ/FINAL/维度增强』，只匹配了"维度增强"，
漏掉同构的『维度补齐』/『维度批量补齐』批量污染节（19 文件 / 20 节 / 974 行）。
这些节含占位提案号 PxxxxRxx、无来源数字断言 ~5ns、以及无空格拼接的关键词沙拉，
属生成式灌水，触犯 AGENT.md 红线#1/#3。

做法
====
section-aware 状态机：从 `## 维度补齐` / `## 维度批量补齐` 头开始，删除其后所有行，
直到遇到下一个**真实**（非污染）`## ` 节标题为止。天然处理：
  - 连续两个污染头（维度补齐 → 维度批量补齐 紧邻）
  - 污染头与其后 `## 相关章节` 之间的无空格拼接关键词沙拉（如 StackHeapCache...）
  - 孤行的 stray 碎片（如『定义 基本语法 使用方式 注意事项。』）
保留其后 `## 相关章节` / `## 自测练习` 等优质节。

纪律
====
- 不改源语义：只删污染节，不稀释、不注水。
- 幂等：已无污染头的文件跳过，不产生空备份。
- 可回滚：落盘前写 `<name>.dimension_junk.bak`。
- 默认 dry-run：只打印计划；`--apply` 才真正写入。

用法
====
  python tools/clean_dimension_junk.py                 # dry-run 全库
  python tools/clean_dimension_junk.py --apply         # 实际清理全库
  python tools/clean_dimension_junk.py Book/.../chXX.md --apply
"""
from __future__ import annotations
import argparse
import glob
import pathlib
import re
import sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
BOOK = ROOT / "Book"

JUNK_HDR = re.compile(r"^##\s+(维度补齐|维度批量补齐)\s*$")
HDR = re.compile(r"^##\s+")


def clean_text(text: str) -> tuple[str, int]:
    """删除所有污染节。返回 (新文本, 删除行数)。"""
    lines = text.split("\n")
    out: list[str] = []
    in_junk = False
    removed = 0
    for ln in lines:
        if JUNK_HDR.match(ln):
            in_junk = True
            removed += 1
            continue
        if in_junk:
            # 遇到真实（非污染）`## ` 节 → 停止删除并保留该行
            if HDR.match(ln) and not JUNK_HDR.match(ln):
                in_junk = False
                out.append(ln)
                continue
            removed += 1
            continue
        out.append(ln)
    return "\n".join(out), removed


def main() -> int:
    ap = argparse.ArgumentParser(description="残留污染节清理（维度补齐/维度批量补齐）")
    ap.add_argument("paths", nargs="*", help="指定章节；省略则全库")
    ap.add_argument("--apply", action="store_true", help="实际写入（默认 dry-run）")
    args = ap.parse_args()

    if args.paths:
        files = []
        for p in args.paths:
            pp = pathlib.Path(p)
            if not pp.is_absolute():
                pp = ROOT / p
            files.append(pp.resolve())
    else:
        files = [pathlib.Path(f).resolve()
                 for f in glob.glob(str(BOOK / "**" / "ch*.md"), recursive=True)]
    files = [f for f in files if f.exists() and not str(f).endswith(".bak")]

    mode = "APPLY" if args.apply else "DRY-RUN"
    print(f"=== clean_dimension_junk [{mode}] 目标 {len(files)} 文件 ===")
    total_removed = 0
    changed = 0
    for f in files:
        text = f.read_text(encoding="utf-8")
        new, removed = clean_text(text)
        if removed == 0:
            continue
        changed += 1
        total_removed += removed
        rel = f.relative_to(ROOT).as_posix()
        if args.apply:
            bak = f.with_suffix(f.suffix + ".dimension_junk.bak")
            if not bak.exists():
                bak.write_text(text, encoding="utf-8")
            f.write_text(new, encoding="utf-8")
            print(f"  [CLEAN] {rel}: 删 {removed} 行 (备份 {bak.name})")
        else:
            print(f"  [PLAN ] {rel}: 将删 {removed} 行")
    print("-" * 64)
    print(f"变更文件 {changed} · 删除行数 {total_removed}")
    if not args.apply:
        print("（dry-run，未写入。加 --apply 执行）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
