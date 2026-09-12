"""纯注释 cpp 块盘点工具（L2 真机深耕管线）。

与 compile_all.extract_blocks 采用相同的 ```cpp 围栏语义，因此本工具的 block 编号
与 CI 编译报告（compile_report.json 的 block 字段）一一对应，可直接据此设计替换。

用法：
    python tools/comment_blocks.py scan --all
        # 全库盘点：按残留纯注释块数降序列出章节 + 汇总
    python tools/comment_blocks.py scan --chapter ch165
        # 单章：列出每个纯注释块的编号与行区间
    python tools/comment_blocks.py scan --chapter ch165 --dump
        # 单章 + 打印嫌疑块正文（便于人工判定 A/B/C 处理策略）
    python tools/comment_blocks.py scan --chapter ch165 --all-block
        # 单章全块概览（含非嫌疑块），用于核对编号对齐

判定规则：剥掉行注释(//)与块注释(/* */)后若整块无任何代码行，即为「纯注释块」。
"""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

BOOK: Path = Path(__file__).resolve().parent.parent / "Book"
SKIP_DIRS = {"_legacy_ModernCppBible"}
SKIP_FILES = {"SUMMARY.md", "GLOSSARY.md", "PREREQUISITES.md", "INDEX.md", "MANIFEST.md"}
FENCE_OPEN_RE = re.compile(r"^\s*```cpp")


@dataclass
class Block:
    index: int
    body: list[str]
    start: int  # 1-based 围栏起始行
    end: int    # 1-based 围栏结束行


def iter_md_files(book: Path) -> list[Path]:
    out: list[Path] = []
    for p in sorted(book.rglob("*.md")):
        if any(part in SKIP_DIRS for part in p.parts):
            continue
        if p.name in SKIP_FILES:
            continue
        out.append(p)
    return out


def find_chapter(book: Path, prefix: str) -> Path:
    hits = [p for p in iter_md_files(book) if p.stem.startswith(prefix)]
    if len(hits) != 1:
        raise SystemExit(f"expected 1 file for prefix {prefix!r}, got {len(hits)}: {hits}")
    return hits[0]


def parse(path: Path) -> list[Block]:
    """按 compile_all 语义提取所有 ```cpp 块（只认 cpp，不看 c++）。"""
    raw = path.read_text(encoding="utf-8")
    lines = raw.split("\n")
    blocks: list[Block] = []
    i = 0
    n = len(lines)
    while i < n:
        if FENCE_OPEN_RE.match(lines[i]):
            j = i + 1
            body: list[str] = []
            while j < n and lines[j].strip() != "```":
                body.append(lines[j])
                j += 1
            blocks.append(Block(len(blocks) + 1, body, i + 1, j + 1))
            i = j + 1
        else:
            i += 1
    return blocks


def code_lines(body: Sequence[str]) -> list[str]:
    out: list[str] = []
    for ln in body:
        t = re.sub(r"/\*.*?\*/", "", ln)
        k = t.find("//")
        if k >= 0:
            t = t[:k]
        t = t.strip()
        if t:
            out.append(t)
    return out


def is_pure_comment(body: Sequence[str]) -> bool:
    return not code_lines(body)


def _print_block(blk: Block, book_rel: Path, dump: bool) -> None:
    print(f"  blk#{blk.index:3} L{blk.start}-{blk.end} n={len(blk.body)}")
    if dump:
        for ln in blk.body:
            print("      | " + ln)


def run_scan(args: argparse.Namespace) -> None:
    if args.all_block:
        path = find_chapter(BOOK, args.chapter)
        print(f"file: {path}")
        for blk in parse(path):
            head = next((x.strip() for x in blk.body if x.strip()), "")
            flag = "PURE" if is_pure_comment(blk.body) else ""
            print(f"  blk#{blk.index:3} L{blk.start}-{blk.end} n={len(blk.body):3} {flag:4} {head[:80]}")
        return

    if args.chapter:
        path = find_chapter(BOOK, args.chapter)
        print(f"file: {path}")
        all_blocks = parse(path)
        pure_list = [b for b in all_blocks if is_pure_comment(b.body)]
        print(f"total cpp blocks = {len(all_blocks)} | pure-comment = {len(pure_list)}")
        for blk in pure_list:
            _print_block(blk, path, args.dump)
        return

    rows: list[tuple[int, Path]] = []
    grand = 0
    grand_main = 0
    for p in iter_md_files(BOOK):
        blocks = parse(p)
        pure = sum(1 for b in blocks if is_pure_comment(b.body))
        grand += len(blocks)
        grand_main += pure
        if pure:
            rows.append((pure, p))
    print(f"TOTAL cpp blocks = {grand} | pure-comment = {grand_main} across "
          f"{len([1 for _ in rows])} chapters")
    print()
    print(f"chapters with pure-comment blocks ({len(rows)}):")
    for pure, p in sorted(rows, key=lambda r: -r[0]):
        print(f"  {pure:4}  {p.relative_to(BOOK).as_posix()}")


def main(argv: Sequence[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="纯注释 cpp 块盘点")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p_scan = sub.add_parser("scan", help="盘点纯注释 cpp 块")
    p_scan.add_argument("--all", action="store_true", help="全库盘点（默认）")
    p_scan.add_argument("--chapter", help="章前缀，如 ch165")
    p_scan.add_argument("--dump", action="store_true", help="打印嫌疑块正文")
    p_scan.add_argument("--all-block", action="store_true", help="单章全块概览")
    p_scan.set_defaults(func=run_scan)

    args = ap.parse_args(argv)
    args.func(args)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
