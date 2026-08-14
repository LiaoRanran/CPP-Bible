#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""cppbible.py — 《现代 C++ 终极圣经》统一工具链 CLI

设计原则
========
- 只包装、不替代现有 tools/ 脚本，确保现有 CI/本地工作流零破坏。
- 自动处理 Windows Git Bash POSIX 路径（/c/...）与 Windows 原生 Python 路径问题。
- 所有子命令返回标准退出码：0 = 成功，非 0 = 失败。

用法
====
    python tools/cppbible.py check                 # 本地秒级质量门禁
    python tools/cppbible.py check --stage quality # 等价 CI quality job
    python tools/cppbible.py build site            # 构建静态站点
    python tools/cppbible.py clean                 # 清理构建副产物
    python tools/cppbible.py install-hooks         # 安装 git pre-push hook
    python tools/cppbible.py --version             # 显示工具链版本
"""
from __future__ import annotations

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Iterable, Sequence


# ---------------------------------------------------------------------------
# 路径与配置发现
# ---------------------------------------------------------------------------

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent


def _win_path_from_posix(path: str | Path) -> str:
    """Git Bash /c/... -> C:/...，供 Windows 原生 Python/EXE 使用。"""
    p = Path(path).as_posix()
    if sys.platform == "win32" and len(p) >= 3 and p.startswith("/") and p[2] == "/":
        # /c/foo -> C:/foo
        drive = p[1].upper()
        p = f"{drive}:{p[2:]}"
    return p


def find_managed_python() -> str:
    """优先使用项目记忆中的 managed Python，否则回退 sys.executable。"""
    managed = ROOT / ".workbuddy" / "managed_python.txt"
    if managed.exists():
        exe = managed.read_text(encoding="utf-8").strip()
        if Path(exe).exists():
            return exe
    candidates = [
        Path("C:/Users/ASUS/.workbuddy/binaries/python/versions/3.13.12/python.exe"),
        Path("C:/Users/ASUS/.workbuddy/binaries/python/versions/3.13.12/python.exe"),
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return sys.executable


def find_gcc() -> str:
    """优先返回 Windows 本机 mingw1530 g++。"""
    candidates = [
        Path("C:/Qt/Tools/mingw1530_64/bin/g++.exe"),
        Path("C:/Qt/Tools/mingw1310_64/bin/g++.exe"),
    ]
    for c in candidates:
        if c.exists():
            return str(c)
    return "g++"


PYTHON_EXE = find_managed_python()
GCC_EXE = find_gcc()


# ---------------------------------------------------------------------------
# 底层执行 helpers
# ---------------------------------------------------------------------------

def run(cmd: Sequence[str | Path], *, cwd: Path | None = None, check: bool = True, timeout: int | None = None) -> subprocess.CompletedProcess:
    """统一封装 subprocess.run，输出命令本身便于调试。"""
    cmd_str = [str(c) for c in cmd]
    print(f"  $ {' '.join(cmd_str)}", flush=True)
    return subprocess.run(cmd_str, cwd=cwd or ROOT, check=check, text=True, capture_output=True, timeout=timeout)


def run_python(script: str | Path, *args: str, check: bool = True) -> subprocess.CompletedProcess:
    """用本工具链的 Python 执行 tools/ 下的脚本。"""
    return run([PYTHON_EXE, str(script), *args], check=check)


# ---------------------------------------------------------------------------
# 子命令实现
# ---------------------------------------------------------------------------

def cmd_version(_args: argparse.Namespace) -> int:
    """显示工具链版本与关键路径。"""
    print("CPP-Bible Toolchain v1.0.0")
    print(f"  ROOT      : {ROOT}")
    print(f"  Python    : {PYTHON_EXE}")
    print(f"  GCC       : {GCC_EXE}")
    # 尝试获取 GCC 版本
    try:
        r = run([GCC_EXE, "--version"], check=False)
        first = r.stdout.splitlines()[0] if r.stdout else "unknown"
        print(f"  GCC ver   : {first}")
    except Exception as e:
        print(f"  GCC ver   : (无法调用: {e})")
    print(f"  Platform  : {sys.platform}")
    return 0


def cmd_check(args: argparse.Namespace) -> int:
    """运行质量门禁。"""
    stage = args.stage or "fast"
    print(f"\n[cppbible] running check --stage={stage}\n")

    if stage == "fast":
        gates = [
            ("Preflight", [PYTHON_EXE, "tools/preflight_check.py"]),
            ("Consistency", [PYTHON_EXE, "tools/consistency_check.py"]),
            ("Cross-Reference", [PYTHON_EXE, "tools/crossref_audit.py"]),
            ("Xref", [PYTHON_EXE, "tools/xref_check.py"]),
            ("Index Freshness", [PYTHON_EXE, "tools/gen_indexes.py", "--check"]),
            ("Density", [PYTHON_EXE, "tools/density_audit.py", "--check", "20"]),
            ("Whitespace", [PYTHON_EXE, "tools/whitespace_fix.py", "--check"]),
            ("Fence Sweep", [PYTHON_EXE, "tools/sweep_fences.py", "--check"]),
            ("Terminology", [PYTHON_EXE, "tools/terminology_normalize.py", "--check"]),
        ]
    elif stage == "quality":
        # 完整 quality job：调用 CI 中所有硬门禁（跳过咨询/软门禁）
        gates = [
            ("Preflight", [PYTHON_EXE, "tools/preflight_check.py"]),
            ("Consistency", [PYTHON_EXE, "tools/consistency_check.py"]),
            ("Cross-Reference", [PYTHON_EXE, "tools/crossref_audit.py"]),
            ("Xref", [PYTHON_EXE, "tools/xref_check.py"]),
            ("Index Freshness", [PYTHON_EXE, "tools/gen_indexes.py", "--check"]),
            ("Density", [PYTHON_EXE, "tools/density_audit.py", "--check", "20"]),
            ("D5 Appendix", [PYTHON_EXE, "tools/d5_appendix_audit.py"]),
            ("D5 Source Integrity", [PYTHON_EXE, "tools/d5_source_integrity.py", "--check"]),
            ("Terminology", [PYTHON_EXE, "tools/terminology_normalize.py", "--check"]),
            ("Exercise Dup", [PYTHON_EXE, "tools/exercise_dup_guard.py"]),
            ("ASM Evidence", [PYTHON_EXE, "tools/verify_asm_evidence.py", "--root", "Book", "--examples", "Examples"]),
            ("Book ASM Freshness", [PYTHON_EXE, "tools/book_asm_freshness.py"]),
            ("Structure", [PYTHON_EXE, "tools/structure_audit.py", "--check"]),
            ("Fence Sweep", [PYTHON_EXE, "tools/sweep_fences.py", "--check"]),
            ("Whitespace", [PYTHON_EXE, "tools/whitespace_fix.py", "--check"]),
            ("S10 Verify", [PYTHON_EXE, "tools/s10_verify_mark.py", "--check"]),
        ]
    elif stage == "compile":
        gates = [
            ("Compile All", [PYTHON_EXE, "tools/compile_all.py", "--main-only", "--parallel"]),
            ("Compile Gate", [PYTHON_EXE, "tools/compile_gate.py"]),
            ("Exempt Audit", [PYTHON_EXE, "tools/exempt_audit.py", "--check"]),
            ("D5 Compile Gate", [PYTHON_EXE, "tools/d5_compile_gate.py", "--check"]),
            ("Assertions", [PYTHON_EXE, "tools/run_cpp_assertions.py", "--gcc", GCC_EXE]),
        ]
    else:
        print(f"Unknown stage: {stage}")
        return 2

    passed = 0
    failed = 0
    for name, cmd in gates:
        print(f"\n[{name}]")
        try:
            run(cmd, check=True)
            print(f"  ✅ {name} PASS")
            passed += 1
        except subprocess.CalledProcessError as e:
            print(f"  ❌ {name} FAIL")
            if e.stdout:
                print(e.stdout[-800:])
            if e.stderr:
                print(e.stderr[-800:])
            failed += 1

    print(f"\n────────────────────────────────────────")
    print(f"  Result: {passed} passed / {failed} failed")
    print(f"────────────────────────────────────────")
    return 1 if failed else 0


def cmd_build(args: argparse.Namespace) -> int:
    """构建发布产物。"""
    target = args.target
    print(f"\n[cppbible] build {target}\n")
    if target == "site":
        run_python("tools/rewrite_links.py", "--mode", "site")
        run_python("tools/gen_mkdocs_nav.py")
        return run(["mkdocs", "build", "--strict", "--config-file", "build/site/mkdocs.yml"]).returncode
    elif target == "pdf":
        run_python("tools/rewrite_links.py", "--mode", "pdf")
        return run(["bash", "tools/generate_pdf.sh", "--by-part"]).returncode
    elif target == "epub":
        run_python("tools/rewrite_links.py", "--mode", "pdf")
        return run(["bash", "tools/generate_epub.sh"]).returncode
    else:
        print(f"Unknown build target: {target}")
        return 2


def cmd_clean(_args: argparse.Namespace) -> int:
    """清理构建副产物与根目录泄漏。"""
    print("\n[cppbible] clean\n")
    # 1. 调用现有清理脚本
    if (ROOT / "tools" / "clean_root_artifacts.py").exists():
        run_python("tools/clean_root_artifacts.py")

    # 2. 清理 build/ 下的临时日志/轮询文件（保留 site_out/ pdf/ epub/ 等发布产物）
    build = ROOT / "build"
    if build.exists():
        removed = 0
        for pattern in ["_ci_poll*.log", "_compile_job.log", "_intake_*.log", "*.log"]:
            for p in build.glob(pattern):
                p.unlink()
                removed += 1
        print(f"  Removed {removed} build scratch log(s)")

    # 3. 清理根目录编译产物（未被 git 跟踪）
    root_removed = 0
    for ext in ["*.cpp", "*.exe", "*.o", "*.obj"]:
        for p in ROOT.glob(ext):
            r = subprocess.run(["git", "ls-files", "--error-unmatch", str(p)], capture_output=True)
            if r.returncode != 0:  # 未跟踪
                p.unlink()
                root_removed += 1
    print(f"  Removed {root_removed} untracked root artifact(s)")
    return 0


def cmd_install_hooks(_args: argparse.Namespace) -> int:
    """安装 git pre-push hook。"""
    hooks_dir = ROOT / ".git" / "hooks"
    if not hooks_dir.exists():
        print("Error: .git/hooks not found. Are you in a git repo?")
        return 1

    hook = hooks_dir / "pre-push"
    # Git hook 需要正斜杠路径，即便在 Windows 上
    python_posix = Path(PYTHON_EXE).as_posix()
    root_posix = ROOT.as_posix()
    content = f"""#!/bin/sh
