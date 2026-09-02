#!/usr/bin/env python3
"""tools/teaching_audit.py — 写作红线审计（报告型，离线跑）。

把 TEACHING.md 的「禁编造轶事」红线部分自动化：扫描全书中
「疑似编造轶事」的信号句式，提示人工复核。

  FABRICATED_ANECDOTE (WARN) —— 编造轶事信号句式，且既无诚实标注、也无可溯源引用键。
     信号词：据记载 / 据说 / 有传言 / 传闻 / 众所周知 / 广为流传。
     TEACHING 红线：禁止编造轶事；人文素材与事实素材同等可溯源（挂键）。
     历史事故：ch20/ch50/ch76 的「广为流传的轶事」均无出处（已清除）。

  豁免（不算编造伪装）：
    * `badge-anecdote`（轶）或 `[据记载]` / `[轶]` 自述标注——作者已诚实声明是轶事；
    * 附近（±2 行）出现可溯源引用键（[de:]/[hopl:]/[book:]/[ritchie:]/[qcon:]/
      [stepanov:]/[std-]/[cert:]/[ubsan:]/[so:] 等）——已有出处。

可靠性：
  * 跳过 ``` / ~~~ 代码围栏内的内容。
  * 误报率较高（信号词可能出现在有出处/已标注/合理口传的上下文），定位为报告型提示，
    人工复核，不进 CI。目标是「列出需人工核实的轶事」，而非「证明其编造」。

用法:
    python tools/teaching_audit.py [path] [--json|--porcelain]
默认扫描 Book/。
"""
from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys

FENCE_RE = re.compile(r"^\s*(```|~~~)")

# 编造轶事信号词
# 注：① 不含「传闻」——它常作修辞名词（「不再怕…传闻」「远小于传闻」），误报率高；
#     ② 「据说」加 (?<!证) 负向后瞻，排除「证据说明」这类「证+据说+明」的误匹配。
ANECDOTE_SIGNAL_RE = re.compile(r"(?:据记载|(?<!证)据说|有传言|众所周知|广为流传)")
# 诚实标注豁免：badge-anecdote 或 [据记载]/[轶] 自述
HONEST_MARK_RE = re.compile(r"badge-anecdote|\[据记载\]|\[轶\]")
# 可溯源引用键（有出处则豁免）
REF_KEY_RE = re.compile(
    r"\[(?:de|hopl|book|ritchie|qcon|stepanov|cert|ubsan|so|std|core|cppref)[:\-]"
)


def scan_lines(lines: list[str]) -> list[tuple[int, str, str]]:
    """扫描单个文件的行序列，返回 [(行号(1-based), 类别, 说明)]。"""
    issues: list[tuple[int, str, str]] = []
    in_fence = False

    for i, ln in enumerate(lines):
        if FENCE_RE.match(ln):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        for m in ANECDOTE_SIGNAL_RE.finditer(ln):
            signal = m.group(0)
            # 豁免窗口：该行 ±2 行
            ctx = "\n".join(lines[max(0, i - 2): i + 3])
            if HONEST_MARK_RE.search(ctx) or REF_KEY_RE.search(ctx):
                continue
            issues.append((
                i + 1,
                "FABRICATED_ANECDOTE",
                f"编造轶事嫌疑（「{signal}」无诚实标注、无引用键）——请核实出处或删除",
            ))
    return issues


def _iter_md(root: str) -> list[str]:
    if os.path.isdir(root):
        out: list[str] = []
        for r, _dirs, fs in os.walk(root):
            for fn in fs:
                if fn.endswith(".md"):
                    out.append(os.path.join(r, fn))
        return sorted(out)
    return [root]


def main() -> int:
    ap = argparse.ArgumentParser(description="写作红线审计：扫描编造轶事信号（报告型）")
    ap.add_argument("path", nargs="?", default="Book", help="扫描根（默认 Book/）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    ap.add_argument("--porcelain", action="store_true", help="机器可读：file:line:kind:msg")
    args = ap.parse_args()

    files = _iter_md(args.path)
    rows: list[dict[str, object]] = []
    for fp in files:
        with open(fp, "r", encoding="utf-8", newline="") as f:
            lines = f.read().split("\n")
        for ln, kind, msg in scan_lines(lines):
            rows.append({"file": fp, "line": ln, "kind": kind, "severity": "WARN", "msg": msg})

    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    elif args.porcelain:
        for it in rows:
            print(f"{it['file']}:{it['line']}:{it['kind']}:{it['msg']}")
    else:
        cur = ""
        for it in rows:
            fp = str(it["file"])
            if fp != cur:
                cur = fp
                n = sum(1 for x in rows if str(x["file"]) == cur)
                print(f"== {cur} ({n}) ==")
            print(f"   L{it['line']}: [{it['severity']}] {it['msg']}")
        print(
            f"\n合计 {len(rows)} 处疑似编造轶事（WARN，需人工核实），扫描 {len(files)} 文件；"
            "诚实标注(badge-anecdote)/引用键已豁免，定位为人工复核清单，不进 CI"
        )
    return 0


if __name__ == "__main__":
    # 仅对真实 TextIOWrapper 重配编码（本机 GBK 终端直接 print 中文会抛 UnicodeEncodeError）
    if isinstance(sys.stdout, io.TextIOWrapper):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    raise SystemExit(main())
