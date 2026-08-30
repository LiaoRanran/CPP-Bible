#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""d5_appendix_audit.py — D5 性能附录四段结构审计（报告型，不入 CI 门禁）

为什么需要这个轮子
==================
D5 性能附录是本书的"非显然性能真相"载体，全库 57+ 章已铺开。附录有严格约定的
四段结构（模板见 ch41 L2172）：

  ## 附录 D5：真实基准与性能分析 — <主题>（GCC 15.3.0）
  > 测试环境…本附录目的…**绝对毫秒随机器而变，加速比才是可移植信号。**
  ### D5.1 基准结果
  ### D5.2 非显然结论
  ### D5.3 可复现 demo   ← 恰好 1 个 ```cpp 块，且内部 `<<"\n"` 须改 `<<std::endl`
  ### D5.4 方法学注

历史踩坑（写进 MEMORY.md 红线与关键教训）：
- 子 agent 派发 Wave 5/6 时，附录四段结构、标题、blockquote 行容易漏写或被改写
  （如 ch47 用"下一节 可复现 demo"/"最后 方法学注"非标准标题，blockquote 措辞也变体）。
- demo 内 `<< "\n"` 必须 `<< std::endl`（LaTeX 安全），曾有章节漏改。
- "基准源文件：`xxx.cpp`" 措辞会触发 consistency 的 SRC_FILE_RE（`文件[:：]\s*\S+`）
  WARN（因为全文无 `行号：` 配对）。正确写法是"基准源码见库根 `xxx.cpp`"。
- D5.3 引用的 `_bench_d5_*.cpp` 必须在库根真实存在，否则读者无法复现。

本工具是**收口与巡检的地基**：扫全库所有含"附录 D5"的章节，逐项校验上述结构，
输出报告供人工 triage。只读 `Book/`，绝不修改源文件。

严重级语义
==========
- ERROR：结构断裂，必须修（缺段、D5.3 cpp 数≠1、`<<"\n"` 违规、bench 文件缺失、缺 GCC 标签）。
- WARN ：偏离模板但内容可能正确（非标准段标题、blockquote 措辞变体、"基准源文件："措辞）。
- INFO ：未提交残留（bench 文件在库根但未被 git 跟踪），非缺陷，提示收口。

用法
====
  python3 tools/d5_appendix_audit.py                 # 人类可读报告
  python3 tools/d5_appendix_audit.py --porcelain     # 仅 issue 行，便于 grep
  python3 tools/d5_appendix_audit.py --json          # 写 build/d5_appendix_audit.json
