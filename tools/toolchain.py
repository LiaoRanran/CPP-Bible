#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""toolchain.py — 工具链路径解析（唯一事实源 = 仓库根 ``toolchain.toml``）

背景
====
此前 6 个 ``tools/*.py`` 中散落 **12 处**硬编码 ``C:/Qt/Tools/...``。后果：
换机器 / 换 CI 镜像 / Qt 升级即全链崩溃，且失败信息不指向根因（ISSUES #6
只登记了 1 处，实际 12 处）。

本模块把所有路径解析收敛到一处：
- 优先按 ``toolchain.toml`` 的 ``prefer`` 列表顺序探测（第一个存在即用）；
- ``prefer`` 全缺失才回退 ``PATH`` 上的 ``fallback_names``；
- 配置文件缺失时回退到内置 ``_DEFAULTS``（与配置文件同值，**永不因缺配置而崩**）。

设计约束（对齐项目红线）
========================
- 零第三方依赖：自带极简 TOML 子集解析器，不依赖 ``tomllib``(3.11+)，
  以免在旧版 CI Python 上 ImportError。
- 只读取，不写源文件。

用法
====
    from toolchain import resolve_gpp, resolve_cxxfilt, resolve_objdump
    gpp = resolve_gpp()          # -> 绝对路径字符串
    filt = resolve_cxxfilt()     # -> 绝对路径字符串 或 None

命令行自检::

    python tools/toolchain.py
"""
from __future__ import annotations

import glob
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
CONFIG = ROOT / "toolchain.toml"

# 与 toolchain.toml 同值的内置兜底：配置文件缺失时行为完全一致。
_DEFAULTS: dict[str, dict[str, list[str]]] = {
    "compiler": {
        "prefer": [
            r"C:/Qt/Tools/mingw1530_64/bin/g++.exe",
            r"C:/Qt/Tools/mingw1310_64/bin/g++.exe",
        ],
        "fallback_names": ["g++", "clang++"],
    },
    "binutils": {
        "cxxfilt_prefer": [
            r"C:/Qt/Tools/mingw1530_64/bin/c++filt.exe",
            r"C:/Qt/Tools/mingw1310_64/bin/c++filt.exe",
        ],
        "cxxfilt_names": ["c++filt", "x86_64-w64-mingw32-c++filt", "c++filt.exe"],
        "objdump_prefer": [
            r"C:/Qt/Tools/mingw1530_64/bin/objdump.exe",
            r"C:/Qt/Tools/mingw1310_64/bin/objdump.exe",
        ],
        "objdump_names": ["objdump", "x86_64-linux-gnu-objdump", "objdump.exe"],
    },
    "python": {
        "prefer": [
            r"C:/Users/ASUS/.workbuddy/binaries/python/versions/3.13.*/python.exe",
        ],
        "expected": ["3.13"],
    },
}

_SECTION_RE = re.compile(r"^\[([A-Za-z0-9_]+)\]\s*$")
_STR_RE = re.compile(r"^([A-Za-z0-9_]+)\s*=\s*[\"']([^\"']*)[\"']\s*$")
_LIST_RE = re.compile(r"^([A-Za-z0-9_]+)\s*=\s*\[(.*?)\]", re.S)
_STR_ITEM_RE = re.compile(r"[\"']([^\"']*)[\"']")


def _strip_comment(line: str) -> str:
    """去掉行注释（不处理引号内的 #，本项目配置无此情况）。"""
    idx = line.find("#")
    return line[:idx] if idx >= 0 else line


