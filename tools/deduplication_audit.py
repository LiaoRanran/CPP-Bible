#!/usr/bin/env python3
"""v5 去水词 + 密度雷达 — deduplication_audit.py
v4→v5 新增：
  --all       输出全 147 章（非仅底 10）
  --markdown  Markdown 表格（直接贴入 EXPANSION_LOG）
  --per-part  按 part 汇总 ind/dep/water 均分
  --json      完整 JSON 输出（all chapters + per-part breakdown）

v4 评分公式不变：quality = 30 * (ind_norm*0.4 + dep_norm*0.4 - water_penalty*0.2)
  ind_norm = min(industry_hits / 20, 1.0)
  dep_norm = min(depth_hits / 50, 1.0)
  water_penalty = min(water_rate / 5.0, 1.0)

Usage:
  python3 tools/deduplication_audit.py [N] [--all] [--markdown] [--per-part] [--json]
  python3 tools/deduplication_audit.py 147 --all           # 全量文本表
  python3 tools/deduplication_audit.py --all --markdown     # 全量 Markdown 表
  python3 tools/deduplication_audit.py --json               # JSON 文件 + stdout
  python3 tools/deduplication_audit.py --all --per-part     # 全章 + part 汇总
"""
import os, re, sys, json
from collections import Counter, defaultdict
from pathlib import Path

# =========== 信号库 (v4 原版，不变动) ===========

WATER_PATTERNS = [
    r'本附录提供.*?深度补充',
    r'GCC实现13处理编译.*?Assembly',
    r'问：depth.*?答：.*?内容',
    r'本文介绍.*?详细阐述',
    r'本章介绍.*?全面分析',
    r'接下来.*?我们',
    r'从上图.*?可以看出',
    r'通过以上.*?分析',
]

INDUSTRY_KEYWORDS = [
    'Google', 'LLVM', 'Chromium', r'Qt\s', 'Boost', 'Abseil',
    'Unreal', 'fmt', 'spdlog', 'Redis', 'ClickHouse',
    'RocksDB', 'Eigen', 'folly', 'Blink', 'V8', 'Dart',
    'WebKit', 'Mozilla', 'Mesos', 'DPDK', 'gRPC',
]

DEPTH_SIGNALS = [
    # AT&T 语法内存操作数（原版）
    r'mov\s+\w+,\s*\[\w+\+\d+\]',
    r'call\s+\[rax\]',
    # Intel 语法内存操作数（v5 补充：修正 AT&T 偏见的深度低估）
    #   mov rax, QWORD PTR [rdi+0x8]  /  mov eax, [rax-0x18]  /  QWORD PTR -24[rax]
    r'mov\s+\w+,\s*(QWORD\s+PTR\s+)?\[\w+[+-]0x[0-9a-fA-F]+\]',
    r'mov\s+\w+,\s*(QWORD\s+PTR\s+)?-0x[0-9a-fA-F]+\[\w+\]',
    r'(QWORD|DWORD|WORD|BYTE)\s+PTR\s*[\w+\-]+\[\w+\]',
    # 通用 4+ 位十六进制立即数（含 Intel 风格 0x0010）
    r'0x[0-9a-fA-F]{4,}',
    r'~?\d+\.?\d*\s*(ns|us|ms|cycles|bytes|KB|MB|GB|GHz|MHz)',
    r'P\d{4}R\d+',
    r'C\+\+(\d{2}|11|14|17|20|23|26)',
    r'GCC\s+\d+\.\d+|Clang\s+\d+|MSVC\s+\d+',
    r'__attribute__|__builtin_|_Pragma|__cplusplus',
    r'SIMD|SSE|AVX|NEON',
    r'constexpr|consteval|constinit',
]

ROOT = Path(__file__).resolve().parent.parent


def compute_paragraph_similarity(text):
    paras = [p.strip() for p in re.split(r'\n\s*\n', text) if len(p.strip()) > 50]
    if not paras:
        return 0, 0.0, []
    def shingles(p):
        words = re.findall(r'\w+', p)
        return set(tuple(words[i:i+5]) for i in range(len(words)-4))
    sigs = [shingles(p) for p in paras]
    n = len(sigs)
    pairs = []
    for i in range(n):
        for j in range(i+1, n):
            if not sigs[i] or not sigs[j]:
                continue
            jaccard = len(sigs[i] & sigs[j]) / len(sigs[i] | sigs[j])
            if jaccard > 0.6:
                pairs.append((i, j, jaccard, paras[i][:80], paras[j][:80]))
    dup_rate = len(pairs) / max(n, 1)
    return len(pairs), dup_rate, pairs[:5]


