#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
example_tag_inject.py — 逐示例标注注入器（M2 机械铺标签工具）。

为章节中"未被标注"的代码示例（```cpp / 裸 ``` 代码块）在其围栏前插入一行
标准标题：

    > **示例 N** [难度 ★☆☆] [主题：<最近小节标题>]

设计约束（安全、幂等、不碰代码）：
  - 仅在围栏前插入一行 blockquote，绝不改动围栏内任何代码 -> 编译门禁不受影响。
  - 幂等：若该代码块前一行已是 `> **示例` 标题则跳过。
  - 主题(Theme)自动派生自"最近的上层 ## / ### 标题"文本（去除序号与特殊符号），
    保证即使自动生成也有可读语义；人工可后续精修。
  - 难度(Difficulty)取自章首难度标记（如 `难度：★★★★☆`），缺省 ★☆☆。
  - 跳过非代码围栏：mermaid / text / table / bash / asm / dot / html / json / xml。
  - 跳过习题答案段内的代码块？不跳过——它们也是可运行示例，统一标注无害。

用法：
  python3 tools/example_tag_inject.py [--root Book] [--only PATH] [--dry-run]
  --dry-run 只报告将插入多少，不落盘。
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
CAPTION = re.compile(r'^>\s*\*\*示例\s*\d+')
CHAPTER_DIFF = re.compile(r'难度\s*[:：]\s*([★☆]+)')

SKIP_LANGS = {"mermaid", "text", "table", "bash", "sh", "console", "asm",
              "dot", "html", "json", "xml", ""}

# 把小节标题清洗成主题词：去序号(①②③⑳⑫等)、去标签/括号组、截断
def clean_theme(h: str) -> str:
    h = h.strip()
    # 先整体移除成对的括号/标签组，避免硬截断把括号切开产生残缺主题
    h = re.sub(r'\[[^\]]*\]', '', h)      # 移除 [xxx] 标签组（如 [实现·libstdc++]）
    h = re.sub(r'（[^（）]*）', '', h)     # 移除全角括号组
    h = re.sub(r'\([^()]*\)', '', h)      # 移除半角括号组
    h = re.sub(r'^[①-⑳0-9a-zA-Z\s/、，。：:.（）()\-]+', '', h)  # 去前导序号/标点
    h = re.sub(r'[`*_#]', '', h)
    h = h.strip(' ：:')
    h = re.sub(r'[（(]\s*$', '', h).strip()  # 兜底去除行尾孤立开括号
    if not h:
        h = "未分类"
    # 安全网：若仍有括号不平衡，降级为未分类（绝不输出残缺主题）
    if h.count('（') != h.count('）') or h.count('(') != h.count(')'):
        h = "未分类"
    return h[:30]


def stars(n: int) -> str:
    return '★' * n + '☆' * (5 - n)


def process_file(path: str, dry: bool):
    raw = open(path, encoding='utf-8', errors='replace').read()
    lines = raw.split('\n')
    out = []
    in_fence = False
    fence_lang = ''
    theme = '未分类'
    chapter_diff_n = 1  # 默认 ★☆☆
    inserted = 0
    ex_no = 0
    i = 0

    # 先取章首难度 + 章标题(作主题回退)
    head = '\n'.join(lines[:40])
    m = CHAPTER_DIFF.search(head)
    if m:
        chapter_diff_n = min(5, max(1, m.group(1).count('★')))
    m1 = H1.search(head)
    if m1:
        theme = clean_theme(m1.group(1))

    while i < len(lines):
        line = lines[i]
        fm = FENCE.match(line)
        if fm:
            if not in_fence:
                in_fence = True
                fence_lang = fm.group(1).strip().lower()
                # 开围栏：若该代码块前一行(跳过空行)已是示例标题则跳过（幂等）
                prev = lines[i-1].strip() if i > 0 else ''
                if fence_lang in ('cpp', ''):
                    if CAPTION.match(prev):
                        pass  # 已标注
                    else:
                        ex_no += 1
                        caption = f"> **示例 {ex_no}** [难度 {stars(chapter_diff_n)}] [主题：{theme}]"
                        out.append(caption)
                        inserted += 1
                out.append(line)
            else:
                in_fence = False
                out.append(line)
            i += 1
            continue
        if in_fence:
            out.append(line)
            i += 1
            continue
        # 非围栏：更新主题上下文（最近 ## / ###，回退 H1）
        h2 = H2.match(line)
        h3 = H3.match(line)
        if h2:
            theme = clean_theme(h2.group(1)) or theme
        elif h3:
            theme = clean_theme(h3.group(1)) or theme
        out.append(line)
        i += 1

    if not dry and inserted > 0:
        with open(path, 'w', encoding='utf-8', newline='\n') as fh:
            fh.write('\n'.join(out))
    return inserted


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="Book")
    ap.add_argument("--only", default=None, help="仅处理单文件(相对或绝对路径)")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    targets = []
    if args.only:
        targets = [args.only]
    else:
        for dp, _, ns in os.walk(args.root):
            for n in ns:
                if CHAPTER_RE.match(n):
                    targets.append(os.path.join(dp, n))
    targets.sort()

    total = 0
    for f in targets:
        ins = process_file(f, args.dry_run)
        total += ins
        if ins:
            print(f"  +{ins:3d}  {os.path.relpath(f)}")
    print(f"\n{'[dry-run] ' if args.dry_run else ''}共插入 {total} 个示例标题")
    return 0


if __name__ == "__main__":
    sys.exit(main())
