#!/usr/bin/env python3
r"""fix_missing_includes.py — 自动补齐 [merged] 块缺失的标准库 include

背景（2026-07-14, L1 内容质量闭环）：
  compile_all.py --main-only 暴露的失败分三类：
    A 类  找不到外部/自定义头 (fmt/core.h, _ch12_mylib.h, counter.hpp ...)
          —— 多文件工程 / 第三方库演示，单块编译的固有局限，非内容错误。
    B 类  C++20 Modules (import / module 关键字) —— GCC13 支持不完整，演示性质。
    C 类  用了 std::X 却漏了 #include <X> —— 真 bug，本工具专修。
          典型错误串：
            'format' is not a member of 'std'      -> <format>
            'std::chrono' has not been declared    -> <chrono>

策略：
  只处理 C 类。对每个失败章，扫描其所有含 `int main` 的 cpp 块，
  若块内使用了某符号但缺对应 include，则在块首个 #include 行后插入。
  绝不碰 A/B 类（文件缺失 / import / module / 跨块符号未声明）。

用法：
  python3 tools/fix_missing_includes.py            # dry-run，仅报告将改什么
  python3 tools/fix_missing_includes.py --apply     # 实际写入
  python3 tools/fix_missing_includes.py --report tools/compile_report.json
退出码：0=无需修复 / 0=已修复(apply) / 1=检测到可修项(dry-run)
"""

import os, re, sys, json

# 符号 -> 头文件。key 是出现在代码里的字面片段，value 是所需 include。
SYMBOL_HEADER = [
    ('std::format',        '<format>'),
    ('std::print',         '<print>'),
    ('std::println',       '<print>'),
    ('std::chrono',        '<chrono>'),
    ('std::span',          '<span>'),
    ('std::jthread',       '<thread>'),
    ('std::stop_token',    '<stop_token>'),
    ('std::stop_source',   '<stop_token>'),
    ('std::ranges',        '<ranges>'),
    ('std::views',         '<ranges>'),
    ('std::optional',      '<optional>'),
    ('std::variant',       '<variant>'),
    ('std::string_view',   '<string_view>'),
    ('std::bit_cast',      '<bit>'),
    ('std::byteswap',      '<bit>'),
    ('std::source_location','<source_location>'),
    ('std::numbers::',     '<numbers>'),
    ('std::accumulate',    '<numeric>'),
    ('std::iota',          '<numeric>'),
    ('std::function',      '<functional>'),
    ('std::array',         '<array>'),
    ('std::tuple',         '<tuple>'),
    ('std::any',           '<any>'),
    ('std::mutex',         '<mutex>'),
    ('std::lock_guard',    '<mutex>'),
    ('std::unique_lock',   '<mutex>'),
    ('std::scoped_lock',   '<mutex>'),
    ('std::condition_variable', '<condition_variable>'),
    ('std::atomic',        '<atomic>'),
    ('std::atomic_ref',    '<atomic>'),
    ('std::shared_mutex',  '<shared_mutex>'),
    ('std::shared_lock',   '<shared_mutex>'),
    ('std::latch',         '<latch>'),
    ('std::barrier',       '<barrier>'),
    ('std::counting_semaphore', '<semaphore>'),
    ('std::binary_semaphore',   '<semaphore>'),
    ('std::this_thread',   '<thread>'),
    ('std::filesystem',    '<filesystem>'),
]

# 从错误串直接解析缺失符号（更精确，作为主判据）
ERR_PATTERNS = [
    (re.compile(r"'(\w+)' is not a member of 'std'"),      lambda m: 'std::' + m.group(1)),
    (re.compile(r"'std::(\w+)' has not been declared"),    lambda m: 'std::' + m.group(1)),
    (re.compile(r"'std::(\w+)' is not a member"),          lambda m: 'std::' + m.group(1)),
    (re.compile(r"'(\w+)' in namespace 'std' does not name a type"), lambda m: 'std::' + m.group(1)),
]

