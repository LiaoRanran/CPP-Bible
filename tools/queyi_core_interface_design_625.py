# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
# 660 B6：canonical 已迁至 queyi-verifier/tools/queyi_core_interface_design_625.py（本文件为薄 wrapper）。
"""queyi_core_interface_design_625 — 666 薄 wrapper：canonical 在 `queyi-verifier/tools/`。

**目标**：让 CPP-Bible 侧 25 个工具/测试继续 `import queyi_core_interface_design_625` 而不必复制实现
（单一实现、两处入口）。运行期向上逐级找 `queyi-verifier/tools/<同名文件>`，
用 importlib 载入后把 `sys.modules[__name__]` 换成它 —— 因此 `import queyi_core_interface_design_625`
拿到的就是 canonical 模块**本身**，属性与行为逐字不变。

**数据源**：`queyi-verifier/tools/queyi_core_interface_design_625.py`（660 B6 拆仓后的 canonical）。
本文件不含任何实现，既不是副本、也不是代理实现。

**边界（只读）**：不写任何产物、不改语料；找不到 canonical 文件时 **fail-loud**
（`raise RuntimeError`），绝不静默退化 —— 静默退化会让"内核缺失"看起来像"内核正常"。
静态分析：见下方 `TYPE_CHECKING` 里 PEP 562 的 `__getattr__` 声明（属性由运行期提供）。
"""
from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:  # 666 A1：静态分析的「动态模块」声明（运行期不执行）
    # 本文件运行期会把 sys.modules[__name__] 换成 canonical 模块（见文件末尾），
    # 静态分析看不到那一步 ⇒ 用 PEP 562 的模块级 __getattr__ 声明「属性由运行期提供」，
    # 使使用方按 Any 处理（否则 CPP-Bible 侧 25 个工具报 67 条 Module has no attribute）。
    def __getattr__(name: str) -> Any: ...

import importlib.util
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))


def _find_qv_tools(m):
    d = _HERE
    for _ in range(8):
        cand = os.path.join(d, "queyi-verifier", "tools", m + ".py")
        if os.path.isfile(cand):
            return os.path.join(d, "queyi-verifier", "tools")
        d = os.path.dirname(d)
    return None


_QVT = _find_qv_tools("queyi_core_interface_design_625")
if _QVT:
    if _QVT not in sys.path:
        sys.path.insert(0, _QVT)
    _spec = importlib.util.spec_from_file_location("_qv_queyi_core_interface_design_625", os.path.join(_QVT, "queyi_core_interface_design_625.py"))
    assert _spec is not None and _spec.loader is not None
    _mod = importlib.util.module_from_spec(_spec)
    sys.modules["_qv_queyi_core_interface_design_625"] = _mod  # 注册后再 exec，避免 dataclass _is_type 查 sys.modules 得 None
    _spec.loader.exec_module(_mod)
    sys.modules[__name__] = _mod
else:
    raise RuntimeError("queyi-verifier/tools not found for queyi_core_interface_design_625")
