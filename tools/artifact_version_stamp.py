#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""artifact_version_stamp.py — 工件-卡版本号迁移（498 任务 2，**台账方案**）。

⚠️ 为什么用台账而不是"给 .asm 加注释"（本轮实测教训，勿回退）
=============================================================
最初按 498 §2.1 给 51 个 `.asm` 首行插 `; artifact_version: 1`，结果撞上**第二处字节契约**：
`writer_selfcheck.py` 的 `WC-01 artifact_same_generation` 校验的是「**磁盘工件 sha256 == 卡值**」，
而 replay 校验的是「**重生成产物 sha256 == 卡值**」（`删旧工件 → 重跑生成命令 → 比对`）。
加注释后：磁盘 sha 变、重生成产物不变 ⇒ WC-01 全库 fail（实测 56/56）。
若反向同步卡值 ⇒ replay 全库 `refute:sha256_mismatch`（实测 EV-CONC-001）。
**两个契约同时成立 ⇒ 工件字节不可改**；版本号必须走旁路载体 ⇒ 本工具改用**台账**：

    Examples/atoms/artifact_versions.json     {"Examples/atoms/_x.asm": 1, ...}

做两件事（可分开）：
  --target ledger ：为 `Examples/atoms/*.asm` 建立/补齐版本台账（已登记的保留其版本值）
  --target cards  ：给证据卡 frontmatter 插 `artifact_version: 1`（有 `artifact:` 字段的卡）
  --target both   ：两者都做（默认）

另保留 `--dedupe`：清理历史上被重复插入的 `artifact_version` 卡字段（幂等 bug 的清理通道）。
字节级读写、默认 dry-run。
"""
from __future__ import annotations

import sys

import argparse
import json
import re
from pathlib import Path

from utf8_console import ensure_utf8

ROOT = Path(__file__).resolve().parent.parent
ASM_DIR = ROOT / "Examples" / "atoms"
LEDGER = ASM_DIR / "artifact_versions.json"
EVIDENCE = ROOT / "evidence"
VERSION = 1
_CARD_STAMP = re.compile(rb"^artifact_version:\s*(\d+)", re.MULTILINE)


def _eol(raw: bytes) -> bytes:
    i = raw.find(b"\n")
    return b"\r\n" if i > 0 and raw[i - 1:i] == b"\r" else b"\n"


def _fm_segment(raw: bytes) -> bytes:
    """frontmatter 段——幂等检查必须看整段（首版只看前 2000 字节 ⇒ 7 张长卡被重复插入）。"""
    if not raw.lstrip(b"\xef\xbb\xbf").startswith(b"---"):
        return raw
    end = raw.find(b"\n---", 3)
    return raw[:end] if end > 0 else raw


def load_ledger() -> dict:
    if not LEDGER.is_file():
        return {}
    try:
        d = json.loads(LEDGER.read_text(encoding="utf-8"))
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def stamp_ledger(apply: bool) -> tuple[int, int]:
    """返回 (added, kept)。已有条目保留原版本值（不覆盖人工递增过的版本）。"""
    data = load_ledger()
    added = kept = 0
    for p in sorted(ASM_DIR.rglob("*.asm")):
        key = p.relative_to(ROOT).as_posix()
        if key in data:
            kept += 1
        else:
            data[key] = VERSION
            added += 1
    if apply:
        LEDGER.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n",
                          encoding="utf-8")
    return added, kept


def stamp_card(path: Path, apply: bool) -> str:
    raw = path.read_bytes()
    if b"artifact:" not in raw:
        return "no-artifact"
    if _CARD_STAMP.search(_fm_segment(raw)):
        return "skip"
    eol = _eol(raw)
    line = f"artifact_version: {VERSION}".encode() + eol
    m = re.search(rb"^artifact:[^\r\n]*" + re.escape(eol), raw, re.MULTILINE)
    if m:
        new = raw[:m.end()] + line + raw[m.end():]
    else:
        fm_end = raw.find(b"---", 3)
        new = raw[:fm_end] + line + raw[fm_end:] if fm_end > 0 else raw
    if apply:
        path.write_bytes(new)
    return "add"


def dedupe_cards(apply: bool) -> int:
    """删除重复的 `artifact_version:` 行（保留首个）。"""
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
                    continue
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
    ap = argparse.ArgumentParser(description="工件-卡版本号迁移（498 任务 2，台账方案）")
    ap.add_argument("--apply", action="store_true", help="实际写入（默认 dry-run）")
    ap.add_argument("--target", choices=["ledger", "cards", "both"], default="both")
    ap.add_argument("--dedupe", action="store_true", help="只清理重复的卡字段")
    a = ap.parse_args(argv)
    if a.dedupe:
        n = dedupe_cards(a.apply)
        print(f"\n[stamp] DEDUPE {'APPLY' if a.apply else 'DRY-RUN'}：{n} 份含重复行")
        return 0

    if a.target in ("ledger", "both"):
        added, kept = stamp_ledger(a.apply)
        print(f"[stamp] 台账 {'写入' if a.apply else 'dry-run'}：新增 {added} · 保留 {kept}"
              f" → {LEDGER.relative_to(ROOT).as_posix()}")
    if a.target in ("cards", "both"):
        added = skipped = 0
        for p in sorted(EVIDENCE.rglob("EV-*.md")):
            r = stamp_card(p, a.apply)
            if r == "add":
                added += 1
                print(f"[CARD +] {p.relative_to(ROOT).as_posix()}")
            elif r == "skip":
                skipped += 1
        print(f"[stamp] 卡字段 {'写入' if a.apply else 'dry-run'}：新增 {added} · 跳过 {skipped}")
    if not a.apply:
        print("[stamp] 这是 dry-run；确认后加 --apply")
    return 0

if "--check" in sys.argv:
    print("OK: artifact_version_stamp --check（只读：加载即校验，不执行任何业务逻辑）")
    sys.exit(0)

if __name__ == "__main__":
    raise SystemExit(main())
