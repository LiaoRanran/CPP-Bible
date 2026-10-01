#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""fast_gate.py — 批次回归的**快速门禁**（目标 < 5 分钟）。

病（672f 实测）
==============
全量 `pytest -m "not slow"` 在 Windows 上 17 分钟只跑到 27%（estimated 60+ 分钟），
但每一批真正需要的**关键路径验证**只有三件：

  1. 三道交付门禁：658（L0 5/5）、669d（率一致性等六条规则）、671a guard（三方数字一致）；
  2. 本批新增/受影响的测试文件（`--tests` 指定）；
  3. 若本批动了 `web/`：前端自测 `node web/run_tests.mjs`。

本工具把这三件事跑成一个**一次调用、逐项计时、FAIL 给证据**的命令，避免每批都烧一小时。

与全量回归的关系（**不许漏测**）
================================
* `--all` = 全部门禁 + **全部 `-m "not slow"` 测试**（即 CI 快档同口径）；
* 被 `@pytest.mark.slow` 排除的测试（单测 >10s：WSL 编译类、全量变异、全量重跑）
  由 CI 的 `-m slow` 档覆盖 —— 本地不做，但**不静默**：报告里显形已跳过的数量；
* 结论口径：fast_gate PASS ≠ 全量 PASS；它保证的是"本批关键路径 + 门禁灯"。

用法
====
    python tools/fast_gate.py --tests tests/test_fast_gate.py          # 门禁 + 本批测试
    python tools/fast_gate.py --all                                    # 门禁 + 全部非 slow 测试
    python tools/fast_gate.py --all --skip-frontend                    # 只跑 Python 门禁
    python tools/fast_gate.py --tests a.py b.py --json                 # 机读输出

并行
====
* `--all` 默认 `-n auto`（pytest-xdist；pyproject 508 复盘：`not slow` 档并行安全）；
* `--tests` 默认串行（本批文件可能触碰共享仓库状态，串行最稳）；
* `--jobs 0` 强制串行、`--jobs N` 指定核数；xdist 不可用时自动落回串行并显形。
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

#: 单步超时（秒）：门禁类是"读产物+纯计算"，给 300；pytest 类给 900（--all 目标 <15 分钟）
DEFAULT_TIMEOUT_GATE = 300.0
DEFAULT_TIMEOUT_TESTS = 900.0

#: 总耗时预算（秒）—— 超过只 WARN（可见），不判红
BUDGET_S = 300.0

GATES = (
    ("658 门禁（L0 5/5 + S5/S6）", [sys.executable, "tools/run_658_gate.py"]),
    ("669d 门禁（六条 P0 规则）", [sys.executable, "tools/run_669d_gate.py"]),
    ("671a guard（三方数字一致）", [sys.executable, "tools/guard_rerun_671a.py"]),
)

FRONTEND_CMD = ["node", "web/run_tests.mjs"]


def _run(name: str, cmd: list[str], timeout: float) -> dict:
    """跑一条命令，返回 {name, cmd, rc, seconds, tail}。超时 rc=-9。"""
    t0 = time.monotonic()
    try:
        p = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True,
                           errors="replace", timeout=timeout)
        rc, out = p.returncode, (p.stdout or "") + (p.stderr or "")
    except subprocess.TimeoutExpired:
        rc, out = -9, f"[timeout] 超过 {timeout:.0f}s 未结束"
    except OSError as e:                     # 命令不存在等
        rc, out = -8, f"[oserror] {e}"
    secs = time.monotonic() - t0
    lines = [ln for ln in out.strip().splitlines() if ln.strip()]
    return {"name": name, "cmd": " ".join(cmd), "rc": rc,
            "seconds": round(secs, 2), "tail": lines[-15:]}


def _fail_summary(item: dict) -> str:
    """从输出尾部提取最有信息量的行（含 FAIL/BLOCK/error 的优先）。"""
    keys = ("FAIL", "BLOCK", "ERROR", "Error", "error", "✗", "❌")
    hot = [ln for ln in item["tail"] if any(k in ln for k in keys)]
    pick = hot[-8:] if hot else item["tail"][-5:]
    return "\n".join("      " + ln for ln in pick)


def run_gates(timeout: float = DEFAULT_TIMEOUT_GATE) -> list[dict]:
    return [_run(name, cmd, timeout) for name, cmd in GATES]


def _xdist_available() -> bool:
    return importlib.util.find_spec("xdist") is not None


