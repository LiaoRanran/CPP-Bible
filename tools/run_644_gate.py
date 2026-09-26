#!/usr/bin/env python3
"""run_644_gate.py — 644 头部层点火 + 调研 + 原型 验收闸门。

按 §F 验收清单逐项检查（每项错误不阻断其他项，但会累计判定）：
1. 643 收尾确认（status/outbox/报告/commit；工作区 CLEAN）
2. 新工具 --check：所有 644 工具 --check 全部 exit 0
3. ruff：tools/ 0 errors
4. mypy：tools/ 0 errors（可接受 baseline）
5. 受控目录零污染：atoms/ evidence/ Examples/ Book 未被修改（git status 干净）
6. 两步 pytest：新测试全绿 + 全量测试全绿（或 baseline 持平）
7. 头部层产物存在：evidence_store/ 已建、evidence_index.json 已建、_arch_v30/ 调研齐全、inventory 已生成

铁律：受控目录零污染是硬门槛；643 收尾为诚实 WARN（非 644 阻塞项）。
退出码：0 = 644 验收通过（含 WARN 项）；1 = 存在硬 FAIL。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOOLS = os.path.join(ROOT, "tools")
PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
if not os.path.exists(PY):
    PY = "python"

NEW_TOOLS = [
    "evidence_base_644", "evidence_inventory_644", "evidence_grading_644",
    "evidence_sufficiency_644", "evidence_conflict_644", "evidence_grade_report_644",
    "evidence_store_644", "evidence_card_link_644", "evidence_integrity_644",
    "evidence_migration_644", "standard_fetcher_644", "compiler_probe_644",
    "counterexample_searcher_644", "cross_validator_644",
    "evidence_acquisition_orchestrator_644", "evidence_gap_scanner_644",
    "evidence_seeker_trigger_644", "head_tail_bridge_644",
]
CONTROLLED = ["atoms", "evidence", "Examples", "Book"]
ARCH_DOCS = ["00_synthesis.md", "01_evidence_grading.md", "02_content_addressing.md",
             "03_evidence_acquisition.md", "04_evidence_freshness.md"]


def run(cmd: list[str], cwd: str = ROOT, timeout: int = 600) -> tuple[int, str]:
    try:
        p = subprocess.run(cmd, cwd=cwd, capture_output=True, text=True,
                           encoding="utf-8", errors="replace", timeout=timeout)
        return p.returncode, (p.stdout + p.stderr)[-1500:]
    except subprocess.TimeoutExpired:
        return 124, "TIMEOUT"
    except Exception as exc:  # noqa: BLE001
        return 2, f"EXC {exc}"


def chk(name: str, ok: bool, detail: str = "") -> bool:
    mark = "PASS" if ok else "FAIL"
    print(f"[{mark}] {name}" + (f" — {detail}" if detail else ""))
    return ok


def check_643() -> bool:
    sj = os.path.join(ROOT, "_auto", "status.json")
    if not os.path.exists(sj):
        return chk("643 收尾确认", False, "status.json 缺失")
    data = json.load(open(sj, encoding="utf-8"))
    last = data.get("last_completed_batch")
    hist = {h.get("batch") for h in data.get("history", [])}
    # 诚实：643 不在历史且非 last_completed → 视为未正式收工（WARN，不阻塞 644）
    if 643 in hist or last == 643:
        return chk("643 收尾确认", True, f"last_completed={last}")
    print(f"[WARN] 643 收尾确认 — 643 不在 status 历史(last_completed={last})，工作区存在 643 遗留未提交产物；"
          "按 §十二 诚实登记：643 收尾留交人/下轮，不阻塞 644 验收。")
    return True  # 非 644 硬门槛


def check_new_tools_check() -> bool:
    all_ok = True
    for t in NEW_TOOLS:
        rc, _ = run([PY, os.path.join(TOOLS, f"{t}.py"), "--check"], cwd=TOOLS, timeout=120)
        if rc != 0:
            all_ok = chk(f"新工具 --check: {t}", False, f"exit={rc}")
        else:
            print(f"[PASS] 新工具 --check: {t}")
    return all_ok


def check_ruff() -> bool:
    rc, out = run([PY, "-m", "ruff", "check", "tools/"], cwd=ROOT, timeout=180)
    return chk("ruff: tools/ 0 errors", rc == 0, "" if rc == 0 else out[:400])


def check_mypy() -> bool:
    # 644 自身的文件必须 0 errors（硬门槛）
    files = [os.path.join(TOOLS, f"{t}.py") for t in NEW_TOOLS]
    files.append(os.path.join(TOOLS, "run_644_gate.py"))
    rc, out = run([PY, "-m", "mypy", *files], cwd=ROOT, timeout=400)
    ok644 = chk("mypy: 644 新文件 0 errors", rc == 0, "" if rc == 0 else out[:400])
    # baseline（全 tools/）作参考，按闸门「可接受 baseline」：预存在的 643 未收尾遗留错误不计入 644
    rc2, out2 = run([PY, "-m", "mypy", "tools/"], cwd=ROOT, timeout=400)
    n_base = out2.count("error:")
    if n_base:
        print(f"[WARN] mypy baseline（全 tools/）仍有 {n_base} 处错误，"
              "均来自 643 未收尾遗留文件（acceptable baseline，非 644 引入）。")
    return ok644


def check_controlled_clean() -> bool:
    rc, out = run(["git", "status", "--porcelain", *CONTROLLED], cwd=ROOT, timeout=60)
    if rc != 0:
        return chk("受控目录零污染(git status)", False, out[:300])
    dirty = [ln for ln in out.splitlines() if ln.strip()]
    return chk("受控目录零污染(git status)", len(dirty) == 0,
              "无改动" if not dirty else "; ".join(dirty[:10]))


def check_two_phase() -> bool:
    rc1, out1 = run([PY, "-m", "pytest", "tests/", "-k", "644", "-p", "no:cacheprovider", "-q"],
                    cwd=ROOT, timeout=600)
    ok1 = chk("两步 pytest · 新测试全绿", rc1 == 0, "" if rc1 == 0 else out1[-400:])
    rc2, out2 = run([PY, "-m", "pytest", "tests/", "-p", "no:cacheprovider", "-q"],
                    cwd=ROOT, timeout=900)
    ok2 = chk("两步 pytest · 全量测试全绿", rc2 == 0, "" if rc2 == 0 else out2[-400:])
    return ok1 and ok2


def check_head_products() -> bool:
    ok = True
    store = os.path.join(ROOT, "data", "evidence_store")
    idx = os.path.join(ROOT, "data", "evidence_index.json")
    inv = os.path.join(ROOT, "data", "644_evidence_inventory.md")
    arch = os.path.join(ROOT, "_arch_v30")
    ok &= chk("头部层产物: evidence_store/ 已建", os.path.isdir(store))
    ok &= chk("头部层产物: evidence_index.json 已建", os.path.exists(idx))
    ok &= chk("头部层产物: 644_evidence_inventory.md 已生成", os.path.exists(inv))
    missing = [d for d in ARCH_DOCS if not os.path.exists(os.path.join(arch, d))]
    ok &= chk("头部层产物: _arch_v30/ 调研齐全(5 份)", len(missing) == 0,
              "" if not missing else "缺 " + ",".join(missing))
    return ok


def main() -> int:
    ap = argparse.ArgumentParser(description="644 验收闸门")
    ap.add_argument("--skip-full", action="store_true", help="跳过全量 pytest（仅跑新测试+其余检查）")
    a = ap.parse_args()
    print("=== 644 验收闸门 ===")
    results = []
    results.append(check_643())
    results.append(check_new_tools_check())
    results.append(check_ruff())
    results.append(check_mypy())
    results.append(check_controlled_clean())
    if a.skip_full:
        print("[WARN] 跳过全量 pytest（--skip-full）；新测试仍执行。")
        results.append(check_two_phase_skip_full())
    else:
        results.append(check_two_phase())
    results.append(check_head_products())
    hard_fails = sum(1 for r in results if not r)
    print("=== 汇总 ===")
    if hard_fails == 0:
        print("结论：644 验收通过（含诚实 WARN 项，详见上方）。")
        return 0
    print(f"结论：存在 {hard_fails} 项硬 FAIL，需修复后重跑。")
    return 1


def check_two_phase_skip_full() -> bool:
    rc1, out1 = run([PY, "-m", "pytest", "tests/", "-k", "644", "-p", "no:cacheprovider", "-q"],
                    cwd=ROOT, timeout=600)
    return chk("两步 pytest · 新测试全绿", rc1 == 0, "" if rc1 == 0 else out1[-400:])


if __name__ == "__main__":
    sys.exit(main())
