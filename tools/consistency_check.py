#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
《现代 C++ 终极圣经》一致性检查器
================================

用途：对每个章节做质量门禁检查，输出一致性报告。
这是可复制、可重复运行的工程脚本（非描述）。

用法：
    python tools/consistency_check.py                 # 自动定位 Book/ 目录
    python tools/consistency_check.py --root C:/.../CPP-Bible
    python tools/consistency_check.py --json report.json

检查项：
    1. 模板 A 20 元素覆盖（①..⑳ 标记）
    2. 禁止独立「推荐阅读」节（用户要求删除并内化）
    3. 示例数下限（整章 ```cpp 代码块 >= 阈值，默认 30）
    4. 立场分层标签 [标准]/[实现]/[平台]/[经验] 至少出现 1 次
    5. 交叉引用文件存在性（Book/... 相对路径真实存在）
    6. ASCII 框线图使用统计（INFO，不报错；Bible 允许 ASCII 图）
    7. glossary.json 合法 + chapter_ref 指向真实文件
    8. 标题编号重复检测
    9. 源码剖析是否用模板 C 风格（含「文件：」与行号标注）

退出码：0=全部通过(或无 ERROR)，1=存在 ERROR。
"""

import argparse
import json
import os
import re
import sys
from pathlib import Path

# ── 配置 ──────────────────────────────────────────────
EXPECTED_ELEMENTS = [f"{i}" for i in range(1, 21)]  # "1".."20" 匹配 ①②..⑳
BANNED_HEADINGS = ["推荐阅读", "参考文献", "延伸阅读"]
STANCE_LABELS = ["[标准]", "[实现]", "[平台]", "[经验]"]
CROSSREF_RE = re.compile(r"(?:⟶\s*|见\s*|→\s*)(Book/[^\s\)\]>。，；：、》）(（]+)")
FILE_LINK_RE = re.compile(r"`?(Book/[A-Za-z0-9_/.\-]+\.md)`?")
ASCII_BOX_RE = re.compile(r"[─│┌┐└┘├┤┬┴┼]")
CPP_BLOCK_RE = re.compile(r"^```cpp", re.MULTILINE)
HEADING_RE = re.compile(r"^#{1,6}\s+(.*)$", re.MULTILINE)
HEADING_NUM_RE = re.compile(r"^#+\s*第(\d+)章")
SRC_FILE_RE = re.compile(r"文件[:：]\s*(\S+)")
SRC_LINE_RE = re.compile(r"行号[:：]\s*(\S+)")
MIN_EXAMPLES = 30

# 废弃的 v1 老版本目录（已被 INDEX.md + v3 新章取代），不参与 v3 门禁扫描
SKIP_DIRS = {"_legacy_ModernCppBible"}


def find_book_root(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit)
    here = Path(__file__).resolve().parent
    # tools/ -> CPP-Bible/
    cand = here.parent
    if (cand / "Book").is_dir():
        return cand
    # 兜底：向上搜
    for p in [here, here.parent, here.parent.parent]:
        if (p / "Book").is_dir():
            return p
    return cand


def scan_elements(text: str) -> set[str]:
    """返回命中的 ①..⑳ 数字集合。"""
    found = set()
    for m in re.finditer(r"[①-⑳]", text):
        ch = m.group(0)
        # 圈码数字 ①=1 .. ⑳=20
        idx = "①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳".index(ch) + 1
        found.add(str(idx))
    return found


