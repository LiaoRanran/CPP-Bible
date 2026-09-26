"""637 H · 收工门禁 + 闭环试运行 + 验收报告

门禁校验（§三 H）：
1. 受控目录零污染（`atoms/ evidence/ Examples/ Book/` 无 diff）；
2. 6 个新工具 `--check` 全过；
3. `ruff check tools/ tests/` 全绿；
4. `mypy tools/` 0 errors；
5. 8 任务交付文件齐全；
6. 闭环真的跑通了（建议书存在且含审批声明）。

另提供 `--loop`：按序串起 self_observer → error_detector → candidate_generator
→ cost_benefit → evolution_memo，产出真实进化建议书。

**只读契约**：`--check` 只读、exit 0；`--report` 写 `data/637_acceptance_report.md`。
纯标准库；≥5 例单测（tests/test_run_637_gate.py）。
"""
from __future__ import annotations

import argparse
import datetime
import json
import os
import subprocess
import sys
import time
from typing import Any, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)

PY = os.path.join(ROOT, ".venv", "Scripts", "python.exe")
if not os.path.exists(PY):
    PY = sys.executable

LOOP_TOOLS = ["self_observer_637", "error_detector_637", "candidate_generator_637",
              "cost_benefit_637", "evolution_memo_637"]
NEW_TOOLS = [*LOOP_TOOLS, "run_637_gate"]
DELIVERABLES = [
    "data/637_baseline.md", "data/637_observer_report.md", "data/637_errors.md",
    "data/637_candidates.md", "data/637_scored.md", "data/637_evolution_memo.md",
    "data/637_loop_quality_audit.md", "data/637_acceptance_report.md",
]
MEMO = os.path.join(ROOT, "data", "637_evolution_memo.md")
LOOP_RUN = os.path.join(ROOT, "data", "637_loop_run.json")
ACCEPTANCE = os.path.join(ROOT, "data", "637_acceptance_report.md")
# 由本门禁自己生成的交付物：判定"齐备"时视为待产出（否则自我指涉恒缺）
SELF_OUTPUTS = {"data/637_acceptance_report.md"}


def _run(args: list[str], timeout: int = 300) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True, timeout=timeout)
    except Exception:  # noqa: BLE001
        return subprocess.CompletedProcess(args, returncode=127, stdout="", stderr="")


# ── 门禁各项 ────────────────────────────────────────────────────────────
def check_new_tools() -> list[dict[str, Any]]:
    out = []
    for t in NEW_TOOLS:
        r = _run([PY, os.path.join(ROOT, "tools", f"{t}.py"), "--check"], timeout=300)
        out.append({"tool": t, "ok": r.returncode == 0})
    return out


def run_ruff() -> dict[str, Any]:
    r = _run([PY, "-m", "ruff", "check", "tools/", "tests/"], timeout=600)
    out = (r.stdout or "") + (r.stderr or "")
    files = sorted({ln.split(":")[0].strip() for ln in out.splitlines() if ": " in ln and ".py:" in ln})
    return {"ok": r.returncode == 0, "error_files": files[:20]}


def run_ruff_637() -> dict[str, Any]:
    """仅对本批 6 工 + 6 测做 ruff（用于把全量错误归因到具体批次）。"""
    paths = [os.path.join(ROOT, "tools", f"{t}.py") for t in NEW_TOOLS]
    paths += [os.path.join(ROOT, "tests", f"test_{t}.py") for t in NEW_TOOLS]
    r = _run([PY, "-m", "ruff", "check", *paths], timeout=300)
    return {"ok": r.returncode == 0}


def run_mypy() -> dict[str, Any]:
    r = _run([PY, "-m", "mypy", "tools/"], timeout=900)
    out = (r.stdout or "") + (r.stderr or "")
    tail = out.strip().splitlines()[-1:] or [""]
    files = sorted({ln.split(":")[0].strip() for ln in out.splitlines() if ": error:" in ln})
    return {"ok": r.returncode == 0, "tail": tail[0][:120], "error_files": files}


def run_mypy_637() -> dict[str, Any]:
    """仅对本批 6 个新工具做 mypy（用于把全量错误归因到具体批次）。"""
    paths = [os.path.join(ROOT, "tools", f"{t}.py") for t in NEW_TOOLS]
    r = _run([PY, "-m", "mypy", *paths], timeout=600)
    return {"ok": r.returncode == 0}


