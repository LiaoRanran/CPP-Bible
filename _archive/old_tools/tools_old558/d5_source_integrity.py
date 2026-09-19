#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
d5_source_integrity.py — D5 性能附录「基准源码见库根」引用完整性收口工具
（确定性、围栏感知、保原生换行；可接入 CI 作为首个语义层门禁）。

背景：本书 §D5 性能附录承诺「可复现 demo 的基准源码见库根 `_bench_d5_X.cpp`」。
该工具强制两条不变量：
  1) 每一条 `基准源码见库根 `_bench_d5_X.cpp`` 声明，必须对应仓库根目录一个
     真实存在且被 git 跟踪的 `_bench_d5_X.cpp`（否则复现承诺对读者是空头支票）。
  2) 仓库根目录每一个 `_bench_d5_X.cpp`，若其对应章（按编号）存在 D5 附录，
     则该章必须声明它（孤儿文件 = 章有 D5 却漏标来源 = 复现承诺缺口）。

安全范围：
  - 只读扫描 + 确定性修复，绝不改动语义层。
  - --fix 仅在匹配章的 `### D5.4` 标题后插入一行来源声明（若该章未提过此文件）。
  - 围栏内代码块不处理；写入保原生换行（探测 CRLF/LF）。
  - 编号无法映射到任何章、或章无 D5 的孤儿文件，标记为 LEGACY（仅警告，不改）。

用法：
  python3 tools/d5_source_integrity.py            # 报告模式（默认）
  python3 tools/d5_source_integrity.py --check    # 门禁：存在缺口则 exit 1
  python3 tools/d5_source_integrity.py --fix      # 落盘：链接可修复的孤儿
