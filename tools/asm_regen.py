#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
asm_regen.py — Examples/*.asm 版本统一再生驱动器（13.1.0 -> 15.3.0）。

《现代 C++ 终极圣经》证据库 Examples/*.asm 现状：13.1.0×207 / 15.3.0×42 / unmarked×9。
本工具把「可重编的陈旧 13.1.0 证据」用本地 MinGW GCC 15.3.0 按可推断约定重新编译，
就地替换为 15.3.0 产物，使证据库版本一致（红线要求：有源必须真实重生，无源诚实标注）。

安全护栏（绝不制造伪证据 / 绝不丢失用户符号）：
  1. 仅替换「重编成功」且「重编后用户级被定义函数符号集合 ⊇ 原存储」的文件；
     若重编丢掉了源里曾有的用户函数（如源码演进后函数改名），SKIP 并报 LOST_SYMBOLS，
     绝不静默替换成缺符号的产物。
  2. 保留原文件行尾（CRLF/LF）以消除伪 diff。
  3. 不触碰：无源文件（NO_SOURCE/unmarked）、modules 编译失败（COMPILE_FAIL）、已是 15.3.0。

为什么是本地门禁而非 CI ubuntu：证据库是 MinGW 生成（.seh_proc/.def/__main），
ubuntu gcc-15（CFI/AT&T）无法复现，故再生也在 Windows+MinGW 下进行，预推送自检。

用法:
  python tools/asm_regen.py --gpp <g++.exe> --examples Examples --dry-run
  python tools/asm_regen.py --gpp <g++.exe> --examples Examples --apply [--batch 30]
"""
import os
import re
import subprocess
import json
import glob
import argparse
from collections import Counter


def flags_for(name):
    """文件级编译标志推断（与 asm_repro_spotcheck.flags_for 同步）。
    ch47 vtable 特例：-O1 -fno-inline（书 D4.3 显记），否则 -O2 会内联
    析构函数导致 vtable 符号消失，误判 DRIFT/LOST_SYMBOL。"""
    low = name.lower()
    base = ["-std=c++23", "-O2"]
    if "_o0" in low or low.endswith("o0"):
        base = ["-std=c++23", "-O0"]
    elif "_o1" in low:
        base = ["-std=c++23", "-O1"]
    elif "_os" in low:
        base = ["-std=c++23", "-Os"]
    if "ch14" in low:
        base = ["-std=c++23", "-g", "-O0"]
    if "_ch47_d4_vtable" in low:
        base = ["-std=c++23", "-O1", "-fno-inline"]
    return base


def detect_format(stored):
    if "file format" in stored or "Disassembly of section" in stored:
        return "OBJDUMP"
    if re.search(r'^\s*\.(text|globl|p2align|seh_|file)\b', stored, re.M):
        return "GPP_S"
    return "OTHER"


def detect_version(stored):
    m = re.search(r'GCC:.*?(\d+\.\d+\.\d+)', stored)
    return m.group(1) if m else "UNMARKED"


def seh_procs(text):
    return re.findall(r'^\s*\.seh_proc\s+(\S+)', text, re.M)


def is_user_sym(raw):
    # 用户级被定义函数：非编译器/库内部前缀、非 std、非 stdio、非编译器生成子符号
    if raw.startswith("__"):
        return False
    if raw.startswith("_Z") and re.match(r'_Z(?:St|NS|NSt|NV?St|NK?St|NVK?St)', raw):
        return False
    # C 标准库函数（printf/snprintf/...）的内部链接克隆（_ZL6printfPKcz 等）
    if re.search(r'(printf|snprintf|fprintf|scanf|sprintf|puts|putchar|memcpy|'
                 r'memmove|memset|strlen|strcmp|strcpy)', raw):
        return False
    if re.search(r'\.(part|constprop|isra|cold|clone|localalias)\.', raw):
        return False
    # 编译器生成的子符号（协程帧、内联助手等）版本不稳定，不算顶层用户函数
    if re.search(r'\.(Frame\.[a-zA-Z]+|\.actor|\.destroy|\.resume|\.promise|'
                 r'\.handle|\.cleanup|\.__destroy|\.__resume)', raw):
        return False
    if raw.startswith("_Z") and "Frame" in raw:
        return False
    return True


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gpp", required=True)
    ap.add_argument("--examples", required=True)
    ap.add_argument("--only", default="13.1.0", help="仅处理该版本 (默认 13.1.0)")
    ap.add_argument("--dry-run", action="store_true", help="只报告不写盘")
    ap.add_argument("--apply", action="store_true", help="实际替换")
    ap.add_argument("--force", action="store_true",
                    help="忽略 LOST_SYMBOL 跳过（版本一致化优先；随后由 verify_asm_evidence 兜底）")
    ap.add_argument("--batch", type=int, default=0, help="分批大小(0=全部)")
    ap.add_argument("--names", default="", help="仅处理逗号分隔的文件名(不含.asm)，如 _ch13_use,_ch113_co_O2")
    a = ap.parse_args()
    if not a.dry_run and not a.apply:
        a.dry_run = True
    GPP, EX = a.gpp, a.examples
    NAME_SET = {n.strip() for n in a.names.split(",") if n.strip()} if a.names else None

    results = []
    for asm in sorted(glob.glob(os.path.join(EX, "*.asm"))):
        name = os.path.splitext(os.path.basename(asm))[0]
        if NAME_SET and name not in NAME_SET:
            continue
        stored = open(asm, encoding="utf-8", errors="replace").read()
        ver = detect_version(stored)
        if a.only != "all" and ver != a.only:
            continue
        mfile = re.search(r'^\s*\.file\s+"([^"]+)"', stored, re.M)
        if not mfile:
            results.append({"name": name, "ver": ver, "action": "SKIP_NO_SOURCE"})
            continue
        src = os.path.join(EX, mfile.group(1))
        if not os.path.exists(src):
            results.append({"name": name, "ver": ver, "action": "SKIP_NO_SOURCE"})
            continue
        fmt = detect_format(stored)
        if fmt != "GPP_S":
            results.append({"name": name, "ver": ver, "action": "SKIP_FORMAT"})
            continue
        flags = flags_for(name)
        tmp = os.path.join(EX, "_regen_" + name + ".s")
        p = subprocess.run([GPP] + flags + ["-S", "-masm=intel", src, "-o", tmp],
                           capture_output=True, text=True)
        if p.returncode != 0:
            results.append({"name": name, "ver": ver, "action": "SKIP_COMPILE_FAIL",
                            "detail": (p.stderr.strip().splitlines() or ["?"])[0][:120]})
            if os.path.exists(tmp):
                os.remove(tmp)
            continue
        fresh = open(tmp, encoding="utf-8", errors="replace").read()
        os.remove(tmp)
        orig_procs = seh_procs(stored)
        new_procs = seh_procs(fresh)
        orig_user = {s for s in orig_procs if is_user_sym(s)}
        new_user = {s for s in new_procs if is_user_sym(s)}
        lost = orig_user - new_user
        if lost and not a.force:
            results.append({"name": name, "ver": ver, "action": "SKIP_LOST_SYMBOL",
                            "lost": sorted(lost)[:5]})
            continue
        # 安全：保留原 EOL
        orig_eol = "\r\n" if "\r\n" in stored else "\n"
        forced = bool(lost)
        if a.apply:
            # g++ 产物可能 LF；按原 EOL 重写以消伪 diff
            fresh_eol = "\r\n" if "\r\n" in fresh else "\n"
            if fresh_eol != orig_eol:
                fresh = fresh.replace(fresh_eol, orig_eol)
            open(asm, "w", encoding="utf-8", newline="").write(fresh)
            results.append({"name": name, "ver": ver, "action": "REPLACED",
                            "newver": detect_version(fresh),
                            "forced_lost": sorted(lost)[:5] if forced else None})
        else:
            results.append({"name": name, "ver": ver, "action": "WOULD_REPLACE",
                            "newver": detect_version(fresh),
                            "forced_lost": sorted(lost)[:5] if forced else None})

    cnt = Counter(r["action"] for r in results)
    n_forced = sum(1 for r in results if r["action"] in ("REPLACED", "WOULD_REPLACE")
                   and r.get("forced_lost"))
    print(f"[only={a.only}] scanned={len(results)}  (其中 forced_lost={n_forced})")
    for k in ["REPLACED", "WOULD_REPLACE", "SKIP_LOST_SYMBOL",
              "SKIP_COMPILE_FAIL", "SKIP_NO_SOURCE", "SKIP_FORMAT"]:
        if cnt[k]:
            print(f"  {k:18s}: {cnt[k]}")
    out = os.path.join(EX, "_regen_report.json")
    json.dump({"summary": dict(cnt), "results": results},
              open(out, "w", encoding="utf-8", newline="\n"), ensure_ascii=False, indent=2)
    print(f"-> {out}")
    if a.batch:
        print(f"(batch limit {a.batch} not yet applied across multiple runs)")


if __name__ == "__main__":
    main()
