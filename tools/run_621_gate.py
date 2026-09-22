r"""621 E2 · 收工门禁（6 项串行检查）

1. **受控目录零污染**：`atoms/ evidence/ Examples/ Book/` 无未提交改动
2. **621 新工具 --check**（9 个，不含本脚本自身）
3. **620 工具 --check 回归**（7 个）
4. **ci.yml 语法验证**（本批改了 ci.yml，必须验）
5. **ruff**（621 新工具 + 新单测）
6. **pytest（621 新增单测）**

**刻意不跑**（621 §六.3 硬边界）：`tool_integrity --check` / `gate_engine --check` /
`poison_drill` / `atom_evidence_replay --check` —— 原因：
- 该四项属**监工门禁**，621 明确不跑；
- CI 竞态修复（B 线）**需要在 CI 环境验证**（本地串行跑看不出并行差异）；
- `replay --check` 会重写 `Examples/atoms/*.asm`（受控目录），验收批次不应主动写受控目录。

**解释器选择**：优先 `.venv\Scripts\python.exe`，但**先探活**——
621 期间该 uv trampoline 曾损坏（error 448），探活失败时回退 `sys.executable`，
避免整个门禁因环境问题误红。

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

# 621 新增工具（不含 run_621_gate 自身，避免自指）
NEW_TOOLS_621 = (
    "mutation_generator_621",
    "mutation_quality_621",
    "ci_race_reproducer_621",
    "ci_concurrency_check_621",
    "abstain_classifier_621",
    "pck_abstain_sync_621",
    "authority_pending_621",
    "human_review_quality_compare_621",
    "human_review_anonymize_621",
)

# 620 工具回归
TOOLS_620 = (
    "adversarial_loop_620",
    "adversarial_weight_calibration_620",
    "vfdr_realtime_620",
    "pck_batch_migrator_620",
    "pck_status_stats_620",
    "authority_log_620",
    "pck_authority_sync_620",
)

# 621 单测（不含 test_621_gate.py —— 它会调用本门禁，纳入会形成自指递归）
NEW_TESTS_621 = (
    "tests/test_621_a1.py", "tests/test_621_a2.py", "tests/test_621_a3.py",
    "tests/test_621_a4.py", "tests/test_621_b1.py", "tests/test_621_b2.py",
    "tests/test_621_b3.py", "tests/test_621_c1.py", "tests/test_621_c2.py",
    "tests/test_621_c3.py", "tests/test_621_d1.py", "tests/test_621_d2.py",
    "tests/test_621_d3.py",
)

CI_YML = os.path.join(ROOT, ".github", "workflows", "ci.yml")

NOT_RUN = ("tool_integrity --check", "gate_engine --check",
           "poison_drill", "atom_evidence_replay --check")


def _probe(cmd: list[str]) -> bool:
    try:
        return subprocess.run(cmd, cwd=ROOT, capture_output=True, timeout=90).returncode == 0
    except Exception:  # noqa: BLE001
        return False


def pick_python() -> str:
    """优先 venv 解释器，但必须探活成功（uv trampoline 可能损坏）。"""
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
    ok, msg = _tool_check(NEW_TOOLS_621)
    return ok, msg + "（run_621_gate 自身不参与，避免自指）" if ok else msg


def check_tools_620() -> tuple[bool, str]:
    return _tool_check(TOOLS_620)


def check_ci_yml() -> tuple[bool, str]:
    rc, out = _run([PY, "-c",
                    "import yaml,sys; yaml.safe_load(open('.github/workflows/ci.yml',"
                    "encoding='utf-8')); print('ci.yml YAML OK')"])
    if rc != 0:
        return False, "ci.yml 语法错误：\n" + "\n".join(out.strip().splitlines()[-6:])
    # 同时确认竞态修复仍在位
    rc2, out2 = _run([PY, os.path.join("tools", "ci_concurrency_check_621.py")])
    if rc2 != 0:
        return False, "并发安全检查未通过：\n" + "\n".join(out2.strip().splitlines()[-6:])
    return True, "YAML 语法 OK + 并发安全检查通过"


def check_ruff() -> tuple[bool, str]:
    paths = [os.path.join("tools", f"{n}.py") for n in NEW_TOOLS_621]
    paths.append(os.path.join("tools", "run_621_gate.py"))
    paths += list(NEW_TESTS_621)
    rc, out = _run([PY, "-m", "ruff", "check", *paths])
    if rc != 0:
        return False, "ruff 失败：\n" + "\n".join(out.strip().splitlines()[-8:])
    return True, f"{len(paths)} 个文件通过"


def check_pytest() -> tuple[bool, str]:
    rc, out = _run([PY, "-m", "pytest", *NEW_TESTS_621, "-q", "-p", "no:cacheprovider"])
    if rc != 0:
        return False, "pytest 失败：\n" + "\n".join(out.strip().splitlines()[-8:])
    _rc2, out2 = _run([PY, "-m", "pytest", *NEW_TESTS_621, "--collect-only", "-q",
                       "-p", "no:cacheprovider"])
    n = len([ln for ln in out2.splitlines() if "::" in ln])
    if n == 0:
        n = sum(int(m.group(1)) for m in re.finditer(r"\.py:\s*(\d+)\s*$", out2, re.MULTILINE))
    return True, f"{n} passed"


CHECKS = (
    ("受控目录零污染", check_controlled_dirs),
    ("621 新工具 --check", check_new_tools),
    ("620 工具 --check 回归", check_tools_620),
    ("ci.yml 语法 + 并发安全", check_ci_yml),
    ("ruff 静态检查", check_ruff),
    ("pytest（621 新增单测）", check_pytest),
)


def run_all() -> int:
    print(f"run_621_gate · 621 收工门禁（6 项，串行）\n解释器：{PY}\n")
    results = []
    for i, (label, fn) in enumerate(CHECKS, 1):
        ok, msg = fn()
        results.append(ok)
        print(f"[{i}/{len(CHECKS)}] {label:<24} {'✅' if ok else '❌'} {msg}")
    print(f"\n刻意不跑（621 §六.3）：{', '.join(NOT_RUN)}")
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
    chk("621 新工具 9 个（不含自身）", len(NEW_TOOLS_621) == 9)
    chk("620 回归工具 7 个", len(TOOLS_620) == 7)
    chk("621 单测文件 13 个（不含 gate 自身）", len(NEW_TESTS_621) == 13)
    chk("受控目录清单 4 个", len(CONTROLLED) == 4)
    chk("不跑清单含 four 监工门禁", len(NOT_RUN) == 4
        and any("gate_engine" in x for x in NOT_RUN))
    chk("解释器可用", bool(PY) and os.path.exists(PY))
    chk("所有 621 工具文件存在",
        all(os.path.exists(os.path.join(ROOT, "tools", f"{n}.py")) for n in NEW_TOOLS_621))
    print(f"E2 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="621 E2 收工门禁")
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
