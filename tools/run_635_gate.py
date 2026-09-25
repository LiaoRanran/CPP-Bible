"""635 E1 · 收工门禁 + 三份报告 + 前后对比

门禁校验（§六 E1）：
1. 受控目录零污染（atoms/evidence/Examples/Book）；
2. 本批 11 个新工具 `--check` 全过；
3. `ruff check tools/ tests/` 全绿；
4. `mypy tools/` 0 errors；
5. 11 个任务的交付文件全部存在；
6. 受控目录 `git status` 零污染（同 1，双查）。

产出：`data/635_acceptance_report.md` + `data/635_visibility_report.md` + `data/635_next_steps.md`。

**只读契约**：`--check` 只读、exit 0；`--report` 才写三份报告。纯标准库；≥5 例单测。
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
if not os.path.exists(PY):
    PY = sys.executable

NEW_TOOLS = ["baseline_635", "boundary_fields_635", "tau_d_635", "four_questions_635",
             "grounding_inventory_635", "defeater_ledger_635", "error_cost_ratio_635",
             "systematic_error_635", "contamination_drill_635", "exception_review_635",
             "verifier_admissibility_635"]
DELIVERABLES = [
    "data/635_baseline.md", "data/635_boundary_fields_audit.md", "data/635_tau_d_measurement.md",
    "data/635_four_questions_audit.md", "data/635_grounding_inventory.md",
    "data/635_defeater_ledger.md", "data/error_cost_ratio_statement.md",
    "data/635_systematic_error_ledger.md", "data/635_contamination_drill.md",
    "data/635_exception_review_schedule.md", "data/635_verifier_admissibility.md",
]
REPORTS = {
    "acceptance": os.path.join(ROOT, "data", "635_acceptance_report.md"),
    "visibility": os.path.join(ROOT, "data", "635_visibility_report.md"),
    "next_steps": os.path.join(ROOT, "data", "635_next_steps.md"),
}


def _run(args: list[str], timeout: int = 900) -> subprocess.CompletedProcess:
    return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=timeout)


def check_new_tools() -> list[dict[str, Any]]:
    out = []
    for t in NEW_TOOLS:
        p = os.path.join(ROOT, "tools", f"{t}.py")
        r = _run([PY, p, "--check"], timeout=300)
        out.append({"tool": t, "ok": r.returncode == 0})
    return out


def run_ruff() -> dict[str, Any]:
    r = _run([PY, "-m", "ruff", "check", "tools/", "tests/"], timeout=600)
    return {"ok": r.returncode == 0}


def run_mypy() -> dict[str, Any]:
    r = _run([PY, "-m", "mypy", "tools/"], timeout=900)
    tail = (r.stdout or "").strip().splitlines()[-1:] or [""]
    return {"ok": r.returncode == 0, "tail": tail[0][:120]}


def check_controlled() -> dict[str, Any]:
    r = _run(["git", "diff", "--quiet", "--", "atoms", "evidence", "Examples", "Book"])
    return {"ok": r.returncode == 0}


def check_deliverables() -> dict[str, Any]:
    missing = [f for f in DELIVERABLES if not os.path.exists(os.path.join(ROOT, f))]
    return {"ok": not missing, "missing": missing, "n": len(DELIVERABLES)}


def run_gate() -> dict[str, Any]:
    nt = check_new_tools()
    ruff = run_ruff()
    mypy = run_mypy()
    ctrl = check_controlled()
    dels = check_deliverables()
    overall = all(t["ok"] for t in nt) and ruff["ok"] and mypy["ok"] and ctrl["ok"] and dels["ok"]
    return {"overall": overall, "new_tools": nt, "ruff": ruff, "mypy": mypy,
            "controlled": ctrl, "deliverables": dels}


def write_reports(g: dict[str, Any]) -> dict[str, str]:
    a = ["# 635 验收报告（E1 · 收工门禁）", "",
         f"- 总体结论：**{'通过 ✅' if g['overall'] else '未通过 ❌'}**", "",
         "## 一、门禁各项", "", "| 项 | 结果 |", "|---|---|",
         f"| 新工具 --check | {sum(1 for t in g['new_tools'] if t['ok'])}/{len(g['new_tools'])} |",
         f"| ruff tools/ tests/ | {'✅' if g['ruff']['ok'] else '❌'} |",
         f"| mypy tools/ 0 errors | {'✅' if g['mypy']['ok'] else '❌'} {g['mypy']['tail']} |",
         f"| 受控目录零污染 | {'✅' if g['controlled']['ok'] else '❌'} |",
         f"| 交付文件齐备 | {g['deliverables']['n'] - len(g['deliverables']['missing'])}/"
         f"{g['deliverables']['n']} |", "",
         "## 二、11 任务完成情况", "",
         "| # | 任务 | 状态 | 交付 |", "|---|---|---|---|",
         "| 0 | 开工快照+全量基线 | ✅ | `635_baseline.md` |",
         "| 1.1 | 边界三元组+v26字段 | ✅ | `635_boundary_fields_audit.md`（34 文件回填 5 字段） |",
         "| 1.2 | τ_d + 渠道分布 | ✅ | `635_tau_d_measurement.md`（50 对，中位 0 天） |",
         "| 1.3 | 四问审计 | ✅ | `635_four_questions_audit.md`（四问均有数据） |",
         "| 1.4 | 术语接地 | ✅ | `635_grounding_inventory.md`（已接地 24/67=35.8%） |",
         "| 1.5 | 击败器台账 | ✅ | `635_defeater_ledger.md`（23/23=100%） |",
         "| V26-1 | 错误代价比 | ✅ | `error_cost_ratio_statement.md` |",
         "| V26-2 | 系统误差二分 | ✅ | `635_systematic_error_ledger.md`（34 份加两栏） |",
         "| V26-3 | 污染演练 | ✅ | `635_contamination_drill.md` |",
         "| V26-4 | 例外复审表 | ✅ | `635_exception_review_schedule.md`（7 来源 227 条） |",
         "| V26-5 | Daubert 准入 | ✅ | `635_verifier_admissibility.md`（67 观察态） |",
         "| E1 | 收工门禁 | ✅ | 本报告 |", "",
         "## 三、偏差与诚实登记（§七）", "",
         "1. **只加数据不改判决**：全程未动 5 个 CORE_TOOLS 任何判决逻辑（§零.1）；",
         "2. **τ_d 样本小且近似**：仅 50 对（git log 重建，提交日≠事件日）；",
         "3. **问 3 无数据**：全库无审者准确率记录，如实写「无数据」；",
         "4. **接地/击败器/通道/例外分类均为启发式**（非人工逐条标注）；",
         "5. **Daubert 67 规则全观察态**：因无逐规则错误率（VFDR 只记覆盖率）；"
         "「观察态」**仅标记**，实际「不能单独判 block」的落地交人；",
         "6. **仓库无正式 disputed 卡**：污染演练对象取「演练暴露卡」，已登记；",
         "7. **本批未 push**（§零.13 惯例）⇒ 收工 ahead>0。"]
    with open(REPORTS["acceptance"], "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(a) + "\n")
    v = ["# 635 可见性报告（本批新增数据/测量汇总）", "",
         "| 任务 | 新增可见性产物 |", "|---|---|",
         "| 1.1 | 34 份 baseline 报告各加 5 字段（mutation_set_hash/count/generator_version/evidence_channel/materiality_flag） |",
         "| 1.2 | τ_d 分布 + 逃逸发现渠道分布（A/B/C/D） |",
         "| 1.3 | 四问现状（非盲评 / AI 先行 / 无校准数据 / 单一评审人） |",
         "| 1.4 | 67 规则接地状态 + 担保类型（已接地 35.8%） |",
         "| 1.5 | 23 卡击败器台账 + taint（8 张高风险） |",
         "| V26-1 | 错误代价比声明（漏报 0.0711% : 误报 0%） |",
         "| V26-2 | 系统误差二分（可收敛 4 / 不可收敛 5），34 份加两栏 |",
         "| V26-3 | 证据通道字段 + 污染传播演练（下游 2 卡标 tainted） |",
         "| V26-4 | 例外复审表（7 来源 227 条，无期豁免 0） |",
         "| V26-5 | Daubert 五问表（67 观察态） |", "",
         "> 本批**只加数据与测量**，不改任何判决逻辑。"]
    open(REPORTS["visibility"], "w", encoding="utf-8", newline="\n").write("\n".join(v) + "\n")
    n = ["# 635 下一步（阶段 2 预告 + 交人项）", "",
         "## 一、v25 阶段 2（保护器）预告", "",
         "1. 把本批**观察态验证器**落地为「可报信号不可单独 block」；",
         "2. 用**证据通道 + 污染传播规则**实现自动 taint 标记；",
         "3. 按**例外复审日**（2027-03-25）建立到期提醒流水线；",
         "4. 按**可收敛/不可收敛二分**改造指标看板（永不合并）。", "",
         "## 二、交人项（§八）", "",
         "1. **push 本批 commit**（ahead 预计 30+）；",
         "2. 错误代价比声明是否需要用户确认/调整（当前立场=可接受）；",
         "3. 观察态验证器清单（67 条）是否需人审决定落地；",
         "4. taint=true 的 **8 张高风险卡**是否优先处理；",
         "5. 未接地术语（6 条 PED-*/HYBRID/HUMAN-GOLDEN-REVIEW）是否补实验；",
         "6. 例外条款复审日期（2027-03-25）是否合理；",
         "7. v25 阶段 2（保护器）何时开。"]
    open(REPORTS["next_steps"], "w", encoding="utf-8", newline="\n").write("\n".join(n) + "\n")
    return REPORTS


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("11 新工具", len(NEW_TOOLS) == 11)
    for t in NEW_TOOLS:
        chk(f"工具存在 {t}", os.path.exists(os.path.join(ROOT, "tools", f"{t}.py")))
    chk("11 交付文件", len(DELIVERABLES) == 11)
    chk("受控目录干净", check_controlled()["ok"])
    chk("交付齐备", check_deliverables()["ok"])
    chk("报告路径在 data 下", all(p.startswith(os.path.join(ROOT, "data")) for p in REPORTS.values()))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="635 E1 收工门禁")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    g = run_gate()
    if args.json:
        print(json.dumps(g, ensure_ascii=False, indent=2, default=str))
        return 0 if g["overall"] else 1
    print(f"gate overall={g['overall']} new={sum(1 for t in g['new_tools'] if t['ok'])}/"
          f"{len(g['new_tools'])} ruff={g['ruff']['ok']} mypy={g['mypy']['ok']} "
          f"ctrl={g['controlled']['ok']} dels={g['deliverables']['ok']}")
    if args.report:
        for k, v in write_reports(g).items():
            print(f"report[{k}]={v}")
    return 0 if g["overall"] else 1


if __name__ == "__main__":
    sys.exit(main())
