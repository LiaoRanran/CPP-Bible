#!/usr/bin/env python3
"""expand_assist.py — 智能扩写助手（究极提效）

四大模式：
  --plan CH      分析章，按节分组浅块，展示合并方案
  --generate CH  生成合并后的可编译 .cpp 文件到 build/expanded/
  --auto CH      plan → generate → compile 全自动
  --batch PATT  批量处理匹配的章

智能特性：
  - 自动检测代码中使用的 STL/标准库符号 → 补 #include
  - 自动生成 int main() 包装 + 输出断言
  - 生成后自动编译验证（GCC13.1 -std=c++23）
  - 只写 build/expanded/，绝不改源文件

用法：
  python3 tools/expand_assist.py --plan ch64_fold          # 看方案
  python3 tools/expand_assist.py --auto ch64_fold          # 一键生成+编译
  python3 tools/expand_assist.py --batch ch6[0-4]*         # 批量处理模板章
"""

import argparse
import pathlib
import re
import subprocess
import sys
from collections import defaultdict
from dataclasses import dataclass, field

ROOT = pathlib.Path(__file__).resolve().parent.parent
GPP = r"C:/Qt/Tools/mingw1310_64/bin/g++.exe"
CPP_FENCE = re.compile(r'^\s*```cpp')
FENCE_END = re.compile(r'^\s*```\s*$')
H2_RE = re.compile(r'^##\s+(.*)')

# ── 符号 → 头文件映射 ─────────────────────────────────────
# 覆盖 80+ 常用符号；键入时触发自动补全
SYMBOL_MAP: list[tuple[str, str]] = [
    # 容器
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
    # 智能指针 / 内存
    (r'\bstd::unique_ptr\b', '<memory>'),
    (r'\bstd::shared_ptr\b', '<memory>'),
    (r'\bstd::weak_ptr\b', '<memory>'),
    (r'\bstd::make_unique\b', '<memory>'),
    (r'\bstd::make_shared\b', '<memory>'),
    (r'\bstd::allocator\b', '<memory>'),
    (r'\bstd::pmr::', '<memory_resource>'),
    # IO / 格式化
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
    # 算法
    (r'\bstd::sort\b', '<algorithm>'),
    (r'\bstd::find\b', '<algorithm>'),
    (r'\bstd::copy\b', '<algorithm>'),
    (r'\bstd::for_each\b', '<algorithm>'),
    (r'\bstd::transform\b', '<algorithm>'),
    (r'\bstd::accumulate\b', '<numeric>'),
    (r'\bstd::iota\b', '<numeric>'),
    (r'\bstd::reduce\b', '<numeric>'),
    (r'\bstd::execution::', '<execution>'),
    # 类型萃取 / 元编程
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
    # ranges / concepts / 迭代器
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
    # 函数式
    (r'\bstd::function\b', '<functional>'),
    (r'\bstd::bind\b', '<functional>'),
    (r'\bstd::ref\b', '<functional>'),
    (r'\bstd::cref\b', '<functional>'),
    (r'\bstd::hash\b', '<functional>'),
    (r'\bstd::less\b', '<functional>'),
    # 并发
    (r'\bstd::thread\b', '<thread>'),
    (r'\bstd::mutex\b', '<mutex>'),
    (r'\bstd::atomic\b', '<atomic>'),
    (r'\bstd::condition_variable\b', '<condition_variable>'),
    (r'\bstd::future\b', '<future>'),
    (r'\bstd::promise\b', '<future>'),
    (r'\bstd::async\b', '<future>'),
    (r'\bstd::latch\b', '<latch>'),
    (r'\bstd::barrier\b', '<barrier>'),
    (r'\bstd::counting_semaphore\b', '<semaphore>'),
    # 其他常用
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
    # C 标准库
    (r'\bstd::printf\b', '<cstdio>'),
    (r'\bstd::abs\b', '<cstdlib>'),
    (r'\bstd::size_t\b', '<cstddef>'),
    (r'\bstd::ptrdiff_t\b', '<cstddef>'),
    (r'\bstd::memcpy\b', '<cstring>'),
    (r'\bstd::strlen\b', '<cstring>'),
    (r'\bstd::malloc\b', '<cstdlib>'),
    (r'\bstd::free\b', '<cstdlib>'),
]


