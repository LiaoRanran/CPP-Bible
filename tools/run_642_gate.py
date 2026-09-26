"""642 D1 · 收工门禁

八项检查：
1. **642 新工具 `--check` 全绿**（10 个：A1–A6 + B2 + B3 + C1 + C2）
2. **641 收尾确认**（`_auto/status.json` 的 `last_completed_batch ≥ 641`；641 工具 `--check` 绿；
   641 验收报告已完成回填）
3. 整目录 ruff（`tools/` + `tests/`）全绿
4. mypy `tools/` = 0 errors
5. 受控目录（atoms/evidence/Examples/Book）零污染
6. **保护器灰度验证**：五保护器联调**零漂移** + 生产判决被改变 **0** + 标记可叠加 / 回滚到底为空
7. **内核零领域 import**（AST 机械证明；641 不变量未被 642 破坏）
8. **CORE_TOOLS / 信任根 / 尺子完整性**（`tool_integrity --check`；判决面零改动）

铁律：不跑监工门禁；`--check` 只读（除报告外不写任何文件）；**未 push、未代签**。
产物：`--report` 写 `data/642_gate_result.md`。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "642_gate_result.md")
PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
CONTROLLED = ("atoms", "evidence", "Examples", "Book")
STATUS = os.path.join(ROOT, "_auto", "status.json")
ACC_641 = os.path.join(ROOT, "data", "641_acceptance_report.md")

#: 本批 642 新工具（均带 --check）
NEW_TOOLS = ("conflict_detector_642", "anti_windup_642", "blind_protocol_642",
             "calibration_tracker_642", "mdl_gate_642", "protector_rollout_642",
             "kernel_minimality_audit_642", "fail_closed_audit_642",
             "auto_executor_whitelist_eval_642", "loop_calibration_642")
#: 641 关键工具（收尾确认要复跑）
TOOLS_641 = ("queyi_core_v10_641", "verifier_closure_641", "queyi_core_cpp_641")


def _run(args: list[str], timeout: int = 900) -> tuple[int, str]:
    try:
        p = subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return p.returncode, (p.stdout + p.stderr).strip()
    except (OSError, subprocess.SubprocessError) as exc:
        return 1, f"{type(exc).__name__}: {exc}"


def check_new_tools() -> dict[str, Any]:
    bad = []
    for name in NEW_TOOLS:
        rc, out = _run([PY, os.path.join("tools", f"{name}.py"), "--check"])
        if rc != 0:
            bad.append(f"{name}: {out[-200:]}")
    return {"ok": not bad, "n_tools": len(NEW_TOOLS),
            "detail": "; ".join(bad) or f"{len(NEW_TOOLS)}/{len(NEW_TOOLS)} --check 绿"}


def check_641_closure() -> dict[str, Any]:
    """641 收尾确认：status 状态 + 641 工具自检 + 验收报告已回填。"""
    problems = []
    try:
        st = json.loads(open(STATUS, encoding="utf-8").read())
        lcb = int(st.get("last_completed_batch", 0))
        if lcb < 641:
            problems.append(f"last_completed_batch={lcb} < 641")
    except (OSError, json.JSONDecodeError, ValueError) as exc:
        problems.append(f"status.json 不可读：{type(exc).__name__}")
    for name in TOOLS_641:
        rc, out = _run([PY, os.path.join("tools", f"{name}.py"), "--check"], timeout=600)
        if rc != 0:
            problems.append(f"{name} --check 红：{out[-120:]}")
    try:
        txt = open(ACC_641, encoding="utf-8", errors="replace").read()
        if "已收尾" not in txt or "58 passed" not in txt:
            problems.append("641 验收报告未回填终验节")
    except OSError as exc:
        problems.append(f"641 报告不可读：{exc}")
    return {"ok": not problems,
            "detail": "; ".join(problems) or
                      f"last_completed_batch≥641 · 641 工具 {len(TOOLS_641)} 个自检绿 · "
                      "验收报告已回填"}


def check_ruff() -> dict[str, Any]:
    rc, out = _run([PY, "-m", "ruff", "check", "tools/", "tests/"])
    return {"ok": rc == 0, "detail": out.splitlines()[-1] if out else ""}


def check_mypy() -> dict[str, Any]:
    rc, out = _run([PY, "-m", "mypy", "tools/"], timeout=900)
    n = out.count(": error:")
    return {"ok": rc == 0 and n == 0, "detail": f"{n} errors"}


def check_controlled() -> dict[str, Any]:
    rc, out = _run(["git", "diff", "--quiet", "--", *CONTROLLED])
    return {"ok": rc == 0, "detail": out or "受控目录零改动"}


def check_protector_rollout() -> dict[str, Any]:
    """五保护器灰度验证：零漂移 + 零判决改变 + 标记可叠加 / 回滚可验证。"""
    try:
        import protector_rollout_642 as rr
        r = rr.rollout()
        marks = dict(r["marks"])
        for pid in rr.PROTECTORS:
            marks = rr.rollback_marks(marks, pid)
        overlap = len([k for p in rr.PROTECTORS for k in rr.MARK_NAMESPACES[p]]) != \
            len({k for p in rr.PROTECTORS for k in rr.MARK_NAMESPACES[p]})
        ok = (r["zero_drift"] and r["critical_changed"] == 0 and marks == {}
              and not overlap)
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "detail": f"{type(exc).__name__}: {exc}"}
    return {"ok": bool(ok),
            "detail": f"漂移 {r['drift'] or '零'}；判决被改变 {r['critical_changed']}；"
                      f"标记键 {len(r['marks'])} 且回滚到底为空；键空间互不重叠={not overlap}"}


def check_kernel_purity() -> dict[str, Any]:
    try:
        import queyi_core_v10_641 as core
        hits = core.verify_no_domain_imports(os.path.join(HERE, "queyi_core_v10_641.py"))
    except Exception as exc:  # noqa: BLE001
        return {"ok": False, "detail": f"{type(exc).__name__}: {exc}"}
    return {"ok": hits == [], "detail": f"领域 import：{hits or '零'}"}


def check_integrity() -> dict[str, Any]:
    """CORE_TOOLS / 信任根 / Merkle / 尺子完整性（判决面零改动）。"""
    rc, out = _run([PY, os.path.join("tools", "tool_integrity.py"), "--check"], timeout=600)
    tail = [ln for ln in out.splitlines() if ln.strip()][-4:]
    return {"ok": rc == 0, "detail": " / ".join(t.strip() for t in tail)[:240]}


def build() -> dict[str, Any]:
    checks = {
        "642 新工具 --check": check_new_tools(),
        "641 收尾确认": check_641_closure(),
        "ruff 全绿": check_ruff(),
        "mypy 0 errors": check_mypy(),
        "受控目录零污染": check_controlled(),
        "保护器灰度验证（零漂移/零改判/可回滚）": check_protector_rollout(),
        "内核零领域 import（AST）": check_kernel_purity(),
        "CORE_TOOLS/信任根/尺子完整性": check_integrity(),
    }
    return {"checks": checks, "all_ok": all(v["ok"] for v in checks.values())}


def write_report(r: dict[str, Any]) -> str:
    c = r["checks"]
    lines = ["# 642 D1 · 收工门禁结果", "",
             "| # | 检查 | 结果 | 详情 |", "|---|---|---|---|"]
    for i, (k, v) in enumerate(c.items(), 1):
        lines.append(f"| {i} | {k} | {'✅' if v['ok'] else '❌'} | {v['detail']} |")
    lines += ["", f"**总判定**：{'全部通过 ✅' if r['all_ok'] else '存在未过项 ❌'}",
              "", "> 本门禁**不跑监工门禁**、**未 push**、**未代签**；"
                  "受控目录零污染为实测项。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return OUT_MD


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="642 收工门禁")
    ap.add_argument("--check", action="store_true", help="只读自检（默认）")
    ap.add_argument("--report", action="store_true", help="写门禁结果报告")
    a = ap.parse_args(argv)
    r = build()
    for k, v in r["checks"].items():
        print(f"  [{'ok' if v['ok'] else 'FAIL'}] {k} — {v['detail']}")
    print(f"D1 gate: {'PASS' if r['all_ok'] else 'FAIL'}")
    if a.report:
        print(f"written {write_report(r)}")
    return 0 if r["all_ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
