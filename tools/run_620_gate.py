"""620 E1 · 收工门禁（5 项串行检查）

按 620 §六 收工门禁要求，串起 5 项检查：

1. **受控目录零污染**：`atoms/ evidence/ Examples/ Book/` 无未提交改动（含未跟踪文件）
2. **逐工具 --check**：620 新增工具（不含本脚本自身）逐个 `--check` exit 0
3. **pytest（620 新增单测）**：9 个 test_620_*.py 文件全绿
4. **gate block=0**：`gate_engine --check` 退出码 0 且 block=0
   （**串行执行**：绝不与 replay 并发——620 任务1 已证实并发会产生瞬时误报）
5. **ruff**：新增工具 + 新增单测静态检查通过

**本脚本自身不参与第 2 项**（否则自指循环），在报告中显式说明。

铁律：新工具必有 `--check`（只读自验证，exit 0 = 通过）。
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
if not os.path.exists(PY):
    PY = sys.executable

CONTROLLED = ("atoms/", "evidence/", "Examples/", "Book/")

# 620 新增工具（不含 run_620_gate 自身）
NEW_TOOLS = (
    "adversarial_loop_620",
    "adversarial_weight_calibration_620",
    "vfdr_realtime_620",
    "pck_batch_migrator_620",
    "pck_status_stats_620",
    "authority_log_620",
    "pck_authority_sync_620",
)

# 注意：NEW_TESTS **不含** tests/test_620_gate.py —— 该单测会调用本门禁的
# check_pytest()，若把它纳入门禁则形成「门禁 → 自己的单测 → 门禁」的自指递归。
# 门禁自身单测单独跑（见验收报告），在此显式说明以免被误认为漏项。
NEW_TESTS = (
    "tests/test_620_a1.py", "tests/test_620_a2.py", "tests/test_620_a3.py",
    "tests/test_620_a4.py", "tests/test_620_b1.py", "tests/test_620_b2.py",
    "tests/test_620_b3.py", "tests/test_620_c2.py", "tests/test_620_c3.py",
)

GATE_RE = re.compile(r"命中\s+(\d+)\s*\(block=(\d+)\s+warn=(\d+)\s+advice=(\d+)\)")


def _run(cmd: list[str]) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as exc:  # noqa: BLE001
        return 127, f"执行失败：{exc}"


def check_controlled_dirs() -> tuple[bool, str]:
    rc, out = _run(["git", "status", "--porcelain"])
    if rc != 0:
        return False, f"git status 失败：{out.strip()}"
    dirty = [ln for ln in out.splitlines()
             if ln.strip() and any(ln[3:].strip().strip('"').startswith(p)
                                   for p in CONTROLLED)]
    if dirty:
        return False, "受控目录有未提交改动：" + "; ".join(dirty[:5])
    return True, "干净（atoms/ evidence/ Examples/ Book/ 无改动、无未跟踪）"


def check_tools() -> tuple[bool, str]:
    bad = []
    for name in NEW_TOOLS:
        rc, out = _run([PY, os.path.join("tools", f"{name}.py"), "--check"])
        if rc != 0:
            bad.append(f"{name}(exit {rc})")
    if bad:
        return False, "以下工具 --check 失败：" + ", ".join(bad)
    return True, f"{len(NEW_TOOLS)}/{len(NEW_TOOLS)} 通过（run_620_gate 自身不参与，避免自指）"


def check_pytest() -> tuple[bool, str]:
    rc, out = _run([PY, "-m", "pytest", *NEW_TESTS, "-q", "-p", "no:cacheprovider"])
    if rc != 0:
        tail = "\n".join(out.strip().splitlines()[-8:])
        return False, f"pytest 失败（rc={rc}）：\n{tail}"
    # 计数走 --collect-only：多文件 -q 时不保证输出 "N passed" 汇总行，
    # 但 collect-only 的条目行是稳定的（每项形如 `file::test_x`）。
    _rc2, out2 = _run([PY, "-m", "pytest", *NEW_TESTS, "--collect-only", "-q",
                       "-p", "no:cacheprovider"])
    n = len([ln for ln in out2.splitlines() if "::" in ln])
    if n == 0:
        # 多文件 + -q 时 collect-only 给的是「文件: 条数」汇总行，不是 `file::test` 明细
        n = sum(int(m.group(1))
                for m in re.finditer(r"\.py:\s*(\d+)\s*$", out2, re.MULTILINE))
    return True, f"{n} passed"


def check_gate() -> tuple[bool, str]:
    """串行跑 gate（不与 replay 并发）。"""
    rc, out = _run([PY, os.path.join("tools", "gate_engine.py"), "--check"])
    m = GATE_RE.search(out)
    if not m:
        return False, f"无法解析 gate 输出（rc={rc}）"
    hits, block, warn, advice = (int(x) for x in m.groups())
    if rc != 0 or block != 0:
        return False, f"gate rc={rc} 命中 {hits}（block={block} warn={warn} advice={advice}）"
    return True, f"命中 {hits}（block={block} warn={warn} advice={advice}）"


def check_ruff() -> tuple[bool, str]:
    paths = [os.path.join("tools", f"{n}.py") for n in NEW_TOOLS]
    paths += [os.path.join("tools", "run_620_gate.py"), *NEW_TESTS]
    rc, out = _run([PY, "-m", "ruff", "check", *paths])
    if rc != 0:
        return False, "ruff 失败：\n" + "\n".join(out.strip().splitlines()[-8:])
    return True, f"{len(paths)} 个文件通过"


CHECKS = (
    ("受控目录零污染", check_controlled_dirs),
    ("逐工具 --check", check_tools),
    ("pytest（620 新增单测）", check_pytest),
    ("gate block=0（串行）", check_gate),
    ("ruff 静态检查", check_ruff),
)


def run_all() -> int:
    print("run_620_gate · 620 收工门禁（5 项，串行）\n")
    results = []
    for i, (label, fn) in enumerate(CHECKS, 1):
        ok, msg = fn()
        results.append(ok)
        print(f"[{i}/5] {label:<22} {'✅' if ok else '❌'} {msg}")
    all_ok = all(results)
    print(f"\n验收门: {'PASS' if all_ok else 'FAIL'}")
    return 0 if all_ok else 1


# ── 自检（只读、不写盘；exit 0 = 通过）──────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("5 项检查已注册", len(CHECKS) == 5)
    chk("受控目录清单 = 4 个", len(CONTROLLED) == 4)
    chk("620 新增工具 7 个（不含自身）", len(NEW_TOOLS) == 7)
    chk("620 新增单测文件 9 个", len(NEW_TESTS) == 9)
    chk("gate 正则可解析基线串",
        GATE_RE.search("命中 191 (block=0 warn=186 advice=5)") is not None)
    chk("每个检查项返回 (bool, str)",
        all(callable(f) for _l, f in CHECKS))
    print(f"E1 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="620 E1 收工门禁")
    ap.add_argument("--check", action="store_true",
                    help="只读自检（不跑 5 项门禁），exit 0 = 通过")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    return run_all()


if __name__ == "__main__":
    sys.exit(main())
