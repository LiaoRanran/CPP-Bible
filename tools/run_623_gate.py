"""623 C1 · 收工门禁（整目录 ruff 口径统一）

**问题**：622 的收工门禁对 623 这批"只跑本批新文件 ruff"——这会让 **tools/ 的存量债**
（如 618/619 的 F401/E702 等）在门禁绿的情况下溜进主线。622 B2 实测 CI 红因之一正是
`tools/` 存量 ruff 债，而"只查新文件"的门禁永远不会发现存量债。

**623 修正**：收工门禁对 **整个 tools/（及 tests/）目录**跑 ruff，而非仅本批新增文件。
本工具即该统一门禁的本地实现，供 F2 收工门禁调用。

铁律：不修改受控目录/工具逻辑；仅执行 ruff 检查，不改写任何文件（--fix 不开放）。
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def collect_py_files(dirs: list[str]) -> list[str]:
    """递归收集目录下所有 .py 文件（跳过 .venv / node_modules / 隐藏目录）。"""
    out: list[str] = []
    for d in dirs:
        if not os.path.isdir(d):
            continue
        for root, sub, files in os.walk(d):
            if any(part in (".venv", "node_modules", ".git") for part in root.split(os.sep)):
                continue
            for fn in files:
                if fn.endswith(".py"):
                    out.append(os.path.join(root, fn))
    return sorted(out)


def collect_batch_files(dirs: list[str], patterns: list[str]) -> list[str]:
    """仅收集匹配本批模式的文件（演示"只跑本批"的反模式用）。"""
    import fnmatch
    all_py = collect_py_files(dirs)
    return [p for p in all_py if any(fnmatch.fnmatch(os.path.basename(p), pat) for pat in patterns)]


def run_ruff(paths: list[str]) -> tuple[int, str]:
    if not paths:
        return 0, "no python files to check"
    cmd = [sys.executable, "-m", "ruff", "check", *paths]
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return proc.returncode, proc.stdout + proc.stderr


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="623 C1 收工门禁：整目录 ruff")
    ap.add_argument("--dirs", nargs="+", default=["tools", "tests"],
                    help="要检查的目录（默认 tools tests，整目录）")
    ap.add_argument("--only-batch", nargs="+", default=None,
                    help="若提供，仅检查匹配该 glob 的本批文件（演示反模式，默认关闭）")
    args = ap.parse_args(argv)

    if args.only_batch:
        targets = collect_batch_files(args.dirs, args.only_batch)
        mode = f"only-batch({args.only_batch})"
    else:
        targets = collect_py_files(args.dirs)
        mode = "whole-dir"

    rc, out = run_ruff(targets)
    print(f"[run_623_gate] 模式={mode} 检查 {len(targets)} 个 .py 文件")
    if out.strip():
        print(out.strip())
    if rc == 0:
        print("✓ ruff 全绿")
    else:
        print("✗ ruff 发现违规（门禁红）")
    return rc


if __name__ == "__main__":
    sys.exit(main())
