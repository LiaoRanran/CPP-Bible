#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
json_project_gate.py — 贯穿项目线（台阶二）· 手写 JSON 库编译+运行门禁
====================================================================

把 `Examples/json/` 的贯穿项目纳入 CI 门禁：编译并运行
`json_test.cpp`（自测 84 例）与 `json_demo.cpp`（配置读→查→改→回写演示），
验证 JSON 库「可编译、可测、可运行」。未来任何编辑若破坏 JSON 库，
CI 立即变红 BLOCK。

用法:
    python3 tools/json_project_gate.py            # 报告模式（默认，exit 0 表示全过）
    python3 tools/json_project_gate.py --check    # 门禁模式：任一失败 exit 1
    python3 tools/json_project_gate.py --gpp PATH # 覆盖编译器路径（默认见 toolchain.toml）

退出码：0 = 全部通过；1 = 存在失败；2 = 环境错误（找不到 g++）。
"""

import os
import sys
import shutil
import argparse
import subprocess
import tempfile

_TOOLS_DIR = os.path.dirname(os.path.abspath(__file__))
if _TOOLS_DIR not in sys.path:
    sys.path.insert(0, _TOOLS_DIR)
from toolchain import resolve_gpp  # noqa: E402

ROOT = os.path.dirname(_TOOLS_DIR)
JSON_DIR = os.path.join(ROOT, "Examples", "json")

STD = "-std=c++23"
OPT = "-O2"
WARN = ["-Wall", "-Wextra"]

# (源文件, 期望输出片段 or None)。None 表示仅要求「编译 + 退出码 0」。
TARGETS = [
    ("json_test.cpp", "84 passed, 0 failed"),
    ("json_demo.cpp", None),
]


def find_gpp(explicit):
    gpp = explicit or os.environ.get("JSON_GPP") or resolve_gpp()
    if not gpp:
        return None, "(toolchain.toml 未解析到 g++)"
    if os.path.dirname(gpp):
        if not os.path.exists(gpp):
            return None, gpp
    else:
        found = shutil.which(gpp)
        if found is None:
            return None, gpp
        gpp = found
    try:
        out = subprocess.run([gpp, "--version"], capture_output=True, text=True, timeout=30)
        ver = out.stdout.splitlines()[0] if out.stdout else "(unknown)"
    except Exception:  # noqa
        return None, gpp
    return gpp, ver


def build_and_run(gpp, src, tmpdir):
    """编译并运行 src，返回 (ok, stdout, note)。"""
    base = os.path.splitext(os.path.basename(src))[0]
    exe = os.path.join(tmpdir, base + (".exe" if os.name == "nt" else ""))
    src_abs = os.path.join(JSON_DIR, src)
    cmd = [gpp, STD, OPT, *WARN, "-I", JSON_DIR, "-o", exe, src_abs]
    r = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        err = (r.stderr or r.stdout).strip()
        return False, "", "COMPILE: " + (err.splitlines()[-1] if err else "no output")
    r = subprocess.run([exe], capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != 0:
        return False, "", "RUN: exit " + str(r.returncode)
    return True, r.stdout, ""


def main():
    ap = argparse.ArgumentParser(description="JSON 贯穿项目编译+运行门禁")
    ap.add_argument("--check", action="store_true", help="门禁模式：任一失败 exit 1")
    ap.add_argument("--gpp", default=None, help="覆盖编译器路径")
    args = ap.parse_args()

    gpp, note = find_gpp(args.gpp)
    if gpp is None:
        print(f"[ENV-ERR] 找不到编译器: {note}（可用 --gpp 或 JSON_GPP 指定）")
        return 2

    print(f"[toolchain] {gpp}  |  {note}")
    tmpdir = tempfile.mkdtemp(prefix="json_gate_")
    fail = 0
    for src, expect in TARGETS:
        ok, out, note = build_and_run(gpp, src, tmpdir)
        if not ok:
            fail += 1
            print(f"[FAIL] {src}: {note}")
            continue
        if expect and expect not in out:
            fail += 1
            print(f"[FAIL] {src}: 期望输出含 '{expect}' 但未匹配")
            continue
        print(f"[PASS] {src}")
    print(f"json_project_gate: {len(TARGETS) - fail}/{len(TARGETS)} passed")
    return 1 if fail else 0


if __name__ == "__main__":
    sys.exit(main())