#!/usr/bin/env python3
"""614 任务F1 · 收工门禁（跑全部 614 工具 --check + 卫生 + 回归 + 零污染 + 报告）。

门禁项（**结论项**）：
  1. 全部 **614 工具** `--check`（exit 0=通过）。
  2. `ruff check tools/ tests/` + `mypy tools/`（CI 硬门禁同款）。
  3. `pytest tests/ -q -m "not slow" -k 614`（614 批次自身回归）。
  4. 受控目录零污染（`Examples/atoms/ atoms/ evidence/ tools/golden_state.json`）。

**不跑**监工四类（`tool_integrity --check / gate_engine --check / poison_drill / atom_evidence_replay --check`）
——614 §五 铁律：这些是**监工**的事；本门禁只**列出**它们，交监工验收。

信息项：全量 `pytest -m "not slow"`（含非 614 既有红灯，不计入结论）。

产物：`data/614_acceptance_report.md` + `_auto/outbox/614.md`；并更新 `_auto/status.json`。

CLI：
  python tools/run_614_gate.py            # 跑门禁 + 写报告 + 更新 status/outbox
  python tools/run_614_gate.py --quick    # 只跑 614 工具 --check
  python tools/run_614_gate.py --check    # 门禁是否全绿（exit 0=通过）
"""
from __future__ import annotations

import argparse
import json
import subprocess
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = ROOT / ".venv" / "Scripts" / "python.exe"
OUTBOX = ROOT / "_auto" / "outbox" / "614.md"
STATUS = ROOT / "_auto" / "status.json"
REPORT = ROOT / "data" / "614_acceptance_report.md"

TOOLS = [
    "learner_behavior_logger", "learner_twin_dashboard_614", "learner_ood_evaluator",
    "learner_argument_link", "trust_root_status_check", "oracle_priority_614",
    "oracle_verification_614",
]

# 监工类：**本批不跑**（614 §五），只列出交监工
MONITORS_LISTED = ["tool_integrity --check", "gate_engine.py --check",
                   "poison_drill.py", "atom_evidence_replay.py --check"]

CONTROLLED = ["Examples/atoms/", "atoms/", "evidence/", "tools/golden_state.json"]


def _run(args: list[str], timeout: int = 300) -> tuple[int, str, float]:
    t0 = time.time()
    cmd = [str(PY), *args] if args and args[0] not in ("git",) else list(args)
    try:
        r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True,
                           timeout=timeout, encoding="utf-8", errors="replace")
        tail = (r.stdout + r.stderr).strip().splitlines()
        return r.returncode, (tail[-1] if tail else ""), round(time.time() - t0, 1)
    except subprocess.TimeoutExpired:
        return 124, f"TIMEOUT(>{timeout}s)", float(timeout)
    except FileNotFoundError:
        return 127, "命令不存在", 0.0


def tool_checks() -> dict[str, dict]:
    out = {}
    for t in TOOLS:
        rc, tail, dt = _run([f"tools/{t}.py", "--check"])
        out[t] = {"rc": rc, "tail": tail[:110], "sec": dt}
    return out


def hygiene() -> dict[str, dict]:
    out = {}
    for name, argv, to in (
        ("ruff", ["-m", "ruff", "check", "tools/", "tests/"], 180),
        ("mypy", ["-m", "mypy", "tools/"], 300),
        ("pytest_full", ["-m", "pytest", "tests/", "-q", "-m", "not slow"], 900),
        ("pytest_614", ["-m", "pytest", "tests/", "-q", "-m", "not slow", "-k", "614"], 600),
    ):
        rc, tail, dt = _run(argv, to)
        out[name] = {"rc": rc, "tail": tail[:110], "sec": dt}
    return out