def _parse_toml(text: str) -> dict[str, dict[str, list[str]]]:
    """极简 TOML 子集解析：``[section]`` + ``key = "v"`` + ``key = [... ]``。

    只覆盖 toolchain.toml 用到的语法；解析失败时返回 ``{}``，
    由调用方回退到 ``_DEFAULTS``（**配置错误不应导致工具链崩溃**）。
    """
    out: dict[str, dict[str, list[str]]] = {}
    section = ""
    buf: list[str] = []
    lines = [_strip_comment(ln).rstrip() for ln in text.splitlines()]

    def flush() -> None:
        """把缓冲区里的（可能跨行的）数组定义解析出来。"""
        if not section or not buf:
            return
        joined = "\n".join(buf)
        m = _LIST_RE.match(joined)
        if m:
            out.setdefault(section, {})[m.group(1)] = _STR_ITEM_RE.findall(m.group(2))

    for ln in lines:
        m_sec = _SECTION_RE.match(ln.strip())
        if m_sec:
            flush()
            buf = []
            section = m_sec.group(1)
            out.setdefault(section, {})
            continue
        if not ln.strip():
            continue
        m_str = _STR_RE.match(ln.strip())
        if m_str and section:
            out.setdefault(section, {})[m_str.group(1)] = [m_str.group(2)]
            continue
        if "[" in ln:
            buf = [ln] if not buf else buf + [ln]
            if "]" in ln:
                flush()
                buf = []
            continue
        if buf:
            buf.append(ln)
    flush()
    return out


def _load() -> dict[str, dict[str, list[str]]]:
    """加载配置；缺失或解析失败时回退内置默认值。"""
    try:
        if not CONFIG.is_file():
            return _DEFAULTS
        parsed = _parse_toml(CONFIG.read_text(encoding="utf-8"))
        # 与默认值合并：配置文件可只写部分键
        merged = {k: dict(v) for k, v in _DEFAULTS.items()}
        for sec, kv in parsed.items():
            merged.setdefault(sec, {}).update(kv)
        return merged
    except Exception:  # 配置损坏 → 静默回退，保证门禁可用
        return _DEFAULTS


_CFG = _load()


def _resolve(prefer_key: str, names_key: str, section: str) -> str | None:
    """按 prefer 绝对路径 → PATH 名称 的顺序解析一个可执行文件路径。"""
    sec = _CFG.get(section, {})
    for p in sec.get(prefer_key, []):
        if p and os.path.isfile(p):
            return os.path.normpath(p)
    for name in sec.get(names_key, []):
        found = shutil.which(name)
        if found:
            return os.path.normpath(found)
    return None


def resolve_gpp(explicit: str | None = None) -> str:
    """返回 g++ 路径。``explicit`` 非空时直接采用（命令行 --gcc 覆盖）。"""
    if explicit:
        return os.path.normpath(explicit)
    found = _resolve("prefer", "fallback_names", "compiler")
    if found:
        return found
    # 兜底：宁可返回裸命令让 subprocess 报错，也不要在此抛异常打断门禁
    return "g++"


def resolve_cxxfilt() -> str | None:
    """返回 c++filt 路径；全部缺失返回 None（调用方按可选工具处理）。"""
    return _resolve("cxxfilt_prefer", "cxxfilt_names", "binutils")


def resolve_objdump() -> str | None:
    """返回 objdump 路径；全部缺失返回 None。"""
    return _resolve("objdump_prefer", "objdump_names", "binutils")


def _patch_key(path: str) -> tuple[int, int, int]:
    """从 glob 命中的路径里抽 ``(major, minor, patch)`` 作为数值排序键。

    纯字典序排序会把 ``3.13.12`` 排在 ``3.13.2`` 之前（``'1' < '2'``），
    与「取最新 patch」的直觉相反；故按数值比较。无法解析时返回 (0,0,0)，
    使「无版本号」的候选稳定沉底，不喧宾夺主。
    """
    m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", path)
    if not m:
        return (0, 0, 0)
    return (int(m.group(1)), int(m.group(2)), int(m.group(3) or 0))