def check_chapter(path: Path, root: Path) -> dict:
    text = path.read_text(encoding="utf-8")
    rel = path.relative_to(root).as_posix()
    rep = {"file": rel, "errors": [], "warns": [], "info": []}

    # 1. 20 元素覆盖
    elems = scan_elements(text)
    missing = [e for e in EXPECTED_ELEMENTS if e not in elems]
    if missing:
        rep["warns"].append(f"模板A元素缺失: {','.join(missing)}/20")
    rep["elements_hit"] = len(elems)

    # 2. 禁止独立「推荐阅读」节（仅当标题核心即为该词，避免误伤"内化说明"标题）
    paren_re = re.compile(r"[（(].*?[)）]")
    for line in text.splitlines():
        s = line.strip()
        if not s.startswith("#"):
            continue
        core = paren_re.sub("", s)               # 去括号说明
        core = re.sub(r"^#+\s*", "", core)        # 去 #
        core = re.sub(r"^[①-⑳]\.?\s*", "", core)  # 去圈码
        core = core.strip()
        if any(core == b or core.startswith(b) for b in BANNED_HEADINGS):
            rep["errors"].append(f"发现禁止的独立节: '{s}'（应内化进正文）")
            break

    # 3. 示例数（以 ```cpp 代码块为代理；允许其他语言块，但 cpp 为主）
    # part-aware: history/reading chapters have lower threshold (narrative-focused)
    cpp_blocks = len(CPP_BLOCK_RE.findall(text))
    rep["cpp_blocks"] = cpp_blocks
    part_name = path.parent.name
    effective_min = 10 if 'history' in part_name or 'reading' in part_name else MIN_EXAMPLES
    if cpp_blocks < effective_min:
        rep["warns"].append(f"可编译示例(cpp块)={cpp_blocks} < 阈值{effective_min}({part_name})")
    else:
        rep["info"].append(f"示例数达标: {cpp_blocks}")

    # 4. 立场分层标签
    have_stance = any(lbl in text for lbl in STANCE_LABELS)
    if not have_stance:
        rep["warns"].append("未见立场分层标签[标准]/[实现]/[平台]/[经验]")
    rep["stance"] = have_stance

    # 5. 交叉引用存在性
    refs = set(FILE_LINK_RE.findall(text)) | set(CROSSREF_RE.findall(text))
    broken = []
    for r in refs:
        # 规范化：去反引号，转 posix
        r = r.strip("`").replace("\\", "/")
        target = root / r
        if not target.exists():
            broken.append(r)
    if broken:
        rep["warns"].append(f"交叉引用断链({len(broken)}): {broken[:5]}")
    rep["broken_refs"] = broken

    # 6. ASCII 框线统计（INFO）
    ascii_hits = len(ASCII_BOX_RE.findall(text))
    if ascii_hits:
        rep["info"].append(f"ASCII框线字符数={ascii_hits}（Bible允许ASCII图，仅统计）")

    # 9. 源码剖析模板 C 风格（含「文件：」+ 行号）
    src_files = SRC_FILE_RE.findall(text)
    if src_files:
        no_line = [f for f in src_files if not SRC_LINE_RE.search(text)]
        if no_line:
            rep["warns"].append(f"源码剖析缺行号标注: {no_line[:3]}")
        # 校验源码文件路径是否真实可读（若为本地绝对/相对路径）
        for f in src_files:
            fp = Path(f)
            if fp.is_absolute() and not fp.exists():
                rep["warns"].append(f"源码路径不可达(本机): {f}")
            elif not fp.is_absolute() and not (root / fp).exists() and ("/" in f):
                # 可能是编译器安装路径，仅 INFO
                rep["info"].append(f"源码路径(可能本机无): {f}")

    return rep


def check_glossary(root: Path) -> dict:
    gpath = root / "glossary.json"
    rep = {"errors": [], "warns": [], "info": []}
    if not gpath.exists():
        rep["errors"].append("glossary.json 缺失")
        return rep
    try:
        data = json.loads(gpath.read_text(encoding="utf-8"))
    except Exception as e:
        rep["errors"].append(f"glossary.json 非法 JSON: {e}")
        return rep
    terms = data.get("terms", [])
    rep["info"].append(f"glossary.json 术语数={len(terms)}")
    ids = [t.get("id") for t in terms]
    dups = {i for i in set(ids) if ids.count(i) > 1}
    if dups:
        rep["errors"].append(f"glossary 重复 id: {dups}")
    # chapter_ref 指向真实文件?
    book = root / "Book"
    broken = []
    for t in terms:
        ref = t.get("chapter_ref", "")
        if ref.startswith("Book/"):
            if not (root / ref).exists():
                broken.append(ref)
    if broken:
        rep["warns"].append(f"glossary chapter_ref 断链({len(broken)}): {broken[:5]}")
    return rep