CPP_FENCE = re.compile(r'(```cpp\n)(.*?)(\n```)', re.S)


def header_for(symbol):
    for frag, hdr in SYMBOL_HEADER:
        if frag == symbol or symbol.startswith(frag) or frag.startswith(symbol):
            return hdr
    # 退化：std::chrono::year -> std::chrono
    base = '::'.join(symbol.split('::')[:2])
    for frag, hdr in SYMBOL_HEADER:
        if frag == base:
            return hdr
    return None


def needed_headers_from_errors(file_failures):
    """从该文件的错误串集合推断需要补的头文件（只认 missing-include 签名）。"""
    hdrs = set()
    for b in file_failures:
        err = b.get('error', '')
        for pat, fn in ERR_PATTERNS:
            m = pat.search(err)
            if m:
                sym = fn(m)
                h = header_for(sym)
                if h:
                    hdrs.add(h)
    return hdrs


def fix_block(block_body, needed):
    """在含 int main 的块里补齐缺失 include。返回 (新块, 补了哪些)。"""
    if 'int main' not in block_body:
        return block_body, []
    added = []
    lines = block_body.split('\n')
    have = set(re.findall(r'#include\s*(<[^>]+>)', block_body))
    to_add = []
    for h in needed:
        if h in have:
            continue
        # 该块是否真的用到了这个头对应的符号
        used = any((frag if frag != '' else h) in block_body
                   for frag, hdr in SYMBOL_HEADER if hdr == h)
        if used:
            to_add.append(h)
    if not to_add:
        return block_body, []
    # 找插入点：最后一个 #include 行之后；若无 include，放在首个非注释行前
    last_inc = -1
    for i, ln in enumerate(lines):
        if ln.strip().startswith('#include'):
            last_inc = i
    if last_inc >= 0:
        for h in to_add:
            lines.insert(last_inc + 1, f'#include {h}')
            last_inc += 1
            added.append(h)
    else:
        ins = 0
        for i, ln in enumerate(lines):
            if not ln.strip().startswith('//') and ln.strip():
                ins = i
                break
        for k, h in enumerate(to_add):
            lines.insert(ins + k, f'#include {h}')
            added.append(h)
    return '\n'.join(lines), added


def main():
    apply = '--apply' in sys.argv
    report = 'tools/compile_report.json'
    if '--report' in sys.argv:
        report = sys.argv[sys.argv.index('--report') + 1]
    if not os.path.exists(report):
        print(f'[ERR] 报告不存在: {report}', file=sys.stderr)
        return 2
    d = json.load(open(report, encoding='utf-8'))
    failures = d.get('failures', [])
    total_fixed_blocks = 0
    total_files = 0
    plan = []
    for f in failures:
        path = f['path']
        needed = needed_headers_from_errors(f['failures'])
        if not needed:
            continue  # A/B 类或非 include 问题，跳过
        if not os.path.exists(path):
            continue
        src = open(path, encoding='utf-8').read()
        file_added = []
        def repl(m):
            body = m.group(2)
            nb, added = fix_block(body, needed)
            if added:
                file_added.append(added)
            return m.group(1) + nb + m.group(3)
        new_src = CPP_FENCE.sub(repl, src)
        if file_added:
            total_files += 1
            total_fixed_blocks += len(file_added)
            plan.append((path, [h for a in file_added for h in a]))
            if apply and new_src != src:
                open(path, 'w', encoding='utf-8', newline='\n').write(new_src)
    verb = '已修复' if apply else '将修复(dry-run)'
    print(f'=== fix_missing_includes {verb} ===')
    for path, hdrs in plan:
        print(f'  {path}: +{hdrs}')
    print(f'--- {total_files} 文件 / {total_fixed_blocks} 块 ---')
    if not apply and plan:
        return 1
    return 0


if __name__ == '__main__':
    sys.exit(main())
