#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
d5_compile_gate.py — D5 性能附录「基准源码真能编译」门禁
（确定性、幂等、可接入 CI；深化 E9 的引用完整性门禁）

背景
----
本书 §D5 性能附录承诺「可复现 demo 的基准源码见库根 `_bench_d5_X.cpp`」。
E9 的 `d5_source_integrity.py` 已把承诺从「口头声明」升级为「文件存在且被
git 跟踪」。本工具把同一条承诺再推深一层：

    「文件存在 + 被跟踪」  ──►  「文件在 GCC 15.3.0 -std=c++23 下真能编译并链接」

即复现性承诺的最硬一档：读者抄走的基准源码，至少能在现代标准 + 优化下编过。

门禁内容（每个 `_bench_d5_*.cpp`）
--------------------------------
  1) 编译（translation-unit 正确性，主导检查）：
       g++ -std=c++23 -O2 -Wall -Wextra -c <file> -o /dev/null
  2) 链接（可执行性，佐证「能跑」）：
       g++ -std=c++23 -O2 <file> -latomic [-lwinmm] -o <tmp>
  部分基准需要平台/标准库：
     - 128-bit std::atomic 需要 -latomic（全平台，已在链接命令常驻）。
     - Win32 高精度计时 timeBeginPeriod/timeEndPeriod 需要 -lwinmm（仅 Windows）。

平台感知
--------
  仓库的基准在作者本机 MinGW GCC 15.3.0 (Windows) 上实测通过。其中 4 个文件
  直接使用 <windows.h>（WIN_ONLY），在 Linux 等非 Windows runner 上无法编译。
  为保持 CI 可移植，本工具在非 Windows 环境下自动跳过 WIN_ONLY 文件（仅跳过，
  不计入失败），其余文件在 Linux gcc 下同样编过（已用 ubuntu gcc 验证子集）。

CLI
---
  python3 tools/d5_compile_gate.py            # 报告模式（默认，exit 0）
  python3 tools/d5_compile_gate.py --check    # 门禁：任一应过文件失败则 exit 1
  python3 tools/d5_compile_gate.py --no-link  # 仅编译检查，跳过链接
  python3 tools/d5_compile_gate.py --json     # 机器可读报告
  python3 tools/d5_compile_gate.py --gpp PATH # 覆盖编译器（默认见下）

