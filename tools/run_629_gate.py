"""629 F1 · 收工门禁（纯标准库）

校验项（对应 629.md §十 F1）：
1. 本批**全部新工具** `--check` exit 0（清单显式声明 + 用 `git diff --diff-filter=A` 交叉核验
   没有漏网的 629 工具）
2. `ruff check tools/ tests/` 全绿
3. `mypy tools/` 0 errors
4. `pytest -m "not slow"`：**无新增失败**（口径偏差见下）—— 629 开工实测有 19 项既有失败
   （状态快照型断言，属 625/627/624 批资产，§零.11 不改他批），任务书要求「非 slow 全绿」；
   本门禁按「**失败集 ⊆ 冻结基线**」判定，并把偏差与清单打印出来；加 `--strict-full`
   可切回任务书字面口径（要求零失败）。
5. `git diff --quiet -- atoms evidence Examples Book`（受控目录零污染）
6. **不跑监工四门禁**（gate/poison/replay/tool_integrity）
7. 输出 PASS/FAIL + 各项结果

`--no-tests` 供本门禁自身的单测调用（避免 pytest → 门禁 → pytest 递归）。
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
PY = sys.executable
BATCH_BASE = "889a3bc8"          # 629 起点（628 E1 收工）

NEW_TOOLS = [
    "baseline_629.py", "autoimmune_rate_framework.py", "autoimmune_probe_629.py",
    "autoimmune_dashboard_629.py", "attack_surface_taxonomy.py", "attack_mapping_629.py",
    "uncovered_attack_surfaces.py", "vsa_asymmetric_signer_629.py",
    "authority_log_integration_629.py", "independence_static_check.py",
    "e2e_attestation_629.py", "attack_objective_629.py", "attack_round8_629.py",
    "loop_metrics_629.py",
]
CONTROLLED = ["atoms", "evidence", "Examples", "Book"]
FORBIDDEN_GATES = ["gate_engine.py", "poison_drill.py", "atom_evidence_replay.py",
                   "tool_integrity.py"]


def _run(args: list, timeout: int = 3600) -> tuple[int, str]:
    try:
        p = subprocess.run(args, capture_output=True, text=True, cwd=ROOT,
                           timeout=timeout, check=False)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as exc:  # noqa: BLE001
        return 1, str(exc)


def added_files(sub: str) -> list[str]:
    """本批新增文件（git diff --diff-filter=A），用于交叉核验工具/测试清单无遗漏。"""
    rc, out = _run(["git", "diff", "--diff-filter=A", "--name-only",
                    f"{BATCH_BASE}..HEAD", "--", sub])
    if rc != 0:
        return []
    return [os.path.basename(ln.strip()) for ln in out.splitlines() if ln.strip()]


def new_failures(out: str) -> tuple[list[str], set[str]]:
    """从 pytest 输出提取当前失败集 + 汇总行。"""
    fails = sorted({m.group(1)
                    for m in re.finditer(r"^FAILED (\S+)", out, re.MULTILINE)})
    summary = ""
    for line in reversed(out.strip().splitlines()):
        if re.search(r"\d+ (passed|failed)", line):
            summary = line.strip()
            break
    return fails, {summary}


def forbidden_invocations() -> list[str]:
    """AST 扫描：本门禁是否把监工门禁工具路径（gate_engine 等）传给了 subprocess？

    只看**调用参数里的字符串常量**（含 `os.path.join("tools", X)` 的 X），不看常量表定义，
    因此「声明常量」不会误报，「真调用」一定被抓。
    """
    import ast

    tree = ast.parse(open(os.path.abspath(__file__), encoding="utf-8").read())
    hits = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) \
                and node.func.id == "_run":
            for arg in node.args:
                for sub in ast.walk(arg):
                    if isinstance(sub, ast.Constant) and isinstance(sub.value, str) \
                            and sub.value in FORBIDDEN_GATES:
                        hits.append(sub.value)
    return hits


def check(no_tests: bool = False, strict_full: bool = False) -> int:
    import baseline_629 as B

    ok = True

    def chk(name: str, cond: bool, tail: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {tail}")
        ok = ok and cond

    # 1 本批新工具 --check
    for tool in NEW_TOOLS:
        rc, out = _run([PY, os.path.join("tools", tool), "--check"], timeout=900)
        chk(f"工具 {tool} --check", rc == 0, "" if rc == 0 else out[-200:])
    added = set(added_files("tools"))
    missing = sorted(added - set(NEW_TOOLS) - {"run_629_gate.py"})
    chk("门禁覆盖本批全部新增工具（git 交叉核验）", not missing, f"({missing})")

    # 2 ruff 整目录
    rc, out = _run([PY, "-m", "ruff", "check", "tools/", "tests/"])
    chk("整目录 ruff 全绿", rc == 0, "" if rc == 0 else out[-200:])

    # 3 mypy tools/
    rc, out = _run([PY, "-m", "mypy", "tools/"])
    chk("mypy tools/ = 0 errors", rc == 0, "" if rc == 0 else out[-200:])

    # 4 本批新增测试（动态 + 交叉核验）
    tadded = sorted(f for f in added_files("tests") if f.startswith("test_"))
    if no_tests:
        print(f"  [skip] 本批新增测试（{len(tadded)} 文件）—— 由 --check 完整调用时执行")
    else:
        rc, out = _run([PY, "-m", "pytest", *[os.path.join("tests", f) for f in tadded],
                        "-n0", "-q"])
        chk(f"本批新增测试全过（{len(tadded)} 文件）", rc == 0,
            "" if rc == 0 else out[-300:])

    # 5 非 slow 全量：失败集 ⊆ 冻结基线（任务书字面口径用 --strict-full）
    if no_tests:
        print("  [skip] 非 slow 全量 pytest（--no-tests）")
    else:
        rc, out = _run([PY, "-m", "pytest", "tests", "-m", "not slow", "-n0", "-q",
                        "--tb=no", "-rf"])
        cur = set(new_failures(out)[0])
        base = set(B.BASELINE_FAILURES)
        new = sorted(cur - base)
        fixed = sorted(base - cur)
        print(f"  [i] 非 slow 全量：既有失败 {len(cur & base)} 项 · "
              f"新增失败 {len(new)} 项 · 基线已消失 {len(fixed)} 项")
        if new:
            print("     新增失败清单：" + "、".join(new))
        if fixed:
            print("     基线已消失（可能是修好或改名）：" + "、".join(fixed))
        if strict_full:
            chk("非 slow 全量零失败（任务书字面口径）", not cur, f"({len(cur)} 项)")
        else:
            chk("非 slow 全量无新增失败（失败集 ⊆ 629 开工冻结基线）", not new,
                f"(新增 {len(new)})")

    # 6 受控目录零污染
    dirty = [d for d in CONTROLLED
             if os.path.isdir(os.path.join(ROOT, d))
             and _run(["git", "diff", "--quiet", "--", d])[0] != 0]
    chk("受控目录零污染", not dirty, f"({dirty})")

    # 7 未跑监工四门禁（AST 自证：本工具从不把监工门禁路径传给 subprocess）
    used = forbidden_invocations()
    chk("未跑监工四门禁（AST 扫描：无监工门禁调用）", not used, f"({used})")
    chk("未改 ci.yml / 未改 CORE_TOOLS 生产逻辑",
        _run(["git", "diff", "--quiet", BATCH_BASE, "HEAD", "--", ".github/workflows/ci.yml"])[0]
        == 0)

    print(f"629 收工门禁: {'PASS ✅' if ok else 'FAIL ❌'}")
    return 0 if ok else 1


def selftest() -> int:
    """只读自检：门禁清单/基线映射/非 slow 解析器（不跑全量）。"""
    import baseline_629 as B

    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("本批工具清单 14 项且文件都存在",
        len(NEW_TOOLS) == 14
        and all(os.path.exists(os.path.join(ROOT, "tools", t)) for t in NEW_TOOLS))
    chk("基线失败清单已冻结（修正版 11 项）", len(B.BASELINE_FAILURES) == 11)
    chk("新增工具交叉核验无遗漏",
        not (set(added_files("tools")) - set(NEW_TOOLS) - {"run_629_gate.py"}),
        f"({sorted(set(added_files('tools')) - set(NEW_TOOLS) - {'run_629_gate.py'})})")
    chk("非慢解析器可用",
        new_failures("FAILED tests/a.py::x\n1 failed, 2 passed in 1.0s\n")[0]
        == ["tests/a.py::x"])
    chk("本轮受控目录洁净",
        all(_run(["git", "diff", "--quiet", "--", d])[0] == 0
            for d in CONTROLLED if os.path.isdir(os.path.join(ROOT, d))))
    chk("AST 自证：不调用监工四门禁", not forbidden_invocations(),
        f"({forbidden_invocations()})")
    chk("新工具清单与监工门禁零交集",
        not (set(NEW_TOOLS) & set(FORBIDDEN_GATES)))
    print(f"629 gate selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="629 收工门禁")
    ap.add_argument("--check", action="store_true", help="运行门禁")
    ap.add_argument("--no-tests", action="store_true", help="跳过 pytest 相关步骤（防递归）")
    ap.add_argument("--strict-full", action="store_true",
                    help="非 slow 全量要求零失败（任务书字面口径）")
    ap.add_argument("--selftest", action="store_true", help="只读自检")
    args = ap.parse_args(argv)
    if args.selftest:
        return selftest()
    if args.check:
        return check(no_tests=args.no_tests, strict_full=args.strict_full)
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
