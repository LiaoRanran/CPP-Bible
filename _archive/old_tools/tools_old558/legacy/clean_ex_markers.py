#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
清理全书 <!--EX-START--> / <!--EX-END--> 模板残骸

这些标记是 v1 模板预处理系统的遗留，不渲染、仅噪声。
删除所有仅含 EX 标记的行，保留被包裹的代码内容。

用法:
    python tools/clean_ex_markers.py            # 清理全部 Book/
    python tools/clean_ex_markers.py --dry-run  # 仅预览
    python tools/clean_ex_markers.py Book/part01_history/  # 指定目录
"""

import argparse
import sys
from pathlib import Path

EX_LINES = {"<!--EX-START-->", "<!--EX-END-->"}


def clean_file(path: Path, dry: bool) -> tuple[int, int]:
    """清理单个文件，返回 (EX行数, 清理后行数)。"""
    with open(path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    ex_count = sum(1 for line in lines if line.strip() in EX_LINES)
    if ex_count == 0:
        return 0, len(lines)

    cleaned = [line for line in lines if line.strip() not in EX_LINES]

    # 清理连续空行（超过 2 行 -> 压缩为 1 空行）
    deduped = []
    blank_streak = 0
    for line in cleaned:
        if line.strip() == "":
            blank_streak += 1
            if blank_streak <= 1:
                deduped.append(line)
        else:
            blank_streak = 0
            deduped.append(line)

    if not dry:
        with open(path, "w", encoding="utf-8") as f:
            f.writelines(deduped)

    return ex_count, len(deduped)


def main():
    ap = argparse.ArgumentParser(description="清理 EX-START/EX-END 模板残骸")
    ap.add_argument("path", nargs="?", default=None, help="目标目录或文件")
    ap.add_argument("--dry-run", action="store_true", help="仅预览，不写入")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    target = Path(args.path) if args.path else root / "Book"

    if target.is_file():
        files = [target]
    elif target.is_dir():
        files = sorted(target.rglob("*.md"))
    else:
        print(f"[X] 路径不存在: {target}")
        sys.exit(1)

    total_ex = 0
    affected = 0
    total_saved = 0

    for f in files:
        ex, new_len = clean_file(f, args.dry_run)
        if ex > 0:
            total_ex += ex
            affected += 1
            old_len = ex + new_len  # 近似
            saved_lines = old_len - new_len
            total_saved += saved_lines
            prefix = "[DRY] " if args.dry_run else "[OK] "
            print(f"{prefix}{f.relative_to(root)}: -{saved_lines} 行 (清理 {ex} 个 EX 标记)")

    mode = "DRY RUN" if args.dry_run else "已清理"
    print(f"\n[{mode}] {affected} 个文件, {total_ex} 个 EX 标记, 节省 {total_saved} 行")


if __name__ == "__main__":
    main()
