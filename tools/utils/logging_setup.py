#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""tools.utils.logging_setup — 693-D3：统一日志格式。

为什么需要
==========
``tools/`` 下 716 个脚本的进度输出格式各异：有的 ``print("[x] …")``，有的裸 print，
有的什么都不打。这导致**复现时看不出卡在哪一步**，也让 CI 日志无法机器解析。

本模块给出一个**零依赖、零副作用**的 ``get_logger()``：

* 格式统一为 ``<ISO时间> <LEVEL> <工具名> <消息>``；
* 默认**不**给根 logger 加 handler（避免污染调用方配置）；
* ``--verbose`` 之类的开关由调用方决定，本模块不猜。

用法
====
    from utils.logging_setup import get_logger   # tools/ 在 sys.path 时

    log = get_logger("annotate_693_b")
    log.info("已分析 %d 条", n)
"""
from __future__ import annotations

import logging
import os
import sys
from typing import Final

_FORMAT: Final[str] = "%(asctime)s %(levelname)-7s %(name)s | %(message)s"
_DATEFMT: Final[str] = "%H:%M:%S"

# 环境变量开关：QUEYI_LOG_LEVEL=DEBUG 可临时提级，不改代码
_ENV_LEVEL: Final[str] = "QUEYI_LOG_LEVEL"
_DEFAULT_LEVEL: Final[int] = logging.INFO

_configured: bool = False


def _configure_root_once() -> None:
    """给根 logger 装一个 stderr handler（只做一次，幂等）。

    只在**没有**任何 handler 时才装，避免与 pytest / CI 的日志配置打架。
    """
    global _configured
    if _configured:
        return
    root = logging.getLogger()
    if not root.handlers:
        handler = logging.StreamHandler(sys.stderr)
        handler.setFormatter(logging.Formatter(_FORMAT, datefmt=_DATEFMT))
        root.addHandler(handler)
        root.setLevel(_DEFAULT_LEVEL)
    _configured = True


def get_logger(name: str, level: int | None = None) -> logging.Logger:
    """取得一个格式统一的 logger。

    Args:
        name: 工具名，建议用脚本文件名（去 ``.py``）。
        level: 显式级别；为 ``None`` 时读 ``QUEYI_LOG_LEVEL`` 环境变量，
            再回落 :data:`_DEFAULT_LEVEL`。

    Returns:
        已配置好传播链的 :class:`logging.Logger`。
    """
    _configure_root_once()
    log = logging.getLogger(name)
    if level is None:
        env = os.environ.get(_ENV_LEVEL, "").strip().upper()
        level = getattr(logging, env, _DEFAULT_LEVEL) if env else _DEFAULT_LEVEL
    log.setLevel(level)
    return log
