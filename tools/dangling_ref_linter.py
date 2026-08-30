#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
悬空章节引用 linter (T1-2)
=======================
扫描全书「正文」对所有“第N章 / chN”的引用，核对 N 是否落在有效章节编号
集合内；不在集合内即报警（悬空引用，读者点进去是空章 / 已被删除的编号）。

有效编号集合（ground truth）= 磁盘真实存在的 Book/**/chNN_*.md 文件编号。
同时解析 Book/SUMMARY.md 的链接集合做交叉校验，报告孤儿链接 / 缺失链接。

设计要点：
  - 只扫「代码围栏之外」的 prose，避免把 cpp 代码里的 `char`/`chmod`/`epoch3`
    等误判为章节引用（靠 \\b 词边界 + 引用语境双重过滤）。
  - 章节自身在标题里写自己的编号属正常，跳过。
  - 生成索引文件（SUMMARY/PREREQUISITES/GLOSSARY）本身不扫，它们只列有效链接。
  - 范围覆盖「任何不在有效集合里的编号」，不局限于已知的 18 个空缺，使后续
    再删 / 再合并章节也能自动兜住。

用法:
    python tools/dangling_ref_linter.py
    python tools/dangling_ref_linter.py --json out.json
    python tools/dangling_ref_linter.py --book /path/to/Book
