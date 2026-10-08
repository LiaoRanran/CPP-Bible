#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""tools.utils.errors — 693-D3：统一异常层次。

设计原则
========
1. **不要用裸 ``SystemExit``/``ValueError`` 表达"数据不对"**。调用方无法区分
   "环境没装好"、"文件缺失"、"数据被改"、"口径不一致"这四类失败，
   于是只能一律打印"失败"，静默降级就在这里发生。
2. 每个异常都带 ``hint``：一条**可执行的**下一步命令或排查方向，直接进日志。
3. 层次扁平但语义明确，方便 ``except QueyiDataError`` 一把兜住"数据侧问题"。
"""
from __future__ import annotations


class QueyiError(Exception):
    """所有 Queyi 工具异常的基类。

    Attributes:
        message: 人可读的错误描述。
        hint: 一条**可执行**的下一步建议（命令或排查方向），允许为空。
    """

    def __init__(self, message: str, hint: str = "") -> None:
        super().__init__(message)
        self.message = message
        self.hint = hint

    def __str__(self) -> str:
        if self.hint:
            return f"{self.message}\n  → {self.hint}"
        return self.message


class QueyiDataError(QueyiError):
    """数据侧问题：文件缺失 / 校验和不符 / 字段缺失 / 口径不一致。

    **一律 fail-loud**：捕获方可以决定是否降级，但异常本身不允许静默吞掉。
    """


class DataMissingError(QueyiDataError):
    """权威产物文件不存在。

    典型 hint：``python tools/gen_693_manifest.py --check`` 看缺哪一项。
    """


class ChecksumMismatchError(QueyiDataError):
    """sha256 校验失配 ⇒ 冻结产物被改动。

    ⚠ 处置纪律：**不要**重新生成清单去"让它过"。先查清是谁改的、为什么改。
    """

    def __init__(self, path: str, expected: str, actual: str) -> None:
        super().__init__(
            f"sha256 失配：{path}（期望 {expected[:12]}…，实际 {actual[:12]}…）",
            hint="冻结产物不应被改动：先 git log 查该文件历史，再决定是否需要新批次产出新文件；"
                 "绝不要重新生成清单来掩盖",
        )
        self.path = path
        self.expected = expected
        self.actual = actual


class SchemaError(QueyiDataError):
    """结构/字段不符合预期（缺键、类型不对、必需字段为空）。"""


class EnvironmentError_(QueyiError):  # noqa: N818  （后缀避免与内置 OSError 别名混淆）
    """环境侧问题：编译器缺失、sanitizer 运行时不可用、WSL 横幅未规避。

    与数据侧错误分开，是为了让调用方能给出**不同的处置**：
    环境错可以换环境重跑，数据错必须停下来查。
    """

    def __init__(self, message: str, hint: str = "") -> None:
        super().__init__(message, hint or "bash scripts/verify_environment.sh --report")


class GateFailure(QueyiError):
    """门禁未通过（论文门禁 / 数据完整性 / 类型检查）。

    与 :class:`QueyiDataError` 的区别：门禁失败是**结论**，数据错误是**原因**。
    """
