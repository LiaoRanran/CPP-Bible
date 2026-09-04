#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""codeblock_style.py — 代码块版式统一工具（围栏标签 + 行尾注释对齐）。

对应 TEACHING.md §8「代码块与注释风格」的**可脚本化**两条规则：

  ① 围栏语言标签统一：可编译 C++ → ```cpp；ASCII 图/程序输出 → ```text；
     汇编 → ```asm；shell → ```bash。消除裸 ``` ``` 与同义标签混用
     （c++/C++/cpp、console/output、sh/zsh）。
  ② 行尾注释对齐：块内所有"代码 + 行尾 // 注释"行，按最长代码行（显示宽度，
     CJK 记 2）计算对齐列，代码与 // 之间补空格到该列，替换手敲空格。

不可脚本化的两条（语义判断，随深耕人工落地）：
  ③ 围栏题注 ```cpp title="示例 2 · ★★★☆☆"（见 §8.3 迁移前置条件）
  ④ 注释写法：中文注释 / 圈号①引导块用途 / 去逐行冗余注 / 标点与中英混排

安全护栏（防误伤，任何时候都生效）：
  - 只处理 ```cpp（含同义标签）块；asm / text / bash / mermaid 块原样保留
    （保护反汇编证据与 ASCII 图）。
  - 行尾 // 的判定：跳过整行注释、`///` `//!` doxygen、URL 中的 `//`、
    以及 `//` 落在字符串/字符字面量内的情况（前缀引号计数为奇）。
  - 对齐列上限 ALIGN_CAP（显示宽度）：超过则整块跳过，避免超长对齐列。
  - 字节级读写，保留 LF/CRLF 原样（Windows 上 Path.write_text 会污染行尾）。

用法：
  python tools/codeblock_style.py --check  [文件...]
  python tools/codeblock_style.py --apply  [文件...]
  python tools/codeblock_style.py --apply --titles [文件...]   # ③ 题注（默认关闭）
