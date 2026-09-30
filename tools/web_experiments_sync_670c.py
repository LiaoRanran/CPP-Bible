#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""web_experiments_sync_670c.py — 670c A2/A4：把「仓库根数据」同步进 web/data/。

为什么需要
==========
670c 的实验结果页与判决页要 fetch 真实数据，而页面以 **web/ 为文档根**：
    python -m http.server 8765 --directory web
此时 fetch('data/baseline.json') 与 fetch('../data/baseline.json') 会被 URL
规范化成同一个 /data/baseline.json ⇒ 都指向 web/data/，仓库根那份取不到（404）。

治法不是把数字抄进页面（那就破坏了"数字可复算"），而是**复制文件**：
    data/baseline.json              -> web/data/baseline.json
    data/experiments/*.json         -> web/data/experiments/*.json
复制是幂等的、只读源、只写 web/ 下；源缺失时打印待办并**退出 0**
（670a 还没落盘 baseline_static/random 时，页面按设计显示"待670a生成"）。

用法
====
    python tools/web_experiments_sync_670c.py
    python tools/web_experiments_sync_670c.py --check   # 只报差异，不写
"""
from __future__ import annotations

import argparse
import hashlib
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
WEB_DATA = ROOT / "web" / "data"

#: (源, 目标) —— 源在仓库根，目标是页面能取到的位置
FILES = [
    (ROOT / "data" / "baseline.json", WEB_DATA / "baseline.json"),
]
#: 整目录同步
DIRS = [
    (ROOT / "data" / "experiments", WEB_DATA / "experiments"),
]


def sha256_file(p: Path) -> str:
    h = hashlib.sha256()
    with p.open("rb") as f:
        for chunk in iter(lambda: f.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def plan() -> list[dict]:
    """算出要复制什么；不改任何文件。"""
    items: list[dict] = []
    for src, dst in FILES:
        items.append({"src": src, "dst": dst})
    for src_dir, dst_dir in DIRS:
        if src_dir.is_dir():
            for src in sorted(src_dir.glob("*.json")):
                items.append({"src": src, "dst": dst_dir / src.name})
    out = []
    for it in items:
        src, dst = it["src"], it["dst"]
        if not src.is_file():
            out.append({**it, "action": "MISSING_SOURCE"})
            continue
        if dst.is_file() and sha256_file(src) == sha256_file(dst):
            out.append({**it, "action": "UP_TO_DATE"})
        elif dst.is_file():
            out.append({**it, "action": "UPDATE"})
        else:
            out.append({**it, "action": "COPY"})
    return out


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="670c：同步根数据到 web/data/（页面可 fetch）")
    ap.add_argument("--check", action="store_true", help="只报差异，不写文件")
    args = ap.parse_args(argv)

    rows = plan()
    copied = updated = same = missing = 0
    for r in rows:
        rel_src = r["src"].relative_to(ROOT) if r["src"].is_absolute() else r["src"]
        rel_dst = r["dst"].relative_to(ROOT)
        if r["action"] == "MISSING_SOURCE":
            missing += 1
            print("  [待落盘] %s 不存在 —— 页面将显示占位（670a 尚未生成）" % rel_src)
            continue
        if r["action"] == "UP_TO_DATE":
            same += 1
            print("  [已最新] %s" % rel_dst)
            continue
        if args.check:
            print("  [需同步] %s -> %s" % (rel_src, rel_dst))
            continue
        r["dst"].parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(r["src"], r["dst"])
        if r["action"] == "COPY":
            copied += 1
        else:
            updated += 1
        print("  [%s] %s -> %s" % ("复制" if r["action"] == "COPY" else "更新", rel_src, rel_dst))

    verb = "将同步" if args.check else "已同步"
    print("[web_experiments_sync_670c] 共 %d 项：%s 新增 %d / 更新 %d；已最新 %d；源缺失 %d"
          % (len(rows), verb, copied, updated, same, missing))
    return 0


if __name__ == "__main__":
    sys.exit(main())