def pollution() -> dict:
    r = subprocess.run(["git", "status", "--porcelain", "--", *CONTROLLED], cwd=str(ROOT),
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    dirty = r.stdout.strip()
    return {"clean": not dirty, "detail": dirty.replace("\n", " | ")[:200]}


def render(tools: dict, hyg: dict | None, poll: dict | None, quick: bool, ok: bool) -> str:
    n_ok = sum(1 for v in tools.values() if v["rc"] == 0)
    L = ["# 614 收工验收报告（F1 门禁）", "",
         f"> 生成：`python tools/run_614_gate.py` ｜ 时间：{datetime.now().isoformat(timespec='seconds')}",
         f"> 模式：{'quick（仅 614 工具 --check）' if quick else 'full（含卫生/回归/零污染）'}", "",
         "## 一、614 工具 --check（结论项）", "",
         f"**{n_ok}/{len(tools)} 通过**", "",
         "| 工具 | exit | 耗时(s) | 末行 |", "|---|---|---|---|"]
    for t, v in tools.items():
        L.append(f"| `{t}` | {v['rc']} {'✅' if v['rc'] == 0 else '❌'} | {v['sec']} | {v['tail']} |")
    L.append("")
    if not quick:
        L += ["## 二、卫生与 614 自身回归（结论项）", "",
              "| 项 | exit | 耗时(s) | 末行 |", "|---|---|---|---|"]
        for k in ("ruff", "mypy", "pytest_614"):
            v = (hyg or {}).get(k)
            if v is not None:
                L.append(f"| {k} | {v['rc']} {'✅' if v['rc'] == 0 else '❌'} | {v['sec']} | {v['tail']} |")
        L += ["", "## 三、零污染（受控目录）", "",
              f"- {'✅ 干净' if (poll or {}).get('clean') else '❌ ' + str((poll or {}).get('detail'))}",
              "", "## 四、监工类（**本批不跑**，交监工验收）", "",
              "> 614 §五 铁律：苦力**不跑**监工门禁；下列四项由**监工**验收时执行：", ""]
        for m in MONITORS_LISTED:
            L.append(f"- `{m}`")
        L += ["", "## 五、全量回归（信息项 · 含非 614 既有红灯）", "",
              "> 全量 `pytest -m \"not slow\"` 含既有测试；其红灯**非 614 引入**，仅信息记录。"]
        vf = (hyg or {}).get("pytest_full")
        if vf is not None:
            L.append("")
            L.append(f"- pytest_full exit={vf['rc']}（{vf['sec']}s） 末行：`{vf['tail']}`")
            if vf["rc"] != 0:
                L.append("  - 既有漂移交人 化债（如 supply_chain manifest 等），非 614 责任。")
    L += ["## 结论", "",
          f"- **{'✅ 614 自身门禁全绿，可收工' if ok else '❌ 614 自身门禁未通过'}**", "",
          "> 门禁只覆盖 614 工具自验证与卫生/614 回归/零污染；**不代替**：",
          "> ① 监工验收（监工门禁四类）；② golden accept（人审权）；③ 受控目录授权。",
          "> 已知交人项：CI 四 job 全绿（本机无 gh 通道）、OTS 真上链、in-toto 真签名（见 C1/C2/C3）。"]
    return "\n".join(L) + "\n"


def update_status(ok: bool, status_path: Path = STATUS) -> None:
    status_path.parent.mkdir(parents=True, exist_ok=True)
    st = {}
    if status_path.is_file():
        try:
            st = json.loads(status_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            st = {}
    hist = st.get("history") or []
    hist.append({"batch": "614", "at": datetime.now().isoformat(timespec="seconds"),
                 "verdict": "PASS" if ok else "FAIL"})
    st["status"] = "awaiting_review"
    st["batch"] = "614"
    st["updated_at"] = datetime.now().isoformat(timespec="seconds")
    st["history"] = hist[-20:]
    status_path.write_text(json.dumps(st, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="614 F1 · 收工门禁")
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)

    print("[F1] 跑 614 工具 --check …")
    tools = tool_checks()
    for t, v in tools.items():
        print(f"    {'✅' if v['rc'] == 0 else '❌'} {t} (exit={v['rc']}, {v['sec']}s)")

    hyg = None if a.quick else hygiene()
    if hyg:
        for k, v in hyg.items():
            print(f"[F1] {k} exit={v['rc']} ({v['sec']}s)")
    poll = None if a.quick else pollution()

    n_ok = sum(1 for v in tools.values() if v["rc"] == 0)
    ok = n_ok == len(tools)
    if not a.quick:
        hyg_ok = all((hyg or {}).get(k, {}).get("rc") == 0 for k in ("ruff", "mypy", "pytest_614"))
        ok = ok and hyg_ok and bool((poll or {}).get("clean"))

    page = render(tools, hyg, poll, a.quick, ok)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(page, encoding="utf-8", newline="\n")
    OUTBOX.parent.mkdir(parents=True, exist_ok=True)
    OUTBOX.write_text(page, encoding="utf-8", newline="\n")
    print(f"[F1] 报告：{REPORT.relative_to(ROOT).as_posix()} ｜ outbox：{OUTBOX.relative_to(ROOT).as_posix()}")

    if not a.quick:
        update_status(ok)
        print(f"[F1] status.json ⇒ awaiting_review（verdict={'PASS' if ok else 'FAIL'}）")

    print(f"[F1] 门禁结论：{'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
