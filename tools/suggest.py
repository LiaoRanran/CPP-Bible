#!/usr/bin/env python3
"""suggest.py — Content Suggestion Engine
Given a chapter, scans its weak dimensions and suggests specific content to add.

Usage: python3 tools/suggest.py Book/partXX_YY/chZZZ.md
       python3 tools/suggest.py --batch 5   # suggest for 5 weakest chapters"""

import os, re, sys

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

SUGGESTIONS = {
    'B.原理': '追加WG21提案号(PxxxxRxx) + 历史背景(为什么这个特性存在) + C++标准版本演化的影响。表格形式: | 版本 | 提案 | 内容 |',
    'C.编译器': '追加GCC/Clang/MSVC的实现差异表 + Name Mangling示例 + 关键ABI影响',
    'D.标准库': '追加libstdc++ vs libc++ vs MS STL对比表 + 源码阅读入口(文件+行数)',
    'E.底层': '追加汇编代码块(带mov/call/ret指令) + 性能数据(ns/cycles) + Cache/TLB影响分析',
    'F.工业': '追加Google/LLVM/Chromium/Qt/Boost至少3个项目如何使用该特性 + 为什么用/为什么不用',
    'G.性能': '追加benchmark数据(真实数值, ns/us级别) + 复杂度分析 + 与其他方案的性能对比表',
    'H.设计': '追加Trade-off表(| 方案 | 优点 | 缺点 | 适用 |) + 反模式警示(至少3个)',
    'I.实战': '追加工业故障案例 + Debug方法 + Code Review Checklist',
    'J.学习': '追加面试Q&A(至少3题) + 推荐阅读 + 练习题建议',
}

def suggest_chapter(path):
    text = open(path, encoding='utf-8').read()
    weak = []
    for dim, keywords in DIMENSIONS.items():
        hits = sum(1 for kw in keywords if re.search(kw, text, re.IGNORECASE))
        if hits < 1:
            weak.append((dim, SUGGESTIONS.get(dim, '')))
    return weak

def main():
    if '--batch' in sys.argv:
        try:
            n = int(sys.argv[sys.argv.index('--batch') + 1])
        except:
            n = 5
        # Find N weakest chapters
        chaps = []
        for r,d,f in os.walk('Book/'):
            if '_legacy' in r: continue
            for ff in sorted(f):
                if not ff.endswith('.md'): continue
                path = r+'/'+ff
                weak = suggest_chapter(path)
                chaps.append((len(weak), path, weak))
        chaps.sort(key=lambda x: -x[0])
        for i, (nweak, path, weak) in enumerate(chaps[:n]):
            name = os.path.basename(path)
            print(f'\n## {i+1}. {name} ({nweak} zero dims)')
            for dim, suggestion in weak:
                print(f'  [{dim}] {suggestion[:120]}...')
    else:
        path = sys.argv[1]
        weak = suggest_chapter(path)
        print(f'{os.path.basename(path)}: {len(weak)} zero dimensions:')
        for dim, suggestion in weak:
            print(f'  [{dim}] {suggestion}')

if __name__ == '__main__':
    main()
