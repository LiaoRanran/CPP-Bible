#!/usr/bin/env python3
"""auto_include.py — 自动补全缺失头文件（突破 72→85+ 代码质量）

扫描全书 cpp 块，对不含 #include 的块：
  1. 检测使用的 STL/标准库符号
  2. 自动注入对应的 #include 头文件
  3. Dry-run 报告 → --apply 落盘（.auto_include.bak 备份）

用法:
  python3 tools/auto_include.py                 # 全局 dry-run 报告
  python3 tools/auto_include.py --apply          # 落盘（创建 .auto_include.bak）
  python3 tools/auto_include.py --chapter ch64   # 单章 dry-run
  python3 tools/auto_include.py --verify         # 落盘后编译验证

设计原则:
  - 只加 STL 标准库头文件（不碰项目内头文件、第三方库头文件）
  - 幂等：已含 #include 的块跳过
  - 安全：--apply 前自动备份，支持 git checkout 回滚
"""

import argparse
import pathlib
import re
import subprocess
import sys
import time

ROOT = pathlib.Path(__file__).resolve().parent.parent
GPP = r"C:/Qt/Tools/mingw1530_64/bin/g++.exe"
CPP_FENCE = re.compile(r'^\s*```cpp')
FENCE_END = re.compile(r'^\s*```\s*$')
ALREADY_INCLUDE = re.compile(r'^\s*#include\s*[<"]')

