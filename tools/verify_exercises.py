#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
verify_exercises.py — Phase 2 练习闭环验证器

仅编译每章「## 自测练习（Exercises）」小节内的 ```cpp 块，
确认注入的练习题答案真实可编译（C++23 / GCC13 / -Wall -Wextra）。
不编译正文块，故速度远快于 chapter_compile_check，适合全量快速复验。

用法：
  python3 tools/verify_exercises.py            # 全部章
  python3 tools/verify_exercises.py Book/partXX/chYY.md   # 单章
  python3 tools/verify_exercises.py --summary   # 仅打印汇总
"""
import re, os, sys, subprocess, tempfile, argparse

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
GPP = "g++"
FLAGS = ["-std=c++23", "-O0", "-fsyntax-only", "-Wall", "-Wextra"]

SEC_HDR = "## 自测练习（Exercises）"


def collect_blocks(md_path):
    """返回该章练习小节内的 (block_index, src) 列表。"""
    text = open(md_path, encoding="utf-8").read()
    idx = text.rfind(SEC_HDR)
    if idx < 0:
        return []
    sec = text[idx:]
    blocks = re.findall(r"```cpp(.*?)```", sec, re.S)
    out = []
    for i, b in enumerate(blocks, 1):
        src = b.strip() + "\n"
        # 去掉可能混入的 HTML details 标签
        src = re.sub(r"</?details[^>]*>", "", src)
        out.append((i, src))
    return out


def compile_src(src):
    with tempfile.NamedTemporaryFile("w", suffix=".cpp", delete=False, encoding="utf-8") as tf:
        tf.write(src)
        p = tf.name
    r = subprocess.run([GPP, *FLAGS, p], capture_output=True, text=True)
    os.unlink(p)
    return r.returncode, r.stderr.strip()


def verify_file(md_path):
    blocks = collect_blocks(md_path)
    if not blocks:
        return None  # 无练习小节
    fails = []
    for i, src in blocks:
        rc, err = compile_src(src)
        if rc != 0:
            fails.append((i, err))
    return (len(blocks), fails)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="*", help="指定章 md；缺省=Book 下全部 ch*.md")
    ap.add_argument("--summary", action="store_true", help="仅汇总")
    args = ap.parse_args()

    if args.paths:
        files = [p if os.path.isabs(p) else os.path.join(ROOT, p) for p in args.paths]
    else:
        files = sorted(
            os.path.join(dp, f)
            for dp, _, fs in os.walk(os.path.join(ROOT, "Book"))
            for f in fs
            if re.match(r"ch\d+_.*\.md$", f)
        )

    total_blocks = 0
    total_files = 0
    fail_files = 0
    fail_blocks = 0
    details = []
    for fp in files:
        res = verify_file(fp)
        if res is None:
            continue
        n, fails = res
        total_files += 1
        total_blocks += n
        if fails:
            fail_files += 1
            fail_blocks += len(fails)
            rel = os.path.relpath(fp, ROOT)
            for i, err in fails:
                details.append(f"  [FAIL] {rel} 练习块#{i}\n{err[:280]}")
                if not args.summary:
                    print(f"  [FAIL] {rel} 练习块#{i}")
                    print("    " + err[:280].replace("\n", "\n    "))

    print(f"\n=== 练习闭环验证: 章={total_files} 练习块={total_blocks} "
          f"失败章={fail_files} 失败块={fail_blocks} ===")
    if details and args.summary:
        print("\n".join(details))
    sys.exit(1 if fail_blocks else 0)


if __name__ == "__main__":
    main()
