"""619 D1 · 收工门禁（受控目录零污染 + 逐工具 --check + pytest）

619 批次的本地收工门禁。**不跑监工门禁**（gate/poison/replay/tool_integrity 的 --check），
与 619 §六 硬边界 2 一致——只验证本批次产物自身：受控目录零污染、619 新工具 --check 全绿、619 新增单测全绿。

铁律：新工具必有 `--check`（只读自验证，exit 0）。
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 受控目录 / 文件（619 §六 硬边界 1）：任何修改都算污染
CONTROLLED_PATHS = [
    "atoms", "evidence", "Examples", "Book",
    "tools/gate_engine.py", "tools/atom_evidence_replay.py", "tools/poison_drill.py",
    "tools/toolchain.py", "tools/cppbible.py", "golden_lock.py", "tools/mutation_fuzz.py",
]

# 619 新建 / 改动的工具（逐 --check）
CHECK_TOOLS = [
    "adversarial_objective_619.py",
    "adversarial_attacker_619.py",
    "vfdr_619.py",
    "pck_certificate_verifier_619.py",
    "pck_pilot_generator_619.py",
    "pck_renderer_619.py",
    "snapshot_manifest.py",  # C1 改动（非 CORE/钉扎面）
]

# 619 新增单测
GATE_TESTS = [
    "tests/test_619_a1.py", "tests/test_619_a2.py", "tests/test_619_a3.py",
    "tests/test_619_b2.py", "tests/test_619_b3.py", "tests/test_619_b4.py",
    "tests/test_snapshot_manifest.py",  # C1 改动的工具，回归保护
    "tests/test_619_gate.py",           # 门禁自身测试（含 monkeypatch 恢复回归）
]


def check_controlled_clean() -> tuple[bool, str]:
    """受控目录/文件相对 HEAD 必须零污染（git status --short）。"""
    res = subprocess.run(["git", "status", "--short", "--"] + CONTROLLED_PATHS,
                         cwd=ROOT, capture_output=True, text=True)
    dirty = [ln for ln in res.stdout.splitlines() if ln.strip()]
    return (len(dirty) == 0, "\n".join(dirty))


def run_tool_checks() -> tuple[bool, dict[str, int]]:
    results: dict[str, int] = {}
    ok = True
    for tool in CHECK_TOOLS:
        path = os.path.join(ROOT, "tools", tool)
        if not os.path.exists(path):
            results[tool] = -1
            ok = False
            continue
        r = subprocess.run([sys.executable, path, "--check"], cwd=ROOT,
                           capture_output=True, text=True)
        results[tool] = r.returncode
        if r.returncode != 0:
            ok = False
            print(f"  [FAIL] {tool} --check (exit {r.returncode})")
            print(r.stdout + r.stderr)
        else:
            print(f"  [ok] {tool} --check")
    return ok, results


def run_tests() -> tuple[bool, int]:
    present = [t for t in GATE_TESTS if os.path.exists(os.path.join(ROOT, t))]
    r = subprocess.run([sys.executable, "-m", "pytest", "-q"] + present,
                       cwd=ROOT, capture_output=True, text=True)
    print(r.stdout)
    if r.returncode != 0:
        print(r.stderr)
    return (r.returncode == 0), r.returncode


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("所有 CHECK_TOOLS 文件存在", all(
        os.path.exists(os.path.join(ROOT, "tools", t)) for t in CHECK_TOOLS))
    chk("所有 GATE_TESTS 测试文件存在", all(
        os.path.exists(os.path.join(ROOT, t)) for t in GATE_TESTS))
    chk("受控清单非空且含 atoms/evidence", "atoms" in CONTROLLED_PATHS and "evidence" in CONTROLLED_PATHS)
    print(f"run_619_gate selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="619 D1 收工门禁")
    ap.add_argument("--check", action="store_true", help="只读自验证（不跑门禁主体），exit 0 = 通过")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()

    print("=== 619 收工门禁 ===")
    print("[1/3] 受控目录零污染检查")
    clean, dirty = check_controlled_clean()
    if not clean:
        print("  FAIL 受控目录被污染：\n" + dirty)
        return 2

    print("[2/3] 逐工具 --check（619 新工具 + C1 改动）")
    tools_ok, tool_res = run_tool_checks()
    if not tools_ok:
        print("  FAIL 有工具 --check 未通过")
        return 3

    print("[3/3] pytest（619 新增单测）")
    tests_ok, _ = run_tests()
    if not tests_ok:
        print("  FAIL 单测有红")
        return 4

    print("验收门: PASS (EXIT=0)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
