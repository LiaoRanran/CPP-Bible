#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""template_audit.py — 章节作者性审计：模板化/套话节扫描（终极打磨的自查工具）

背景
====
全书 147 章大量机械套用「学习目标/思考题/习题」等产品式节——评价第 1 条点名
「空泛总结、重复定义、机械模板、无信息量的学习目标/总结/展望」属灌水；第 2 条要求
按主题自由选叙事方式，不要所有章套固定结构。

本工具把『模板化痕迹』客观化：扫描每章的节标题，命中 CLICHES 模板节即计数，
输出全书排名，供精修时按章定位。只读数、不改写、零依赖。

用法
====
  python tools/template_audit.py            # 打印全部命中分级清单
  python tools/template_audit.py --top 20   # 只看模板化最重的 20 章
  python tools/template_audit.py --check 8  # 命中≥8 个模板节即非零退出(可选卡口)

注意
====
命中的模板节可能是「确有信息量的技术小结」，不自动定罪——本工具只提供定位线索，
真相由人工审读判断（对齐项目纯读侧门禁的一贯风格）。
"""
from __future__ import annotations
import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# 产品式/空泛套话节标题关键词（命中整段标题，非正文任意词）
CLICHES = [
    "学习目标", "教学目标", "本节目标", "本章目标",
    "本节小结", "本节总结", "本章小结", "本章总结",
    "本节要点", "本章要点", "本节预告", "本节收获", "本讲小结",
    "思考题", "巩固练习", "课后练习", "课后作业", "课后习题",
    "小结", "总结", "展望", "习题", "复习", "学完本章",
]

HEAD_RE = re.compile(r"^#{1,6}\s+(.+?)\s*#*\s*$", flags=re.M)


def chapter_hits(md: Path) -> list[str]:
    text = md.read_text(encoding="utf-8", errors="replace")
    heads = [h.strip() for h in HEAD_RE.findall(text)]
    seen: set[str] = set()
    hits: list[str] = []
    for h in heads:
        for cl in CLICHES:
            if cl in h and cl not in seen:
                seen.add(cl)
                hits.append(cl)
                break
    return hits


def main() -> int:
    ap = argparse.ArgumentParser(description="章节作者性审计：模板化/套话节扫描")
    ap.add_argument("--top", type=int, default=0, help="只看模板化最重的前 N 章")
    ap.add_argument("--check", type=int, default=0, metavar="N",
                    help="命中≥N 个模板节则退出码 1（可选卡口）")
    args = ap.parse_args()

    rows: list[tuple[Path, list[str]]] = []
    for md in sorted(ROOT.glob("Book/**/ch*.md")):
        if "_legacy" in md.as_posix():
            continue
        hits = chapter_hits(md)
        if hits:
            rows.append((md, hits))
    rows.sort(key=lambda r: (-len(r[1]), r[0].as_posix()))

    n_hit = len(rows)
    print(f"[tpl] 命中模板节的章数: {n_hit} / 147")
    if args.top:
        rows = rows[: args.top]
        print(f"[tpl] 前 {args.top}（模板化最重）:")
    for md, hits in rows:
        label = "/".join(hits)
        print(f"        {md.relative_to(ROOT).as_posix()}  {len(hits):2d}  {label}")

    if args.check and n_hit:
        worst = max(len(h) for _, h in rows)
        print(f"[tpl] 单章最高命中 {worst} 个模板节（阈值 {args.check}）。")
        if worst >= args.check:
            return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())