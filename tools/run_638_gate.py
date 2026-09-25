"""638 E1 · 收工门禁 + 验收报告

门禁校验（§三.E1）：
1. 受控目录零污染（`atoms/ evidence/ Examples/ Book/` 无 diff）；
2. **7 个新工具** `--check` 全过（exit 0）；
3. `ruff check tools/ tests/` 全绿；
4. `mypy tools/` **0 errors**；
5. **8 个任务**的交付文件全部存在；
6. 638 测试套件跑绿（`pytest -k 638`）。

**只读契约**：`--check` 只读、exit 0、不写盘；`--report` 才写
`data/638_acceptance_report.md` + `data/638_gate_result.json`。
纯标准库；≥5 例单测（tests/test_run_638_gate.py）。
"""
from __future__ import annotations

import argparse
import datetime
import glob
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

ACCEPTANCE = os.path.join(ROOT, "data", "638_acceptance_report.md")
RESULT_JSON = os.path.join(ROOT, "data", "638_gate_result.json")

CONTROLLED = ["atoms", "evidence", "Examples", "Book"]

NEW_TOOLS = [
    "four_state_verdict_638", "lifecycle_fsm_638", "error_rate_collector_638",
    "rr_conflict_classifier_638", "loop_rerun_638", "loop_tuning_638", "run_638_gate",
]

# 8 个任务 → 交付物
TASK_DELIVERABLES: list[dict[str, Any]] = [
    {"task": "0", "name": "开工快照 + 637 闭环复盘", "files": ["data/638_baseline.md"]},
    {"task": "3.1", "name": "四态结论 schema", "files": [
        "tools/four_state_verdict_638.py", "tests/test_four_state_verdict_638.py",
        "data/638_four_state_schema.md"]},
    {"task": "3.2", "name": "Lifecycle FSM", "files": [
        "tools/lifecycle_fsm_638.py", "tests/test_lifecycle_fsm_638.py",
        "data/638_lifecycle_fsm.md"]},
    {"task": "B1", "name": "known_error_rate 收集器", "files": [
        "tools/error_rate_collector_638.py", "tests/test_error_rate_collector_638.py",
        "data/638_error_rate_estimate.md"]},
    {"task": "B2", "name": "RR 冲突分类器", "files": [
        "tools/rr_conflict_classifier_638.py", "tests/test_rr_conflict_classifier_638.py",
        "data/638_rr_conflict_analysis.md"]},
    {"task": "C1", "name": "闭环第二次运行", "files": [
        "tools/loop_rerun_638.py", "tests/test_loop_rerun_638.py",
        "data/638_evolution_memo.md"]},
    {"task": "C2", "name": "闭环规则调优", "files": [
        "tools/loop_tuning_638.py", "tests/test_loop_tuning_638.py",
        "data/638_loop_tuning.md"]},
    {"task": "E1", "name": "收工门禁 + 报告", "files": [
        "tools/run_638_gate.py", "tests/test_run_638_gate.py",
        "data/638_acceptance_report.md"]},
]


def _run(args: list[str], timeout: int = 1800) -> subprocess.CompletedProcess:
    try:
        return subprocess.run(args, cwd=ROOT, capture_output=True, text=True,
                              timeout=timeout)
    except Exception:  # noqa: BLE001
        return subprocess.CompletedProcess(args, returncode=127, stdout="", stderr="")


# ── 1. 受控目录 ─────────────────────────────────────────────────────────
def check_controlled() -> dict[str, Any]:
    r = _run(["git", "diff", "--quiet", "--", *CONTROLLED])
    return {"ok": r.returncode == 0, "exit": r.returncode}


# ── 2. 工具 --check ─────────────────────────────────────────────────────
def run_tools() -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    for t in NEW_TOOLS:
        p = os.path.join(ROOT, "tools", f"{t}.py")
        r = _run([PY, p, "--check"], timeout=600)
        out.append({"tool": t, "exists": os.path.exists(p), "exit": r.returncode,
                    "ok": os.path.exists(p) and r.returncode == 0})
    return out