# Auto-installed by cppbible install-hooks
exec "{python_posix}" "{root_posix}/tools/cppbible.py" preflight
"""
    hook.write_text(content, encoding="utf-8", newline="\n")
    # POSIX 系统加执行权限；Windows Git 忽略权限但仍可执行
    if sys.platform != "win32":
        hook.chmod(hook.stat().st_mode | 0o111)
    print(f"Installed pre-push hook: {hook}")
    return 0


def cmd_preflight(_args: argparse.Namespace) -> int:
    """推送前快速预检（等价原 pre_push_check.sh 7 项）。"""
    print("\n[cppbible] preflight (push guard)\n")
    checks = [
        ("Consistency", [PYTHON_EXE, "tools/consistency_check.py"]),
        ("Cross-Ref", [PYTHON_EXE, "tools/crossref_audit.py"]),
        ("Deduplication", [PYTHON_EXE, "tools/deduplication_audit.py"]),
        ("Chapter Lint HIGH", [PYTHON_EXE, "tools/chapter_lint.py", "--fail-on", "HIGH"]),
        ("ASM Evidence", [PYTHON_EXE, "tools/verify_asm_evidence.py"]),
    ]

    passed = 0
    failed = 0

    # 卫生检查：只关注未跟踪的泄漏产物；已跟踪的 _bench_d5_*.cpp 等是合法源
    bak = list((ROOT / "Book").rglob("*.bak"))
    probes = [p for p in (ROOT / "tools").glob("_*.py") if p.name != "_clean_junk.py"]
    root_arts = []
    for ext in ["*.cpp", "*.exe", "*.o"]:
        for p in ROOT.glob(ext):
            r = subprocess.run(["git", "ls-files", "--error-unmatch", str(p)], capture_output=True)
            if r.returncode != 0:  # 未跟踪才视为泄漏产物
                root_arts.append(p)
    if not bak and not probes and not root_arts:
        print("  [Hygiene] ✅")
        passed += 1
    else:
        print(f"  [Hygiene] ❌ .bak={len(bak)} probes={len(probes)} untracked_root_artifacts={len(root_arts)}")
        failed += 1

    # 断言缓存
    cache = ROOT / "build" / "assert_report.txt"
    if cache.exists() and "FAIL-CLAIM] 0" in cache.read_text(encoding="utf-8"):
        print("  [Assertions] ✅ (cache FAIL=0)")
        passed += 1
    else:
        print("  [Assertions] ⚠️  cache missing or FAIL>0; run: cppbible check --stage compile")
        # 断言缓存不阻断预检，仅警告

    for name, cmd in checks:
        print(f"\n[{name}]")
        try:
            run(cmd, check=True)
            print(f"  ✅ {name} PASS")
            passed += 1
        except subprocess.CalledProcessError as e:
            print(f"  ❌ {name} FAIL")
            if e.stderr:
                print(e.stderr[-500:])
            failed += 1

    print(f"\nResult: {passed} passed / {failed} failed")
    return 1 if failed else 0


def cmd_report(_args: argparse.Namespace) -> int:
    """汇总 build/reports/ 下各门禁报告（占位，后续 T4 完善）。"""
    reports_dir = ROOT / "build"
    print("\n[cppbible] report summary\n")
    files = sorted(reports_dir.glob("*_report.json")) + sorted(reports_dir.glob("*_audit.json"))
    if not files:
        print("  No reports found in build/")
        return 0
    for f in files[:20]:
        print(f"  - {f.name}")
    if len(files) > 20:
        print(f"  ... and {len(files)-20} more")
    return 0


# ---------------------------------------------------------------------------
# CLI 入口
# ---------------------------------------------------------------------------

def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="cppbible",
        description="CPP-Bible unified toolchain CLI",
    )
    parser.add_argument("--version", action="store_true", help="show version and paths")
    sub = parser.add_subparsers(dest="command", metavar="COMMAND")

    check = sub.add_parser("check", help="run quality/compile gates")
    check.add_argument("--stage", choices=["fast", "quality", "compile"], default="fast",
                       help="fast=local seconds, quality=full CI quality job, compile=compile job")

    build_cmd = sub.add_parser("build", help="build site/pdf/epub")
    build_cmd.add_argument("target", choices=["site", "pdf", "epub"])

    sub.add_parser("clean", help="clean build artifacts and root leaks")
    sub.add_parser("install-hooks", help="install git pre-push hook")
    sub.add_parser("preflight", help="pre-push local checks")
    sub.add_parser("report", help="summarize build reports")

    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.version:
        return cmd_version(args)
    if args.command == "check":
        return cmd_check(args)
    if args.command == "build":
        return cmd_build(args)
    if args.command == "clean":
        return cmd_clean(args)
    if args.command == "install-hooks":
        return cmd_install_hooks(args)
    if args.command == "preflight":
        return cmd_preflight(args)
    if args.command == "report":
        return cmd_report(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
