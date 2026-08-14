#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
example_caption_cleanup.py — 修正 M2 注入产生的"主题"缺陷（一次性收口工具）。

问题背景
========
example_tag_inject 初版的 clean_theme 在 18 字处硬截断，常把全角括号（...）
切到一半，产生形如 `[主题：内存图（C 的 struct vs ]` 的不平衡/截断主题。
全库扫描共约 1453 / 7751 处（≈19%）。

本工具
======
逐章扫描 `> **示例 N** [难度 X] [主题：Y]` 标题行，仅当主题"括号不平衡"时，
用改进版 clean_theme 重新从"最近 ##/### 标题"派生主题并重写该行。

安全约束（与 M2 注入器一致）
  - 不改动任何代码围栏内的内容 -> 编译门禁不受影响。
  - 幂等：仅重写不平衡主题，平衡主题原样保留；已清过的再跑 0 改动。
  - LF 安全：写入一律 newline='\\n'。
  - 仅重写，不新增/删除示例标题行（示例编号与难度严格保留）。

用法
====
  python3 tools/example_caption_cleanup.py [--root Book] [--dry-run]
"""

import argparse
import os
import re
import sys

CHAPTER_RE = re.compile(r'^ch\d+_.*\.md$')
FENCE = re.compile(r'^\s*```(.*)$')
H1 = re.compile(r'^#\s+(.*)$')
H2 = re.compile(r'^##\s+(.*)$')
H3 = re.compile(r'^###\s+(.*)$')
# 捕获示例标题行的 7 个片段：前缀/编号/难度段/难度星/主题段/主题/结尾
CAP_RE = re.compile(
    r'^(>\s*\*\*示例\s*)(\d+)(\*\*\s*\[难度\s*)([★☆]+)(\]\s*\[主题：)(.*?)(\]\s*)$'
)


def clean_theme(h: str) -> str:
    h = h.strip()
    h = re.sub(r'\[[^\]]*\]', '', h)
    h = re.sub(r'（[^（）]*）', '', h)
    h = re.sub(r'\([^()]*\)', '', h)
    h = re.sub(r'^[①-⑳0-9a-zA-Z\s/、，。：:.（）()\-]+', '', h)
    h = re.sub(r'[`*_#]', '', h)
    h = h.strip(' ：:')
    h = re.sub(r'[（(]\s*$', '', h).strip()
    if not h:
        h = "未分类"
    if h.count('（') != h.count('）') or h.count('(') != h.count(')'):
        h = "未分类"
    return h[:30]


def balanced(t: str) -> bool:
    return t.count('（') == t.count('）') and t.count('(') == t.count(')')


def process_file(path: str, dry: bool):
    raw = open(path, encoding='utf-8', errors='replace').read()
    lines = raw.split('\n')
    out = []
    in_fence = False
    theme = '未分类'
    # 章首 H1 作主题回退（与注入器一致）
    head = '\n'.join(lines[:40])
    m1 = H1.search(head)
    if m1:
        theme = clean_theme(m1.group(1))
    fixed = 0
    for line in lines:
        fm = FENCE.match(line)
        if fm:
            in_fence = not in_fence
            out.append(line)
            continue
        if not in_fence:
            h2 = H2.match(line)
            h3 = H3.match(line)
            if h2:
                theme = clean_theme(h2.group(1)) or theme
            elif h3:
                theme = clean_theme(h3.group(1)) or theme
        m = CAP_RE.match(line.rstrip('\n'))
        if m and not balanced(m.group(6)):
            new = (f"{m.group(1)}{m.group(2)}{m.group(3)}{m.group(4)}"
                   f"{m.group(5)}{theme}{m.group(7)}")
            out.append(new)
            fixed += 1
            continue
        out.append(line)
    if not dry and fixed > 0:
        with open(path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(out))
    return fixed


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="Book")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    targets = []
    for dp, _, ns in os.walk(args.root):
        for n in ns:
            if CHAPTER_RE.match(n):
                targets.append(os.path.join(dp, n))
    targets.sort()

    total = 0
    touched = 0
    for f in targets:
        fx = process_file(f, args.dry_run)
        total += fx
        if fx:
            touched += 1
            print(f"  ~{fx:3d}  {os.path.relpath(f)}")
    print(f"\n{'[dry-run] ' if args.dry_run else ''}"
          f"共修正 {total} 个示例主题（涉及 {touched} 个文件）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
