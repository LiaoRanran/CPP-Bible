#!/usr/bin/env python3
"""industrial_precision.py — 工业引用精度审计
扫描全仓 GitHub URL 与工业域名，按精度分级：
  L3 (行级)    github.com/org/repo/blob/.../file.cc#L123
  L2 (文件级)  github.com/org/repo/blob/.../file.cc
  L1 (仓库级)  github.com/org/repo
  L0 (域级)    boost.org (仅域名引用，无具体路径)

Phase E 攻击目标：L0/L1 章应升级到 L2/L3。

Usage:
  python3 tools/industrial_precision.py [--markdown] [--json] [--per-chapter N]
"""
import re, sys, json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BOOK = ROOT / 'Book'

# GitHub URL patterns by precision level
L3_LINE_RE = re.compile(
    r'https?://(?:www\.)?github\.com/[\w.-]+/[\w.-]+/blob/[^/]+/[^)#\s]+#L\d+', re.I)
L2_FILE_RE = re.compile(
    r'https?://(?:www\.)?github\.com/[\w.-]+/[\w.-]+/blob/[^/\s)#]+/[^)#\s]+', re.I)
L1_REPO_RE = re.compile(
    r'https?://(?:www\.)?github\.com/[\w.-]+/[\w.-]+(?:[/?#)][^\s)]*)?', re.I)

# Non-GitHub industrial domain references
DOMAIN_L3_RE = re.compile(
    r'https?://(?:www\.)?(?:llvm\.org|boost\.org|en\.cppreference\.com|'
    r'abseil\.io|fmt\.dev|spdlog\.dev|chromium\.googlesource\.com|'
    r'webkit\.org|v8\.dev|nodejs\.org|unrealengine\.com|'
    r'oneapi\.io|openmp\.org|nvidia\.com/cuda|amd\.com/rocm|'
    r'grpc\.io|protobuf\.dev|clickhouse\.com|redis\.io|'
    r'qt\.io|eigen\.tuxfamily\.org|tensorflow\.org|pytorch\.org)'
    r'/[^\s)]*', re.I)

# Key industrial projects (domain-level recognition)
INDUSTRIAL_PROJECTS = [
    'abseil.io', 'boost.org', 'llvm.org', 'chromium.googlesource.com',
    'github.com/abseil', 'github.com/llvm', 'github.com/google',
    'github.com/facebook', 'github.com/ClickHouse', 'github.com/redis',
    'github.com/fmtlib', 'github.com/gabime/spdlog',
    'github.com/protocolbuffers/protobuf', 'github.com/grpc',
    'github.com/oneapi-src/oneTBB', 'github.com/ROCm',
    'github.com/tensorflow', 'github.com/pytorch', 'github.com/nodejs',
    'github.com/v8', 'github.com/WebKit', 'github.com/qt',
]

def classify_urls(text: str):
    """Classify all industrial URLs in text by precision level.
    Returns dict with L3/L2/L1/L0 lists of (url, context_line)."""
    results = {'L3': [], 'L2': [], 'L1': [], 'L0': []}
    seen = set()

    # L3: github line-level
    for m in L3_LINE_RE.finditer(text):
        url = m.group(0).rstrip(')')
        if url not in seen:
            seen.add(url)
            results['L3'].append(url)

    # L2: github file-level (exclude ones already caught as L3)
    for m in L2_FILE_RE.finditer(text):
        url = m.group(0).rstrip(').,;')
        if url not in seen:
            seen.add(url)
            # Only L2 if not already L3
            if not L3_LINE_RE.match(url):
                # But must have a real file path (not just repo root)
                parts = url.split('/')
                if len(parts) > 7:  # github.com/org/repo/blob/branch/file
                    results['L2'].append(url)

    # L1: github repo-level
    for m in L1_REPO_RE.finditer(text):
        url = m.group(0).rstrip(')')
        if url not in seen and not L2_FILE_RE.search(url):
            seen.add(url)
            results['L1'].append(url)

    # L0/L3: non-GitHub industrial domains
    for m in DOMAIN_L3_RE.finditer(text):
        url = m.group(0).rstrip(')')
        if url not in seen:
            seen.add(url)
            results['L3'].append(url)

    return results


def audit_all():
    """Audit all chapters. Returns per-chapter data and summary."""
    chapters = []
    for ch in sorted(BOOK.rglob('ch*.md')):
        text = ch.read_text(encoding='utf-8', errors='replace')
        classified = classify_urls(text)

        # Determine highest precision level
        top_level = 'L0'
        if classified['L3']: top_level = 'L3'
        elif classified['L2']: top_level = 'L2'
        elif classified['L1']: top_level = 'L1'

        total = sum(len(v) for v in classified.values())
        part = ch.parent.name if ch.parent.name.startswith('part') else 'unknown'
        chapters.append({
            'file': ch.name,
            'part': part,
            'path': str(ch.relative_to(BOOK)),
            'L3': len(classified['L3']),
            'L2': len(classified['L2']),
            'L1': len(classified['L1']),
            'L0': len(classified['L0']),
            'top_level': top_level,
            'total': total,
        })

    chapters.sort(key=lambda c: (c['total'], c['L3'] + c['L2']))
    return chapters


