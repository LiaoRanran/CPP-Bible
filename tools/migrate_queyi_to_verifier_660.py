#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""migrate_queyi_to_verifier_660.py — 660 B6：把 queyi_core_* 模块迁到 queyi-verifier。

做法：
  1. 把 CPP-Bible/tools/queyi_*.py + queyi_data_models_645.py 复制到
     queyi-verifier/tools/（canonical 副本，用 CPP-Bible 当前版覆盖，保证 canonical=最新）。
  2. 把 CPP-Bible 侧的同名文件改写为薄 wrapper：向上搜索 queyi-verifier/tools/<m>.py，
     用 importlib 直接加载并替换本模块在 sys.modules 的条目，使所有
     `import queyi_core_*` 的下游工具（conflict_detector_642 等）透明拿到 queyi-verifier 版本。
  3. 不碰 run_658_gate / status_reconciler / gate_engine（它们不依赖 queyi_core）。
"""
from __future__ import annotations

import os
import shutil
import sys

CPP = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# queyi-verifier 仓为固定布局：C:\CodeLearnling\queyi-verifier
QV = r"C:\CodeLearnling\queyi-verifier"
SRC_TOOLS = os.path.join(CPP, "tools")
DST_TOOLS = os.path.join(QV, "tools")

MODS = [
    "queyi_core_cpp_641",
    "queyi_core_interface_design_625",
    "queyi_core_interface_v02_631",
    "queyi_core_interface_v03_632",
    "queyi_core_toy_641",
    "queyi_core_trigger_check_625",
    "queyi_core_v10_641",
    "queyi_data_models_645",
]

WRAP = '''# 660 B6：canonical 已迁至 queyi-verifier/tools/{m}.py（本文件为薄 wrapper）。
import importlib.util, os, sys
_HERE = os.path.dirname(os.path.abspath(__file__))


def _find_qv_tools(m):
    d = _HERE
    for _ in range(8):
        cand = os.path.join(d, "queyi-verifier", "tools", m + ".py")
        if os.path.isfile(cand):
            return os.path.join(d, "queyi-verifier", "tools")
        d = os.path.dirname(d)
    return None


_QVT = _find_qv_tools("{m}")
if _QVT:
    if _QVT not in sys.path:
        sys.path.insert(0, _QVT)
    _spec = importlib.util.spec_from_file_location("_qv_{m}", os.path.join(_QVT, "{m}.py"))
    _mod = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_mod)
    sys.modules[__name__] = _mod
else:
    raise RuntimeError("queyi-verifier/tools not found for {m}（请确认 C:\\\\CodeLearnling\\\\queyi-verifier 已克隆）")
'''


def main() -> int:
    if not os.path.isdir(QV):
        print(f"[REFUSED] queyi-verifier 仓不存在：{QV}", file=sys.stderr)
        return 2
    os.makedirs(DST_TOOLS, exist_ok=True)
    for m in MODS:
        src = os.path.join(SRC_TOOLS, m + ".py")
        dst = os.path.join(DST_TOOLS, m + ".py")
        if not os.path.isfile(src):
            print("SKIP (missing)", src)
            continue
        shutil.copy2(src, dst)  # canonical 副本（用 CPP-Bible 当前版覆盖）
        with open(src, "w", encoding="utf-8") as f:
            f.write(WRAP.format(m=m))  # CPP-Bible 侧改写为 wrapper
        print("moved", m)
    print("DONE -> queyi-verifier/tools/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
