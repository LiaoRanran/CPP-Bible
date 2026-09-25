"""640 A4 · 守卫劫持修复验证（≥6 例）。

病（634 A2 引入）：79 个工具的模块级 `if "--check" in sys.argv: sys.exit(0)` 守卫，
在**被其他工具 import** 时看到外层进程 argv ⇒ 劫持调用方（实证：replay_invariants
--check 被 toolchain 守卫 exit(0)）。
修：8 个有劫持风险的工具守卫移入 `__main__`。
"""
from __future__ import annotations

import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
TOOLS = os.path.join(ROOT, "tools")
sys.path.insert(0, TOOLS)

RISKY = ["chapter_compile_check", "compile_all", "impact_analysis", "mutation_fuzz",
         "overturned_events", "prop_closure", "prop_graph", "stat_bounds"]


def _import_with_check_argv(mod: str) -> str:
    """在 argv 含 --check 的子进程里 import 模块 ⇒ 若仍被守卫劫持则无 IMPORT_OK。"""
    code = (f"import sys; sys.argv.append('--check'); "
            f"sys.path.insert(0, r'{TOOLS}'); import {mod}; print('IMPORT_OK')")
    p = subprocess.run([sys.executable, "-c", code], capture_output=True,
                       text=True, cwd=ROOT, timeout=120)
    return p.stdout + p.stderr


def test_no_module_level_guard_left_in_risky_tools():
    import re
    for mod in RISKY:
        src = open(os.path.join(TOOLS, mod + ".py"), encoding="utf-8").read()
        m = re.search(r'if "--check" in sys\.argv:', src)
        assert m is None or src.find("__main__") != -1 and m.start() > src.find("__main__"), mod


def test_import_with_check_argv_not_hijacked():
    for mod in RISKY:
        out = _import_with_check_argv(mod)
        assert "IMPORT_OK" in out, f"{mod} 仍被守卫劫持：{out[-200:]}"


def test_direct_check_still_exits_zero():
    for mod in ("toolchain", "prop_graph", "stat_bounds"):
        p = subprocess.run([sys.executable, os.path.join(TOOLS, mod + ".py"), "--check"],
                           capture_output=True, text=True, cwd=ROOT, timeout=120)
        assert p.returncode == 0, (mod, p.stdout[-200:], p.stderr[-200:])
        assert "OK:" in p.stdout, (mod, p.stdout[-120:])


def test_replay_invariants_check_runs_real_invariants():
    p = subprocess.run([sys.executable, os.path.join(TOOLS, "replay_invariants.py"),
                        "--check", "--no-heavy"],
                       capture_output=True, text=True, cwd=ROOT, timeout=300)
    assert p.returncode == 0
    assert "全部通过" in p.stdout, p.stdout[-300:]
    assert "加载即校验" not in p.stdout, "仍被 toolchain 守卫劫持"
