#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""dist_verify_670c2.py — 构建产物验证（670c2 C2）。

检查 `web/dist/`：
  1. 8 个 HTML 齐全
  2. 所有 JS 通过 `node --check`（无语法错误）
  3. 每个 HTML 引用的本地资源（src/href）都存在
  4. 体积预算：首页（index.html + 其引用资源）≤ 200KB

只读。退出码：0 = 全通过；1 = 有失败项。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "web", "dist")
PAGES = ["index", "cards", "learn", "experiments", "verdicts", "starmap", "verify", "card"]
HOME_BUDGET = 200 * 1024
REF_RE = re.compile(r'(?:src|href)\s*=\s*"([^"]+)"')


def node_bin() -> str | None:
    for c in (os.environ.get("NODE"),
              shutil.which("node"),
              r"C:\Users\ASUS\.workbuddy-ai\binaries\node\versions\22.22.2-3\node.exe",
              r"C:\Program Files\nodejs\node.exe"):
        if c and os.path.isfile(c):
            return c
    return shutil.which("node")


def run() -> dict:
    errors, ok = [], []

    # 1. HTML 齐全
    for p in PAGES:
        f = os.path.join(DIST, p + ".html")
        if os.path.isfile(f):
            ok.append(f"HTML 存在: {p}.html")
        else:
            errors.append(f"缺 HTML: {p}.html")

    # 2. JS 语法
    node = node_bin()
    js_files = []
    for dirpath, _, files in os.walk(DIST):
        for fn in files:
            if fn.endswith(".js"):
                js_files.append(os.path.join(dirpath, fn))
    if node:
        bad = 0
        for js in js_files:
            r = subprocess.run([node, "--check", js], capture_output=True, text=True)
            if r.returncode != 0:
                bad += 1
                errors.append(f"JS 语法错误: {os.path.relpath(js, DIST)} :: {r.stderr.strip().splitlines()[:1]}")
        ok.append(f"JS 语法检查: {len(js_files)} 个文件, {bad} 个错误")
    else:
        errors.append("未找到 node，无法做 JS 语法检查")

    # 3. HTML 引用资源存在
    missing = 0
    for p in PAGES:
        html_path = os.path.join(DIST, p + ".html")
        if not os.path.isfile(html_path):
            continue
        text = open(html_path, encoding="utf-8", errors="replace").read()
        for ref in REF_RE.findall(text):
            if ref.startswith(("http://", "https://", "//", "data:", "#", "mailto:")):
                continue
            target = os.path.normpath(os.path.join(DIST, ref.split("?")[0].split("#")[0]))
            if not os.path.isfile(target):
                missing += 1
                errors.append(f"{p}.html 引用缺失: {ref}")
    ok.append(f"引用资源: 缺失 {missing}")

    # 4. 首页体积预算
    idx = os.path.join(DIST, "index.html")
    if os.path.isfile(idx):
        total = os.path.getsize(idx)
        text = open(idx, encoding="utf-8", errors="replace").read()
        seen = set()
        for ref in REF_RE.findall(text):
            if ref.startswith(("http://", "https://", "//", "data:", "#", "mailto:")):
                continue
            t = os.path.normpath(os.path.join(DIST, ref.split("?")[0].split("#")[0]))
            if t in seen:
                continue
            seen.add(t)
            if os.path.isfile(t):
                total += os.path.getsize(t)
        if total <= HOME_BUDGET:
            ok.append(f"首页体积 {total/1024:.1f}KB ≤ 200KB")
        else:
            errors.append(f"首页体积 {total/1024:.1f}KB > 200KB 预算")

    return {"pages": len(PAGES), "js_files": len(js_files), "ok": ok, "errors": errors}


def main() -> int:
    ap = argparse.ArgumentParser(description="dist 构建产物验证（670c2 C2）")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if not os.path.isdir(DIST):
        print(f"[dist] 缺 {DIST}")
        return 1
    res = run()
    if args.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        print(f"[dist] HTML {res['pages']} 页, JS {res['js_files']} 个")
        for s in res["ok"]:
            print("  [OK ]", s)
        for e in res["errors"]:
            print("  [ERR]", e)
        print("[dist] " + ("PASS" if not res["errors"] else "FAIL"))
    return 0 if not res["errors"] else 1


if __name__ == "__main__":
    sys.exit(main())
