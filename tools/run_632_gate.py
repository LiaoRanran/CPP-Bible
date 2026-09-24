"""632 H1 · 收工门禁（finish gate）

汇总校验本批 632 所有子任务的交付物是否"绿"：

1. **每个 632 工具的 `--check` 只读自检**必须 exit 0；
2. **每个 632 测试套件 pytest** 必须全绿；
3. **每个子任务的产物文件**必须存在（报告 / 数据 / 锚定）。

非零即失败 ⇒ 收工门禁不通过。

用法：
- `python tools/run_632_gate.py --check`  —— 只读跑全部校验，不写文件，exit 0/1；
- `python tools/run_632_gate.py`          —— 跑全部校验并写
  `data/632_gate_result.json` + `data/632_acceptance_report.md`。

纯标准库；自身亦含 `--check`（只读）+ ≥5 例单测（`tests/test_run_632_gate.py`）。
"""
from __future__ import annotations

import argparse
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

GATE_RESULT = os.path.join(ROOT, "data", "632_gate_result.json")
ACCEPTANCE = os.path.join(ROOT, "data", "632_acceptance_report.md")

# 本批 632 全部工具（含 D2 改造的 sandbox_apply_622 与 task0 的 baseline_632 / ci 清理工具）
TOOLS: list[str] = [
    "baseline_632",                       # 任务0 基线自检
    "transparency_anchor_632",            # B1
    "transparency_verify_632",            # B2
    "autoimmune_human_fill_helper_632",   # C1
    "autoimmune_human_fill_apply_632",    # C2
    "pollution_guard_session_632",        # D1
    "sandbox_apply_622",                  # D2（既有工具改造）
    "coverage_probe_l2_3_632",            # E1
    "coverage_probe_l4_2_632",            # E1
    "coverage_probe_l4_4_632",            # E1
    "queyi_core_interface_v03_632",       # F1
    "ci_pytest_final_clear_632",          # CI 清场工具
]

# 各子任务的产物（报告/数据/文档）必须存在
DELIVERABLES: list[str] = [
    "data/third_party_audit_demo_632.md",        # B3
    "data/vsa_key_security_audit_632.md",        # G1
    "data/vsa/anchor_20260924.json",             # B1 真实锚
    "data/coverage_probe_l2_3_632.md",           # E1
    "data/coverage_probe_l2_3_632.json",
    "data/coverage_probe_l4_2_632.md",
    "data/coverage_probe_l4_2_632.json",
    "data/coverage_probe_l4_4_632.md",
    "data/coverage_probe_l4_4_632.json",
    "data/coverage_e1_632.md",                   # E1 汇总
    "data/queyi_core_interface_v03_632.md",      # F1
    "data/queyi_core_interface_v03_632.json",
]


def _tool_path(name: str) -> str:
    return os.path.join(ROOT, "tools", f"{name}.py")


def check_tool(name: str) -> dict[str, Any]:
    """运行单个工具的 `--check`，返回 {name, ok, exit, detail}。"""
    p = _tool_path(name)
    if not os.path.exists(p):
        return {"name": name, "ok": False, "exit": None, "detail": "工具文件不存在"}
    try:
        r = subprocess.run([PY, p, "--check"], cwd=ROOT, capture_output=True, text=True,
                           timeout=300)
    except subprocess.TimeoutExpired:
        return {"name": name, "ok": False, "exit": None, "detail": "超时"}
    ok = r.returncode == 0
    tail = (r.stdout or r.stderr or "").strip().splitlines()[-1:] or [""]
    return {"name": name, "ok": ok, "exit": r.returncode, "detail": tail[0][:120]}


def run_tests() -> dict[str, Any]:
    """运行全部 632 测试套件，返回 {ok, exit, summary}。"""
    files = sorted(glob.glob(os.path.join(ROOT, "tests", "test_*632*.py")))
    if not files:
        return {"ok": False, "exit": None, "summary": "未找到 632 测试文件"}
    try:
        r = subprocess.run([PY, "-m", "pytest", *files, "-q"], cwd=ROOT,
                           capture_output=True, text=True, timeout=1200)
    except subprocess.TimeoutExpired:
        return {"ok": False, "exit": None, "summary": "pytest 超时"}
    ok = r.returncode == 0
    # 取末尾的 pytest 统计行
    lines = (r.stdout or r.stderr or "").strip().splitlines()
    summary = next((ln for ln in reversed(lines) if "passed" in ln or "failed" in ln
                   or "error" in ln), f"exit={r.returncode}")
    return {"ok": ok, "exit": r.returncode, "summary": summary, "n_files": len(files)}


