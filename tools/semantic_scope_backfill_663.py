#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
r"""semantic_scope_backfill_663.py — 663 C1：给 26 张 verified 卡补 semantic scope。

红线：**只加 frontmatter 字段，不改正文**。插入点 = `status:` 行之后。
派生规则（诚实、宁缺勿猜）：
  - cpp_standard ← 优先 frontmatter 里对 `ISO/IEC 14882:<年>` 的引用（映射到 C++NN）；
                   次选 frontmatter 里的 `C++NN` 字样；都没有 → [unknown]
                   （**不**从正文全量匹配——那会让几乎每张卡都得到 C++11..23 全集，等于没 scope）
  - compiler    ← 卡文本里 gcc/g++/clang/clang++/msvc 命中；无命中 → [unknown]
  - platform    ← x86_64/aarch64/windows/linux/riscv64 命中；无命中 → [unknown]
  - input_domain ← frontmatter 已有 `boundary` 则引用其值；否则 "unknown"

用法：python tools/semantic_scope_backfill_663.py [--dry-run]
输出：data/semantic_scope_backfill_663.json（+ 控制台摘要）
"""
from __future__ import annotations

import argparse
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ATOMS = os.path.join(ROOT, "atoms")
OUT = os.path.join(ROOT, "data", "semantic_scope_backfill_663.json")
TARGET_STATUS = {"verified", "red-team-verified"}
FIELDS = ("cpp_standard", "compiler", "platform", "input_domain")
ISO_MAP = {"2011": "C++11", "2014": "C++14", "2017": "C++17", "2020": "C++20", "2023": "C++23"}


def _fm_block(txt):
    return re.match(r"^---\n(.*?)\n---", txt, re.DOTALL)


def derive(txt, fm_txt):
    """返回 (cpp_standard, compiler, platform)。派生不出即 ['unknown']。"""
    years = set(re.findall(r"14882:(\d{4})", fm_txt))
    std = sorted({ISO_MAP[y] for y in years if y in ISO_MAP})
    if not std:
        std = sorted({f"C++{s}" for s in re.findall(r"C\+\+(\d{2})", fm_txt)})
    cpp_standard = std or ["unknown"]

    comp = []
    for pat, name in ((r"\bgcc\b|\bg\+\+", "gcc"), (r"\bclang\b|\bclang\+\+", "clang"),
                      (r"\bmsvc\b", "msvc")):
        if re.search(pat, txt, re.IGNORECASE):
            comp.append(name)
    compiler = comp or ["unknown"]

    plat = []
    for pat, name in ((r"x86_64", "x86_64"), (r"aarch64", "aarch64"), (r"riscv64", "riscv64"),
                      (r"\bwindows\b", "windows"), (r"\blinux\b", "linux")):
        if re.search(pat, txt, re.IGNORECASE):
            plat.append(name)
    platform = plat or ["unknown"]
    return cpp_standard, compiler, platform


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    a = ap.parse_args()

    rows = []
    changed = 0
    for dp, _dn, fn in os.walk(ATOMS):
        for f in sorted(fn):
            if not f.endswith(".md") or f == "README.md":
                continue
            p = os.path.join(dp, f)
            txt = open(p, encoding="utf-8").read()
            m = _fm_block(txt)
            if not m:
                continue
            fm_txt = m.group(1)
            sm = re.search(r"^status:\s*(\S+)", fm_txt, re.MULTILINE)
            status = sm.group(1).strip() if sm else "?"
            if status not in TARGET_STATUS:
                continue
            rel = os.path.relpath(p, ROOT).replace("\\", "/")
            missing = [k for k in FIELDS if not re.search(rf"^{k}:", fm_txt, re.MULTILINE)]
            if not missing:
                rows.append({"card": rel, "status": status, "action": "skip(已齐)"})
                continue
            cpp_standard, compiler, platform = derive(txt, fm_txt)
            bm = re.search(r"^boundary:\s*(.+)$", fm_txt, re.MULTILINE)
            input_domain = bm.group(1).strip() if bm else "unknown"
            lines = [
                f"cpp_standard: [{', '.join(cpp_standard)}]",
                f"compiler: [{', '.join(compiler)}]",
                f"platform: [{', '.join(platform)}]",
                f"input_domain: {json.dumps(input_domain, ensure_ascii=False)}",
            ]
            if not a.dry_run:
                new_fm = re.sub(r"^(status:\s*\S+)$", r"\1\n" + "\n".join(lines),
                                fm_txt, count=1, flags=re.MULTILINE)
                new_txt = txt[:m.start(1)] + new_fm + txt[m.end(1):]
                open(p, "w", encoding="utf-8", newline="\n").write(new_txt)
            changed += 1
            rows.append({"card": rel, "status": status, "action": "added",
                         "cpp_standard": cpp_standard, "compiler": compiler,
                         "platform": platform, "input_domain": input_domain,
                         "needs_review": True})
    rep = {
        "schema": "queyi-semantic-scope-backfill/v1",
        "generated_at": "2026-09-28",
        "generated_by": "tools/semantic_scope_backfill_663.py",
        "mode": "dry-run" if a.dry_run else "write",
        "target_status": sorted(TARGET_STATUS),
        "cards_touched": changed,
        "rule": "只加 frontmatter 字段，不改正文；cpp_standard 优先 ISO 14882 引用；派生不出即 unknown（不猜）",
        "rows": rows,
    }
    json.dump(rep, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"{'[dry-run] ' if a.dry_run else ''}处理卡数 = {changed}")
    for r in rows:
        if r["action"] == "added":
            print(f"  {r['card']:<44} {r['cpp_standard']} {r['compiler']} {r['platform']}"
                  f"  input_domain={r['input_domain'][:30]}")
    print(f"已写 {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
