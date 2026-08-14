#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Python 工具链健壮性审计 (#202 工具)。

扫描 tools/*.py，按类别产出可定位报告。用 ast 做结构检查（裸 except / 可变默认参数
/ eval·exec / 通配导入 / assert 做运行时校验），用正则做文本检查（open 缺 encoding、
subprocess shell=True、非 LF 写库文件、rm -rf / git clean 危险操作、吞异常）。

输出：tools/audit_py_tools.json + 汇总。
用法：python tools/audit_py_tools.py
"""
from __future__ import annotations
import ast
import json
import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
TOOLS = REPO / "tools"
OUT = REPO / "tools" / "audit_py_tools.json"

RE_OPEN = re.compile(r"\bopen\s*\(\s*[^)]*\)")
RE_OPEN_HAS_ENCODING = re.compile(r"\bopen\s*\([^)]*encoding\s*=")
RE_SUBPROCESS_SHELL = re.compile(r"subprocess\.\w+\([^)]*shell\s*=\s*True")
RE_RM_RF = re.compile(r"\brm\s+-rf\b|\bshutil\.rmtree\b|\bgIT clean\b", re.IGNORECASE)
RE_GIT_CLEAN = re.compile(r"git\s+clean\s+-[frd]", re.IGNORECASE)
RE_NEWLINE = re.compile(r'\.open\([^)]*newline\s*=')
RE_WRITE_MODE = re.compile(r"open\([^)]*['\"](?:w|a)\b|mode\s*=\s*['\"][^'\"]*w")
RE_WRITE_REPO = re.compile(r'REPO|BOOK|tools/|\.md"|\.json"')

findings: dict[str, list] = {
    "bare_except": [],
    "broad_except_pass": [],
    "mutable_default": [],
    "eval_exec": [],
    "wildcard_import": [],
    "assert_runtime": [],
    "open_no_encoding": [],
    "subprocess_shell_true": [],
    "rm_rf_or_git_clean": [],
    "non_lf_repo_write": [],
}


def add(cat, rel, line, msg):
    findings[cat].append({"file": rel, "line": line, "note": msg})


def audit_file(path: Path):
    rel = path.relative_to(REPO).as_posix()
    if path.name.startswith("audit_"):  # 不扫描审计脚本自身（避免字面量误报）
        return
    src = path.read_text(encoding="utf-8", errors="replace")
    lines = src.split("\n")
    try:
        tree = ast.parse(src)
    except SyntaxError as e:
        add("bare_except", rel, getattr(e, "lineno", 0), f"语法错误无法解析: {e}")
        return

    for node in ast.walk(tree):
        # 裸 except
        if isinstance(node, ast.ExceptHandler) and node.type is None:
            add("bare_except", rel, node.lineno, "裸 except Exception: 会捕获 KeyboardInterrupt/SystemExit，应 except Exception")
        # 可变默认参数
        if isinstance(node, ast.FunctionDef | ast.AsyncFunctionDef):
            for d in node.args.defaults:
                if isinstance(d, (ast.List, ast.Dict, ast.Set)):
                    add("mutable_default", rel, node.lineno, f"可变默认参数: def {node.name}(...) 默认 {type(d).__name__}")
        # eval / exec
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id in ("eval", "exec"):
            add("eval_exec", rel, node.lineno, f"使用了 {node.func.id}()（代码注入/安全隐患）")
        # 通配导入
        if isinstance(node, ast.ImportFrom) and node.names and node.names[0].name == "*":
            add("wildcard_import", rel, node.lineno, "from ... import *（命名空间污染）")
        # assert 做运行时校验
        if isinstance(node, ast.Assert):
            add("assert_runtime", rel, node.lineno, "assert 在 python -O 下被禁用，运行时校验应改显式 if+raise")

    # 文本级检查
    for i, ln in enumerate(lines, 1):
        s = ln.strip()
        # 吞异常：except ...: 之后紧跟 pass（粗略）
        m = re.match(r"except\s+(Exception|\w+)\s*:", s)
        if m and i < len(lines) and lines[i].strip() == "pass":
            add("broad_except_pass", rel, i, f"{m.group(1)} 异常被 pass 吞掉（无日志/无重抛）")
        # open 缺 encoding（仅文本模式、且为内置 open）
        if RE_OPEN.search(ln) and "encoding=" not in ln:
            if (".open(" in ln or "webbrowser.open" in ln
                    or "'rb'" in ln or '"rb"' in ln or "'wb'" in ln or '"wb"' in ln
                    or ("mode=" in ln and ("rb" in ln or "wb" in ln))
                    or '\\"' in ln):  # C++ 字符串字面量内的 open 误报
                pass
            else:
                add("open_no_encoding", rel, i, "open() 未指定 encoding=（文本读写为非确定编码，跨平台风险）")
        # subprocess shell=True
        if RE_SUBPROCESS_SHELL.search(ln):
            add("subprocess_shell_true", rel, i, "subprocess shell=True（命令注入/可移植风险）")
        # rm -rf / git clean / rmtree
        if RE_RM_RF.search(ln):
            add("rm_rf_or_git_clean", rel, i, "检测到 rm -rf / shutil.rmtree / git clean（对仓库/个人目录高危）")
        if RE_GIT_CLEAN.search(ln):
            add("rm_rf_or_git_clean", rel, i, "git clean -f（会删除未跟踪文件，含参考库，极高危）")
        # 写库文件却未用 newline="\n"
        if RE_OPEN.search(ln) and not RE_NEWLINE.search(ln):
            if RE_WRITE_MODE.search(ln) and RE_WRITE_REPO.search(ln):
                add("non_lf_repo_write", rel, i,
                    "向库文件文本写入未指定 newline=\"\\n\"（违反 LF 红线，致 CRLF 伪 diff）")


def main() -> int:
    py_files = sorted(TOOLS.glob("*.py"))
    scanned = 0
    for p in py_files:
        scanned += 1
        audit_file(p)
    summary = {k: len(v) for k, v in findings.items()}
    OUT.write_text(
        json.dumps({"scanned_files": scanned, "categories": findings, "summary": summary},
                   ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"扫描 .py 文件={scanned}")
    print("类别计数:")
    for k, v in summary.items():
        print(f"  {k:22s} {v}")
    print(f"\n报告已写入 {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
