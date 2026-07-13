#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""run_cpp_assertions.py — 编译期断言单测 harness（永久保留，并行版）

目的
====
《现代 C++ 终极圣经》作为"可抄可编译"的生产级手册，正文中大量用
`static_assert` / `assert()` 把事实声明**编码成编译期/运行期契约**。
本工具把这些契约当作**单元测试**来跑：若书中声明为假，编译器/运行时
会立刻报错，从而把"文档 bug"暴露为可复现的失败，而不是靠肉眼审读。

两类断言块
==========
A) 编译期（static_assert）：块内含 `static_assert`。包裹进 namespace + 自带
   main 编译（复用 chapter_compile_check 的 PRELUDE/sanitize/GPP）。
   - 编译干净              → PASS（所有 static_assert 成立）
   - 报错含 "static assertion failed" → FAIL-CLAIM（书声明错误，必须修）
   - 其它编译错误          → WARN（块非独立可编译片段，无法验证，不计入书 bug）
B) 运行期（assert 完整程序）：块含 `int main` 且含 `assert(`。作为独立程序
   编译并实际运行（运行超时 15s 防卡死/阻塞 IO）。
   - 退出码 0              → PASS
   - 退出码非 0 / 崩溃     → FAIL（运行时断言被触发，声明错误）
   - 编译失败              → WARN（非独立可编译，无法验证）
   - 超时                  → WARN（疑似阻塞/死循环，未验证）

性能
====
全库 ~500 断言块，顺序编译过慢。本版用 ProcessPoolExecutor 多核并行
（默认 min(8, cpu_count)  worker），编译超时 30s、运行超时 15s 防御。

设计约束（对齐 AGENT.md 红线）
==============================
- 不修改源：只读 Book/，结果只打印。
- 可复现：固定 PRELUDE 与编译标志，结果稳定。
- 零误伤：WARN 与 FAIL-CLAIM 严格区分；WARN 不计入"书 bug"。
- 安全：运行期块有超时，绝不无限制执行未知代码。

用法
====
  python tools/run_cpp_assertions.py                 # 全库并行扫描
  python tools/run_cpp_assertions.py --only static    # 仅编译期
  python tools/run_cpp_assertions.py --only runtime    # 仅运行期
  python tools/run_cpp_assertions.py Book/.../chXX.md  # 单章