# ── 符号→头文件映射（与 expand_assist.py 共用）─────────────
SYMBOL_MAP: list[tuple[str, str]] = [
    # === 容器 ===
    (r'\bstd::vector\b', '<vector>'),
    (r'\bstd::deque\b', '<deque>'),
    (r'\bstd::list\b', '<list>'),
    (r'\bstd::forward_list\b', '<forward_list>'),
    (r'\bstd::array\b', '<array>'),
    (r'\bstd::string\b', '<string>'),
    (r'\bstd::wstring\b', '<string>'),
    (r'\bstd::u8string\b', '<string>'),
    (r'\bstd::string_view\b', '<string_view>'),
    (r'\bstd::map\b', '<map>'),
    (r'\bstd::set\b', '<set>'),
    (r'\bstd::unordered_map\b', '<unordered_map>'),
    (r'\bstd::unordered_set\b', '<unordered_set>'),
    (r'\bstd::multimap\b', '<map>'),
    (r'\bstd::multiset\b', '<set>'),
    (r'\bstd::span\b', '<span>'),
    (r'\bstd::pair\b', '<utility>'),
    (r'\bstd::tuple\b', '<tuple>'),
    (r'\bstd::variant\b', '<variant>'),
    (r'\bstd::optional\b', '<optional>'),
    (r'\bstd::any\b', '<any>'),
    (r'\bstd::expected\b', '<expected>'),
    (r'\bstd::stack\b', '<stack>'),
    (r'\bstd::queue\b', '<queue>'),
    (r'\bstd::priority_queue\b', '<queue>'),
    (r'\bstd::bitset\b', '<bitset>'),
    (r'\bstd::valarray\b', '<valarray>'),
    # === 智能指针 / 内存 ===
    (r'\bstd::unique_ptr\b', '<memory>'),
    (r'\bstd::shared_ptr\b', '<memory>'),
    (r'\bstd::weak_ptr\b', '<memory>'),
    (r'\bstd::make_unique\b', '<memory>'),
    (r'\bstd::make_shared\b', '<memory>'),
    (r'\bstd::allocator\b', '<memory>'),
    (r'\bstd::pmr::', '<memory_resource>'),
    # === IO / 格式化 ===
    (r'\bstd::cout\b', '<iostream>'),
    (r'\bstd::cin\b', '<iostream>'),
    (r'\bstd::cerr\b', '<iostream>'),
    (r'\bstd::endl\b', '<iostream>'),
    (r'\bstd::format\b', '<format>'),
    (r'\bstd::print\b', '<print>'),
    (r'\bstd::fstream\b', '<fstream>'),
    (r'\bstd::ifstream\b', '<fstream>'),
    (r'\bstd::ofstream\b', '<fstream>'),
    (r'\bstd::stringstream\b', '<sstream>'),
    (r'\bstd::ostringstream\b', '<sstream>'),
    (r'\bstd::to_string\b', '<string>'),
    # === 算法 ===
    (r'\bstd::sort\b', '<algorithm>'),
    (r'\bstd::find\b', '<algorithm>'),
    (r'\bstd::copy\b', '<algorithm>'),
    (r'\bstd::for_each\b', '<algorithm>'),
    (r'\bstd::transform\b', '<algorithm>'),
    (r'\bstd::accumulate\b', '<numeric>'),
    (r'\bstd::iota\b', '<numeric>'),
    (r'\bstd::reduce\b', '<numeric>'),
    (r'\bstd::execution::', '<execution>'),
    # === 类型萃取 / 元编程 ===
    (r'\bstd::is_same\b', '<type_traits>'),
    (r'\bstd::enable_if\b', '<type_traits>'),
    (r'\bstd::conditional\b', '<type_traits>'),
    (r'\bstd::decay\b', '<type_traits>'),
    (r'\bstd::remove_reference\b', '<type_traits>'),
    (r'\bstd::integral_constant\b', '<type_traits>'),
    (r'\bstd::true_type\b', '<type_traits>'),
    (r'\bstd::false_type\b', '<type_traits>'),
    (r'\bstd::void_t\b', '<type_traits>'),
    (r'\bstd::conjunction\b', '<type_traits>'),
    (r'\bstd::disjunction\b', '<type_traits>'),
    (r'\bstd::is_trivial_v\b', '<type_traits>'),
    (r'\bstd::is_same_v\b', '<type_traits>'),
    (r'\bstd::enable_if_t\b', '<type_traits>'),
    (r'\bstd::conditional_t\b', '<type_traits>'),
    (r'\bstd::decay_t\b', '<type_traits>'),
    (r'\bstd::remove_reference_t\b', '<type_traits>'),
    # === ranges / concepts / 迭代器 ===
    (r'\bstd::ranges::', '<ranges>'),
    (r'\bstd::views::', '<ranges>'),
    (r'\bstd::input_iterator\b', '<iterator>'),
    (r'\bstd::forward_iterator\b', '<iterator>'),
    (r'\bstd::output_iterator\b', '<iterator>'),
    (r'\bstd::random_access_iterator\b', '<iterator>'),
    (r'\bstd::iterator_traits\b', '<iterator>'),
    (r'\bstd::begin\b', '<iterator>'),
    (r'\bstd::end\b', '<iterator>'),
    (r'\bstd::next\b', '<iterator>'),
    (r'\bstd::advance\b', '<iterator>'),
    (r'\bstd::distance\b', '<iterator>'),
    (r'\bstd::input_iterator_tag\b', '<iterator>'),
    (r'\bstd::contiguous_iterator_tag\b', '<iterator>'),
    # === 函数式 ===
    (r'\bstd::function\b', '<functional>'),
    (r'\bstd::bind\b', '<functional>'),
    (r'\bstd::ref\b', '<functional>'),
    (r'\bstd::cref\b', '<functional>'),
    (r'\bstd::hash\b', '<functional>'),
    (r'\bstd::less\b', '<functional>'),
    (r'\bstd::greater\b', '<functional>'),
    # === 并发 ===
    (r'\bstd::thread\b', '<thread>'),
    (r'\bstd::mutex\b', '<mutex>'),
    (r'\bstd::atomic\b', '<atomic>'),
    (r'\bstd::condition_variable\b', '<condition_variable>'),
    (r'\bstd::future\b', '<future>'),
    (r'\bstd::promise\b', '<future>'),
    (r'\bstd::async\b', '<future>'),
    (r'\bstd::jthread\b', '<thread>'),
    (r'\bstd::latch\b', '<latch>'),
    (r'\bstd::barrier\b', '<barrier>'),
    (r'\bstd::counting_semaphore\b', '<semaphore>'),
    (r'\bstd::lock_guard\b', '<mutex>'),
    (r'\bstd::unique_lock\b', '<mutex>'),
    (r'\bstd::shared_lock\b', '<shared_mutex>'),
    (r'\bstd::shared_mutex\b', '<shared_mutex>'),
    (r'\bstd::scoped_lock\b', '<mutex>'),
    (r'\bstd::once_flag\b', '<mutex>'),
    # === 其他常用 ===
    (r'\bstd::chrono::', '<chrono>'),
    (r'\bstd::filesystem::', '<filesystem>'),
    (r'\bstd::source_location\b', '<source_location>'),
    (r'\bstd::initializer_list\b', '<initializer_list>'),
    (r'\bstd::numeric_limits\b', '<limits>'),
    (r'\bstd::bit_cast\b', '<bit>'),
    (r'\bstd::numbers::', '<numbers>'),
    (r'\bstd::from_chars\b', '<charconv>'),
    (r'\bstd::coroutine_handle\b', '<coroutine>'),
    (r'\bstd::compare_', '<compare>'),
    (r'\bstd::strong_ordering\b', '<compare>'),
    (r'\bstd::weak_ordering\b', '<compare>'),
    (r'\bstd::partial_ordering\b', '<compare>'),
    (r'\bstd::assert\b', '<cassert>'),
    # === C 库 ===
    (r'\bstd::printf\b', '<cstdio>'),
    (r'\bstd::abs\b', '<cstdlib>'),
    (r'\bstd::atoi\b', '<cstdlib>'),
    (r'\bstd::size_t\b', '<cstddef>'),
    (r'\bstd::ptrdiff_t\b', '<cstddef>'),
    (r'\bstd::memcpy\b', '<cstring>'),
    (r'\bstd::memset\b', '<cstring>'),
    (r'\bstd::memmove\b', '<cstring>'),
    (r'\bstd::strlen\b', '<cstring>'),
    (r'\bstd::strcmp\b', '<cstring>'),
    (r'\bstd::malloc\b', '<cstdlib>'),
    (r'\bstd::free\b', '<cstdlib>'),
    (r'\bstd::realloc\b', '<cstdlib>'),
    (r'\bstd::rand\b', '<cstdlib>'),
    (r'\bstd::qsort\b', '<cstdlib>'),
    (r'\bstd::bsearch\b', '<cstdlib>'),
    (r'\bstd::FILE\b', '<cstdio>'),
    (r'\bstd::fopen\b', '<cstdio>'),
    (r'\bstd::fclose\b', '<cstdio>'),
    # === C++ 基本设施 ===
    (r'\bstd::move\b', '<utility>'),
    (r'\bstd::forward\b', '<utility>'),
    (r'\bstd::swap\b', '<utility>'),
    (r'\bstd::exchange\b', '<utility>'),
    (r'\bstd::declval\b', '<utility>'),
    (r'\bstd::index_sequence\b', '<utility>'),
    (r'\bstd::make_index_sequence\b', '<utility>'),
    (r'\bstd::initializer_list\b', '<initializer_list>'),
    (r'\bstatic_assert\b', None),   # 关键字，无需头文件
    (r'\bnoexcept\b', None),
    (r'\bconstexpr\b', None),
    (r'\bconsteval\b', None),
    (r'\bdecltype\b', None),
    (r'\bsizeof\.\.\.\b', None),     # sizeof... 是关键字
    (r'\bconcept\b', None),
    (r'\brequires\b', None),
]