退出码：0 = 全部应过文件通过；1 = 存在失败；2 = 环境/配置错误（如找不到 g++）。
幂等：重复运行不改变仓库任何文件，结果稳定。
"""

import os
import sys
import glob
import json
import shutil
import argparse
import subprocess
import tempfile

ROOT = os.getcwd()

# 默认编译器：Windows 上锁定作者实测的 MinGW GCC 15.3.0（PATH 的 g++ 可能是旧版 13.1.0）；
# 非 Windows 用系统 g++（GitHub ubuntu runner 自带，覆盖非 WIN_ONLY 子集）。
if os.name == "nt":
    DEFAULT_GPP = r"C:/Qt/Tools/mingw1530_64/bin/g++.exe"
else:
    DEFAULT_GPP = "g++"

STD = "-std=c++23"
OPT = "-O2"
WARN = ["-Wall", "-Wextra"]

# 直接使用 <windows.h> / Win32 API 的基准，非 Windows runner 跳过（无法编译）。
WIN_ONLY = {
    "_bench_d5_ch101_algo_theory.cpp",
    "_bench_d5_ch119_ranges.cpp",
    "_bench_d5_ch120_coroutine.cpp",
    "_bench_d5_ch95_stl_algorithms.cpp",
}


def find_gpp(explicit):
    gpp = explicit or os.environ.get("D5_GPP") or DEFAULT_GPP
    # 解析可执行文件是否存在（Windows 补 .exe 已在路径中含）
    if os.path.isabs(gpp) or os.path.dirname(gpp):
        if not os.path.exists(gpp):
            return None, gpp
    else:
        # PATH 查找
        found = shutil.which(gpp)
        if found is None:
            return None, gpp
        gpp = found
    # 确认能运行并返回版本
    try:
        out = subprocess.run([gpp, "--version"], capture_output=True, text=True, timeout=30)
        ver = out.stdout.splitlines()[0] if out.stdout else "(unknown)"
    except Exception as e:  # noqa
        return None, gpp
    return gpp, ver


def compile_one(gpp, f):
    """返回 (ok, last_line)。编译到对象文件，不链接。"""
    cmd = [gpp, STD, OPT, *WARN, "-c", f, "-o", os.devnull]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode == 0:
        return True, ""
    err = (r.stderr or r.stdout).strip()
    return False, (err.splitlines()[-1] if err else "no stderr / no output")


def link_one(gpp, f, libs, tmpdir):
    """返回 (ok, last_line)。完整链接为可执行文件，验证可运行性。"""
    exe = os.path.join(tmpdir, "d5gate_out" + (".exe" if os.name == "nt" else ""))
    cmd = [gpp, STD, OPT, f, *libs, "-o", exe]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode == 0:
        return True, ""
    err = (r.stderr or r.stdout).strip()
    return False, (err.splitlines()[-1] if err else "no stderr / no output")


def main():
    ap = argparse.ArgumentParser(description="D5 benchmark compile/link gate")
    ap.add_argument("--check", action="store_true", help="门禁模式：任一应过文件失败则 exit 1")
    ap.add_argument("--no-link", action="store_true", help="仅编译检查，跳过链接")
    ap.add_argument("--json", action="store_true", help="输出机器可读 JSON")
    ap.add_argument("--gpp", default=None, help="覆盖编译器路径")
    args = ap.parse_args()

    gpp, ver = find_gpp(args.gpp)
    if gpp is None:
        msg = f"[ENV-ERR] 找不到编译器: {ver}（可用 --gpp 或环境变量 D5_GPP 指定 GCC 15.3.0+）"
        if args.json:
            print(json.dumps({"error": msg, "ok": False}, ensure_ascii=False))
        else:
            print(msg)
        return 2

    libs = ["-latomic"] + (["-lwinmm"] if os.name == "nt" else [])
    files = sorted(glob.glob(os.path.join(ROOT, "_bench_d5_*.cpp")))
    files = [os.path.basename(f) for f in files]
    total = len(files)

    compile_ok = compile_fail = link_ok = link_fail = skipped = 0
    failures = []  # (file, stage, last_line)
    tmpdir = tempfile.mkdtemp(prefix="d5gate_")
    try:
        for f in files:
            if os.name != "nt" and f in WIN_ONLY:
                skipped += 1
                continue
            ok, line = compile_one(gpp, f)
            if not ok:
                compile_fail += 1
                failures.append((f, "COMPILE", line))
                continue
            compile_ok += 1
            if args.no_link:
                link_ok += 1
                continue
            lok, lline = link_one(gpp, f, libs, tmpdir)
            if lok:
                link_ok += 1
            else:
                link_fail += 1
                failures.append((f, "LINK", lline))
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

    # 失败判定：编译失败必算失败；链接失败在 --no-link 下不算。
    hard_fail = compile_fail + (0 if args.no_link else link_fail)
    passed = (compile_ok == (total - skipped)) and (args.no_link or link_fail == 0)

    if args.json:
        print(json.dumps({
            "gpp": gpp, "gpp_version": ver,
            "total": total, "skipped_win_only": skipped,
            "compile_ok": compile_ok, "compile_fail": compile_fail,
            "link_ok": link_ok, "link_fail": link_fail,
            "failures": [{"file": f, "stage": s, "detail": d} for f, s, d in failures],
            "ok": passed,
        }, ensure_ascii=False, indent=2))
    else:
        print("=" * 64)
        print(f"D5 编译门禁 (GCC {ver})")
        print("=" * 64)
        print(f"  编译器        : {gpp}")
        print(f"  标准/优化     : {STD} {OPT} {' '.join(WARN)}  (链接 +{', '.join(libs)})")
        print(f"  基准总数      : {total}")
        print(f"  编译通过      : {compile_ok}")
        print(f"  编译失败      : {compile_fail}")
        print(f"  链接通过      : {link_ok}")
        print(f"  链接失败      : {link_fail}")
        print(f"  Windows跳过   : {skipped} (非 Windows runner 跳过 WIN_ONLY)")
        if failures:
            print("  --- 失败清单 ---")
            for f, s, d in failures:
                print(f"    [{s}] {f}: {d}")
        print(f"  结论          : {'✅ 全部通过' if passed else '❌ 存在失败'}")

    if args.check and not passed:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
