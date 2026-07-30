#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""disclaimer_audit.py — P2 通用免责声明套话审计（报告型，不入 CI 门禁）

为什么需要这个轮子
==================
外部模型双评审（2026-07-30，GPT 总评 80 分 + Claude 对抗审查）给出 P2 优先级：
「免责声明降级治理」——全库存在一批**通用套话免责声明**（如"仅供学习交流"、
"生产环境请谨慎使用"、"不构成任何建议"），它们与具体章节内容脱节，属于
"模板填空"式水词，应逐条**具体化**或**删除**。

本工具是治理的**地基**：扫全库 `Book/` 下所有 `ch*.md`，定位候选通用免责声明
套话出现的 (章节, 行号, 原文)，输出报告供人工 triage。

设计约束（对齐 AGENT.md 红线）
==============================
- 只读 `Book/`，绝不修改源文件。
- 结果只写 stdout + 可选 `--json` 文件，不污染源码树。
- 纯正则解析，秒级完成。
- **本工具只报候选，不判罪**：像 ch108 L288「无锁结构难度极高，生产环境优先
  复用 std::stack+mutex…」这种**带具体内容**的免责声明是高质量教学，不应被
  当作套话删。triage 时靠行号人工区分"通用套话"与"具体警示"。

P2 治理目标（degraded disclaimer → specific）
============================================
对每条命中，人工判断：
  1. 若声明与上下文强相关（点名具体设施/具体风险）→ 保留，并在报告标注 OK。
  2. 若声明是空泛模板 → 删除，或改写为绑定本节的 concrete guidance。

用法
====
  python3 tools/disclaimer_audit.py                 # 人类可读报告
  python3 tools/disclaimer_audit.py --json          # 同时写 build/disclaimer_audit.json
  python3 tools/disclaimer_audit.py --porcelain     # 仅 `chapter|line|matched|text` 便于 grep
"""
import re, sys, json, argparse
from pathlib import Path
from collections import defaultdict

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / 'Book'

# 通用免责声明套话候选模式（中文技术手册常见模板填空）
PATTERNS = [
    (r'仅供学习', '仅供学习'),
    (r'仅供参[考学]', '仅供参考/学'),
    (r'学习交流', '学习交流'),
    (r'不构成.*?(建议|意见|承诺)', '不构成建议'),
    (r'谨慎使用.*?生产', '谨慎使用生产'),
    (r'生产环境.*?(谨慎|慎重|小心|注意|慎用)', '生产环境慎用'),
    (r'自行承担.*?风险', '自行承担风险'),
    (r'风险自负', '风险自负'),
    (r'免责声明', '免责声明(标题/词)'),
    (r'本文档.*?(不对|不保证|不负)', '本文档不保证'),
    (r'仅供参考', '仅供参考'),
    (r'不代表.*?(观点|立场|建议)', '不代表观点'),
    (r'如有.*?(错误|疏漏).*?不负', '如有错误不负责'),
    (r'用途.*?(自负|自行)', '用途自负'),
]

COMPILED = [(re.compile(p, re.I), label) for p, label in PATTERNS]

# 跳过区域：代码块（``` ... ```）内的命中通常是示例代码里的字符串，不是声明。
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
        for rx, label in COMPILED:
            if rx.search(line):
                hits.append({'line': i, 'label': label,
                             'text': line.strip()[:160]})
                break  # 一行只记首个命中，避免重复
    return hits


def chapter_id(path: Path) -> str:
    m = re.match(r'(ch\d+[_\w]*)', path.stem)
    return m.group(1) if m else path.stem


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', action='store_true', help='写 build/disclaimer_audit.json')
    ap.add_argument('--porcelain', action='store_true',
                    help='仅输出 chapter|line|label|text 便于管道处理')
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
                print(f"{cid}|{hit['line']}|{hit['label']}|{hit['text']}")
        return

    print("=" * 70)
    print(f"P2 通用免责声明套话审计  —  命中 {total} 处 / {len(per_chapter)} 章")
    print("=" * 70)
    for cid, hits in per_chapter.items():
        print(f"\n### {cid}  ({len(hits)} 处)")
        for hit in hits:
            print(f"  L{hit['line']:<5} [{hit['label']}]  {hit['text']}")
    print("\n" + "=" * 70)
    print("说明：本工具只报候选，不判罪。triage 时区分")
    print("  - 具体警示（绑定本节内容，保留）")
    print("  - 通用套话（模板填空，应具体化或删除）")
    print("=" * 70)

    if args.json:
        out = ROOT / 'build' / 'disclaimer_audit.json'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(
            {'total': total, 'chapters': per_chapter},
            ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"\n[json] -> {out}")


if __name__ == '__main__':
    main()
