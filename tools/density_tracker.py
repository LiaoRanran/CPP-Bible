#!/usr/bin/env python3
"""density_tracker.py — Density Evolution Tracker
Saves audit snapshots to .workbuddy/density_history.json and shows trends.

Usage: python3 tools/density_tracker.py            # save snapshot + show trend
       python3 tools/density_tracker.py --history  # show history only (no save)"""

import os, re, sys, json
from datetime import datetime
from collections import Counter

HISTORY_FILE = '.workbuddy/density_history.json'

DIMENSIONS = {
    'A.基础': [r'定义', r'基本语法', r'使用方式', r'注意事项'],
    'B.原理': [r'历史背景', r'设计目标', r'标准演化', r'WG21', r'Proposal', r'P\d{4}'],
    'C.编译器': [r'GCC\s*(实现|13|处理|编译)', r'Clang\s*实现', r'MSVC\s*实现', r'ABI', r'Name Mangling', r'汇编'],
    'D.标准库': [r'libstdc\x2b\x2b', r'libc\x2b\x2b', r'Microsoft STL', r'源码区别', r'实现权衡'],
    'E.底层': [r'assembly', r'寄存器', r'Stack', r'Heap', r'Cache', r'TLB', r'NUMA', r'False Sharing', r'Branch Prediction'],
    'F.工业': [r'Google', r'LLVM', r'Chromium', r'Qt\s', r'Boost', r'Abseil', r'Unreal', r'fmt', r'spdlog', r'Redis', r'ClickHouse', r'RocksDB', r'Eigen', r'folly'],
    'G.性能': [r'benchmark', r'Complexity', r'CPU Cost', r'Allocation Cost', r'ns', r'cycles', r'latency', r'overhead'],
    'H.设计': [r'Design Pattern', r'Anti.?Pattern', r'Trade.?off', r'API Design', r'反模式', r'设计取舍', r'设计权衡'],
    'I.实战': [r'工业案例', r'常见Bug', r'Debug方法', r'Code Review', r'重构建议', r'production'],
    'J.学习': [r'面试', r'FAQ', r'Exercise', r'Reading', r'Source Guide'],
}

DEPTH = {
    'code_blocks': r'```cpp',
    'tables': r'\|.*\|.*\|',
    'assembly': r'\b(mov|lea|call|ret|jmp|cmp|add|sub|xor|push|pop|lock|mfence)\b',
    'wg21_ids': r'(P|N)\d{4}R?\d*',
    'comparisons': r'vs\b|区别|对比|比较|difference|trade.off',
    'interview': r'面试|Q:|FAQ',
    'warnings': r'陷阱|pitfall|反模式|错误|警告|Bug|UB',
}

def snapshot():
    chapters = {}
    for r,d,f in os.walk('Book/'):
        if '_legacy' in r: continue
        for ff in sorted(f):
            if not ff.endswith('.md'): continue
            path = r+'/'+ff
            text = open(path, encoding='utf-8').read()
            dim = sum(min(sum(1 for kw in kws if re.search(kw, text, re.I)), 3) for kws in DIMENSIONS.values())
            depth = sum(min(len(re.findall(p, text, re.I)), 5) for p in DEPTH.values())
            chapters[ff] = int(dim * 0.6 + depth * 0.4 * 0.6)

    snap = {
        'timestamp': datetime.now().isoformat(),
        'avg': sum(chapters.values()) / len(chapters),
        'min': min(chapters.values()),
        'max': max(chapters.values()),
        'distribution': dict(Counter(chapters.values())),
    }
    return snap

def main():
    if not os.path.exists(HISTORY_FILE):
        with open(HISTORY_FILE, 'w') as f: json.dump([], f)

    history = json.load(open(HISTORY_FILE))

    if '--history' not in sys.argv:
        snap = snapshot()
        history.append(snap)
        with open(HISTORY_FILE, 'w') as f: json.dump(history, f, indent=2)
        print(f'Snapshot saved: {snap["timestamp"]}')

    # Show trend
    if len(history) >= 1:
        last = history[-1]
        print(f'\nCurrent: avg={last["avg"]:.1f}/30  min={last["min"]}  max={last["max"]}')

    if len(history) >= 2:
        prev = history[-2]
        delta = last['avg'] - prev['avg']
        print(f'Previous: avg={prev["avg"]:.1f}/30  Δ={delta:+.1f}')

        if len(history) >= 3:
            print('\nTrend:')
            for h in history[-5:]:
                print(f'  {h["timestamp"][:16]}  avg={h["avg"]:.1f}/30  min={h["min"]}')

if __name__ == '__main__':
    main()