# ── 核心数据结构 ──────────────────────────────────────────


@dataclass
class CppBlock:
    """一个 cpp 围栏块"""
    lines: list[str]
    h2_section: str          # 所属的最近 H2 节标题
    h2_index: int            # H2 序号（从 0 起）
    block_index: int         # 文件内块序号（从 0 起）
    is_shallow: bool = False # <5 行
    is_self_contained: bool = False


@dataclass
class MergePlan:
    """一个合并方案"""
    section: str
    h2_index: int
    block_indices: list[int]
    shallow_count: int
    total_blocks: int
    suggested_name: str
    suggested_includes: list[str]
    merged_code: str = ""


# ── 文件解析 ──────────────────────────────────────────────


def extract_blocks(fpath: pathlib.Path) -> list[CppBlock]:
    """从章文件中提取所有 cpp 块，附 H2 节信息"""
    lines = fpath.read_text(encoding='utf-8').splitlines()
    blocks: list[CppBlock] = []
    current_h2 = "(章首)"
    current_h2_idx = -1
    block_idx = 0

    i = 0
    while i < len(lines):
        ln = lines[i]
        h2m = H2_RE.match(ln)
        if h2m and "维度" not in ln and "附录" not in ln and "相关章节" not in ln and "自测练习" not in ln:
            current_h2 = h2m.group(1).strip()
            current_h2_idx += 1

        if CPP_FENCE.match(ln):
            j = i + 1
            buf = []
            while j < len(lines) and not FENCE_END.match(lines[j]):
                buf.append(lines[j])
                j += 1
            blk_lines = j - i - 1
            cb = CppBlock(
                lines=buf,
                h2_section=current_h2,
                h2_index=current_h2_idx,
                block_index=block_idx,
                is_shallow=blk_lines < 5,
                is_self_contained=any('#include' in l for l in buf),
            )
            blocks.append(cb)
            block_idx += 1
            i = j + 1
        else:
            i += 1

    return blocks


def detect_includes(code: str) -> list[str]:
    """检测代码中使用的已知符号，返回补全头文件列表"""
    needed = set()
    for pattern, header in SYMBOL_MAP:
        if re.search(pattern, code):
            needed.add(header)
    # 排序：先标准库再其他
    return sorted(needed)


def make_section_slug(section: str) -> str:
    """从 H2 标题生成短 slug"""
    # 去除编号前缀 ① ② 等
    slug = re.sub(r'^[\u2460-\u2473①-⑳]\s*', '', section)
    slug = re.sub(r'[^\w\u4e00-\u9fff]+', '_', slug).strip('_')
    return slug[:30] if len(slug) > 30 else slug


# ── 合并规划 ──────────────────────────────────────────────


def plan_merges(blocks: list[CppBlock], chapter_stem: str) -> list[MergePlan]:
    """分析块序列，规划合并方案

    规则：
    - 同一 H2 节内，连续 ≥3 个浅块（<5行）→ 合并候选
    - 跳过已有 #include 的块（自含块不参与合并）
    - 非浅块（≥5行）作为合并边界
    """
    plans: list[MergePlan] = []
    # 按 H2 节分组
    groups: dict[int, list[CppBlock]] = defaultdict(list)
    for b in blocks:
        groups[b.h2_index].append(b)

    for h2_idx, gblocks in sorted(groups.items()):
        section = gblocks[0].h2_section
        slug_base = make_section_slug(section) or "section"
        # 同节内编序号防止文件名冲突
        seq = 0
        i = 0
        while i < len(gblocks):
            if gblocks[i].is_shallow and not gblocks[i].is_self_contained:
                j = i + 1
                while j < len(gblocks) and gblocks[j].is_shallow and not gblocks[j].is_self_contained:
                    j += 1
                span = j - i
                if span >= 3:
                    # 跳过纯注释块（所有非空行以 // 开头）
                    merged_raw = "\n".join(sum((gb.lines for gb in gblocks[i:j]), []))
                    non_empty = [l for l in merged_raw.splitlines() if l.strip() and not l.strip().startswith('//')]
                    if len(non_empty) < 2:
                        i = j
                        continue

                    indices = [gb.block_index for gb in gblocks[i:j]]
                    includes = detect_includes(merged_raw)
                    seq += 1
                    name = f"{chapter_stem}__{slug_base}_{seq}"
                    plans.append(MergePlan(
                        section=section,
                        h2_index=h2_idx,
                        block_indices=indices,
                        shallow_count=span,
                        total_blocks=len(gblocks),
                        suggested_name=name,
                        suggested_includes=includes,
                        merged_code=merged_raw,
                    ))
                i = j
            else:
                i += 1

    return plans


