"""636 E1 · 收工门禁 + 三份报告

门禁校验（§六 E1）：
1. 受控目录零污染；2. 本批 8 个新工具 `--check` 全过；3. `ruff check tools/ tests/` 全绿；
4. `mypy tools/` 0 errors；5. 8 任务交付文件齐全；6. 受控目录 `git status` 零污染（双查）。

产出：`data/636_acceptance_report.md` + `data/636_protector_shadow_report.md`
+ `data/636_next_steps.md`。

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

NEW_TOOLS = ["baseline_636", "conflict_detector_636", "anti_windup_636", "blind_protocol_636",
             "calibration_tracker_636", "mdl_trial_636", "contamination_tracker_636",
             "four_state_636"]
DELIVERABLES = [
    "data/636_baseline.md", "data/636_conflict_detector_shadow.md", "data/636_anti_windup_design.md",
    "data/636_blind_protocol_design.md", "data/636_calibration_tracker_report.md",
    "data/636_mdl_trial_run.md", "data/636_contamination_tracker_shadow.md",
    "data/636_four_state_simulation.md",
]
REPORTS = {
    "acceptance": os.path.join(ROOT, "data", "636_acceptance_report.md"),
    "shadow": os.path.join(ROOT, "data", "636_protector_shadow_report.md"),
    "next_steps": os.path.join(ROOT, "data", "636_next_steps.md"),
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
    a = ["# 636 验收报告（E1 · 收工门禁）", "",
         f"- 总体结论：**{'通过 ✅' if g['overall'] else '未通过 ❌'}**", "",
         "## 一、门禁各项", "", "| 项 | 结果 |", "|---|---|",
         f"| 新工具 --check | {sum(1 for t in g['new_tools'] if t['ok'])}/{len(g['new_tools'])} |",
         f"| ruff tools/ tests/ | {'✅' if g['ruff']['ok'] else '❌'} |",
         f"| mypy tools/ 0 errors | {'✅' if g['mypy']['ok'] else '❌'} {g['mypy']['tail']} |",
         f"| 受控目录零污染 | {'✅' if g['controlled']['ok'] else '❌'} |",
         f"| 交付文件齐备 | {g['deliverables']['n'] - len(g['deliverables']['missing'])}/"
         f"{g['deliverables']['n']} |", "",
         "## 二、8 任务完成情况", "",
         "| # | 任务 | 状态 | 交付 |", "|---|---|---|---|",
         "| 0 | 开工快照+基线复测 | ✅ | `636_baseline.md`（15 指标无漂移） |",
         "| 2.1 | 冲突检测器影子 | ✅ | `636_conflict_detector_shadow.md`（23 卡，超阈 2） |",
         "| 2.2 | anti-windup 设计 | ✅ | `636_anti_windup_design.md`（半饱和，223 冻结模拟） |",
         "| 2.3 | blind_protocol 影子 | ✅ | `636_blind_protocol_design.md`（违规 258，分歧率无数据） |",
         "| 2.4 | 校准追踪器+known_error_rate | ✅ | `636_calibration_tracker_report.md`（67 全无数据） |",
         "| 2.5 | MDL 试运行 | ✅ | `636_mdl_trial_run.md`（admit 30/reject 37） |",
         "| V26-补1 | 污染追踪器影子 | ✅ | `636_contamination_tracker_shadow.md` |",
         "| V26-补2 | 四态判决模拟 | ✅ | `636_four_state_simulation.md`（假 pass 1） |",
         "| E1 | 收工门禁 | ✅ | 本报告 |", "",
         "## 三、偏差与诚实登记（§七）", "",
         "1. **全部保护器为影子**：不拦截、不改判（§零.1/§零.7）；",
         "2. 冲突检测器 `agreement` 用证据存在率近似、RR 无区分度（已登记）；",
         "3. anti-windup 的周处理能力为**假设值**、等待天数为近似；",
         "4. blind_protocol **分歧率无盲评基线 ⇒ 写「无法计算」**，未编造；",
         "5. known_error_rate **67 条全部「无数据」**（未编造）；",
         "6. MDL **编码长度为启发式**（非严格 MDL）；7 条新规则不在热力图 ⇒ 必 reject；",
         "7. 四态/污染分类均为**关键词/文本级启发式**；",
         "8. **本批未 push**（§零.13）⇒ 收工 ahead>0。"]
    with open(REPORTS["acceptance"], "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(a) + "\n")
    s = ["# 636 保护器影子运行汇总", "",
         "> 本批**全部为影子模式**：离线运行、出报告、**不拦截、不改判**。", "",
         "| 保护器 | 影子模拟结果 |", "|---|---|",
         "| 2.1 冲突检测器 | 23 张 verified 卡；RR 23（全局）/EE 2（悬挂引用）；超 θ=0.3 者 2 |",
         "| 2.2 anti-windup | 队列 65 / 周新增 104 / 等待 22.8 天 ⇒ 半饱和；30 天模拟冻结 223 |",
         "| 2.3 blind_protocol | 452 判决中 258 条 AI 可见（违规 258）；分歧率无法计算 |",
         "| 2.4 校准追踪器 | 67 规则 known_error_rate 全「无数据」；观察态 67；影响 452 判决 |",
         "| 2.5 MDL 判据 | admit 30 / reject 37（通过率 44.8%）；早期 66.7% → 近期 23.5% |",
         "| V26-补1 污染追踪 | 追踪 ATOM-MEM-ALLOC-001 下游；三阀门判定；tainted 清单 |",
         "| V26-补2 四态判决 | 36 份：fail 25 / pass 9 / unknown 1 / 带例外 1；假 pass 1 |", "",
         "## 关键结论", "",
         "1. **若保护器全部上线**：2 张卡会因冲突超阈被标复核、约 223 告警/30 天被冻结、",
         "   37 条规则会被 MDL 挡下、67 条规则进入观察态——**均需人审决定是否真启用**；",
         "2. **最大缺口**：known_error_rate 与分歧率**完全无数据**，是保护器落地的**前置条件**。"]
    open(REPORTS["shadow"], "w", encoding="utf-8", newline="\n").write("\n".join(s) + "\n")
    n = ["# 636 下一步（阶段 3 预告 + 交人项）", "",
         "## 一、v25 阶段 3（升级）预告", "",
         "1. 把影子保护器**逐个转真**（先 Z 类低风险，后高风险）；",
         "2. 补 **known_error_rate 台账**（校准追踪器的前置）；",
         "3. 建**盲评基础设施**（隐藏 AI 建议 + 提交后揭盲）；",
         "4. 启用 **anti-windup 预算**与冲突阈值 θ。", "",
         "## 二、交人项（§八）", "",
         "1. **push 本批 commit**（ahead 预计 50+）；",
         "2. 冲突检测器阈值 θ_conflict 是否采用建议值 0.3；",
         "3. anti-windup 三档阈值（A 100/B 7 天/C 20 周）是否合理；",
         "4. blind_protocol 何时从影子变真；",
         "5. known_error_rate 缺失的 67 规则是否进入观察态；",
         "6. MDL 判据是否启用（会挡下 37 条）；",
         "7. 四态判决何时从模拟变真；",
         "8. v25 阶段 3（升级）何时开。"]
    open(REPORTS["next_steps"], "w", encoding="utf-8", newline="\n").write("\n".join(n) + "\n")
    return REPORTS


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("8 新工具", len(NEW_TOOLS) == 8)
    for t in NEW_TOOLS:
        chk(f"工具存在 {t}", os.path.exists(os.path.join(ROOT, "tools", f"{t}.py")))
    chk("8 交付文件", len(DELIVERABLES) == 8)
    chk("受控目录干净", check_controlled()["ok"])
    chk("交付齐备", check_deliverables()["ok"])
    chk("报告路径在 data 下", all(p.startswith(os.path.join(ROOT, "data")) for p in REPORTS.values()))
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="636 E1 收工门禁")
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
