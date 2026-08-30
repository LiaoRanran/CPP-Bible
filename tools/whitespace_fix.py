#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
whitespace_fix.py — 围栏感知的空白符卫生修复（确定性，单文件幂等）

修复三类 Markdown 标准门禁缺陷（MD009 / MD012），均围栏感知、保原生换行、
零语义变更：
  W1 行尾空格：剥离围栏外每行的尾部空白。
  W2 连续空行：围栏外 2+ 连续空行折叠为 1（代码块内空行原样保留）。
  W3 末尾换行：确保文件以恰好一个换行结尾，且首尾无多余空行。

用法：
  python3 tools/whitespace_fix.py [--root Book] [--dir <d>] [--apply] [--json out.json]
默认只读（dry-run），打印将变更的文件与计数；--apply 才落盘。
"""
import os
import re
import json
import argparse
import sys

FENCE_RE = re.compile(r'^(`{3,}|~{3,})')
H_RE = re.compile(r'^(#{1,6})\s')

def fix_text(raw):
    """返回 (new_text, {w1,w2,w3})。无变更时 new_text==raw。"""
    had_cr = '\r\n' in raw
    nl = '\r\n' if had_cr else '\n'
    lines = raw.split(nl)
    if raw.endswith(nl):
        lines = lines[:-1]  # 去掉末尾空切分
    out = []
    in_fence = False
    prev_blank = False
    counts = {'w1': 0, 'w2': 0, 'w3': 0}
    started = False
    for l in lines:
        fm = FENCE_RE.match(l)
        if fm:
            in_fence = not in_fence
            prev_blank = False
            started = True
            out.append(l)
            continue
        if in_fence:
            prev_blank = False
            out.append(l)
            continue
        stripped = l.rstrip()
        if stripped == '':
            if not started:
                continue  # 丢弃文件开头空行
            if prev_blank:
                counts['w2'] += 1
                continue  # 折叠多余空行
            prev_blank = True
            out.append('')
            continue
        # 非空行
        if l != stripped:
            counts['w1'] += 1
        prev_blank = False
        started = True
        out.append(stripped)
    # 去掉尾部空行
    while out and out[-1] == '':
        out.pop()
        counts['w3'] += 1
    new_text = nl.join(out) + nl
    if new_text != raw:
        # w3 仅在确实因末尾缺换行/多余空行变化时才记；上面 pop 已计
        return new_text, counts
    return raw, {'w1': 0, 'w2': 0, 'w3': 0}

def collect(root):
    fs = []
    for dp, _, fns in os.walk(root):
        for fn in fns:
            if fn.startswith('ch') and fn.endswith('.md'):
                fs.append(os.path.join(dp, fn))
    return sorted(fs)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default='Book')
    ap.add_argument('--dir', default=None)
    ap.add_argument('--apply', action='store_true')
    ap.add_argument('--json', default=None)
    ap.add_argument('--check', action='store_true',
                    help="gate mode: exit 1 if any whitespace defect (W1/W2/W3) would be fixed")
    args = ap.parse_args()

    if args.dir:
        files = sorted(os.path.join(args.dir, f) for f in os.listdir(args.dir)
                       if f.startswith('ch') and f.endswith('.md'))
    else:
        files = collect(args.root)

    changed = {}
    for fp in files:
        raw = open(fp, encoding='utf-8', errors='replace').read()
        new_text, counts = fix_text(raw)
        if new_text != raw:
            changed[fp] = counts
            if args.apply:
                with open(fp, 'w', encoding='utf-8', newline='') as f:
                    f.write(new_text)
    total = {'w1': 0, 'w2': 0, 'w3': 0}
    for c in changed.values():
        for k in total:
            total[k] += c[k]
    mode = 'APPLY' if args.apply else 'dry-run'
    print(f"[{mode}] files_changed={len(changed)} totals={total}", file=__import__('sys').stderr)
    for fp, c in sorted(changed.items()):
        print(f"{fp}: w1={c['w1']} w2={c['w2']} w3={c['w3']}")
    if args.json:
        with open(args.json, 'w', encoding='utf-8', newline="\n") as f:
            json.dump(changed, f, ensure_ascii=False, indent=2)

    if args.check:
        sys.exit(1 if changed else 0)

if __name__ == '__main__':
    main()