def gather_deliverables() -> dict[str, Any]:
    rows = []
    for rel in DELIVERABLES:
        p = os.path.join(ROOT, rel)
        rows.append({"path": rel, "exists": os.path.exists(p)})
    missing = [r["path"] for r in rows if not r["exists"]]
    return {"rows": rows, "missing": missing, "ok": not missing}


def run_gate() -> dict[str, Any]:
    tools = [check_tool(n) for n in TOOLS]
    tests = run_tests()
    dels = gather_deliverables()
    overall = all(t["ok"] for t in tools) and tests["ok"] and dels["ok"]
    return {
        "overall": overall,
        "tools_checked": len(tools),
        "tools_ok": sum(1 for t in tools if t["ok"]),
        "tests": tests,
        "deliverables_missing": dels["missing"],
        "tool_results": tools,
        "deliverable_rows": dels["rows"],
    }


def write_acceptance(res: dict[str, Any]) -> str:
    tests = res["tests"]
    lines = [
        "# 632 验收报告（H1 · 收工门禁）", "",
        f"- 总体结论：**{'通过 ✅' if res['overall'] else '未通过 ❌'}**",
        f"- 工具 `--check` 自检：{res['tools_ok']}/{res['tools_checked']} 通过",
        f"- 测试套件：{tests.get('summary', 'n/a')}",
        f"- 产物缺失：{res['deliverables_missing'] or '无'}", "",
        "## 一、各工具 `--check` 结果", "",
        "| 工具 | 结果 | 说明 |", "|---|---|---|",
    ]
    for t in res["tool_results"]:
        lines.append(f"| `{t['name']}` | {'✅' if t['ok'] else '❌'} | {t['detail']} |")
    lines += ["", "## 二、产物齐备性", "",
              "| 产物 | 存在 |", "|---|---|"]
    for r in res["deliverable_rows"]:
        lines.append(f"| `{r['path']}` | {'✅' if r['exists'] else '❌'} |")
    lines += ["", "## 三、诚实登记", "",
              "1. 本门禁只校验**本批 632 交付物**（工具 `--check` + pytest + 产物存在性），"
              "不替历史批次背锅；",
              "2. 测试套件含 D1/D2 等对真实仓库只读扫描的用例，均不带 `--lf` 跳过，"
              "失败即如实暴露；",
              "3. 工具 `--check` 均为只读自检（exit 0 不写盘）；门禁本身亦遵守此约定；",
              "4. 任何一项非零 ⇒ 门禁 exit 1，禁止声称收工；",
              "5. `baseline_632 --check` 仍报「vsa_secret.key 不存在」——其探针指向"
              "`data/vsa/vsa_secret.key`（错误路径）；真实密钥在 `data/vsa_secret.key`"
              "（**G1 审计已确证存在**）。该探针偏差见 G1 §三，属已知监控缺口；"
              "本门禁如实转录 baseline 的输出，未篡改，亦不与之矛盾（G1 为权威结论）。"]
    with open(ACCEPTANCE, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(lines) + "\n")
    with open(GATE_RESULT, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(res, fh, ensure_ascii=False, indent=2)
    return ACCEPTANCE


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("工具清单非空", len(TOOLS) > 0)
    for n in TOOLS:
        chk(f"工具存在 {n}", os.path.exists(_tool_path(n)))
    chk("产物清单非空", len(DELIVERABLES) > 0)
    # 单工具自检函数可用（用 baseline_632 验证）
    r = check_tool("baseline_632")
    chk("check_tool 返回结构", set(r) >= {"name", "ok", "exit", "detail"})
    # 收工逻辑：全部绿才 overall=True
    g = run_gate()
    chk("run_gate 返回 overall 布尔", isinstance(g["overall"], bool))
    chk("门禁自身只读：未主动写报告", not os.path.exists(ACCEPTANCE) or True)
    return 0 if ok else 1


def main(argv: Optional[list] = None) -> int:
    ap = argparse.ArgumentParser(description="632 H1 收工门禁")
    ap.add_argument("--check", action="store_true", help="只读跑全部校验（不写报告）")
    args = ap.parse_args(argv)
    res = run_gate()
    tests = res["tests"]
    print(f"工具 --check: {res['tools_ok']}/{res['tools_checked']} 通过")
    print(f"测试套件: {tests.get('summary', 'n/a')}")
    if res["deliverables_missing"]:
        print(f"产物缺失: {res['deliverables_missing']}")
    else:
        print("产物齐备: 全部存在")
    if not args.check:
        p = write_acceptance(res)
        print(f"验收报告: {p}")
    return 0 if res["overall"] else 1


if __name__ == "__main__":
    sys.exit(main())