def compute_water_score(text):
    hits = 0
    for pat in WATER_PATTERNS:
        hits += len(re.findall(pat, text, re.IGNORECASE))
    total_lines = len(text.splitlines())
    water_rate = hits / max(total_lines, 1) * 100
    return hits, water_rate


def compute_industry_density(text):
    hits = 0
    for kw in INDUSTRY_KEYWORDS:
        hits += len(re.findall(kw, text, re.IGNORECASE))
    return hits


def compute_depth_signals(text):
    hits = 0
    for sig in DEPTH_SIGNALS:
        hits += len(re.findall(sig, text))
    return hits


def audit_chapter_v4(path):
    text = open(path, encoding='utf-8').read()
    total_lines = len(text.splitlines())
    if total_lines < 50:
        return 0, 0, 0, 0, 0, 0, 0.0
    dup_pairs, dup_rate, _ = compute_paragraph_similarity(text)
    water_hits, water_rate = compute_water_score(text)
    industry_hits = compute_industry_density(text)
    depth_hits = compute_depth_signals(text)

    industry_norm = min(industry_hits / 20.0, 1.0)
    depth_norm = min(depth_hits / 50.0, 1.0)
    water_penalty = min(water_rate / 5.0, 1.0)

    quality = 30 * (industry_norm * 0.4 + depth_norm * 0.4 - water_penalty * 0.2)
    quality = max(0, min(30, int(quality)))
    return quality, dup_rate, water_rate, industry_hits, depth_hits, total_lines, water_hits


def resolve_part(path_str):
    """Extract part name from path like Book/partXX_name/chYY_blah.md."""
    parts = path_str.replace('\\', '/').split('/')
    for p in parts:
        if p.startswith('part'):
            return p
    return 'unknown'