"""

import argparse
import pathlib
import re
import sys
from typing import Any

# --- 同义标签归一表 -------------------------------------------------------
LANG_ALIAS = {
    "cpp": "cpp", "c++": "cpp", "C++": "cpp", "cc": "cpp", "cxx": "cpp",
    "asm": "asm", "nasm": "asm", "s": "asm",
    "bash": "bash", "sh": "bash", "zsh": "bash", "shell": "bash", "console": "bash",
    "text": "text", "txt": "text", "output": "text", "plain": "text",
    "mermaid": "mermaid", "python": "python", "cmake": "cmake", "json": "json",
    "toml": "toml", "yaml": "yaml", "table": "text",
}

# 行尾注释判定的"非注释"干扰：URL 协议头
URL_RE = re.compile(r"https?://")
# 推断裸围栏语言用的信号
CPP_SIGNAL = re.compile(
    r"^\s*(#include|template\s*<|struct\s+\w+|class\s+\w+|int\s+main|void\s+\w+\s*\(|"
    r"std::|using\s+namespace|auto\s+\w+\s*=|//\s*\S|/\*)")
ASM_SIGNAL = re.compile(r"^\s*[a-z][a-z0-9.]*:|^\s{2,}(mov|lea|call|jmp|ret|push|pop|add|sub|cmp|test)\b")
TEXT_SIGNAL = re.compile(r"^\s*(\+[-=]+|[-=]{3,}|[│┌└├─┐┘┤|]|\[?\s*\d+\s*\]\s)")

ALIGN_CAP = 76  # 显示宽度上限：最长代码行超过它则整块不对齐
MIN_TRAILING = 2  # 代码与 // 之间至少的空格数


def display_width(s: str) -> int:
    """显示宽度：CJK/全角记 2，其余记 1（与 markdown_style_guard 同口径）。"""
    return sum(2 if ord(ch) > 0x2E7F else 1 for ch in s)


def split_fences(lines):
    """扫描围栏，返回 [(open_idx, close_idx, lang, body_lines)]（body 为行号区间内行）。"""
    blocks = []
    i, n = 0, len(lines)
    while i < n:
        m = re.match(r"^(\s*)```(.*)$", lines[i])
        if not m:
            i += 1
            continue
        indent, info = m.group(1), m.group(2).strip()
        lang = info.split()[0] if info else ""
        j = i + 1
        body = []
        while j < n and not re.match(r"^\s*```\s*$", lines[j]):
            body.append(lines[j])
            j += 1
        blocks.append([i, j, lang, info, body, indent])
        i = j + 1
    return blocks


def infer_lang(body):
    """按内容信号推断裸围栏语言；无法判定返回 None（保持原样，交人工）。

    安全设计（2026-09-04）：**绝不自动判 cpp**——裸围栏若真是可独立编译的 C++，
    历次深度改写后早已是 ```cpp；判 cpp 只会：(a) 让 cpp_blocks 指标漂移、
    (b) 把源码摘录送进门禁编译。故代码性裸围栏一律返回 None 交人工。
    """
    if not body:
        return None
    head = [ln for ln in body[:6] if ln.strip()]
    if not head:
        return None
    text_cue = "\n".join(head)
    # libstdc++/编译器私有实现摘录（保留标识符 _X / __x）→ 展示文本（同 LIBSTDCXX 规则）
    if re.search(r"\b_[A-Z]\w*\b|\b\w*__\w*\b", text_cue):
        return "text"
    if any(ASM_SIGNAL.match(ln) for ln in head):
        return "asm"
    # 纯文本信号：Q&A/面试/提案历程/选型速查/ASCII 图等
    if re.search(r"^(?:Q:|A:|面试|提案|N\d{4}|反模式\d|速查|选择|演进|演化|标准化|"
                 r"[│┌└├┐┘┤┼─0-9→*>#\-\+].{0,12})", text_cue, re.M):
        return "text"
    has_code = any((";" in ln) or ("{" in ln) or ("}" in ln) for ln in body)
    if has_code:
        return None
    return "text"


def trailing_comment_code(line):
    """若该行是"代码 + 行尾 // 注释"，返回 (code_part, comment_part)；否则 None。

    护栏：整行注释、`///`/`//!`、URL 中的 `//`、字符串/字符字面量内的 `//` 全部跳过。
    """
    if "//" not in line:
        return None
    stripped = line.strip()
    if stripped.startswith("//"):          # 整行注释：不参与对齐
        return None
    if stripped.startswith("///") or stripped.startswith("//!"):
        return None
    idx = line.find("//")
    if idx <= 0:
        return None
    if URL_RE.search(line[:idx + 2]) and line[idx - 1] == ":":
        return None
    prefix = line[:idx]
    # 字符串/字符字面量内的 //：前缀引号计数为奇 → 处于字面量中
    if prefix.count('"') % 2 == 1 or prefix.count("'") % 2 == 1:
        return None
    code = prefix.rstrip()
    if not code:
        return None
    return code, line[idx:]


def align_block(body):
    """对块内行尾注释对齐，返回 (new_body, changed_count)。"""
    parsed = [trailing_comment_code(ln) for ln in body]
    widths = [display_width(p[0]) for p in parsed if p]
    if len(widths) < 2:                    # 单行无需对齐
        return body, 0
    target = max(widths) + MIN_TRAILING
    if max(widths) > ALIGN_CAP:            # 过长则整块跳过
        return body, 0
    out, changed = [], 0
    for ln, p in zip(body, parsed):
        if not p:
            out.append(ln)
            continue
        code, comment = p
        comment = re.sub(r"^//\s*", "// ", comment)      # 规范化 // 后空白
        new = code + " " * (target - display_width(code)) + comment
        if new != ln:
            changed += 1
        out.append(new)
    return out, changed


def list_bare(path: pathlib.Path):
    """列出该文件所有裸围栏（``` 后无语言标签）的位置与前 3 行内容，供人工定标签。"""
    lines = path.read_text(encoding="utf-8").split("\n")
    blocks = split_fences(lines)
    for open_i, _close, lang, _info, body, _ind in blocks:
        if lang:
            continue
        head = [ln.strip() for ln in body[:4] if ln.strip()][:3]
        guess = infer_lang(body)
        print(f"{path.name}:{open_i + 1}  推断={guess or '未知'}")
        for h in head:
            print(f"      | {h[:96]}")
    return len([1 for _o, _c, lang, _i, _b, _n in blocks if not lang])


def process_file(path: pathlib.Path, apply: bool, titles: bool):
    raw = path.read_bytes()
    text = raw.decode("utf-8")
    newline = "\r\n" if b"\r\n" in raw else "\n"
    lines = text.splitlines()  # 自动剥离 \r，避免 CRLF 残留
    stats: dict[str, Any] = {"file": str(path), "tag": 0, "align": 0, "title": 0, "bare_unknown": 0}
    out = list(lines)

    blocks = split_fences(lines)
    # 倒序处理，避免行号位移影响后续替换
    for open_i, close_i, lang, info, body, indent in reversed(blocks):
        new_lang = LANG_ALIAS.get(lang, lang)
        new_info = info

        # ① 标签统一（含裸围栏推断）
        if lang == "":
            guessed = infer_lang(body)
            if guessed:
                new_lang = guessed
                new_info = guessed
            else:
                stats["bare_unknown"] += 1
        elif new_lang != lang:
            new_info = new_lang + (" " + " ".join(info.split()[1:]) if len(info.split()) > 1 else "")

        # ③ 题注（默认关闭）：只取"示例 N · 星级"，主题/徽章/版本留在正文
        if titles and new_lang == "cpp" and "title=" not in new_info:
            cap = next((out[k] for k in range(open_i - 1, max(open_i - 4, -1), -1)
                        if out[k].startswith("> **示例")), None)
            if cap:
                m = re.search(r"\*\*(示例\s*\d+)\*\*.*?难度\s*([★☆]+)", cap)
                if m:
                    new_info = f'{new_lang} title="{m.group(1)} · {m.group(2)}"'
                    stats["title"] += 1

        if new_info != info:
            stats["tag"] += 1
            out[open_i] = f"{indent}```{new_info}"

        # ② 行尾注释对齐（仅 cpp 块）
        if new_lang == "cpp":
            new_body, changed = align_block(body)
            if changed:
                stats["align"] += changed
                out[open_i + 1:close_i] = new_body

    new_text = newline.join(out)
    if not new_text.endswith(newline):
        new_text += newline
    if apply and new_text != text:
        path.write_bytes(new_text.encode("utf-8"))
    return stats


