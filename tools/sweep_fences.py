#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
sweep_fences.py — 机械缺陷大扫荡（结构/渲染完整性）扫描器。

扫描 CPP-Bible 指定 part 目录下的 ch*.md，检测五类结构性缺陷：
  C1 不平衡围栏        : 文件内 ``` 围栏开闭数量非偶数（奇偶不匹配）
  C2 GCC行标记被当H1   : 未围栏的 GCC linemarker (# 0 "x" / # 1 "x") 或
                         note:/warning:/error: 编译诊断被误判为 H1
  C3 未围栏诊断输出     : shell/gdb/objdump/asm/终端输出裸奔（含 $ / < / > /
                         0x 地址 / 寄存器 / 列号 等特征）
  C4 未闭合HTML注释     : <!-- 出现但无对应 -->
  C5 空围栏            : 连续两个围栏行（中间无内容）形成空代码块

甄别规则（避免上一轮初版的相邻闭开围栏误报）：
  - C5 仅在“同一开围栏紧跟闭围栏(中间零内容)”时命中；正常“上块闭合+下块开启”
    的相邻 ``` 不报（围栏状态机处理：闭围栏后 in_fence=False，下一个开围栏
    重新开始，不触发 C5）。
  - C3 仅保留强信号：shell '$ '/gdb '(gdb)'/objdump 地址列/裸寄存器；
    丢弃 '.asm'/'.s' 文件名与 register+0x 噪声，避免散文/引用块误报。

红线：
  - 不修改以 _ 开头的文件
  - 保留原生换行（CRLF/LF 混合），仅做字节级读取
  - 脚本默认只扫描报告；不修改章节文件。

用法：
  python3 tools/sweep_fences.py [--root ROOT] [--parts p1 p2 ...]
  不带 --parts 时扫描全部 16 个 part。
