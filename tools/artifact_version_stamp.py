#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""artifact_version_stamp.py — 工件-卡版本号迁移脚本（498 任务 2.1/2.2）。

做两件事（可分开）：
  --target asm   ：给 `Examples/atoms/*.asm` 首行插 `; artifact_version: 1`
  --target cards ：给证据卡 frontmatter 插 `artifact_version: 1`（有 `artifact:` 字段的卡）
  --target both  ：两者都做（默认）

⚠️ **不重算 artifact_sha256**（与 498 提示词 2.2 的偏差，有实测依据）：
    replay 的 artifact 校验是「**删旧工件 → 重跑生成命令 → 比对卡值 sha256**」
    （`atom_evidence_replay.py` ④ 段）。asm 里手工加注释**不会**进入重生成产物 ⇒
    若把卡值同步成"带注释文件"的 sha，全库必然 `refute:sha256_mismatch`
    （2026-08-14 实测：EV-CONC-001 期望 3d6f55e6… vs 实际 8dd19bc6…）。
    故卡值保持"生成产物"的 sha；版本绑定改用**卡字段 vs asm 注释**直接比对
    （gate 规则 `EV-ARTIFACT-VERSION-MATCH`，比 sha 间接绑定更直接）。

工程约束：**字节级**读写（沿用原文件行尾），幂等（已 stamp 则跳过），默认 dry-run。
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from utf8_console import ensure_utf8

ROOT = Path(__file__).resolve().parent.parent
ASM_DIR = ROOT / "Examples" / "atoms"
EVIDENCE = ROOT / "evidence"
VERSION = 1
_ASM_STAMP = re.compile(rb"^;?\s*artifact_version:\s*(\d+)", re.M)
_CARD_STAMP = re.compile(rb"^artifact_version:\s*(\d+)", re.M)


def _eol(raw: bytes) -> bytes:
    i = raw.find(b"\n")
    return b"\r\n" if i > 0 and raw[i - 1:i] == b"\r" else b"\n"


def stamp_asm(path: Path, apply: bool) -> str:
    raw = path.read_bytes()
    head = raw[:200]
    if _ASM_STAMP.match(head) or _ASM_STAMP.search(head):
        return "skip"
    if apply:
        path.write_bytes(f"; artifact_version: {VERSION}".encode() + _eol(raw) + raw)
    return "add"


def _fm_segment(raw: bytes) -> bytes:
    """frontmatter 段（首个 `---` 到下一个行首 `---`）——幂等检查必须看整段。

    踩坑实录（498 任务 2）：首版只查 `raw[:2000]`，7 张 frontmatter >2000B 的长卡
    （EV-CONC-001/002、EV-LANG-001/002、EV-MEM-038/043/045）被**重复插入**该字段 ⇒
    gate 的 `EV-FM-DUP-KEY`（重复顶层键）会判 block。修法：按段查 + 提供 `--dedupe` 清理。
    """
    if not raw.lstrip(b"\xef\xbb\xbf").startswith(b"---"):
        return raw
    end = raw.find(b"\n---", 3)
    return raw[:end] if end > 0 else raw


def stamp_card(path: Path, apply: bool) -> str:
    raw = path.read_bytes()
    if b"artifact:" not in raw:
        return "no-artifact"
    if _CARD_STAMP.search(_fm_segment(raw)):
        return "skip"
    eol = _eol(raw)
    line = f"artifact_version: {VERSION}".encode() + eol
    # 插在 `artifact:` 行之后（保持字段邻近，便于阅读）；找不到则插在 frontmatter 末尾
    m = re.search(rb"^artifact:[^\r\n]*" + re.escape(eol), raw, re.M)
    if m:
        new = raw[:m.end()] + line + raw[m.end():]
    else:
        fm_end = raw.find(b"---", 3)
        new = raw[:fm_end] + line + raw[fm_end:] if fm_end > 0 else raw
    if apply:
        path.write_bytes(new)
    return "add"


def dedupe_cards(apply: bool) -> int:
    """删除重复的 `artifact_version:` 行（保留首个）——幂等 bug 的清理通道。"""
    n = 0
    for p in sorted(EVIDENCE.rglob("EV-*.md")):
        raw = p.read_bytes()
        if raw.count(b"artifact_version:") <= 1:
            continue
        eol = _eol(raw)
        seen = False
        out: list[bytes] = []
        for ln in raw.split(eol):
            if ln.startswith(b"artifact_version:"):
                if seen:
                    continue          # 丢弃重复行（保留首个）
                seen = True
            out.append(ln)
        n += 1
        print(f"[DEDUP] {p.relative_to(ROOT).as_posix()} "
              f"（{raw.count(b'artifact_version:')} -> 1）")
        if apply:
            p.write_bytes(eol.join(out))
    return n


def main(argv: list[str] | None = None) -> int:
    ensure_utf8()
    ap = argparse.ArgumentParser(description="工件-卡版本号迁移（498 任务 2）")
    ap.add_argument("--apply", action="store_true", help="实际写入（默认 dry-run）")
    ap.add_argument("--target", choices=["asm", "cards", "both"], default="both")
    ap.add_argument("--dedupe", action="store_true",
                    help="只清理重复的 artifact_version 行（幂等 bug 的清理通道）")
    a = ap.parse_args(argv)
    if a.dedupe:
        n = dedupe_cards(a.apply)
        print(f"\n[stamp] DEDUPE {'APPLY' if a.apply else 'DRY-RUN'}：{n} 份含重复行")
        return 0

    added = skipped = 0
    if a.target in ("asm", "both"):
        for p in sorted(ASM_DIR.rglob("*.asm")):
            r = stamp_asm(p, a.apply)
            if r == "add":
                added += 1
                print(f"[ASM  +] {p.relative_to(ROOT).as_posix()}")
            else:
                skipped += 1
    if a.target in ("cards", "both"):
        for p in sorted(EVIDENCE.rglob("EV-*.md")):
            r = stamp_card(p, a.apply)
            if r == "add":
                added += 1
                print(f"[CARD +] {p.relative_to(ROOT).as_posix()}")
            elif r == "skip":
                skipped += 1
    print(f"\n[stamp] {'APPLY' if a.apply else 'DRY-RUN'}（target={a.target}）："
          f"新增 {added} · 跳过 {skipped}"
          f"（sha256 未改动——见模块 docstring 的机制说明）")
    if not a.apply:
        print("[stamp] 这是 dry-run；确认后加 --apply")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