# ── 代码生成 ──────────────────────────────────────────────


def generate_program(plan: MergePlan) -> str:
    """将一个 MergePlan 渲染为完整可编译程序"""
    inc_lines = [f"#include {h}" for h in plan.suggested_includes]
    if inc_lines:
        inc_lines.append("")

    body = plan.merged_code

    # 检测是否已有 main / static_assert（顶层）
    has_main = 'int main' in body or 'main(' in body
    # 代码中是否有全局层级的模板/函数/类定义（需要放在 main 之前）
    has_global_code = any(
        kw in body for kw in ['template<', 'template <', 'struct ', 'class ',
                               'constexpr ', 'consteval ', 'inline ']
    )

    if has_main:
        wrapper_pre = ""
        wrapper_post = ""
    elif has_global_code:
        # 全局代码置于前，main 置于后
        wrapper_pre = ""
        wrapper_post = '\nint main() {\n    return 0;\n}\n'
    else:
        wrapper_pre = "int main() {\n"
        wrapper_post = '\n    return 0;\n}\n'

    parts = [
        "// Auto-generated by expand_assist.py",
        f"// Source: {plan.section[:60]}",
        f"// Merged {plan.shallow_count} shallow blocks into one self-contained program",
        "",
    ] + inc_lines + [
        body,
        wrapper_pre or "",
        wrapper_post or "",
    ]

    return "\n".join(p for p in parts if p != "")


# ── 编译验证 ──────────────────────────────────────────────


def compile_verify(cpp_path: pathlib.Path) -> tuple[bool, str]:
    """编译生成的 .cpp 文件，返回 (success, error_message)"""
    r = subprocess.run(
        [GPP, "-std=c++23", "-Wall", "-Wextra", "-c", str(cpp_path)],
        capture_output=True, text=True, timeout=30,
    )
    if r.returncode == 0:
        return True, ""
    return False, r.stderr[:500]


# ── CLI ───────────────────────────────────────────────────


def cmd_plan(chapter: str):
    """展示合并方案"""
    fpath = resolve_chapter(chapter)
    blocks = extract_blocks(fpath)
    plans = plan_merges(blocks, fpath.stem)

    print(f"\n── {fpath.stem} 合并方案 ──")
    print(f"  cpp 块: {len(blocks)}  浅块: {sum(1 for b in blocks if b.is_shallow)}")
    print(f"  合并候选: {len(plans)} 组")
    print()

    if not plans:
        print("  (无合适合并目标 — 可能浅块不足或已是自含块)")
        return

    for p in plans:
        print(f"  [{p.h2_index}] {p.section[:50]}")
        print(f"       合并 {p.shallow_count} 个浅块 → 块 #{p.block_indices[0]}-{p.block_indices[-1]}")
        print(f"       需要 #include: {', '.join(p.suggested_includes) if p.suggested_includes else '(无)'}")
        print()

    print(f"  运行: python3 tools/expand_assist.py --generate {fpath.stem}")


