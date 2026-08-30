#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""utf8_console.py — Windows 中文控制台（GBK）下的 UTF-8 输出兜底。

为什么收敛到一处
================
原先 `tools/` 下有 8 个脚本各写一份 `try: sys.stdout.reconfigure(...)`
（有的再叠 `hasattr` 或 `# type: ignore`）。三处代价：

1. 重复；
2. `sys.stdout` 的类型是 `TextIO | Any`，而 `reconfigure()` 只存在于
   `io.TextIOWrapper`，故每处都让 mypy 报 `attr-defined`（实测 9 处）；
3. 有的站点漏了 stderr（`cppbible.py` 之外的多数只处理 stdout），行为不一致。

用法
====
    from utf8_console import ensure_utf8
    ensure_utf8()

以 `python tools/xxx.py` 直接运行时，Python 会把脚本所在目录加入
`sys.path[0]`，故同目录模块可直接导入，无需手工 sys.path 处理。
"""
from __future__ import annotations

import io
import sys


def ensure_utf8() -> None:
    """把 stdout/stderr 重配为 UTF-8（无法编码的字符替换而非抛错）。

    用 `isinstance` 收窄而非 `try/except` 或 `hasattr`：既让类型检查通过，
    也明确表达「只对真实的 TextIOWrapper 流生效」。若 stdout 被 pytest /
    IDE 等替换成非 TextIOWrapper 对象，静默跳过（仅影响显示，不影响门禁）。
    """
    for stream in (sys.stdout, sys.stderr):
        if isinstance(stream, io.TextIOWrapper):
            stream.reconfigure(encoding="utf-8", errors="replace")
