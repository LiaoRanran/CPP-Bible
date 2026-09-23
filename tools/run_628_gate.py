"""628 E1 · 收工门禁（纯标准库）

校验项（对应 628.md 第三节验收门禁 15 条）：
1. 整目录 ruff（tools/ + tests/）全绿
2. 本批 12 个新工具 `--check` 全部 exit 0
3. mypy tools/ = 0 errors
4. 本批新增测试全绿（`tests/test_*_628.py`）
5. 受控目录（atoms/evidence/Examples/Book）零污染
6. `tool_integrity.py --check`（A1 改 626 工具后已 `--update` 重钉，尺子仍 34/34）
7. CORE_TOOLS 在本批次未被修改
8. V2 flag 接入后 **V1/V2 模式 W2 数字一致**（IN114/OUT7/UNDEC0）
9. 4 项技术债清算状态核查
10. 他验三件套状态核查（B1–B4）
11. 独立验证者**零 import 本项目工具**（静态分析）
12. 学习者镜像门状态 = closed

铁律：**不跑监工门禁**（gate/poison/replay 一律不跑）、**不 push**、**不 golden accept**、
**不打开 delegation**、**不代签人审**、**不执行真实 Blind Review**。
"""
from __future__ import annotations

import argparse
import glob
import json
import os
import re
import subprocess
import sys
from typing import cast

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
PY = sys.executable
BATCH_BASE = "b913b0fe"  # 628 起点（627 E1 收工）

NEW_TOOLS = [
    "v2_flag_integration_verify_628", "pck_hash_renewal_628",
    "mirror_edge_symmetry_write_628", "replay_manifest_fix_628",
    "independent_verifier_628", "vsa_attestation_628", "vsa_verify_628",
    "transparency_log_628", "third_party_audit_demo_628",
    "human_review_dashboard_v2_628",
    "learner_behavior_collector_628", "learner_twin_gate_monitor_628",
]
CONTROLLED = ["atoms", "evidence", "Examples", "Book"]
CORE_TOOLS = ["gate_engine.py", "atom_evidence_replay.py", "poison_drill.py",
              "toolchain.py", "cppbible.py"]
ZERO_IMPORT_TOOLS = ["independent_verifier_628.py", "vsa_verify_628.py"]
EXPECT_W2 = {"IN": 114, "OUT": 7, "UNDEC": 0}
ACCEPT_MD = os.path.join(ROOT, "data", "628_acceptance_report.md")

_SNIPPET = (
    "import sys, json\n"
    "sys.path.insert(0, {here!r})\n"
    "import authority_projection_compiler_626 as C\n"
    "c = C.AuthorityProjectionCompiler()\n"
    "print(json.dumps({{'w2': c.w2_summary(), 'v2_mode': c.v2_mode}}))\n"
)


def _run(args: list, env: dict | None = None) -> tuple[int, str]:
    try:
        p = subprocess.run(args, capture_output=True, text=True, cwd=ROOT,
                           timeout=600, env=env)
        return p.returncode, (p.stdout + p.stderr)[-1500:]
    except Exception as exc:  # noqa: BLE001
        return 1, str(exc)


def _local_modules() -> set:
    return {os.path.splitext(f)[0] for f in os.listdir(HERE) if f.endswith(".py")}


def imports_of(path: str) -> list:
    mods = []
    with open(path, encoding="utf-8") as fh:
        for line in fh:
            m = re.match(r"(?:from|import)\s+([A-Za-z_][A-Za-z0-9_]*)", line.strip())
            if m:
                mods.append(m.group(1))
    return mods


def w2_summary(v2: bool) -> dict:
    env = dict(os.environ)
    if v2:
        env["QUEYI_AUTHORITY_V2"] = "1"
    else:
        env.pop("QUEYI_AUTHORITY_V2", None)
    rc, out = _run([PY, "-c", _SNIPPET.format(here=HERE)] + [], env=env)
    if rc != 0:
        return {}
    for line in reversed(out.strip().splitlines()):
        if line.startswith("{"):
            return cast(dict, json.loads(line))
    return {}


def _json(path: str) -> dict:
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return cast(dict, json.load(fh))