"""
import re
import sys
import json
import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / 'Book'

D5_HEADER_RE = re.compile(r'^##\s+附录 D5：真实基准与性能分析')
# GCC 标签：接受全角（GCC 15.3.0）或半角 (GCC 15.3.0)，仅"完全缺标签"才报错
GCC_TAG_RE = re.compile(r'[（(]GCC\s*15\.3\.0[)）]')
TOP_H2_RE = re.compile(r'^##\s+')
SUBSEC_RE = re.compile(r'^###\s+D5\.([1-4])\b')
BLOCKQUOTE_SIG = '绝对毫秒随机器而变，加速比才是可移植信号。'
# 允许缩进围栏：开/闭都是 ```` ``` ````，可能前有空格
FENCE_RE = re.compile(r'^(\s*)```(.*)$')
BAD_WORDING_RE = re.compile(r'基准源文件[：:]')
BENCH_RE = re.compile(r'_bench_d5_[A-Za-z0-9_]+\.cpp')
# demo 内禁止 `<< "\n"` / `<<"\n"` / `<< '\n'`（须 `<<std::endl`）
SINK_BAD_RE = re.compile(r'<<\s*["\']\\n["\']')

SEV_ORDER = {'ERROR': 0, 'WARN': 1, 'INFO': 2}


def tracked_files():
    """返回 git 已跟踪文件集合（相对仓库根）。"""
    try:
        out = subprocess.run(
            ['git', '-C', str(ROOT), 'ls-files'],
            capture_output=True, text=True, timeout=30)
        return set(out.stdout.splitlines())
    except Exception:
        return set()


def audit_region(lines, chapter):
    """对单个附录区域做结构校验，返回 issue 列表。"""
    issues = []

    # 1) 标题 GCC 15.3.0 标签（仅完全缺失才 ERROR）
    hdr = lines[0]
    if not GCC_TAG_RE.search(hdr):
        issues.append(('ERROR', 'HDR_GCC_TAG',
                        f'{chapter}: 附录标题缺 GCC 15.3.0 标签 -> {hdr.strip()[:80]}'))

    # 2) blockquote 环境行
    has_block = any(l.strip().startswith('>') for l in lines)
    has_sig = any(l.strip().startswith('>') and BLOCKQUOTE_SIG in l for l in lines)
    if not has_block:
        issues.append(('ERROR', 'MISSING_BLOCKQUOTE',
                        f'{chapter}: 附录缺 `>` blockquote 环境行'))
    elif not has_sig:
        issues.append(('WARN', 'BLOCKQUOTE_WORDING',
                        f'{chapter}: blockquote 缺标准签名句'
                        f'"{BLOCKQUOTE_SIG}"（措辞变体，建议统一）'))

    # 3) 四段完整性
    present = set()
    for l in lines:
        m = SUBSEC_RE.match(l)
        if m:
            present.add('D5.' + m.group(1))
    for sec in ('D5.1', 'D5.2'):
        if sec not in present:
            issues.append(('ERROR', 'MISSING_SECTION',
                            f'{chapter}: 缺 {sec} 小节（四段结构要求 D5.1-D5.4 齐全）'))

    h3 = [(i, l) for i, l in enumerate(lines) if re.match(r'^###\s+', l)]

    def find_sec(headers, semantic_re, std_prefix):
        for i, l in headers:
            if semantic_re.search(l):
                return i, l, True
        for i, l in headers:
            if re.match(std_prefix, l):
                return i, l, False
        return None, None, False

    demo_sem = re.compile(r'可复现\s*(demo|演示)|验证\s*(demo|演示)')
    method_sem = re.compile(r'方法学注')
    d53_idx, d53_line, d53_via_sem = find_sec(h3, demo_sem, r'^###\s+D5\.3\b')
    d54_idx, d54_line, d54_via_sem = find_sec(h3, method_sem, r'^###\s+D5\.4\b')

    # D5.3 编号但内容非 demo（如 ch108 把"非显然结论"误标为 D5.3）
    for i, l in h3:
        if re.match(r'^###\s+D5\.3\b', l) and not demo_sem.search(l):
            issues.append(('WARN', 'D53_MISLABELED',
                            f'{chapter}: "### D5.3" 段内容非 demo（须为可复现 demo）'
                            f' -> {l.strip()[:60]}'))
    for i, l in h3:
        if re.match(r'^###\s+D5\.4\b', l) and not method_sem.search(l):
            issues.append(('WARN', 'D54_MISLABELED',
                            f'{chapter}: "### D5.4" 段内容非方法学注'
                            f' -> {l.strip()[:60]}'))

    if d53_idx is None:
        issues.append(('ERROR', 'MISSING_DEMO',
                        f'{chapter}: 缺 D5.3 可复现 demo 小节'))
    else:
        if not d53_via_sem:
            issues.append(('WARN', 'D53_NONSTD_NAME',
                            f'{chapter}: D5.3 段标题非标准（须 "### D5.3 可复现 demo"）'
                            f' -> {d53_line.strip()[:60]}'))
        # D5.3 区域：到下一个 `### ` 或区域末
        d53_end = len(lines)
        for k in range(d53_idx + 1, len(lines)):
            if re.match(r'^###\s+', lines[k]):
                d53_end = k
                break
        sub = lines[d53_idx:d53_end]
        cpp_count = 0
        sink_hits = []
        in_fence = False
        fence_lang = ''
        for l in sub:
            m = FENCE_RE.match(l)
            if m:
                if not in_fence:
                    in_fence = True
                    fence_lang = m.group(2).strip()
                    if fence_lang == 'cpp':
                        cpp_count += 1
                else:
                    in_fence = False
                    fence_lang = ''
                continue
            if in_fence and fence_lang == 'cpp':
                if SINK_BAD_RE.search(l):
                    sink_hits.append(l.strip()[:120])
        if cpp_count != 1:
            issues.append(('ERROR', 'D53_CPP_COUNT',
                            f'{chapter}: D5.3 内 cpp demo 数 = {cpp_count}（约定恰好 1 个）'))
        for s in sink_hits:
            issues.append(('ERROR', 'D53_BAD_SINK',
                            f'{chapter}: D5.3 demo 内发现 `<<"\\n"`（须改 `<<std::endl`）-> {s}'))

    if d54_idx is None:
        issues.append(('ERROR', 'MISSING_METHOD',
                        f'{chapter}: 缺 D5.4 方法学注小节'))
    elif not d54_via_sem:
        issues.append(('WARN', 'D54_NONSTD_NAME',
                        f'{chapter}: D5.4 段标题非标准（须 "### D5.4 方法学注"）'
                        f' -> {d54_line.strip()[:60]}'))

    # 4) "基准源文件：" 措辞坑（触发 consistency WARN）
    for i, l in enumerate(lines, 1):
        if BAD_WORDING_RE.search(l):
            issues.append(('WARN', 'BAD_WORDING',
                            f'{chapter}: 使用"基准源文件："措辞（建议改"基准源码见库根 `xxx.cpp`"）'
                            f' -> L{i}: {l.strip()[:80]}'))

    # 5) 引用的 _bench_d5_*.cpp 存在性 + 跟踪状态
    benches = sorted(set(BENCH_RE.findall('\n'.join(lines))))
    if benches:
        tracked = tracked_files()
        for b in benches:
            p = ROOT / b
            if not p.exists():
                issues.append(('ERROR', 'BENCH_MISSING',
                                f'{chapter}: 引用的基准源文件不存在于库根 -> {b}'))
            elif b not in tracked:
                issues.append(('INFO', 'BENCH_UNTRACKED',
                                f'{chapter}: 基准源文件在库根但未被 git 跟踪（未提交）-> {b}'))
    return issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--json', action='store_true', help='写 build/d5_appendix_audit.json')
    ap.add_argument('--porcelain', action='store_true', help='仅输出 issue 行便于管道')
    args = ap.parse_args()

    files = sorted(BOOK.rglob('ch*.md'))
    all_issues = []
    chapters_with_d5 = 0
    for f in files:
        text = f.read_text(encoding='utf-8')
        if '附录 D5：真实基准与性能分析' not in text:
            continue
        lines = text.splitlines()
        starts = [i for i, l in enumerate(lines) if D5_HEADER_RE.match(l)]
        if not starts:
            continue
        chapters_with_d5 += 1
        m = re.match(r'(ch\d+[_\w]*)', f.stem)
        chapter = m.group(1) if m else f.stem
        for s in starts:
            region_end = len(lines)
            for j in range(s + 1, len(lines)):
                if TOP_H2_RE.match(lines[j]):
                    region_end = j
                    break
            issues = audit_region(lines[s:region_end], chapter)
            all_issues.extend(issues)

    all_issues.sort(key=lambda x: (SEV_ORDER.get(x[0], 9), x[1]))

    if args.porcelain:
        for sev, code, detail in all_issues:
            print(f"{sev}|{code}|{detail}")
        return

    counts = {'ERROR': 0, 'WARN': 0, 'INFO': 0}
    for sev, _, _ in all_issues:
        counts[sev] = counts.get(sev, 0) + 1

    print("=" * 72)
    print(f"D5 性能附录结构审计  —  含 D5 附录 {chapters_with_d5} 章，"
          f"issue {len(all_issues)} 条")
    print(f"  ERROR={counts['ERROR']}  WARN={counts['WARN']}  INFO={counts['INFO']}")
    print("=" * 72)
    if not all_issues:
        print("  全部 D5 附录结构合规 ✅")
    else:
        cur = None
        for sev, code, detail in all_issues:
            if sev != cur:
                print(f"\n[{sev}]")
                cur = sev
            print(f"  {code:<18} {detail}")
    print("\n" + "=" * 72)
    print("说明：ERROR 必须修；WARN 为模板偏离建议（内容可能正确）；"
          "INFO 为未提交残留提示。")
    print("=" * 72)

    if args.json:
        out = ROOT / 'build' / 'd5_appendix_audit.json'
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(json.dumps(
            {'chapters_with_d5': chapters_with_d5, 'counts': counts,
             'issues': [{'sev': s, 'code': c, 'detail': d} for s, c, d in all_issues]},
            ensure_ascii=False, indent=2), encoding='utf-8')
        print(f"\n[json] -> {out}")

    # CI gate: exit 1 if any ERROR-level issue
    if counts['ERROR'] > 0:
        sys.exit(1)
        print(f"\n[json] -> {out}")


if __name__ == '__main__':
    main()
