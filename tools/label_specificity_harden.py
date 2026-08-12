#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
label_specificity_harden.py — §1 立场分层标签「具体化」收口工具（确定性、围栏感知、保原生换行）。

宪章 CONVENTIONS.md §1 要求：凡是 [实现]/[ABI]/[平台]/[微架构] 内容，必须标注具体
实现/架构（如 [实现·GCC15]、[平台·x86-64]）。[标准]/[经验]/[算法]/[假设] 不需要 ·specific。

安全范围（本工具只做这两类，其余留待人工/逐条判断，遵守「不确定即跳过」）：
  - [实现]：仅当章节散文里某个编译器/库占主导（>50% 且 >=2 次）时，补全为
           [实现·GCC15] / [实现·Clang19] / [实现·MSVC] / [实现·libstdc++] /
           [实现·libc++] / [实现·Boost] / [实现·Qt] / [实现·LLVM] / ...
           编译器统一用本书工具链规范（GCC15 / Clang19），不追杂版本号避免误标。
  - [平台]：仅当 x86-64 / ARM64 / Windows / Linux 占主导时补全。
  - [微架构] / [ABI]：本工具【不】自动补全（同一文件内常混用多种微架构/ABI，需逐条判断），
           保持裸标签，留待人工或后续逐条处理。

绝不改动语义层（不碰 [标准]/[经验]）；围栏内代码块不处理；保原生换行。

用法：
  python3 tools/label_specificity_harden.py            # dry-run
  python3 tools/label_specificity_harden.py --apply    # 落盘