"""

import os
import re
import sys

ALL_PARTS = [
    "Book/part01_history", "Book/part02_toolchain", "Book/part03_language",
    "Book/part04_memory", "Book/part05_oo", "Book/part06_templates",
    "Book/part07_stl", "Book/part08_algorithms", "Book/part09_concurrency",
    "Book/part10_modern", "Book/part11_source", "Book/part12_patterns",
    "Book/part13_engineering", "Book/part14_perf", "Book/part15_cases",
    "Book/part16_reading",
]

FENCE_RE = re.compile(r"^(\s*)(`{3,}|~{3,})")
# GCC 预处理行标记:  # 1 "file"  或  # 1 "file" 1 2 3
GCC_LINE_MARKER = re.compile(r"^#\s+\d+\s+[\"\d]")
# 裸编译诊断
DIAG_RE = re.compile(r"^(note|warning|error):")
# 终端/诊断强特征（围栏外）
SHELL_PROMPT = re.compile(r"^\$\s")
GDB_PROMPT = re.compile(r"^\(gdb\)")
ASM_ADDR = re.compile(r"^\s*0x[0-9a-fA-F]")
ASM_LABEL = re.compile(r"^<\s")
REG_LINE = re.compile(r"^\s*(rax|rbx|rcx|rdx|rsi|rdi|rsp|rbp|r[0-9]+|eax|ebx|esp|ebp)\b")
OBJ_LINE = re.compile(r"^\s*[0-9a-fA-F]+:\s+([0-9a-fA-F]{2}\s+)+")
COL_MARK = re.compile(r":\d+:\d+")  # file:line:col 常见于诊断


def split_eol(data: bytes):
    """返回 (lines: list[bytes], 是否 CRLF 主导)。按 \\n 切，去掉 \\r。"""
    if b"\r\n" in data:
        raw_lines = data.split(b"\n")
        lines = [ln[:-1] if ln.endswith(b"\r") else ln for ln in raw_lines]
        return lines, True
    return data.split(b"\n"), False


def scan_file(path: str):
    """返回该文件的缺陷列表，元素为 dict。"""
    defects = []
    with open(path, "rb") as fh:
        data = fh.read()
    lines, _ = split_eol(data)
    n = len(lines)

    in_fence = False
    fence_stack = []
    fence_count = 0

    i = 0
    while i < n:
        raw = lines[i]
        stripped = raw.strip()
        m = FENCE_RE.match(raw.decode("utf-8", "replace"))
        if m:
            fence_count += 1
            if not in_fence:
                # 开围栏
                in_fence = True
                fence_stack.append(i + 1)
                # C5：开围栏后紧跟闭围栏（中间无任何内容）=> 空围栏
                if i + 1 < n:
                    nxt = lines[i + 1].decode("utf-8", "replace")
                    if FENCE_RE.match(nxt):
                        defects.append({
                            "type": "C5", "line": i + 1,
                            "snippet": stripped.decode("utf-8", "replace")[:40],
                            "detail": "开围栏后紧跟闭围栏（空代码块）",
                        })
                        in_fence = False
                        if fence_stack:
                            fence_stack.pop()
                        fence_count += 1
                        i += 2
                        continue
            else:
                # 闭围栏
                in_fence = False
                if fence_stack:
                    fence_stack.pop()
            i += 1
            continue

        # 在围栏外才检测 C2/C3
        if not in_fence:
            text = raw.decode("utf-8", "replace")
            if GCC_LINE_MARKER.match(text):
                defects.append({
                    "type": "C2", "line": i + 1, "snippet": text[:80],
                    "detail": "GCC 预处理行标记被当 H1",
                })
            if DIAG_RE.match(text):
                defects.append({
                    "type": "C2", "line": i + 1, "snippet": text[:80],
                    "detail": "裸 note/warning/error 诊断被当 H1/正文",
                })
            is_c3 = False
            reason = ""
            if SHELL_PROMPT.match(text):
                is_c3, reason = True, "shell 提示符 $"
            elif GDB_PROMPT.match(text):
                is_c3, reason = True, "gdb 提示符 (gdb)"
            elif ASM_ADDR.match(text):
                is_c3, reason = True, "裸 0x 地址"
            elif ASM_LABEL.match(text):
                is_c3, reason = True, "裸 < 标号"
            elif REG_LINE.match(text):
                is_c3, reason = True, "裸寄存器"
            elif OBJ_LINE.match(text):
                is_c3, reason = True, "objdump 行"
            elif COL_MARK.search(text) and (
                text.startswith("In file")
                or "required from" in text
                or text.lstrip().startswith("/")
            ):
                is_c3, reason = True, "诊断列号"
            if is_c3:
                defects.append({
                    "type": "C3", "line": i + 1, "snippet": text[:80],
                    "detail": "未围栏终端/诊断: " + reason,
                })
        i += 1

    # C1: 围栏奇偶
    if fence_count % 2 != 0:
        defects.append({
            "type": "C1", "line": fence_stack[-1] if fence_stack else 1,
            "snippet": "围栏总数=%d（奇数）" % fence_count,
            "detail": "围栏开闭不平衡，后续内容被吞入代码块",
        })

    # C4: 未闭合 HTML 注释
    text_all = data.decode("utf-8", "replace")
    opens = text_all.count("<!--")
    closes = text_all.count("-->")
    if opens > closes:
        for idx, raw in enumerate(lines):
            if b"<!--" in raw and b"-->" not in raw:
                defects.append({
                    "type": "C4", "line": idx + 1,
                    "snippet": raw.decode("utf-8", "replace")[:80],
                    "detail": "未闭合 HTML 注释 (<!-- 无 -->)",
                })

    return defects


def main():
    root = os.getcwd()
    args = sys.argv[1:]
    parts = ALL_PARTS
    if "--root" in args:
        ri = args.index("--root")
        root = args[ri + 1]
    if "--parts" in args:
        pi = args.index("--parts")
        parts = args[pi + 1:]

    targets = []
    for p in parts:
        full = os.path.join(root, p)
        if not os.path.isdir(full):
            print("[warn] 目录不存在: %s" % full, file=sys.stderr)
            continue
        for fn in sorted(os.listdir(full)):
            if not fn.startswith("ch") or not fn.endswith(".md"):
                continue
            if fn.startswith("_"):
                continue
            targets.append(os.path.join(full, fn))

    total = 0
    by_type = {}
    for path in targets:
        defects = scan_file(path)
        rel = os.path.relpath(path, root)
        if defects:
            for d in defects:
                total += 1
                by_type[d["type"]] = by_type.get(d["type"], 0) + 1
                print("%s:%d:%s  %s" % (rel, d["line"], d["type"], d["detail"]))
                print("        | %s" % d["snippet"])
    print("---")
    print("扫描文件数: %d" % len(targets))
    print("缺陷总数: %d  按类: %s" % (total, by_type))


if __name__ == "__main__":
    main()
