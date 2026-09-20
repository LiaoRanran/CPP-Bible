#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""backup.py — 关键数据自动备份 + 一键恢复（508 任务7）。

为什么（497/508）：本仓的"运行时状态"散在几处非书档案里——质量基线
（`tools/golden_state.json`）、度量序列（`data/metrics.jsonl`）、知识图谱
（`data/knowledge_graph.db`）、工件台账（`Examples/atoms/artifact_versions.json`）。
它们**都不在 git 里**（或被 gitignore），一次误删/误 sync 就永久丢失
（`golden_lock sync --accept` 会直接改写基线，属高危操作）。备份是这条链上唯一的安全网。

设计要点
========
* **白名单制**：只备份显式列出的文件，不做整目录递归——备份的价值在"能一眼看清备了什么"。
* **缺失不报错**：白名单里允许有"尚未产生"的文件（如 `data/golden_state.json` 在本仓
  并不存在），`snapshot` 记 `skipped` 而非失败。
* **每份带 MANIFEST**：记录相对路径 + 字节数 + sha256 + 源文件 mtime，
  让"恢复的是不是当时那份"可校验（只靠文件名无法回答这个问题）。
* **restore 不删原件**：覆盖前把现有文件另存为 `.bak`（同一目录），
  恢复动作本身也必须可回退。
* `cleanup` 保留最近 N 份（默认 10），更老的删——**只删自己产的目录**（前缀校验）。

用法
====
    python tools/backup.py snapshot          # 建一份备份
    python tools/backup.py list              # 列出所有备份（含文件数/时间）
    python tools/backup.py restore <dir|latest>
    python tools/backup.py cleanup [--keep 10]