# ── 核心逻辑 ──────────────────────────────────────────────


def detect_missing_includes(block_lines: list[str]) -> list[str]:
    """检测块中使用的 STL 符号，返回缺失的头文件列表"""
    text = "\n".join(block_lines)
    needed = set()
    for pattern, header in SYMBOL_MAP:
        if header is None:
            continue  # 关键字跳过
        if re.search(pattern, text):
            # 检查该头文件是否已在块中
            inc_str = f"#include {header}"
            if inc_str not in text:
                needed.add(header)
    return sorted(needed)


def inject_includes(block_lines: list[str], headers: list[str]) -> list[str]:
    """在 cpp 块顶部注入 #include 行"""
    if not headers:
        return block_lines

    inc_lines = [f"#include {h}" for h in headers]
    result = list(block_lines)

    # 找到首个已有的 #include 行，插入其后；若没有则插在块首非空行之后
    insert_idx = 0
    for i, ln in enumerate(result):
        if ALREADY_INCLUDE.match(ln):
            insert_idx = i + 1
        elif insert_idx == 0 and ln.strip():
            insert_idx = i

    # 如果块首行是 ```cpp 后面的第一行，插在 content 最前面
    if insert_idx == len(result):
        insert_idx = 0

    # 确保前后有空行
    out = result[:insert_idx]
    if out and out[-1].strip():
        out.append("")
    out.extend(inc_lines)
    out.append("")
    out.extend(result[insert_idx:])
    return out


def process_file(fpath: pathlib.Path, dry_run: bool = True) -> dict:
    """处理单个章文件，返回统计信息"""
    lines = fpath.read_text(encoding='utf-8').splitlines()
    stem = fpath.stem
    blocks_total = 0
    blocks_fixed = 0
    blocks_skipped = 0  # 已有 include 或不需要
    new_lines = list(lines)

    i = 0
    while i < len(lines):
        if CPP_FENCE.match(lines[i]):
            fence_line = lines[i]  # ```cpp
            j = i + 1
            buf = []
            while j < len(lines) and not FENCE_END.match(lines[j]):
                buf.append(lines[j])
                j += 1
            blocks_total += 1

            # 已有 #include 的跳过
            if any(ALREADY_INCLUDE.match(ln) for ln in buf):
                blocks_skipped += 1
                i = j + 1
                continue

            missing = detect_missing_includes(buf)
            if missing:
                blocks_fixed += 1
                if not dry_run:
                    new_buf = inject_includes(buf, missing)
                    # 替换原块内容（保留 ```cpp 和 ``` 围栏）
                    new_lines[i+1:j] = new_buf
            else:
                blocks_skipped += 1
            i = j + 1
        else:
            i += 1

    if not dry_run and blocks_fixed > 0:
        # 写备份
        bak = fpath.with_suffix(fpath.suffix + ".auto_include.bak")
        if not bak.exists():
            bak.write_text("\n".join(lines), encoding='utf-8')
        fpath.write_text("\n".join(new_lines), encoding='utf-8')

    return {
        "stem": stem,
        "total": blocks_total,
        "fixed": blocks_fixed,
        "skipped": blocks_skipped,
    }