# ── 3. ruff ─────────────────────────────────────────────────────────────
def run_ruff() -> dict[str, Any]:
    r = _run([PY, "-m", "ruff", "check", "tools/", "tests/"])
    tail = [ln for ln in (r.stdout or "").strip().splitlines()[-3:] if ln.strip()]
    return {"ok": r.returncode == 0, "exit": r.returncode, "tail": tail}


# ── 4. mypy ─────────────────────────────────────────────────────────────
def run_mypy() -> dict[str, Any]:
    r = _run([PY, "-m", "mypy", "tools/"])
    txt = (r.stdout or "") + (r.stderr or "")
    ok = r.returncode == 0 and "Success: no issues found" in txt
    tail = [ln for ln in txt.strip().splitlines()[-2:] if ln.strip()]
    return {"ok": ok, "exit": r.returncode, "tail": tail}


# ── 5. 交付物 ───────────────────────────────────────────────────────────
def check_deliverables(pending: Optional[list[str]] = None) -> dict[str, Any]:
    """检查 8 任务交付物是否存在。

    `pending`：**本次运行即将生成**的文件（只有验收报告自身）——标记为 ok 并注明，
    避免「报告必须先存在才能被检查」的自举悖论。`--check` 不传该参数（严格只读）。
    """
    pend = set(pending or [])
    rows = []
    missing: list[str] = []
    n = 0
    for d in TASK_DELIVERABLES:
        for f in d["files"]:
            n += 1
            ok = os.path.exists(os.path.join(ROOT, f.replace("/", os.sep)))
            is_pending = (not ok) and f in pend
            if not ok and not is_pending:
                missing.append(f)
            rows.append({"task": d["task"], "file": f, "ok": ok or is_pending,
                         "pending": is_pending})
    return {"n": n, "missing": missing, "ok": not missing, "rows": rows}


# ── 6. 638 测试套件 ─────────────────────────────────────────────────────
def run_tests() -> dict[str, Any]:
    files = sorted(glob.glob(os.path.join(ROOT, "tests", "test_*638*.py")))
    if not files:
        return {"ok": False, "why": "未找到 638 测试文件", "n_files": 0}
    r = _run([PY, "-m", "pytest", *[os.path.relpath(f, ROOT) for f in files],
              "-q", "-p", "no:cacheprovider"], timeout=1800)
    lines = [ln.strip() for ln in (r.stdout or "").splitlines() if ln.strip()]
    summary = next((ln for ln in reversed(lines)
                    if "passed" in ln or "failed" in ln or "error" in ln),
                   lines[-1] if lines else "")
    # 进度行（`....  [100%]`）的点数 = 通过用例数（本环境 pytest 汇总行常被截断）
    n_dots = sum(ln.count(".") for ln in lines if "[100%]" in ln)
    return {"ok": r.returncode == 0, "exit": r.returncode, "n_files": len(files),
            "n_passed": n_dots, "tail": summary}


def build(pending: Optional[list[str]] = None) -> dict[str, Any]:
    tools = run_tools()
    ruff = run_ruff()
    mypy = run_mypy()
    ctrl = check_controlled()
    dels = check_deliverables(pending)
    tests = run_tests()
    overall = (all(t["ok"] for t in tools) and ruff["ok"] and mypy["ok"]
               and ctrl["ok"] and dels["ok"] and tests["ok"])
    return {"generated": datetime.datetime.now().isoformat(timespec="seconds"),
            "overall": overall, "tools": tools, "ruff": ruff, "mypy": mypy,
            "controlled": ctrl, "deliverables": dels, "tests": tests}


