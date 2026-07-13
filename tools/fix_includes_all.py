#!/usr/bin/env python3
"""fix_includes_all.py — Generalized surgical include fixer.

For EVERY cpp block in EVERY chapter under Book/, if it USES a symbol that
requires a specific standard header AND that header is absent from the
block, insert the `#include` right after the block's last existing
`#include` (or at top). This is a correctness fix: every standalone block
must compile. It is NOT content padding.

INTENTIONAL error-demo blocks (marked with 编译失败 / 错误演示 / ❌ /
error demo / intentional) are SKIPPED so the pedagogy survives.

Verification: run compile_all.py --main-only before and after; the
'MISSING_INCLUDE' class of failures should drop to ~0.

Symbol -> required standard header(s):
  printf/scanf/fprintf       -> <cstdio>
  cout/cin/cerr/clog/endl    -> <iostream>
  std::move/std::forward/
  std::exchange              -> <utility>
  uint8_t..uint64_t          -> <cstdint>
  size_t                     -> <cstddef>
  aligned_alloc              -> <cstdlib>
  initializer_list (msg)     -> <initializer_list>
  unique_ptr/shared_ptr/
  weak_ptr/make_shared/
  make_unique                -> <memory>
  mutex/lock_guard/
  unique_lock                -> <mutex>
  thread                     -> <thread>
  strdup                     -> <cstring>
  vector (not member)        -> <vector>
  string (not member)        -> <string>
  optional                   -> <optional>
  expected                   -> <expected>
  variant                    -> <variant>
  any                        -> <any>
  assert(                    -> <cassert>
  typeid                     -> <typeinfo>
  string_view                -> <string_view>
  span                       -> <span>
  array                      -> <array>
  map/unordered_map          -> <map>/<unordered_map>
  set                        -> <set>
  function                   -> <functional>
  ranges::                   -> <ranges> + <algorithm>
  pair/tuple                 -> <utility>/<tuple>
"""
import os, re, sys

# Ordered list of (compiled-regex, [headers-to-add])
# Each header added only if absent from the block.
RULES = [
    (re.compile(r'(?<!//)\b(printf|scanf|fprintf|snprintf)\s*\('), ['<cstdio>']),
    (re.compile(r'\b(std::)?(cout|cin|cerr|clog|endl)\b'), ['<iostream>']),
    (re.compile(r'std::(move|forward|exchange|as_const)\b'), ['<utility>']),
    (re.compile(r'\b(?:uint|int)(?:8|16|32|64)_t\b'), ['<cstdint>']),
    (re.compile(r'\bsize_t\b'), ['<cstddef>']),
    (re.compile(r'aligned_alloc'), ['<cstdlib>']),
    (re.compile(r'std::initializer_list'), ['<initializer_list>']),
    (re.compile(r'std::(unique_ptr|shared_ptr|weak_ptr|make_shared|make_unique)\b'),
     ['<memory>']),
    (re.compile(r'std::(mutex|lock_guard|unique_lock|scoped_lock)\b'), ['<mutex>']),
    (re.compile(r'std::thread\b'), ['<thread>']),
    (re.compile(r'(?<!//)\bstrdup\s*\('), ['<cstring>']),
    (re.compile(r'std::vector\b'), ['<vector>']),
    (re.compile(r'std::string\b'), ['<string>']),
    (re.compile(r'std::optional\b'), ['<optional>']),
    (re.compile(r'std::expected\b'), ['<expected>']),
    (re.compile(r'std::variant\b'), ['<variant>']),
    (re.compile(r'std::any\b'), ['<any>']),
    (re.compile(r'(?<!//)\bassert\s*\('), ['<cassert>']),
    (re.compile(r'\btypeid\b'), ['<typeinfo>']),
    (re.compile(r'std::string_view\b'), ['<string_view>']),
    (re.compile(r'std::span\b'), ['<span>']),
    (re.compile(r'std::array\b'), ['<array>']),
    (re.compile(r'std::(unordered_)?map\b'), ['<map>']),
    (re.compile(r'std::set\b'), ['<set>']),
    (re.compile(r'std::function\b'), ['<functional>']),
    (re.compile(r'std::ranges::'), ['<ranges>', '<algorithm>']),
    (re.compile(r'std::(pair|tuple)\b'), ['<utility>']),
    # Standard <algorithm> functions (sort/find/count/all_of/set_difference/...)
    (re.compile(r'std::(set_difference|set_union|set_intersection|sort|stable_sort|'
                r'partial_sort|find|find_if|count|count_if|all_of|any_of|none_of|'
                r'for_each|transform|copy|copy_if|fill|replace|remove|unique|'
                r'binary_search|lower_bound|upper_bound|equal_range|merge|'
                r'partition|is_sorted|reverse|rotate|shuffle|max_element|'
                r'min_element|clamp)\b'), ['<algorithm>']),
    # <numeric> functions
    (re.compile(r'std::(accumulate|inner_product|iota|reduce|inclusive_scan|'
                r'exclusive_scan|partial_sum|gcd|lcm)\b'), ['<numeric>']),
]

DEMO_MARKERS = ['编译失败', '错误演示', 'error demo', 'intentional', '❌',
                '演示错误', '故意']

SKIP_DIRS = ['_legacy']


def block_is_demo(body):
    return any(m in body for m in DEMO_MARKERS)


def fix_block_body(body):
    if block_is_demo(body):
        return body, []
    added = []
    for pat, hdrs in RULES:
        if pat.search(body):
            for hdr in hdrs:
                inc = f'#include {hdr}'
                if inc not in body:
                    added.append(hdr)
                    lines = body.split('\n')
                    last_inc = -1
                    for idx, ln in enumerate(lines):
                        if ln.strip().startswith('#include'):
                            last_inc = idx
                    if last_inc >= 0:
                        lines.insert(last_inc + 1, inc)
                    else:
                        lines.insert(0, inc)
                    body = '\n'.join(lines)
    return body, added


def main():
    total_added = 0
    files_touched = 0
    for r, d, f in os.walk('Book/'):
        if any(sd in r for sd in SKIP_DIRS):
            continue
        for ff in sorted(f):
            if not ff.endswith('.md'):
                continue
            path = r + '/' + ff
            text = open(path, encoding='utf-8').read()
            lines = text.split('\n')
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
                files_touched += 1
                open(path, 'w', encoding='utf-8').write('\n'.join(new_lines))
    print(f'Files touched: {files_touched}')
    print(f'Total includes added: {total_added}')


if __name__ == '__main__':
    main()
