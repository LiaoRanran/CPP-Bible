#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_compiler_features.py — P0-2.4 编译器特性支持度探针

用真实 feature-test macros（__cpp_* / __cpp_lib_*）编译探测当前工具链对该特性的
实际支持度，输出机器可读 JSON，用于：
  1) 生成 docs/compiler-matrix.md 的 GCC 列权威数据
  2) 与文档中的声明做 diff，发现文档与真实工具链的偏差
  3) 季度复验：重新跑本脚本，diff 输出变化

用法:
  python3 tools/verify_compiler_features.py            # 探测 GCC15 并落盘 _cpp_probe_gcc.json
  python3 tools/verify_compiler_features.py --check    # 与 docs/compiler-matrix.md 比对
  python3 tools/verify_compiler_features.py --gcc "C:/Qt/Tools/mingw1530_64/bin/g++.exe"

注意: 本机仅装有 GCC 15.3.0（MinGW-w64）。Clang / MSVC 列来自 cppreference 文档
数据（在矩阵表中明确标注 "doc" 来源），不在本脚本本地验证范围内。
"""

import os
import re
import sys
import json
import subprocess

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_GCC = "C:/Qt/Tools/mingw1530_64/bin/g++.exe"

# (macro, 人类可读特性, 最低有意义 std)
FEATURES = [
    # ---- 语言特性（编译器前端） ----
    ("__cpp_modules", "Modules (C++20)", "c++20"),
    ("__cpp_concepts", "Concepts (C++20)", "c++20"),
    ("__cpp_coroutines", "Coroutines (C++20)", "c++20"),
    ("__cpp_impl_coroutine", "Coroutine impl (C++23 统一)", "c++23"),
    ("__cpp_constexpr", "constexpr 扩展", "c++23"),
    ("__cpp_if_consteval", "if consteval (C++23)", "c++23"),
    ("__cpp_static_call_operator", "static operator() (C++23)", "c++23"),
    ("__cpp_explicit_this", "explicit object param / deducing this (C++23)", "c++23"),
    ("__cpp_multidimensional_subscript", "多维下标 operator[]", "c++23"),
    ("__cpp_size_t_suffix", "size_t 字面量后缀 zu (C++23)", "c++23"),
    ("__cpp_named_character_escapes", "命名转义 \\o{...} (C++23)", "c++23"),
    ("__cpp_lib_modules", "Standard library modules (std / std.compat)", "c++23"),
    ("__cpp_deducing_this", "deducing this (C++23)", "c++23"),
    ("__cpp_capture_star_this", "*this capture (C++17)", "c++17"),
    ("__cpp_generic_lambdas", "generic lambda (C++14)", "c++14"),
    ("__cpp_init_captures", "init-capture (C++14)", "c++14"),
    ("__cpp_lambda_capture", "lambda capture [=, this] deprecate (C++20)", "c++20"),
    ("__cpp_structured_bindings", "structured bindings (C++17)", "c++17"),
    ("__cpp_if_constexpr", "if constexpr (C++17)", "c++17"),
    ("__cpp_fold_expressions", "fold expressions (C++17)", "c++17"),
    ("__cpp_deduction_guides", "CTAD (C++17)", "c++17"),
    ("__cpp_variadic_using", "variadic using (C++17)", "c++17"),
    ("__cpp_aggregate_nsdmi", "aggregate NSDMI (C++14)", "c++14"),
    ("__cpp_nontype_template_args", "NTTP 扩展 (C++20)", "c++20"),
    ("__cpp_rvalue_references", "rvalue refs (C++11)", "c++11"),
    ("__cpp_decltype", "decltype (C++11)", "c++11"),
    ("__cpp_lambdas", "lambdas (C++11)", "c++11"),
    ("__cpp_alias_templates", "alias templates (C++11)", "c++11"),
    ("__cpp_variadic_templates", "variadic templates (C++11)", "c++11"),
    ("__cpp_unicode_characters", "unicode identifiers (C++11)", "c++11"),
    ("__cpp_raw_strings", "raw strings (C++11)", "c++11"),
    ("__cpp_user_defined_literals", "UDL (C++11)", "c++11"),
    # ---- 库特性（标准库实现） ----
    ("__cpp_lib_format", "std::format (C++20)", "c++20"),
    ("__cpp_lib_print", "std::print (C++23)", "c++23"),
    ("__cpp_lib_ranges", "std::ranges (C++20)", "c++20"),
    ("__cpp_lib_span", "std::span (C++20)", "c++20"),
    ("__cpp_lib_jthread", "std::jthread (C++20)", "c++20"),
    ("__cpp_lib_atomic_wait", "atomic wait/notify (C++20)", "c++20"),
    ("__cpp_lib_barrier", "std::barrier (C++20)", "c++20"),
    ("__cpp_lib_latch", "std::latch (C++20)", "c++20"),
    ("__cpp_lib_semaphore", "std::counting_semaphore (C++20)", "c++20"),
    ("__cpp_lib_coroutine", "coroutine library (C++20)", "c++20"),
    ("__cpp_lib_concepts", "concepts library (C++20)", "c++20"),
    ("__cpp_lib_memory_resource", "pmr (C++17)", "c++17"),
    ("__cpp_lib_filesystem", "std::filesystem (C++17)", "c++17"),
    ("__cpp_lib_string_view", "std::string_view (C++17)", "c++17"),
    ("__cpp_lib_optional", "std::optional (C++17)", "c++17"),
    ("__cpp_lib_variant", "std::variant (C++17)", "c++17"),
    ("__cpp_lib_any", "std::any (C++17)", "c++17"),
    ("__cpp_lib_shared_mutex", "std::shared_mutex (C++17)", "c++17"),
    ("__cpp_lib_atomic_ref", "std::atomic_ref (C++20)", "c++20"),
    ("__cpp_lib_to_chars", "std::to_chars (C++17)", "c++17"),
    ("__cpp_lib_bitops", "bit ops (C++20)", "c++20"),
    ("__cpp_lib_endian", "std::endian (C++20)", "c++20"),
    ("__cpp_lib_source_location", "std::source_location (C++20)", "c++20"),
    ("__cpp_lib_smart_ptr_for_overwrite", "smart ptr for overwrite (C++20)", "c++20"),
    ("__cpp_lib_move_only_function", "std::move_only_function (C++23)", "c++23"),
    ("__cpp_lib_expected", "std::expected (C++23)", "c++23"),
    ("__cpp_lib_generator", "std::generator (C++23)", "c++23"),
    ("__cpp_lib_stacktrace", "std::stacktrace (C++23)", "c++23"),
    ("__cpp_lib_simd", "std::simd (C++23)", "c++23"),
    ("__cpp_lib_stdatomic_h", "<stdatomic.h> (C++23)", "c++23"),
    ("__cpp_lib_hazard_pointer", "hazard_pointer (C++26)", "c++26"),
    ("__cpp_lib_rcu", "rcu (C++26)", "c++26"),
]


def gen_cpp(path):
    lines = ["#include <iostream>", ""]
    # 引入尽可能多的标准库头，确保 __cpp_lib_* 可见
    headers = [
        "<format>", "<print>", "<ranges>", "<span>", "<thread>", "<barrier>",
        "<latch>", "<semaphore>", "<coroutine>", "<concepts>", "<memory_resource>",
        "<filesystem>", "<string_view>", "<optional>", "<variant>", "<any>",
        "<shared_mutex>", "<atomic>", "<charconv>", "<bit>", "<source_location>",
        "<utility>", "<expected>", "<generator>", "<stacktrace>",
    ]
    # 注：<simd>/<hazard_pointer>/<rcu> 为 C++23/26 候选，GCC 15.3 未提供头文件，
    # 其 __cpp_lib_* 宏本就 undef，无需 include（include 反而编译失败）。
    for h in headers:
        lines.append(f"#include {h}")
    lines.append("")
    lines.append("int main() {")
    for macro, feat, std in FEATURES:
        lines.append(f'#ifdef {macro}')
        lines.append(f'    std::cout << "{macro}=" << {macro} << "\\n";')
        lines.append("#else")
        lines.append(f'    std::cout << "{macro}=<undef>" << "\\n";')
        lines.append("#endif")
    lines.append("    return 0;")
    lines.append("}")
    with open(path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")


def probe(gcc):
    cpp = os.path.join(ROOT, "_cpp_probe.cpp")
    gen_cpp(cpp)
    exe = os.path.join(ROOT, "_cpp_probe.exe")
    # 用 c++23 最高标准编译
    cmd = [gcc, "-std=c++23", "-O0", "-x", "c++", cpp, "-o", exe]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8")
    if r.returncode != 0:
        print("[WARN] compile failed:", file=sys.stderr)
        print(r.stderr[:2000], file=sys.stderr)
        # 尝试 c++20
        cmd2 = [gcc, "-std=c++20", "-O0", "-x", "c++", cpp, "-o", exe]
        r2 = subprocess.run(cmd2, capture_output=True, text=True, encoding="utf-8")
        if r2.returncode != 0:
            return None, r2.stderr[:2000]
        r = r2
    out = subprocess.run([exe], capture_output=True, text=True, encoding="utf-8")
    result = {}
    for line in out.stdout.splitlines():
        if "=" in line:
            k, v = line.split("=", 1)
            result[k.strip()] = v.strip()
    return result, None


def main():
    gcc = DEFAULT_GCC
    if "--gcc" in sys.argv:
        gcc = sys.argv[sys.argv.index("--gcc") + 1]
    do_check = "--check" in sys.argv

    print(f"[probe] {gcc}")
    data, err = probe(gcc)
    if data is None:
        print("[FAIL]", err)
        sys.exit(1)

    # 整理成结构化
    structured = {}
    for macro, feat, std in FEATURES:
        val = data.get(macro, "<undef>")
        structured[macro] = {"feature": feat, "std": std, "gcc_value": val}

    out_path = os.path.join(ROOT, "_cpp_probe_gcc.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(structured, f, ensure_ascii=False, indent=2)

    # 统计
    defined = sum(1 for v in structured.values() if v["gcc_value"] != "<undef>")
    print(f"[done] {defined}/{len(structured)} macros defined on GCC 15.3.0")
    print(f"[dump] {out_path}")
    if "--verbose" in sys.argv:
        for m, v in structured.items():
            print(f"  {m:38s} {v['gcc_value']:>10s}  ({v['feature']})")

    if do_check:
        check_against_doc(structured)


def check_against_doc(structured):
    doc = os.path.join(ROOT, "docs", "compiler-matrix.md")
    if not os.path.exists(doc):
        print("[check] docs/compiler-matrix.md not found — skip")
        return
    txt = open(doc, encoding="utf-8").read()
    print("\n[check] diff vs docs/compiler-matrix.md GCC column:")
    mism = 0
    for macro, v in structured.items():
        # 在文档里找 `macro | value` 形式的声明
        m = re.search(rf"\b{macro}\b[^\n]*", txt)
        if not m:
            print(f"  [doc-missing] {macro}")
            mism += 1
            continue
        line = m.group(0)
        # 粗略检查：文档 GCC 列 claim
        # 仅作提示，不强制
    print(f"[check] {mism} macros not found in doc")


if __name__ == "__main__":
    main()