# ── 报告 ────────────────────────────────────────────────────────────────
def write_report(g: Optional[dict[str, Any]] = None) -> dict[str, str]:
    # 自举：本报告由本次运行生成，检查交付物时按 pending 处理
    g = g or build(pending=["data/638_acceptance_report.md"])
    with open(RESULT_JSON, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(g, fh, ensure_ascii=False, indent=2)
    ok_tools = sum(1 for t in g["tools"] if t["ok"])
    lines = [
        "# 638 验收报告（收工门禁自动生成）", "",
        f"> 生成时间：{g['generated']}；工具：`tools/run_638_gate.py`。",
        f"> **总判定：{'PASS' if g['overall'] else 'FAIL'}**", "",
        "## 一、门禁结果", "",
        "| 检查项 | 结果 |", "|---|---|",
        f"| 受控目录零污染 | {'✅' if g['controlled']['ok'] else '❌'} |",
        f"| 7 个新工具 `--check` | {'✅' if ok_tools == len(g['tools']) else '❌'} "
        f"{ok_tools}/{len(g['tools'])} |",
        f"| ruff tools/ tests/ | {'✅' if g['ruff']['ok'] else '❌'} "
        f"{' '.join(g['ruff']['tail'][-1:]) if g['ruff']['tail'] else ''} |",
        f"| mypy tools/ 0 errors | {'✅' if g['mypy']['ok'] else '❌'} "
        f"{' '.join(g['mypy']['tail'][-1:]) if g['mypy']['tail'] else ''} |",
        f"| 交付文件齐备 | {'✅' if g['deliverables']['ok'] else '❌'} "
        f"{g['deliverables']['n'] - len(g['deliverables']['missing'])}/"
        f"{g['deliverables']['n']} |",
        f"| 638 测试套件 | {'✅' if g['tests']['ok'] else '❌'} "
        f"{g['tests'].get('n_passed', '?')} 例通过 / "
        f"{g['tests'].get('n_files', 0)} 个测试文件 |", "",
        "## 二、8 个任务交付情况", "",
        "| 任务 | 名称 | 交付文件 | 存在 |", "|---|---|---|---|",
    ]
    for d in TASK_DELIVERABLES:
        marks = []
        for f in d["files"]:
            ok = os.path.exists(os.path.join(ROOT, f.replace("/", os.sep)))
            marks.append(f"{'✅' if ok else '❌'} `{os.path.basename(f)}`")
        lines.append(f"| {d['task']} | {d['name']} | {'; '.join(marks)} | "
                     f"{'✅' if all(os.path.exists(os.path.join(ROOT, f.replace('/', os.sep))) for f in d['files']) else '❌'} |")

    lines += [
        "", "## 三、本批核心结论（实测）", "",
        "| 项 | 结果 | 来源 |", "|---|---|---|",
        "| 四态 schema | 已定义并强制边界三元组；**23 张 verified 卡 0 边界 ⇒ 全 `unknown`** | "
        "`638_four_state_schema.md` |",
        "| Lifecycle FSM | 五态 + 11 条合法迁移；28 卡初态 `draft 2 / verified 26`；"
        "**0 卡有 `lifecycle` 字段** | `638_lifecycle_fsm.md` |",
        "| known_error_rate | **67/67 规则「无数据」**（ledger 无规则字段、target_type 全 edge）；"
        "全库代理：改判率 18.81% / 人审改判 8.76% / 逃逸率 0.071% | `638_error_rate_estimate.md` |",
        "| RR 冲突 | 同 scope 候选 **927 对**（退化），**高置信仅 24 对**"
        "（type1 6 / type2 14 / type3 4）；卡级 23 张全分类 | `638_rr_conflict_analysis.md` |",
        "| 闭环第二次运行 | 异常 **4 → 2**，误报 **2 → 0**（误报率 0.5 → 0.0），top3 已变 | "
        "`638_evolution_memo.md` |",
        "| 闭环调参 | 3 项（T1/T2/T3），**未改 637 工具**（覆盖层实现） | `638_loop_tuning.md` |", "",
        "## 四、诚实登记", "",
        "1. 本门禁只校验**本批 638 交付物**，不替历史批次背锅；",
        "2. 门禁的 `--check` 只读（exit 0 不写盘），`--report` 才落盘；",
        "3. **测试套件数据隔离**：根级 `conftest.py`（634 A1）在 pytest 会话结束时"
        "**删除会话期间**在 `data/` 新建的文件（**已存在的文件不受影响**——本批实证："
        "把文件放回后跑 `pytest tests/test_run_638_gate.py`，15 个 638 文件全部存活）；",
        "   因此本批丢失**已存在**的 `data/638_*.md/json` **不能**由 conftest 解释，"
        "已按「环境/工具层不稳定」登记（见 §五），此后一律**先跑测试、后生成报告、"
        "生成后立即核验文件大小、再提交**；",
        "4. mypy 断言用「`Success: no issues found` + exit 0」双条件，避免只看 exit；",
        "5. 四态/FSM 是**新数据用新格式**，历史判决与报告**未改**（§零.1 向后兼容）；",
        "6. known_error_rate / RR / 调参均为**先有再说**（§四.1~4），不是最终形态。", "",
        "## 五、本批偏差与事故（如实登记）", "",
        "| 项 | 事实 | 影响 |", "|---|---|---|",
        "| 637 闭环产物缺失 | 开工时 `637_evolution_memo.md` 等不存在（637 未落盘），"
        "本批**重跑**得到「第一次产出」 | 复盘基于重跑产物，非 637 原物 |",
        "| `637_observer.json` 被污染 | 本批中途该文件被其它进程/测试改写为"
        "（`pytest_failures=82`、`tools_total=428`） | C2/C1 改用**实时采集**，"
        "并已 `git checkout` 还原该文件 |",
        "| `data/638_*` 文件两度凭空丢失 | 先后丢失 `638_baseline.md` / "
        "`638_four_state_schema.{md,json}` / `638_lifecycle_fsm.{md,json}` / "
        "`638_rr_conflict_analysis.{md,json}`（7 个，含**已提交**文件）。"
        "**机制未查明**：已排除根 conftest（实证已存在文件不受影响）；另观察到 "
        "`write_to_file` 写 `data/638_baseline.md` 曾产生 **0 字节**文件 | "
        "全部已用 `git checkout` / 重新生成复原；登记为本环境**工具层不稳定**风险，"
        "收工前已逐个核验文件大小 |",
        "| §一 表两处过期 | 工具数（表 417 / 实测 429）、四态 fail（表 25 / 实测 26） | "
        "以实测为准 |",
    ]
    with open(ACCEPTANCE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    return {"json": RESULT_JSON, "md": ACCEPTANCE}


# ── 自检 ────────────────────────────────────────────────────────────────
def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("7 个新工具", len(NEW_TOOLS) == 7)
    chk("8 个任务", len(TASK_DELIVERABLES) == 8)
    chk("任务编号齐全",
        [d["task"] for d in TASK_DELIVERABLES] == ["0", "3.1", "3.2", "B1", "B2", "C1", "C2", "E1"])
    chk("工具清单含 gate 自身", "run_638_gate" in NEW_TOOLS)
    for t in NEW_TOOLS:
        chk(f"工具存在 {t}", os.path.exists(os.path.join(ROOT, "tools", f"{t}.py")))
    chk("交付清单含 E1 报告",
        any(f.endswith("638_acceptance_report.md")
            for d in TASK_DELIVERABLES for f in d["files"]))
    chk("受控目录定义", CONTROLLED == ["atoms", "evidence", "Examples", "Book"])
    chk("报告路径在 data 下",
        ACCEPTANCE.startswith(os.path.join(ROOT, "data"))
        and RESULT_JSON.startswith(os.path.join(ROOT, "data")))
    chk("受控目录干净（实测）", check_controlled()["ok"])
    return 0 if ok else 1


def main(argv: Optional[list[str]] = None) -> int:
    ap = argparse.ArgumentParser(description="638 E1 收工门禁")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--report", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args(argv)
    if args.check:
        return selftest()
    if args.report:
        out = write_report()
        print(f"written {out['json']} {out['md']}")
        return 0
    g = build()
    if args.json:
        print(json.dumps({k: v for k, v in g.items() if k != "deliverables"},
                         ensure_ascii=False, indent=2))
        return 0
    print(f"overall={g['overall']} tools={sum(1 for t in g['tools'] if t['ok'])}/"
          f"{len(g['tools'])} ruff={g['ruff']['ok']} mypy={g['mypy']['ok']} "
          f"ctrl={g['controlled']['ok']} dels={g['deliverables']['ok']} "
          f"tests={g['tests']['ok']}")
    return 0 if g["overall"] else 1


if __name__ == "__main__":
    sys.exit(main())
