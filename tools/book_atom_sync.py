#!/usr/bin/env python3
"""Book 与原子双向同步检查工具（309 方案落地）。

检查：
  1. 原子无 Book 引用：sources 中没有 Book/ 路径 → warn
  2. Book 论断无原子支撑：出现"实测/实验/性能数据/基准"等关键词但无 <atom> → warn
  3. 孤儿原子引用：Book 中 <atom>XXX</atom> 指向不存在的原子 → block

用法：
  python tools/book_atom_sync.py --check      # 检查同步状态，有问题 exit 1
  python tools/book_atom_sync.py --report     # 生成详细同步报告
  python tools/book_atom_sync.py --atom XXX   # 检查某颗原子的同步状态
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ATOMS = ROOT / "atoms"
BOOK = ROOT / "Book"

# 373 §5 收编（2026-09-13）：本工具原先自带一份"极简 frontmatter 解析器"——
# 与 `atom_evidence_replay.parse_frontmatter` 是**双轨实现**（同一份语法两套语义：
# 折叠块、flow map、嵌套结构各写一遍，改一处漏一处）。重叠部分砍掉，复用单点实现。
sys.path.insert(0, str(Path(__file__).resolve().parent))
from atom_evidence_replay import parse_frontmatter  # noqa: E402

# Book 中暗示"有实验证据"的关键词（应有 <atom> 标注）
EVIDENCE_KEYWORDS = [
    "实测", "实验证明", "性能数据", "基准测试", "benchmark",
    "我们测", "本机测", "编译器输出", "汇编显示", "运行结果",
]

ATOM_TAG_RE = re.compile(r"<atom>([A-Z]+-[A-Z0-9-]+)</atom>")
BOOK_PATH_RE = re.compile(r"Book/[^\s\"')]+")


def scan_atoms() -> list[dict]:
    """扫描所有原子，返回同步状态。"""
    atoms = []
    for p in sorted(ATOMS.rglob("ATOM-*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text)
        atom_id = fm.get("id", p.stem)
        sources = fm.get("sources", [])
        if isinstance(sources, str):
            sources = [sources]
        book_refs = []
        for s in sources:
            book_refs.extend(BOOK_PATH_RE.findall(str(s)))
        atoms.append({
            "id": atom_id,
            "path": p.relative_to(ROOT).as_posix(),
            "book_refs": book_refs,
            "has_book_ref": bool(book_refs),
            "status": fm.get("status", "unknown"),
        })
    return atoms


def scan_book() -> list[dict]:
    """扫描 Book，返回 <atom> 标签使用情况。"""
    chapters = []
    for p in sorted(BOOK.rglob("ch*.md")):
        text = p.read_text(encoding="utf-8", errors="replace")
        atom_tags = ATOM_TAG_RE.findall(text)
        # 检查有证据关键词但无 atom 标签的段落
        evidence_without_atom = 0
        for para in text.split("\n\n"):
            if any(kw in para for kw in EVIDENCE_KEYWORDS) and "<atom>" not in para:
                evidence_without_atom += 1
        chapters.append({
            "path": p.relative_to(ROOT).as_posix(),
            "atom_tags": atom_tags,
            "evidence_without_atom": evidence_without_atom,
        })
    return chapters


def cmd_check() -> int:
    """检查同步状态，有问题 exit 1。"""
    atoms = scan_atoms()
    chapters = scan_book()

    # 373 §5（2026-09-13）：**退出码与 severity 对齐**——warn 类只提示不阻断，
    # 只有 block 类（孤儿引用）才 exit 1。原因：当前存量 27/27 原子无 Book 引用、
    # 143/147 章缺 `<atom>` 标注（共 170 处 warn），若 warn 也 exit 1，本工具一接入
    # 质量门就恒红 ⇒ 门禁沦为"狼来了"。补标注是 Book 内容改动（本批铁律禁止），
    # 登记为债务逐步消化；**孤儿引用（引用了不存在的原子）才是必须阻断的错误**。
    issues = 0
    # 1. 原子无 Book 引用
    no_book = [a for a in atoms if not a["has_book_ref"]]
    if no_book:
        print(f"[WARN] {len(no_book)}/{len(atoms)} 颗原子无 Book 引用：")
        for a in no_book:
            print(f"       {a['id']}  ({a['path']})")
        issues += len(no_book)

    # 2. Book 论断无原子支撑
    no_atom = [c for c in chapters if c["evidence_without_atom"] > 0]
    if no_atom:
        total = sum(c["evidence_without_atom"] for c in no_atom)
        print(f"[WARN] {len(no_atom)} 章含证据关键词但无 <atom> 标注（共 {total} 段）：")
        for c in no_atom[:10]:
            print(f"       {c['path']}  ({c['evidence_without_atom']} 段)")
        if len(no_atom) > 10:
            print(f"       ... 共 {len(no_atom)} 章")
        issues += total

    # 3. 孤儿原子引用
    atom_ids = {a["id"] for a in atoms}
    orphan_refs = []
    for c in chapters:
        for tag in c["atom_tags"]:
            if tag not in atom_ids:
                orphan_refs.append((c["path"], tag))
    if orphan_refs:
        print(f"[BLOCK] {len(orphan_refs)} 处 <atom> 引用指向不存在的原子：")
        for path, tag in orphan_refs:
            print(f"        {path} → {tag}")
        issues += len(orphan_refs)

    # 汇总
    print(f"\n[summary] 原子 {len(atoms)} · Book 章 {len(chapters)} · "
          f"原子有 Book 引用 {len(atoms)-len(no_book)}/{len(atoms)} · "
          f"Book 有 <atom> 标签 {sum(1 for c in chapters if c['atom_tags'])}/{len(chapters)} · "
          f"warn {issues - len(orphan_refs)} · block {len(orphan_refs)}")

    return 1 if orphan_refs else 0      # 只 block 类阻断（见上方 373 §5 说明）


def cmd_report() -> int:
    """生成详细同步报告。"""
    atoms = scan_atoms()
    chapters = scan_book()

    print("=" * 60)
    print("Book 与原子同步报告")
    print("=" * 60)

    print(f"\n## 原子概览（{len(atoms)} 颗）")
    by_domain: dict[str, int] = {}
    for a in atoms:
        domain = a["id"].split("-")[1] if "-" in a["id"] else "unknown"
        by_domain[domain] = by_domain.get(domain, 0) + 1
    for dom, cnt in sorted(by_domain.items()):
        print(f"  {dom}: {cnt}")

    print("\n## 原子 → Book 引用")
    has_ref = [a for a in atoms if a["has_book_ref"]]
    print(f"  有 Book 引用: {len(has_ref)}/{len(atoms)}")
    for a in has_ref:
        print(f"    {a['id']}: {', '.join(a['book_refs'])}")

    print("\n## Book → 原子引用")
    has_atom = [c for c in chapters if c["atom_tags"]]
    print(f"  有 <atom> 标签: {len(has_atom)}/{len(chapters)} 章")
    for c in has_atom:
        print(f"    {c['path']}: {', '.join(c['atom_tags'])}")

    print("\n## 证据关键词但无 <atom> 的章节")
    no_atom = [c for c in chapters if c["evidence_without_atom"] > 0]
    for c in sorted(no_atom, key=lambda x: -x["evidence_without_atom"]):
        print(f"  {c['path']}: {c['evidence_without_atom']} 段")

    return 0


def cmd_atom(atom_id: str) -> int:
    """检查某颗原子的同步状态。"""
    atoms = scan_atoms()
    target = next((a for a in atoms if a["id"] == atom_id), None)
    if not target:
        print(f"[ERROR] 原子不存在: {atom_id}")
        return 1

    print(f"原子: {target['id']}")
    print(f"  路径: {target['path']}")
    print(f"  状态: {target['status']}")
    print(f"  Book 引用: {', '.join(target['book_refs']) if target['book_refs'] else '（无）'}")

    # 反向查找：哪些 Book 章引用了这颗原子
    chapters = scan_book()
    refs = [c["path"] for c in chapters if atom_id in c["atom_tags"]]
    print(f"  被 Book 引用: {', '.join(refs) if refs else '（无）'}")
    return 0


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Book 与原子双向同步检查")
    ap.add_argument("--check", action="store_true", help="检查同步状态")
    ap.add_argument("--report", action="store_true", help="生成详细报告")
    ap.add_argument("--atom", help="检查某颗原子的同步状态")
    a = ap.parse_args(argv)

    if a.atom:
        return cmd_atom(a.atom)
    if a.report:
        return cmd_report()
    return cmd_check()


if __name__ == "__main__":
    raise SystemExit(main())