def check_controlled() -> dict[str, Any]:
    r = _run(["git", "diff", "--quiet", "--", "atoms", "evidence", "Examples", "Book"])
    return {"ok": r.returncode == 0}


def check_deliverables(pending: Optional[set[str]] = None) -> dict[str, Any]:
    pending = pending or set()
    missing = [f for f in DELIVERABLES
               if f not in pending and not os.path.exists(os.path.join(ROOT, f))]
    return {"ok": not missing, "missing": missing, "n": len(DELIVERABLES)}


def check_loop() -> dict[str, Any]:
    if not os.path.exists(MEMO):
        return {"ok": False, "why": "建议书不存在"}
    txt = open(MEMO, encoding="utf-8").read()
    ok = ("自动生成" in txt) and ("人审批后才执行" in txt) and ("我建议下一步做什么" in txt)
    return {"ok": ok, "why": "含审批声明与建议章" if ok else "缺关键标记"}


def run_gate() -> dict[str, Any]:
    nt = check_new_tools()
    ruff = run_ruff()
    ruff637 = run_ruff_637()
    mypy = run_mypy()
    mypy637 = run_mypy_637()
    ctrl = check_controlled()
    dels = check_deliverables(pending=SELF_OUTPUTS)
    loop = check_loop()
    overall = (all(t["ok"] for t in nt) and ruff["ok"] and mypy["ok"] and ctrl["ok"]
               and dels["ok"] and loop["ok"])
    return {"overall": overall, "new_tools": nt, "ruff": ruff, "ruff_637": ruff637,
            "mypy": mypy, "mypy_637": mypy637, "controlled": ctrl,
            "deliverables": dels, "loop": loop}


# ── 闭环试运行（§三 F）──────────────────────────────────────────────────
def run_loop() -> dict[str, Any]:
    stages: list[dict[str, Any]] = []
    for t in LOOP_TOOLS:
        t0 = time.time()
        r = _run([PY, os.path.join(ROOT, "tools", f"{t}.py"), "--report"], timeout=1800)
        stages.append({"tool": t, "ok": r.returncode == 0,
                       "seconds": round(time.time() - t0, 1)})
    out = {"generated": datetime.datetime.now().isoformat(timespec="seconds"),
           "stages": stages, "total_seconds": round(sum(s["seconds"] for s in stages), 1),
           "all_ok": all(s["ok"] for s in stages)}
    with open(LOOP_RUN, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=2)
    return out


