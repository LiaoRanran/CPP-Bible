#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
scan_compiler_refs.py — P0-2.1 编译器对比提及扫描器

扫描 Book/ 下所有 .md 章节中同时涉及 >=2 种编译器（GCC/Clang/MSVC）的对比提及，
按语义分类为：
  - feature   : 特性支持度（concepts/modules/coroutines 等是否被支持）
  - diag      : 报错信息 / 诊断差异（concepts 报错、模板报错友好度）
  - perf      : 性能差异（编译速度 / 运行速度 / 代码大小）
  - abi       : ABI 差异（名称修饰 / 二进制兼容 / 标准库 ABI）

输出：
  1) 按章节统计对比提及数
  2) 按类别统计
  3) 抽样打印每条比对上下文（前/后各 1 行），供人工建表

设计原则：正文不写死版本号，全部通过 docs/compiler-matrix.md 间接引用。
本脚本是 P0-2.2/2.3 的前置——先知道"对比集中在哪些章、哪类语义"，再建表。
"""

import os
import re
import json
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BOOK = os.path.join(ROOT, "Book")

# 三种编译器的识别正则
GCC_RE = re.compile(r"\b(GCC|g\+\+|G\+\+)\b", re.IGNORECASE)
CLANG_RE = re.compile(r"\b(Clang|clang\+\+)\b", re.IGNORECASE)
MSVC_RE = re.compile(r"\b(MSVC|Visual C\+\+|cl\.exe|MSVC)\b", re.IGNORECASE)

# 版本号
VER_RE = re.compile(r"\b(GCC|Clang|MSVC)?\s*(\d{1,2})(\.\d+)?\b")

# 语义分类关键词
CAT_PATTERNS = {
    "feature": re.compile(
        r"(支持|support|不支持|未实现|experimental|实现|可用|认可|可用|可用|可用|特性|feature|enabled|enable|需要.*标志|feature-test|__cpp_)",
        re.IGNORECASE,
    ),
    "diag": re.compile(
        r"(报错|error|diagnostic|诊断|友好|可读|提示|message|报错信息|编译错误|更易|更易读|模板报错|concept.*error)",
        re.IGNORECASE,
    ),
    "perf": re.compile(
        r"(编译速度|编译时间|运行速度|性能|perf|benchmark|更快|慢|代码大小|code size|体积|开销|overhead|优化|optimi)",
        re.IGNORECASE,
    ),
    "abi": re.compile(
        r"(ABI|名称修饰|name mangl|二进制兼容|二进制接口|libstdc\+\+|libc\+\+|MSVCRT|链接|link|动态库|静态库|\.so|\.dll|符号)",
        re.IGNORECASE,
    ),
}


def iter_md():
    for dirpath, _, filenames in os.walk(BOOK):
        for fn in sorted(filenames):
            if fn.endswith(".md"):
                yield os.path.join(dirpath, fn)


def classify(text):
    cats = set()
    for cat, pat in CAT_PATTERNS.items():
        if pat.search(text):
            cats.add(cat)
    return cats or {"uncategorized"}


def main():
    only_chapter = "--chapter" in sys.argv
    target = None
    if only_chapter and len(sys.argv) > sys.argv.index("--chapter") + 1:
        target = sys.argv[sys.argv.index("--chapter") + 1]

    per_chapter = {}
    per_cat = {}
    samples = []

    for path in iter_md():
        rel = os.path.relpath(path, ROOT)
        if target and target not in rel:
            continue
        with open(path, encoding="utf-8") as f:
            lines = f.readlines()
        for i, line in enumerate(lines):
            # 跳过代码块（``` 之间）
            stripped = line.strip()
            if stripped.startswith("```"):
                # 简单跳过：统计反引号配对
                depth = 1
                j = i + 1
                while j < len(lines) and depth > 0:
                    if lines[j].strip().startswith("```"):
                        depth -= 1
                    j += 1
                continue
            gcc = GCC_RE.search(line)
            clang = CLANG_RE.search(line)
            msvc = MSVC_RE.search(line)
            compilers = sum(bool(x) for x in (gcc, clang, msvc))
            if compilers >= 2:
                cats = classify(line)
                per_chapter[rel] = per_chapter.get(rel, 0) + 1
                for c in cats:
                    per_cat[c] = per_cat.get(c, 0) + 1
                ctx = lines[max(0, i - 1)].rstrip("\n") if i > 0 else ""
                samples.append(
                    {"file": rel, "line": i + 1, "cats": sorted(cats),
                     "text": stripped[:160], "ctx": ctx[:120]}
                )

    # 输出
    print("=" * 72)
    print(f"编译器对比提及扫描（同句/同行 >=2 编译器）")
    print(f"扫描目录: {BOOK}")
    print("=" * 72)
    total = sum(per_chapter.values())
    print(f"\n[总对比提及] {total} 条，覆盖 {len(per_chapter)} 个章节文件")
    print("\n[按类别]")
    for c, n in sorted(per_cat.items(), key=lambda kv: -kv[1]):
        print(f"  {c:12s} {n:4d}")
    print("\n[Top 25 章节（对比提及最多）]")
    for rel, n in sorted(per_chapter.items(), key=lambda kv: -kv[1])[:25]:
        print(f"  {n:3d}  {rel}")

    # 抽样：每类打印前若干条
    if "--samples" in sys.argv:
        print("\n" + "=" * 72)
        print("[抽样上下文]")
        print("=" * 72)
        for s in samples[:60]:
            print(f"\n{s['file']}:{s['line']}  [{','.join(s['cats'])}]")
            if s["ctx"]:
                print(f"  上下文: {s['ctx']}")
            print(f"  原文  : {s['text']}")

    # 机器可读
    out = {"total": total, "per_chapter": per_chapter, "per_cat": per_cat}
    with open(os.path.join(ROOT, "_compiler_scan.json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print(f"\n[已导出] _compiler_scan.json")


if __name__ == "__main__":
    main()
