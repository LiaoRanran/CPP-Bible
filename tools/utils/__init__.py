#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""tools.utils — 693-D1/D3：共用基础设施包（异常处理 / 日志 / 缓存数据访问）。

为什么现在才建这个包
====================
693-D1 的任务书要求"把 ``tools/`` 按功能分子目录"。**我们没有做这件事**，理由必须写明：

* ``tools/`` 下有 **716 个 .py**，其中大量脚本被 CI（`.github/workflows/ci.yml`）、
  ``conftest.py``、``tools/fast_gate.py``、``tools/tool_integrity.py`` 的**哈希面**
  以**字面路径**引用；
* 物理移动会让 34 条信任根哈希面全部失配、CI 十余个 job 直接变红，
  属于"优化动作本身制造了事故"，违背本项目"不静默降级、不出半成品"的红线；
* 收益（目录好看）远小于代价（信任根断裂 + 数十小时回归）。

因此 693-D1 采取**渐进方案**：新建 ``tools/utils/`` 作为**新增共用代码的唯一去处**，
并用 ``tools/README.md`` 给出**功能分类索引**（分类是标注出来的，不是靠目录猜的）。
未来的搬迁应逐个脚本做，且每搬一个都要同步更新哈希面引用。

包内容
======
* :mod:`tools.utils.errors`  —— 自定义异常层次（统一错误处理，693-D3）
* :mod:`tools.utils.logging_setup` —— 统一日志格式（693-D3）
* :mod:`tools.utils.data_access` —— 带缓存的大矩阵读取（693-D4）
"""
from __future__ import annotations

__all__ = ["errors", "logging_setup", "data_access"]
__version__ = "693-D1"
