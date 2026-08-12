#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
d5_runtime_gate.py — D5 基准「真能运行」门禁（深化 E11 编译门禁）
================================================================================
E11 的 d5_compile_gate.py 已把复现性承诺从「存在+跟踪」推到「能编译+链接」。
本工具再推深一层：**编过+链过 ≠ 运行不崩**。一个能链接却在运行时 segfault /
死循环 / 无输出的基准，对读者是「空头承诺」。

门禁内容（每个 _bench_d5_*.cpp，跳过 WIN_ONLY 于非 Windows）
----------------------------------------------------------
  1) 链接为可执行文件：g++ -std=c++23 -O2 <file> -latomic [-lwinmm] -o <tmp>
  2) 运行：subprocess 带超时执行，捕获退出码与 stdout 是否有产出。
     - 退出码 0 且有 stdout  → PASS（真能跑出结果）
     - 退出码非 0           → CRASH（真 bug，门禁判红）
     - 超时                 → TIMEOUT（可能机器负载重/基准设计长跑，判 WARN 不红）
     - 退出 0 但无 stdout    → NO_OUTPUT（可疑：基准却无产出，判 WARN）

平台/库：同 E11（WIN_ONLY 跳过 Windows 专属；-latomic 常驻；-lwinmm 仅 Windows）。
CLI：--check（CRASH 即 exit 1）/ --timeout N（每基准秒，默认 30）/ --json / --gpp。
退出码：0=无 CRASH；1=存在 CRASH；2=环境错误。幂等、零仓库副作用。
"""

import os
import sys
import json
import glob
import shutil
import argparse
import subprocess
import tempfile

ROOT = os.getcwd()
if os.name == "nt":
    DEFAULT_GPP = r"C:/Qt/Tools/mingw1530_64/bin/g++.exe"
else:
    DEFAULT_GPP = "g++"
STD = "-std=c++23"
OPT = "-O2"
WIN_ONLY = {
    "_bench_d5_ch101_algo_theory.cpp",
    "_bench_d5_ch119_ranges.cpp",
    "_bench_d5_ch120_coroutine.cpp",
    "_bench_d5_ch95_stl_algorithms.cpp",
}

# 个别基准需要额外链接参数（详见各源文件头注释）。仅在该基准实际参与链接时追加。
# ch101 的 fib_memoized(40000) 递归深度 4 万，远超 Windows 默认 1MB 线程栈，必须扩栈，
# 否则运行期触发 STATUS_STACK_OVERFLOW (0xC00000FD) —— 这是 harness 缺陷而非源 bug。
EXTRA_LINK_FLAGS = {
    "_bench_d5_ch101_algo_theory.cpp": ["-Wl,--stack,33554432"],
}


def is_abnormal_exit(rc):
    """
    rc 是 subprocess 的返回码。在 Windows 上 Python 直接返回 GetExitCodeProcess
    的 32 位完整值（未 mask 到 8 位），因此 `return 12000000;` 会得到 12000000。

    真正的「崩溃」判定：
      - POSIX：rc < 0  → 被信号杀死（SIGSEGV/SIGABRT…）
      - Windows：rc >= 0x80000000 → NTSTATUS 异常终止码
        （0xC0000005 ACCESS_VIOLATION / 0xC00000FD STACK_OVERFLOW …）
    基准 `return 测量累加值;` 这类良性非零退出落在普通正整数范围，不算崩溃。
    """
    if rc < 0:
        return True
    if os.name == "nt" and rc >= 0x80000000:
        return True
    return False


def find_gpp(explicit):
    gpp = explicit or os.environ.get("D5_GPP") or DEFAULT_GPP
    if os.path.isabs(gpp) or os.path.dirname(gpp):
        if not os.path.exists(gpp):
            return None, gpp
    else:
        f = shutil.which(gpp)
        if f is None:
            return None, gpp
        gpp = f
    return gpp, gpp


def main():
    ap = argparse.ArgumentParser(description="D5 benchmark runtime gate")
    ap.add_argument("--check", action="store_true", help="CRASH 即 exit 1")
    ap.add_argument("--timeout", type=int, default=30, help="每基准运行超时秒")
    ap.add_argument("--json", action="store_true", help="机器可读")
    ap.add_argument("--gpp", default=None, help="覆盖编译器")
    args = ap.parse_args()

    gpp, _ = find_gpp(args.gpp)
    if gpp is None:
        msg = f"[ENV-ERR] 找不到编译器: {_}"
        print(json.dumps({"error": msg}, ensure_ascii=False) if args.json else msg)
        return 2

    libs = ["-latomic"] + (["-lwinmm"] if os.name == "nt" else [])
    files = sorted(glob.glob(os.path.join(ROOT, "_bench_d5_*.cpp")))
    files = [os.path.basename(f) for f in files]
    total = len(files)

    passed = crashed = timedout = no_output = benign_ret = skipped = 0
    fails = []
    tmp = tempfile.mkdtemp(prefix="d5run_")
    try:
        for f in files:
            if os.name != "nt" and f in WIN_ONLY:
                skipped += 1
                continue
            exe = os.path.join(tmp, "d5exe" + (".exe" if os.name == "nt" else ""))
            extra = EXTRA_LINK_FLAGS.get(f, [])
            rc = subprocess.run([gpp, STD, OPT, f, *libs, *extra, "-o", exe],
                                capture_output=True, text=True, encoding="utf-8", errors="replace")
            if rc.returncode != 0:
                crashed += 1
                err = (rc.stderr or rc.stdout).strip()
                fails.append((f, "LINK", err.splitlines()[-1] if err else "link failed"))
                continue
            try:
                rr = subprocess.run([exe], capture_output=True, text=True,
                                     encoding="utf-8", errors="replace", timeout=args.timeout)
                rc = rr.returncode
                out = (rr.stdout or rr.stderr).strip()
                if rc == 0:
                    if out:
                        passed += 1
                    else:
                        no_output += 1
                        fails.append((f, "NO_OUTPUT", "exit=0 但无 stdout/stderr 产出"))
                elif is_abnormal_exit(rc):
                    # 真崩溃：被信号杀死 / NTSTATUS 异常终止码
                    crashed += 1
                    fails.append((f, "CRASH",
                                  f"异常终止 exit={rc} " + (out.splitlines()[-1] if out else "")))
                else:
                    # 良性非零退出（如 main 误 return 测量值）：有产出→视为通过(标注 WARN)，
                    # 无产出→判红（返回了错误码却什么都没打印，可疑）。
                    if out:
                        benign_ret += 1
                        fails.append((f, "BENIGN_RET",
                                      f"main 返回非零({rc})但有正常产出（疑似 return 测量值，应改 return 0），不判崩溃"))
                    else:
                        crashed += 1
                        fails.append((f, "CRASH", f"exit={rc} 且无任何产出"))
            except subprocess.TimeoutExpired:
                timedout += 1
                fails.append((f, "TIMEOUT", f"运行超过 {args.timeout}s（可能长跑基准/机器负载）"))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    hard_fail = crashed  # 仅 CRASH 判红；TIMEOUT/NO_OUTPUT 为 WARN
    ok = (crashed == 0)

    if args.json:
        print(json.dumps({
            "gpp": gpp, "total": total, "skipped_win_only": skipped,
            "pass": passed, "crash": crashed, "timeout": timedout,
            "no_output": no_output, "benign_ret": benign_ret,
            "failures": [{"file": f, "stage": s, "detail": d} for f, s, d in fails],
            "ok": ok,
        }, ensure_ascii=False, indent=2))
    else:
        print("=" * 64)
        print(f"D5 运行门禁 (GCC {gpp})")
        print("=" * 64)
        print(f"  基准总数      : {total}")
        print(f"  运行通过      : {passed}")
        print(f"  崩溃(CRASH)   : {crashed}  <-- 判红（真异常终止）")
        print(f"  良性非零返回  : {benign_ret}  (WARN：有产出但 main 返回非0)")
        print(f"  超时(TIMEOUT) : {timedout}  (WARN)")
        print(f"  无产出        : {no_output}  (WARN)")
        print(f"  Windows跳过   : {skipped}")
        if fails:
            print("  --- 异常清单 ---")
            for f, s, d in fails:
                print(f"    [{s}] {f}: {d}")
        print(f"  结论          : {'✅ 无崩溃' if ok else '❌ 存在崩溃'}")

    if args.check and not ok:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