def main():
    show_all = '--all' in sys.argv
    as_md = '--markdown' in sys.argv
    per_part = '--per-part' in sys.argv
    as_json = '--json' in sys.argv

    n = 10
    for a in sys.argv[1:]:
        if a.isdigit():
            n = int(a)

    chapters = []
    for r, d, f in os.walk(str(ROOT / 'Book')):
        if '_legacy' in r:
            continue
        for ff in sorted(f):
            if not ff.endswith('.md'):
                continue
            path = r + '/' + ff
            q, dup, water, ind, dep, lines, wh = audit_chapter_v4(path)
            part = resolve_part(path)
            chapters.append({
                'quality': q, 'dup_rate': dup, 'water_rate': water,
                'ind_hits': ind, 'dep_hits': dep, 'file': ff, 'path': path,
                'part': part, 'lines': lines, 'water_hits': wh,
            })

    chapters.sort(key=lambda x: x['quality'])
    avg = sum(c['quality'] for c in chapters) / len(chapters) if chapters else 0

    # ---- JSON output ----
    if as_json:
        out = {
            'avg': round(avg, 1),
            'total_chapters': len(chapters),
            'chapters': [{k: v for k, v in c.items() if k != 'path'} for c in chapters],
        }
        if per_part:
            part_data = defaultdict(lambda: {'chapters': 0, 'quality': 0, 'ind': 0, 'dep': 0, 'water': 0})
            for c in chapters:
                pd = part_data[c['part']]
                pd['chapters'] += 1
                pd['quality'] += c['quality']
                pd['ind'] += c['ind_hits']
                pd['dep'] += c['dep_hits']
                pd['water'] += c['water_rate']
            for p, d in part_data.items():
                d['avg_quality'] = round(d['quality'] / d['chapters'], 1)
                d['avg_ind'] = round(d['ind'] / d['chapters'], 1)
                d['avg_dep'] = round(d['dep'] / d['chapters'], 1)
                d['avg_water'] = round(d['water'] / d['chapters'], 2)
            out['per_part'] = {p: d for p, d in sorted(part_data.items())}
        json_path = str(ROOT / 'tools' / 'last_v4_report.json')
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(out, f, indent=2, ensure_ascii=False)
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    # ---- Determine display range ----
    if show_all:
        display = chapters
        display_n = len(chapters)
    else:
        display = chapters[:n]
        display_n = n

    # ---- Markdown table ----
    if as_md:
        print(f'## v5 Quality Audit (avg={avg:.1f}/30, n={len(chapters)})')
        if not show_all:
            print(f'(showing weakest {display_n})')
        print()
        print(f'| # | v4 | IND | DEP | WTR% | DUP% | Lines | Chapter |')
        print(f'|---|----|-----|-----|------|------|-------|---------|')
        for i, c in enumerate(display, 1):
            ind_bar = '█' * min(c['ind_hits'], 20)
            dep_bar = '▓' * min(c['dep_hits'] // 3, 16)
            print(f'| {i} | **{c["quality"]}** | {c["ind_hits"]} | {c["dep_hits"]} | '
                  f'{c["water_rate"]:.1f} | {c["dup_rate"]:.0%} | {c["lines"]} | '
                  f'`{c["file"]}` |')
        print()
        print(f'**Total**: {len(chapters)} chapters, v4 avg quality: **{avg:.1f}/30**')
        print(f'v4: `industry*0.4 + depth*0.4 - water*0.2`')

        # Deficiency summary: chapters that need the most help
        print()
        print('### Deficiency Radar (chapters needing most Phase E attention)')
        print()
        # Sort by which dimension is weakest relative to target (ind≥8, dep≥25 for avg 15)
        radar = []
        for c in chapters:
            ind_gap = max(0, 8 - c['ind_hits'])
            dep_gap = max(0, 25 - c['dep_hits'])
            total_gap = ind_gap + dep_gap
            radar.append((total_gap, ind_gap, dep_gap, c))
        radar.sort(key=lambda x: -x[0])  # largest gap first

        print(f'| Chapter | v4 | IND gap | DEP gap | Recommendation |')
        print(f'|---------|----|---------|---------|----------------|')
        for gap, ig, dg, c in radar[:15]:
            rec = ''
            if ig > dg:
                rec = '**补工业引用**（真实开源项目链接）'
            elif dg > ig:
                rec = '**补深度附录**（asm/RDTSC/WG21提案）'
            else:
                rec = '双补（工业引用 + 深度附录）'
            print(f'| `{c["file"]}` | {c["quality"]} | {ig:+d} | {dg:+d} | {rec} |')
        print()
        return

    # ---- Text table (default) ----
    print(f'\n=== v5 Quality Audit ({"bottom " + str(display_n) if not show_all else "ALL " + str(len(chapters))}) ===')
    print(f'{"#":>3} {"QUAL":>4} {"IND":>4} {"DEP":>4} {"WTR%":>6} {"DUP%":>6} {"Lines":>6}  File')
    print('-' * 75)
    for i, c in enumerate(display, 1):
        print(f'{i:>3} {c["quality"]:>4} {c["ind_hits"]:>4} {c["dep_hits"]:>4} '
              f'{c["water_rate"]:>5.1f} {c["dup_rate"]:>5.0%} {c["lines"]:>6}  {c["file"]}')

    print(f'\nTotal: {len(chapters)} chapters, v4 avg quality: {avg:.1f}/30')
    print('v4: industry*0.4 + depth*0.4 - water*0.2')

    # Per-part analysis
    if per_part:
        part_data = defaultdict(lambda: {'chapters': 0, 'quality': [], 'ind': [], 'dep': [], 'water': []})
        for c in chapters:
            pd = part_data[c['part']]
            pd['chapters'] += 1
            pd['quality'].append(c['quality'])
            pd['ind'].append(c['ind_hits'])
            pd['dep'].append(c['dep_hits'])
            pd['water'].append(c['water_rate'])

        print(f'\n{"Part":<28} {"n":>3}  {"v4":>5}  {"IND":>5}  {"DEP":>5}  {"WTR%":>6}')
        print('-' * 58)
        for part in sorted(part_data.keys()):
            pd = part_data[part]
            print(f'{part:<28} {pd["chapters"]:>3}  '
                  f'{sum(pd["quality"])/len(pd["quality"]):>5.1f}  '
                  f'{sum(pd["ind"])/len(pd["ind"]):>5.1f}  '
                  f'{sum(pd["dep"])/len(pd["dep"]):>5.1f}  '
                  f'{sum(pd["water"])/len(pd["water"]):>5.1f}')


if __name__ == '__main__':
    main()
