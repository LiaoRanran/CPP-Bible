#!/usr/bin/env python3
"""density_audit.py v3 — Deep Information Density Audit
Key changes from v3:
- Depth signals cap raised 5→15 (rewards chapters with real code)
- New signals: section_density, xref_density, paragraph_depth
- Combined formula: dim 40% + depth 60% (depth matters more)
- Quality gate: actual depth analysis, not just keyword count

Usage: python3 tools/density_audit.py [N] [dim_filter] [part_filter]
       python3 tools/density_audit.py --json  → machine-readable output"""

import os, re, sys, json
from collections import Counter

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

# v3: Depth signals with higher caps and new metrics
DEPTH_SIGNALS = {
    'code_blocks': (r'```cpp', 25),
    'numeric_data': (r'\d+\s*(ns|us|ms|cycles|bytes|KB|MB|GB|GHz|MHz|%)', 15),
    'tables': (r'\|.*\|.*\|', 20),
    'assembly': (r'\b(mov|lea|call|ret|jmp|cmp|add|sub|xor|push|pop|lock|mfence|sfence|lfence|dmb)\b', 15),
    'wg21_ids': (r'(P|N)\d{4}R?\d*', 13),
    'real_projects': (r'Google|LLVM|Chromium|Qt\s|Boost\s|Abseil|Unreal|fmtlib|spdlog|Redis|ClickHouse|RocksDB|Eigen|folly', 13),
    'interview': (r'面试|Q:|FAQ|高频', 15),
    'comparisons': (r'vs\b|区别|对比|比较|difference|Trade.?off|权衡|取舍|优劣', 13),
    'warnings': (r'陷阱|pitfall|反模式|错误|警告|Bug|UB|undefined|CVE', 13),
    'cross_refs': (r'⟶\s*Book/part', 20),
}

# v3 new: Section-level density metrics
SECTION_SIGNALS = {
    'deep_sections': r'^##\s+(附录|第[⑩-⑳]|第\d+节)',  # Appendix and major sections
    'paragraphs_per_section': r'^[A-Z\u4e00-\u9fff]',     # Any content paragraph
}

def audit_chapter(path):
    text = open(path, encoding='utf-8').read()
    lines = text.split('\n')
    
    # Dimension scores (unchanged from v3: 0-3 each, max 30)
    dim_scores = {}
    for dim, keywords in DIMENSIONS.items():
        hits = sum(1 for kw in keywords if re.search(kw, text, re.IGNORECASE))
        dim_scores[dim] = min(hits, 3)
    dim_total = sum(dim_scores.values())
    
    # v3 Depth scores: higher caps, rewards genuine density
    depth_scores = {}
    for signal, (pattern, cap) in DEPTH_SIGNALS.items():
        matches = re.findall(pattern, text, re.IGNORECASE | re.MULTILINE)
        depth_scores[signal] = min(len(matches), cap)
    depth_total = sum(depth_scores.values())  # max ~102 (was 50)
    
    # v3: Section density bonus
    sections = len(re.findall(SECTION_SIGNALS['deep_sections'], text, re.MULTILINE))
    total_lines = len(lines)
    
    # Section density: total lines per major section
    section_count = max(sections, 1)
    avg_section_depth = total_lines / section_count
    
    # v3 Quality gate: shallower threshold (more strict)
    is_shallow = (dim_total >= 10 and depth_total < 8)
    
    # v3 Combined: depth matters MORE (dim 40% + depth 60%)
    # dim max=30, depth max~100 → depth has higher ceiling, rewards genuinely rich chapters
    depth_norm = min(depth_total / 100.0, 1.0)  # normalize to 0-1
    dim_norm = dim_total / 30.0
    
    combined = int((dim_norm * 0.4 + depth_norm * 0.6) * 30)
    
    return combined, dim_total, depth_total, dim_scores, depth_scores, is_shallow, avg_section_depth

def main():
    chapters = []
    for r,d,f in os.walk('Book/'):
        if '_legacy' in r: continue
        for ff in sorted(f):
            if not ff.endswith('.md'): continue
            path = r+'/'+ff
            c, dt, dpt, ds, dps, sh, asd = audit_chapter(path)
            total_lines = len(open(path, encoding='utf-8').read().splitlines())
            chapters.append((c, dt, dpt, ds, sh, ff, path, os.path.basename(r), total_lines, asd))

    chapters.sort(key=lambda x: x[0])
    
    # Safety: detect duplicate chapter filenames
    seen = {}
    for i, c in enumerate(chapters):
        n = c[5]
        if n in seen:
            print(f'WARN: DUPLICATE {n}: {c[6]} and {seen[n]}', file=sys.stderr)
        seen[n] = c[6]
    
    if '--json' in sys.argv:
        result = [{
            'chapter': c[5], 'combined': c[0], 'dim': c[1], 'depth': c[2],
            'shallow': c[4], 'lines': c[8], 'section_depth': round(c[9], 1)
        } for c in chapters]
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return

    top_n = int(sys.argv[1]) if len(sys.argv) > 1 and sys.argv[1].isdigit() else 15

    print(f"{'#':>3} {'Comb':>5} {'Dim':>4} {'Dpth':>5} {'Shal':>4} {'SectD':>5} {'Chapter':<35} {'Lines':>6}")
    print("-" * 90)
    for i, (c, dt, dpt, ds, sh, name, path, part, lines, asd) in enumerate(chapters[:top_n]):
        shallow_flag = 'YES!' if sh else ''
        print(f"{i+1:>3} {c:>4}/30 {dt:>3}/30 {dpt:>3}/100 {shallow_flag:>4} {asd:>4.1f}  {name:<35} {lines:>5}L")

    dist = Counter(c[0] for c in chapters)
    avg = sum(c[0] for c in chapters) / len(chapters)
    shallow_count = sum(1 for c in chapters if c[4])
    min_chapter = chapters[0]
    max_chapter = chapters[-1]
    
    print(f"\n--- Distribution (avg: {avg:.1f}/30, shallow: {shallow_count}, range: {min_chapter[0]}-{max_chapter[0]}) ---")
    for s in sorted(dist):
        bar = '#' * dist[s]
        print(f"  {s:>2}/30: {bar} ({dist[s]})")

if __name__ == '__main__':
    main()