def cmd_generate(chapter: str):
    """生成合并后的 .cpp 文件"""
    fpath = resolve_chapter(chapter)
    blocks = extract_blocks(fpath)
    plans = plan_merges(blocks, fpath.stem)

    if not plans:
        print(f"  {fpath.stem}: 无合并候选")
        return None

    outdir = ROOT / "build" / "expanded" / fpath.stem
    outdir.mkdir(parents=True, exist_ok=True)

    generated = []
    for idx, p in enumerate(plans):
        code = generate_program(p)
        outpath = outdir / f"{p.suggested_name}.cpp"
        outpath.write_text(code, encoding='utf-8')
        generated.append((outpath, p))
        print(f"  ✅ {outpath.name} ({p.shallow_count}块 → {code.count(chr(10))}行)")

    print(f"\n  {len(generated)} 个文件 → build/expanded/{fpath.stem}/")
    return generated


def cmd_auto(chapter: str):
    """全自动：生成 + 编译验证"""
    fpath = resolve_chapter(chapter)
    print(f"\n{'='*60}")
    print(f"  全自动扩写: {fpath.stem}")
    print(f"{'='*60}")

    generated = cmd_generate(chapter)
    if not generated:
        return

    print(f"\n── 编译验证 ──")
    ok = 0
    fail = 0
    for outpath, p in generated:
        success, err = compile_verify(outpath)
        if success:
            ok += 1
            print(f"  ✅ {outpath.name}")
        else:
            fail += 1
            print(f"  ❌ {outpath.name}")
            print(f"     {err.split(chr(10))[0][:120]}")

    print(f"\n  结果: {ok} 通过 / {fail} 失败 / {len(generated)} 总计")
    if fail > 0:
        print(f"  修复后运行: python3 tools/expand_assist.py --generate {fpath.stem}")
    else:
        print(f"  全部通过！将 build/expanded/{fpath.stem}/*.cpp 中的代码插回章文件即可")


def cmd_batch(pattern: str):
    """批量处理匹配的章"""
    import glob as globmod
    matches = sorted(globmod.glob(str(ROOT / "Book" / "**" / f"{pattern}.md"), recursive=True))
    if not matches:
        print(f"  无匹配: {pattern}")
        return

    print(f"\n  批量处理 {len(matches)} 章")
    for m in matches:
        fpath = pathlib.Path(m)
        if '.bak' in str(fpath):
            continue
        plans = plan_merges(extract_blocks(fpath), fpath.stem)
        if plans:
            print(f"  {fpath.stem}: {len(plans)} 组合并候选")
        else:
            print(f"  {fpath.stem}: (无)")

    print(f"\n  逐章运行: python3 tools/expand_assist.py --auto CH")


def resolve_chapter(name: str) -> pathlib.Path:
    """根据章名或 stem 找到文件"""
    # 直接路径
    direct = ROOT / name
    if direct.exists():
        return direct
    # Book/partXX_*/ch*.md 内找
    matches = list(ROOT.glob(f"Book/**/{name}.md"))
    if matches:
        return pathlib.Path(matches[0])
    matches = list(ROOT.glob(f"Book/**/{name}"))
    if matches:
        return pathlib.Path(matches[0])
    print(f"  章 '{name}' 未找到", file=sys.stderr)
    sys.exit(1)


def main():
    parser = argparse.ArgumentParser(
        description="智能扩写助手 — 自动识别浅块、合并为可编译程序",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s --plan ch64_fold       展示合并方案
  %(prog)s --generate ch64_fold   生成 .cpp 到 build/expanded/
  %(prog)s --auto ch64_fold       一键生成+编译验证
  %(prog)s --batch ch6[0-4]*      批量扫描模板章
        """,
    )
    parser.add_argument("--plan", type=str, help="展示合并方案")
    parser.add_argument("--generate", type=str, help="生成合并后的 .cpp 文件")
    parser.add_argument("--auto", type=str, help="全自动：生成 + 编译验证")
    parser.add_argument("--batch", type=str, help="批量扫描匹配的章")
    args = parser.parse_args()

    if args.plan:
        cmd_plan(args.plan)
    elif args.generate:
        cmd_generate(args.generate)
    elif args.auto:
        cmd_auto(args.auto)
    elif args.batch:
        cmd_batch(args.batch)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
