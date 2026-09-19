#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""title_style_lint.py — P3 AI 风格标题词审计（报告型，不入 CI 门禁）

为什么需要这个轮子
==================
外部模型双评审（2026-07-30，GPT 总评 80 分 + Claude 对抗审查）给出 P3 优先级：
「标题净化」——部分章节标题带有 AI 生成内容典型的**夸张/营销化**措辞，例如
  ch19  "(工业级深度版)"   ch20  "生命周期战争"
  ch24 / ch26 / ch41  "全解"
这些词本身不降低信息密度，但暴露"AI 组装感"，与全库"硬核、可直接抄"的定位
略有张力。P3 治理方向：在保留信息量的前提下，把夸张词替换为更克制的表述。

本工具是治理的**地基**：扫全库 `Book/` 下所有 `ch*.md` 的 markdown 标题
（`#`/`##`/`###` …），定位 AI 风格词的 (章节, 行号, 标题, 命中词)，输出报告
供人工 triage。

设计约束（对齐 AGENT.md 红线）
==============================
- 只读 `Book/`，绝不修改源文件。
- 结果只写 stdout + 可选 `--json`，不污染源码树。
- 纯正则解析，秒级完成。
- **只报候选，不判罪**：像「全解」在 ch41 智能指针语境下信息量充足，可保留；
  而「生命周期战争」的"战争"隐喻偏营销。triage 时人工决定保留/改写。

P3 治理目标（AI-hype → sober）
=============================
候选词（命中即报告，由人工决定）：
  战争/大战/血战/之争        隐喻营销（ch20 已知）
  全解/完全指南/完全解读       "全"字承诺，部分成立
  工业级/专家级/大师级         等级自夸
  终极/史上最/最强            夸张最高级
  深度版/深度剖析/深度解析     "深度"冗余修饰
  一文搞懂/一篇读懂/彻底搞懂   速成营销
  保姆级/手把手/零基础         受众营销
  硬核/通关/封神/神器/必看/必读 情绪词
  秘籍/宝典/秘笈/圣经          神秘化
  从入门到精通/从零到一        跨度承诺

用法
====
  python3 tools/title_style_lint.py              # 人类可读报告
  python3 tools/title_style_lint.py --json       # 同时写 build/title_style_lint.json
  python3 tools/title_style_lint.py --porcelain  # 仅 chapter|line|words|heading
"""
import re
import json
import argparse
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / 'Book'

# AI 风格标题词（命中即候选，人工 triage）
HYPE_WORDS = [
    '战争', '大战', '血战', '之争', '对决',
    '全解', '完全指南', '完全解读', '完全手册',
    '工业级', '专家级', '大师级', '专业级',
    '终极', '史上最', '最强', '之王',
    '深度版', '深度剖析', '深度解析', '深度解读',
    '一文搞懂', '一篇读懂', '彻底搞懂', '秒懂',
    '保姆级', '手把手', '零基础', '小白',
    '硬核', '通关', '封神', '神器', '必看', '必读', '劝退',
    '秘籍', '宝典', '秘笈', '圣经',
    '从入门到精通', '从零到一', '从零开始',
    '血泪', '干货满满',
]

# 按长度降序编译，避免 "完全指南" 被 "指南" 之类的短词误命中
HYPE_WORDS_SORTED = sorted(HYPE_WORDS, key=len, reverse=True)
COMPILED = [(w, re.compile(re.escape(w))) for w in HYPE_WORDS_SORTED]

HEADING_RE = re.compile(r'^(\s{0,3})(#{1,6})\s+(.*)$')
FENCE_RE = re.compile(r'^\s*```')


def scan_file(path: Path):
    hits = []
    in_fence = False
    for i, line in enumerate(path.read_text(encoding='utf-8').splitlines(), 1):
        if FENCE_RE.match(line):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        m = HEADING_RE.match(line)
        if not m:
            continue
        heading = m.group(3).strip()
        found = []
        for word, rx in COMPILED:
            if rx.search(heading):
                found.append(word)
        if found:
            hits.append({'line': i, 'words': found, 'heading': heading[:160]})
    return hits


def chapter_id(path: Path) -> str:
    m = re.match(r'(ch\d+[_\w]*)', path.stem)
    return m.group(1) if m else path.stem


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', action='store_true', help='写 build/title_style_lint.json')
    ap.add_argument('--porcelain', action='store_true',
                    help='仅输出 chapter|line|words|heading 便于管道处理')
    args = ap.parse_args()

    files = sorted(BOOK.rglob('ch*.md'))
    per_chapter = {}
    total = 0
    for f in files:
        h = scan_file(f)
        if h:
            per_chapter[chapter_id(f)] = h
            total += len(h)

    if args.porcelain:
        for cid, hits in per_chapter.items():
            for hit in hits:
                print(f"{cid}|{hit['line']}|{','.join(hit['words'])}|{hit['heading']}")
        return

    print("=" * 70)
    print(f"P3 AI 风格标题词审计  —  命中 {total} 处 / {len(per_chapter)} 章")
    print("=" * 70)
    for cid, hits in per_chapter.items():
        print(f"\n### {cid}  ({len(hits)} 处)")
        for hit in hits:
            print(f"  L{hit['line']:<5} [{','.join(hit['words'])}]  {hit['heading']}")
    print("\n" + "=" * 70)
    print("说明：只报候选，不判罪。triage 时决定保留(信息量足)或改写(去营销)。")
    print("=" * 70)

    if args.json:
        out = ROOT / 'build' / 'title_style_lint.json'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(
            {'total': total, 'chapters': per_chapter},
            ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"\n[json] -> {out}")


if __name__ == '__main__':
    main()
