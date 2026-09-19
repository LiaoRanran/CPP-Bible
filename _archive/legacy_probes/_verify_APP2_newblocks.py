#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
APP2 精准编译验证（分段版）：只抽取我注入的两段——
  EX:  `## 自测练习` → `## 附录：用法演绎` 之间（习题答案）
  DEMO:`## 附录：用法演绎` → EOF（用法演绎）
排除 preserve 章原有的 ASM 附录 cpp 块（那些已被 compile_exempt.json 豁免，CI 绿）。
对每段 cpp 块用与 chapter_compile_check.py 相同的 PRELUDE + 编译标志逐块 -c 编译。
用法: python3 _verify_APP2_newblocks.py
"""
import pathlib, re, subprocess, tempfile, sys

GPP = r"C:/Qt/Tools/mingw1310_64/bin/g++.exe"
PRELUDE = """#include <iostream>
#include <vector>
#include <string>
#include <string_view>
#include <memory>
#include <algorithm>
#include <numeric>
#include <map>
#include <set>
#include <unordered_map>
#include <unordered_set>
#include <functional>
#include <thread>
#include <mutex>
#include <shared_mutex>
#include <condition_variable>
#include <semaphore>
#include <future>
#include <atomic>
#include <barrier>
#include <latch>
#include <stop_token>
#include <tuple>
#include <utility>
#include <initializer_list>
#include <array>
#include <deque>
#include <list>
#include <forward_list>
#include <queue>
#include <stack>
#include <bitset>
#include <stdexcept>
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstddef>
#include <cstring>
#include <limits>
#include <ciso646>
#include <iomanip>
#include <sstream>
#include <iterator>
#include <filesystem>
#include <variant>
#include <any>
#include <optional>
#include <ranges>
#include <bit>
#include <chrono>
#include <execution>
#include <type_traits>
#include <concepts>
#include <span>
#include <expected>
#include <format>
#include <memory_resource>
#include <version>
#include <cmath>
#include <cassert>
#include <coroutine>
#include <regex>
#include <random>
#include <numbers>
#include <fstream>
#include <source_location>
#include <stacktrace>
#include <syncstream>
#include <spanstream>
#include <scoped_allocator>
#include <valarray>
#include <ios>
#include <ostream>
#include <exception>
#include <new>
#include <system_error>
#include <typeindex>
#include <typeinfo>
#include <compare>
#include <cctype>
#include <ctime>
#include <cwchar>
#include <climits>
#include <cerrno>
#include <cfenv>
#include <csignal>
#include <codecvt>
#include <immintrin.h>
#include <cpuid.h>
"""

TARGETS = [
    "Book/part03_language/ch21_const_family.md",
    "Book/part03_language/ch31_operator_overloading.md",
    "Book/part04_memory/ch39_raii_rule.md",
    "Book/part04_memory/ch42_strict_aliasing.md",
    "Book/part04_memory/ch43_cache_locality.md",
    "Book/part04_memory/ch44_memory_pool.md",
    "Book/part05_oo/ch50_multiple_inheritance.md",
    "Book/part05_oo/ch51_crtp.md",
]

CPP_FENCE = re.compile(r"^```cpp\s*$")
FENCE_END = re.compile(r"^```\s*$")
ERR_RE = re.compile(r"error:")


def extract_sections(text):
    """返回 (ex_blocks, demo_blocks)，元素为 (src_line, code)。"""
    lines = text.split("\n")
    ex_start = demo_start = None
    for i, l in enumerate(lines):
        if l.startswith("## 自测练习") and ex_start is None:
            ex_start = i
        if "## 附录：用法演绎" in l and demo_start is None:
            demo_start = i
            break
    if ex_start is None:
        return [], []
    ex_end = demo_start if demo_start is not None else len(lines)
    ex_body = lines[ex_start:ex_end]
    demo_body = lines[demo_start:] if demo_start is not None else []

    def blocks_from(body, base):
        out, in_b, buf, start = [], False, [], 0
        for j, l in enumerate(body):
            if CPP_FENCE.match(l):
                in_b, buf, start = True, [], base + j
                continue
            if in_b and FENCE_END.match(l):
                in_b = False
                out.append((start + 1, "\n".join(buf)))
                continue
            if in_b:
                buf.append(l)
        return out

    return blocks_from(ex_body, ex_start), blocks_from(demo_body, demo_start or 0)


def compile_one(tag, code, outdir):
    stripped = "\n".join(l for l in code.split("\n")
                         if not re.match(r"^\s*#include\b", l))
    stripped = re.sub(r"\bint\s+main\s*\(", "int __main_(", stripped)
    wrapped = f"namespace chk_{tag} {{\n{stripped}\n}}\n"
    full = PRELUDE + "\n" + wrapped + "\nint main(){}\n"
    p = outdir / f"blk_{tag}.cpp"
    p.write_text(full, encoding="utf-8")
    o = outdir / f"blk_{tag}.o"
    r = subprocess.run(
        [GPP, "-std=c++23", "-O2", "-Wall", "-Wextra", "-mavx2",
         "-mavx512f", "-mfma", "-c", str(p), "-o", str(o)],
        capture_output=True, text=True)
    return r.returncode, r.stderr


def main():
    tmp = pathlib.Path(tempfile.mkdtemp())
    total, fails = 0, []
    for t in TARGETS:
        text = pathlib.Path(t).read_text(encoding="utf-8")
        ex_blocks, demo_blocks = extract_sections(text)
        stem = pathlib.Path(t).stem
        for sec, blks in (("EX", ex_blocks), ("DEMO", demo_blocks)):
            for ln, b in blks:
                total += 1
                tag = f"{stem}_{sec}_{ln}"
                rc, err = compile_one(tag, b, tmp)
                if rc != 0:
                    el = [l.strip() for l in err.split("\n") if ERR_RE.search(l)][:3]
                    fails.append((t, sec, ln, "\n".join(el)))
                    print(f"[FAIL] {t} [{sec}] src~{ln}")
                    for e in el:
                        print(f"        {e}")
    print(f"\n=== INJECTED BLOCKS: {total}, FAILS: {len(fails)} ===")
    sys.exit(1 if fails else 0)


if __name__ == "__main__":
    main()
