#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
交叉引用审计工具
================
检测全书的交叉引用覆盖度、断链和缺失。

用法:
    python tools/crossref_audit.py                  # 审计全部
    python tools/crossref_audit.py --missing-only   # 仅显示缺失交叉引用的 part
    python tools/crossref_audit.py --fix-suggest    # 为每个缺失章节生成建议的交叉引用

输出:
    - 每 part 的交叉引用总条数/断链数/平均每章条数
    - 完全无交叉引用的 part（裸模块）
    - 断链清单（引用了不存在的文件）
"""

import argparse
import re
import sys
from collections import defaultdict
from pathlib import Path

CROSSREF_RE = re.compile(r"(?:⟶\s*|→\s*)(Book/[^\s\)\]>。，；：、》）(（]+)")
FILE_LINK_RE = re.compile(r"`?(Book/[A-Za-z0-9_/.\-]+\.md)`?")


def find_book_root():
    here = Path(__file__).resolve().parent
    for p in [here.parent, here]:
        if (p / "Book").is_dir():
            return p
    return here.parent


def audit(root: Path):
    book = root / "Book"
    if not book.is_dir():
        print(f"[X] Book 目录不存在: {book}")
        return

    part_stats = {}
    all_broken = []
    total_refs = 0

    for part_dir in sorted(book.iterdir()):
        if not part_dir.is_dir():
            continue
        chapters = sorted(part_dir.glob("ch*.md"))
        if not chapters:
            continue

        part_refs = 0
        part_broken = []

        for ch in chapters:
            text = ch.read_text(encoding="utf-8")
            refs = set(FILE_LINK_RE.findall(text)) | set(CROSSREF_RE.findall(text))
            part_refs += len(refs)

            for r in refs:
                r_clean = r.strip("`").replace("\\", "/")
                if not (root / r_clean).exists():
                    part_broken.append((ch.name, r_clean))

        part_stats[part_dir.name] = {
            "chapters": len(chapters),
            "refs": part_refs,
            "avg_refs": part_refs / len(chapters),
            "broken": part_broken,
        }
        total_refs += part_refs
        all_broken.extend(part_broken)

    return part_stats, all_broken, total_refs


def suggest_refs(chapter_path: Path, all_chapters: list) -> list:
    """根据章节编号和主题推荐交叉引用目标。"""
    suggestions = []
    name = chapter_path.stem
    num_match = re.match(r"ch(\d+)", name)
    if not num_match:
        return suggestions
    num = int(num_match.group(1))

    # 前/后章
    for offset in [-1, 1, -2, 2]:
        target_num = num + offset
        for c in all_chapters:
            if c.stem.startswith(f"ch{target_num:02d}"):
                suggestions.append(f"⟶ {c.relative_to(chapter_path.parents[3]).as_posix()}")
                break

    # 同 part 推荐
    for c in all_chapters:
        if c.parent == chapter_path.parent and c != chapter_path:
            suggestions.append(f"⟶ {c.relative_to(chapter_path.parents[3]).as_posix()}")
            break

    return list(set(suggestions))[:5]


def main():
    ap = argparse.ArgumentParser(description="交叉引用审计")
    ap.add_argument("--root", default=None, help="CPP-Bible 根目录")
    ap.add_argument("--missing-only", action="store_true", help="仅显示缺失引用的 part")
    ap.add_argument("--fix-suggest", action="store_true", help="为裸章节生成建议的交叉引用")
    args = ap.parse_args()

    root = Path(args.root) if args.root else find_book_root()
    print(f"[*] 审计根目录: {root}")

    part_stats, all_broken, total_refs = audit(root)

    if not part_stats:
        print("[X] 未找到任何 part")
        return

    # 输出报告
    print(f"\n{'='*70}")
    print(f"{'Part':<25} {'章数':>4} {'引用':>5} {'均/章':>6} {'断链':>4} {'状态'}")
    print(f"{'-'*70}")

    bare_parts = []
    for pname, stats in sorted(part_stats.items()):
        refs = stats["refs"]
        broken_count = len(stats["broken"])
        avg = stats["avg_refs"]
        status = "OK" if avg >= 3 and broken_count == 0 else "⚠️ 缺引用" if avg == 0 else "⚡ 不足"
        if avg == 0:
            bare_parts.append(pname)

        print(f"{pname:<25} {stats['chapters']:>4} {refs:>5} {avg:>5.1f} {broken_count:>4} {status}")

    print(f"{'-'*70}")
    print(f"{'合计':<25} {sum(s['chapters'] for s in part_stats.values()):>4} {total_refs:>5}")
    print()

    # 裸模块（完全无交叉引用）
    if bare_parts:
        print(f"[!] {len(bare_parts)} 个 part 完全没有交叉引用:")
        for bp in bare_parts:
            print(f"    - {bp}")
        print()

    # 断链
    if all_broken and not args.missing_only:
        print(f"[!] {len(all_broken)} 条断链:")
        for fname, ref in all_broken[:15]:
            print(f"    {fname}: {ref}")
        if len(all_broken) > 15:
            print(f"    ... 共 {len(all_broken)} 条，以上前 15 条")
        print()

    # 修复建议
    if args.fix_suggest:
        print("[*] 生成交叉引用建议:")
        book = root / "Book"
        all_chapters = list(book.rglob("ch*.md"))
        for pname in bare_parts:
            part_dir = book / pname
            for ch in sorted(part_dir.glob("ch*.md")):
                suggestions = suggest_refs(ch, all_chapters)
                if suggestions:
                    print(f"  {ch.relative_to(book).as_posix()}:")
                    for s in suggestions:
                        print(f"      {s}")
        print()

    # 汇总评分
    covered_parts = len(part_stats) - len(bare_parts)
    coverage_pct = covered_parts / len(part_stats) * 100 if part_stats else 0
    print(f"[*] 交叉引用覆盖率: {covered_parts}/{len(part_stats)} part ({coverage_pct:.0f}%)")
    print(f"[*] 断链总数: {len(all_broken)}")
    print(f"[*] 交叉引用总计: {total_refs} 条")

    if coverage_pct < 50:
        print("\n[!] ⚠️  覆盖率低于 50%，建议分批回填交叉引用。")


if __name__ == "__main__":
    main()