退出码: 发现悬空引用返回 1（可作 CI 门禁），否则 0。
"""
import argparse
import json
import re
import sys
from pathlib import Path
from collections import Counter

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
BOOK = ROOT / "Book"

CJK = r"[一-鿿]"
CHNUM_REF = re.compile(r"\bch(\d+)\b")        # chNN 缩写（\b 防止 epoch3 / char 误判）
CN_CHAPTER = re.compile(r"第\s*(\d+)\s*章")    # 第N章

# 引用语境：chN 前后需贴近 CJK / 标点 / 箭头，才认定为章节引用
REF_BEFORE = re.compile(rf"({CJK}|见|参|→|⟶|see|See)\s*$")
REF_AFTER = re.compile(rf"^(\s*[（(：、，。/|]|{CJK})")

SKIP_FILES = {"SUMMARY.md", "PREREQUISITES.md", "GLOSSARY.md",
              "INDEX.md", "README.md", "changelog.md"}


def valid_from_disk(book: Path) -> set:
    s = set()
    for p in book.rglob("ch*.md"):
        m = re.match(r"ch(\d+)_", p.name)
        if m:
            s.add(int(m.group(1)))
    return s


def valid_from_summary(book: Path) -> set:
    s = set()
    sm = book / "SUMMARY.md"
    if sm.is_file():
        # SUMMARY 链接形如 (part01_history/ch01_c_history.md)；ch 后紧跟 '_'，
        # 故用无词边界的 ch(\d+) 提取（URL 里的编号才是有效链接）。
        for ln in sm.read_text(encoding="utf-8").splitlines():
            for m in re.finditer(r"ch(\d+)", ln):
                s.add(int(m.group(1)))
    return s


def scan_chapter(path: Path, valid: set, findings: list, per_missing: Counter):
    """返回 (refs_total,)。把悬空引用追加到 findings / per_missing。"""
    lines = path.read_text(encoding="utf-8").splitlines()
    refs_total = 0
    inside = False
    stem_m = re.match(r"ch(\d+)_", path.name)
    self_n = int(stem_m.group(1)) if stem_m else None

    for i, ln in enumerate(lines, 1):
        if ln.strip().startswith("```"):
            inside = not inside
            continue
        if inside:
            continue
        refs_total += len(CN_CHAPTER.findall(ln)) + len(CHNUM_REF.findall(ln))

        rel = path.relative_to(BOOK).as_posix()
        # 第N章
        for m in CN_CHAPTER.finditer(ln):
            n = int(m.group(1))
            if n not in valid:
                findings.append((rel, i, f"第{n}章", n, ln.strip()))
                per_missing[n] += 1
        # chN
        for m in CHNUM_REF.finditer(ln):
            n = int(m.group(1))
            if n in valid:
                continue
            if self_n is not None and n == self_n:
                continue
            before_char = ln[m.start() - 1] if m.start() > 0 else ""
            after = ln[m.end():]
            is_ref = (not before_char.isalnum()) and (
                REF_BEFORE.search(ln[:m.start()]) is not None
                or REF_AFTER.match(after) is not None
                or after == ""
            )
            if not is_ref:
                continue
            findings.append((rel, i, f"ch{n}", n, ln.strip()))
            per_missing[n] += 1
    return refs_total


def main():
    ap = argparse.ArgumentParser(description="悬空章节引用 linter (T1-2)")
    ap.add_argument("--book", default=str(BOOK))
    ap.add_argument("--json", default=None, help="输出 JSON 路径")
    args = ap.parse_args()
    book = Path(args.book)

    valid = valid_from_disk(book)
    summary_valid = valid_from_summary(book)
    orphan_links = summary_valid - valid     # SUMMARY 列了但磁盘没有
    missing_links = valid - summary_valid     # 磁盘有但 SUMMARY 没列

    findings = []
    per_missing = Counter()
    files_scanned = 0
    refs_total = 0

    for ch in sorted(book.rglob("ch*.md")):
        if ch.name in SKIP_FILES:
            continue
        files_scanned += 1
        refs_total += scan_chapter(ch, valid, findings, per_missing)

    print(f"[*] 有效章节编号集合大小: {len(valid)} (来自磁盘 chNN_*.md)")
    if orphan_links:
        print(f"[!] SUMMARY 列出了但磁盘不存在的编号: {sorted(orphan_links)}")
    if missing_links:
        print(f"[!] 磁盘存在但 SUMMARY 未链接的编号: {sorted(missing_links)}")
    print(f"[*] 扫描章节文件: {files_scanned} | 粗略引用出现次数: {refs_total}")
    print(f"[*] 悬空章节引用: {len(findings)} 处，涉及 {len(per_missing)} 个不同空缺编号")
    if per_missing:
        print("    空缺编号被正文引用频次（按编号排序）:")
        for n in sorted(per_missing):
            print(f"      ch{n:<4} : {per_missing[n]} 次")

    # 与审计报告声明对照
    audit_missing = {33, 34, 53, 54, 55, 56, 57, 58, 59,
                    73, 74, 75, 102, 103, 104, 105, 106, 114}
    covered = sorted(set(per_missing) & audit_missing)
    print(f"\n[对照审计] 审计列出的 18 个空缺中，正文确实引用到的: {covered}")
    print(f"[对照审计] 审计 18 空缺中，正文未引用（可能已迁移/无碍）: "
          f"{sorted(audit_missing - set(per_missing))}")

    if findings:
        print(f"\n[!] 明细（前 80 条；完整见 --json）:")
        for f in findings[:80]:
            print(f"    {f[0]}:{f[1]}  [{f[2]}]  {f[4][:78]}")
        if len(findings) > 80:
            print(f"    ... 共 {len(findings)} 条")

    if args.json:
        payload = {
            "valid_count": len(valid),
            "orphan_links": sorted(orphan_links),
            "missing_links": sorted(missing_links),
            "dangling_count": len(findings),
            "per_missing_number": {str(k): v for k, v in sorted(per_missing.items())},
            "audit_missing": sorted(audit_missing),
            "audit_missing_referenced": covered,
            "findings": [
                {"file": f[0], "line": f[1], "ref": f[2],
                 "number": f[3], "context": f[4]}
                for f in findings
            ],
        }
        out = Path(args.json)
        out.parent.mkdir(parents=True, exist_ok=True)  # CI 干净 checkout 无 outputs/，需自建
        out.write_text(
            json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
        print(f"\n[+] JSON 写入: {args.json}")

    return 1 if (findings or orphan_links) else 0


if __name__ == "__main__":
    sys.exit(main())