def process_all(dry_run: bool = True, verify: bool = False,
                target_chapter: str | None = None):
    """主入口"""
    if target_chapter:
        matches = list(ROOT.glob(f"Book/**/{target_chapter}.md"))
        if not matches:
            print(f"  章 '{target_chapter}' 未找到")
            return
        files = [pathlib.Path(m) for m in matches]
    else:
        files = [pathlib.Path(f) for f in sorted(ROOT.glob("Book/**/ch*.md"))]
        files = [f for f in files if '.bak' not in str(f)]

    mode = "DRY-RUN" if dry_run else "APPLY"
    print(f"\n{'='*60}")
    print(f"  auto_include  {mode}  |  {len(files)} 章")
    print(f"{'='*60}\n")

    total_blocks = 0
    total_fixed = 0
    total_skipped = 0
    affected = []

    for fpath in files:
        r = process_file(fpath, dry_run=dry_run)
        if r["fixed"] > 0:
            affected.append(r)
            print(f"  {r['stem']:<35} {r['fixed']:>3} 块补头文件  ({r['total']}块中)")
        total_blocks += r["total"]
        total_fixed += r["fixed"]
        total_skipped += r["skipped"]

    print(f"\n{'─'*60}")
    print(f"  总计: {total_fixed}/{total_blocks} 块可补 ({100*total_fixed/max(1,total_blocks):.1f}%)")
    print(f"  已有 include: {total_skipped}/{total_blocks} 块 ({100*total_skipped/max(1,total_blocks):.1f}%)")
    print(f"  涉及 {len(affected)} 章")
    print(f"{'─'*60}")

    if dry_run:
        print(f"\n  运行 --apply 落盘: python3 tools/auto_include.py --apply")
    else:
        print(f"\n  已落盘，备份 .auto_include.bak。")
        print(f"  回滚: git checkout -- Book/")
        print(f"  验证: python3 tools/auto_include.py --verify")

    if verify and not dry_run:
        # 编译验证：对修改过的章跑 chapter_compile_check
        print(f"\n── 编译验证 ({len(affected)} 章) ──")
        ok = 0
        fail = 0
        for r in affected:
            stem = r["stem"]
            matches = list(ROOT.glob(f"Book/**/{stem}.md"))
            if not matches:
                continue
            cp = subprocess.run(
                ["C:/Users/ASUS/.workbuddy/binaries/python/versions/3.13.12/python.exe",
                 str(ROOT/"tools"/"chapter_compile_check.py"),
                 str(matches[0])],
                capture_output=True, text=True, timeout=120,
            )
            if "0 fail" in cp.stdout or "blocks=0 fail=0" in cp.stdout.lower():
                ok += 1
                print(f"  ✅ {stem}")
            else:
                fail += 1
                last = cp.stdout.strip().splitlines()[-1] if cp.stdout.strip() else cp.stderr[:100]
                print(f"  ❌ {stem}: {last}")
        print(f"\n  编译: {ok} 通过 / {fail} 失败 / {ok+fail} 总计")


# ── CLI ───────────────────────────────────────────────────


def main():
    parser = argparse.ArgumentParser(
        description="自动补全缺失的 STL 头文件",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument("--apply", action="store_true", help="落盘修改（创建 .auto_include.bak 备份）")
    parser.add_argument("--verify", action="store_true", help="落盘后编译验证（需先 --apply）")
    parser.add_argument("--chapter", type=str, help="仅处理指定章")
    args = parser.parse_args()

    dry_run = not args.apply

    if args.chapter and args.apply and not dry_run:
        # 单章先用 dry-run 确认
        process_all(dry_run=True, target_chapter=args.chapter)
        print(f"\n  确认无误后重跑: python3 tools/auto_include.py --apply --chapter {args.chapter}")
        return

    process_all(dry_run=dry_run, verify=args.verify,
                target_chapter=args.chapter)


if __name__ == "__main__":
    main()
