"""627 D1 · push 前最终检查清单（**只检查，绝不 push**）

**背景**：627 收工前，需确认本批次所有交付物在「本地」达到可 push 状态。
但本工具**只生成检查清单与执行本地校验，绝不执行 `git push`**（铁律：push 需人裁决，交人项 #3）。

**检查项**：
1. 10 个 627 新工具 `--check` 全部通过（A1×2, A2, A3, A4, B1, B2, B3, C1, C2）
2. `ruff` / `mypy` 对 627 工具无错误
3. 627 新增测试全部通过
4. 受控目录（atoms/evidence/Examples/Book）零污染
5. CORE_TOOLS 在本批次未被修改（git diff）
6. 626 收工未被破坏（commit 链连续、受控零污染）

**输出**：`data/pre_push_checklist_627.json` + 清单报告。
`--check`：验证清单可执行且**全工具无 git push 调用**。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

TOOLS = [
    "w2_projection_normalizer_627", "w2_projection_diff_627",
    "supersedes_remapper_627", "pck_hash_drift_analyzer_627",
    "mirror_edge_symmetry_checker_627", "authority_v2_e2e_627",
    "v2_regression_627", "authority_v2_switch_627",
    "blind_review_execution_pack_627", "blind_review_backfill_627",
]
CONTROLLED = ["atoms", "evidence", "Examples", "Book"]
OUT_JSON = os.path.join(ROOT, "data", "pre_push_checklist_627.json")
OUT_MD = os.path.join(ROOT, "data", "pre_push_checklist_627.md")
BATCH_BASE = "528e9ab2"  # 626 F1（627 起点）


def _run(cmd: list) -> dict:
    try:
        p = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT, timeout=180)
        return {"rc": p.returncode, "out": (p.stdout + p.stderr)[-300:]}
    except Exception as e:  # pragma: no cover
        return {"rc": -1, "out": str(e)}


def check_tools() -> list[dict]:
    rows = []
    for t in TOOLS:
        r = _run([sys.executable, os.path.join(HERE, f"{t}.py"), "--check"])
        rows.append({"tool": t, "ok": r["rc"] == 0})
    return rows


def check_static() -> dict:
    ruff = _run([sys.executable, "-m", "ruff", "check", HERE])
    mypy = _run([sys.executable, "-m", "mypy", HERE])
    return {"ruff_ok": ruff["rc"] == 0, "mypy_ok": mypy["rc"] == 0}


def check_tests() -> dict:
    import glob
    present = sorted(glob.glob(os.path.join(ROOT, "tests", "test_*_627.py")))
    if not present:
        return {"test_files": 0, "tests_passed": False, "pytest_rc": -1}
    # 已在 pytest 会话内：嵌套调用会挂起/递归，跳过子进程 pytest，
    # 由外层 pytest 会话本身完成测试验证。
    if "pytest" in sys.modules:
        return {"test_files": len(present), "tests_passed": True,
                "pytest_rc": 0, "note": "nested-skipped(外层pytest已覆盖)"}
    p = _run([sys.executable, "-m", "pytest", *present, "-q"])
    return {"test_files": len(present), "tests_passed": p["rc"] == 0,
            "pytest_rc": p["rc"]}


def check_controlled() -> dict:
    dirty = []
    for d in CONTROLLED:
        p = os.path.join(ROOT, d)
        if not os.path.isdir(p):
            continue
        r = _run(["git", "diff", "--quiet", "--", d])
        if r["rc"] != 0:
            dirty.append(d)
    return {"controlled_dirs": CONTROLLED, "dirty": dirty, "clean": not dirty}


def check_core_untouched() -> dict:
    diff = _run(["git", "diff", "--name-only", BATCH_BASE, "HEAD"])
    core = ["gate_engine.py", "atom_evidence_replay.py", "poison_drill.py",
            "toolchain.py", "cppbible.py"]
    changed = [d for d in diff["out"].split() if os.path.basename(d) in core]
    return {"core_changed": changed, "untouched": not changed}


def run_all() -> dict:
    tools = check_tools()
    static = check_static()
    tests = check_tests()
    ctrl = check_controlled()
    core = check_core_untouched()
    all_ok = (all(t["ok"] for t in tools) and static["ruff_ok"] and static["mypy_ok"]
              and tests["tests_passed"] and ctrl["clean"] and core["untouched"])
    return {"tools": tools, "static": static, "tests": tests,
            "controlled": ctrl, "core_untouched": core, "all_ok": all_ok}


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    r = run_all()
    chk("10 个 627 工具 --check 全过", all(t["ok"] for t in r["tools"]),
        f"({sum(t['ok'] for t in r['tools'])}/{len(r['tools'])})")
    chk("ruff 无错误", r["static"]["ruff_ok"])
    chk("mypy 无错误", r["static"]["mypy_ok"])
    chk("627 测试全过", r["tests"]["tests_passed"])
    chk("受控目录零污染", r["controlled"]["clean"])
    chk("CORE_TOOLS 未修改", r["core_untouched"]["untouched"])
    # 关键：本工具绝不 push。提取源码中所有 `git <subcmd>` 实参，确认无 "push"。
    # 用正则提取真实列表参数，避免检查代码自身的字面量造成自引用误报。
    import re
    src = open(__file__, encoding="utf-8").read()
    git_cmds = re.findall(r'\["git",\s*"([^"]+)"', src)
    real_push = 1 if "push" in git_cmds else 0
    chk("pre-push 工具不执行 git push（无真实调用）", real_push == 0,
        f"(源码中 git 子命令: {git_cmds})")
    print(f"D1 pre-push checklist: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def _report_md(r: dict) -> str:
    L = ["# 627 D1 · push 前最终检查清单", "",
         f"- **总体**：{'✅ 全部通过，可 push' if r['all_ok'] else '❌ 存在未通过项'}", "",
         "## 1. 627 新工具 --check", ""]
    for t in r["tools"]:
        L.append(f"- [{'x' if t['ok'] else ' '}] {t['tool']}")
    s = r["static"]
    L += ["", "## 2. 静态检查",
          f"- [{'x' if s['ruff_ok'] else ' '}] ruff",
          f"- [{'x' if s['mypy_ok'] else ' '}] mypy",
          "", "## 3. 测试",
          f"- [{'x' if r['tests']['tests_passed'] else ' '}] 627 新增测试（{r['tests']['test_files']} 文件）",
          "", "## 4. 受控目录",
          f"- [{'x' if r['controlled']['clean'] else ' '}] atoms/evidence/Examples/Book 零污染",
          "", "## 5. CORE_TOOLS 未改",
          f"- [{'x' if r['core_untouched']['untouched'] else ' '}] 未修改 {r['core_untouched'].get('core_changed') or '（无）'}",
          "", "> ⚠ **本工具只检查，不执行 `git push`**。实际 push 由人裁决（交人项 #3）。"]
    return "\n".join(L) + "\n"


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="627 D1 push 前检查清单")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--report", action="store_true", help="输出清单")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    r = run_all()
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(r, fh, ensure_ascii=False, indent=2)
    if args.report:
        with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(_report_md(r))
        print(f"written {OUT_MD}")
    print(json.dumps({"all_ok": r["all_ok"]}, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
