#!/usr/bin/env python3
"""fix_missing_includes.py — Surgical include fixer for P0 chapters.

For each cpp block in the target files, if it USES a symbol that requires a
specific standard header AND that header is absent from the block, insert the
`#include` right after the block's last existing `#include` (or at top).

This is a correctness fix (every standalone block must compile), NOT content
padding. Verification: re-run compile_p0.py -> 0 fails for these symbols.

Symbols -> required header:
  std::exchange            -> <utility>
  assert(                  -> <cassert>
  typeid                   -> <typeinfo>
  std::ranges:: / ranges:: -> <ranges> + <algorithm>
"""
import re, os, sys

# (regex on block text, header to add)
RULES = [
    (r'std::exchange', '<utility>'),
    (r'(?<!//)\bassert\s*\(', '<cassert>'),
    (r'\btypeid\b', '<typeinfo>'),
    (r'std::ranges::|[^:]:ranges::', '<ranges>'),
    (r'std::ranges::(sort|count|find|for_each|transform|filter|take|drop|'
     r'begin|end|any_of|all_of|none_of|fill|replace|reverse|unique)',
     '<algorithm>'),
]

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


def split_blocks(text):
    """Return (prologue, list_of_(fence_line, body), epilogue)."""
    lines = text.split('\n')
    out = []
    i = 0
    prologue = []
    while i < len(lines):
        if lines[i].strip().startswith('```cpp'):
            fence = lines[i]
            body = []
            i += 1
            while i < len(lines) and lines[i].strip() != '```':
                body.append(lines[i])
                i += 1
            # i now at closing ```
            out.append((fence, '\n'.join(body)))
            i += 1  # skip closing ```
            # capture prologue before first block
        else:
            if not out:
                prologue.append(lines[i])
            i += 1
    return prologue, out, None


def fix_block_body(body):
    """Insert missing includes into a single block body. Returns (new_body, added)."""
    added = []
    for pat, hdr in RULES:
        if re.search(pat, body):
            inc = f'#include {hdr}'
            if inc not in body:
                added.append(hdr)
                # insert after last existing #include, else at top
                lines = body.split('\n')
                last_inc = -1
                for idx, ln in enumerate(lines):
                    if ln.strip().startswith('#include'):
                        last_inc = idx
                if last_inc >= 0:
                    lines.insert(last_inc + 1, inc)
                else:
                    # insert at top (before first code line)
                    lines.insert(0, inc)
                body = '\n'.join(lines)
    return body, added


def main():
    total_added = 0
    for path in TARGETS:
        if not os.path.exists(path):
            print('MISSING', path)
            continue
        text = open(path, encoding='utf-8').read()
        lines = text.split('\n')
        # Walk and rebuild, replacing cpp block bodies
        new_lines = []
        i = 0
        file_adds = 0
        while i < len(lines):
            if lines[i].strip().startswith('```cpp'):
                fence = lines[i]
                body_lines = []
                i += 1
                while i < len(lines) and lines[i].strip() != '```':
                    body_lines.append(lines[i])
                    i += 1
                # i at closing ```
                body = '\n'.join(body_lines)
                new_body, added = fix_block_body(body)
                if added:
                    file_adds += len(added)
                    total_added += len(added)
                new_lines.append(fence)
                new_lines.append(new_body)
                new_lines.append('```')
                i += 1
            else:
                new_lines.append(lines[i])
                i += 1
        if file_adds:
            open(path, 'w', encoding='utf-8').write('\n'.join(new_lines))
            print(f'{path.split("/")[-1]:35s} +{file_adds} includes')
    print(f'TOTAL added: {total_added}')


if __name__ == '__main__':
    main()