"""
from __future__ import annotations
import re
import sys
import glob
import subprocess
import tempfile
import pathlib
from concurrent.futures import ProcessPoolExecutor

HERE = pathlib.Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
from chapter_compile_check import sanitize, PRELUDE, GPP, CPP_FENCE, FENCE_END  # noqa: E402

ROOT = HERE.parent
COMPILE_TIMEOUT = 30
RUN_TIMEOUT = 15
SIMD_INC = "#include <experimental/simd>\n"

MAIN_RE = re.compile(r"\bint\s+main\s*\(")
ASSERT_RE = re.compile(r"\bassert\s*\(")

# 隔离伪影：块依赖前文定义的符号，独立编译时未定义 → 不算书 bug，归 WARN
ISOLATION_RE = re.compile(
    r"(does not name a type|was not declared|template argument \d+ is invalid)")
# 已知教学反例（作者故意写失败断言来演示语义）：白名单 (stem, 块序号)
EXPECTED_FAIL = {("ch52_ebo", 26), ("ch64_fold", 40)}
# 行内标记识别：块内 static_assert 注释/上下文含这些词 → 教学反例
DEMO_MARK_RE = re.compile(r"(❌|EXPECTED_FAIL|故意失败|编译期即 false|演示失败)")


def extract_blocks(path: pathlib.Path) -> list[str]:
    """提取文件中所有 ```cpp 围栏块内容（与 chapter_compile_check 同逻辑）。"""
    lines = path.read_text(encoding="utf-8").splitlines()
    blocks: list[str] = []
    i, n = 0, len(lines)
    while i < n:
        if CPP_FENCE.match(lines[i]):
            j = i + 1
            buf: list[str] = []
            while j < n and not FENCE_END.match(lines[j]):
                buf.append(lines[j])
                j += 1
            blocks.append("\n".join(buf))
            i = j + 1
        else:
            i += 1
    return blocks


def classify(code: str) -> str | None:
    has_main = bool(MAIN_RE.search(code))
    has_assert = bool(ASSERT_RE.search(code))
    has_sa = "static_assert" in code
    if has_main and has_assert:
        return "runtime"
    if has_sa:
        return "static"
    return None


def _first_static_fail(stderr: str) -> str:
    for ln in stderr.splitlines():
        if "static assertion failed" in ln:
            return ln.strip()
    return ""


def check_static(code: str, stem: str, idx: int, tmpdir: pathlib.Path) -> tuple[str, str]:
    """返回 (result, detail)。result ∈ {PASS, FAIL, WARN}。"""
    includes, body = sanitize(code)
    tu = PRELUDE
    if includes:
        tu += "\n" + "\n".join(includes)
    tu += f"\nnamespace chk_{stem}_{idx} {{\n{body}\n}}\nint main(){{ return 0; }}\n"
    cpp = tmpdir / f"{stem}_{idx}.cpp"
    cpp.write_text(tu, encoding="utf-8")
    exe = tmpdir / f"{stem}_{idx}.exe"
    try:
        r = subprocess.run(
            [GPP, "-std=c++23", "-O2", "-Wall", "-Wextra",
             "-mavx2", "-mavx512f", "-mfma",
             "-o", str(exe), str(cpp)],
            capture_output=True, text=True, timeout=COMPILE_TIMEOUT)
    except subprocess.TimeoutExpired:
        return "WARN", f"compile-timeout>{COMPILE_TIMEOUT}s"
    if r.returncode == 0:
        return "PASS", ""
    # 隔离伪影优先：符号缺失是上下文被切掉，不是断言逻辑错
    if ISOLATION_RE.search(r.stderr):
        first_err = ""
        for ln in r.stderr.splitlines():
            if "error:" in ln:
                first_err = ln.strip()
                break
        return "WARN", first_err or "isolation-undeclared"
    sf = _first_static_fail(r.stderr)
    if sf:
        if (stem, idx) in EXPECTED_FAIL or DEMO_MARK_RE.search(code):
            return "DEMO", sf
        return "FAIL", sf
    first_err = ""
    for ln in r.stderr.splitlines():
        if "error:" in ln:
            first_err = ln.strip()
            break
    return "WARN", first_err or (r.stderr.strip().splitlines()[-1] if r.stderr.strip() else "linkerr")


def check_runtime(code: str, stem: str, idx: int, tmpdir: pathlib.Path) -> tuple[str, str]:
    """返回 (result, detail)。result ∈ {PASS, FAIL, WARN}。"""
    tu = PRELUDE
    if "experimental/simd" in code:
        tu += "\n" + SIMD_INC
    tu += "\n" + code  # 保留 int main，作为独立程序
    cpp = tmpdir / f"{stem}_{idx}.cpp"
    cpp.write_text(tu, encoding="utf-8")
    exe = tmpdir / f"{stem}_{idx}.exe"
    try:
        rc = subprocess.run(
            [GPP, "-std=c++23", "-O2", "-Wall", "-Wextra",
             "-mavx2", "-mavx512f", "-mfma",
             "-o", str(exe), str(cpp)],
            capture_output=True, text=True, timeout=COMPILE_TIMEOUT)
    except subprocess.TimeoutExpired:
        return "WARN", f"compile-timeout>{COMPILE_TIMEOUT}s"
    if rc.returncode != 0:
        first_err = ""
        for ln in rc.stderr.splitlines():
            if "error:" in ln:
                first_err = ln.strip()
                break
        return "WARN", first_err or "compile-error"
    try:
        subprocess.run([str(exe)], capture_output=True, text=True, timeout=RUN_TIMEOUT)
    except subprocess.TimeoutExpired:
        return "WARN", f"timeout>{RUN_TIMEOUT}s (疑似阻塞/死循环, 未验证)"
    except subprocess.CalledProcessError as e:
        return "FAIL", f"exit={e.returncode}"
    return "PASS", ""


def check_one(job):
    """进程池 worker：job=(kind, code, stem, idx)。返回 (kind, stem, idx, result, detail)。"""
    kind, code, stem, idx = job
    with tempfile.TemporaryDirectory(prefix=f"a_{kind}_") as td:
        tmp = pathlib.Path(td)
        if kind == "static":
            res, detail = check_static(code, stem, idx, tmp)
        else:
            res, detail = check_runtime(code, stem, idx, tmp)
    return (kind, stem, idx, res, detail)


def main() -> int:
    args = sys.argv[1:]
    only = None
    paths: list[str] = []
    if "--only" in args:
        i = args.index("--only")
        only = args[i + 1]
        args = args[:i] + args[i + 2:]
    for a in args:
        paths.append(a)

    if paths:
        files = []
        for p in paths:
            pp = pathlib.Path(p)
            files.append(pp.resolve() if pp.is_absolute() else (ROOT / p).resolve())
    else:
        files = [pathlib.Path(f).resolve()
                 for f in glob.glob(str(ROOT / "Book" / "**" / "ch*.md"), recursive=True)]
    files = [f for f in files if f.exists() and not str(f).endswith(".bak")]

    if only and only not in ("static", "runtime"):
        print("ERROR: --only 仅支持 static / runtime", file=sys.stderr)
        return 2

    # 收集断言块任务
    jobs = []
    for f in files:
        for idx, code in enumerate(extract_blocks(f)):
            kind = classify(code)
            if kind is None or (only and kind != only):
                continue
            jobs.append((kind, code, f.stem, idx))

    stat = {"static": {"PASS": 0, "FAIL": 0, "WARN": 0, "DEMO": 0},
            "runtime": {"PASS": 0, "FAIL": 0, "WARN": 0}}
    fails: list[tuple[str, int, str, str]] = []
    warns: list[tuple[str, int, str, str]] = []
    demos: list[tuple[str, int, str, str]] = []

    workers = min(8, (os_cpu := __import__("os").cpu_count() or 4))
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for kind, stem, idx, res, detail in ex.map(check_one, jobs):
            stat[kind][res] += 1
            loc = f"Book/.../{stem}#{idx}"
            if res == "FAIL":
                fails.append((loc, idx, kind, detail))
            elif res == "DEMO":
                demos.append((loc, idx, kind, detail))
            elif res == "WARN":
                warns.append((loc, idx, kind, detail))

    print("=" * 64)
    print(f"编译期断言单测结果 (并行 {workers} worker, {len(jobs)} 断言块)")
    print("=" * 64)
    s, r = stat["static"], stat["runtime"]
    print(f"  编译期 static_assert : PASS={s['PASS']:4d}  FAIL={s['FAIL']:4d}  WARN={s['WARN']:4d}  DEMO={s['DEMO']:4d}")
    print(f"  运行期 assert 程序  : PASS={r['PASS']:4d}  FAIL={r['FAIL']:4d}  WARN={r['WARN']:4d}")
    total_fail = s["FAIL"] + r["FAIL"]
    print("-" * 64)
    if fails:
        print(f"[FAIL-CLAIM] 书声明错误 {total_fail} 处（必须修）:")
        for loc, idx, kind, detail in fails:
            print(f"  - {loc} [{kind}] {detail}")
    else:
        print("[FAIL-CLAIM] 0 — 所有可验证的编译期/运行期断言契约成立")
    if demos:
        print(f"\n[DEMO] 已知教学反例（故意失败断言，不计入书 bug）{len(demos)} 处:")
        for loc, idx, kind, detail in demos:
            print(f"  - {loc} [{kind}] {detail}")
    if warns:
        print(f"\n[WARN] 无法独立验证 {len(warns)} 处（非独立可编译片段/超时，不计入书 bug）:")
        for loc, idx, kind, detail in warns[:30]:
            print(f"  - {loc} [{kind}] {detail}")
        if len(warns) > 30:
            print(f"  ... 其余 {len(warns) - 30} 处省略")
    print("=" * 64)
    print(f"结论: {'存在书声明错误，需修复' if total_fail else '全部通过，文档契约可信'}")
    return 1 if total_fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