def fmt_table(chapters, as_md=False):
    """Format results as text or markdown table."""
    header = f'{"File":<35} {"Part":<22} {"L3":>4} {"L2":>4} {"L1":>4} {"L0":>4} {"Total":>5}  {"Top":>3}'
    sep = '-' * 98

    rows = []
    for c in chapters:
        row = (f'{c["file"]:<35} {c["part"]:<22} {c["L3"]:>4} {c["L2"]:>4} '
               f'{c["L1"]:>4} {c["L0"]:>4} {c["total"]:>5}  {c["top_level"]:>3}')
        rows.append(row)

    if as_md:
        md_header = f'| File | Part | L3 | L2 | L1 | L0 | Total | Top |'
        md_sep = '|' + '|'.join(['---'] * 8) + '|'
        md_rows = []
        for c in chapters:
            md_rows.append(f'| `{c["file"]}` | {c["part"]} | {c["L3"]} | '
                          f'{c["L2"]} | {c["L1"]} | {c["L0"]} | {c["total"]} | '
                          f'**{c["top_level"]}** |')
        return '\n'.join([md_header, md_sep] + md_rows)

    return '\n'.join([header, sep] + rows)


def summary(chapters):
    """Generate precision summary statistics."""
    total_refs = sum(c['total'] for c in chapters)
    total_L3 = sum(c['L3'] for c in chapters)
    total_L2 = sum(c['L2'] for c in chapters)
    total_L1 = sum(c['L1'] for c in chapters)
    total_L0 = sum(c['L0'] for c in chapters)

    only_L0_L1 = [c for c in chapters if c['top_level'] in ('L0', 'L1')]
    only_L0 = [c for c in chapters if c['top_level'] == 'L0']
    no_refs = [c for c in chapters if c['total'] == 0]

    return {
        'total_chapters': len(chapters),
        'total_refs': total_refs,
        'L3_count': total_L3,
        'L2_count': total_L2,
        'L1_count': total_L1,
        'L0_count': total_L0,
        'L3_pct': round(total_L3 / max(total_refs, 1) * 100, 1),
        'L2_pct': round(total_L2 / max(total_refs, 1) * 100, 1),
        'L1_pct': round(total_L1 / max(total_refs, 1) * 100, 1),
        'chapters_only_L0_L1': len(only_L0_L1),
        'chapters_only_L0': len(only_L0),
        'chapters_no_refs': len(no_refs),
        'phase_e_attack_list': [f'{c["file"]} ({c["part"]}, top={c["top_level"]}, total={c["total"]})'
                                for c in sorted(only_L0_L1, key=lambda x: x['total'])],
    }


def main():
    as_md = '--markdown' in sys.argv
    as_json = '--json' in sys.argv
    per_ch_n = None
    for i, a in enumerate(sys.argv):
        if a == '--per-chapter' and i + 1 < len(sys.argv):
            try: per_ch_n = int(sys.argv[i + 1])
            except: pass

    chapters = audit_all()
    stats = summary(chapters)

    if as_json:
        out = {'summary': stats, 'chapters': chapters}
        print(json.dumps(out, indent=2, ensure_ascii=False))
        return

    # Print summary
    print('=' * 70)
    print('  工业引用精度审计')
    print('=' * 70)
    print()
    print(f'  总章数:           {stats["total_chapters"]}')
    print(f'  总工业引用数:     {stats["total_refs"]}')
    print(f'  ──────────────────────────')
    print(f'  L3 行级 (文件+行号): {stats["L3_count"]:>4}  ({stats["L3_pct"]}%)')
    print(f'  L2 文件级:          {stats["L2_count"]:>4}  ({stats["L2_pct"]}%)')
    print(f'  L1 仓库级:          {stats["L1_count"]:>4}  ({stats["L1_pct"]}%)')
    print(f'  ──────────────────────────')
    print(f'  仅 L0/L1 级章:      {stats["chapters_only_L0_L1"]}  ← Phase E 攻击目标')
    print(f'  零引用章:           {stats["chapters_no_refs"]}')
    print()

    # Phase E attack list
    if stats['phase_e_attack_list']:
        print('### Phase E 精准攻击清单（仅 L0/L1 级引用章）')
        print()
        for item in stats['phase_e_attack_list']:
            print(f'  {item}')
        print()

    # Per-chapter detail
    if per_ch_n:
        print(f'### Per-Chapter Detail (showing {per_ch_n} weakest)')
        print()
        print(fmt_table(chapters[:per_ch_n], as_md=as_md))
    elif as_md:
        print('### Per-Chapter Detail (all)')
        print()
        print(fmt_table(chapters, as_md=True))


if __name__ == '__main__':
    main()
