#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""env_probe_671g.py — 671g A4：实验环境依赖自动探测（编译器 / OS / WSL / ASLR / 优化档）。

为什么要有它
============
669 独立审计指出：holdout / corpus 的数字**依赖未被声明的 WSL + sanitizer 环境**，
在缺 WSL 的机器上重跑会静默掉分。671g A4 要求**每个实验产物都带 env 字段**。
本工具把"谁在测"探测成一份机读 JSON，供两类复用：

  1. 新实验产物落盘时，把 :func:`probe` 的结果原样塞进 ``env`` 字段；
  2. 旧产物缺 env 时，门禁（G-ENV-PRESENT）把它标成 ``UNVERIFIED``——
     缺环境声明的数字"可复现性未知"，而不是"默认可复现"。

设计约定
========
* **纯失败软化**：任何一项探测不到（无 WSL / 无编译器 / 非 Windows）都记 ``None``
  + ``error``，绝不抛栈、绝不臆造一个版本号；
* :func:`assemble` 是**纯函数**（输入是已探测到的事实字典）⇒ 单测不必起子进程；
* 只探测、只输出，除 ``--out`` 外不写任何仓库文件。

用法
====
    python tools/env_probe_671g.py                 # 打印机读 JSON
    python tools/env_probe_671g.py --out data/env_671g.json
    python tools/env_probe_671g.py --check         # 关键项可得才 exit 0（CI 用）
