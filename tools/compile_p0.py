#!/usr/bin/env python3
"""compile_p0.py — Targeted compile of known P0 chapters.

Compiles only 'int main' blocks (--main-only semantics) and appends a
result line per file to results_p0.txt immediately, so progress survives
a killed session.
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import compile_all as ca

TARGETS = [
    'Book/part10_modern/ch120_coroutine_app.md',
    'Book/part10_modern/ch121_contracts.md',
    'Book/part10_modern/ch122_pmr.md',
    'Book/part14_perf/ch157_compiler_explorer.md',
    'Book/part14_perf/ch158_perf_antipatterns.md',
    'Book/part03_language/ch26_lambda.md',
    'Book/part07_stl/ch90_ranges.md',
    'Book/part05_oo/ch46_encapsulation_inheritance.md',
]

OUT = 'tools/results_p0.txt'
# Fresh file
with open(OUT, 'w', encoding='utf-8') as f:
    f.write('# P0 compile results (main-only)\n')

for f in TARGETS:
    try:
        txt = open(f, encoding='utf-8').read()
    except FileNotFoundError:
        line = f'MISSING {f}\n'
        with open(OUT, 'a', encoding='utf-8') as fo:
            fo.write(line)
        print(line, flush=True)
        continue
    blocks = ca.extract_blocks(txt)
    mains = [b for b in blocks if ca.block_has_main(b)]
    fails = [(i + 1, ca.compile_block(b))
             for i, b in enumerate(blocks)
             if ca.block_has_main(b) and ca.compile_block(b)]
    line = f'{f.split("/")[-1]:35s} main={len(mains):3d} fail={len(fails):2d}\n'
    with open(OUT, 'a', encoding='utf-8') as fo:
        fo.write(line)
        for i, e in fails:
            fo.write(f'    block#{i}: {e[:200]}\n')
    print(line, flush=True)
    for i, e in fails:
        print(f'    block#{i}: {e[:200]}', flush=True)

print('DONE', flush=True)