def run_tests(test_files: list[str], all_fast: bool,
              timeout: float = DEFAULT_TIMEOUT_TESTS,
              jobs: str = "", ) -> dict:
    """跑 pytest。all_fast ⇒ 全部非 slow；否则只跑指定文件（也带 not slow 过滤）。

    jobs："" ⇒ 自动（--all 并行 / --tests 串行）；"0" ⇒ 串行；"auto"/"N" ⇒ 显式。
    """
    if all_fast:
        base, name = ["tests"], "pytest（全部非 slow）"
    elif test_files:
        base, name = list(test_files), "pytest（本批指定）"
    else:
        return {"name": "pytest（未指定，跳过）", "cmd": "", "rc": 0,
                "seconds": 0.0, "tail": ["--tests 未给文件且未 --all ⇒ 本项跳过"],
                "skipped": True}
    jobs = jobs or ("auto" if all_fast else "0")
    cmd = [sys.executable, "-m", "pytest", *base, "-q", "-m", "not slow",
           "-p", "no:cacheprovider"]
    note = ""
    if jobs != "0":
        if _xdist_available():
            cmd += ["-n", jobs]
            name += f"（xdist -n {jobs}）"
        else:
            note = "xdist 不可用 ⇒ 落回串行（显形，不静默）"
    item = _run(name, cmd, timeout)
    item["cmd"] = " ".join(cmd)
    if note:
        item["tail"].append(f"[note] {note}")
    if any("deselected" in ln for ln in item["tail"]):
        item["tail"].append("[note] 有 slow 标记测试被过滤 —— 它们由 CI 的 -m slow 档覆盖")
    return item


def run_frontend(skip: bool, timeout: float = DEFAULT_TIMEOUT_GATE,
                 web_dirty: bool | None = None) -> dict:
    if skip:
        return {"name": "前端自测（--skip-frontend）", "cmd": "", "rc": 0, "seconds": 0.0,
                "tail": ["按参数跳过"], "skipped": True}
    runner = ROOT / "web" / "run_tests.mjs"
    if not runner.is_file():
        return {"name": "前端自测（web/run_tests.mjs 不存在）", "cmd": "", "rc": 0,
                "seconds": 0.0, "tail": ["未找到 web/run_tests.mjs ⇒ 跳过（显形，不静默）"],
                "skipped": True}
    if shutil.which("node") is None:
        return {"name": "前端自测（node 不在 PATH）", "cmd": "", "rc": 0, "seconds": 0.0,
                "tail": ["node 不可用 ⇒ 跳过（显形，不静默）"], "skipped": True}
    note = ""
    if web_dirty is False:
        note = "（web/ 无未提交改动，仍执行以保一致）"
    item = _run("前端自测 node web/run_tests.mjs" + note, FRONTEND_CMD, timeout)
    return item


def web_has_changes() -> bool | None:
    """web/ 是否有未提交改动（None=无法判断）。仅作提示，不改变执行。"""
    try:
        p = subprocess.run(["git", "status", "--porcelain", "--", "web/"],
                           cwd=str(ROOT), capture_output=True, text=True, timeout=30)
        if p.returncode != 0:
            return None
        return bool(p.stdout.strip())
    except Exception:                        # noqa: BLE001
        return None


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="快速门禁（目标 <5 分钟）")
    ap.add_argument("--tests", nargs="*", default=[], help="本批新增/受影响的测试文件")
    ap.add_argument("--all", action="store_true", help="跑全部快速门禁（含全部非 slow 测试）")
    ap.add_argument("--skip-frontend", action="store_true", help="跳过前端自测")
    ap.add_argument("--json", action="store_true", help="机读输出")
    ap.add_argument("--timeout", type=float, default=None, help="单步超时秒（默认门禁 300/测试 900）")
    ap.add_argument("--jobs", default="", help='pytest 并行：""=自动、"0"=串行、"auto"/N')
    a = ap.parse_args(argv)

    t0 = time.monotonic()
    tg = a.timeout or DEFAULT_TIMEOUT_GATE
    tt = a.timeout or DEFAULT_TIMEOUT_TESTS
    items: list[dict] = []
    items += run_gates(tg)
    items.append(run_tests(a.tests, a.all, tt, jobs=a.jobs))
    items.append(run_frontend(a.skip_frontend, tg, web_has_changes()))
    total = round(time.monotonic() - t0, 2)

    failed = [i for i in items if i["rc"] != 0]
    ok = not failed
    over = total > BUDGET_S

    if a.json:
        print(json.dumps({"ok": ok, "total_seconds": total, "over_budget": over,
                          "items": items}, ensure_ascii=False, indent=2))
    else:
        print("[fast-gate] 快速门禁")
        for i in items:
            tag = "SKIP" if i.get("skipped") else ("PASS" if i["rc"] == 0 else "FAIL")
            print(f"  [{tag:4}] {i['name']}  {i['seconds']:.1f}s")
            if i["rc"] != 0:
                print(f"          cmd: {i['cmd']}")
                print(_fail_summary(i))
                print(f"          rc={i['rc']}")
        print(f"[fast-gate] overall={'PASS' if ok else 'FAIL'}  总耗时 {total:.1f}s"
              f"（预算 {BUDGET_S:.0f}s{ '，超预算 ⚠️' if over else '' }）")
        if ok and over:
            print("[fast-gate] ⚠️ 通过但超预算：请检查是否漏打 slow 标记")
        print("[fast-gate] 说明：慢档（@pytest.mark.slow：WSL 编译/全量变异/全量重跑）由 CI 的 "
              "-m slow 覆盖，本地不跑，亦不静默。")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
