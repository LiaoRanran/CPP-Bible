#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""queyi_common.py — 696 批次：工程线公共库（异常 / 日志 / 文件纯函数）。

定位（与 ``tools/utils/`` 的关系）
==================================
本仓 693-D1 已建 ``tools/utils/`` 共用基础设施包（``errors`` / ``logging_setup`` /
``data_access``）。本模块是 **696 批次的独立、零依赖公共库**，刻意**不 import** ``utils.*``：

* 不引入 ``sys.path`` 耦合 —— 本模块既可被 ``sys.path.insert(0, 'tools')`` 后的脚本
  直接 ``import queyi_common``，也可被当作单文件复制到别处使用；
* 只依赖**标准库**，不依赖仓库任何既有模块，便于单测与静态检查（ruff / mypy 双绿）。

因此它与 ``utils/`` 是**并列**关系：新代码若已在 ``utils/`` 生态内，优先复用 ``utils/``；
若需要一个"自带电池、无路径耦合"的公共库，用本模块。二者语义一致（异常层次、日志格式
统一），但不互相依赖。

设计纪律
========
1. **不造裸 ``ValueError`` / ``SystemExit`` 表达"数据不对"** —— 用带 ``hint`` 的异常层次，
   让调用方能区分"门禁未过 / 数据被改 / 结构不符"三类失败。
2. **纯函数无副作用**（``read_json`` / ``sha256_file``）便于测试与复用；
   唯一的落盘函数 ``atomic_write_text`` 保证**要么写全、要么原文件不动**。
3. **类型注解 + docstring 全覆盖**，作为本批新增代码的静态检查基线。

