#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""evidence_cmd_redirect_668.py — 668 P2-5：修掉证据卡里"用 shell 重定向"的命令写法。

问题（666 slow 三分类登记、667 结转）
=====================================
648 批写下的 10 张证据卡，命令块最后一行是：

    build/c648/_c_decay.exe > Examples/atoms/_c_decay.out

而 `atom_evidence_replay.py` 的**安全设计**是：命令里出现管道/重定向/通配/变量 ⇒ 直接判
`refute:unsupported_shell`（rc=127，不猜、不交给 shell）。于是这 10 张卡在重放里恒红 ——
**红的不是证据，是写法**。

本批定的口径（二选一，选前者）
==============================
* **改记录写法**：把"让 shell 去捕获 stdout"改成"让**运行器**去捕获" ——
  运行器本来就抓子进程的 stdout，并与卡里的 `expected.run` / `run_match_file` 比对。
  所以重定向那一截是**冗余**的，删掉即等价，且不再触碰 shell 特性。
* （不选）让运行器支持 `>`：那要给一个"只读门禁"开一个 shell 解析口子，安全代价不划算。

零越界保证
==========
只改 `command:` 块里**以 `.exe >` 结尾**的那一行；`fixture` / `artifact` / `artifact_sha256` /
`expected` / `actual` 等字段**一字不动**（否则就是在改证据而不只是改写法）。
`Examples/atoms/*.out` 是受控产物，**本工具不写**。

用法
====
    python tools/evidence_cmd_redirect_668.py --check    # 只读：列出将改的行
    python tools/evidence_cmd_redirect_668.py --apply    # 就地改写法
    python tools/evidence_cmd_redirect_668.py --report   # 写 data/668_evidence_redirect.{json,md}
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

OUT_JSON = os.path.join(ROOT, "data", "668_evidence_redirect.json")
OUT_MD = os.path.join(ROOT, "data", "668_evidence_redirect.md")

#: 只匹配"可执行文件 + 重定向到文件"这种形态；`2>&1`、管道、`$( )` 等一律不动（交人）。
_REDIR_RE = re.compile(r"^(?P<indent>\s*)(?P<exe>[^\s|;&()$<>]+\.exe)\s*>\s*(?P<out>[^\s|;&()$<>]+)\s*$")


def cards() -> list[str]:
    out: list[str] = []
    for r, _d, fs in os.walk(os.path.join(ROOT, "evidence")):
        out += [os.path.join(r, f) for f in fs if f.endswith(".md")]
    return sorted(out)


def scan() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for p in cards():
        rel = os.path.relpath(p, ROOT).replace(os.sep, "/")
        text = open(p, encoding="utf-8").read()
        for i, ln in enumerate(text.splitlines(), start=1):
            m = _REDIR_RE.match(ln)
            if m:
                rows.append({"card": rel, "line": i, "before": ln.strip(),
                             "after": m.group("exe"), "out": m.group("out")})
    return rows


def apply() -> int:
    n_files = n_lines = 0
    for p in cards():
        text = open(p, encoding="utf-8").read()
        nl = "\r\n" if "\r\n" in text else "\n"
        lines = text.split(nl)
        changed = False
        for i, ln in enumerate(lines):
            m = _REDIR_RE.match(ln)
            if m:
                lines[i] = m.group("indent") + m.group("exe")
                changed = True
                n_lines += 1
        if changed:
            with open(p, "w", encoding="utf-8", newline=nl) as fh:
                fh.write(nl.join(lines))
            n_files += 1
            print(f"[ev668] 改写法 {os.path.relpath(p, ROOT)}")
    print(f"[ev668] 共 {n_files} 张卡 / {n_lines} 行")
    return n_lines


def render_md(d: dict[str, Any]) -> str:
    lines = [
        "# 668 · 证据卡命令写法修复（shell 重定向 → 运行器捕获）",
        "",
        "> 由 `python tools/evidence_cmd_redirect_668.py --report` 生成，**禁止手改**。",
        "",
        f"待修（`--check` 时）：**{d['pending']}** 处 / 共 {d['cards_scanned']} 张证据卡。",
        "",
        "## 口径（为什么删而不是让运行器支持 `>`）",
        "",
        "`atom_evidence_replay.py` **拒绝**含管道/重定向/通配/变量的命令（`refute:unsupported_shell`，rc=127）。",
        "运行器本身就会捕获子进程 stdout 并与卡里的 `expected.run` / `run_match_file` 比对，",
        "所以 shell 重定向是**冗余**的一截；删掉它 ⇒ 命令可跑、语义不变。",
        "另一条路（放开 `>`）等于给只读门禁开一个 shell 解析口，安全代价不划算 ⇒ **不选**。",
        "",
        "## 逐条",
        "",
        "| 卡 | 行 | 改前 | 改后 |",
        "|---|---:|---|---|",
    ]
    for r in d["rows"]:
        lines.append(f"| `{r['card']}` | {r['line']} | `{r['before']}` | `{r['after']}` |")
    lines += [
        "",
        "## 边界",
        "",
        "- 只动 `command:` 块里形如 `<exe> > <file>` 的行；`fixture` / `artifact_sha256` / `expected` / `actual` **一字不动**。",
        "  （改证据本身与改写写法是两件事；本工具只做后者。）",
        "- 形如 `2>&1` / 管道 / `$( )` 的其他 shell 特性**不在此列**，遇则交人。",
        "- `Examples/atoms/*.out` 是受控产物，本工具**不写**；它仍是 `run_match_file` 的比对基准。",
    ]
    return "\n".join(lines) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="668 P2-5 · 证据卡命令写法修复")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--report", action="store_true")
    a = ap.parse_args(argv)

    if a.apply:
        apply()
        return 0

    rows = scan()
    from collections import Counter
    per_card = Counter(r["card"] for r in rows)
    d = {"schema": "queyi-evidence-redirect/668", "generated_by":
         "tools/evidence_cmd_redirect_668.py",
         "rule": "删掉冗余的 shell 重定向；运行器自己捕获 stdout 并与 expected.run 比对",
         "cards_scanned": len(cards()), "pending": len(rows),
         "cards_affected": sorted(per_card), "rows": rows}

    if a.report:
        os.makedirs(os.path.dirname(OUT_JSON), exist_ok=True)
        with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(d, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(render_md(d))
        print(f"[ev668] 已写 {os.path.relpath(OUT_JSON, ROOT)} / {os.path.relpath(OUT_MD, ROOT)}")
        print(f"[ev668] 待修 {d['pending']} 处，涉及 {len(per_card)} 张卡")
        return 0

    for r in rows:
        print(f"  {r['card']}:{r['line']}  {r['before']}  →  {r['after']}")
    print(f"[ev668] --check：待修 {len(rows)} 处 / {len(per_card)} 张卡（扫描 {d['cards_scanned']} 张）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
