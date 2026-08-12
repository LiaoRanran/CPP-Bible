#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
terminology_normalize.py — 全书术语/格式归一化收口工具
（确定性、约定背书、散文感知、幂等；可接入 CI 作为格式层门禁）。

背景：本书 CONVENTIONS.md 明文规定平台/架构命名约定（第 22、31 行）：
  - `[平台·x86-64]`  —— 架构用连字符形式 x86-64（非下划线 x86_64）
  - `x86-64 / ARM64` —— 64 位 ARM 用 ARM64（非 AArch64/aarch64/arm64）
  - 全文 C++ 用全大写（非 c++）「仅限散文语言名」
本书在成文过程中混用了上述变体。本工具强制归一，守住「同一概念同一写法」的
可读性底线，且**零语义改变**（仅替换散文中的同义术语拼写）。

关于 c++（关键裁定，勿误改）：
  CONVENTIONS 第 152 行写 `-std=c++23`（**小写标志**），第 179 行写 prose 语言名
  `C++20`（**大写**）。本书本就区分：散文语言名 `C++` 大写、编译器标志 `c++23`
  小写。全书 5381 处大写 `C++` 之外，仅剩的小写 `c++` 全部是：
    - 编译器标志 `-std=c++23` / `-std=c++20` …（标志字面量，须小写）
    - 真实路径 `include/c++/`（GCC 头目录，大小写即文件名）
    - 真实库名 `c++_shared` / `libc++`（NDK/LLVM 库名，大小写即身份）
  这些**不是不一致，是正确的**；强改会破坏可编译命令、文件系统路径、库身份。
  故本波【不】归一 `c++`——宁可漏过，绝不误伤（遵循「不确定即跳过」）。
  未来若需归一散文语言名 `c++`，须另写专门规则精确排除上述三类语境。

不变量（安全范围）：
  1) 仅替换【散文】中的术语：围栏代码块（``` / ~~~）、行内代码（`...`）、
     Markdown 链接目标（[text](url) 的 url 部分）、autolink（<...>）一律跳过，
     绝不改动代码、URL、或可能破坏链接的路径。
  2) 约定背书：每条映射都有 CONVENTIONS 明文或全库主导用法支撑，不改变含义。
  3) 幂等：应用一次后再次运行不再产生任何替换。
  4) 保原生换行：读写一律 newline=''，绝不注入 CRLF（守 LF 红线）。
  5) AMD64 故意【不】归一：它是 x86-64 的历史别名，且在「Microsoft AMD64
     calling convention」等专有名词语境下改为 x86-64 可能失真；留待人工裁定。

映射表（pattern 均为散文感知、词边界约束，避免误伤工具链三元组如
x86_64-w64-mingw32 或 aarch64-linux-gnu）：
  x86_64        -> x86-64      (CONVENTIONS §1.1 示例 [平台·x86-64])
  AArch64       -> ARM64       (CONVENTIONS 第22行 x86-64 / ARM64)
  aarch64       -> ARM64
  arm64         -> ARM64       (当前 0 命中：arm64-v8a 等连字符语境已排除，备用)
  # 注：c++（小写）故意不归一——小写 c++NN 是 GCC 标志/路径/库名的正确字面量
  #     （CONVENTIONS 第152行 `-std=c++23`），散文语言名已用大写 `C++`；
  #     全书剩余小写 c++ 全部是上述三类语境，强改会破坏可编译命令与真实路径/库名。

用法：
  python3 tools/terminology_normalize.py            # 报告模式（默认，exit 0）
  python3 tools/terminology_normalize.py --check    # 门禁：有可归一项则 exit 1
  python3 tools/terminology_normalize.py --fix      # 落盘：应用全部归一
"""

import os
import re
import sys
import argparse

ROOT = os.getcwd()
BOOK = os.path.join(ROOT, 'Book')


# ---------- 散文感知：受保护区间（代码/链接/autolink 不替换） ----------
def protected_spans(text):
    """返回 [(start, end), ...] 受保护区间，区间内不做术语替换。"""
    spans = []

    # 1) 围栏代码块 + 行内代码（统一用反引号 run 状态机）
    runs = list(re.finditer(r'`+', text))
    state = 0          # 0=散文 1=行内码 2=围栏
    open_start = None
    for m in runs:
        s, e = m.start(), m.end()
        k = e - s
        if k >= 3:                       # ``` 围栏切换
            if state == 0:
                state = 2; open_start = s
            elif state == 2:
                spans.append((open_start, e)); state = 0; open_start = None
            else:                         # 行内码态内遇围栏：先收行内，再开围栏
                if open_start is not None:
                    spans.append((open_start, s))
                state = 2; open_start = s
        else:                             # 单行反引号
            if state == 0:
                state = 1; open_start = s
            elif state == 1:
                spans.append((open_start, e)); state = 0; open_start = None
            # state==2（围栏内）遇单行反引号：忽略，不切换
    if state != 0 and open_start is not None:
        spans.append((open_start, len(text)))

    # 2) Markdown 链接/图片目标：[text](url) 与 ![alt](url) 的 url 部分
    for m in re.finditer(r'\]\(([^)]*)\)', text):
        spans.append((m.start() + 1, m.end()))          # 含 (...)
    # 3) autolink <...>
    for m in re.finditer(r'<[^\s>]+>', text):
        spans.append((m.start(), m.end()))

    # 合并重叠区间
    spans.sort()
    merged = []
    for a, b in spans:
        if merged and a <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], b))
        else:
            merged.append((a, b))
    return merged


