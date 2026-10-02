# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""671i-C4 · 随机种子固定检查工具（门禁 G-SEED-FIXED）。

核查所有使用随机性的脚本是否固定了随机种子：
  - 实验类脚本（baseline/attack/mutation/blind/select_assets/targeted/random/fuzz 等）
    若未固定种子 → **ERROR**（实验不可复现，硬问题）；
  - 工具/日志类脚本使用随机性但未固定 → **WARN**（非实验，影响小）。

判定：文件出现 `random`/`np.random`/`numpy.random` 且未出现
  `*.seed(` / `default_rng(` / `RandomState(` → 视为未固定种子。
（注：本工具只做静态文本判定；若种子经 CLI/环境变量传入，需人工确认。）

CLI:
  python tools/seed_check_671i.py [--tools dir]
  退出码 0 = 无 ERROR；1 = 有 ERROR（供门禁）。
"""
from __future__ import annotations

import argparse
import os
import re
import sys

EXPERIMENT_HINTS = ("experiment", "baseline", "attack", "mutation", "blind",
                    "select_assets", "targeted", "random", "fuzz", "mutator",
                    "ablation", "replay")

USE_RE = re.compile(r"(?:^|\W)(?:import\s+random|from\s+random|np\.random|numpy\.random|random\.)", re.MULTILINE)
SEED_RE = re.compile(r"(?:random|np\.random|numpy\.random|torch)\.seed\(|np\.random\.default_rng|RandomState\(|torch\.manual_seed\(")


def scan_file(path: str):
    t = open(path, encoding="utf-8", errors="replace").read()
    uses = bool(USE_RE.search(t))
    seed = bool(SEED_RE.search(t))
    return uses, seed


def run_all(tools_dir: str):
    issues = []
    for r, _, fs in os.walk(tools_dir):
        if ".git" in r:
            continue
        for f in fs:
            if not f.endswith(".py"):
                continue
            p = os.path.join(r, f)
            uses, seed = scan_file(p)
            if not uses:
                continue
            rel = os.path.relpath(p, os.path.dirname(tools_dir) if False else os.getcwd())
            is_exp = any(h in os.path.basename(p).lower() for h in EXPERIMENT_HINTS)
            if not seed:
                sev = "ERROR" if is_exp else "WARN"
                issues.append({"severity": sev, "code": "NO_SEED",
                               "card": rel,
                               "detail": f"使用随机性但未固定种子（{'实验脚本' if is_exp else '工具/日志'}）"})
    errors = [i for i in issues if i["severity"] == "ERROR"]
    return {"issues": issues, "errors": errors}


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--tools", default="tools")
    a = ap.parse_args(argv)
    res = run_all(a.tools)
    by_sev = {}
    for i in res["issues"]:
        by_sev[i["severity"]] = by_sev.get(i["severity"], 0) + 1
    print("随机性使用扫描:", by_sev)
    for i in res["issues"]:
        print(f"  [{i['severity']}] {i['code']} | {i['card']} | {i['detail']}")
    print(f"ERROR 级（实验脚本未固定种子）: {len(res['errors'])}")
    return 1 if res["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
