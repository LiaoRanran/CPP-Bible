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
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Sequence

# 工具链路径解析：唯一事实源 = 仓库根 toolchain.toml（见 tools/toolchain.py）
_TOOLS_DIR = str(Path(__file__).resolve().parent)
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
from toolchain import resolve_gpp as _resolve_gpp  # noqa: E402
from toolchain import resolve_python as _resolve_python  # noqa: E402


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
    """优先 .workbuddy 记忆，否则委托 toolchain.toml 唯一事实源（resolve_python）。"""
    managed = ROOT / ".workbuddy" / "managed_python.txt"
    if managed.exists():
        exe = managed.read_text(encoding="utf-8").strip()
        if Path(exe).exists():
            return exe
    return _resolve_python()


def find_gcc() -> str:
    """解析 g++：唯一事实源为仓库根 toolchain.toml（经 tools/toolchain.py）。

    prefer 列表顺序探测（默认 mingw1530 → mingw1310），全缺失才回退 PATH。
    换机器 / 换 CI 镜像只需编辑 toolchain.toml，不要改本文件。
    """
    return _resolve_gpp()


PYTHON_EXE = find_managed_python()
GCC_EXE = find_gcc()


# ---------------------------------------------------------------------------
# 底层执行 helpers
# ---------------------------------------------------------------------------

def run(cmd: Sequence[str | Path], *, cwd: Path | None = None, check: bool = True, timeout: int | None = None) -> subprocess.CompletedProcess:
    """统一封装 subprocess.run，输出命令本身便于调试。"""
    cmd_str = [str(c) for c in cmd]
    print(f"  $ {' '.join(cmd_str)}", flush=True)
    # 子进程（tools/*.py 等）统一输出 UTF-8（见 xref_check 等工具的 reconfigure）；
    # 这里显式按 UTF-8 解码，避免 Windows 中文控制台按 GBK 解码抛
    # UnicodeDecodeError 把门禁 runner 打崩。
    return subprocess.run(cmd_str, cwd=cwd or ROOT, check=check, text=True,
                          encoding="utf-8", errors="replace",
                          capture_output=True, timeout=timeout)


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


def cmd_env(_args: argparse.Namespace) -> int:
    """工具链自检：探测关键可执行文件与版本，缺失/不匹配即非零退出。

    用于 bootstrap 与 CI 的 `self-check`：保证开发/测试/发布环境一致
    （对应 UPGRADE_PLAN §1.5「dev/test/prod 平滑切换」）。
    """

    print("[cppbible] environment self-check")
    failures = 0

    def probe(label, name, expected=None, prefer=None):
        nonlocal failures
        # prefer 优先（toolchain.toml 同款策略）
        for cand in (prefer or []):
            if os.path.isfile(cand):
                print(f"  [OK] {label}: {cand}")
                return True
        found = shutil.which(name)
        if found:
            ver = ""
            try:
                r = subprocess.run([found, "--version"], capture_output=True,
                                   text=True, encoding="utf-8", errors="replace",
                                   timeout=10)
                ver = (r.stdout or r.stderr).splitlines()[0] if (r.stdout or r.stderr) else ""
            except Exception:
                pass
            ok = (expected is None) or (expected in ver)
            print(f"  [{'OK' if ok else 'MISMATCH'}] {label}: {found} {ver}")
            if not ok:
                failures += 1
            return ok
        print(f"  [FAIL] {label}: 未找到 {name}")
        failures += 1
        return False

    probe("Python", "python", PYTHON_EXE and "3.", prefer=[str(PYTHON_EXE)] if PYTHON_EXE else None)
    probe("GCC/g++", "g++", "15.3.0", prefer=[str(GCC_EXE)] if GCC_EXE else None)
    probe("objdump", "objdump")
    probe("c++filt", "c++filt")
    probe("uv", "uv")
    probe("git", "git")

    print(f"  lock file: uv.lock={'存在' if (ROOT/'uv.lock').exists() else '缺失'}; "
          f"requirements.lock.txt={'存在' if (ROOT/'requirements.lock.txt').exists() else '缺失'}")
    if not (ROOT / "uv.lock").exists():
        failures += 1

    if failures:
        print(f"\n[FAIL] env self-check: {failures} 项异常")
        return 1
    print("\n[OK] env self-check: 工具链完备")
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

    print("\n────────────────────────────────────────")
    print(f"  Result: {passed} passed / {failed} failed")
    print("────────────────────────────────────────")
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

    # 度量看板：每次推送重新生成 build/metrics.json（单一真相源）并打印 15 条验收看板。
    # 非阻塞（与 Assertions 同款）：当前 14/15 未达标，若启用 --strict 会阻断全部真实
    # 工作；待指标接近达标后再于此处加 --strict 升级为 blocking 门禁。
    print("\n[Metrics]")
    try:
        r = run([PYTHON_EXE, "tools/metrics_snapshot.py", "--check"], check=True)
        if r.stdout:
            print(r.stdout, end="")
        print("  ✅ Metrics snapshot OK (build/metrics.json regenerated)")
    except subprocess.CalledProcessError as e:
        print("  ⚠️  Metrics snapshot failed to run (non-blocking)")
        if e.stdout:
            print(e.stdout, end="")
        if e.stderr:
            print(e.stderr[-500:])

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
    """汇总并归集各门禁报告到 build/reports/（T4 归集器 + M1 版式守门员）。

    非阻塞：仅产出可见性报告，不 fail CI。源报告 writer 不动，避免回归。
    """
    print("\n[cppbible] report (collect + style audit)\n")

    # 1) M1 版式守门员：生成 build/markdown_style_report.json（仅报告）
    style_report = ROOT / "build" / "markdown_style_report.json"
    try:
        run([PYTHON_EXE, "tools/markdown_style_guard.py", "--root", "Book",
             "--json", str(style_report)], check=True)
        print("  ✅ markdown_style_guard 完成（非阻塞，详见报告）")
    except subprocess.CalledProcessError as e:
        print(f"  ⚠️  markdown_style_guard 异常（不阻断）: {e}")

    # 2) T4 归集：散落报告 -> build/reports/ + INDEX.json
    reports_out = ROOT / "build" / "reports"
    try:
        run([PYTHON_EXE, "tools/collect_reports.py", "--root", str(ROOT),
             "--out", str(reports_out)], check=True)
    except subprocess.CalledProcessError as e:
        print(f"  ⚠️  collect_reports 异常（不阻断）: {e}")

    # 3) 摘要
    if reports_out.exists():
        idx = reports_out / "INDEX.json"
        n = 0
        if idx.exists():
            data = json.loads(idx.read_text(encoding="utf-8"))
            n = len(data.get("reports", {}))
        files = sorted(reports_out.glob("*.json"))
        print(f"\n  build/reports/ 共 {n} 个报告条目（物理文件 {len(files)}）:")
        for f in files[:25]:
            print(f"    - {f.name}")
        if len(files) > 25:
            print(f"    ... and {len(files)-25} more")
    return 0


