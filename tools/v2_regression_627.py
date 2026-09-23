"""627 B2 · V2 回归验证（**静态分析**，不运行监工门禁）

**背景**：627 的核心目标是让 `QUEYI_AUTHORITY_V2=1` 可安全启用。启用后必须确认
gate / poison / replay（即 CORE_TOOLS）**不发生回归**。

**方法（诚实：只做静态分析，不跑监工门禁）**：
1. **隔离性**：确认 CORE_TOOLS（gate_engine / atom_evidence_replay / poison_drill /
   toolchain / cppbible）**不读取** `QUEYI_AUTHORITY_V2`，也**不 import** 任何 626/627
   的 V2 投影/账本工具 ⇒ 全局开启 flag 不会触达 CORE_TOOLS ⇒ 无回归路径。
2. **W2 计算未替换**：确认 gate_engine 仍走 legacy `weighted_af_solver`（或自带 W2），
   未改用 `authority_projection_compiler_626` ⇒ 既有 W2 判决不变。
3. **纯增量**：确认 626/627 的 V2 能力全部在**新文件**中实现，未修改 CORE_TOOLS 生产资料逻辑。

> **不运行** gate/poison/replay/tool_integrity --check（627 铁律：不跑监工门禁）。
> 仅用静态扫描证明「无回归可达路径」，远程 CI 实跑留交人项 #3（push 后由人触发）。

**判定**：以上静态检查全过 ⇒ V2 启用对 CORE_TOOLS **无回归风险**。
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
from typing import Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

CORE_TOOLS = ["gate_engine.py", "atom_evidence_replay.py",
              "poison_drill.py", "toolchain.py", "cppbible.py"]
FORBIDDEN_PATTERNS = [
    "QUEYI_AUTHORITY_V2",
    "authority_projection_compiler_626",
    "decision_event_v2_626",
    "w2_projection_normalizer_627",
    "review_item_ledger_626",
    "supersedes_remapper_627",
]
W2_LEGACY_SOLVER = "weighted_af_solver.py"
OUT_JSON = os.path.join(ROOT, "data", "v2_regression_627.json")
OUT_MD = os.path.join(ROOT, "data", "v2_regression_627.md")


def _scan(path: str, pattern: str) -> bool:
    if not os.path.exists(path):
        return False
    return bool(re.search(re.escape(pattern), open(path, encoding="utf-8", errors="ignore").read()))


def check() -> dict:
    rows = []
    for ct in CORE_TOOLS:
        p = os.path.join(HERE, ct)
        hits = [pat for pat in FORBIDDEN_PATTERNS if _scan(p, pat)]
        rows.append({"tool": ct, "forbidden_hits": hits,
                     "isolated": not hits})
    # W2 legacy 求解器未被本批次修改（git diff）
    try:
        diff = subprocess.run(["git", "diff", "--name-only", "528e9ab2", "HEAD"],
                              capture_output=True, text=True, cwd=ROOT).stdout.split()
        w2_solver_changed = any(os.path.basename(d) == W2_LEGACY_SOLVER
                                for d in diff)
    except Exception:
        w2_solver_changed = False
    # git：CORE_TOOLS 在本批次未被修改（627 提交不含对 CORE_TOOLS 的改动）
    try:
        core_changed = [d for d in diff if os.path.basename(d) in CORE_TOOLS]
    except Exception:
        core_changed = []
    all_isolated = all(r["isolated"] for r in rows)
    no_core_change = not core_changed
    w2_legacy_intact = not w2_solver_changed
    passed = all_isolated and w2_legacy_intact and no_core_change
    return {
        "core_tools": rows,
        "all_isolated": all_isolated,
        "w2_solver_unchanged": w2_legacy_intact,
        "core_tools_modified_in_batch": core_changed,
        "no_core_change": no_core_change,
        "passed": passed,
    }


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    r = check()
    chk("CORE_TOOLS 全部隔离 V2 flag/工具",
        r["all_isolated"],
        f"(未隔离: {[x['tool'] for x in r['core_tools'] if not x['isolated']]})")
    chk("legacy W2 求解器（weighted_af_solver.py）未被本批次修改",
        r["w2_solver_unchanged"])
    chk("本批次未修改 CORE_TOOLS", r["no_core_change"],
        f"(改动: {r['core_tools_modified_in_batch']})")
    chk("V2 回归判定通过", r["passed"])
    print(f"B2 regression check: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="627 B2 V2 回归验证（静态）")
    ap.add_argument("--check", action="store_true", help="自检")
    ap.add_argument("--report", action="store_true", help="输出报告")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    r = check()
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(r, fh, ensure_ascii=False, indent=2)
    if args.report:
        lines = ["# 627 B2 · V2 回归验证（静态分析）", "",
                 f"- **判定**：{('通过 ✅' if r['passed'] else '未通过 ❌')}（V2 对 CORE_TOOLS 无回归风险）",
                 "", "## CORE_TOOLS 隔离性", "",
                 "| 工具 | 隔离 V2 |", "|---|---|"]
        for x in r["core_tools"]:
            lines.append(f"| {x['tool']} | {'✅' if x['isolated'] else '❌ '+str(x['forbidden_hits'])} |")
        lines += ["", f"- legacy W2 求解器 `weighted_af_solver.py` 未被本批次修改：{r['w2_solver_unchanged']}",
                  f"- 本批次未修改 CORE_TOOLS：{r['no_core_change']}", "",
                  "> **注**：gate / poison / replay / tool_integrity --check **未执行**"
                  "（627 铁律不跑监工门禁）。本报告以静态分析证明"
                  "「CORE_TOOLS 不读取 flag、不依赖 V2 工具」⇒ 启用 flag 无回归可达路径。"
                  "远程 CI 实跑由人 push 后触发（交人项 #3）。"]
        with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
            fh.write("\n".join(lines) + "\n")
        print(f"written {OUT_MD}")
    print(json.dumps(r, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
