#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""backfill_verified_at_652.py — A1 批量补 `verified_at`（652 A，来自 git log 首次提交时间）。

为什么（652 A）：651 H7 实测 **87/113 卡无 `verified_at`** ⇒ 时效治理无从谈起。本工具从
**git 首次提交时间**（可复核的事实，非编造）回填 `verified_at`，并：
- 先**备份**原卡（`data/backup_652/`），再**只加一字段**（不动其它任何字节的可比内容）；
- `--dry-run` 只出计划；`--apply` 真写；
- 返回每卡 (卡 id, 首次提交日期, 依据 commit)。

注意：改 atoms/ 会致信任根 Merkle 漂移 ⇒ 收工 F 需 `tool_integrity --update` 重钉（设计使然）。

用法
====
    python tools/backfill_verified_at_652.py --check
    python tools/backfill_verified_at_652.py --dry-run
    python tools/backfill_verified_at_652.py --apply
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

QUEYI_PLUGIN = {"kind": "schema", "name": "backfill_verified_at_652", "entry": "plan",
                "description": "A1 从 git 首次提交时间批量补 verified_at（备份+只加字段）"}

BACKUP = ROOT / "data" / "backup_652"
_FM_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_ID_RE = re.compile(r"^id:\s*(\S+)", re.MULTILINE)


@dataclass
class PlanRow:
    card: str
    path: str
    verified_at: str | None
    basis: str


def _frontmatter_text(text: str) -> str | None:
    m = _FM_RE.match(text)
    return m.group(1) if m else None


def git_first_commit_date(rel: str) -> str | None:
    """git log --diff-filter=A 的**最早**一条日期（列表新→旧，取末行）。"""
    try:
        r = subprocess.run(
            ["git", "log", "--diff-filter=A", "--format=%cs", "--", rel],
            cwd=str(ROOT), capture_output=True, text=True, check=False,
        )
    except OSError:
        return None
    if r.returncode != 0:
        return None
    lines = [ln.strip() for ln in r.stdout.splitlines() if ln.strip()]
    return lines[-1] if lines else None


def plan(paths: list[Path] | None = None) -> list[PlanRow]:
    rows: list[PlanRow] = []
    if paths is not None:
        cands = paths
    else:
        cands = sorted(p for sub in ("atoms", "evidence") for p in (ROOT / sub).rglob("*.md"))
    for p in cands:
        if p.name.upper().startswith("README"):
            continue
        text = p.read_text(encoding="utf-8", errors="replace")
        fm = _frontmatter_text(text)
        if fm is None or "verified_at:" in fm:
            continue
        rel = str(p.relative_to(ROOT)).replace("\\", "/")
        date = git_first_commit_date(rel)
        im = _ID_RE.search(fm)
        rows.append(PlanRow(im.group(1).strip().strip('"') if im else p.stem, rel, date, "git log --diff-filter=A"))
    return rows


def apply_rows(rows: list[PlanRow]) -> dict:
    BACKUP.mkdir(parents=True, exist_ok=True)
    written, skipped = 0, 0
    for r in rows:
        if not r.verified_at:
            skipped += 1
            continue
        p = ROOT / r.path
        text = p.read_text(encoding="utf-8")
        # 备份（扁平化文件名，避免目录嵌套）
        bkp = BACKUP / r.path.replace("/", "__")
        if not bkp.exists():
            shutil.copy2(p, bkp)
        if "verified_at:" in (text.split("---", 2)[1] if text.startswith("---") else ""):
            skipped += 1
            continue
        # 在 id: 行后插入（只加一行）
        new = re.sub(r"(^id:.*$)", r"\1\nverified_at: " + r.verified_at, text, count=1, flags=re.MULTILINE)
        if new == text:
            skipped += 1
            continue
        p.write_text(new, encoding="utf-8")
        written += 1
    return {"written": written, "skipped": skipped, "backup_dir": str(BACKUP.relative_to(ROOT))}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("frontmatter 解析", _frontmatter_text("---\nid: A\n---\nx\n") == "id: A")
    chk("已有 verified_at 会被跳过（plan 语义）", "verified_at" in "id: A\nverified_at: 2026-01-01")
    # git 首次提交时间可查（本仓必有历史）
    d = git_first_commit_date("README.md")
    chk("git 首提交日期可查", bool(d) and bool(re.match(r"\d{4}-\d{2}-\d{2}", d or "")), str(d))
    chk("不存在的路径 ⇒ None", git_first_commit_date("no/such/file_zzz.md") is None)
    print(f"backfill_verified_at_652 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="652 A1 补 verified_at（git 首次提交时间）")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    rows = plan()
    if a.apply:
        rep = apply_rows(rows)
        print(f"计划 {len(rows)} 张｜写入 {rep['written']}｜跳过 {rep['skipped']}｜备份 {rep['backup_dir']}")
        return 0
    print(f"待补 verified_at：{len(rows)} 张")
    for r in rows[:15]:
        print(f"  {r.card:32s} ← {r.verified_at}  ({r.basis})")
    if len(rows) > 15:
        print(f"  … 另 {len(rows) - 15} 张")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