# ---------- 映射表 ----------
# 每条：(名称, 正则, 替换串)。正则均带词边界约束，避免误伤工具链标识符。
MAPPING = [
    ('x86_64->x86-64',
     re.compile(r'(?<![A-Za-z0-9_-])x86_64(?![A-Za-z0-9_-])'),
     'x86-64'),
    ('AArch64->ARM64',
     re.compile(r'(?<![A-Za-z0-9_-])AArch64(?![A-Za-z0-9_-])'),
     'ARM64'),
    ('aarch64->ARM64',
     re.compile(r'(?<![A-Za-z0-9_-])aarch64(?![A-Za-z0-9_-])'),
     'ARM64'),
    ('arm64->ARM64',
     re.compile(r'(?<![A-Za-z0-9_-])arm64(?![A-Za-z0-9_-])'),
     'ARM64'),
    # 注：c++（小写）故意不归一（见文件头裁定）。小写 c++NN 是 GCC 标志/路径/
    # 库名的正确字面量，强改会破坏可编译命令与真实路径/库名，故本波排除。
]


def scan_file(path):
    """返回该文件内的替换操作列表 [(rule_name, start, end, repl), ...]。"""
    with open(path, 'r', encoding='utf-8', errors='replace', newline='') as f:
        text = f.read()
    prot = protected_spans(text)
    def protected(pos):
        return any(a <= pos < b for a, b in prot)
    ops = []
    for name, pat, repl in MAPPING:
        for m in pat.finditer(text):
            if protected(m.start()):
                continue
            ops.append((name, m.start(), m.end(), repl))
    # 按位置排序（映射间无重叠，按顺序拼接即可）
    ops.sort(key=lambda o: o[1])
    return text, ops


def collect():
    """遍历 Book/**/*.md，收集 (path, text, ops)。"""
    results = []
    for dp, _, fns in os.walk(BOOK):
        for fn in sorted(fns):
            if not fn.endswith('.md'):
                continue
            p = os.path.join(dp, fn)
            text, ops = scan_file(p)
            if ops:
                results.append((p, text, ops))
    return results


def apply_ops(text, ops):
    out = []
    last = 0
    for _, s, e, repl in ops:
        out.append(text[last:s]); out.append(repl); last = e
    out.append(text[last:])
    return ''.join(out)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--check', action='store_true',
                    help='门禁模式：存在可归一项则 exit 1')
    ap.add_argument('--fix', action='store_true',
                    help='落盘：应用全部归一')
    args = ap.parse_args()

    results = collect()

    # 统计
    total = 0
    per_rule = {name: 0 for name, _, _ in MAPPING}
    per_file = {}
    for p, _, ops in results:
        per_file[p] = len(ops)
        total += len(ops)
        for name, s, e, _ in ops:
            per_rule[name] += 1

    print('=== 术语/格式归一化报告 ===')
    print('波及文件:', len(results), ' 拟替换总数:', total)
    print('--- 按规则 ---')
    for name, _, _ in MAPPING:
        print('  %-18s %4d' % (name, per_rule[name]))
    print('--- 按文件（前 40，完整见 git diff）---')
    for p, _, ops in results[:40]:
        print('  %4d  %s' % (len(ops), os.path.relpath(p, ROOT)))
    if len(results) > 40:
        print('  ... 其余 %d 文件' % (len(results) - 40))

    if args.fix:
        n_file = 0
        for p, text, ops in results:
            new = apply_ops(text, ops)
            with open(p, 'w', encoding='utf-8', newline='') as f:
                f.write(new)
            n_file += 1
        print('--- fix done: 改写 %d 文件，共 %d 处' % (n_file, total),
              file=sys.stderr)

    if args.check:
        sys.exit(1 if total > 0 else 0)


if __name__ == '__main__':
    main()