def check(no_tests: bool = False) -> int:
    """`no_tests=True` 供门禁自身的单测调用（否则 pytest 会递归调用门禁 → 无限套娃）。"""
    ok = True

    def chk(name: str, cond: bool, tail: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {tail}")
        ok = ok and cond

    # 1 ruff（整目录）
    rc, _ = _run([PY, "-m", "ruff", "check", "tools/", "tests/"])
    chk("整目录 ruff 全绿", rc == 0)

    # 2 本批 12 个工具 --check
    for name in NEW_TOOLS:
        rc, out = _run([PY, os.path.join("tools", f"{name}.py"), "--check"])
        chk(f"工具 {name} --check", rc == 0, "" if rc == 0 else out[-160:])

    # 3 mypy
    rc, _ = _run([PY, "-m", "mypy", "tools/"])
    chk("mypy tools/ = 0 errors", rc == 0)

    # 4 本批测试
    tfiles = sorted(glob.glob(os.path.join(ROOT, "tests", "test_*_628.py")))
    if no_tests:
        print(f"  [skip] 本批新增测试（{len(tfiles)} 文件）—— 由 --check 完整调用时执行")
    else:
        rc, out = _run([PY, "-m", "pytest", *tfiles, "-q"])
        chk(f"本批新增测试全过（{len(tfiles)} 文件）", rc == 0,
            "" if rc == 0 else out[-300:])

    # 5 受控目录零污染
    dirty = [d for d in CONTROLLED if os.path.isdir(os.path.join(ROOT, d))
             and _run(["git", "diff", "--quiet", "--", d])[0] != 0]
    chk("受控目录零污染", not dirty, f"({dirty})")

    # 6 尺子一致（A1 改 626 工具后已重钉）
    rc, out = _run([PY, os.path.join("tools", "tool_integrity.py"), "--check"])
    chk("tool_integrity --check（尺子一致）", rc == 0, "" if rc == 0 else out[-160:])

    # 7 CORE_TOOLS 未修改
    rc, out = _run(["git", "diff", "--name-only", BATCH_BASE, "HEAD"])
    changed = [d for d in out.split() if os.path.basename(d) in CORE_TOOLS]
    chk("CORE_TOOLS 未修改", not changed, f"({changed})")

    # 8 V1/V2 数字一致
    v1, v2s = w2_summary(False), w2_summary(True)
    chk("V1 模式 W2 = IN114/OUT7/UNDEC0", v1.get("w2") == EXPECT_W2, f'({v1.get("w2")})')
    chk("V2 模式 W2 = IN114/OUT7/UNDEC0", v2s.get("w2") == EXPECT_W2, f'({v2s.get("w2")})')
    chk("V1/V2 数字一致", v1.get("w2") == v2s.get("w2") and bool(v1.get("w2")))
    chk("flag 默认关闭（V1 为默认）", v1.get("v2_mode") is False)

    # 9 四项技术债清算核查
    chk("A1 flag 真接入（v2_mode 可读且 V2 走归一化）", v2s.get("v2_mode") is True)
    chk("A1 报告存在",
        os.path.exists(os.path.join(ROOT, "data", "v2_flag_integration_report_628.md")))
    pck = _json("data/pck_hash_renewal_628.json")
    chk("A2 PCK 83 张全量处置且复查 0 待处理",
        pck.get("total_certs") == 83 and pck.get("stats", {}).get("needs_human") == 0,
        f'({pck.get("total_certs")}/{pck.get("stats")})')
    mir = _json("data/mirror_symmetry_proofs_628.json")
    ledger_proof = sum(
        1 for ln in open(os.path.join(ROOT, "data", "review_item_ledger.jsonl"),
                         encoding="utf-8")
        if ln.strip() and json.loads(ln).get("symmetry_proof_id"))
    chk("A3 镜像边 194 条自动证明", mir.get("auto_proved") == 194, f'({mir.get("auto_proved")})')
    chk("A3 账本写入 76 条 symmetry_proof_id", ledger_proof == 76, f"({ledger_proof})")
    chk("A4 DEBT-001 处置 + replay 修复报告存在",
        os.path.exists(os.path.join(ROOT, "data", "debt_001_disposition_628.md"))
        and os.path.exists(os.path.join(ROOT, "data", "debt_replay_fix_report_628.md")))

    # 10 他验三件套
    vsa = sorted(f for f in os.listdir(os.path.join(ROOT, "data", "vsa"))
                 if f.startswith("attestation_") and f.endswith(".json"))
    log_lines = [ln for ln in open(os.path.join(ROOT, "data", "transparency_log.jsonl"),
                                  encoding="utf-8") if ln.strip()]
    chk("B2 VSA 凭证 ≥ 1 张", len(vsa) >= 1, f"({len(vsa)} 张)")
    chk("B3 透明日志 ≥ 1 条", len(log_lines) >= 1, f"({len(log_lines)} 条)")
    chk("B4 端到端审计报告存在",
        os.path.exists(os.path.join(ROOT, "data", "third_party_audit_demo_report_628.md")))
    chk("C1 仪表盘 v2 与设计说明存在",
        os.path.exists(os.path.join(ROOT, "data", "human_review_dashboard_v2.html"))
        and os.path.exists(
            os.path.join(ROOT, "data", "human_review_dashboard_v2_design_628.md")))

    # 11 独立验证者零 import 本项目工具
    local = _local_modules()
    for f in ZERO_IMPORT_TOOLS:
        bad = sorted(set(imports_of(os.path.join(HERE, f))) & local)
        chk(f"{f} 零 import 本项目工具", not bad, f"({bad})")

    # 12 学习者镜像门
    rc, out = _run([PY, os.path.join("tools", "learner_twin_gate_monitor_628.py")])
    chk("学习者镜像门 = closed（真实学习事件 0/50）", rc == 0 and "state=closed" in out,
        f"({out.strip()[-60:]})")

    print(f"628 收工门禁: {'PASS ✅' if ok else 'FAIL ❌'}")
    return 0 if ok else 1


def main(argv: list | None = None) -> int:
    ap = argparse.ArgumentParser(description="628 E1 收工门禁")
    ap.add_argument("--check", action="store_true", help="运行门禁")
    ap.add_argument("--no-tests", action="store_true",
                    help="跳过 pytest 步骤（供门禁自身单测调用，防递归）")
    args = ap.parse_args(argv)
    return check(no_tests=args.no_tests)


if __name__ == "__main__":
    sys.exit(main())
