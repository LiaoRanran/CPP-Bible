"""624 F1 · 收工门禁（继承 623 的整目录 ruff 口径）

检查项：
1. **整目录 ruff**（tools/ + tests/，继承 623 C1 口径）；
2. **本批（624）新文件 ruff**（快速定位）；
3. **624 新工具 `--check`**（cross_card_attack / escape_root_cause_v3 / vfdr_updater_v2 /
   pck_authorized_upgrade / human_review_item_by_item_generator）；
4. **623/622/621 工具 `--check` 回归**；
5. **ci.yml 语法**（YAML 可解析）；
6. **受控目录零污染**（`git diff --quiet -- atoms evidence Examples Book`）。

**刻意不跑**（监工的事，铁律 §六.4）：`tool_integrity --check` / `gate_engine --check` /
`poison_drill` / `atom_evidence_replay --check`。

铁律：不改受控目录/工具逻辑；只做检查，不写盘（`--check` 为只读自检）。
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
if HERE not in sys.path:
    sys.path.insert(0, HERE)

import run_623_gate as G623  # noqa: E402  （复用整目录 ruff 口径）

NEW_624 = ["cross_card_attack_624", "escape_root_cause_v3_624", "vfdr_updater_v2_624",
           "pck_authorized_upgrade_624", "human_review_item_by_item_generator_624"]
REGRESSION = ["high_complexity_mutator_623", "ruler_coverage_audit_623", "run_623_gate",
              "authority_to_annotations_sync_623", "w2_recompute_623",
              "sandbox_apply_622", "mutation_generator_621", "adversarial_loop_620"]
CONTROLLED = ["atoms", "evidence", "Examples", "Book"]


def _run(cmd: list[str]) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    return proc.returncode, (proc.stdout or "") + (proc.stderr or "")


def check_tools(tools: list[str]) -> list[str]:
    """对每个工具跑 `--check`；返回失败（或缺失）的工具名列表。"""
    fails: list[str] = []
    for t in tools:
        p = os.path.join(ROOT, "tools", t + ".py")
        if not os.path.exists(p):
            fails.append(f"{t}(缺)")
            continue
        rc, _out = _run([sys.executable, p, "--check"])
        if rc != 0:
            fails.append(t)
    return fails


def ci_yml_ok() -> bool:
    import yaml  # type: ignore[import-untyped]
    p = os.path.join(ROOT, ".github", "workflows", "ci.yml")
    try:
        with open(p, encoding="utf-8") as fh:
            yaml.safe_load(fh)
        return True
    except (OSError, ValueError):
        return False


def controlled_clean() -> bool:
    rc, _ = _run(["git", "diff", "--quiet", "--", *CONTROLLED])
    return rc == 0


def batch_624_files() -> list[str]:
    return [p for p in G623.collect_py_files(["tools", "tests"])
            if "_624" in os.path.basename(p)]


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool) -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name}")
        ok = ok and cond

    chk("枚举到 624 新文件", len(batch_624_files()) >= 5)
    chk("整目录枚举非空", len(G623.collect_py_files(["tools", "tests"])) > 0)
    chk("ci.yml 可解析", ci_yml_ok())
    rc, _ = G623.run_ruff(G623.collect_py_files(["tools", "tests"]))
    chk("ruff 可运行", rc in (0, 1))
    chk("受控目录检查可调用", isinstance(controlled_clean(), bool))
    print(f"F1 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="624 F1 收工门禁")
    ap.add_argument("--check", action="store_true", help="只读自检，exit 0 = 通过")
    ap.add_argument("--skip-tools", action="store_true", help="跳过工具 --check（快速）")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()

    steps: list[tuple[str, bool, str]] = []

    rc, out = G623.run_ruff(G623.collect_py_files(["tools", "tests"]))
    steps.append(("整目录 ruff（tools/ tests/）", rc == 0,
                  (out.strip().splitlines() or [""])[-1]))

    rc, out = G623.run_ruff(batch_624_files())
    steps.append(("本批(624)文件 ruff", rc == 0, (out.strip().splitlines() or [""])[-1]))

    if not args.skip_tools:
        f = check_tools(NEW_624)
        steps.append(("624 新工具 --check", not f, ",".join(f) or "5/5"))
        f2 = check_tools(REGRESSION)
        steps.append(("623/622/621 回归 --check", not f2, ",".join(f2) or "8/8"))

    steps.append(("ci.yml 语法", ci_yml_ok(), "YAML OK" if ci_yml_ok() else "解析失败"))
    steps.append(("受控目录零污染", controlled_clean(),
                  "clean" if controlled_clean() else "DIRTY"))

    print("[run_624_gate] 收工门禁")
    passed_all = True
    for name, passed, extra in steps:
        mark = "✅" if passed else "❌"
        print(f"  {mark} {name}  {extra}")
        passed_all = passed_all and passed
    print(f"[run_624_gate] {'PASS' if passed_all else 'FAIL'}")
    return 0 if passed_all else 1


if __name__ == "__main__":
    sys.exit(main())
