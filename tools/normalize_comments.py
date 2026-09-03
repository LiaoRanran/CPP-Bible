#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
normalize_comments.py — C++ 代码块注释写法规范化（机械、零语义）。

仅处理 ```cpp 围栏内的注释（不碰 asm/text/bash/裸围栏，保护反汇编证据）。

机械规则：
  R1  // 之后空白折叠为恰好一个空格（//x -> // x；//  x -> // x）
  R2  // 前若紧贴代码且无空格（code//），补一个空格（code //）
  R3  单行 /* ... */ 注释转为 //（整行或行尾；跨行块注释不动）
  R4  (--check 报告) 纯英文注释（无 CJK）计数，供人工中文化

语义规则（圈号①引导 / 去逐行冗余 / 句号 / 中英文混排）不由脚本处理，
交给逐章 deep-rewrite；脚本只做零风险、确定性的写法兜底。

红线：
  - 字节级读写，保留原文件 CRLF/LF
  - 字符串字面量（含 "http://"、R"(...)" 原始字符串）内的 // 与 /* */ 不处理
  - 不修改 asm 块（证据完整性）
  - 默认 --check 只报告；--apply 才写回

用法：
  python3 tools/normalize_comments.py --check
  python3 tools/normalize_comments.py --apply
  python3 tools/normalize_comments.py --apply --parts part07_stl part14_perf
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
CJK_RE = re.compile(r"[\u4e00-\u9fff]")


def split_eol(data: bytes):
    """返回 (lines: list[str], crlf: bool)。按 \\n 切，去掉 \\r。"""
    if b"\r\n" in data:
        raw = data.split(b"\n")
        return [ln[:-1].decode("utf-8", "replace") if ln.endswith(b"\r") else ln.decode("utf-8", "replace") for ln in raw], True
    return [ln.decode("utf-8", "replace") for ln in data.split(b"\n")], False


def locate_comment(s: str):
    """在字符串 s 中定位第一个注释。

    返回 (prefix, comment, idx)：
      - prefix: 注释前的代码文本（含其原有尾部空白，保留对齐）
      - comment: 注释原文（以 // 或 /* 开头）
      - idx: 注释起始下标
    若处于块注释跨行中（/* 无 */）返回 None。
    字符串字面量内的 // 与 /* */ 跳过。
    """
    i, n = 0, len(s)
    in_dq = in_sq = False
    while i < n:
        c = s[i]
        if in_dq:
            if c == "\\":
                i += 2
                continue
            if c == '"':
                in_dq = False
            i += 1
            continue
        if in_sq:
            if c == "\\":
                i += 2
                continue
            if c == "'":
                in_sq = False
            i += 1
            continue
        # 不在字符串内
        if c == '"':
            # 原始字符串 R"(...)delim"
            if s[i:i + 2] == 'R"' and i + 2 < n and s[i + 2] == '(':
                j = s.find(')', i + 3)
                if j != -1:
                    k = s.find('"', j)
                    if k != -1:
                        i = k + 1
                        continue
            in_dq = True
            i += 1
            continue
        if c == "'":
            in_sq = True
            i += 1
            continue
        if s[i:i + 2] == '//':
            return s[:i], s[i:], i
        if s[i:i + 2] == '/*':
            end = s.find('*/', i + 2)
            if end == -1:
                return None  # 跨行块注释，不动
            return s[:i], s[i:end + 2], i
        i += 1
    return None


def normalize_cpp_block(lines):
    """规整一个 cpp 代码块的全部行。

    返回 (out_lines, changed_count, english_count)。
    """
    out = []
    changed = 0
    english = 0
    in_block = False
    for raw in lines:
        if in_block:
            end = raw.find('*/')
            if end == -1:
                out.append(raw)
                continue
            # 块注释闭合，剩余部分正常处理
            rest = raw[end + 2:]
            in_block = False
            if rest.strip():
                nl, c, e = _normalize_rest(rest)
                out.append(raw[:end + 2] + nl)
                changed += c
                english += e
            else:
                out.append(raw)
            continue

        res = locate_comment(raw)
        if res is None:
            out.append(raw)
            continue
        prefix, comment, idx = res

        if comment.startswith('/*'):
            # 保留 doxygen 块注释 /** */、/*! */ 原样
            if comment[2:3] in ('*', '!'):
                out.append(raw)
                continue
            end = raw.find('*/', idx + 2)
            if end == -1:
                in_block = True
                out.append(raw)
                continue
            body = comment[2:-2].strip()
            if not body:
                new_comment = '//'
            else:
                new_comment = '// ' + body
                if not CJK_RE.search(body):
                    english += 1
            prefix_new = prefix + (' ' if prefix and not prefix[-1].isspace() else '')
            out.append(prefix_new + new_comment)
            changed += 1
            continue

        # // 注释（先自愈 doxygen 损坏，再保留 doxygen/Qt 风格）
        # 自愈：早期版本曾把 /// -> // / 、//! -> // !，此处还原
        if comment[:4] == '// /':
            comment = '///' + comment[4:]
        elif comment[:4] == '// !':
            comment = '//!' + comment[4:]
        # 保留 doxygen / Qt 风格（/// 、//! 、///< 、//!< 等）
        after2 = comment[2:]
        if after2 and after2[0] in ('/', '!'):
            # doxygen / Qt 风格：原样保留（写回自愈后的 comment）
            new_line = prefix + comment
            if new_line != raw:
                out.append(new_line)
                changed += 1
            else:
                out.append(raw)
            continue
        body = comment[2:]
        stripped = body.lstrip(' \t')
        if stripped:
            new_comment = '// ' + stripped
            if not CJK_RE.search(stripped):
                english += 1
        else:
            new_comment = '//'
        attached = bool(prefix) and not prefix[-1].isspace()
        prefix_new = prefix + (' ' if attached else '')
        new_line = prefix_new + new_comment
        if new_line != raw:
            out.append(new_line)
            changed += 1
        else:
            out.append(raw)
    return out, changed, english


def _normalize_rest(rest: str):
    """处理块注释闭合后的剩余文本（可能含 // 或 /* */）。"""
    res = locate_comment(rest)
    if res is None:
        return rest, 0, 0
    prefix, comment, idx = res
    if comment.startswith('/*'):
        if comment[2:3] in ('*', '!'):
            return rest, 0, 0
        end = rest.find('*/', idx + 2)
        if end == -1:
            return rest, 0, 0
        body = comment[2:-2].strip()
        new_comment = '// ' + body if body else '//'
        eng = 0 if CJK_RE.search(body) else (1 if body else 0)
        prefix_new = prefix + (' ' if prefix and not prefix[-1].isspace() else '')
        return prefix_new + new_comment, 1, eng
    if comment[:4] == '// /':
        comment = '///' + comment[4:]
    elif comment[:4] == '// !':
        comment = '//!' + comment[4:]
    after2 = comment[2:]
    if after2 and after2[0] in ('/', '!'):
        new_rest = prefix + comment
        return new_rest, (1 if new_rest != rest else 0), 0
    body = comment[2:].lstrip(' \t')
    new_comment = '// ' + body if body else '//'
    eng = 0 if CJK_RE.search(body) else (1 if body else 0)
    attached = bool(prefix) and not prefix[-1].isspace()
    prefix_new = prefix + (' ' if attached else '')
    return prefix_new + new_comment, 1, eng


def process_file(path: str, apply: bool):
    with open(path, "rb") as fh:
        data = fh.read()
    lines, crlf = split_eol(data)
    out: list[str] = []
    changed = 0
    english = 0
    in_fence = False
    fence_lang = ""
    buf: list[str] = []
    for ln in lines:
        m = FENCE_RE.match(ln)
        if m:
            if not in_fence:
                in_fence = True
                fence_lang = ln.strip()[3:].strip().lower()
                # 只处理 cpp 块
                if fence_lang == "cpp":
                    buf = []
                    out.append(ln)
                    continue
                else:
                    out.append(ln)
                    continue
            else:
                # 闭围栏
                if fence_lang == "cpp" and buf:
                    b_out, c, e = normalize_cpp_block(buf)
                    out.extend(b_out)
                    changed += c
                    english += e
                out.append(ln)
                in_fence = False
                fence_lang = ""
                buf = []
                continue
        if in_fence and fence_lang == "cpp":
            buf.append(ln)
        else:
            out.append(ln)

    if changed == 0:
        return 0, english

    if apply:
        joined = ("\r\n" if crlf else "\n").join(out)
        with open(path, "wb") as fh:
            fh.write(joined.encode("utf-8"))
    return changed, english


def main():
    args = sys.argv[1:]
    apply = "--apply" in args
    check = "--check" in args or not apply
    parts = [a for a in args if not a.startswith("--")]
    if not parts:
        parts = ALL_PARTS

    total_changed = 0
    total_english = 0
    touched_files = 0
    for part in parts:
        if not os.path.isdir(part):
            print("[warn] 目录不存在: %s" % part)
            continue
        for root, _dirs, files in os.walk(part):
            for fn in files:
                if not fn.startswith("ch") or not fn.endswith(".md"):
                    continue
                p = os.path.join(root, fn)
                c, e = process_file(p, apply)
                if c:
                    touched_files += 1
                    total_changed += c
                    total_english += e
                    if check:
                        print("  %s  +%d 行改动, %d 纯英文注" % (p, c, e))

    if check:
        print("── --check 报告 ──")
        print("  改动文件数: %d" % touched_files)
        print("  注释行改动: %d" % total_changed)
        print("  纯英文注释(待人工中文化): %d" % total_english)
        if apply is False:
            print("  （未写回；加 --apply 才落盘）")
    else:
        print("── --apply 完成 ──")
        print("  改动文件数: %d" % touched_files)
        print("  注释行改动: %d" % total_changed)
        print("  纯英文注释(待人工中文化): %d" % total_english)


if __name__ == "__main__":
    main()
