#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""C++ 主程序块编译告警扫描 (#201 深度功能正确性信号)。

对 Book/**/ch*.md 中所有含 `int main` 的 cpp 块，分别用
    g++ -std=c++23 -O0 -fsyntax-only -Wall -Wextra -Wpedantic
编译（仅语法+警告，不链接不运行），按告警类型归类计数，并保留样本定位。

设计：
  * 仅扫描 int main 块（自包含可编译），避免把教学片段的大量预期告警淹没信号。
  * 已排除「教学性错误示例」（前置 prose / 块内注释含 错误/UB/undefined 等标记），
    这些块的告警是刻意演示，不计缺陷。
  * 输出 tools/audit_cpp_warnings.json + 汇总打印。
用法：python tools/audit_cpp_warnings.py
"""
from __future__ import annotations
import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
BOOK = REPO / "Book"
OUT = REPO / "tools" / "audit_cpp_warnings.json"
GCC = r"C:/Qt/Tools/mingw1530_64/bin/g++.exe"

FENCE_RE = re.compile(r"^```(cpp|c\+\+)\s*(.*)$", re.MULTILINE)
END_RE = re.compile(r"^```\s*$", re.MULTILINE)
ERROR_MARKERS = re.compile(
    r"(错误|UB|undefined\s*behavior|ill[- ]?formed|编译失败|无法编译|反例|错误示范|"
    r"should\s+not|won't\s+compile|does\s+not\s+compile|bug|缺陷|未定义|悬垂|泄漏|越界)",
    re.IGNORECASE,
)
IN_BLOCK_ERROR = re.compile(r"//\s*(错误|UB|undefined|ill-formed|反例|bad|wrong)|/\*\s*(错误|UB|bad|wrong)")
INTENT_OK_MAIN = re.compile(r"\bint\s+main\s*\(")

# 告警类型 -> 正则
WARN_KINDS = {
    "unused_variable": re.compile(r"-Wunused(-variable|-but-set-variable)?"),
    "sign_compare": re.compile(r"-Wsign-compare"),
    "unused_parameter": re.compile(r"-Wunused-parameter"),
    "reorder": re.compile(r"-Wreorder"),
    "parentheses": re.compile(r"-Wparentheses"),
    "narrowing": re.compile(r"-Wnarrowing"),
    "conversion": re.compile(r"-Wconversion"),
    "maybe_uninitialized": re.compile(r"-Wmaybe-uninitialized|-Wuninitialized"),
    "format": re.compile(r"-Wformat"),
    "old_style_cast": re.compile(r"-Wold-style-cast"),
    "unused_function": re.compile(r"-Wunused-function"),
    "comment": re.compile(r"-Wcomment"),
    "unknown_pragmas": re.compile(r"-Wunknown-pragmas"),
}


def extract_blocks(path: Path):
    text = path.read_text(encoding="utf-8", errors="replace")
    lines = text.split("\n")
    out = []
    i, n = 0, len(lines)
    while i < n:
        m = FENCE_RE.match(lines[i])
        if m:
            start = i + 1
            j = start
            while j < n and not END_RE.match(lines[j]):
                j += 1
            code = "\n".join(lines[start:j])
            pre = "\n".join(lines[max(0, i - 3):i])
            out.append((i + 1, code, pre))
            i = j + 1
        else:
            i += 1
    return out


def is_intent_error(code: str, pre: str) -> bool:
    return bool(IN_BLOCK_ERROR.search(code) or ERROR_MARKERS.search(pre))


def main() -> int:
    files = sorted(BOOK.rglob("ch*.md"))
    compiled = 0
    skipped_didactic = 0
    skipped_nonmain = 0
    kind_counts: dict[str, int] = {k: 0 for k in WARN_KINDS}
    other = 0
    samples: dict[str, list] = {k: [] for k in WARN_KINDS}

    for f in files:
        rel = f.relative_to(REPO).as_posix()
        for (ln, code, pre) in extract_blocks(f):
            if not INTENT_OK_MAIN.search(code):
                skipped_nonmain += 1
                continue
            if is_intent_error(code, pre):
                skipped_didactic += 1
                continue
            compiled += 1
            with tempfile.NamedTemporaryFile("w", suffix=".cpp", delete=False, encoding="utf-8") as tf:
                tf.write(code)
                tmp = tf.name
            try:
                proc = subprocess.run(
                    [GCC, "-std=c++23", "-O0", "-fsyntax-only",
                     "-Wall", "-Wextra", "-Wpedantic", tmp],
                    capture_output=True, text=True, timeout=30,
                )
            except subprocess.TimeoutExpired:
                continue
            finally:
                Path(tmp).unlink(missing_ok=True)
            for wline in proc.stderr.splitlines():
                if ": warning:" not in wline:
                    continue
                matched = False
                for kind, rx in WARN_KINDS.items():
                    if rx.search(wline):
                        kind_counts[kind] += 1
                        if len(samples[kind]) < 4:
                            samples[kind].append(f"{rel}:{ln}  {wline.strip()}")
                        matched = True
                        break
                if not matched:
                    other += 1

    result = {
        "compiled_main_blocks": compiled,
        "skipped_didactic": skipped_didactic,
        "skipped_nonmain": skipped_nonmain,
        "kind_counts": kind_counts,
        "other_warnings": other,
        "samples": samples,
    }
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"编译主块={compiled}  跳过(教学错误)={skipped_didactic}  跳过(非main)={skipped_nonmain}")
    print("告警类型计数:")
    for k, v in kind_counts.items():
        print(f"  {k:20s} {v}")
    print(f"  其他告警={other}")
    print(f"\n报告已写入 {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
