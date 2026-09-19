#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""fix_book_links.py — 正文跨章 markdown 链接前缀修复器（Book/ → 源相对）

背景
====
147 章正文里的真实 markdown 链接写作 `](Book/partXX/chYY.md)`，`Book/` 前缀
是仓库根相对 - 工具链（xref_check / crossref_audit）按根解析没问题；但任何
**标准相对渲染器**（GitHub 预览、编辑器、mdBook）都会按"当前文件所在目录"
解析，前缀导致路径翻倍一层 → 一律 404。

本脚本把这类链接改写为**以当前章文件为基准的正确相对路径** `](../partXX/chYY.md)`，
使源码在编辑器/GitHub/mdBook 中可点击、可跳转。发布产物（site/PDF/EPUB）由
tools/rewrite_links.py 在构建期另行处理，不受影响（PDF 合并单文件会把相对
链接映射回 `#chNN` 锚点）。

设计约束（对齐 AGENT.md 红线）
==============================
- 只改正文 markdown 链接 `](...)`，不动裸文本 `⟶ Book/...`（后者源码本非链接，
  由 rewrite_links 构建期转链接，无失效问题）。
- 跳过代码围栏（``` / ~~~）内的内容，避免误改示例字符串。
- 幂等：只改写带 `Book/` 前缀的链接；已是相对/无前缀的链接原样保留。
- `--check` 只报不改（供 CI 卡口）；`--apply` 落盘改动。

关键：字节级外科替换
====================
目标模式为纯 ASCII，且不跨行。行尾（LF 或 CRLF）与其余字节原样保留，
只在命中的链接文本上做替换——绝不因文本模式读写而整体改写行尾/编码。
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "Book"

# 仅匹配 markdown 链接内（前置 ](），且目标为 Book/ 前缀的书内 .md，纯 ASCII。
PREFIXED_RE = re.compile(
    rb"\]\(Book/(part\d+[A-Za-z0-9_]*/ch\d+[A-Za-z0-9_]*\.md)(#[-\w]+)?\)"
)


def _strip_fences_line(buf: bytes) -> bytes:
    """返回同一行切成带围栏标记版本，供进程内判断。"""
    return buf


def _fenced(lines: list[bytes]) -> set[int]:
    """返回处于代码围栏（``` / ~~~）内的行号集合（字节级判定）。"""
    inside: set[int] = set()
    infence = False
    fence = b""
    for i, raw in enumerate(lines):
        s = raw.lstrip()
        if not infence:
            if s.startswith(b"```") or s.startswith(b"~~~"):
                infence = True
                fence = s[:3]
        elif s.startswith(fence):
            infence = False
            fence = b""
        else:
            inside.add(i)
    return inside


def transform_line(line: bytes) -> tuple[bytes, int]:
    """改写单行内所有带 Book/ 前缀的 md 链接为源相对路径，返回 (新行, 改写数)。"""
    def repl(m: re.Match) -> bytes:
        return bytes(b"](../" + m.group(1) + (m.group(2) or b"") + b")")
    hits = PREFIXED_RE.findall(line)
    new = PREFIXED_RE.sub(repl, line)
    return new, (len(hits) if new != line else 0)


def _iter_lines(raw: bytes) -> list[bytes]:
    """按 b'\\n' 切行；保留各行内的 \\r，rejoin 用 b'\\n' 即可逐字节复原行尾。"""
    return raw.split(b"\n")


def count_chapter(md: Path) -> int:
    raw = md.read_bytes()
    lines = _iter_lines(raw)
    fenced = _fenced(lines)
    return sum(len(PREFIXED_RE.findall(ln)) for i, ln in enumerate(lines) if i not in fenced)


def visit() -> list[tuple[Path, int]]:
    """扫描全部正式章，返回 [(文件, 待改链接数)]。"""
    out: list[tuple[Path, int]] = []
    for md in sorted(BOOK.rglob("ch*.md")):
        if "_legacy" in md.as_posix() or md.name.endswith(".bak"):
            continue
        n = count_chapter(md)
        if n:
            out.append((md, n))
    return out


def apply_file(md: Path) -> int:
    raw = md.read_bytes()
    lines = _iter_lines(raw)
    fenced = _fenced(lines)
    new_lines: list[bytes] = []
    total = 0
    for i, ln in enumerate(lines):
        if i not in fenced:
            nxt, n = transform_line(ln)
            new_lines.append(nxt)
            total += n
        else:
            new_lines.append(ln)
    md.write_bytes(b"\n".join(new_lines))
    return total


def main() -> int:
    ap = argparse.ArgumentParser(description="正文跨章 markdown 链接前缀修复器")
    ap.add_argument("--check", action="store_true",
                    help="仅报告待改数量，不改动；有待改则退出码 1（供 CI 卡口）")
    ap.add_argument("--apply", action="store_true", help="落盘改写")
    args = ap.parse_args()

    hits = visit()
    total = sum(n for _, n in hits)
    files = len(hits)

    if not hits:
        print("[links] ✅ 无带 Book/ 前缀的正文链接（已全部为源相对或已清理）")
        return 0

    print(f"[links] 发现 {total} 处带 Book/ 前缀链接，分布于 {files} 个文件：")
    for md, n in hits[:10]:
        print(f"        {md.relative_to(ROOT).as_posix()}: {n}")
    if files > 10:
        print(f"        ... 共 {files} 个文件")

    if args.apply:
        done = sum(apply_file(md) for md, _ in hits)
        print(f"[links] ✅ 已改写 {done} 处链接为源相对路径（{files} 文件）。")
        return 0

    print("[links] ⚠ 使用 --apply 落盘改写（可 git revert 回滚）。")
    return 1


if __name__ == "__main__":
    sys.exit(main())