"""

import os
import re
import sys
import argparse

HIGH_RISK_FILES = [
    "Book/part09_concurrency/ch107_atomic.md",
    "Book/part09_concurrency/ch108_memory_order.md",
    "Book/part09_concurrency/ch109_fence.md",
    "Book/part09_concurrency/ch110_lockfree.md",
    "Book/part09_concurrency/ch111_aba.md",
    "Book/part09_concurrency/ch112_hazard_rcu.md",
    "Book/part09_concurrency/ch113_coroutine.md",
    "Book/part03_language/ch30_volatile.md",
    "Book/part10_modern/ch115_move.md",
    "Book/part07_stl/ch93_thread_async.md",
    "Book/part07_stl/ch94_stop_token.md",
    "Book/part10_modern/ch120_coroutine_app.md",
    "Book/part15_cases/ch159_threadpool.md",
    "Book/part15_cases/ch160_mempool.md",
    "Book/part15_cases/ch161_logger.md",
    "Book/part15_cases/ch163_net.md",
    "Book/part05_oo/ch45_oop_object_model.md",
    "Book/part05_oo/ch46_encapsulation_inheritance.md",
    "Book/part05_oo/ch47_virtual_functions.md",
    "Book/part05_oo/ch48_rtti.md",
    "Book/part05_oo/ch49_virtual_inheritance.md",
    "Book/part05_oo/ch50_multiple_inheritance.md",
    "Book/part05_oo/ch51_crtp.md",
    "Book/part05_oo/ch52_ebo.md",
    "Book/part02_toolchain/ch11_compilers.md",
    "Book/part12_patterns/ch139_crtp_pattern.md",
    "Book/part11_source/ch124_libstdcxx.md",
    "Book/part11_source/ch125_libcxx.md",
    "Book/part11_source/ch126_msstl.md",
    "Book/part11_source/ch127_llvm.md",
    "Book/part11_source/ch128_boost.md",
    "Book/part11_source/ch129_qt.md",
    "Book/part11_source/ch130_chromium_abseil.md",
    "Book/part11_source/ch131_fmt_spdlog.md",
    "Book/part11_source/ch132_leveldb_rocksdb.md",
    "Book/part11_source/ch133_clickhouse_redis.md",
    "Book/part11_source/ch134_unreal.md",
    "Book/part03_language/ch23_namespace_adl.md",
    "Book/part10_modern/ch117_copy_elision.md",
    "Book/part10_modern/ch118_modules.md",
    "Book/part06_templates/ch60_template_basics.md",
    "Book/part06_templates/ch61_template_overload.md",
    "Book/part06_templates/ch62_specialization.md",
    "Book/part06_templates/ch63_variadic.md",
    "Book/part06_templates/ch64_fold.md",
    "Book/part06_templates/ch65_type_traits.md",
    "Book/part06_templates/ch66_sfinae.md",
    "Book/part06_templates/ch67_concepts.md",
    "Book/part06_templates/ch68_tmp.md",
    "Book/part06_templates/ch69_constexpr.md",
    "Book/part06_templates/ch70_tag_dispatch.md",
    "Book/part06_templates/ch71_policy.md",
    "Book/part06_templates/ch72_expression_templates.md",
    "Book/part10_modern/ch123_ct_programming.md",
    "Book/part14_perf/ch152_perf_model.md",
    "Book/part14_perf/ch153_cpu_micro.md",
    "Book/part14_perf/ch154_cache_opt.md",
    "Book/part14_perf/ch155_simd.md",
    "Book/part14_perf/ch156_compiler_opt.md",
    "Book/part14_perf/ch157_compiler_explorer.md",
    "Book/part14_perf/ch158_perf_antipatterns.md",
    "Book/part04_memory/ch35_memory_layout.md",
    "Book/part04_memory/ch36_stack_heap.md",
    "Book/part04_memory/ch37_new_delete.md",
    "Book/part04_memory/ch38_allocator.md",
    "Book/part04_memory/ch41_smart_pointers.md",
    "Book/part04_memory/ch42_strict_aliasing.md",
    "Book/part04_memory/ch43_cache_locality.md",
    "Book/part04_memory/ch44_memory_pool.md",
    "Book/part03_language/ch27_cast.md",
    "Book/part03_language/ch28_lifetime_ub.md",
    "Book/part13_engineering/ch151_benchmark.md",
    "Book/part02_toolchain/ch15_profiling.md",
    "Book/part02_toolchain/ch18_buildconfig.md",
    "Book/part12_patterns/ch142_ecs.md",
    "Book/part12_patterns/ch143_dod.md",
]

FENCE_RE = re.compile(r'^(`{3,}|~{3,})')

# 实现/库 token -> (正则, 标签后缀)。编译器用本书工具链规范（GCC15/Clang19）。
IMPL_TOKENS = {
    'gcc':        (r'\bg\+\+|\bgcc\b', 'GCC15'),
    'clang':      (r'\bclang\b', 'Clang19'),
    'msvc':       (r'\bmsvc\b|visual c\+\+|ms vc', 'MSVC'),
    'libstdc++':  (r'libstdc\+\+', 'libstdc++'),
    'libc++':     (r'libc\+\+', 'libc++'),
    'ms stl':     (r'ms stl|ms-stl', 'MS STL'),
    'boost':      (r'\bboost\b', 'Boost'),
    'qt':         (r'\bqt\b|qt6|qt5', 'Qt'),
    'abseil':     (r'\babseil\b', 'Abseil'),
    'fmt':        (r'\bfmt\b|\{fmt\}', 'fmt'),
    'chromium':   (r'\bchromium\b', 'Chromium'),
    'llvm':       (r'\bllvm\b', 'LLVM'),
    'unreal':     (r'\bunreal\b', 'Unreal'),
    'leveldb':    (r'\bleveldb\b', 'leveldb'),
    'rocksdb':    (r'\brocksdb\b', 'RocksDB'),
    'redis':      (r'\bredis\b', 'Redis'),
    'clickhouse': (r'\bclickhouse\b', 'ClickHouse'),
}
IMPL_RX = {k: re.compile(v, re.I) for k, (v, _) in IMPL_TOKENS.items()}

PLAT_TOKENS = {
    'x86-64':  r'x86[-_ ]?64',
    'ARM64':   r'\barm64\b|aarch64',
    'Windows': r'\bwindows\b',
    'Linux':   r'\blinux\b',
}
PLAT_RX = {k: re.compile(v, re.I) for k, v in PLAT_TOKENS.items()}

# 仅自动补全这两个标签
APPLY_TAGS = {
    '实现': re.compile(r'\[实现\]'),
    '平台': re.compile(r'\[平台\]'),
}


def dominant(tokens_rx, text, min_share=0.5, min_count=2):
    counts = {name: len(rx.findall(text)) for name, rx in tokens_rx.items()}
    total = sum(counts.values())
    if total == 0:
        return None
    best = max(counts, key=counts.get)
    if counts[best] >= min_count and counts[best] / total >= min_share:
        return best
    return None


def resolve_impl_suffix(prose):
    best = dominant(IMPL_RX, prose)
    return IMPL_TOKENS[best][1] if best else None


def resolve_plat_suffix(prose):
    return dominant(PLAT_RX, prose)


def harden_file(fp, apply):
    raw = open(fp, encoding='utf-8', errors='replace').read()
    had_cr = '\r\n' in raw
    nl = '\r\n' if had_cr else '\n'
    lines = raw.split(nl)
    if raw.endswith(nl):
        lines = lines[:-1]

    prose_parts = []
    in_fence = False
    for ln in lines:
        if FENCE_RE.match(ln):
            in_fence = not in_fence
            continue
        if not in_fence:
            prose_parts.append(ln)
    prose_text = '\n'.join(prose_parts)

    suf_map = {
        '实现': resolve_impl_suffix(prose_text),
        '平台': resolve_plat_suffix(prose_text),
    }
    if not (suf_map['实现'] or suf_map['平台']):
        return None

    counts = {'实现': 0, '平台': 0}
    new_lines = []
    changed = False
    in_fence = False
    for ln in lines:
        if FENCE_RE.match(ln):
            in_fence = not in_fence
            new_lines.append(ln)
            continue
        if in_fence:
            new_lines.append(ln)
            continue
        new_ln = ln
        for tag, rx in APPLY_TAGS.items():
            if suf_map[tag]:
                new_ln, n = rx.subn(lambda m, t=tag: '[%s·%s]' % (t, suf_map[t]), new_ln)
                counts[tag] += n
        if new_ln != ln:
            changed = True
        new_lines.append(new_ln)

    if not changed:
        return None

    new_text = nl.join(new_lines) + nl
    if apply:
        with open(fp, 'w', encoding='utf-8', newline='') as f:
            f.write(new_text)
    return {'counts': counts, 'suffixes': suf_map}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--apply', action='store_true', help='落盘；默认 dry-run')
    ap.add_argument('--files', default=None, help='自定义文件列表（每行一个路径）')
    ap.add_argument('--root', default='.')
    args = ap.parse_args()

    files = [l.strip() for l in open(args.files, encoding='utf-8')] if args.files \
        else HIGH_RISK_FILES

    total = {'实现': 0, '平台': 0}
    changed_files = 0
    for fp in files:
        full = fp if os.path.isabs(fp) else os.path.join(args.root, fp)
        if not os.path.isfile(full):
            print('[warn] 文件不存在，跳过: %s' % fp, file=sys.stderr)
            continue
        res = harden_file(full, args.apply)
        if res:
            changed_files += 1
            c = res['counts']
            total['实现'] += c['实现']
            total['平台'] += c['平台']
            s = res['suffixes']
            sstr = ', '.join('%s→%s' % (k, s[k]) for k in s if s[k])
            print('%s: 实现+%d 平台+%d  [%s]' % (fp, c['实现'], c['平台'], sstr))

    mode = 'APPLY' if args.apply else 'dry-run'
    print('--- [%s] files_changed=%d totals=%s' %
          (mode, changed_files, total), file=sys.stderr)


if __name__ == '__main__':
    main()
