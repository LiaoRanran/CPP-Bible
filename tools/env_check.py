#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
env_check.py — 一键环境体检（秒级，不跑慢门禁）

用途：任何新会话/苦力/好模型开工前跑一次，就知道"这套环境能干什么、缺什么、哪里分裂"，
      不必反复 where / --version 烧 token。只读探测，不改任何文件。

用法:
    .venv\\Scripts\\python.exe tools/env_check.py            # 人读报告
    .venv\\Scripts\\python.exe tools/env_check.py --json     # 机器读（CI/agent 解析）

退出码: 0=环境健康; 1=有不一致/缺失（详情看报告，不 fail-closed，只提示）
"""
# mypy: ignore-errors
# 存量工具：类型注解债务，CI 先转绿，后续逐步修
from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
REPORT: dict = {}
RED: list[str] = []


def sh(*args: str) -> str:
    try:
        out = subprocess.run(args, capture_output=True, text=True, timeout=20,
                             encoding="utf-8", errors="replace")
        return (out.stdout or out.stderr).strip().splitlines()
    except Exception as e:
        return [f"<err: {e}>"]


def which_all(name: str) -> list[str]:
    r = sh("where.exe", name)
    return [ln for ln in r if ln.lower().endswith((".exe", name)) or "\\" in ln]


def first_line(lines: list[str]) -> str:
    return lines[0] if lines else "(无输出)"


# ── 1. Python ──────────────────────────────────────────────────────────
py = {"exe": sys.executable, "version": sys.version.split()[0]}
deps = {}
for mod in ("yaml", "pytest", "pytest_xdist", "filelock", "rich", "numpy"):
    try:
        m = __import__(mod)
        deps[mod] = getattr(m, "__version__", "?")
    except Exception:
        deps[mod] = "MISSING"
        RED.append(f"python 依赖缺失: {mod}")
REPORT["python"] = py
REPORT["python_deps"] = deps

# ── 2. 编译器（重点：版本分裂检测）─────────────────────────────────────
compilers = {}
for name in ("g++", "gcc", "clang++", "clang", "clang-cl", "cl",
             "riscv64-unknown-elf-g++", "ccache", "clang-tidy",
             "clang-format", "cppcheck"):
    paths = which_all(name)
    if not paths:
        compilers[name] = {"present": False}
        continue
    # 每个候选都取版本，找出分裂
    versions = []
    for p in paths:
        ver = first_line(sh(p, "--version"))
        versions.append({"path": p, "version": ver})
    compilers[name] = {"present": True, "candidates": versions,
                       "on_path": paths[0]}
    if len(paths) > 1:
        uniq = {v["version"] for v in versions}
        if len(uniq) > 1:
            RED.append(f"{name} 版本分裂: " + " | ".join(
                f'{os.path.basename(v["path"])}={v["version"]}' for v in versions))
REPORT["compilers"] = compilers

# ── 3. WSL ────────────────────────────────────────────────────────────
wsl = sh("wsl", "-l", "-v")
REPORT["wsl"] = [ln for ln in wsl if ln.strip() and ("Ubuntu" in ln or "STATE" in ln)]

# ── 4. 磁盘 ───────────────────────────────────────────────────────────
try:
    free_gb = round((ROOT.drive and shutil.disk_usage(ROOT.drive + "\\")[2]) / 1e9, 1)
except Exception:
    free_gb = "?"
REPORT["disk_free_gb"] = free_gb

# ── 5. git 状态 ────────────────────────────────────────────────────────
def git(*a: str) -> str:
    return first_line(sh("git", *a))
REPORT["git"] = {
    "head": git("rev-parse", "--short", "HEAD"),
    "branch": git("rev-parse", "--abbrev-ref", "HEAD"),
    "remote": git("remote", "get-url", "origin"),
    "status": git("status", "-sb"),
}

# ── 6. 关键门禁工具可执行性（不跑全量，只看 --help 能起来）─────────────
tools = ["gate_engine.py", "atom_evidence_replay.py", "poison_drill.py",
         "golden_lock.py", "knowledge_graph.py", "tool_integrity.py"]
exec_ok = {}
for t in tools:
    p = ROOT / "tools" / t
    exec_ok[t] = p.exists()
REPORT["tool_files_present"] = exec_ok
for t, ok in exec_ok.items():
    if not ok:
        RED.append(f"关键工具缺失: tools/{t}")


def human(r: dict) -> str:
    L = ["=" * 60, "环境体检 env_check", "=" * 60]
    L.append(f"Python   : {r['python']['exe']}  (v{r['python']['version']})")
    dep = "  ".join(f"{k}={v}" for k, v in r["python_deps"].items())
    L.append(f"依赖     : {dep}")
    L.append("编译器:")
    for name, c in r["compilers"].items():
        if not c["present"]:
            L.append(f"  - {name:<28} [缺失]")
            continue
        main = c["on_path"]
        L.append(f"  - {name:<28} PATH首={os.path.basename(os.path.dirname(main))} "
                 f"({len(c['candidates'])}个候选)")
        for v in c["candidates"]:
            L.append(f"      · {v['path']}")
            L.append(f"          {v['version']}")
    L.append(f"WSL      : {'; '.join(r['wsl']) or '(查询失败)'}")
    L.append(f"磁盘剩余 : {r['disk_free_gb']} GB")
    g = r["git"]
    L.append(f"git      : {g['branch']} @ {g['head']}  remote={g['remote']}")
    L.append(f"           {g['status']}")
    L.append("-" * 60)
    if RED:
        L.append(f"⚠ 发现 {len(RED)} 项需关注:")
        for x in RED:
            L.append(f"   ! {x}")
    else:
        L.append("✓ 未发现环境不一致")
    return "\n".join(L)


if "--json" in sys.argv:
    print(json.dumps({"report": REPORT, "warnings": RED},
                     ensure_ascii=False, indent=2))
else:
    print(human(REPORT))
sys.exit(1 if RED else 0)
