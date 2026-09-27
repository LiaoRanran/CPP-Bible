#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""run_651_gate.py — 651 收工门禁（两阶段 pytest + ruff/mypy + 保护器联调 + 信任根 + 零污染）。

阶段：
1. fast pytest（-m 'not slow'）→ 2. slow/full pytest
3. ruff / mypy（仅 651 文件）→ 4. 各 651 工具 --check
5. 保护器联调（shadow 轮转 + 校准 + 人审队列 + 判决扩展），前后 atoms 指纹不变（受控零污染）
6. 信任根 tool_integrity --check（闭包未破）

用法：python tools/run_651_gate.py [--fast-only]；退出码非 0 = 未过。
"""
from __future__ import annotations

import argparse
import hashlib
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent

NEW_TESTS = ["tests/test_core_pbt_651.py"]
NEW_TOOLS = [
    "tools/evidence_aging_651.py", "tools/seeker_replay_651.py", "tools/ledger_checkpoint_651.py",
    "tools/verdict_extension_651.py", "tools/replay_probe_651.py", "tools/shadow_rotator_651.py",
    "tools/calibration_upgrade_651.py", "tools/human_review_queue_651.py", "tools/run_651_gate.py",
]
SELFTESTS = NEW_TOOLS[:8]


def _run(label: str, cmd: list[str], cwd: Path = ROOT) -> bool:
    print(f"\n=== {label} ===\n$ {' '.join(cmd)}")
    r = subprocess.run(cmd, cwd=str(cwd), check=False)
    print(f"--- {label}: {'PASS' if r.returncode == 0 else 'FAIL'} (exit={r.returncode})")
    return r.returncode == 0


def _atoms_fingerprint() -> str:
    h = hashlib.sha256()
    for p in sorted((ROOT / "atoms").rglob("*.md")):
        h.update(str(p.relative_to(ROOT)).encode())
        h.update(hashlib.sha256(p.read_bytes()).digest())
    return h.hexdigest()


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="651 收工门禁")
    ap.add_argument("--fast-only", action="store_true")
    a = ap.parse_args(argv)
    py = sys.executable
    res: dict[str, bool] = {}

    res["fast"] = _run("阶段1 fast pytest(-m 'not slow')",
                       [py, "-m", "pytest", *NEW_TESTS, "-q", "-m", "not slow", "-p", "no:cacheprovider"])
    if not a.fast_only:
        res["full"] = _run("阶段2 full pytest",
                           [py, "-m", "pytest", *NEW_TESTS, "-q", "-p", "no:cacheprovider"])
        res["ruff"] = _run("阶段3a ruff（651 文件）", [py, "-m", "ruff", "check", *NEW_TOOLS])
        res["mypy"] = _run("阶段3b mypy（651 文件）",
                           [py, "-m", "mypy", "--ignore-missing-imports", "--no-error-summary", *NEW_TOOLS])
        ok_sel = True
        for t in SELFTESTS:
            ok_sel = _run(f"阶段4 selftest {Path(t).name}", [py, t, "--check"]) and ok_sel
        res["selftest"] = ok_sel

        # 阶段5 保护器联调 + 受控零污染
        before = _atoms_fingerprint()
        integ_ok = True
        integ_ok = _run("阶段5 保护器联调·shadow 轮转", [py, "tools/shadow_rotator_651.py", "--advance"]) and integ_ok
        integ_ok = _run("阶段5 保护器联调·校准", [py, "tools/calibration_upgrade_651.py", "--run"]) and integ_ok
        integ_ok = _run("阶段5 保护器联调·人审队列", [py, "tools/human_review_queue_651.py", "--build"]) and integ_ok
        integ_ok = _run("阶段5 保护器联调·判决扩展回填(dry-run)",
                        [py, "tools/verdict_extension_651.py", "--backfill"]) and integ_ok
        after = _atoms_fingerprint()
        zero_pollution = before == after
        print(f"\n--- 阶段5 受控 atoms 指纹: before={before[:16]} after={after[:16]} "
              f"{'一致(PASS)' if zero_pollution else '漂移(FAIL)'}")
        res["protector_integration"] = integ_ok
        res["zero_pollution"] = zero_pollution

        res["trust_root"] = _run("阶段6 信任根 tool_integrity --check",
                                 [py, "tools/tool_integrity.py", "--check"])

    print("\n===== 651 门禁汇总 =====")
    for k, v in res.items():
        print(f"  {k:22s}: {'PASS' if v else 'FAIL'}")
    allok = all(res.values())
    print(f"651 gate: {'PASS' if allok else 'FAIL'}")
    return 0 if allok else 1


if __name__ == "__main__":
    raise SystemExit(main())
