"""625 F1 · 收工门禁（625 专用）

校验项：
1. 整目录 ruff（tools/ + tests/）全绿
2. 本批 625 新工具 `--check` 全部 exit 0
3. 完整性根：`tool_integrity.py --check`（尺子 34/34 一致）
4. OTS anchor：`ots_anchor_613.py --check`
5. mypy tools/ = 0 errors（625 A1 已清零）
6. 受控目录（atoms/evidence/Examples/Book）零污染

铁律：不跑监工门禁；必有 `--check`。
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PY = sys.executable

# 本批 625 新工具（均带 --check；None 表示用对应既有校验器）
NEW_TOOLS: list[tuple[str, list[str]]] = [
    ("loop_stability_metrics_625", ["--check"]),
    ("vfdr_convergence_625", ["--check"]),
    ("path_config_625", ["--check"]),
    ("queyi_core_interface_design_625", ["--check"]),
    ("queyi_core_trigger_check_625", ["--check"]),
    ("round7_mutator_625", ["--check"]),
    ("human_review_dashboard_625", ["--check"]),
    ("human_review_executor_625", ["--check"]),
    ("pck_upgrade_strategy_625", ["--check"]),
]


def _run(args: list[str]) -> tuple[int, str]:
    try:
        p = subprocess.run(args, capture_output=True, text=True, cwd=ROOT, timeout=300)
        return p.returncode, (p.stdout + p.stderr)[-1500:]
    except Exception as exc:  # noqa: BLE001
        return 1, str(exc)


def check() -> int:
    ok = True

    def chk(name: str, cond: bool, tail: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {tail}")
        ok = ok and cond

    # 1. 整目录 ruff
    rc, _ = _run([PY, "-m", "ruff", "check", "tools/", "tests/"])
    chk("整目录 ruff 全绿", rc == 0)

    # 2. 625 新工具 --check
    for name, extra in NEW_TOOLS:
        rc, out = _run([PY, os.path.join("tools", f"{name}.py"), *extra])
        chk(f"{name} --check", rc == 0, out[-200:].replace("\n", " "))

    # 3. 完整性根
    rc, _ = _run([PY, os.path.join("tools", "tool_integrity.py"), "--check"])
    chk("tool_integrity --check（尺子 34/34）", rc == 0)

    # 4. OTS anchor
    rc, _ = _run([PY, os.path.join("tools", "ots_anchor_613.py"), "--check"])
    chk("ots_anchor --check", rc == 0)

    # 5. mypy tools/ = 0
    rc, out = _run([PY, "-m", "mypy", "tools/"])
    n_err = out.count(": error:")
    chk("mypy tools/ = 0 errors", rc == 0 and n_err == 0, f"({n_err} errors)")

    # 6. 受控目录零污染
    rc, _ = _run(["git", "diff", "--quiet", "--", "atoms", "evidence", "Examples", "Book"])
    chk("受控目录零污染", rc == 0)

    print(f"F1 gate: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="625 F1 收工门禁")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--skip-tools", action="store_true",
                    help="跳过外部工具调用（仅做结构自检），用于快速本地校验")
    args = ap.parse_args(argv)
    if args.check:
        return check()
    return check()


if __name__ == "__main__":
    sys.exit(main())