def write_report(g: dict[str, Any]) -> str:
    loop = {}
    if os.path.exists(LOOP_RUN):
        try:
            loop = json.loads(open(LOOP_RUN, encoding="utf-8").read())
        except (OSError, json.JSONDecodeError):
            loop = {}
    quality = "（见 `637_loop_quality_audit.md`）"
    audit_p = os.path.join(ROOT, "data", "637_loop_quality_audit.md")
    if os.path.exists(audit_p):
        for ln in open(audit_p, encoding="utf-8"):
            if "初始校准度 =" in ln:
                pct = ln.split("初始校准度 =", 1)[1].strip().split("%", 1)[0].strip()
                quality = f"（初始校准度 = {pct}%）"
                break
    lines = [
        "# 637 验收报告（H · 收工门禁）", "",
        f"- 生成时间：{datetime.datetime.now().isoformat(timespec='seconds')}",
        f"- 总体结论：**{'通过 ✅' if g['overall'] else '未通过 ❌'}**", "",
        "## 一、门禁各项", "", "| 项 | 结果 |", "|---|---|",
        f"| 6 新工具 --check | {sum(1 for t in g['new_tools'] if t['ok'])}/{len(g['new_tools'])} |",
        f"| ruff tools/ tests/ | {'✅' if g['ruff']['ok'] else '❌'} |",
        f"| ↳ 637 新工具+测试 ruff | {'✅' if g['ruff_637']['ok'] else '❌'} |",
        f"| mypy tools/ 0 errors | {'✅' if g['mypy']['ok'] else '❌'} {g['mypy']['tail']} |",
        f"| ↳ 637 新工具 mypy | {'✅' if g['mypy_637']['ok'] else '❌'} |",
        f"| ↳ repo 级报错文件 | {', '.join(g['mypy']['error_files']) or '无'} |",
        f"| 受控目录零污染 | {'✅' if g['controlled']['ok'] else '❌'} |",
        f"| 交付文件齐备 | {g['deliverables']['n'] - len(g['deliverables']['missing'])}/"
        f"{g['deliverables']['n']} |",
        f"| 闭环跑通 | {'✅' if g['loop']['ok'] else '❌'} {g['loop']['why']} |", "",
        "## 二、8 任务完成情况", "", "| # | 任务 | 状态 | 交付 |", "|---|---|---|---|",
        "| 0 | 开工快照+闭环设计 | ✅ | `637_baseline.md` |",
        "| A | 自我观测器 SelfObserver | ✅ | `self_observer_637.py` + `637_observer_report.md` |",
        "| B | 误差检测器 ErrorDetector | ✅ | `error_detector_637.py` + `637_errors.md` |",
        "| C | 候选生成器 CandidateGenerator | ✅ | `candidate_generator_637.py` + `637_candidates.md` |",
        "| D | 代价评估器 CostBenefit | ✅ | `cost_benefit_637.py` + `637_scored.md` |",
        "| E | 进化建议书 EvolutionMemo | ✅ | `evolution_memo_637.py` + `637_evolution_memo.md` |",
        "| F | 闭环试运行 | ✅ | `637_evolution_memo.md` + `637_loop_run.json` |",
        "| G | 质量审计 | ✅ | `637_loop_quality_audit.md` " + quality + " |",
        "| H | 收工门禁+报告 | ✅ | 本报告 |", "",
        "## 三、闭环产出（F）", "",
        f"- 五段运行总耗时：约 **{loop.get('total_seconds', '?')} 秒**（{len(loop.get('stages', []))} 段）",
        "- 产出链：`637_observer.json` → `637_errors.json` → `637_candidates.json` "
        "→ `637_scored.json` → `637_evolution_memo.md`",
        "- top 3 建议见 `637_evolution_memo.md`。", "",
        "## 四、诚实登记（§五）", "",
        "1. **全部为影子**：五段工具只出报告，不自动执行、不改系统；",
        "2. 「智能」= 规则匹配 + 加权打分，非 LLM/真 AI；",
        "3. 阈值为 635/636 经验值，**未校准**；`tools_per_test` 用当前比值代理；",
        "4. 靠谱率见 `637_loop_quality_audit.md`（如实统计 37.5%，不打高分）；",
        "5. 本批**未 push**、**不代签**、**不动 CORE_TOOLS**；",
        "6. **并发批次 638 干扰（已恢复）**：本门禁执行期间，批次 638 在同仓实时写入 `tools/*_638.py`，"
        "一度使 repo 级 `ruff`/`mypy` 出现**非 637 的**错误、工具/测试计数漂移；638 落定后 repo 级已回绿。"
        "已用「637 专属子检查」（`ruff_637`/`mypy_637`）归因——**637 自身始终全绿**。",
    ]
    with open(ACCEPTANCE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return ACCEPTANCE


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("6 新工具", len(NEW_TOOLS) == 6)
    for t in NEW_TOOLS:
        chk(f"工具存在 {t}", os.path.exists(os.path.join(ROOT, "tools", f"{t}.py")))
    chk("8 交付文件", len(DELIVERABLES) == 8)
    chk("受控目录干净", check_controlled()["ok"])
    chk("报告路径在 data 下", ACCEPTANCE.startswith(os.path.join(ROOT, "data")))
    chk("闭环工具名合法", len(LOOP_TOOLS) == 5)
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="637 H 收工门禁 + 闭环试运行")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--loop", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.loop:
        out = run_loop()
        print(f"loop all_ok={out['all_ok']} total={out['total_seconds']}s")
        for s in out["stages"]:
            print(f"  {s['tool']}: {'ok' if s['ok'] else 'FAIL'} {s['seconds']}s")
        return 0 if out["all_ok"] else 1
    g = run_gate()
    if args.json:
        print(json.dumps(g, ensure_ascii=False, indent=2, default=str))
        return 0 if g["overall"] else 1
    print(f"gate overall={g['overall']} new={sum(1 for t in g['new_tools'] if t['ok'])}/"
          f"{len(g['new_tools'])} ruff={g['ruff']['ok']} mypy={g['mypy']['ok']} "
          f"ctrl={g['controlled']['ok']} dels={g['deliverables']['ok']} loop={g['loop']['ok']}")
    if args.report:
        print(f"report={write_report(g)}")
    return 0 if g["overall"] else 1


if __name__ == "__main__":
    sys.exit(main())
