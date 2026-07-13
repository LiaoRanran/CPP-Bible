#!/usr/bin/env python3
"""compile_classify.py — Classify compile failures from compile_report.json

Reads tools/compile_report.json (produced by compile_all.py --main-only) and
buckets every failing block into a category so the real bugs surface above
the noise of intentional fragments and missing third-party libraries.

Categories:
  env      third-party header missing (fmt / spdlog / boost / grpc / ...)
  missing  standard header missing (typeinfo / utility / cassert / algorithm ...)
  logic    genuine syntax / type / name error in a complete program
  frag     references a symbol defined in a sibling code fence (not standalone)
  other    anything else

Usage: python3 tools/compile_classify.py [path/to/compile_report.json]
"""
import os, re, sys, json
from collections import Counter, defaultdict

# third-party libs not shipped with MinGW libstdc++
ENV_HDR = re.compile(r'(fmt/|spdlog/|boost/|grpc/|gtest/|gmock/|absl/|'
                     r'catch2?/|opencv/|eigen3?/)')
ENV_NAME = re.compile(r'(fmt|spdlog|boost|grpc[+/]|gtest|gmock|abseil|'
                      r'catch2|opencv|eigen)\b', re.IGNORECASE)
# POSIX / platform-specific headers unavailable on the MinGW/Windows target
POSIX_ENV = re.compile(r'(sys/mman\.h|sys/wait\.h|sys/|unistd\.h|'
                       r'dlfcn\.h|pthread\.h|Windows\.h|windows\.h|'
                       r'PDWORD|HANDLE)')
# references an external .h/.hpp/.cpp file (illustrative fragment / project-local)
LOCAL_INC = re.compile(r'(\.hpp|\.h|\.cpp): No such file or directory')

# maps an error substring -> the standard header that fixes it
MISSING_MAP = [
    (r"'typeid'", '<typeinfo>'),
    (r"'type_info'", '<typeinfo>'),
    (r'printf|scanf|fprintf|snprintf', '<cstdio>'),
    (r"(cout|cin|cerr|clog|endl)", '<iostream>'),
    (r"std::exchange", '<utility>'),
    (r"std::move|'move' is not a member of 'std'", '<utility>'),
    (r"'forward' is not a member of 'std'", '<utility>'),
    (r"std::(unique_ptr|shared_ptr|weak_ptr|make_shared|make_unique)",
     '<memory>'),
    (r"std::(mutex|lock_guard|unique_lock|scoped_lock)", '<mutex>'),
    (r"std::thread|'thread' in namespace 'std'", '<thread>'),
    (r"strdup", '<cstring>'),
    (r"'assert'", '<cassert>'),
    (r"aligned_alloc", '<cstdlib>'),
    (r"requires '#include <initializer_list>'", '<initializer_list>'),
    (r"std::ranges::sort|'sort' is not a member of 'std::ranges'", '<algorithm>'),
    (r"std::sort|'sort' is not a member of 'std'", '<algorithm>'),
    (r"std::greater|std::less", '<functional>'),
    (r"'size_t' does not name|'size_t' has not been declared", '<cstddef>'),
    (r"'uint\d+_t'|'int\d+_t'", '<cstdint>'),
    (r"'string' in namespace 'std' does not name", '<string>'),
    (r"'vector' in namespace 'std' does not name", '<vector>'),
    (r"'function' in namespace 'std' does not name", '<functional>'),
    (r"'error_code' in namespace 'std'", '<system_error>'),
    (r"'variant' in namespace 'std'", '<variant>'),
    (r"'optional' in namespace 'std'", '<optional>'),
    (r"'any' in namespace 'std'", '<any>'),
    (r"'tuple' in namespace 'std'", '<tuple>'),
    (r"'span' in namespace 'std'", '<span>'),
    (r"'expected' in namespace 'std'", '<expected>'),
    (r"'filesystem'|std::filesystem", '<filesystem>'),
    (r"'format'|std::format", '<format>'),
    (r"'source_location'|std::source_location", '<source_location>'),
    (r"'print'|std::print", '<print>'),
    (r"'jthread'|std::jthread", '<thread>'),
    (r"'latch'|std::latch", '<latch>'),
    (r"'barrier'|std::barrier", '<barrier>'),
    (r"'semaphore'|std::counting_semaphore", '<semaphore>'),
    (r"'stop_token'|std::stop_token", '<stop_token>'),
    (r"'coroutine_handle'|std::coroutine", '<coroutine>'),
    (r"'ranges'|std::ranges|std::views", '<ranges>'),
    (r"'bit_cast'|std::bit", '<bit>'),
    (r"'chrono'|std::chrono", '<chrono>'),
]

# signals that the block is a fragment referencing a sibling fence's symbol
FRAG_HINT = re.compile(
    r"was not declared in this scope|"
    r"does not name a type|"
    r"not declared|"
    r"undeclared")

LOGIC_HINT = re.compile(
    r"expected (unqualified-id|')|"
    r"cannot declare|"
    r"no matching|"
    r"invalid|"
    r"redefinition|"
    r"is private|"
    r"cannot convert|"
    r"too few|too many|"
    r"requires|"
    r"static assertion|"
    r"non-constant|"
    r"dangling")


def classify(error):
    if ENV_HDR.search(error) or ENV_NAME.search(error) \
            or POSIX_ENV.search(error):
        return 'env'
    if LOCAL_INC.search(error):
        return 'frag'
    # C++ modules need -fmodules / -fmodule; flagged as env (compiler flag)
    if re.search(r"'import' does not name a type|'module' does not name a type",
                 error):
        return 'env'
    for pat, hdr in MISSING_MAP:
        if re.search(pat, error):
            return 'missing', hdr
    if LOGIC_HINT.search(error):
        return 'logic'
    if FRAG_HINT.search(error):
        return 'frag'
    return 'other'


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'tools/compile_report.json'
    if not os.path.exists(path):
        print(f'no report at {path}; run: python3 tools/compile_all.py --main-only')
        return 1
    rep = json.load(open(path, encoding='utf-8'))

    buckets = defaultdict(list)
    missing_headers = Counter()
    for ch in rep['failures']:
        for fr in ch['failures']:
            res = classify(fr['error'])
            if isinstance(res, tuple):
                cat, hdr = res
                missing_headers[hdr] += 1
            else:
                cat = res
            buckets[cat].append((ch['file'], fr['block'], fr['error']))

    print(f"Report: {path}")
    print(f"Chapters checked: {rep['total_chapters']} | "
          f"blocks: {rep['total_blocks_checked']} | "
          f"failed: {rep['failed_blocks']}")
    print(f"main_only={rep['main_only']}  gcc={rep['gcc']}")
    print('=' * 70)

    order = ['env', 'missing', 'logic', 'frag', 'other']
    for cat in order:
        items = buckets.get(cat, [])
        print(f"\n### {cat.upper()}  ({len(items)})")
        if cat == 'missing':
            print("  header fix histogram:")
            for hdr, n in missing_headers.most_common():
                print(f"    {hdr:<20} x{n}")
        for f, b, e in items[:40]:
            print(f"  {f} #{b}: {e}")
        if len(items) > 40:
            print(f"  ... +{len(items)-40} more")

    print('\n' + '=' * 70)
    print("SUMMARY:", {c: len(buckets.get(c, [])) for c in order})


if __name__ == '__main__':
    main()
