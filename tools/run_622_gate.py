r"""622 F2 · 收工门禁（6 项串行检查）

1. **受控目录零污染**：`atoms/ evidence/ Examples/ Book/` 无未提交改动
2. **622 新工具 --check**（5 个，不含本脚本自身）
3. **621/620 工具 --check 回归**（含 622 期间被升级的 621 工具）
4. **ci.yml 语法 + 并发安全检查**（622 B1 已 push，本步在本地再验一次）
5. **ruff**（622 新工具 + 新单测 + 本脚本）
6. **pytest（622 新增单测）**

**刻意不跑**（622 §六.4 硬边界）：`tool_integrity --check` / `gate_engine --check` /
`poison_drill` / `atom_evidence_replay --check`。
- 属**监工门禁**，622 明确不跑；
- 622 的 gate 判决已通过**沙箱**（A1/A2/A4）以 `--run --json` 方式使用，
  与"监工门禁 `--check`"是**不同用途**（前者是判决 oracle，后者是验收判定）；
- `replay --check` 会重写 `Examples/atoms/*.asm`（受控目录）。

**解释器探活**：优先 `.venv\Scripts\python.exe`，探活失败回退 `sys.executable`
（621 期间该 uv trampoline 曾损坏）。

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

CONTROLLED = ("atoms/", "evidence/", "Examples/", "Book/")

# 622 新增工具（不含 run_622_gate 自身，避免自指）
NEW_TOOLS_622 = (
    "sandbox_apply_622",
    "escape_root_cause_622",
    "vfdr_calculator_622",
    "atom_verdict_extractor_622",
    "verification_horizon_622",
)

# 621/620 工具回归（含 622 期间被升级的 621 工具）
TOOLS_REGRESSION = (
    "mutation_generator_621",
    "mutation_quality_621",
    "abstain_classifier_621",
    "authority_pending_621",
    "adversarial_loop_620",
    "adversarial_weight_calibration_620",
    "vfdr_realtime_620",
    "authority_log_620",
    "pck_batch_migrator_620",
)

# 622 单测（不含 test_622_gate.py —— 会调用本门禁，形成自指）
NEW_TESTS_622 = (
    "tests/test_622_a1.py", "tests/test_622_a2.py", "tests/test_622_a3.py",
    "tests/test_622_a4.py", "tests/test_622_a5.py", "tests/test_622_c1.py",
    "tests/test_622_c2.py", "tests/test_622_c3.py", "tests/test_622_d1.py",
    "tests/test_622_d2.py", "tests/test_622_e1.py", "tests/test_622_e2.py",
)

NOT_RUN = ("tool_integrity --check", "gate_engine --check",
           "poison_drill", "atom_evidence_replay --check")


def _probe(cmd: list[str]) -> bool:
    try:
        return subprocess.run(cmd, cwd=ROOT, capture_output=True, timeout=90).returncode == 0
    except Exception:  # noqa: BLE001
        return False


def pick_python() -> str:
    cand = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
    if os.path.exists(cand) and _probe([cand, "-c", "import sys"]):
        return cand
    return sys.executable


PY = pick_python()


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


def _tool_check(names: tuple[str, ...]) -> tuple[bool, str]:
    bad = []
    for name in names:
        rc, out = _run([PY, os.path.join("tools", f"{name}.py"), "--check"])
        if rc != 0:
            bad.append(f"{name}(exit {rc})")
    if bad:
        return False, "失败：" + ", ".join(bad)
    return True, f"{len(names)}/{len(names)} 通过"


def check_new_tools() -> tuple[bool, str]:
    ok, msg = _tool_check(NEW_TOOLS_622)
    return (ok, msg + "（run_622_gate 自身不参与，避免自指）") if ok else (ok, msg)


def check_regression() -> tuple[bool, str]:
    return _tool_check(TOOLS_REGRESSION)


def check_ci_yml() -> tuple[bool, str]:
    rc, out = _run([PY, "-c",
                    "import yaml; yaml.safe_load(open('.github/workflows/ci.yml',"
                    "encoding='utf-8')); print('ci.yml YAML OK')"])
    if rc != 0:
        return False, "ci.yml 语法错误：\n" + "\n".join(out.strip().splitlines()[-6:])
    rc2, out2 = _run([PY, os.path.join("tools", "ci_concurrency_check_621.py")])
    if rc2 != 0:
        return False, "并发安全检查未通过：\n" + "\n".join(out2.strip().splitlines()[-6:])
    return True, "YAML 语法 OK + 并发安全检查通过"


def check_ruff() -> tuple[bool, str]:
    paths = [os.path.join("tools", f"{n}.py") for n in NEW_TOOLS_622]
    paths.append(os.path.join("tools", "run_622_gate.py"))
    paths += list(NEW_TESTS_622)
    rc, out = _run([PY, "-m", "ruff", "check", *paths])
    if rc != 0:
        return False, "ruff 失败：\n" + "\n".join(out.strip().splitlines()[-8:])
    return True, f"{len(paths)} 个文件通过"


def check_pytest() -> tuple[bool, str]:
    rc, out = _run([PY, "-m", "pytest", *NEW_TESTS_622, "-q", "-p", "no:cacheprovider"])
    if rc != 0:
        return False, "pytest 失败：\n" + "\n".join(out.strip().splitlines()[-8:])
    _rc2, out2 = _run([PY, "-m", "pytest", *NEW_TESTS_622, "--collect-only", "-q",
                       "-p", "no:cacheprovider"])
    n = len([ln for ln in out2.splitlines() if "::" in ln])
    if n == 0:
        n = sum(int(m.group(1)) for m in re.finditer(r"\.py:\s*(\d+)\s*$", out2,
                                                    re.MULTILINE))
    return True, f"{n} passed"


CHECKS = (
    ("受控目录零污染", check_controlled_dirs),
    ("622 新工具 --check", check_new_tools),
    ("621/620 工具回归", check_regression),
    ("ci.yml 语法 + 并发安全", check_ci_yml),
    ("ruff 静态检查", check_ruff),
    ("pytest（622 新增单测）", check_pytest),
)


def run_all() -> int:
    print(f"run_622_gate · 622 收工门禁（{len(CHECKS)} 项，串行）\n解释器：{PY}\n")
    results = []
    for i, (label, fn) in enumerate(CHECKS, 1):
        ok, msg = fn()
        results.append(ok)
        print(f"[{i}/{len(CHECKS)}] {label:<22} {'✅' if ok else '❌'} {msg}")
    print(f"\n刻意不跑（622 §六.4）：{', '.join(NOT_RUN)}")
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

    chk("6 项检查已注册", len(CHECKS) == 6)
    chk("622 新工具 5 个（不含自身）", len(NEW_TOOLS_622) == 5)
    chk("回归工具 9 个", len(TOOLS_REGRESSION) == 9)
    chk("622 单测文件 12 个（不含 gate 自身）", len(NEW_TESTS_622) == 12)
    chk("受控目录清单 4 个", len(CONTROLLED) == 4)
    chk("不跑清单 4 项", len(NOT_RUN) == 4)
    chk("解释器可用", bool(PY) and os.path.exists(PY))
    chk("所有 622 工具文件存在",
        all(os.path.exists(os.path.join(ROOT, "tools", f"{n}.py")) for n in NEW_TOOLS_622))
    print(f"F2 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="622 F2 收工门禁")
    ap.add_argument("--check", action="store_true",
                    help="只读自检（不跑 6 项门禁），exit 0 = 通过")
    ap.add_argument("--pick-python", action="store_true", help="打印选定的解释器")
    args = ap.parse_args(argv)
    if args.pick_python:
        print(PY)
        return 0
    if args.check:
        return selftest()
    return run_all()


if __name__ == "__main__":
    sys.exit(main())
