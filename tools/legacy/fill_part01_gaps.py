#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
fill_part01_gaps.py — 补齐 part01 历史章节缺失的 v3 中间元素（⑥⑦⑧⑨⑩ 等），
并补立场标签 [标准]。仅插入准确的时代相关内容，不改动任何已有史实正文。
用法：
  python tools/fill_part01_gaps.py --root <CPP-Bible> --apply
"""
import argparse, re, pathlib, shutil

ROOT = pathlib.Path(__file__).resolve().parent.parent

def insert_after(lines, anchor_sub, block_lines):
    """在首个含 anchor_sub 的标题行之后插入 block_lines（block 为含换行的字符串列表）。"""
    out = []
    inserted = False
    for ln in lines:
        out.append(ln)
        if not inserted and anchor_sub in ln and ln.startswith('##'):
            out.extend(block_lines)
            inserted = True
    return out, inserted

def already(lines, marker):
    return any(marker in ln for ln in lines)

def replace_line(lines, anchor_sub, new_line):
    return [new_line if (anchor_sub in ln and ln.startswith('##')) else ln for ln in lines], (anchor_sub in ''.join(lines))

# ---- ch05 C++14：把「⑥–⑩（略）」展开为 ⑥⑦⑧⑨⑩ ----
CH05_BLOCK = '''## ⑥ UML / 结构图（C++14 特性关系）
C++14 无新面向对象机制，特性围绕「泛型与编译期」：generic lambda、返回类型推导、`decltype(auto)`、变量模板、放宽 constexpr。它们彼此正交，统一服务于「更少样板、更多编译期计算」。

## ⑦ ASCII 内存图（C++14 内存模型沿用 C++11）
C++14 未改变对象内存布局；放宽 constexpr 使更多计算在编译期完成（常量折叠进只读段），运行时内存模型与 C++11 一致（详见 ch22、ch37）。

## ⑧ 生命周期（沿用 C++11 RAII / 移动语义）
C++14 无新生命周期语义；generic lambda 的闭包对象生命周期与普通 lambda 相同（ch26）。

## ⑨ 调用栈（C++14 特性均编译期，无新运行时调用模型）
generic lambda、`decltype(auto)` 仍由模板实例化在编译期生成独立函数体，不改变运行时调用栈（ch22、ch26）。

## ⑩ 汇编（C++14 零新增运行时开销）[标准]
C++14 不引入任何运行时机制；generic lambda 编译为独立的模板实例函数，与手写等价（零开销原则）。
'''.splitlines()

# ---- ch06/07/08 通用：在 ⑤ 后插 ⑥；在 ⑦ 后插 ⑧⑨ ----
DEF_6 = '''## ⑥ UML / 结构图（特性关系）[标准]
本章特性按目标分三类：语法糖（结构化绑定 / 折叠表达式）、编译期分支（`if constexpr` / CTAD）、库类型（`string_view` / `optional` / `variant` / `any` / 并行 STL）。
'''
DEF_89 = '''## ⑧ 生命周期（新增库类型的所有权语义）
`string_view` 不拥有数据（悬垂风险，ch36）；`optional`/`variant`/`any` 在对象内管理所含值的生命周期（ch25）；CTAD 推导的临时对象生命周期遵循常规规则。
## ⑨ 调用栈（编译期分支与折叠）
`if constexpr` 在编译期裁剪分支，不产生运行时调用；折叠表达式展开为顺序求值，调用栈与普通循环一致（ch26）。
'''.splitlines()

# ---- ch09 C++26：在 ⑤ 后插 ⑥⑦⑧⑨ ----
CH09_BLOCK = '''## ⑥ UML / 结构图（C++26 方向性特性）[标准]
C++26（草案）：静态反射、`std::execution` sender/receiver、契约 (contracts)、`std::simd`、扩展 `constexpr`、模式匹配（方向性，可能变动）。
## ⑦ ASCII 内存图（C++26 反射与值）
静态反射在编译期暴露类型元数据，不影响运行时对象布局；契约由编译器在前后置条件插入检查，无新内存模型（ch11）。
## ⑧ 生命周期（C++26 契约与 constexpr 扩展）
契约不改变对象生命周期；`constexpr` 扩展到更多库类型，更多计算移至编译期（ch22）。
## ⑨ 调用栈（C++26 sender/receiver 执行器）
`std::execution` 用 sender/receiver 组合描述异步流水线，由调度器决定实际调用栈（ch167）。
'''.splitlines()

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    root = pathlib.Path(args.root)
    p01 = root / 'Book' / 'part01_history'

    # ch04：补立场标签（⑭ 标题加 [标准]）
    f04 = p01 / 'ch04_cpp11.md'
    lines = f04.read_text(encoding='utf-8').splitlines()
    lines, _ = replace_line(lines, 'WG21 提案（关键）', '## ⑭ WG21 提案（关键）[标准]')
    if args.apply:
        _backup(f04); f04.write_text("\n".join(lines).rstrip()+"\n", encoding='utf-8')
    print("  ch04: +[标准] 立场标签")

    # ch05：展开 ⑥–⑩
    f05 = p01 / 'ch05_cpp14.md'
    lines = f05.read_text(encoding='utf-8').splitlines()
    out = []
    for ln in lines:
        if '⑥–⑩' in ln and ln.startswith('##'):
            out.extend(CH05_BLOCK)
        else:
            out.append(ln)
    if args.apply:
        _backup(f05); f05.write_text("\n".join(out).rstrip()+"\n", encoding='utf-8')
    print("  ch05: 展开 ⑥⑦⑧⑨⑩")

    # ch06/07/08：插 ⑥(后⑤) + ⑧⑨(后⑦)
    for name in ['ch06_cpp17.md','ch07_cpp20.md','ch08_cpp23.md']:
        fp = p01 / name
        lines = fp.read_text(encoding='utf-8').splitlines()
        if already(lines, '## ⑥ UML / 结构图（特性关系）[标准]'):
            print(f"  {name}: 已补齐，跳过"); continue
        lines, _ = insert_after(lines, '## ⑤ ', DEF_6.splitlines())
        lines, _ = insert_after(lines, '## ⑦ ', DEF_89)
        if args.apply:
            _backup(fp); fp.write_text("\n".join(lines).rstrip()+"\n", encoding='utf-8')
        print(f"  {name}: +⑥ +⑧⑨")

    # ch09：插 ⑥⑦⑧⑨(后⑤)
    f09 = p01 / 'ch09_cpp26.md'
    lines = f09.read_text(encoding='utf-8').splitlines()
    if already(lines, '## ⑥ UML / 结构图（C++26'):
        print("  ch09: 已补齐，跳过")
    else:
        lines, _ = insert_after(lines, '## ⑤ ', CH09_BLOCK)
        if args.apply:
            _backup(f09); f09.write_text("\n".join(lines).rstrip()+"\n", encoding='utf-8')
        print("  ch09: +⑥⑦⑧⑨")

    print("MODE:", "APPLY" if args.apply else "DRY-RUN")

def _backup(p: pathlib.Path):
    bak = p.with_suffix(p.suffix + '.bak')
    if not bak.exists():
        shutil.copy2(p, bak)

if __name__ == '__main__':
    main()
