#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
normalize_headings.py — 将 CPP-Bible 章节的 H2 小节标题归一化为 ①–⑳ 圈码标记格式。

规则：
  1. 剥离现有任意编号前缀（中文数字 / 阿拉伯数字 / 元素 N / 44.N / 圈码 / KPn / （续））。
  2. 内容小节（body）按顺序赋 ①,②,…；前 20 个用圈码，超出 20 的小节保持为无编号 H2
     （绝不重复圈码，满足"无重复、无遗漏、连续"）。
  3. 辅助小节（目录/附录/源码阅读路线/小结/速查/交叉引用/附： 等）不编号，保留原文。
  4. 绝不产生空标题。
用法：
  python tools/normalize_headings.py --root <CPP-Bible> --apply
  python tools/normalize_headings.py --root <CPP-Bible>           # 试运行（只打印摘要）
"""
import argparse, re, pathlib, sys

CIRCLED = ['①','②','③','④','⑤','⑥','⑦','⑧','⑨','⑩',
           '⑪','⑫','⑬','⑭','⑮','⑯','⑰','⑱','⑲','⑳']

# 辅助小节关键字（命中则不当作编号 body）
AUX_KW = ['目录','核心知识点 23 项','速查','源码阅读路线','附录','小结','交叉引用',
          '自测','速记','阅读清单','可编译示例索引','程序索引','附：','附:',
          '一页速查','本章速记','全章可编译示例','完整自测','知识点深挖',
          '23 项核心','附：全章','本章导航']

def strip_prefix(title: str) -> str:
    t = title.strip()
    # 去掉 （续）/ 续
    t = re.sub(r'^（续）\s*', '', t)
    t = re.sub(r'^续\s*', '', t)
    # 中文数字 一、二、…
    t = re.sub(r'^[一二三四五六七八九十百零]+[、.．\s]+', '', t)
    # 元素 N
    t = re.sub(r'^元素\s*\d+\s*[·.、\s]*', '', t)
    # 44.N / N.N
    t = re.sub(r'^\d+\.\d+\s*[·.、\s]*', '', t)
    # 阿拉伯 N. / N、
    t = re.sub(r'^\d+[.、．\s]+', '', t)
    # 圈码：先处理 "⑳（续）" 附着形式，再剥离普通 "① 标题" 形式
    # 注意：不可写成 ^[①-⑳]\s*（续）?\s* —— 该可选组在本环境会令整条正则失配。
    t = re.sub(r'^[①-⑳]\s*（续）', '', t)
    t = re.sub(r'^[①-⑳]\s*', '', t)
    # [元素NN] 前缀（ch41 风格）
    t = re.sub(r'^\[元素\s*\d+\]\s*', '', t)
    # KPn
    t = re.sub(r'^KP\d+\s*[·.、\s]*', '', t)
    # 末尾 [核心知识点...] 标签（ch41 风格，剥离不保留）
    t = re.sub(r'(\s*\[核心知识点[^\]]*\])+\s*$', '', t)
    # 清掉 "20 元素 · N/M" 噪声，但保留其后真实注释
    t = re.sub(r'20 元素\s*·\s*\d+/\d+', '', t)
    t = re.sub(r'（\s*·\s*', '（', t)
    t = re.sub(r'（）', '', t)
    return t.strip()

def is_aux(title: str) -> bool:
    # 仅当标题「以」辅助关键字开头才算辅助小节，避免正文标题含有关键字被误判
    return any(title.startswith(kw) for kw in AUX_KW)

def normalize_file(path: pathlib.Path, apply: bool):
    lines = path.read_text(encoding='utf-8').splitlines()
    out = []
    body_n = 0
    aux_n = 0
    overflow = []
    circled_used = []
    problems = []
    i = 0
    while i < len(lines):
        line = lines[i]
        m = re.match(r'^(##)\s+(.*)$', line)
        if m:
            raw_title = m.group(2).strip()
            clean = strip_prefix(raw_title)
            if not clean:
                clean = raw_title  # 兜底，避免空标题
                problems.append(f"空标题兜底: {raw_title!r}")
            if is_aux(clean):
                new_line = f"## {clean}"
                aux_n += 1
            else:
                body_n += 1
                if body_n <= 20:
                    new_line = f"## {CIRCLED[body_n-1]} {clean}"
                    circled_used.append(CIRCLED[body_n-1])
                else:
                    new_line = f"## {clean}"   # 超出 20：无编号 H2，不重复圈码
                    overflow.append(clean)
            out.append(new_line)
        else:
            out.append(line)
        i += 1
    # 重复圈码检测（理论上不应发生）
    if len(circled_used) != len(set(circled_used)):
        problems.append("检测到重复圈码!")
    if apply:
        import shutil
        bak = path.with_suffix(path.suffix + '.bak')
        if not bak.exists():
            shutil.copy2(path, bak)
        path.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    return {
        'file': str(path),
        'h2_total': body_n + aux_n,
        'body': body_n,
        'aux': aux_n,
        'circled': len(circled_used),
        'overflow': overflow,
        'problems': problems,
    }

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', required=True)
    ap.add_argument('--apply', action='store_true')
    args = ap.parse_args()
    root = pathlib.Path(args.root)
    targets = [
        'Book/part03_language/ch19_variables.md',
        'Book/part03_language/ch20_reference_pointer.md',
        'Book/part03_language/ch21_const_family.md',
        'Book/part03_language/ch22_auto_decltype.md',
        'Book/part03_language/ch23_namespace_adl.md',
        'Book/part03_language/ch24_enum.md',
        'Book/part03_language/ch25_union_variant.md',
        'Book/part03_language/ch26_lambda.md',
        'Book/part03_language/ch27_cast.md',
        'Book/part03_language/ch28_lifetime_ub.md',
        'Book/part04_memory/ch35_memory_layout.md',
        'Book/part04_memory/ch36_stack_heap.md',
        'Book/part04_memory/ch37_new_delete.md',
        'Book/part04_memory/ch38_allocator.md',
        'Book/part04_memory/ch39_raii_rule.md',
        'Book/part04_memory/ch40_exception_safety.md',
        'Book/part04_memory/ch41_smart_pointers.md',
        'Book/part04_memory/ch42_strict_aliasing.md',
        'Book/part04_memory/ch43_cache_locality.md',
        'Book/part04_memory/ch44_memory_pool.md',
        'Book/part05_oo/ch45_oop_object_model.md',
        'Book/part05_oo/ch46_encapsulation_inheritance.md',
    ]
    print(f"{'FILE':50} H2  body  aux  circled  overflow  problems")
    any_problem = False
    for rel in targets:
        p = root / rel
        if not p.exists():
            print(f"MISSING: {rel}")
            continue
        r = normalize_file(p, apply=args.apply)
        flag = "!" if (r['problems'] or r['overflow']) else " "
        print(f"{flag} {rel:48} {r['h2_total']:4} {r['body']:4} {r['aux']:4} {r['circled']:5}    {len(r['overflow']):3}     {r['problems']}")
        if r['problems']:
            any_problem = True
            for o in r['overflow']:
                print(f"      overflow> {o}")
    print("\nMODE:", "APPLY (已写入)" if args.apply else "DRY-RUN (未写入)")
    if any_problem:
        print("⚠ 存在需要处理的问题，请检查上方 overflow / problems。")

if __name__ == '__main__':
    main()
