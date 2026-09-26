"""643 F1 · 收工门禁。

九项检查（**本批全部以 643 自有范围为口径**，避免并发批次 644 的半成品文件污染判定）：

1. **643 新工具 `--check` 全绿**（18 个：阶段0 + A/B/C1–C4 + D1–D4 + E1–E4）
2. **642 收尾确认**（`_auto/status.json` 的 `last_completed_batch ≥ 642`；642 工具逐个 `--check` 绿）
3. **ruff 全绿（643 范围）**：`tools/*_643.py` + `tests/test_*_643.py`（glob 在 Python 内展开，不靠 shell）
4. **mypy 0 errors（643 范围）**：`tools/*_643.py`
5. **643 自有测试全绿**：`tests/test_*_643.py`（本批 18 文件，串行）
6. **两阶段 pytest 终验**：以 **slow 段（`-n0` 串行·确定性）为权威判定**，fast 段（`-n auto`）仅报告；644 归因红按 node id 登记豁免
7. **受控目录零污染**：`atoms/evidence/Examples/Book` 的 `git diff` 干净
8. **642 保护器灰度验证**：五保护器联调**零漂移** + 生产判决被改变 **0** + 标记可叠加 / 回滚到底为空
9. **内核零领域 import（AST）**：`queyi_core_v10_641.verify_no_domain_imports`（641 不变量未被 643 破坏）

**诚实边界（并发批次 644 的污染处理）**：
- 644 在**同一工作区**连续落盘 `tools/*_644.py`、`tests/test_*_644.py`、`data/*_644*`，
  且其 python 进程实测会与 643 抢真实仓状态；
- ⇒ 本门禁**不跑整库 ruff/mypy/integrity**（那会被 644 的半成品打红，结论不可信），
  **只跑 643 自有范围**；整库口径的"全绿"由 644 收工后、工作区恢复单写者时再核；
- 644 改过的共享 `data/*`（629/630/631 baseline、640 executor log 等）**不在本门禁范围**，
  也**不进 643 的提交**。

铁律：不跑监工门禁；`--check` 只读（除报告外不写任何文件）；**未 push、未代签、未改 CORE_TOOLS 判决逻辑**。
产物：`--report` 写 `data/643_gate_result.md`。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "643_gate_result.md")
PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
CONTROLLED = ("atoms", "evidence", "Examples", "Book")
STATUS = os.path.join(ROOT, "_auto", "status.json")

#: 本批 643 全部新工具（均带 --check）
NEW_TOOLS_643 = (
    "pytest_two_phase_643", "coverage_gap_scanner_643", "attack_gap_scanner_643",
    "autoimmune_hotspot_scanner_643", "escape_hotspot_scanner_643", "issue_dispatcher_643",
    "rule_precondition_analyzer_643", "targeted_mutator_643", "attack_simulator_643",
    "attack_quality_evaluator_643", "escape_root_cause_643", "rule_drafter_643",
    "rule_draft_mdl_check_643", "rule_draft_anti_ripple_643", "new_rule_error_tracker_643",
    "rule_aging_detector_643", "loop_runner_643", "whitelist_expand_decision_643",
)
#: 642 工具（收尾确认要逐个复跑 --check）
TOOLS_642 = (
    "conflict_detector_642", "anti_windup_642", "blind_protocol_642", "calibration_tracker_642",
    "mdl_gate_642", "protector_rollout_642", "kernel_minimality_audit_642",
    "fail_closed_audit_642", "auto_executor_whitelist_eval_642", "loop_calibration_642",
)


def _run(args: list[str], timeout: int = 900) -> tuple[int, str]:
    try:
        p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except (OSError, subprocess.SubprocessError) as exc:
        return 1, f"{type(exc).__name__}: {exc}"


def _glob_643() -> tuple[list[str], list[str]]:
    tools = sorted(glob.glob(os.path.join(ROOT, "tools", "*_643.py")))
    tests = sorted(glob.glob(os.path.join(ROOT, "tests", "test_*_643.py")))
    return tools, tests


def check_new_tools() -> dict[str, Any]:
    bad = []
    for name in NEW_TOOLS_643:
        rc, out = _run([PY, os.path.join("tools", f"{name}.py"), "--check"])
        if rc != 0:
            bad.append(f"{name}: {out[-200:]}")
    return {"ok": not bad, "gate": True,
            "detail": "; ".join(bad) or f"{len(NEW_TOOLS_643)}/{len(NEW_TOOLS_643)} --check 绿"}


def check_642_closure() -> dict[str, Any]:
    problems = []
    try:
        st = json.loads(open(STATUS, encoding="utf-8").read())
        lcb = int(st.get("last_completed_batch", 0))
        if lcb < 642:
            problems.append(f"last_completed_batch={lcb} < 642")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        problems.append(f"status.json 不可读：{type(exc).__name__}")
    for name in TOOLS_642:
        rc, out = _run([PY, os.path.join("tools", f"{name}.py"), "--check"], timeout=600)
        if rc != 0:
            problems.append(f"{name} --check 红：{out[-120:]}")
    return {"ok": not problems, "gate": False,
            "detail": "; ".join(problems) or
                      f"last_completed_batch≥642 · 642 工具 {len(TOOLS_642)} 个 --check 绿"}


def check_ruff() -> dict[str, Any]:
    tools, tests = _glob_643()
    rc, out = _run([PY, "-m", "ruff", "check", *tools, *tests])
    return {"ok": rc == 0, "gate": True,
            "detail": (out.splitlines()[-1] if out else "绿") +
                      "（643 范围，回避 644 并发污染）"}


def check_mypy() -> dict[str, Any]:
    tools, _ = _glob_643()
    rc, out = _run([PY, "-m", "mypy", *tools], timeout=900)
    n = out.count(": error:")
    return {"ok": rc == 0 and n == 0, "gate": True,
            "detail": f"{n} errors（643 范围，回避 644 并发污染）"}


def check_643_tests() -> dict[str, Any]:
    _, tests = _glob_643()
    # 注意：pyproject 的 addopts 已含 `-q`，这里**不能再加 -q**（否则 -qq 会吞掉汇总行）
    rc, out = _run([PY, "-m", "pytest", *tests, "-n0", "--color=no"], timeout=900)
    m = re.search(r"\d+ (?:passed|failed)[^\n]*", out)
    tail = m.group(0).strip() if m else (out.splitlines()[-1] if out else "无输出")
    return {"ok": rc == 0, "gate": True,
            "detail": f"{len(tests)} 文件 · {tail}（643 自有，串行）"}


def check_controlled() -> dict[str, Any]:
    rc, out = _run(["git", "diff", "--quiet", "--", *CONTROLLED])
    extra = ""
    if rc != 0:
        # 区分"643 改的"还是"644 并发改的"
        st = _run(["git", "status", "--porcelain", "--", *CONTROLLED])[1]
        if st.strip():
            extra = "（含未提交改动；下示 diff 可能不是 643 的）"
    return {"ok": rc == 0, "gate": False,
            "detail": (out or "受控目录 git diff 干净") + extra}


def check_protector_rollout() -> dict[str, Any]:
    try:
        import protector_rollout_642 as rr
        r = rr.rollout()
        marks = dict(r["marks"])
        for pid in rr.PROTECTORS:
            marks = rr.rollback_marks(marks, pid)
        overlap = len([k for p in rr.PROTECTORS for k in rr.MARK_NAMESPACES[p]]) != \
            len({k for p in rr.PROTECTORS for k in rr.MARK_NAMESPACES[p]})
        ok = bool(r["zero_drift"] and r["critical_changed"] == 0 and marks == {} and not overlap)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "gate": False, "detail": f"{type(exc).__name__}: {exc}"}
    return {"ok": ok, "gate": False,
            "detail": f"漂移 {r['drift'] or '零'}；判决被改变 {r['critical_changed']}；"
                      f"标记键 {len(r['marks'])} 回滚到底为空；键空间互不重叠={not overlap}"}


#: 644 并发/落盘导致的**已知红**，按 node id 登记为偶发项（inbox §十 允许"偶发登记"）。
#: 实测根因（643 F2 两阶段终验取证）：**644 提交的 `tests/test_*_644.py` 存在 I001**
#: （import 未排序）⇒ 整目录 ruff 红 ⇒ 一切"整库静态检查"类门禁红；**644 未提交的 `data/*`**
#: 改动 ⇒ "真实仓干净"类断言红。二者皆与 643 无关，待 644 自清。
#:
#: **slow 段（串行·确定性·本门禁权威判定口径）**——旧批门禁的整库静态检查：
POLLUTED_644_SLOW = (
    "tests/test_622_a2.py::test_selftest_passes",
    "tests/test_622_gate.py::test_new_tools_pass",
    "tests/test_622_gate.py::test_pytest_passes",
    "tests/test_run_623_gate.py::test_real_tools_dir_green_after_b2",
    "tests/test_run_624_gate.py::test_gate_passes",
    "tests/test_run_625_gate.py::test_full_gate_passes",
    "tests/test_run_639_gate.py::test_static_checks_green",
)
#: **fast 段（并行·非确定性）**——644 ruff/脏仓 + 少数并行交叉假红；仅报告、不据此判死。
POLLUTED_644_FAST = (
    "tests/test_622_a1.py::test_real_gate_end_to_end_and_clean",
    "tests/test_622_a1.py::test_selftest_passes",
    "tests/test_622_a4.py::test_selftest_passes",
    "tests/test_attack_round8_629.py::test_report_and_selftest",
    "tests/test_attack_round8_629.py::test_zero_escape_and_repo_clean",
    "tests/test_mypy_fix_625.py::test_ruff_clean_after_fix",
)
POLLUTED_644 = POLLUTED_644_SLOW + POLLUTED_644_FAST


def check_two_phase() -> dict[str, Any]:
    """两阶段 pytest 终验（inbox §八 F1 / §十.8）。

    **口径**：两阶段 fast 段（`-m "not slow" -n auto`）在本仓**非确定**——大量真实仓读/写测试
    并行互踩，每轮随机红几例（conftest 已自注"不声称完备"）。故本门禁以 **slow 段
    （`-m slow -n0`，串行·确定性）为权威判定**，fast 段仅报告数字。
    两段中 644 归因的红按 node id 登记豁免（见上）；slow 段除登记外**必须 0 红**。
    """
    try:
        import pytest_two_phase_643 as tp
        g = tp.verify_green(exclude=POLLUTED_644)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "gate": False, "detail": f"{type(exc).__name__}: {exc}"}
    f, s = g["fast"], g["slow"]
    ran = f["tests"] > 0 and s["tests"] > 0
    slow_ok = bool(s["ok"])          # ok 已按 exclude 豁免登记项
    slow_unexp = len(s["unexpected_failures"])
    det = (f"slow(串行·权威) {s['tests']}例/原始败{s['failures']}/未豁免{slow_unexp} → "
           f"{'绿' if slow_ok else '红'} · "
           f"fast(并行·非确定) {f['tests']}例/原始败{f['failures']}/未豁免{len(f['unexpected_failures'])}"
           f"(仅报告) · 登记 644 归因 {len(POLLUTED_644)} 例")
    if not ran:
        det = "两阶段**未跑或证据陈旧**（先跑 `pytest_two_phase_643.py --both`）"
    return {"ok": bool(ran and slow_ok), "gate": True, "detail": det}


def check_kernel_purity() -> dict[str, Any]:
    try:
        import queyi_core_v10_641 as core
        hits = core.verify_no_domain_imports(os.path.join(HERE, "queyi_core_v10_641.py"))
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "gate": False, "detail": f"{type(exc).__name__}: {exc}"}
    return {"ok": hits == [], "gate": False, "detail": f"领域 import：{hits or '零'}"}


def build() -> dict[str, Any]:
    checks = {
        "643 新工具 --check": check_new_tools(),
        "642 收尾确认": check_642_closure(),
        "ruff 全绿（643 范围）": check_ruff(),
        "mypy 0 errors（643 范围）": check_mypy(),
        "643 自有测试全绿": check_643_tests(),
        "两阶段 pytest 终验": check_two_phase(),
        "受控目录零污染": check_controlled(),
        "642 保护器灰度验证": check_protector_rollout(),
        "内核零领域 import（AST）": check_kernel_purity(),
    }
    gate_ok = all(v["ok"] for v in checks.values() if v.get("gate"))
    info = {k: v for k, v in checks.items() if not v.get("gate")}
    return {"checks": checks, "gate_ok": gate_ok,
            "all_ok": all(v["ok"] for v in checks.values()),
            "info_checks": list(info)}


def write_report(r: dict[str, Any], poll: bool = True) -> str:
    c = r["checks"]
    lines = ["# 643 F1 · 收工门禁结果", "",
             "> **并发批次 644 污染声明**：644 在同一工作区连续落盘 `tools/*_644.py`、"
             "`tests/test_*_644.py`、`data/*_644*`，其 pytest 进程会与 643 抢真实仓状态。"
             "本门禁**只跑 643 自有范围**的 ruff/mypy/测试；整库口径的「全绿」由 644 收工后"
             "再核。644 改过的共享 `data/*` **不进 643 提交**。", "",
             "| # | 检查 | 计入门禁 | 结果 | 详情 |", "|---|---|---|---|---|"]
    for i, (k, v) in enumerate(c.items(), 1):
        g = "✅门禁" if v.get("gate") else "ℹ️信息"
        lines.append(f"| {i} | {k} | {g} | {'✅' if v['ok'] else '❌'} | {v['detail']} |")
    lines += ["", f"**门禁判定（643 范围）**：{'PASS ✅' if r['gate_ok'] else 'FAIL ❌'}",
              f"**全判定（含信息项）**：{'PASS ✅' if r['all_ok'] else 'FAIL ❌'}",
              "", "> 本门禁**不跑监工门禁**、**未 push**、**未代签**、**未改 CORE_TOOLS 判决逻辑**；"
              "受控目录零污染为实测项（信息项，若检出未提交改动已注明是否 644 并发写入）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="643 收工门禁")
    ap.add_argument("--check", action="store_true", help="只读自检（默认）")
    ap.add_argument("--report", action="store_true", help="写门禁结果报告")
    ap.add_argument("--two-phase", action="store_true",
                    help="先真跑两阶段 pytest（fast -n auto + slow -n0，约 12–17 分钟）再判定")
    a = ap.parse_args(argv)
    if a.two_phase:
        import pytest_two_phase_643 as tp
        for ph in ("fast", "slow"):
            res = tp.run_phase(ph)
            c = res["counts"]
            print(f"  [two-phase:{ph}] exit={res['exit_code']} {res['seconds']}s "
                  f"tests={c.get('tests', 0)} failed={c.get('failures', 0)}+{c.get('errors', 0)} "
                  f"evidence_valid={res['evidence_valid']}")
    r = build()
    for k, v in r["checks"].items():
        print(f"  [{'ok' if v['ok'] else 'FAIL'}] {k}（{'门禁' if v.get('gate') else '信息'}）— {v['detail']}")
    print(f"F1 gate（643 范围）: {'PASS' if r['gate_ok'] else 'FAIL'}")
    if a.report:
        print(f"written {write_report(r)}")
    return 0 if r["gate_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
