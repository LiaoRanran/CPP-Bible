#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""holdout_merge_672h.py — 672h W3：把扩样定义幂等并入 holdout canonical。

为什么要单独一个合并器（而不是让 reveal 工具顺手改 canonical）：
    671a 复盘原话——"holdout.json 是 holdout_658.py 的产物，旧工具一跑就会把追加抹掉"。
    所以合并必须是**显式、幂等、可重跑**的一步：跑两次结果一样，且不改动已有 seed 的字段。

口径
====
* 只追加：已有 id 一律不动（防止扩样偷偷改历史标签）；
* 追加 `extend_672h` 登记节：记录来源文件、id 列表、count 变化、时间；
* `count` 字段 = len(seeds)；
* `--check`：只读校验 canonical 与扩展文件是否一致（CI/门禁用），不改盘。

用法
====
    python tools/holdout_merge_672h.py --write     # 幂等合并
    python tools/holdout_merge_672h.py --check     # 只读校验（exit 1 表示没合上）
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HOLDOUT = ROOT / "data" / "holdout" / "holdout.json"
EXT = ROOT / "data" / "holdout" / "holdout_extension_672h.json"
SECTION = "extend_672h"


def _load(p: Path) -> dict:
    data: dict = json.loads(p.read_text(encoding="utf-8"))
    return data


def merge(write: bool) -> int:
    if not HOLDOUT.is_file() or not EXT.is_file():
        print(f"[merge-672h] 缺文件：{HOLDOUT.name} 或 {EXT.name}", file=sys.stderr)
        return 1
    h, e = _load(HOLDOUT), _load(EXT)
    have = {s["id"] for s in h["seeds"]}
    added, dup = [], []
    for s in e["seeds"]:
        if s["id"] in have:
            dup.append(s["id"])
            continue
        h["seeds"].append(s)
        have.add(s["id"])
        added.append(s["id"])
    h["count"] = len(h["seeds"])
    h[SECTION] = {
        "source": "data/holdout/holdout_extension_672h.json",
        "added_ids": added or (h.get(SECTION, {}) or {}).get("added_ids", []),
        "n_added_now": len(added),
        "n_already_present": len(dup),
        "policy": e.get("caliber", {}).get("source_policy", ""),
        "generated_by": "tools/holdout_merge_672h.py（幂等：重跑不改已有 seed）",
    }
    if write:
        HOLDOUT.write_text(json.dumps(h, ensure_ascii=False, indent=1) + "\n",
                           encoding="utf-8", newline="\n")
    print(f"[merge-672h] 追加 {len(added)} 条；已在场 {len(dup)} 条；count={h['count']}")
    if added:
        print("            新增：", ", ".join(added))
    return 0


def check() -> int:
    h, e = _load(HOLDOUT), _load(EXT)
    have = {s["id"] for s in h["seeds"]}
    missing = [s["id"] for s in e["seeds"] if s["id"] not in have]
    sec = h.get(SECTION) or {}
    ok = not missing and h.get("count") == len(h["seeds"]) and bool(sec)
    print(f"[merge-672h] check: count={h.get('count')} seeds={len(h['seeds'])} "
          f"missing={missing} section={'有' if sec else '缺'}")
    print("[merge-672h] PASS" if ok else "[merge-672h] FAIL（未合上或 count 不同步）")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="672h holdout 扩样幂等合并器")
    ap.add_argument("--write", action="store_true", help="写回 holdout.json")
    ap.add_argument("--check", action="store_true", help="只读校验")
    a = ap.parse_args(argv)
    if a.check:
        return check()
    if not a.write:
        ap.print_help()
        return 2
    rc = merge(write=True)
    return rc or check()


if __name__ == "__main__":
    raise SystemExit(main())
