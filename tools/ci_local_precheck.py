#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""ci_local_precheck.py — 本地复跑 CI `quality` job 的步骤，push 前预检，避免"修一步推一次"。

为什么要它（2026-09-10 三次盲查的教训）
======================================
CI #550 / #551 / #552 连续红在 quality job，而 GitHub 的 job 日志下载**需要 admin 权限**
（实测 REST API 403），step summary 又只有 UI 可见（API 读不到）。于是每一次都只能：
push → 等 CI → 看不到日志 → 猜根因 → 再 push。三次往返后才发现真正的失败点分别是
"跨编译器哈希"、"断言平台敏感"、"`_pin_compiler` 判据随平台漂移"。

根因是**反馈闭环太长**：CI 里后面的步骤会被前面失败 skip，所以"第 N 步之后从未跑过"。
本工具把 ci.yml 的 `run` 命令抽出来在本地顺序执行，一次暴露全部问题。

用法
====
    python3 tools/ci_local_precheck.py              # 跑全部步骤（跳过需网络的 pip/apt 步）
    python3 tools/ci_local_precheck.py --list       # 只列出步骤名
    python3 tools/ci_local_precheck.py --only asm   # 只跑名字含 asm 的步（大小写不敏感）

注：Linux 环境（CI runner 或 WSL 的 Ubuntu）下最准；Windows 下部分步会因路径/工具差异失真。
需网络的步（`pip install` / `apt-get`）会被跳过并标注——它们已在别处单独验证。
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
YML = ROOT / ".github" / "workflows" / "ci.yml"
SKIP_HINT = ("pip install", "apt-get", "sudo ", "command -v c++filt")


def parse_steps() -> list[tuple[str, list[str]]]:
    """从 ci.yml 抽出 `quality` job 的 (步骤名, 命令行列表)。

    只做够用的子集解析（不引 yaml 依赖）：`- name:` 分段，段内 `run: |` 取缩进块，
    `run: <单行>` 取整行。
    """
    text = YML.read_text(encoding="utf-8")
    m = re.search(r"\n  quality:\n(.*?)(?=\n  [a-z][a-z0-9-]*:\n)", text, re.S)
    if not m:
        sys.exit("[ci-local] 未找到 quality job（ci.yml 结构变了？）")
    lines = m.group(1).split("\n")
    out: list[tuple[str, list[str]]] = []
    i = 0
    while i < len(lines):
        name_m = re.match(r"\s*- name: (.+)$", lines[i])
        if not name_m:
            i += 1
            continue
        name = name_m.group(1).strip()
        cmds: list[str] = []
        j = i + 1
        while j < len(lines) and not re.match(r"\s*- name: ", lines[j]):
            run_m = re.match(r"^(\s*)run: ?(.*)$", lines[j])
            if run_m:
                ind, rest = len(run_m.group(1)), run_m.group(2).strip()
                if rest in ("|", ">"):
                    k = j + 1
                    while k < len(lines) and (not lines[k].strip()
                                              or len(lines[k]) - len(lines[k].lstrip()) > ind):
                        cmds.append(lines[k].strip())
                        k += 1
                    j = k - 1
                elif rest:
                    cmds.append(rest)
            j += 1
        out.append((name, cmds))
        i = j
    return out


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="本地复跑 CI quality job 的步骤")
    ap.add_argument("--list", action="store_true", help="只列出步骤名")
    ap.add_argument("--only", default="", help="只跑名字含该子串的步（大小写不敏感）")
    a = ap.parse_args(argv)

    steps = parse_steps()
    if a.list:
        for n, _ in steps:
            print(n)
        return 0

    fails: list[str] = []
    ran = 0
    for name, cmds in steps:
        if a.only and a.only.lower() not in name.lower():
            continue
        script = "\n".join(cmds)
        if not script:
            continue
        if any(h in script for h in SKIP_HINT):
            print(f"SKIP  {name}（需网络/权限，另行验证）")
            continue
        ran += 1
        try:
            r = subprocess.run(["bash", "-c", script], cwd=str(ROOT), capture_output=True,
                               text=True, errors="replace", timeout=900)
        except (OSError, subprocess.SubprocessError) as exc:
            print(f"FAIL  {name}  (无法执行：{exc})")
            fails.append(name)
            continue
        ok = r.returncode == 0
        print(f"{'OK  ' if ok else 'FAIL'}  {name}  (rc={r.returncode})")
        if not ok:
            fails.append(name)
            for ln in ((r.stdout or "") + (r.stderr or "")).strip().split("\n")[-12:]:
                print("       ", ln[:150])
    print(f"\n[ci-local] 执行 {ran} 步 · 失败 {len(fails)}：{fails if fails else '无'}")
    return 1 if fails else 0


if __name__ == "__main__":
    raise SystemExit(main())
