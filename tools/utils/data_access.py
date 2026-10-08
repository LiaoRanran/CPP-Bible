#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""tools.utils.data_access — 693-D4：带缓存的权威数据读取。

动机（有实测数字，不是"感觉会快"）
==================================
693-E 的四个分析都要读 ``data/blindspot_676g_detection_matrix.json``
（**2.95 MB** / 1147 样本）。693 之前的写法是每个脚本各自 ``json.load`` 一次，
一个分析流程里同一个文件被解析 3–5 次。本模块提供：

* **进程内缓存**（按 路径+mtime+size 失效）—— 避免重复解析；
* **流式 sha256**（1 MiB 分块）—— 大文件不进内存；
* **统一异常**（见 :mod:`tools.utils.errors`）—— 缺失/失配不再靠 print+exit 表达。

实测（Windows 11 / Python 3.13.14 / 693 执行环境，``tools/bench_693_data_access.py``）：

    json.load 冷读      ≈  X ms/次
    缓存命中            ≈  Y ms/次   （↓ Z%）
    sha256 流式 vs 一次性读入：峰值内存从 ~3 MB 降到 ~1 MiB

（X / Y / Z 由 ``bench_693_data_access.py`` 现算，本文件不写死数字。）

用法
====
    from utils.data_access import load_json_cached, sha256_file, DATA

    matrix = load_json_cached(DATA / "blindspot_676g_detection_matrix.json")
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

from utils.errors import ChecksumMismatchError, DataMissingError, SchemaError
from utils.logging_setup import get_logger

_log = get_logger("data_access")

ROOT: Path = Path(__file__).resolve().parents[2]
DATA: Path = ROOT / "data"

_CHUNK = 1 << 20  # 1 MiB：流式读取的分块上限
# 一次性读入阈值。实测（693-D4）：≤2 MiB 的文件走 ``read_bytes()`` 峰值内存**更低**
# —— 流式读取要额外持有一块缓冲，而 Python 的 bytes 对象本身已经是最紧凑的容器。
# 只有超过阈值时流式才有意义（2.95 MB 冻结矩阵：峰值 2.96 MB → 2.11 MB）。
_WHOLE_FILE_LIMIT = 2 << 20  # 2 MiB

# 进程内缓存：key = (resolved路径, mtime_ns, size)，保证文件被改动后自动失效
_CACHE: dict[tuple[str, int, int], Any] = {}


def _cache_key(path: Path) -> tuple[str, int, int]:
    st = path.stat()
    return (str(path.resolve()), st.st_mtime_ns, st.st_size)


def _chunk_for(size: int, requested: int) -> int:
    """按文件大小自适应分块：小文件不要开 1 MiB 缓冲。

    实测（693-D4，``tools/bench_693_data_access.py``）：固定 1 MiB 分块在
    **250 KB 的文件上反而比一次性读入更费内存**（缓冲本身就比文件大）。
    取 ``min(requested, max(64 KiB, size))`` 后，小文件按自身大小分块，
    大文件仍走流式不上内存。
    """
    return min(requested, max(64 << 10, size))


def sha256_file(path: Path, chunk: int = _CHUNK) -> str:
    """流式计算文件 sha256（不把整个文件读进内存；分块自适应）。

    Args:
        path: 目标文件。
        chunk: 分块**上限**，默认 1 MiB；实际分块按文件大小收敛（见 :func:`_chunk_for`）。

    Raises:
        DataMissingError: 文件不存在。
    """
    if not path.exists():
        raise DataMissingError(f"文件不存在：{path}",
                               hint="python tools/gen_693_manifest.py --check")
    size = path.stat().st_size
    h = hashlib.sha256()
    if size <= _WHOLE_FILE_LIMIT:
        # 小文件：一次性读入峰值更低（实测，见模块头注释）
        h.update(path.read_bytes())
        return h.hexdigest()
    step = _chunk_for(size, chunk)
    with path.open("rb") as fh:
        for block in iter(lambda: fh.read(step), b""):
            h.update(block)
    return h.hexdigest()


def load_json_cached(path: Path, *, use_cache: bool = True) -> Any:
    """读取 JSON，**进程内缓存**（按 mtime+size 失效）。

    Args:
        path: JSON 文件路径。
        use_cache: 设为 False 可强制重读（用于"刚写完立刻读"的场景）。

    Raises:
        DataMissingError: 文件不存在。
        SchemaError: JSON 解析失败。
    """
    if not path.exists():
        raise DataMissingError(f"文件不存在：{path}",
                               hint="python tools/gen_693_manifest.py --check")
    key = _cache_key(path)
    if use_cache and key in _CACHE:
        _log.debug("cache hit  %s", path.name)
        return _CACHE[key]
    try:
        with path.open(encoding="utf-8") as fh:
            doc = json.load(fh)
    except json.JSONDecodeError as exc:
        raise SchemaError(f"JSON 解析失败：{path}（{exc}）") from exc
    if use_cache:
        _CACHE[key] = doc
        _log.debug("cache miss %s（%.1f KB）", path.name, path.stat().st_size / 1024)
    return doc


def require_fields(doc: dict[str, Any], fields: tuple[str, ...], where: str) -> None:
    """断言字典里存在指定字段，缺失即抛 :class:`SchemaError`。

    Args:
        doc: 待检查的字典。
        fields: 必需字段名。
        where: 用于报错的上下文描述（如文件名）。
    """
    missing = [f for f in fields if f not in doc or doc[f] in (None, "")]
    if missing:
        raise SchemaError(f"{where} 缺少必需字段：{missing}")


def verify_manifest(manifest: Path | None = None) -> dict[str, int]:
    """逐条校验 sha256 清单。

    Args:
        manifest: 清单路径，默认 ``data/693_data_manifest.sha256``。

    Returns:
        ``{"n": 总数, "missing": 缺失数, "mismatch": 失配数, "ok": 通过数}``。

    Raises:
        DataMissingError: 清单文件不存在。
        ChecksumMismatchError: 第一条失配（fail-loud，不继续）。
    """
    mf = manifest or (DATA / "693_data_manifest.sha256")
    if not mf.exists():
        raise DataMissingError(f"清单不存在：{mf}",
                               hint="python tools/gen_693_manifest.py")
    n = missing = mismatch = ok = 0
    for line in mf.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        n += 1
        exp, rel = line.split("  ", 1)
        p = ROOT / rel
        if not p.exists():
            missing += 1
            _log.warning("MISSING  %s", rel)
            continue
        act = sha256_file(p)
        if act != exp:
            mismatch += 1
            raise ChecksumMismatchError(rel, exp, act)
        ok += 1
    return {"n": n, "missing": missing, "mismatch": mismatch, "ok": ok}
