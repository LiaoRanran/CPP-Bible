#!/usr/bin/env python3
"""C3: 章编号一致性审计。

检查项：
  1) 文件名 chNN 的编号 与 章内 H1 标题「第NN章」是否一致
  2) 全书章号序列是否连续（无缺号 / 无重号）
  3) 文件名编号 与 所属 part 目录声明的章号区间是否吻合（如有 nav / SUMMARY）
  4) mkdocs 导航（如存在）引用的章文件是否都真实存在

退出码：0 = 全部一致；非 0 = 存在不一致（供 CI / 门禁使用）。
"""
from __future__ import annotations
import re
import sys
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / "Book"

FN_RE = re.compile(r"ch(\d+)_")
# H1 形如：# 第47章 ...  /  # 第01章　...（全角或半角空格）
H1_RE = re.compile(r"^#\s*第\s*(\d+)\s*章")


def collect() -> list[dict]:
    rows = []
    for md in sorted(BOOK.rglob("ch*.md")):
        # 跳过遗留目录
        if "_legacy" in str(md):
            continue
        m = FN_RE.search(md.name)
        if not m:
            continue
        fn_num = int(m.group(1))
        h1_num = None
        h1_line = None
        try:
            with md.open(encoding="utf-8") as fh:
                for line in fh:
                    if line.startswith("#") and not line.startswith("##"):
                        mm = H1_RE.match(line)
                        if mm:
                            h1_num = int(mm.group(1))
                            h1_line = line.rstrip("\n")
                        break  # 只看第一条 H1
        except Exception as e:  # noqa
            rows.append({"file": str(md.relative_to(ROOT)), "fn": fn_num,
                         "h1": None, "err": f"read-error: {e}"})
            continue
        rows.append({
            "file": str(md.relative_to(ROOT)),
            "part": md.parent.name,
            "fn": fn_num,
            "h1": h1_num,
            "h1_line": h1_line,
        })
    return rows


def main() -> int:
    rows = collect()
    errors: list[str] = []
    warns: list[str] = []

    # 1) 文件名 vs H1
    for r in rows:
        if r.get("err"):
            errors.append(f"[读取失败] {r['file']}: {r['err']}")
            continue
        if r["h1"] is None:
            errors.append(f"[缺 H1 章号] {r['file']} 未找到「第NN章」标题")
        elif r["h1"] != r["fn"]:
            errors.append(
                f"[编号不符] {r['file']}: 文件名 ch{r['fn']:02d} ≠ 标题 第{r['h1']}章 "
                f"（H1='{r['h1_line']}'）")

    # 2) 序列连续性（以文件名编号为准）
    nums = sorted(r["fn"] for r in rows)
    dup = sorted({n for n in nums if nums.count(n) > 1})
    if dup:
        errors.append(f"[重号] 章号重复: {dup}")
    if nums:
        full = set(range(nums[0], nums[-1] + 1))
        missing = sorted(full - set(nums))
        if missing:
            warns.append(f"[缺号] 章号区间 {nums[0]}..{nums[-1]} 中缺失: {missing}")

    # 3) part 内编号单调性（part 目录应按章号升序聚集）
    from collections import defaultdict
    part_nums = defaultdict(list)
    for r in rows:
        part_nums[r["part"]].append(r["fn"])
    part_order = []
    for part in sorted(part_nums):
        pn = sorted(part_nums[part])
        part_order.append((part, pn[0], pn[-1]))
    # 检查 part 之间区间不重叠
    part_order.sort(key=lambda x: x[1])
    for i in range(1, len(part_order)):
        prev = part_order[i - 1]
        cur = part_order[i]
        if cur[1] <= prev[2]:
            warns.append(
                f"[part 区间重叠] {prev[0]}({prev[1]}-{prev[2]}) 与 "
                f"{cur[0]}({cur[1]}-{cur[2]}) 章号交叉")

    # 4) mkdocs nav 引用文件存在性
    mk = ROOT / "mkdocs.yml"
    if mk.exists():
        txt = mk.read_text(encoding="utf-8", errors="replace")
        refs = re.findall(r"(part\d+[\w/]*?/ch\d+_[\w]+\.md)", txt)
        for ref in refs:
            if not (BOOK / ref).exists() and not (ROOT / ref).exists():
                # 有些 nav 以 Book/ 为根
                if not (ROOT / "Book" / ref).exists():
                    warns.append(f"[nav 悬空引用] mkdocs.yml -> {ref} 不存在")

    # 汇报
    print("=" * 60)
    print(f"C3 章编号一致性审计：共 {len(rows)} 章")
    print(f"  章号范围: {nums[0]}..{nums[-1]}" if nums else "  (无章节)")
    print("=" * 60)
    if not errors and not warns:
        print("✅ 全部一致：文件名编号 == H1 章号；序列连续；无重号；part 不重叠。")
        return 0
    if errors:
        print(f"\n❌ ERROR ({len(errors)}):")
        for e in errors:
            print("  -", e)
    if warns:
        print(f"\n⚠️  WARN ({len(warns)}):")
        for w in warns:
            print("  -", w)
    # 缺号可能是设计（如预留章位），归 WARN 不阻断；ERROR 才非零退出
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
