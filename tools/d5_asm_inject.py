#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""d5_asm_inject.py — 把生成的 D5.5 汇编实证小节插入章节 D5 附录末尾。

D5 附录是四段结构（D5.1-D5.4）。本工具在 D5.4「方法学注」小节之后、下一个
顶层 `## ` 节之前插入 `### D5.5 汇编实证 (GCC 15.3.0)` 小节，使 D5 名副其实地
成为「汇编证据附录」。插入位置保证不破坏 D5.1-D5.4 结构与 D5.3 恰好 1 个 cpp
demo 的约定（D5.5 用 ```asm 围栏，不影响 cpp 计数）。

幂等：章节已含 '### D5.5' 则跳过。

用法
====
  python tools/d5_asm_inject.py --chapter Book/.../chXX.md --block _d5_asm_chXX.md
"""
import argparse
import sys
from pathlib import Path


def main():
    ap = argparse.ArgumentParser(description="插入 D5.5 汇编实证小节")
    ap.add_argument("--chapter", required=True, help="目标章节 md")
    ap.add_argument("--block", required=True, help="D5.5 小节 markdown 文件")
    ap.add_argument("--anchor", default="方法学注",
                    help="在其后、下一个 ## 前插入（默认 D5.4 方法学注）")
    a = ap.parse_args()

    ch = Path(a.chapter)
    block = Path(a.block)
    if not ch.exists():
        print(f"[ERR] 章节不存在: {ch}")
        return 1
    if not block.exists():
        print(f"[ERR] 小节文件不存在: {block}")
        return 1

    text = ch.read_text(encoding="utf-8")
    if "### D5.5" in text:
        print(f"SKIP {ch}: 已含 D5.5")
        return 0

    lines = text.split("\n")
    mi = [i for i, l in enumerate(lines)
          if l.startswith("###") and a.anchor in l]
    if not mi:
        print(f"[ERR] 找不到含 '{a.anchor}' 的小节: {ch}")
        return 1
    start = mi[0]
    nxt = [i for i in range(start + 1, len(lines)) if lines[i].startswith("## ")]
    ins = nxt[0] if nxt else len(lines)

    blk = "\n" + block.read_text(encoding="utf-8").rstrip("\n") + "\n"
    new = lines[:ins] + blk.split("\n") + lines[ins:]
    # newline="\n" 保持与仓库一致的 LF，避免 Windows 默认把 \n 写成 \r\n 导致全文 diff
    ch.write_text("\n".join(new), encoding="utf-8", newline="\n")
    print(f"OK   {ch}: 插入 D5.5 @L{ins}（共 {len(new)-len(lines)} 行）")
    return 0


if __name__ == "__main__":
    sys.exit(main())
