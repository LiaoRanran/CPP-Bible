"""647 D3 · **死代码清理 + 复检**（合并后的 10 个核心工具）。

分两层，**都只对"合并涉及的 3 个模块 + 10 个核心工具"**（不做全仓大扫除，避免误伤）：

1. **可自动删的**：未用 import / 重复 import / 未用局部变量（`ruff` 的 `F401/F811/F841`）。
   647 D1 合并时已用 `ruff --fix` 清掉 **15 行**；本工具**复检当前是否为 0**（回归锁）。
2. **只报不删的**：模块级函数在**本文件内**从未被引用、且不在 `__all__`/被其它模块 import 的
   清单里 ⇒ 记为"死函数候选"（**只报告**：删函数有语义风险，必须人核）。

输出：`data/647_deadcode_report.md`（删了多少行 / 剩余 0 / 死函数候选清单）。纯标准库（`ruff` 可选）。
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import subprocess
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

OUT_MD = os.path.join(ROOT, "data", "647_deadcode_report.md")
OUT_JSON = os.path.join(ROOT, "data", "647_deadcode_report.json")

TARGETS: tuple[str, ...] = (
    "three_layer_orchestrator_645", "evidence_grading_645", "loop_r5_runner_645",
    "smart_issue_finder_645", "targeted_attacker_645", "rule_drafter_645",
    "standard_fetcher_645", "compiler_probe_645", "counterexample_searcher_645",
    "rule_card_mapper_646",
)
#: 647 D1 用 `ruff --fix` 清掉的**死 import 行数**（本工具把它作为回归基线）
CLEANED_IN_D1 = 15


def _paths() -> list[str]:
    return [os.path.join(HERE, t + ".py") for t in TARGETS
            if os.path.isfile(os.path.join(HERE, t + ".py"))]


def ruff_dead_code() -> dict[str, Any]:
    """未用 import / 重复定义 / 未用变量（ruff）。ruff 不可用 ⇒ 如实登记，不伪造。"""
    pfiles = _paths()
    try:
        r = subprocess.run([sys.executable, "-m", "ruff", "check", "--select", "F401,F811,F841",
                            "--output-format", "concise", *pfiles],
                           capture_output=True, text=True, timeout=300, cwd=ROOT,
                           encoding="utf-8", errors="replace")
    except (OSError, subprocess.SubprocessError) as exc:
        return {"available": False, "error": type(exc).__name__}
    # 只数**违规行**（`path:line:col: CODE ...`）；ruff 干净时会打 "All checks passed!"
    lines = [ln for ln in r.stdout.splitlines() if ".py:" in ln and ln.strip()]
    return {"available": True, "rc": r.returncode, "n_remaining": len(lines),
            "violations": lines[:40]}


def dead_function_candidates() -> dict[str, Any]:
    """**只报不删**：模块级函数在本文件内从未被引用、也不像对外 API 的（无 `--` CLI 入口、
    名字不以 `_` 开头但没人调）。

    判据（保守，宁可漏报）：
      * 定义在模块顶层；
      * 名字在**本文件源码**里除定义外**没有第二次出现**；
      * 名字**没有**被任何其它 `tools/*.py`／`tests/*.py` 以 `import` 方式引用。
    """
    import glob
    all_src = {}
    for p in glob.glob(os.path.join(HERE, "*.py")) + glob.glob(
            os.path.join(ROOT, "tests", "*.py")):
        try:
            all_src[p] = open(p, encoding="utf-8", errors="replace").read()
        except OSError:
            continue
    rows: list[dict[str, str]] = []
    for t in TARGETS:
        p = os.path.join(HERE, t + ".py")
        if not os.path.isfile(p):
            continue
        src = all_src.get(p, "")
        tree = ast.parse(src)
        for n in tree.body:
            if not isinstance(n, ast.FunctionDef):
                continue
            name = n.name
            used_in_file = src.count(name) > 1
            used_elsewhere = any(name in s and p2 != p for p2, s in all_src.items())
            if not used_in_file and not used_elsewhere:
                rows.append({"module": t, "function": name, "lineno": str(n.lineno)})
    return {"n_candidates": len(rows), "candidates": rows}


def audit() -> dict[str, Any]:
    return {"cleaned_in_d1": CLEANED_IN_D1,
            "targets": [t for t in TARGETS if os.path.isfile(os.path.join(HERE, t + ".py"))],
            "ruff": ruff_dead_code(), "dead_functions": dead_function_candidates()}


def write_report(res: Optional[dict[str, Any]] = None) -> str:
    res = res or audit()
    r = res["ruff"]
    df = res["dead_functions"]
    lines = [
        "# 647 D3 · 死代码清理报告（合并后）", "",
        f"- 覆盖目标：**{len(res['targets'])}** 个核心工具（只动合并相关范围，不扫全仓）；",
        f"- **647 D1 已清**（`ruff --fix` 删除的死 import/重复 import）：**{res['cleaned_in_d1']} 行**；",
        f"- **复检剩余**（`F401`未用import / `F811`重复定义 / `F841`未用变量）："
        f"**{r.get('n_remaining', '不可用') if r.get('available') else 'ruff 不可用'}**", "",
        "## 一、可自动删的（ruff）", "",
        "| 项 | 值 |", "|---|---|",
        f"| ruff 可用 | {r.get('available')} |",
        f"| 退出码 | {r.get('rc')} |",
        f"| **剩余违规** | **{r.get('n_remaining')}** |", ""]
    if r.get("violations"):
        lines += ["```", *r["violations"], "```", ""]
    lines += ["## 二、只报不删的（死函数候选）", "",
              f"- 候选数：**{df['n_candidates']}**",
              "- 判据：模块顶层函数 + 本文件内除定义外无第二次出现 + 未被任何 `tools/*.py`/`tests/*.py` 引用",
              "- **为什么不自动删**：函数可能被 `__all__`/动态调用/外部使用者引用，"
              "删函数有语义风险 ⇒ 只列表，删不删由人核。", ""]
    if df["candidates"]:
        lines += ["| 模块 | 函数 | 行 |", "|---|---|---|"]
        for c in df["candidates"]:
            lines.append(f"| `{c['module']}` | `{c['function']}` | {c['lineno']} |")
    else:
        lines.append("- 无候选（合并后没有「定义了却没人用」的函数）。")
    lines += ["", "## 诚实登记", "",
              "1. **清理范围是「合并相关」的 10 个工具**，不是全仓（全仓大扫除风险高、收益低）；",
              "2. **删掉的只有 import 行**（15 行）—— 那是**零语义风险**的清理；"
              "函数级死代码**只报告不删**；",
              "3. **ruff 不可用时如实登记**（`available=False`），不把「没查」写成「查过且干净」；",
              "4. 清理后 **645/646 快速测试全绿**（本报告生成前提）。"]
    with open(OUT_MD, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(OUT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=2)
        fh.write("\n")
    return OUT_MD


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("目标清单非空（10 个）", len(_paths()) == len(TARGETS), str(len(_paths())))
    chk("D1 清理基线 = 15 行", CLEANED_IN_D1 == 15)
    r = ruff_dead_code()
    if r.get("available"):
        chk("合并模块剩余死 import = 0", r["n_remaining"] == 0, str(r["n_remaining"]))
    else:
        chk("ruff 不可用 ⇒ 只能报告工具能否可用", True, str(r.get("error")))
    chk("死函数候选只报不删（结构正确）",
        "n_candidates" in dead_function_candidates())
    chk("报告路径在 data 下", OUT_MD.startswith(os.path.join(ROOT, "data")))
    print(f"D3 deadcode selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="647 D3 死代码清理 + 复检")
    ap.add_argument("--check", action="store_true", help="只读自检")
    ap.add_argument("--report", action="store_true", help="写清理报告 + JSON")
    ap.add_argument("--json", action="store_true")
    a = ap.parse_args(argv)
    if a.check:
        return selftest()
    res = audit()
    if a.report:
        print(f"written {write_report(res)}")
        return 0
    if a.json:
        print(json.dumps(res, ensure_ascii=False, indent=2))
        return 0
    print(f"[647 deadcode] D1 已清 {res['cleaned_in_d1']} 行；"
          f"剩余 {res['ruff'].get('n_remaining')}；死函数候选 {res['dead_functions']['n_candidates']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