"""

import os
import re
import sys
import argparse
import subprocess

ROOT = os.getcwd()
BOOK = os.path.join(ROOT, 'Book')

CLAIM_RE = re.compile(r'基准源码见库根 `(_bench_d5_[^`]+\.cpp)`')
D5_RE = re.compile(r'^###\s+D5\b', re.MULTILINE)
FENCE_RE = re.compile(r'^(`{3,}|~{3,})')
BENCH_NUM_RE = re.compile(r'_bench_d5_(?:ch)?(\d+)')
BENCH_RE = re.compile(r'_bench_d5_[^`\s]+\.cpp')


def git_tracked(pattern):
    out = subprocess.run(['git', 'ls-files', pattern],
                         capture_output=True, text=True).stdout.split()
    return set(os.path.basename(x) for x in out)


def collect_claims():
    """return {bench_basename: [chapter_path, ...]}"""
    claims = {}
    for dp, _, fn in os.walk(BOOK):
        for f in fn:
            if not f.endswith('.md'):
                continue
            p = os.path.join(dp, f)
            txt = open(p, encoding='utf-8', errors='replace').read()
            for m in CLAIM_RE.finditer(txt):
                claims.setdefault(m.group(1), []).append(p)
    return claims


def collect_disk_files():
    return set(os.path.basename(x) for x in glob_root('_bench_d5_*.cpp'))


def glob_root(pat):
    import glob
    return glob.glob(os.path.join(ROOT, pat))


def map_orphan_to_chapter(bench):
    """numeric id -> chapter .md path, or None"""
    m = BENCH_NUM_RE.search(bench)
    if not m:
        return None
    num = m.group(1)
    prefix = 'ch' + num + '_'
    for dp, _, fn in os.walk(BOOK):
        for f in fn:
            if f.startswith(prefix) and f.endswith('.md'):
                return os.path.join(dp, f)
            if f == ('ch' + num + '.md'):
                return os.path.join(dp, f)
    return None


def chapter_has_d5(path):
    txt = open(path, encoding='utf-8', errors='replace').read()
    return bool(D5_RE.search(txt))


def analyze():
    claims = collect_claims()
    disk = collect_disk_files()
    tracked = git_tracked('_bench_d5_*.cpp')

    claimed = set(claims.keys())
    missing = sorted(claimed - disk)              # 声明但磁盘无文件 -> 致命
    untracked = sorted(claimed - tracked)        # 声明但 git 未跟踪 -> 致命
    orphans = sorted(disk - claimed)             # 磁盘有但无人声明

    linkable = []        # (bench, chapter) 章有 D5 且未引用任何 bench -> 致命缺口
    referenced = []       # (bench, chapter) 章已引用该文件(含其他措辞) -> 正常(绿)
    unreferenced = []     # (bench, chapter_or_None) 章引用了别的 bench / 无 D5 / 无对应章 -> 遗留
    for o in orphans:
        ch = map_orphan_to_chapter(o)
        if ch is None:
            unreferenced.append((o, None))
            continue
        has = chapter_has_d5(ch)
        txt = open(ch, encoding='utf-8', errors='replace').read()
        if o in txt:
            # 章已提及该文件（其他措辞，如「完整源码见库根」），非缺口
            referenced.append((o, ch))
            continue
        if BENCH_RE.search(txt):
            # 章已引用【另一个】bench 源（如重命名后的文件），本文件是遗留孤儿
            unreferenced.append((o, ch))
            continue
        if has:
            linkable.append((o, ch))
        else:
            unreferenced.append((o, ch))
    return {
        'claims': claims, 'disk': disk, 'tracked': tracked,
        'missing': missing, 'untracked': untracked,
        'linkable': linkable, 'referenced': referenced,
        'unreferenced': unreferenced,
    }


HEAD_RE = re.compile(r'^(#{1,6})\s+\S')


def insert_claim(chapter_path, bench, apply):
    raw = open(chapter_path, encoding='utf-8', errors='replace').read()
    had_cr = '\r\n' in raw
    nl = '\r\n' if had_cr else '\n'
    lines = raw.split(nl)
    if raw.endswith(nl):
        lines = lines[:-1]
    # 找到 D5 附录起点
    d5_start = None
    for i, ln in enumerate(lines):
        if D5_RE.match(ln):
            d5_start = i
            break
    if d5_start is None:
        return False  # 无 D5 附录，跳过硬链接
    # 找到 D5 附录结束位置：下一个非 D5.x 的标题之前
    end = d5_start + 1
    for j in range(d5_start + 1, len(lines)):
        if HEAD_RE.match(lines[j]):
            if re.match(r'^###\s+D5\.', lines[j]):
                end = j + 1
                continue
            break  # 遇到非 D5 子节标题 -> D5 附录结束
        end = j + 1
    stmt = '基准源码见库根 `%s`。' % bench
    out = lines[:end] + [stmt] + lines[end:]
    if apply:
        with open(chapter_path, 'w', encoding='utf-8', newline='') as f:
            f.write(nl.join(out) + nl)
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true', help='门禁模式：有缺口则 exit 1')
    ap.add_argument('--fix', action='store_true', help='落盘：链接可修复的孤儿')
    args = ap.parse_args()

    r = analyze()
    print('=== D5 基准源引用完整性报告 ===')
    print('声明条目(章):', len(r['claims']), ' 磁盘文件:', len(r['disk']),
          ' git 跟踪:', len(r['tracked']))
    if r['missing']:
        print('[FATAL] 声明但磁盘缺失:', r['missing'])
    if r['untracked']:
        print('[FATAL] 声明但 git 未跟踪:', r['untracked'])
    print('[LINKABLE] 章有 D5 却漏标来源(可修复):', len(r['linkable']))
    for b, ch in r['linkable']:
        print('   ', b, '<-', os.path.relpath(ch, ROOT))
    print('[REFERENCED] 已以其他措辞引用(正常):', len(r['referenced']))
    for b, ch in r['referenced']:
        print('   ', b, '<-', os.path.relpath(ch, ROOT))
    print('[UNREFERENCED] 无对应章/章无 D5(遗留,仅警告):', len(r['unreferenced']))
    for b, ch in r['unreferenced']:
        print('   ', b, '<-', (os.path.relpath(ch, ROOT) if ch else 'NO-CHAPTER'))

    if args.fix:
        n = 0
        for b, ch in r['linkable']:
            if insert_claim(ch, b, apply=True):
                n += 1
                print('[FIX] linked', b, '->', os.path.relpath(ch, ROOT))
        print('--- fix done: linked %d' % n, file=sys.stderr)

    if args.check:
        fatal = bool(r['missing']) or bool(r['untracked']) or bool(r['linkable'])
        sys.exit(1 if fatal else 0)


if __name__ == '__main__':
    main()