def resolve_python() -> str:
    """返回托管 Python 路径；全部缺失时回退当前解释器 ``sys.executable``。

    ``prefer`` 项支持 glob（如 ``versions/3.13.*/python.exe``），使配置
    对 patch 级目录改名免疫——托管目录名 ``3.13.12`` 但其内二进制实为
    ``3.13.14``，锁死具体 patch 会让「配置路径」不可信；命中多候选时按
    版本号数值排序取**最高 patch**，既确定又符合直觉。
    """
    for p in _CFG.get("python", {}).get("prefer", []):
        if not p:
            continue
        if any(ch in p for ch in "*?["):
            for hit in sorted(glob.glob(p), key=_patch_key, reverse=True):
                if os.path.isfile(hit):
                    return os.path.normpath(hit)
        elif os.path.isfile(p):
            return os.path.normpath(p)
    return sys.executable


def resolve_python_version() -> str | None:
    """运行已解析 Python 的 ``--version``，返回 ``3.13.14`` 形式的版本串。

    失败（无法执行、超时、正则不匹配）返回 None，绝不抛异常，保证门禁可用。
    """
    exe = resolve_python()
    try:
        r = subprocess.run(
            [exe, "--version"], capture_output=True, text=True, timeout=15
        )
    except (OSError, subprocess.SubprocessError):
        return None
    m = re.search(r"Python\s+(\d+\.\d+(?:\.\d+)?)", r.stdout or r.stderr)
    return m.group(1) if m else None


def expected_python() -> str | None:
    """读 ``[python].expected``（如 ``3.13``）；缺失返回 None。"""
    exp = _CFG.get("python", {}).get("expected", [])
    return exp[0] if exp else None


def report() -> dict[str, str | None]:
    """供 metrics.json 使用的解析结果快照（含配置来源）。"""
    return {
        "config": str(CONFIG) if CONFIG.is_file() else None,
        "config_present": CONFIG.is_file(),
        "gpp": resolve_gpp(),
        "cxxfilt": resolve_cxxfilt(),
        "objdump": resolve_objdump(),
        "python": resolve_python(),
    }


def _main() -> int:
    r = report()
    print("[toolchain] 配置文件:", r["config"] or "(缺失，使用内置默认值)")
    print("  g++     :", r["gpp"])
    print("  c++filt :", r["cxxfilt"] or "(未找到)")
    print("  objdump :", r["objdump"] or "(未找到)")
    print("  python  :", r["python"])
    ver = resolve_python_version()
    exp = expected_python()
    if ver is not None:
        print("  python@ :", ver, f"(期望 {exp}.x)" if exp else "")
    missing = [k for k in ("gpp", "cxxfilt", "objdump") if not r[k]]
    if missing:
        print(f"\n[toolchain] ⚠ 以下工具未解析到: {', '.join(missing)}")
        print(f"[toolchain]   请编辑 {CONFIG} 或把对应可执行文件加入 PATH。")
        return 1
    if exp and ver is not None and not ver.startswith(exp + "."):
        print(f"\n[toolchain] ⚠ Python 版本漂移：解析到 {ver}，配置期望 {exp}.x")
        print(f"[toolchain]   请修正 {CONFIG} 的 [python].prefer / expected，")
        print("[toolchain]   或重装托管解释器（避免 uv 拉到更高版本）。")
        return 1
    print("\n[toolchain] ✅ 全部解析成功")
    return 0


if __name__ == "__main__":
    # 放在 __main__ 内局部导入：toolchain 会被 cppbible/hy3_check 等反覆导入，
    # 没必要让它们都背一个只在「当脚本直接运行」时才用得上的依赖。
    from utf8_console import ensure_utf8

    # Windows 中文控制台（GBK）无法编码 ✅/⚠：本模块会在结论行打印它们。
    # 不做兜底时抛出的 UnicodeEncodeError 会以退出码 1 结束，与「检测到
    # 版本漂移」的退出码相同，极易被误读成自检失败——故先强制 UTF-8 输出。
    ensure_utf8()
    sys.exit(_main())
