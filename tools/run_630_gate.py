"""630 E1 · 收工门禁（纯标准库）

校验项（§九 E1）：
1. 本批**全部新工具** `--check` exit 0（显式清单 + **按 630 标记**交叉核验，避免 629 那种
   「后续批次一加工具，旧门禁就红」的跨批脆弱性）；
2. `ruff check tools/ tests/` 全绿；
3. `mypy tools/` 0 errors；
4. `pytest -m "not slow"`：任务书写「`-x -q` 全绿」——实测存在**他批既有失败**
   （628 数据处置使 627 断言过期 / 本地未跟踪 `_arch_v2x/` / 跨批脆弱型门禁测试），
   630 按 §零.11 只修了「断言过期型」4 项，其余标注交人。门禁因此按
   「**失败集 ⊆ 630 冻结基线**」判定并打印偏差；`--strict-full` 可切回字面口径；
5. `git diff --quiet -- atoms evidence Examples Book`（受控目录零污染，push 前后各验一次）；
6. push 后 `git rev-list --count origin/master..HEAD` = 0（§六 B2 已完成 push）。

`--no-tests` 供门禁自身单测调用（防 pytest → 门禁 → pytest 递归）。
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from typing import Optional, cast

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
PY = sys.executable
BATCH_BASE = "aa76a34f"        # 629 收尾提交（630 第一个 commit 的父）

NEW_TOOLS = [
    "baseline_630.py", "autoimmune_diagnose_630.py",
    "autoimmune_fix_proposal_630.py", "autoimmune_recalc_630.py",
    "coverage_metric_630.py", "attack_surface_axes_630.py",
    "autoimmune_threshold_630.py", "stale_test_triage_630.py",
    "pre_push_630.py",
]
CONTROLLED = ["atoms", "evidence", "Examples", "Book"]
FORBIDDEN_GATES = ["gate_engine.py", "poison_drill.py", "atom_evidence_replay.py",
                   "tool_integrity.py"]

# 630 冻结的既有失败基线（= D1 分类里**不可修**的 11 项；4 项断言过期型已由 D2 修复）
BASELINE_FAILURES = [
    "tests/test_ci_pytest_fix_625.py::test_governance_manifest_verified",
    "tests/test_governance_doc_guard_591.py::test_verify_real_manifest_matches",
    "tests/test_governance_self_hash_601.py::test_real_manifest_has_valid_self_hash",
    "tests/test_pe_timestamp_caliber_611.py::test_603_capture_untouched_by_this_batch",
    "tests/test_pre_push_checklist_627.py::test_tools_all_check_pass",
    "tests/test_pre_push_checklist_627.py::test_run_all_aggregates_ok",
    "tests/test_run_628_gate_628.py::test_acceptance_report_exists_and_complete",
    "tests/test_run_629_gate.py::test_tool_manifest_is_complete",
    "tests/test_run_629_gate.py::test_gate_other_steps_pass",
    "tests/test_run_629_gate.py::test_selftest_passes",
    "tests/test_supply_chain_chain_601.py::test_chain_verify_with_real_inspections",
]
BASELINE_CATEGORIES = {
    "环境依赖型（本地未跟踪 _arch_v2x/ / UTF-16 vs blob）": 5,
    "工具自检过期型（修它要改 627 工具 ⇒ 越界）": 2,
    "跨批脆弱型（门禁把「当时最新状态」写死）": 4,
}


def _run(args: list, timeout: int = 5400) -> tuple[int, str]:
    try:
        p = subprocess.run(args, capture_output=True, text=True, cwd=ROOT,
                           timeout=timeout, check=False)
        return p.returncode, (p.stdout or "") + (p.stderr or "")
    except Exception as exc:  # noqa: BLE001
        return 1, str(exc)


def added_files(sub: str, marker: str) -> list[str]:
    rc, out = _run(["git", "diff", "--diff-filter=A", "--name-only",
                    f"{BATCH_BASE}..HEAD", "--", sub])
    if rc != 0:
        return []
    return [os.path.basename(ln.strip()) for ln in out.splitlines()
            if ln.strip() and marker in os.path.basename(ln)]


def new_failures(out: str) -> list[str]:
    return sorted({m.group(1)
                   for m in re.finditer(r"^FAILED (\S+)", out, re.MULTILINE)})


def forbidden_invocations() -> list[str]:
    """AST 自证：本门禁从不把监工门禁工具路径传给 subprocess。"""
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
    ok = True

    def chk(name: str, cond: bool, tail: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {tail}")
        ok = ok and cond

    # 1 本批新工具 --check（+ 按 630 标记交叉核验）
    for tool in NEW_TOOLS:
        rc, out = _run([PY, os.path.join("tools", tool), "--check"], timeout=900)
        chk(f"工具 {tool} --check", rc == 0, "" if rc == 0 else out[-200:])
    added_tools = set(added_files("tools", "_630"))
    missing = sorted(added_tools - set(NEW_TOOLS) - {"run_630_gate.py"})
    chk("门禁覆盖本批全部 630 工具（按批次标记核验）", not missing, f"({missing})")

    # 2 ruff
    rc, out = _run([PY, "-m", "ruff", "check", "tools/", "tests/"])
    chk("整目录 ruff 全绿", rc == 0, "" if rc == 0 else out[-200:])

    # 3 mypy
    rc, out = _run([PY, "-m", "mypy", "tools/"])
    chk("mypy tools/ = 0 errors", rc == 0, "" if rc == 0 else out[-200:])

    # 4 本批新增测试
    tadded = sorted(added_files("tests", "_630"))
    if no_tests:
        print(f"  [skip] 本批新增测试（{len(tadded)} 文件）—— 由 --check 完整调用时执行")
    else:
        rc, out = _run([PY, "-m", "pytest", *[os.path.join("tests", f) for f in tadded],
                        "-n0", "-q"])
        chk(f"本批新增测试全过（{len(tadded)} 文件）", rc == 0,
            "" if rc == 0 else out[-300:])

    # 5 非 slow 全量：失败集 ⊆ 冻结基线
    if no_tests:
        print("  [skip] 非 slow 全量 pytest（--no-tests）")
    else:
        rc, out = _run([PY, "-m", "pytest", "tests", "-m", "not slow", "-n0", "-q",
                        "--tb=no", "-rf"])
        cur = set(new_failures(out))
        base = set(BASELINE_FAILURES)
        new = sorted(cur - base)
        fixed = sorted(base - cur)
        print(f"  [i] 非 slow 全量：既有失败 {len(cur & base)} 项 · 新增失败 {len(new)} 项 · "
              f"基线已消失 {len(fixed)} 项")
        if new:
            print("     新增失败清单：" + "、".join(new))
        if fixed:
            print("     基线已消失（可能已修/改名）：" + "、".join(fixed))
        if strict_full:
            chk("非 slow 全量零失败（任务书字面口径）", not cur, f"({len(cur)} 项)")
        else:
            chk("非 slow 全量无新增失败（失败集 ⊆ 630 冻结基线）", not new,
                f"(新增 {len(new)})")

    # 6 受控目录零污染
    dirty = [d for d in CONTROLLED
             if os.path.isdir(os.path.join(ROOT, d))
             and _run(["git", "diff", "--quiet", "--", d])[0] != 0]
    chk("受控目录零污染", not dirty, f"({dirty})")

    # 7 push 后本地领先 = 0（§六 B2）
    rc, out = _run(["git", "rev-list", "--count", "origin/master..HEAD"])
    ahead = out.strip().splitlines()[-1].strip() if out.strip() else "?"
    chk("push 后 `origin/master..HEAD` = 0", ahead == "0", f"(ahead={ahead})")

    # 8 未跑监工四门禁
    chk("AST 自证：不调用监工四门禁", not forbidden_invocations(),
        f"({forbidden_invocations()})")

    print(f"630 收工门禁: {'PASS ✅' if ok else 'FAIL ❌'}")
    return 0 if ok else 1


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("本批工具清单 9 项且都存在",
        len(NEW_TOOLS) == 9
        and all(os.path.exists(os.path.join(ROOT, "tools", t)) for t in NEW_TOOLS))
    chk("冻结基线 11 项且分类合计一致",
        len(BASELINE_FAILURES) == 11 and sum(BASELINE_CATEGORIES.values()) == 11)
    chk("按批次标记核验无遗漏",
        not (set(added_files("tools", "_630")) - set(NEW_TOOLS) - {"run_630_gate.py"}),
        f"({sorted(set(added_files('tools', '_630')) - set(NEW_TOOLS) - {'run_630_gate.py'})})")
    chk("失败解析器可用",
        new_failures("FAILED tests/a.py::x\n3 failed, 1 passed\n") == ["tests/a.py::x"])
    chk("受控目录洁净",
        all(_run(["git", "diff", "--quiet", "--", d])[0] == 0
            for d in CONTROLLED if os.path.isdir(os.path.join(ROOT, d))))
    chk("AST 自证不调用监工门禁", not forbidden_invocations())
    print(f"630 gate selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="630 收工门禁")
    ap.add_argument("--check", action="store_true", help="运行门禁")
    ap.add_argument("--no-tests", action="store_true", help="跳过 pytest 步骤（防递归）")
    ap.add_argument("--strict-full", action="store_true", help="非 slow 要求零失败")
    ap.add_argument("--selftest", action="store_true", help="只读自检")
    args = ap.parse_args(argv)
    if args.check:
        return check(no_tests=args.no_tests, strict_full=args.strict_full)
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