def check_duplicate_chapter_numbers(root: Path) -> list[str]:
    book = root / "Book"
    seen = {}
    dups = []
    if not book.is_dir():
        return dups
    for f in book.rglob("*.md"):
        for m in HEADING_NUM_RE.finditer(f.read_text(encoding="utf-8")):
            num = m.group(1)
            seen.setdefault(num, []).append(f.name)
    for num, files in seen.items():
        if len(files) > 1:
            dups.append(f"第{num}章 重复: {files}")
    return dups


def main():
    global MIN_EXAMPLES
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=None, help="CPP-Bible 根目录")
    ap.add_argument("--json", default=None, help="输出 JSON 报告路径")
    ap.add_argument("--min-examples", type=int, default=MIN_EXAMPLES)
    args = ap.parse_args()

    MIN_EXAMPLES = args.min_examples

    root = find_book_root(args.root)
    book = root / "Book"
    print(f"[*] 根目录: {root}")
    print(f"[*] Book 目录: {book} (存在={book.is_dir()})")

    chapters = sorted(book.rglob("*.md")) if book.is_dir() else []
    chapters = [c for c in chapters if not any(s in c.parts for s in SKIP_DIRS)]
    print(f"[*] 扫描章节: {len(chapters)} 个\n")

    all_reps = []
    total_err = 0
    total_warn = 0

    for ch in chapters:
        r = check_chapter(ch, root)
        all_reps.append(r)
        total_err += len(r["errors"])
        total_warn += len(r["warns"])
        # 单行摘要
        status = "ERR" if r["errors"] else ("WARN" if r["warns"] else "OK")
        print(f"[{status:4}] {r['file']:55} "
              f"元素{r['elements_hit']:2}/20 示例{r.get('cpp_blocks','?'):3} "
              f"立场{'Y' if r.get('stance') else 'N'} "
              f"断链{len(r.get('broken_refs',[]))}")
        for e in r["errors"]:
            print(f"        ✗ {e}")
        for w in r["warns"][:4]:
            print(f"        ! {w}")

    # glossary
    print("\n[*] glossary.json 检查:")
    gr = check_glossary(root)
    total_err += len(gr["errors"])
    total_warn += len(gr["warns"])
    for e in gr["errors"]:
        print(f"    ✗ {e}")
    for w in gr["warns"]:
        print(f"    ! {w}")
    for i in gr["info"]:
        print(f"    · {i}")

    # 重复章节号
    dups = check_duplicate_chapter_numbers(root)
    print("\n[*] 章节号重复检查:")
    if dups:
        total_err += len(dups)
        for d in dups:
            print(f"    ✗ {d}")
    else:
        print("    OK 无重复章号")

    # 汇总
    print("\n" + "=" * 60)
    print(f"汇总: 章节={len(chapters)} ERROR={total_err} WARN={total_warn}")
    score = max(0, 100 - total_err * 5 - total_warn)
    print(f"一致性评分(粗): {score}/100")
    print("=" * 60)

    if args.json:
        out = {
            "root": str(root),
            "chapters": all_reps,
            "glossary": gr,
            "duplicate_chapter_numbers": dups,
            "totals": {"errors": total_err, "warns": total_warn},
        }
        Path(args.json).write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"[*] JSON 报告已写: {args.json}")

    sys.exit(1 if total_err else 0)


if __name__ == "__main__":
    main()
