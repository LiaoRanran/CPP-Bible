#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
apply_chapter_tiers.py — 全库章级 L1/L2/L3 分层标记（P2 规模化）

规则（结构派生根规则，透明可审）：
  L1 入门 : part01_history / part02_toolchain / part16_reading
  L2 进阶 : part03_language / part04_memory / part05_oo / part06_templates(基础)
            part07_stl / part08_algorithms / part10_modern / part11_source
            part12_patterns / part13_engineering / part15_cases
  L3 专家 : part09_concurrency / part14_perf（整 part 默认 L3）
            其余 part 中文件名含元编程/性能/底层/并发关键词 -> 提升 L3
            （tmp / trait / sfinae / concept / strict_alias / cache / pool / abi / simd ...）

注入策略（最小侵入、非注水）：
  - 章已有 meta 块注行（前 30 行内、含 标准基/预计阅读/难度/前置/后续 之一 的 > 块注）：
    幂等追加 `｜层级：Lx 中文`。
  - 章无 meta 块注行：在 H1 标题后插入一行 `> 层级：Lx 中文`（最小 meta 行）。
  - 全文已含 `层级：Lx`（带 内存/缓存 负回顾排除）则整章跳过（幂等，不覆盖人工判断）。

输出一律 LF（newline="\n"），符合仓库红线。
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "Book"

TIER_CN = {"L1": "入门", "L2": "进阶", "L3": "专家"}

PART_DEFAULT = {
    "part01_history": "L1",
    "part02_toolchain": "L1",
    "part16_reading": "L1",
    "part03_language": "L2",
    "part04_memory": "L2",
    "part05_oo": "L2",
    "part06_templates": "L2",
    "part07_stl": "L2",
    "part08_algorithms": "L2",
    "part10_modern": "L2",
    "part11_source": "L2",
    "part12_patterns": "L2",
    "part13_engineering": "L2",
    "part15_cases": "L2",
    "part09_concurrency": "L3",
    "part14_perf": "L3",
}

# 仅用于把 L2 提升到 L3（L1 不提升，L3 不降级）
# 匹配规则：下划线/词边界左锚定 (?:^|_)kw，避免 perf→perfect、thread→... 等子串误伤
L3_KEYWORDS = [
    "tmp", "metaprogram", "concept", "sfinae", "trait",
    "strict_alias", "cache", "pool", "mempool", "abi", "simd", "vectoriz",
    "benchmark", "profile", "microarch", "concurrent", "atomic",
    "optim", "inline_asm", "intrinsic",
]


def has_kw(name: str, kw: str) -> bool:
    return re.search(r"(?:^|_)" + re.escape(kw), name) is not None

TIER_RE = re.compile(r"(?<!内存)(?<!缓存)层级\s*[:：]\s*L([123])")
META_KEYS = re.compile(r"标准基\s*[:：]|预计阅读\s*[:：]|难度\s*[:：]|前置\s*[:：]|后续\s*[:：]")


def tier_for(path: Path) -> str:
    part = path.parent.name
    t = PART_DEFAULT.get(part, "L2")
    if t == "L2":
        name = path.stem.lower()
        for kw in L3_KEYWORDS:
            if has_kw(name, kw):
                t = "L3"
                break
    return t


def chapter_files():
    out = []
    for p in BOOK.rglob("*.md"):
        if "_legacy_" in str(p):
            continue
        if not p.stem.startswith("ch"):
            continue
        out.append(p)
    return sorted(out)


def find_meta_line_idx(lines):
    """返回前 30 行内、含 meta key 的 > 块注行索引；无则 None。"""
    for i, line in enumerate(lines[:30]):
        if line.lstrip().startswith(">") and META_KEYS.search(line):
            return i
    return None


def find_title_idx(lines):
    for i, line in enumerate(lines[:10]):
        if line.startswith("# "):
            return i
    return None


def plan(path: Path):
    """返回 (tier, action, detail)。action: skip / append(idx) / insert_after(idx)。"""
    tier = tier_for(path)
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return tier, "error", "read fail"
    lines = text.splitlines()

    # 幂等：全文已有合法 层级：Lx 标记 -> 跳过（不覆盖人工判断）
    for line in lines:
        if line.lstrip().startswith(">") and TIER_RE.search(line):
            m = TIER_RE.search(line)
            return m.group(1) and tier, "skip", f"已有 层级：L{m.group(1)}"

    meta_idx = find_meta_line_idx(lines)
    if meta_idx is not None:
        return tier, "append", f"追加到 meta 行 L{meta_idx+1}"
    title_idx = find_title_idx(lines)
    if title_idx is not None:
        return tier, "insert_after", f"H1 后插入（L{title_idx+1} 后）"
    return tier, "insert_top", "文件顶部插入"


def apply_one(path: Path, dry: bool):
    tier, action, detail = plan(path)
    if action == "skip" or action == "error":
        return tier, action, detail
    if dry:
        return tier, action, detail

    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()
    tag = f"层级：{tier} {TIER_CN[tier]}"
    if action == "append":
        idx = find_meta_line_idx(lines)
        lines[idx] = lines[idx].rstrip() + f"｜{tag}"
    elif action == "insert_after":
        idx = find_title_idx(lines)
        lines.insert(idx + 1, f"> {tag}")
    elif action == "insert_top":
        lines.insert(0, f"> {tag}")
    new_text = "\n".join(lines) + "\n"
    path.write_text(new_text, encoding="utf-8", newline="\n")
    return tier, action, detail


def main():
    dry = "--dry-run" in sys.argv
    files = chapter_files()
    dist = {"L1": 0, "L2": 0, "L3": 0}
    actions = {"skip": 0, "append": 0, "insert_after": 0, "insert_top": 0, "error": 0}
    print(f"[apply_chapter_tiers] {'DRY-RUN' if dry else 'APPLY'}  {len(files)} 章")
    print(f"{'chapter':<52} {'tier':<5} {'action':<13} detail")
    print("-" * 110)
    for p in files:
        tier, action, detail = apply_one(p, dry)
        dist[tier] = dist.get(tier, 0) + 1
        actions[action] = actions.get(action, 0) + 1
        rel = str(p.relative_to(ROOT))
        print(f"{rel:<52} {tier:<5} {action:<13} {detail}")
    print("-" * 110)
    print(f"层级分布: L1={dist.get('L1',0)}  L2={dist.get('L2',0)}  L3={dist.get('L3',0)}")
    print(f"操作统计: {actions}")


if __name__ == "__main__":
    main()
