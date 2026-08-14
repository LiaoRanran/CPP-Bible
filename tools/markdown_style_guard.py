#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
markdown_style_guard.py — Markdown 版式标准化守门员（M1）。

fence-aware 地扫描 Book/ 下所有 ch*.md（章节文件），检测三类版式缺陷：

  S1 多 H1        : 文件顶层（非代码围栏内）出现 >1 个 `# ` 一级标题。
  S2 H1 过长      : 一级标题文本长度（按"宽字符=2、ASCII=1"的显示宽度计）超过阈值。
  S3 围栏缺语言   : 开围栏 ``` 后无语言标签（bare fence），如 ``` 而非 ```cpp。

设计要点：
  - fence 状态机：在 ``` 围栏内的 # 不计入 H1；围栏必须成对（奇数视为结构错误，
    单独报 S0 不平衡，便于与 sweep_fences 交叉核对）。
  - 不修改任何文件（--check 仅报告）。--fix 默认可对"围栏缺语言"补 `text` 标签，
    但属于破坏性，需显式开启且会逐个确认式处理；本版默认只报不修。
  - 输出 JSON 报告（供 cppbible report 归集）+ 人类可读摘要。

用法：
  python3 tools/markdown_style_guard.py [--root ROOT] [--check] [--json OUT]
"""

import argparse
import json
import os
import re
import sys

# 显示宽度：CJK/全角按 2，其余按 1
def display_width(s: str) -> int:
    w = 0
    for ch in s:
        w += 2 if ord(ch) > 0x2E7F else 1  # 粗略：> U+2E7F 视作宽字符
    return w

H1_LIMIT = 40  # 显示宽度阈值（超过报 S2）

OPEN_FENCE = re.compile(r'^\s*```(.*)$')
H1_RE = re.compile(r'^#\s+(.*)$')
CHAPTER_RE = re.compile(r'^ch\d+_.*\.md$')

def analyze_file(path: str):
    """返回该文件的违规列表与统计。"""
    violations = []
    in_fence = False
    fence_line = 0
    h1_count = 0
    h1_texts = []
    fence_total = 0
    fence_without_lang = 0
    try:
        with open(path, 'r', encoding='utf-8', errors='replace') as fh:
            lines = fh.readlines()
    except Exception as e:
        return [{"type": "ERR", "line": 0, "msg": f"read error: {e}"}], {}
    for i, raw in enumerate(lines, 1):
        line = raw.rstrip('\n')
        m = OPEN_FENCE.match(line)
        if m:
            if not in_fence:
                in_fence = True
                fence_line = i
                fence_total += 1
                lang = m.group(1).strip()
                if lang == '':
                    fence_without_lang += 1
                    violations.append({"type": "S3", "line": i,
                                       "msg": "开围栏缺语言标签 (bare ```)"})
            else:
                in_fence = False
            continue
        if in_fence:
            continue  # 围栏内不判 H1
        hm = H1_RE.match(line)
        if hm:
            h1_count += 1
            txt = hm.group(1).strip()
            h1_texts.append((i, txt))
            if h1_count > 1:
                violations.append({"type": "S1", "line": i,
                                   "msg": f"多余一级标题 #{h1_count}: {txt[:30]}"})
            w = display_width(txt)
            if w > H1_LIMIT:
                violations.append({"type": "S2", "line": i,
                                   "msg": f"H1 显示宽度 {w} > {H1_LIMIT}: {txt[:30]}"})
    if in_fence:
        violations.append({"type": "S0", "line": fence_line,
                           "msg": "围栏未闭合（奇数围栏）"})
    stats = {
        "h1_count": h1_count,
        "h1_texts": h1_texts,
        "fence_total": fence_total,
        "fence_without_lang": fence_without_lang,
    }
    return violations, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default="Book")
    ap.add_argument("--check", action="store_true", help="运行检查（默认行为）")
    ap.add_argument("--json", default=None, help="输出 JSON 报告路径")
    args = ap.parse_args()

    root = args.root
    files = []
    for dirpath, _, names in os.walk(root):
        for n in names:
            if CHAPTER_RE.match(n):
                files.append(os.path.join(dirpath, n))
    files.sort()

    report = {
        "tool": "markdown_style_guard",
        "root": os.path.abspath(root),
        "h1_limit": H1_LIMIT,
        "files_scanned": len(files),
        "summary": {"S0": 0, "S1": 0, "S2": 0, "S3": 0},
        "files": {},
    }
    multi_h1_files = []
    long_h1_files = []
    bare_fence_files = []

    for f in files:
        vios, stats = analyze_file(f)
        by_type = {"S0": 0, "S1": 0, "S2": 0, "S3": 0}
        for v in vios:
            if v["type"] in by_type:
                by_type[v["type"]] += 1
                report["summary"][v["type"]] += 1
        if by_type["S1"] > 0 or by_type["S0"] > 0:
            multi_h1_files.append(f)
        if by_type["S2"] > 0:
            long_h1_files.append(f)
        if by_type["S3"] > 0:
            bare_fence_files.append(f)
        if any(by_type.values()):
            report["files"][f] = {"violations": vios, "stats": stats,
                                  "by_type": by_type}

    # 人类可读摘要
    s = report["summary"]
    print(f"扫描章节文件: {len(files)}")
    print(f"  S0 围栏不平衡 : {s['S0']} 处 (跨 {len(multi_h1_files)} 文件, 与 S1 重叠)")
    print(f"  S1 多 H1      : {s['S1']} 处 (跨 {len(multi_h1_files)} 文件)")
    print(f"  S2 H1 过长    : {s['S2']} 处 (跨 {len(long_h1_files)} 文件)")
    print(f"  S3 围栏缺语言 : {s['S3']} 处 (跨 {len(bare_fence_files)} 文件)")
    print(f"  含任一违规文件: {len(report['files'])} / {len(files)}")
    if bare_fence_files:
        print("\n缺语言围栏文件(前20):")
        for f in bare_fence_files[:20]:
            print("   ", os.path.relpath(f))
    if multi_h1_files:
        print("\n多H1/不平衡文件(前20):")
        for f in multi_h1_files[:20]:
            print("   ", os.path.relpath(f))

    if args.json:
        with open(args.json, 'w', encoding='utf-8') as fh:
            json.dump(report, fh, ensure_ascii=False, indent=2)
        print(f"\nJSON 报告已写: {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