诚实边界
========
``atomic_write_text`` 的原子性是**同目录临时文件 + ``os.replace``** 级别的
（POSIX 原子替换语义）；它**不是**断电/崩溃一致性保证，也不做 fsync。
"""
from __future__ import annotations

import hashlib
import json
import logging
import os
import sys
import tempfile
from pathlib import Path
from typing import Any

__all__ = [
    "QueyiError",
    "GateError",
    "DataIntegrityError",
    "SchemaError",
    "setup_logging",
    "read_json",
    "sha256_file",
    "atomic_write_text",
]

#: 统一日志格式：``HH:MM:SS LEVEL name | message``
_LOG_FORMAT: str = "%(asctime)s %(levelname)-7s %(name)s | %(message)s"
_LOG_DATEFMT: str = "%H:%M:%S"

#: 读文件时的默认分块大小（64 KiB），兼顾内存与系统调用次数
_CHUNK_SIZE: int = 1 << 16


# ── 异常层次 ────────────────────────────────────────────────────────────────
class QueyiError(Exception):
    """所有 Queyi 工具异常的基类。

    Attributes:
        message: 人可读的错误描述。
        hint: 一条**可执行**的下一步建议（命令或排查方向），允许为空。
    """

    def __init__(self, message: str, hint: str = "") -> None:
        super().__init__(message)
        self.message: str = message
        self.hint: str = hint

    def __str__(self) -> str:
        if self.hint:
            return f"{self.message}\n  → {self.hint}"
        return self.message


class GateError(QueyiError):
    """门禁未通过（一致性 / 编译 / 数字对账等判定失败）。

    与 :class:`DataIntegrityError` 的区别：门禁失败是**结论**，数据错误是**原因**。
    """


class DataIntegrityError(QueyiError):
    """数据侧问题：文件缺失 / 读取失败 / 校验和不符。

    **一律 fail-loud**：捕获方可决定是否降级，但异常本身不允许被静默吞掉。
    """


class SchemaError(DataIntegrityError):
    """结构/字段不符合预期（非法 JSON、顶层不是对象、必需字段缺失）。

    继承 :class:`DataIntegrityError`：它同样属于"数据不对"，但语义更细，
    便于调用方 ``except SchemaError`` 单独处理结构问题。
    """


# ── 日志 ────────────────────────────────────────────────────────────────────
class _QueyiStreamHandler(logging.StreamHandler):
    """带标记的 stderr handler，便于 :func:`setup_logging` **幂等**地移除旧配置。

    用子类而非给 handler 挂属性：属性写法需要 ``# type: ignore``，会污染静态检查；
    子类让"哪些 handler 是我们装的"变成一次 ``isinstance`` 判断。
    """


def _coerce_level(level: int | str) -> int:
    """把 ``int | str`` 级别归一为 ``logging`` 整数级别。

    Args:
        level: 整数级别，或 ``"DEBUG"/"INFO"/"WARNING"/"ERROR"/"CRITICAL"``（大小写不限）。

    Returns:
        对应的整数级别；字符串无法识别时回落 :data:`logging.INFO`。
    """
    if isinstance(level, int):
        return level
    resolved = logging.getLevelName(level.strip().upper())
    return resolved if isinstance(resolved, int) else logging.INFO


def setup_logging(level: int | str = logging.INFO) -> logging.Logger:
    """配置根 logger 的统一格式（**幂等**）。

    行为：
      * 移除本函数**先前**添加的 handler（``_QueyiStreamHandler``），再加一个新的
        ⇒ 多次调用不会重复打印；
      * 保留调用方自己添加的 handler（不 ``basicConfig``、不 ``clear`` 根 handlers）；
      * 设置根 logger 级别。

    Args:
        level: 日志级别，``int`` 或级别名（见 :func:`_coerce_level`）。

    Returns:
        已配置的根 :class:`logging.Logger`。
    """
    root = logging.getLogger()
    for handler in list(root.handlers):
        if isinstance(handler, _QueyiStreamHandler):
            root.removeHandler(handler)
    handler = _QueyiStreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(_LOG_FORMAT, datefmt=_LOG_DATEFMT))
    root.addHandler(handler)
    root.setLevel(_coerce_level(level))
    return root


# ── 文件纯函数 ──────────────────────────────────────────────────────────────
def read_json(path: str | os.PathLike[str]) -> dict[str, Any]:
    """读取并解析一个 JSON 对象文件。

    Args:
        path: JSON 文件路径。

    Returns:
        解析后的 ``dict``（顶层必须是 JSON 对象）。

    Raises:
        DataIntegrityError: 文件不存在或读取失败（IO 层）。
        SchemaError: 内容不是合法 JSON，或顶层不是对象。
    """
    p = Path(path)
    try:
        text = p.read_text(encoding="utf-8")
    except OSError as exc:
        raise DataIntegrityError(
            f"无法读取文件：{p}（{type(exc).__name__}: {exc}）",
            hint="确认路径存在且可读；产物缺失时先跑对应的生成脚本",
        ) from exc
    try:
        data: Any = json.loads(text)
    except json.JSONDecodeError as exc:
        raise SchemaError(
            f"非法 JSON：{p}（第 {exc.lineno} 行第 {exc.colno} 列：{exc.msg}）",
            hint="检查文件是否被截断/写入半途；重新生成该产物",
        ) from exc
    if not isinstance(data, dict):
        raise SchemaError(
            f"JSON 顶层不是对象：{p}（实际 {type(data).__name__}）",
            hint="本库只接受顶层为 JSON object 的文件；数组请改用 json.loads 自行处理",
        )
    return data


def sha256_file(path: str | os.PathLike[str]) -> str:
    """计算文件内容的 sha256（十六进制小写）。

    分块读取，避免大文件一次性读入内存。

    Args:
        path: 文件路径。

    Returns:
        64 位十六进制 sha256 字符串。

    Raises:
        DataIntegrityError: 文件不存在或读取失败。
    """
    p = Path(path)
    digest = hashlib.sha256()
    try:
        with p.open("rb") as fh:
            for chunk in iter(lambda: fh.read(_CHUNK_SIZE), b""):
                digest.update(chunk)
    except OSError as exc:
        raise DataIntegrityError(
            f"无法读取文件以计算 sha256：{p}（{type(exc).__name__}: {exc}）",
            hint="确认文件存在；冻结产物缺失时先跑 gen_693_manifest.py --check 看缺哪一项",
        ) from exc
    return digest.hexdigest()


def atomic_write_text(
    path: str | os.PathLike[str],
    text: str,
    encoding: str = "utf-8",
) -> Path:
    """原子地写入文本文件（同目录临时文件 + ``os.replace``）。

    语义：**要么新内容完整落盘，要么原文件保持不变**。不会出现"写了一半"的中间态，
    适合写清单/报告这类可被下游读取的产物。

    Args:
        path: 目标文件路径；父目录须已存在。
        text: 要写入的文本。
        encoding: 文本编码，默认 UTF-8。

    Returns:
        目标文件路径（:class:`pathlib.Path`）。

    Raises:
        OSError: 目标目录不可写、磁盘满等系统级失败。
    """
    p = Path(path)
    directory = p.parent
    fd, tmp_name = tempfile.mkstemp(
        prefix=f".{p.name}.", suffix=".tmp", dir=str(directory)
    )
    tmp_path = Path(tmp_name)
    try:
        with os.fdopen(fd, "w", encoding=encoding, newline="\n") as fh:
            fh.write(text)
        os.replace(tmp_path, p)
    except BaseException:
        # 失败时清掉临时文件，避免在目录里留下 .tmp 残骸
        try:
            tmp_path.unlink()
        except OSError:
            pass
        raise
    return p


if __name__ == "__main__":
    setup_logging()
    logging.getLogger("queyi_common").info(
        "queyi_common 公共库自检：异常层次 / setup_logging / read_json / "
        "sha256_file / atomic_write_text 已就绪"
    )
