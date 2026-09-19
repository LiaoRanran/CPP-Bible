#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""doc_frontmatter.py — 批量给架构文档补 YAML frontmatter（498 任务 1 / P0-7）。

为什么：`References/architecture_架构演进/` 下 230 份 .md 此前 **0 份有 frontmatter**——
编号/标题/状态/创建时间只存在于文件名里，机器无法消费（文档生命周期、归档状态、版本管理
都缺少结构化入口；490 的"文档生命周期"设计依赖这些字段）。

字段（逐字按 498 规格）
======================
    ---
    id: <编号，纯数字；archive_ 前缀用 archive-编号；无编号用文件名 slug>
    title: <文件名去编号前缀与 .md，下划线转空格>
    status: active | archived（archive_ 前缀即归档）
    type: architecture-note
    created_at: <文件 mtime 的 YYYY-MM-DD>
    ---

工程约束（勿弱化）
==================
* **字节级操作**：读 `read_bytes`、按原文件行尾（检测首个 `\n` 前的字符）拼 frontmatter，
  再写 `write_bytes`——**原有内容一个字节不动**（避免 read_text/write_text 的
  universal-newlines 把 CRLF 归一成 LF 从而改写整文件行尾；494 任务 1 的同款教训）。
* **幂等**：首行是 `---`（允许 BOM 前缀）即跳过；重复 `--apply` 改动数必须为 0。
* 默认 **dry-run**，必须显式 `--apply` 才写盘。
"""
from __future__ import annotations

import argparse
import re
import sys
import time
from pathlib import Path

from utf8_console import ensure_utf8

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_DIR = ROOT / "References" / "architecture_架构演进"
_NUM_PREFIX = re.compile(r"^(\d+)")
# 归档件编号**保留字母后缀**（实测 `archive_365B_独立红队Agent_投喂提示词.md`：只取数字会把
# `B` 漏进 title ⇒ id=archive-365 + title="B 独立红队…"；正确为 id=archive-365B）
_ARCHIVE = re.compile(r"^archive[_-](\d+[A-Za-z]?)")


def _eol(raw: bytes) -> bytes:
    """原文件行尾（取首个换行判断）——frontmatter 沿用同一行尾，避免混行尾。"""
    i = raw.find(b"\n")
    return b"\r\n" if i > 0 and raw[i - 1:i] == b"\r" else b"\n"


def build_frontmatter(path: Path) -> dict[str, str]:
    """按文件名与 mtime 推导 5 个字段（纯函数，便于单测）。"""
    stem = path.stem
    arc = _ARCHIVE.match(stem)
    num = _NUM_PREFIX.match(stem)
    if arc:
        fid, status = f"archive-{arc.group(1)}", "archived"
        title = stem[arc.end():].lstrip("_-")
    elif num:
        fid, status = num.group(1), "active"
        title = stem[num.end():].lstrip("_-")
    else:
        fid, status = stem, "active"
        title = stem
    return {
        "id": fid,
        "title": title.replace("_", " ") or stem,
        "status": status,
        "type": "architecture-note",
        "created_at": time.strftime("%Y-%m-%d", time.localtime(path.stat().st_mtime)),
    }


def has_frontmatter(raw: bytes) -> bool:
    """首行是否为 `---`（容忍 BOM 与两种行尾）。"""
    head = raw[:8].lstrip(b"\xef\xbb\xbf")
    return head.startswith(b"---\r\n") or head.startswith(b"---\n")


def render(fm: dict[str, str], eol: bytes) -> bytes:
    body = "".join(f"{k}: {v}{eol.decode()}" for k, v in fm.items())
    return f"---{eol.decode()}{body}---{eol.decode()}".encode("utf-8")


def process(d: Path, apply: bool) -> tuple[int, int]:
    """返回 (added, skipped)。"""
    added = skipped = 0
    for p in sorted(d.rglob("*.md")):
        raw = p.read_bytes()
        if has_frontmatter(raw):
            skipped += 1
            print(f"[SKIP] {p.name}（已有 frontmatter）")
            continue
        fm = build_frontmatter(p)
        print(f"[ADD ] {p.name}  id={fm['id']} status={fm['status']} "
              f"created_at={fm['created_at']} title={fm['title'][:40]}")
        if apply:
            p.write_bytes(render(fm, _eol(raw)) + raw)
        added += 1
    return added, skipped


def main(argv: list[str] | None = None) -> int:
    ensure_utf8()
    ap = argparse.ArgumentParser(description="批量补 frontmatter（498 任务 1）")
    ap.add_argument("--apply", action="store_true", help="实际写入（默认只 dry-run）")
    ap.add_argument("--dir", default=None, help=f"目标目录（默认 {DEFAULT_DIR.name}）")
    a = ap.parse_args(argv)
    d = Path(a.dir) if a.dir else DEFAULT_DIR
    if not d.is_dir():
        print(f"[doc_frontmatter] 目录不存在：{d}", file=sys.stderr)
        return 1
    added, skipped = process(d, a.apply)
    print(f"\n[doc_frontmatter] {'APPLY' if a.apply else 'DRY-RUN'}："
          f"新增 {added} · 跳过 {skipped}")
    if not a.apply:
        print("[doc_frontmatter] 这是 dry-run；确认无误后加 --apply 写入")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