def main():
    # GBK 控制台护栏：输出含 ⚠️/中文时 UnicodeEncodeError 会中断批量处理
    if sys.stdout.encoding and sys.stdout.encoding.lower() not in ("utf-8", "utf8"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    ap = argparse.ArgumentParser(description="代码块版式统一（围栏标签 + 行尾注释对齐）")
    ap.add_argument("files", nargs="+", help="章节 .md 文件")
    ap.add_argument("--apply", action="store_true", help="写入修改（默认仅报告）")
    ap.add_argument("--titles", action="store_true", help="③ 生成围栏题注（默认关闭）")
    ap.add_argument("--list-bare", action="store_true", help="列出裸围栏位置与内容（供人工定标签）")
    args = ap.parse_args()

    total: dict[str, Any] = {"tag": 0, "align": 0, "title": 0, "bare_unknown": 0}
    for f in args.files:
        p = pathlib.Path(f)
        if not p.exists():
            p = pathlib.Path("Book") / f
        if not p.exists():
            print(f"[SKIP] 不存在: {f}")
            continue
        if args.list_bare:
            list_bare(p)
            continue
        st = process_file(p, args.apply, args.titles)
        for k in total:
            total[k] += st[k]
        flag = "FIXED" if args.apply else "CHECK"
        note = ""
        if st["bare_unknown"]:
            note = f"  ⚠️ 无法推断的裸围栏 {st['bare_unknown']} 处（需人工定标签）"
        print(f"[{flag}] {p.name}: 标签 {st['tag']} / 对齐 {st['align']} / 题注 {st['title']}{note}")
    print(f"\n汇总: 标签 {total['tag']} / 对齐 {total['align']} / 题注 {total['title']}"
          f" / 待人工定标签 {total['bare_unknown']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