`cppbible.py check --stage quality` 的最后一步会自动 `snapshot()`（失败不影响门禁）。
"""
# mypy: ignore-errors
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BACKUPS = ROOT / "data" / "backups"
MANIFEST = "MANIFEST.json"

# 白名单（508 任务7 指定）：存在则备份，缺则记 skipped。
WHITELIST = (
    "data/golden_state.json",
    "data/metrics.jsonl",
    "data/knowledge_graph.db",
    "Examples/atoms/artifact_versions.json",
    "tools/golden_state.json",
)


def _sha256(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def snapshot(base: Path | None = None, *, tag: str | None = None) -> Path:
    """建一份备份目录，返回其路径（缺失的白名单项记入 manifest.skipped）。"""
    root = base or BACKUPS
    d = root / (tag or time.strftime("%Y-%m-%d-%H%M%S"))
    d.mkdir(parents=True, exist_ok=True)
    files: list[dict] = []
    skipped: list[str] = []
    for rel in WHITELIST:
        src = ROOT / rel
        if not src.is_file():
            skipped.append(rel)
            continue
        dst = d / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        st = src.stat()
        files.append({"path": rel, "bytes": st.st_size, "sha256": _sha256(src),
                      "mtime": time.strftime("%Y-%m-%dT%H:%M:%S",
                                             time.localtime(st.st_mtime))})
    (d / MANIFEST).write_text(json.dumps(
        {"schema": "cppbible-backup/1.0",
         "created": time.strftime("%Y-%m-%dT%H:%M:%S"),
         "root": str(ROOT), "files": files, "skipped": skipped},
        ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return d


def list_backups(base: Path | None = None) -> list[dict]:
    """列出所有备份（新→旧）。无 manifest 的目录也列出（标 manifest=False）。"""
    root = base or BACKUPS
    if not root.is_dir():
        return []
    out = []
    for d in sorted((p for p in root.iterdir() if p.is_dir()), reverse=True):
        man = d / MANIFEST
        info: dict = {"dir": d.name, "manifest": man.is_file(), "files": None,
                      "skipped": None, "created": None}
        if man.is_file():
            try:
                m = json.loads(man.read_text(encoding="utf-8"))
                info["files"] = len(m.get("files") or [])
                info["skipped"] = len(m.get("skipped") or [])
                info["created"] = m.get("created")
            except ValueError:
                info["manifest"] = False
        out.append(info)
    return out


def resolve(target: str, base: Path | None = None) -> Path:
    """`latest` ⇒ 最新一份备份目录；否则按名字解析（也接受完整路径）。"""
    root = base or BACKUPS
    if target in ("latest", ""):
        bs = [b for b in list_backups(root)]
        if not bs:
            raise SystemExit("[backup] 没有任何备份可恢复")
        return root / bs[0]["dir"]
    p = Path(target)
    if p.is_dir():
        return p
    cand = root / target
    if cand.is_dir():
        return cand
    raise SystemExit(f"[backup] 找不到备份目录：{target}")


def restore(target: str, base: Path | None = None) -> dict:
    """从备份恢复白名单文件；**覆盖前把现有文件另存为 `.bak`**（不删原件）。"""
    d = resolve(target, base)
    man = d / MANIFEST
    if not man.is_file():
        raise SystemExit(f"[backup] {d.name} 缺 {MANIFEST}，拒绝盲恢复")
    m = json.loads(man.read_text(encoding="utf-8"))
    restored, backed, missing = [], [], []
    for item in m.get("files") or []:
        rel = str(item.get("path") or "")
        src = d / rel
        if not rel or not src.is_file():
            missing.append(rel)
            continue
        dst = ROOT / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if dst.is_file():
            bak = dst.with_suffix(dst.suffix + ".bak")
            shutil.copy2(dst, bak)                 # 覆盖前留退路
            backed.append(str(bak.relative_to(ROOT).as_posix()))
        shutil.copy2(src, dst)                     # copy2：保留 mtime
        restored.append(rel)
    return {"dir": d.name, "restored": restored, "kept_bak": backed,
            "missing_in_backup": missing}


def cleanup(keep: int = 10, base: Path | None = None) -> list[str]:
    """保留最近 keep 份，删更老的。**只删自己产的目录**（有 manifest 或名为日期）。"""
    root = base or BACKUPS
    if not root.is_dir():
        return []

    def _is_tool_backup(p: Path) -> bool:
        """本工具产物 = 有 MANIFEST，或名为 YYYY-MM-DD-HHMMSS（两次 `-` 且各段是数字）。"""
        if (p / MANIFEST).is_file():
            return True
        parts = p.name.split("-")
        return len(parts) == 3 and all(s.isdigit() for s in parts)

    # **先过滤再计数**：外来目录既不删也不占"保留名额"（508 首版先计数后跳过 ⇒
    # 外来目录占了 slot 0，导致多删了一份本该保留的备份）。
    dirs = sorted((p for p in root.iterdir() if p.is_dir() and _is_tool_backup(p)),
                  reverse=True)
    removed = []
    for d in dirs[keep:]:
        shutil.rmtree(d, ignore_errors=True)
        removed.append(d.name)
    return removed


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="关键数据备份/恢复（508 任务7）")
    sub = ap.add_subparsers(dest="cmd")
    sub.add_parser("snapshot", help="建一份备份")
    sub.add_parser("list", help="列出备份")
    r = sub.add_parser("restore", help="从备份恢复（默认 latest）")
    r.add_argument("dir", nargs="?", default="latest")
    c = sub.add_parser("cleanup", help="保留最近 N 份")
    c.add_argument("--keep", type=int, default=10)
    ap.add_argument("--base", default=None, help="覆盖备份根目录（测试用）")
    a = ap.parse_args(argv)
    base = Path(a.base) if a.base else None

    if a.cmd in (None, "snapshot"):
        d = snapshot(base)
        m = json.loads((d / MANIFEST).read_text(encoding="utf-8"))
        print(f"[backup] 备份完成：{d.relative_to(ROOT).as_posix() if base is None else d}"
              f"（{len(m['files'])} 文件"
              + (f"，跳过 {len(m['skipped'])} 个不存在项" if m["skipped"] else "") + "）")
        for it in m["files"]:
            print(f"   {it['bytes']:>10}B  {it['path']}")
        for sk in m["skipped"]:
            print(f"   {'(skip)':>10}  {sk}")
        return 0
    if a.cmd == "list":
        rows = list_backups(base)
        if not rows:
            print("[backup] 暂无备份")
            return 0
        for b in rows:
            print(f"   {b['dir']}  文件 {b['files']}  跳过 {b['skipped']}  "
                  f"created {b['created']}" + ("" if b["manifest"] else "  [无 manifest]"))
        return 0
    if a.cmd == "restore":
        res = restore(a.dir, base)
        print(f"[backup] 已从 {res['dir']} 恢复 {len(res['restored'])} 个文件：{res['restored']}")
        if res["kept_bak"]:
            print(f"   覆盖前的原件已另存：{res['kept_bak']}")
        if res["missing_in_backup"]:
            print(f"   备份内缺失（未恢复）：{res['missing_in_backup']}")
        return 0
    if a.cmd == "cleanup":
        rm = cleanup(a.keep, base)
        print(f"[backup] 清理 {len(rm)} 份旧备份：{rm}")
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
