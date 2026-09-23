"""627 E1 · 收工门禁（627 专用）

校验项：
1. 整目录 ruff（tools/ + tests/）全绿
2. 10 个 627 新工具 `--check` 全部 exit 0
3. mypy tools/ = 0 errors
4. 627 新增测试全部通过
5. 受控目录（atoms/evidence/Examples/Book）零污染
6. 完整性根：`tool_integrity.py --check`（626 尺子 34/34 仍一致）
7. CORE_TOOLS 在本批次未被修改
8. 626 收工未被破坏（commit 链连续、受控零污染）

铁律：不跑监工门禁（gate/poison/replay/tool_integrity --check 仅 --check，不跑业务门禁）；
不 push；不 golden accept；不代签人审。
"""
from __future__ import annotations

import argparse
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PY = sys.executable
BATCH_BASE = "4f2c976c"  # 627 起点（626 F1）

NEW_TOOLS = [
    "w2_projection_normalizer_627", "w2_projection_diff_627",
    "supersedes_remapper_627", "pck_hash_drift_analyzer_627",
    "mirror_edge_symmetry_checker_627", "authority_v2_e2e_627",
    "v2_regression_627", "authority_v2_switch_627",
    "blind_review_execution_pack_627", "blind_review_backfill_627",
    "pre_push_checklist_627",
]
CONTROLLED = ["atoms", "evidence", "Examples", "Book"]
CORE_TOOLS = ["gate_engine.py", "atom_evidence_replay.py", "poison_drill.py",
              "toolchain.py", "cppbible.py"]


def _run(args: list) -> tuple[int, str]:
    try:
        p = subprocess.run(args, capture_output=True, text=True, cwd=ROOT, timeout=300)
        return p.returncode, (p.stdout + p.stderr)[-1500:]
    except Exception as exc:  # noqa: BLE001
        return 1, str(exc)


def check() -> int:
    ok = True

    def chk(name: str, cond: bool, tail: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {tail}")
        ok = ok and cond

    # 1. 整目录 ruff
    rc, _ = _run([PY, "-m", "ruff", "check", "tools/", "tests/"])
    chk("整目录 ruff 全绿", rc == 0)

    # 2. 627 新工具 --check
    for name in NEW_TOOLS:
        rc, out = _run([PY, os.path.join("tools", f"{name}.py"), "--check"])
        chk(f"工具 {name} --check", rc == 0, "" if rc == 0 else out[-200:])

    # 3. mypy
    rc, _ = _run([PY, "-m", "mypy", "tools/"])
    chk("mypy tools/ = 0 errors", rc == 0)

    # 4. 627 测试
    import glob
    tfiles = sorted(glob.glob(os.path.join(ROOT, "tests", "test_*_627.py")))
    rc, out = _run([PY, "-m", "pytest", *tfiles, "-q"])
    chk("627 新增测试全过", rc == 0, "" if rc == 0 else out[-300:])

    # 5. 受控目录零污染
    dirty = []
    for d in CONTROLLED:
        p = os.path.join(ROOT, d)
        if not os.path.isdir(p):
            continue
        rc, _ = _run(["git", "diff", "--quiet", "--", d])
        if rc != 0:
            dirty.append(d)
    chk("受控目录零污染", not dirty, f"({dirty})")

    # 6. 完整性根（626 尺子仍一致）
    rc, out = _run([PY, os.path.join("tools", "tool_integrity.py"), "--check"])
    chk("tool_integrity --check（尺子一致）", rc == 0, "" if rc == 0 else out[-200:])

    # 7. CORE_TOOLS 未改
    rc, out = _run(["git", "diff", "--name-only", BATCH_BASE, "HEAD"])
    changed = [d for d in out.split() if os.path.basename(d) in CORE_TOOLS]
    chk("CORE_TOOLS 未修改", not changed, f"({changed})")

    # 8. 626 未破坏：受控仍干净 + commit 链连续（HEAD 在 base 之后）
    rc, out = _run(["git", "merge-base", "--is-ancestor", BATCH_BASE, "HEAD"])
    chk("commit 链连续（HEAD 含 627 起点）", rc == 0)

    print(f"627 收工门禁: {'PASS ✅' if ok else 'FAIL ❌'}")
    return 0 if ok else 1


def main(argv: list | None = None) -> int:
    ap = argparse.ArgumentParser(description="627 E1 收工门禁")
    ap.add_argument("--check", action="store_true", help="运行门禁")
    args = ap.parse_args(argv)
    if args.check:
        return check()
    return check()


if __name__ == "__main__":
    sys.exit(main())
