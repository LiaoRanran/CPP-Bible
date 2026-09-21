#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""618 F2 · 轻量验收门（不跑监工门禁）

- 受控目录污染自检：git status --porcelain 不应含 atoms/evidence/Examples/Book/CORE_TOOLS/golden_lock/poison_drill 前缀。
- 运行 618 与 617 新增单测（tests/test_618*.py + test_escape_rate_estimand/test_verify_independence_level/test_snapshot_manifest）。
- 全部绿 ⇒ exit 0；任一失败/污染 ⇒ exit 1。
- **不跑** gate --check / poison / replay --check / tool_integrity --check（监工职责，依 §五 禁跑）。
"""
import os
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CONTROLLED_PREFIXES = (
    "atoms/", "evidence/", "Examples/", "Book/", "CORE_TOOLS/",
    "golden_lock", "poison_drill",
)

GATE_TESTS = [
    "tests/test_618_a3.py", "tests/test_618_b.py", "tests/test_618_c2.py",
    "tests/test_618_c4.py", "tests/test_618_e2.py",
    "tests/test_escape_rate_estimand.py", "tests/test_verify_independence_level.py",
    "tests/test_snapshot_manifest.py",
]


def check_controlled_clean():
    out = subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT).decode("utf-8", "ignore")
    hits = []
    for line in out.splitlines():
        path = line[2:].strip()  # 去除 "XY " 状态前缀
        if any(path.startswith(p) or ("/" + p) in path for p in CONTROLLED_PREFIXES) \
           or path.split("/")[0] in ("atoms", "evidence", "Examples", "Book", "CORE_TOOLS", "golden_lock", "poison_drill"):
            hits.append(path)
    return hits


def collect_tests():
    return [t for t in GATE_TESTS if os.path.exists(os.path.join(ROOT, t))]


def run_tests():
    tests = collect_tests()
    cmd = [sys.executable, "-m", "pytest", *tests, "-q"]
    r = subprocess.run(cmd, cwd=ROOT)
    return r.returncode


def main():
    rc = 0
    hits = check_controlled_clean()
    if hits:
        print("FAIL: 受控目录被改动 -> %s" % hits)
        rc = 1
    else:
        print("OK: 受控目录零污染")
    code = run_tests()
    if code != 0:
        print("FAIL: 618/617 新单测未全绿 (rc=%d)" % code)
        rc = 1
    else:
        print("OK: 618/617 新单测全绿")
    print("验收门:%s" % ("PASS" if rc == 0 else "FAIL"))
    sys.exit(rc)


if __name__ == "__main__":
    main()