"""
from __future__ import annotations

import argparse
import json
import platform
import re
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

SCHEMA = "queyi-env-probe/671g"
TIMEOUT = 20

#: 可复现实验至少需要拿到的环境键（缺任一 ⇒ --check 判失败，但不阻塞其他探测）
REQUIRED_KEYS = ("host_os", "python", "wsl_gpp", "local_gpp", "aslr_control")

_VER_RE = re.compile(r"[^\r\n]*version[^\r\n]*", re.IGNORECASE)


def _run(cmd: list[str], timeout: int = TIMEOUT) -> tuple[int | None, str]:
    """子进程探测，返回 (returncode, 合并输出)；起不来 ⇒ (None, '')，不抛。"""
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, errors="replace",
                             timeout=timeout)
    except (OSError, subprocess.SubprocessError):
        return None, ""
    return r.returncode, ((r.stdout or "") + (r.stderr or "")).strip()


def _first_line(text: str) -> str:
    for line in text.splitlines():
        line = line.strip()
        if line:
            return line
    return text.strip()


def probe_compiler(cmd: list[str]) -> dict[str, Any]:
    """探测一个编译器：{present, version, raw}。cmd 通常是 ['g++','--version']。"""
    code, out = _run(cmd)
    if code is None or not out:
        return {"present": False, "version": None, "raw": "",
                "error": "探测命令不可用或无输出"}
    return {"present": True, "version": _first_line(out), "raw": out[:300], "error": ""}


def probe_wsl() -> dict[str, Any]:
    """探测 WSL 是否可用、其内 g++ 版本、setarch 是否存在（关 ASLR 的手段）。"""
    info: dict[str, Any] = {"available": False, "wsl_gpp": None, "setarch": None,
                              "aslr_sysctl": None, "error": ""}
    if platform.system() != "Windows":
        info["error"] = "非 Windows 宿主，无 WSL 概念"
        return info
    code, out = _run(["wsl", "g++", "--version"])
    if code == 0 and out:
        info["available"] = True
        info["wsl_gpp"] = _first_line(out)
    else:
        info["error"] = "wsl g++ 不可用"
    code2, out2 = _run(["wsl", "setarch", "--help"])
    # setarch --help 在多数发行版上 returncode 非 0 但有输出；认输出即可
    info["setarch"] = "setarch -R 可用" if ("setarch" in out2 or code2 is not None
                                                 and out2) else None
    code3, out3 = _run(["wsl", "cat", "/proc/sys/kernel/randomize_va_space"])
    if code3 == 0 and out3.strip() in {"0", "1", "2"}:
        info["aslr_sysctl"] = int(out3.strip())
    return info


def probe_local() -> dict[str, Any]:
    """探测宿主机本地 g++ / clang++（Windows 上即 MinGW / MSYS2 工具链）。"""
    return {
        "gpp": probe_compiler(["g++", "--version"]),
        "clang": probe_compiler(["clang++", "--version"]),
    }


def probe_aslr_control() -> dict[str, Any]:
    """ASLR 状态说明。

    注意：``setarch -R`` 是**每次调用子进程时临时关 ASLR**，不是一个全局开关，
    所以这里不谎称"当前 ASLR 已关"，只声明：本批实验 run 命令是否用了 setarch -R，
    以及 WSL 内核的全局 ASLR 开关值（0/1/2）。
    """
    wsl = probe_wsl()
    return {
        "method": "实验子进程前缀 `setarch -R`（地址空间随机化在该进程内关闭）",
        "wsl_kernel_randomize_va_space": wsl.get("aslr_sysctl"),
        "setarch_available": bool(wsl.get("setarch")),
        "note": "setarch -R 是 per-run 关闭，不存在持久全局状态；逐样本 run 必须带此前缀",
    }


def assemble(*, host: dict[str, Any] | None = None, python_ver: str | None = None,
            wsl: dict[str, Any] | None = None, local: dict[str, Any] | None = None,
            aslr: dict[str, Any] | None = None, opt_levels: list[str] | None = None,
            generated_at: float | None = None) -> dict[str, Any]:
    """纯函数：把已探测事实装成标准 env 报告（单测走这里，不起子进程）。"""
    return {
        "schema": SCHEMA,
        "generated_at": time.strftime(
            "%Y-%m-%d %H:%M:%S",
            time.localtime(generated_at) if generated_at is not None else time.localtime()),
        "host_os": host or {},
        "python": python_ver or platform.python_version(),
        "wsl": wsl or {},
        "wsl_gpp": (wsl or {}).get("wsl_gpp"),
        "local_gpp": ((local or {}).get("gpp") or {}).get("version"),
        "local_clang": ((local or {}).get("clang") or {}).get("version"),
        "aslr_control": aslr or {},
        "opt_levels": opt_levels or ["-O0", "-O2"],
    }


def probe() -> dict[str, Any]:
    """实地探测当前机器，组装 env 报告（失败软化，不抛异常）。"""
    host = {"system": platform.system(), "release": platform.release(),
            "version": platform.version(), "machine": platform.machine()}
    wsl = probe_wsl()
    local = probe_local()
    aslr = probe_aslr_control()
    return assemble(host=host, python_ver=platform.python_version(), wsl=wsl, local=local,
                  aslr=aslr)


def missing_required(env: dict[str, Any]) -> list[str]:
    """返回关键环境键里"拿不到"的键名（供 --check / 门禁判 UNVERIFIED）。"""
    miss = []
    if not env.get("host_os"):
        miss.append("host_os")
    if not env.get("python"):
        miss.append("python")
    if not env.get("wsl_gpp"):
        miss.append("wsl_gpp")
    if not env.get("local_gpp"):
        miss.append("local_gpp")
    if not (env.get("aslr_control") or {}).get("setarch_available"):
        miss.append("aslr_control.setarch_available")
    return miss


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="671g A4：实验环境依赖探测")
    ap.add_argument("--out", default=None, help="把 JSON 写到指定路径（默认只打印）")
    ap.add_argument("--check", action="store_true",
                    help="关键环境项（WSL g++/本地 g++/setarch）齐全才 exit 0")
    a = ap.parse_args(argv)
    env = probe()
    text = json.dumps(env, ensure_ascii=False, indent=2)
    print(text)
    if a.out:
        p = Path(a.out)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(text + "\n", encoding="utf-8")
    if a.check:
        miss = missing_required(env)
        if miss:
            print(f"[env_probe_671g] 关键环境缺失：{miss} ⇒ 相关实验产物应标 UNVERIFIED",
                  file=sys.stderr)
            return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
