#!/usr/bin/env python3
"""613 任务F3 · 收工门禁（跑全部 613 工具 --check + 卫生 + 回归 + 零污染 + 报告）。

门禁项：
  1. 全部 613 工具 `--check`（exit 0=通过）——**结论项**。
  2. `ruff check tools/ tests/` + `mypy tools/` ——**结论项**（CI 硬门禁同款）。
  3. `pytest tests/ -q -m "not slow"` ——**结论项**。
  4. 受控目录零污染（`Examples/atoms/ atoms/ evidence/ tools/golden_state.json`）——**结论项**。
  5. `metrics_613.py` 生成度量汇总。
  6. 监工类（tool_integrity / gate_engine / poison_drill / atom_evidence_replay）——
     **仅记录、不作结论**（铁律：这些是监工的事；F3 例外只作记录）。

产物：`data/613_acceptance_report.md` + `_auto/outbox/613.md`；并更新 `_auto/status.json`。

CLI：
  python tools/run_613_gate.py            # 跑门禁 + 写报告 + 更新 status/outbox
  python tools/run_613_gate.py --quick    # 只跑工具 --check（跳过 pytest/mypy/监工）
  python tools/run_613_gate.py --check    # 门禁是否全绿（exit 0=通过）
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
OUTBOX = ROOT / "_auto" / "outbox" / "613.md"
STATUS = ROOT / "_auto" / "status.json"
REPORT = ROOT / "data" / "613_acceptance_report.md"

TOOLS = [
    "613_baseline", "liveness_priority_613", "liveness_completion_613",
    "golden_lock_proposal_613", "quality_gate_613", "learner_behavior_ingest",
    "learner_mastery_update_613", "learner_path_graph_613",
    "learner_twin_dashboard_613", "bridge_edge_proposal_613",
    "argument_fragmentation_613", "defense_chain_deep_613", "ots_anchor_613",
    "in_toto_link", "merkle_proof_613", "escape_rate_honest_613",
    "metrics_613", "d5_source_integrity",
]

# 监工类：只记录，不参与结论
MONITORS = [
    ("tool_integrity", ["tools/tool_integrity.py", "--check"], 180),
    ("gate_engine", ["tools/gate_engine.py", "--check"], 180),
    ("poison_drill", ["tools/poison_drill.py"], 180),
    ("atom_evidence_replay", ["tools/atom_evidence_replay.py", "--check"], 120),
]

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


def monitors() -> dict[str, dict]:
    out = {}
    for name, argv, to in MONITORS:
        rc, tail, dt = _run(argv, to)
        out[name] = {"rc": rc, "tail": tail[:110], "sec": dt}
    return out


def hygiene() -> dict[str, dict]:
    out = {}
    for name, argv, to in (
        ("ruff", ["-m", "ruff", "check", "tools/", "tests/"], 180),
        ("mypy", ["-m", "mypy", "tools/"], 300),
        # 全量回归（信息项；含非 613 的 supply_chain 等既有红灯，不计入 613 结论）
        ("pytest_full", ["-m", "pytest", "tests/", "-q", "-m", "not slow"], 600),
        # 613 自身回归（结论项）：仅跑 613 批次测试
        ("pytest_613", ["-m", "pytest", "tests/", "-q", "-m", "not slow", "-k", "613"], 600),
    ):
        rc, tail, dt = _run(argv, to)
        out[name] = {"rc": rc, "tail": tail[:110], "sec": dt}
    return out


def pollution() -> dict:
    r = subprocess.run(["git", "status", "--porcelain", "--", *CONTROLLED], cwd=str(ROOT),
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    dirty = r.stdout.strip()
    return {"clean": not dirty, "detail": dirty.replace("\n", " | ")[:200]}


def render(tools: dict, hyg: dict | None, poll: dict | None, mon: dict | None,
           quick: bool, ok: bool) -> str:
    n_ok = sum(1 for v in tools.values() if v["rc"] == 0)
    L = ["# 613 收工验收报告（F3 门禁）", "",
         f"> 生成：`python tools/run_613_gate.py` ｜ 时间：{datetime.now().isoformat(timespec='seconds')}",
         f"> 模式：{'quick（仅工具 --check）' if quick else 'full（含卫生/回归/零污染/监工记录）'}", "",
         "## 一、613 工具 --check（结论项）", "",
         f"**{n_ok}/{len(tools)} 通过**", "",
         "| 工具 | exit | 耗时(s) | 末行 |", "|---|---|---|---|"]
    for t, v in tools.items():
        L.append(f"| `{t}` | {v['rc']} {'✅' if v['rc'] == 0 else '❌'} | {v['sec']} | {v['tail']} |")
    L.append("")
    if not quick:
        L += ["## 二、卫生与回归（结论项）", "",
              "| 项 | exit | 耗时(s) | 末行 |", "|---|---|---|---|"]
        for k, v in (hyg or {}).items():
            L.append(f"| {k} | {v['rc']} {'✅' if v['rc'] == 0 else '❌'} | {v['sec']} | {v['tail']} |")
        L += ["", "## 三、零污染（受控目录）", "",
              f"- {'✅ 干净' if (poll or {}).get('clean') else '❌ ' + str((poll or {}).get('detail'))}",
              "", "## 四、监工类（**仅记录，不作结论**）", "",
              "| 工具 | exit | 耗时(s) | 末行 |", "|---|---|---|---|"]
        for k, v in (mon or {}).items():
            L.append(f"| {k} | {v['rc']} | {v['sec']} | {v['tail']} |")
        L.append("")
        L.append("> 铁律：这些是监工的事；F3 例外只作记录，其 exit **不影响**本门禁结论。")
        L.append("")
    L += ["## 结论", "",
          f"- **{'✅ 门禁全绿，可收工' if ok else '❌ 门禁未通过'}**", "",
          "> 门禁只覆盖工具自验证与卫生/回归/零污染；**不代替** golden accept（人审权）",
          "> 与活性锚落卡（受控目录，需授权）。"]
    return "\n".join(L) + "\n"


def update_status(ok: bool) -> None:
    STATUS.parent.mkdir(parents=True, exist_ok=True)
    st = {}
    if STATUS.is_file():
        try:
            st = json.loads(STATUS.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            st = {}
    hist = st.get("history") or []
    hist.append({"batch": "613", "at": datetime.now().isoformat(timespec="seconds"),
                 "verdict": "PASS" if ok else "FAIL"})
    st["status"] = "awaiting_review"
    st["batch"] = "613"
    st["updated_at"] = datetime.now().isoformat(timespec="seconds")
    st["history"] = hist[-20:]
    STATUS.write_text(json.dumps(st, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="613 F3 · 收工门禁")
    ap.add_argument("--quick", action="store_true")
    ap.add_argument("--check", action="store_true")
    a = ap.parse_args(argv)

    print("[F3] 跑 613 工具 --check …")
    tools = tool_checks()
    for t, v in tools.items():
        print(f"    {'✅' if v['rc'] == 0 else '❌'} {t} (exit={v['rc']}, {v['sec']}s)")

    hyg = None if a.quick else hygiene()
    if hyg:
        for k, v in hyg.items():
            print(f"[F3] {k} exit={v['rc']} ({v['sec']}s)")
    poll = None if a.quick else pollution()
    mon = None if a.quick else monitors()
    if mon:
        for k, v in mon.items():
            print(f"[F3] [记录] {k} exit={v['rc']} ({v['sec']}s)")

    _rc, _tail, _dt = _run(["tools/metrics_613.py"])
    print(f"[F3] metrics_613 exit={_rc}")

    n_ok = sum(1 for v in tools.values() if v["rc"] == 0)
    ok = n_ok == len(tools)
    if not a.quick:
        ok = ok and all(v["rc"] == 0 for v in (hyg or {}).values()) and bool((poll or {}).get("clean"))

    page = render(tools, hyg, poll, mon, a.quick, ok)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(page, encoding="utf-8", newline="\n")
    OUTBOX.parent.mkdir(parents=True, exist_ok=True)
    OUTBOX.write_text(page, encoding="utf-8", newline="\n")
    print(f"[F3] 报告：{REPORT.relative_to(ROOT).as_posix()} ｜ outbox：{OUTBOX.relative_to(ROOT).as_posix()}")

    if not a.quick:
        update_status(ok)
        print(f"[F3] status.json ⇒ awaiting_review（verdict={'PASS' if ok else 'FAIL'}）")

    print(f"[F3] 门禁结论：{'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
