#!/usr/bin/env python3
"""640 A4 · 模块级 --check 守卫劫持审计（只读）

634 A2 给 79 个老工具在**模块级**插入了 `if "--check" in sys.argv: sys.exit(0)`
守卫。对**会被其他工具 import** 的工具，这是真 bug：import 时守卫看到的是
**外层进程**的 argv ⇒ 打印 OK 并 sys.exit(0)，劫持调用方
（实证：replay_invariants --check 被 toolchain 守卫劫持，640 A1-2 已修 toolchain）。

本审计列出：守卫工具总数、其中被其他 tools/*.py import 的（劫持风险面）。
"""
from __future__ import annotations

import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
GUARD = re.compile(r'^if "--check" in sys\.argv:', re.MULTILINE)
IMP = re.compile(r'import\s+(\w+)|from\s+(\w+)\s+import')


def main() -> dict:
    tools = [f for f in sorted(os.listdir(HERE))
             if f.endswith(".py") and f != "__init__.py"]
    guarded = []
    for f in tools:
        src = open(os.path.join(HERE, f), encoding="utf-8", errors="replace").read()
        m = GUARD.search(src)
        if not m:
            continue
        main_pos = src.find('__main__')
        guarded.append({"tool": f, "module_level": main_pos == -1 or m.start() < main_pos})
    names = {g["tool"][:-3] for g in guarded}
    risk: dict[str, int] = {g["tool"]: 0 for g in guarded if g["module_level"]}
    for f in tools:
        src = open(os.path.join(HERE, f), encoding="utf-8", errors="replace").read()
        mods = {a or b for a, b in IMP.findall(src)}
        for n in mods & names:
            key = n + ".py"
            if key in risk and f != key:
                risk[key] += 1
    return {"total_tools": len(tools), "guarded": len(guarded),
            "module_level": sum(1 for g in guarded if g["module_level"]),
            "hijack_risk": sorted((k, v) for k, v in risk.items() if v > 0),
            "guarded_list": [g["tool"] for g in guarded]}


if __name__ == "__main__":
    r = main()
    print(json.dumps(r, ensure_ascii=False, indent=1))
