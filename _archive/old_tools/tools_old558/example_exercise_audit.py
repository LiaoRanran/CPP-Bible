#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
example_exercise_audit.py — 实例与题库系统化基线审计（M2）。

测量每章：
  - cpp 代码块数（实例候选）：```cpp / ``` (bare, 非 mermaid/asm/table 等)
  - 示例标签数：显式 "示例 N" 标记（章节已用约定）
  - 章级难度：是否存在 ★ 难度标记
  - 逐示例难度/主题标签：代码块紧邻是否带 [难度]/[主题]（本次新增约定待铺）
  - 习题段数：## 自测练习 / ### 练习 计数
  - 习题引用：习题段是否含 [引用]/答案/解析 标记

输出 JSON 基线 + 人类摘要。仅报告，不改文件。
用法：python3 tools/example_exercise_audit.py [--root Book] [--json OUT]
"""

import argparse
import json
import os
import re
import sys

CHAPTER_RE = re.compile(r'^ch\d+_.*\.md$')
FENCE = re.compile(r'^\s*```(.*)$')
EXAMPLE_LABEL = re.compile(r'示例\s*\d+')
CHAPTER_DIFF = re.compile(r'难度\s*[:：]\s*[★☆]+')
PER_EX_DIFF = re.compile(r'\[\s*难度\s*[★☆]+\s*\]')
PER_EX_THEME = re.compile(r'\[\s*主题\s*[:：]\s*[^\]]+\]')
EXERCISE_H2 = re.compile(r'^##\s*(自测练习|附录：练习题|练习题|练习)\b')
EXERCISE_H3 = re.compile(r'^###\s*练习')
REF_MARK = re.compile(r'\[引用\]|答案|解析|参考答案')

# 非代码围栏语言（这些不算"实例"代码块）
NON_CODE_LANGS = {"mermaid", "table", "text", "bash", "sh", "console", "asm",
                  "dot", "html", "json", "xml", ""}


def audit_file(path):
    lines = open(path, encoding='utf-8', errors='replace').read().split('\n')
    in_fence = False
    fence_lang = ''
    cpp_blocks = 0
    example_labels = 0
    has_chapter_diff = False
    per_ex_diff = 0
    per_ex_theme = 0
    ex_h2 = 0
    ex_h3 = 0
    ex_with_ref = 0
    in_exercise = False

    for i, line in enumerate(lines):
        m = FENCE.match(line)
        if m:
            if not in_fence:
                in_fence = True
                _info = m.group(1).strip().lower()
                fence_lang = _info.split()[0] if _info else ""  # 取语言首 token（兼容 title="…" 信息串）
                if fence_lang in ('cpp', '') or (fence_lang == '' ):
                    # bare 或 cpp 都算实例候选（bare 多为 cpp 输出/片段）
                    if fence_lang in ('cpp', ''):
                        cpp_blocks += 1
            else:
                in_fence = False
            continue
        if in_fence:
            continue
        if EXAMPLE_LABEL.search(line):
            example_labels += 1
        if CHAPTER_DIFF.search(line):
            has_chapter_diff = True
        if PER_EX_DIFF.search(line):
            per_ex_diff += 1
        if PER_EX_THEME.search(line):
            per_ex_theme += 1
        if EXERCISE_H2.match(line):
            ex_h2 += 1
            in_exercise = True
        elif EXERCISE_H3.match(line):
            ex_h3 += 1
            in_exercise = True
        elif line.startswith('#'):
            in_exercise = False
        if in_exercise:
            if REF_MARK.search(line):
                ex_with_ref += 1

    return {
        "cpp_blocks": cpp_blocks,
        "example_labels": example_labels,
        "has_chapter_diff": has_chapter_diff,
        "per_ex_diff": per_ex_diff,
        "per_ex_theme": per_ex_theme,
        "exercise_h2": ex_h2,
        "exercise_h3": ex_h3,
        "exercise_ref_marks": ex_with_ref,
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="Book")
    ap.add_argument("--json", default=None)
    args = ap.parse_args()

    files = []
    for dp, _, ns in os.walk(args.root):
        for n in ns:
            if CHAPTER_RE.match(n):
                files.append(os.path.join(dp, n))
    files.sort()

    totals = {"cpp_blocks": 0, "example_labels": 0, "has_chapter_diff": 0,
              "per_ex_diff": 0, "per_ex_theme": 0, "exercise_h2": 0,
              "exercise_h3": 0, "exercise_ref_marks": 0}
    no_label_chapters = []
    per_ch = {}
    for f in files:
        s = audit_file(f)
        per_ch[f] = s
        for k in totals:
            if isinstance(totals[k], int):
                totals[k] += s[k]
        # 章节是否"逐示例标注缺失"：有代码块但示例标签为 0
        if s["cpp_blocks"] > 0 and s["example_labels"] == 0:
            no_label_chapters.append(f)

    print(f"扫描章节: {len(files)}")
    print(f"  cpp 代码块(实例候选): {totals['cpp_blocks']}")
    print(f"  示例标签(示例 N):     {totals['example_labels']}  (仅 {(totals['example_labels']/max(1,totals['cpp_blocks'])*100):.1f}% 代码块有显式编号)")
    print(f"  章级难度标记:         {totals['has_chapter_diff']} 章")
    print(f"  逐示例难度标签[难度]: {totals['per_ex_diff']} 处  <- M2 真缺口")
    print(f"  逐示例主题标签[主题]: {totals['per_ex_theme']} 处  <- M2 真缺口")
    print(f"  习题段(##/###):       {totals['exercise_h2']} / {totals['exercise_h3']}")
    print(f"  习题引用/答案标记:    {totals['exercise_ref_marks']} 处")
    print(f"  无示例标签的章节:     {len(no_label_chapters)} / {len(files)}")
    if no_label_chapters:
        print("  样例(前10):")
        for f in no_label_chapters[:10]:
            print("    ", os.path.relpath(f))

    if args.json:
        out = {"totals": totals, "no_label_chapters": [os.path.relpath(x) for x in no_label_chapters],
               "per_chapter": {os.path.relpath(k): v for k, v in per_ch.items()}}
        with open(args.json, 'w', encoding='utf-8', newline="\n") as fh:
            json.dump(out, fh, ensure_ascii=False, indent=2)
        print(f"\nJSON 基线: {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
