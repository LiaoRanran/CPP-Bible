#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""d5_asm_evidence.py — D5 附录汇编实证生成器（工具型，不直接改源）

《现代 C++ 终极圣经》的 D5 性能附录目前只有四段基准结构（基准结果 / 非显然结论 /
可复现 demo / 方法学注），附录本身不含机器码证据。本工具为「D5 汇编证据附录加厚」
提供可复现的素材：

  - 读取某章 D5 引用的 `_bench_d5_*.cpp`（真实存在、git 跟踪的基准源）
  - 用 MinGW GCC 15.3.0 `-S -masm=intel -O2 -std=c++23` 重新编译，提取用户函数
    的 Intel 语法 disassembly（与 Examples/*.asm 同一工具链、同一调用约定）
  - 输出可直接粘贴进 D5 附录的「### D5.5 汇编实证」候选小节

用法
====
  # 列出某 bench 全部用户函数（挑出热函数名）
  python tools/d5_asm_evidence.py --bench _bench_d5_ch20_passval.cpp --list

  # 提取指定热函数 disassembly（用于 D5.5 实证）
  python tools/d5_asm_evidence.py --bench _bench_d5_ch20_passval.cpp \
        --funcs by_value,by_cref

  # 直接从章节提取其 bench 引用并列出函数
  python tools/d5_asm_evidence.py --chapter Book/part03_language/ch20_reference_pointer.md --list

所有产物都是 GCC 15.3.0 真实生成的机器码，非手写编造；与 asm_prepush_guard 的
证据库同源（MinGW SEH），可在本地复现。
"""
import os
import re
import sys
import subprocess
import argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
GPP_CANON = r"C:/Qt/Tools/mingw1530_64/bin/g++.exe"

SKIP = ('.p2align', '.globl', '.def', '.set', '.type', '.size', '.section',
        '.ident', '.file', '.comm', '.local', '.align', '.balign')


def find_gpp():
    if os.path.isfile(GPP_CANON):
        return GPP_CANON
    from shutil import which
    return which("g++")


def parse_gpp_s(t):
    """归一化解析：仅代码段、仅外部函数符号作用域。

    关键修正：GCC 在 -O2 下会把函数体拆进 `.text.hot`/`.text.unlikely` 等子段，
    并插入大量内部标号（`.L4`/`.LFB21`/`.LCOLDB`/`.LHOTB`/`.seh_*`/`.cfi_*`）。
    - 任何 `.text*` 子段都视为代码段；
    - 以 `.` 开头的标号/指令（内部标号、所有 .directive）一律跳过，不重置 cur；
    - 只把「无前导点」的外部符号（C++ mangled `_Z..`、C `_name`）当作函数边界。
    """
    syms, cur, in_code = {}, None, False
    for line in t.splitlines():
        s = line.rstrip()
        if not s.strip():
            continue
        st = s.strip()
        msec = re.match(r'^\s*\.section\s+(\.\S+)', s)
        if msec:
            in_code = msec.group(1).startswith('.text')
            if not in_code:
                cur = None
            continue
        if re.match(r'^\s*\.text\b', s):
            in_code = True
            continue
        if not in_code:
            continue
        # 所有 .directive（.globl/.def/.type/.size/.p2align/.seh_/.cfi_...）跳过
        if st.startswith('.'):
            continue
        mlbl = re.match(r'^([A-Za-z_][\w$.]*):', st)
        if mlbl:
            label = mlbl.group(1)
            if label.startswith('.'):   # 内部标号 .L/.LFB/.LC... 忽略
                continue
            cur = label
            syms.setdefault(cur, [])
            continue
        s2 = re.sub(r'#.*$', '', st)
        s2 = re.sub(r'\.L([A-Za-z]*)\d+', r'.L\1', s2).strip()
        if not s2:
            continue
        if cur is not None:
            syms[cur].append(s2)
    return syms


def extract_bench_asm(bench: Path, flags):
    """编译 bench 并提取用户函数 disassembly。返回 (syms_dict, error)。"""
    gpp = find_gpp()
    if not gpp:
        return None, "找不到 g++"
    tmp = bench.with_suffix(".d5.s")
    cmd = [gpp] + flags.split() + ["-S", "-masm=intel", str(bench), "-o", str(tmp)]
    p = subprocess.run(cmd, capture_output=True, text=True)
    if p.returncode != 0:
        if tmp.exists():
            tmp.unlink()
        return None, p.stderr.strip().splitlines()[0][:160]
    syms = parse_gpp_s(tmp.read_text(encoding="utf-8", errors="replace"))
    if tmp.exists():
        tmp.unlink()
    return syms, None


def find_bench_in_chapter(ch_path: Path):
    text = ch_path.read_text(encoding="utf-8")
    return sorted(set(re.findall(r'_bench_d5_[A-Za-z0-9_]+\.cpp', text)))


def match_funcs(syms, funcs):
    """funcs 为可读名/子串集合；返回 mangled 符号中匹配的子集。"""
    if not funcs:
        return set(syms)
    out = set()
    for name in syms:
        if name == "main":
            continue
        if any(f and (f == name or f in name) for f in funcs):
            out.add(name)
    return out


def dump_funcs(syms):
    print(f"  [用户函数 {len(syms)} 个] (挑出热函数用于 D5.5)")
    for name in sorted(syms):
        if name == "main":
            continue
        print(f"    {name}  ({len(syms[name])} insns)")


def dump_asm(syms, funcs):
    sel = match_funcs(syms, funcs)
    if not sel:
        print("  [!] 未匹配到函数；可用名见 --list")
        return
    for name in sorted(syms):
        if name not in sel:
            continue
        lines = syms[name]
        print(f"\n; ===== {name}()  —  GCC 15.3.0 -O2 -masm=intel "
              f"({len(lines)} 条指令) =====")
        for ln in lines:
            print("  " + ln)


def main():
    ap = argparse.ArgumentParser(description="D5 汇编实证生成器")
    ap.add_argument("--bench", default=None, help="基准源 _bench_d5_*.cpp")
    ap.add_argument("--chapter", default=None, help="章节 md（自动提取其 bench 引用）")
    ap.add_argument("--flags", default="-std=c++23 -O2",
                    help="编译标志（默认 -std=c++23 -O2）")
    ap.add_argument("--funcs", default=None,
                    help="仅提取这些函数（逗号分隔）；省略=列出全部（跳过 main）")
    ap.add_argument("--list", action="store_true", help="仅列出函数名")
    args = ap.parse_args()

    bench_name = args.bench
    if not bench_name and args.chapter:
        ch = Path(args.chapter)
        if not ch.is_absolute():
            ch = ROOT / ch
        found = find_bench_in_chapter(ch)
        if not found:
            print(f"[ERR] {args.chapter} 未引用任何 _bench_d5_*.cpp")
            return 1
        bench_name = found[0]
        print(f"[*] {args.chapter} -> bench: {bench_name}")

    if not bench_name:
        print("[ERR] 需 --bench 或 --chapter")
        return 1

    bench = Path(bench_name)
    if not bench.is_absolute():
        bench = ROOT / bench
    if not bench.exists():
        print(f"[ERR] bench 不存在: {bench}")
        return 1

    syms, err = extract_bench_asm(bench, args.flags)
    if err:
        print(f"[COMPILE FAIL] {bench_name}: {err}")
        return 1

    funcs = set(f for f in (args.funcs or "").split(",") if f) or None
    if args.list or not funcs:
        dump_funcs(syms)
    else:
        dump_asm(syms, funcs)
    return 0


if __name__ == "__main__":
    sys.exit(main())