def _compile_extra_args(args: argparse.Namespace, *, changed: bool) -> list:
    """Build compile_all.py args for the chosen scope."""
    extra = ["--main-only"]
    if changed:
        extra.append("--changed")
        base = getattr(args, "base", None)
        if base:
            extra += ["--base", base]
    if getattr(args, "parallel", False):
        extra.append("--parallel")
    return extra


def cmd_compile(args: argparse.Namespace) -> int:
    """Incremental/full compile of chapters (produces compile_report.json).

    Default is incremental (--changed): only Book/*.md changed vs git base are
    compiled; if nothing changed it auto-falls back to a full run.  The actual
    regression gate (compile_gate.py) is a separate step/command so CI keeps an
    explicit hard-fail gate; locally follow up with `cppbible check --stage compile`.
    """
    changed = not getattr(args, "full", False)  # 默认增量
    scope = "changed (incremental)" if changed else "full"
    print(f"\n[cppbible] compile --{scope}\n")
    run([PYTHON_EXE, "tools/compile_all.py", *_compile_extra_args(args, changed=changed)],
        check=True)
    print("\n[cppbible] compile done -> tools/compile_report.json")
    print("          下一步: cppbible check --stage compile  (含编译门禁)")
    return 0


def cmd_compile_changed(args: argparse.Namespace) -> int:
    """Alias for `compile --changed`."""
    args.full = False
    return cmd_compile(args)


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
    sub.add_parser("env", help="toolchain self-check (bootstrap/CI)")
    sub.add_parser("install-hooks", help="install git pre-push hook")
    sub.add_parser("preflight", help="pre-push local checks")
    sub.add_parser("report", help="summarize build reports")

    compile_cmd = sub.add_parser("compile", help="compile chapters (incremental/full)")
    compile_cmd.add_argument("--changed", action="store_true",
                             help="only changed chapters (default)")
    compile_cmd.add_argument("--full", dest="full", action="store_true",
                             help="all 151 chapters")
    compile_cmd.add_argument("--base", default=None,
                             help="git base ref for --changed")
    compile_cmd.add_argument("--parallel", action="store_true",
                             help="parallel by part")

    compile_changed = sub.add_parser("compile-changed",
                                     help="alias: compile --changed")
    compile_changed.add_argument("--base", default=None)
    compile_changed.add_argument("--parallel", action="store_true")

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
    if args.command == "env":
        return cmd_env(args)
    if args.command == "install-hooks":
        return cmd_install_hooks(args)
    if args.command == "preflight":
        return cmd_preflight(args)
    if args.command == "report":
        return cmd_report(args)
    if args.command == "compile":
        return cmd_compile(args)
    if args.command == "compile-changed":
        return cmd_compile_changed(args)

    parser.print_help()
    return 0


if __name__ == "__main__":
    # Windows 中文控制台（GBK）无法编码 ✅/⟶ 等字符：统一按 UTF-8 输出，
    # 避免门禁 runner 在打印时抛 UnicodeEncodeError（见审计报告 §5.1）。
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
    sys.exit(main())
