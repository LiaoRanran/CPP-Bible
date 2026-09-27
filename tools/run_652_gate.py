#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""run_652_gate.py — 652 收工门禁（两阶段 pytest + ruff/mypy + 保护器联调 + 信任根 + 零污染）。

阶段：
1. fast pytest（-m 'not slow'）→ 2. full pytest
3. ruff / mypy（652 文件）→ 4. 各 652 工具 --check
5. **保护器联调**：调 queyi-core `protector_rollout_652 --verify`（差分真验证，B7-B10 灰度上岗）
6. 受控 atoms 指纹（前后一致=零污染）
7. 信任根 `tool_integrity --check`（闭包未破）

用法：python tools/run_652_gate.py [--fast-only]
"""
from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
QUEYI = ROOT.parent.parent / "queyi-core"   # C:\CodeLearnling\note\note\queyi-core

NEW_TESTS = ["tests/test_652_tools.py", "tests/test_core_pbt_651.py"]
NEW_TOOLS = [
    "tools/backfill_verified_at_652.py", "tools/handoff_auto_652.py", "tools/probe_assembler_652.py",
    "tools/esbmc_falsify_652.py", "tools/challenger_652.py", "tools/embedded_adapter_652.py",
    "tools/rats_closure_652.py", "tools/pck_export_652.py", "tools/run_652_gate.py",
]
SELFTESTS = NEW_TOOLS[:8]


def _run(label: str, cmd: list[str], cwd: Path = ROOT) -> bool:
    print(f"\n=== {label} ===\n$ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=str(cwd), check=False)
    print(f"--- {label}: {'PASS' if r.returncode == 0 else 'FAIL'} (exit={r.returncode})")
    return r.returncode == 0


def _atoms_fp() -> str:
    h = hashlib.sha256()
    for p in sorted((ROOT / "atoms").rglob("*.md")):
        h.update(str(p.relative_to(ROOT)).encode())
        h.update(hashlib.sha256(p.read_bytes()).digest())
    return h.hexdigest()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="652 收工门禁")
    ap.add_argument("--fast-only", action="store_true")
    a = ap.parse_args(argv)
    py = sys.executable
    res: dict[str, bool] = {}

    res["fast"] = _run("阶段1 fast pytest(-m 'not slow')",
                       [py, "-m", "pytest", *NEW_TESTS, "-q", "-m", "not slow", "-p", "no:cacheprovider"])
    if not a.fast_only:
        res["full"] = _run("阶段2 full pytest",
                           [py, "-m", "pytest", *NEW_TESTS, "-q", "-p", "no:cacheprovider"])
        res["ruff"] = _run("阶段3a ruff（652 文件）", [py, "-m", "ruff", "check", *NEW_TOOLS])
        res["mypy"] = _run("阶段3b mypy（652 文件）",
                           [py, "-m", "mypy", "--ignore-missing-imports", "--no-error-summary", *NEW_TOOLS])
        ok_sel = True
        for t in SELFTESTS:
            ok_sel = _run(f"阶段4 selftest {Path(t).name}", [py, t, "--check"]) and ok_sel
        res["selftest"] = ok_sel

        before = _atoms_fp()
        # 阶段5 保护器联调（queyi-core B7-B10 灰度上岗差分验证）
        res["protector_integration"] = _run(
            "阶段5 保护器联调 queyi-core protector_rollout_652 --verify",
            [py, "tools/protector_rollout_652.py", "--verify"], cwd=QUEYI)
        after = _atoms_fp()
        res["zero_pollution"] = before == after
        print(f"\n--- 阶段6 受控 atoms 指纹: before={before[:16]} after={after[:16]} "
              f"{'一致(PASS)' if res['zero_pollution'] else '漂移(FAIL)'}")
        res["trust_root"] = _run("阶段7 信任根 tool_integrity --check",
                                 [py, "tools/tool_integrity.py", "--check"])

    print("\n===== 652 门禁汇总 =====")
    for k, v in res.items():
        print(f"  {k:22s}: {'PASS' if v else 'FAIL'}")
    allok = all(res.values())
    print(f"652 gate: {'PASS' if allok else 'FAIL'}")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
