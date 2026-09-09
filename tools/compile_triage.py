#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Compile-failure regression triage.

把「局部扫描报告」与「全量基线」对照，按 block 号（不依赖错误文本）把每章的失败分成三类：

    NEW         = 当前失败、基线未失败的块号  → 我的回归（红；--check 退出码 1）
    PREEXISTING = 当前失败、基线也失败的块号  → 预存坏块（非我引入）
    FIXED       = 基线失败、当前通过的块号    → 我修好了（绿）

典型用法（配合 R2 的 scratch 报告）：

    # 局部扫描（R2 默认把报告写到 tools/.compile_report_partial.json，不污染基线）
    python tools/compile_all.py --only Book/partX/chYY.md --main-only
    # 比对全量基线，有 NEW 回归即 exit 1（可挂 CI / pre-commit）
    python tools/compile_triage.py --check

    # 任意两份报告比对（如旧基线 vs 新基线）
    python tools/compile_triage.py --before old.json --after new.json

⚠️ 为得到有意义的回归判定，partial 的编译 scope 须与 baseline 一致（通常都用
--main-only）。若 partial 用全量、baseline 用 --main-only，全量中的预存非-main
坏块会误报为 NEW（它们本就不进 main-only 基线）。
"""
import argparse
import json
import sys
from typing import Dict, Set

DEFAULT_BASELINE = 'tools/compile_report.json'
DEFAULT_PARTIAL = 'tools/.compile_report_partial.json'


def load(path: str) -> dict:
    with open(path, encoding='utf-8') as f:
        data: dict = json.load(f)
    return data


def _norm_path(p: str) -> str:
    """归一化路径分隔符（基线可能在 Windows 生成含反斜杠，局部扫描用正斜杠）。"""
    return (p or '').replace('\\', '/')


def fails_by_path(report: dict) -> Dict[str, Set[int]]:
    """{path: {失败块号集合}}。"""
    out: Dict[str, Set[int]] = {}
    for entry in report.get('failures', []):
        p = _norm_path(entry.get('path') or entry.get('file') or '')
        if not p:
            continue
        blocks = {
            fr.get('block')
            for fr in entry.get('failures', [])
            if fr.get('block') is not None
        }
        # 合并（同 path 可能分多条 entry 时不常见，但稳妥）
        out.setdefault(p, set()).update(blocks)
    return out


def error_by_block(report: dict) -> Dict[str, Dict[int, str]]:
    """{path: {block: error_text}}，用于打印 NEW 块的错误片段。"""
    out: Dict[str, Dict[int, str]] = {}
    for entry in report.get('failures', []):
        p = _norm_path(entry.get('path') or entry.get('file') or '')
        if not p:
            continue
        out[p] = {
            fr.get('block'): (fr.get('error') or '')
            for fr in entry.get('failures', [])
            if fr.get('block') is not None
        }
    return out


def short_err(text: str, limit: int = 90) -> str:
    t = (text or '').replace('\n', ' ').strip()
    return t if len(t) <= limit else t[:limit] + '…'


def triage(base: dict, cur: dict) -> dict:
    base_fails = fails_by_path(base)
    cur_fails = fails_by_path(cur)
    cur_err = error_by_block(cur)

    scanned = [_norm_path(x) for x in
               (cur.get('processed_paths') or sorted(cur_fails.keys()))]
    assessed = set(scanned)
    not_scanned = sorted(set(base_fails) - assessed)

    details = []
    tot_new = tot_pre = tot_fixed = 0
    for p in scanned:
        b = base_fails.get(p, set())
        c = cur_fails.get(p, set())
        new = sorted(c - b)
        pre = sorted(c & b)
        fixed = sorted(b - c)
        tot_new += len(new)
        tot_pre += len(pre)
        tot_fixed += len(fixed)
        if new or fixed or pre:
            details.append({
                'path': p,
                'new': new,
                'preexisting': pre,
                'fixed': fixed,
                'new_errors': {blk: short_err(cur_err.get(p, {}).get(blk, ''))
                               for blk in new},
            })

    return {
        'baseline': base.get('__source__'),
        'partial': cur.get('__source__'),
        'scanned': scanned,
        'not_scanned': not_scanned,
        'details': details,
        'total_new': tot_new,
        'total_preexisting': tot_pre,
        'total_fixed': tot_fixed,
    }


def render(result: dict, quiet: bool) -> str:
    lines = []
    lines.append('=== Compile Triage (partial vs baseline) ===')
    scanned = result['scanned']
    not_scanned = result['not_scanned']
    lines.append(f'扫描章节 : {len(scanned)} 章'
                 + (f'（基线未扫描 {len(not_scanned)} 章不评估）' if not_scanned else ''))
    lines.append('')

    for d in result['details']:
        name = d['path'].split('/')[-1]
        if d['new']:
            blocks = ', '.join(f'#{b}' for b in d['new'])
            lines.append(f'[回归 NEW] {name}: {blocks}')
            for b in d['new']:
                lines.append(f'    block #{b}: {d["new_errors"].get(b, "")}')
        if d['fixed']:
            blocks = ', '.join(f'#{b}' for b in d['fixed'])
            lines.append(f'[已修 FIXED] {name}: {blocks}')
        if not quiet and d['preexisting'] and not d['new'] and not d['fixed']:
            blocks = ', '.join(f'#{b}' for b in d['preexisting'])
            lines.append(f'[预存 PREEXISTING] {name}: {blocks}')
        elif d['preexisting'] and (d['new'] or d['fixed']):
            lines.append(f'    （另含预存 {len(d["preexisting"])} 块：'
                         + ', '.join(f'#{b}' for b in d['preexisting']) + '）')

    if not any((d['new'] or d['fixed'] or d['preexisting'])
               for d in result['details']):
        lines.append('（扫描章节无失败记录）')

    lines.append('')
    lines.append(f'汇总: NEW={result["total_new"]}  '
                 f'PREEXISTING={result["total_preexisting"]}  '
                 f'FIXED={result["total_fixed"]}')
    return '\n'.join(lines)


def main() -> int:
    ap = argparse.ArgumentParser(
        description='编译失败回归 triage（区分预存坏块 vs 我的回归）')
    ap.add_argument('--baseline', default=DEFAULT_BASELINE,
                    help=f'全量基线报告（默认 {DEFAULT_BASELINE}）')
    ap.add_argument('--partial', default=DEFAULT_PARTIAL,
                    help=f'局部扫描报告（默认 {DEFAULT_PARTIAL}，R2 scratch）')
    ap.add_argument('--before', help='比对模式：旧报告路径')
    ap.add_argument('--after', help='比对模式：新报告路径')
    ap.add_argument('--check', action='store_true',
                    help='存在 NEW 回归则退出码 1（可挂 CI / pre-commit）')
    ap.add_argument('--json-out', help='把 triage 结果另写 json')
    ap.add_argument('--quiet', action='store_true',
                    help='仅列出含 NEW/FIXED 的章节，省略纯预存章节明细')
    ap.add_argument('--strict', action='store_true',
                    help='--check 时把 PREEXISTING 也视为失败（exit 1）')
    args = ap.parse_args()

    if args.before and args.after:
        try:
            base = load(args.before)
            cur = load(args.after)
        except Exception as e:
            print(f'[triage] 无法读取报告: {e}', file=sys.stderr)
            return 2
        base = {'__source__': args.before, **base}
        cur = {'__source__': args.after, **cur}
    else:
        try:
            base = load(args.baseline)
            cur = load(args.partial)
        except FileNotFoundError as e:
            print(f'[triage] 报告不存在: {e}（先跑 compile_all.py 生成）',
                  file=sys.stderr)
            return 2
        except Exception as e:
            print(f'[triage] 无法读取报告: {e}', file=sys.stderr)
            return 2
        base = {'__source__': args.baseline, **base}
        cur = {'__source__': args.partial, **cur}

    result = triage(base, cur)
    text = render(result, args.quiet)
    print(text)

    if args.json_out:
        try:
            with open(args.json_out, 'w', encoding='utf-8') as f:
                json.dump(result, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f'[triage] 写 json 失败: {e}', file=sys.stderr)

    if args.check:
        if result['total_new'] > 0:
            print(f'[triage] FAIL: 检测到 {result["total_new"]} 个新增回归块',
                  file=sys.stderr)
            return 1
        if args.strict and result['total_preexisting'] > 0:
            print(f'[triage] FAIL(--strict): 仍有 {result["total_preexisting"]} '
                  f'个预存坏块未清零', file=sys.stderr)
            return 1
        print('[triage] ✅ 无新增回归')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
