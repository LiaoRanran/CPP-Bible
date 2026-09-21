#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""617 D2 · SNAPSHOT_MANIFEST 自动生成（治理数字漂移，纯标准库 + git 只读）

生成 data/SNAPSHOT_MANIFEST_617.json：含【实时 git/filesystem 计数】+【冻结验证基线数字】。
本工具只读，不跑任何 --check；计数由 git/filesystem 直取，杜绝手写漂移。
用途：README / qmd / quickref 的计数应引用本 manifest 的 live_counts，禁止手填。

铁律：verification_baseline_frozen 为冻结数字（取自 616 基线），重跑须走监工门禁；本工具不跑。
"""
import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 冻结验证基线（取自 data/616_baseline.md，last_verified 标注；本工具不重跑）
FROZEN_VERIFICATION = {
    "last_verified": "2026-09-21",
    "source": "data/616_baseline.md",
    "gate": {"rules": 63, "hits": 191, "block": 0, "warn": 186, "advice": 5},
    "poison": {"passed": 124, "total": 124, "coverage_apparent": "63/63", "coverage_honest": "60/63"},
    "replay": {"confirm": 56, "refute": 0, "infra_error": 0},
    "mutation_v7": {"variants": 1593, "blocked": 1405, "escaped": 1, "n_a": 179,
                    "equivalent": 8, "judge_denom": 1406, "escape_rate_contract": "1/1406"},
    "confidence": {"cp_fixed_upper_95": 0.003370, "cs_anytime_upper_95": 0.009062},
    "human_review": {"total": 388, "approve": 354, "modify": 34, "reject": 0,
                     "batch_authorization": 388, "mirror_edge": 194},
    "independence": {"verifier_count": 1, "second_implementation": "1/63",
                     "discrete_level": 1, "continuity_scalar": 0.153},
    "trust_root": "partially_anchored",
}


def _git(*args):
    return subprocess.check_output(["git", *args], cwd=ROOT).decode().strip()


def git_count_commits():
    return int(_git("rev-list", "--count", "HEAD"))


def head_commit():
    return _git("rev-parse", "HEAD")


def count_py(folder):
    p = os.path.join(ROOT, folder)
    if not os.path.isdir(p):
        return 0
    return len([f for f in os.listdir(p) if f.endswith(".py")])


def count_md(folder, recursive, pattern=None):
    p = os.path.join(ROOT, folder)
    if not os.path.isdir(p):
        return 0
    cnt = 0
    if recursive:
        for root, _, files in os.walk(p):
            for f in files:
                if f.endswith(".md") and (pattern is None or pattern in f):
                    cnt += 1
    else:
        for f in os.listdir(p):
            if f.endswith(".md") and (pattern is None or pattern in f):
                cnt += 1
    return cnt


def build_manifest():
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "head_commit": head_commit(),
        "live_counts": {
            "commits": git_count_commits(),
            "tools_py": count_py("tools"),
            "tests_py": count_py("tests"),
            "atoms_md": count_md("atoms", recursive=True),
            "evidence_ev_md": count_md("evidence", recursive=True, pattern="EV-"),
        },
        "verification_baseline_frozen": FROZEN_VERIFICATION,
        "note": (
            "live_counts 由 git/filesystem 直取，为唯一可信计数源；"
            "README/qmd/quickref 应引用本 manifest，禁止手写。"
            "verification_baseline_frozen 为冻结数字，重跑须走监工门禁（本工具不跑）。"
        ),
    }


def verify_clean():
    return _git("status", "--porcelain") == ""


def main():
    ap = argparse.ArgumentParser(description="617 D2 SNAPSHOT_MANIFEST 生成")
    ap.add_argument("--out",
                    default=os.path.join(ROOT, "data", "SNAPSHOT_MANIFEST_617.json"))
    ap.add_argument("--check-clean", action="store_true",
                    help="要求工作区干净，否则非零退出")
    args = ap.parse_args()
    if args.check_clean and not verify_clean():
        print("ERROR: working tree not clean; refuse to snapshot", file=sys.stderr)
        sys.exit(2)
    m = build_manifest()
    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(m, f, indent=2, ensure_ascii=False)
        f.write("\n")
    print(json.dumps(m, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
