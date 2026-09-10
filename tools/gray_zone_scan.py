#!/usr/bin/env python3
"""灰色地带（gray zone）初筛：把全书泛用的「未定义」细分。

背景（G1 已查证）：书内「未定义行为/UB」共现 5158 行，而「未指定」99 行、
「实现定义」91 行——量级差 50 倍，强烈提示「未定义」被泛用。
本工具按句子级上下文做**机械初筛**，输出疑似误分类样本，供人工判定（G2.1 判定流程的输入）。

五类（与 G2.1 判定流程一致）：
  defined            —— 标准有明确规定
  unspecified        —— 标准给若干合法结果，实现任选（不要求文档）
  implementation_defined —— 实现任选但必须写进文档
  ub                 —— 未定义行为（任何结果都可能，含崩溃）
  abi_dependent      —— 取决于 ABI/调用约定/布局/对齐，非标准语义层

用法：
    python tools/gray_zone_scan.py                 # 汇总 + 疑似误分类样本
    python tools/gray_zone_scan.py --json out.json
    python tools/gray_zone_scan.py --top 30        # 每类样本条数

只读，不修改任何文件。
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from comment_blocks import iter_md_files  # noqa: E402

ROOT = HERE.parent

# 触发词（出现即纳入候选句）
TRIGGER = re.compile(r"未定义|undefined|\bUB\b|未指定|unspecified|实现定义|implementation-defined|实现相关|依赖实现")

# 分类线索（按优先级从"最具体"到"最泛"，先命中者优先）
PATTERNS: list[tuple[str, re.Pattern]] = [
    ("implementation_defined",
     re.compile(r"实现定义|implementation-defined|实现相[关切]|由实现定义|实现自定义")),
    ("unspecified",
     re.compile(r"未指定|unspecified| unspecified|不确定（但合法）")),
    ("abi_dependent",
     re.compile(r"\bABI\b|调用约定|名字修饰|mangled|布局差异|对齐要求|vtable\s*布局|结构体填充")),
    ("ub",
     re.compile(r"未定义行为|undefined behavior|\bUB\b|未定义（行为）")),
]

# 疑似误用主题词：句子用了「未定义」但主题其实属于 unspecified / impl-def
SUSPECT_TOPIC: list[tuple[str, str, re.Pattern]] = [
    ("unspecified", "求值顺序", re.compile(r"求值顺序|参数求值|函数实参求值|顺序未定")),
    ("unspecified", "容器/迭代器顺序", re.compile(r"遍历顺序|迭代顺序|unordered.*顺序|顺序不保证")),
    ("implementation_defined", "char 符号性", re.compile(r"char\s*的?符号|char.*有符号|signed\s*char.*默认")),
    ("implementation_defined", "整型大小", re.compile(r"\bint\b.*宽度|整型.*大小|long.*字节|sizeof\(.*\)差异")),
    ("implementation_defined", "右移", re.compile(r"右移|>>.*符号|算术右移")),
    # 注意：「未对齐访问」是 UB（不是 ABI 类），故主题词只收 ABI 语义，
    # 不收裸「对齐」——首跑时把 UBSan 抓未对齐的 20 条误判成 abi_dependent，已修正。
    ("abi_dependent", "布局/调用约定", re.compile(r"对象布局差异|内存布局差异|结构体填充|调用约定|名字修饰|mangled\s*名|vtable\s*布局")),
]

SENT_SPLIT = re.compile(r"(?<=[。；！？\n])")


def sent_candidates(text: str) -> list[str]:
    out = []
    for seg in SENT_SPLIT.split(text):
        s = seg.strip()
        if not s or len(s) > 400:
            continue
        if TRIGGER.search(s):
            out.append(s)
    return out


def classify(s: str) -> str:
    for name, pat in PATTERNS:
        if pat.search(s):
            return name
    return "defined"


def scan() -> tuple[dict, list[dict]]:
    counts: dict[str, int] = {}
    suspects: list[dict] = []
    for p in iter_md_files(ROOT / "Book"):
        rel = p.relative_to(ROOT / "Book").as_posix()
        text = p.read_bytes().decode("utf-8")
        for s in sent_candidates(text):
            cat = classify(s)
            counts[cat] = counts.get(cat, 0) + 1
            # 疑似误用：分类为 ub/defined，但主题词指向另一类
            if cat in ("ub", "defined"):
                for want, why, pat in SUSPECT_TOPIC:
                    if pat.search(s):
                        suspects.append({
                            "chapter": rel, "classified_as": cat,
                            "probably": want, "topic": why,
                            "sentence": s[:180],
                        })
                        break
    return counts, suspects


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="灰色地带初筛：细分泛用的「未定义」")
    ap.add_argument("--json", dest="json_path")
    ap.add_argument("--top", type=int, default=15, help="每类疑似样本条数")
    a = ap.parse_args(argv)

    counts, suspects = scan()
    total = sum(counts.values())
    print(f"[gray-zone] 候选句 {total}")
    for k in ("defined", "ub", "unspecified", "implementation_defined", "abi_dependent"):
        v = counts.get(k, 0)
        pct = (v / total * 100) if total else 0
        print(f"  {k:24} {v:6}  {pct:5.1f}%")

    print(f"\n[gray-zone] 疑似误分类（判为 UB/defined 但主题属他类）：{len(suspects)}")
    by_prob: dict[str, list[dict]] = {}
    for s in suspects:
        by_prob.setdefault(s["probably"], []).append(s)
    for prob, items in sorted(by_prob.items(), key=lambda kv: -len(kv[1])):
        print(f"\n  —— 应属 {prob}：{len(items)} 条")
        for it in items[:a.top]:
            print(f"     [{it['topic']}] {it['chapter']}")
            print(f"       {it['sentence']}")

    if a.json_path:
        Path(a.json_path).write_text(json.dumps(
            {"counts": counts, "suspects": suspects}, ensure_ascii=False, indent=1),
            encoding="utf-8")
        print(f"\n[gray-zone] JSON → {a.json_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
