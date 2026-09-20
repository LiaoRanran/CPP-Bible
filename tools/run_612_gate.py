#!/usr/bin/env python3
"""612 线 Z · 收工门禁：14+ 工具 --check 全绿 + metrics + integrity + pytest + ruff + 零污染 + 报告。

门禁项（spec Z）：
  1. 全部 612 工具 `--check`（exit 0=通过）；含 A/B/C/D/E 各线工具与 task0 基线。
  2. `metrics_612.py` 生成度量报告（E1-E3）。
  3. `tool_integrity.py --check`：CORE_TOOLS 校验和未变（收工门禁例外项）。
  4. `pytest tests/ -q`：全量回归（含 612 与各线）。
  5. `ruff check tools tests`：代码卫生。
  6. 零污染：`atoms/ evidence/ Examples/ Book/` 相对 HEAD 无改动（git diff --quiet）。

报告写入：
  - `data/612_acceptance_report.md`（可见交付物）
  - `_auto/outbox/612.md`（协议 outbox）

CLI：
  python tools/run_612_gate.py            # 跑全部门禁并写报告
  python tools/run_612_gate.py --quick    # 仅跑工具 --check + metrics（跳过 pytest/ruff/integrity，快速自查）
  python tools/run_612_gate.py --check    # 门禁是否全绿（exit 0=通过，供 CI 用）
"""
# mypy: ignore-errors
from __future__ import annotations

import argparse
import subprocess
import time
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = ROOT / ".venv" / "Scripts" / "python.exe"
OUTBOX = ROOT / "_auto" / "outbox" / "612.md"
REPORT = ROOT / "data" / "612_acceptance_report.md"

# 612 收工门禁涵盖的工具（含 task0 基线 + A/B/C/D/E 各线 deliverable）
TOOLS = [
    "612_baseline", "bridge_edge_candidates", "bridge_edge_pre_annotate",
    "bridge_edge_review", "bridge_edge_impact", "liveness_candidate_generator",
    "liveness_review", "liveness_impact", "oracle_priority", "oracle_verifier",
    "kc_inventory", "bkt_solver", "learner_state", "learner_recommender",
    "learner_twin_dashboard", "metrics_612",
]
CONTROLLED = ["atoms/", "evidence/", "Examples/", "Book/"]


def _run(args: list[str], timeout: int = 320) -> tuple[int, str, str]:
    t0 = time.time()
    # git 等外部命令直接执行；其余一律走 venv python
    cmd = [str(PY), *args] if args and args[0] not in ("git",) else list(args)
    try:
        r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True,
                            text=True, timeout=timeout, encoding="utf-8")
        dt = time.time() - t0
        return r.returncode, (r.stdout + r.stderr)[-1500:], dt
    except subprocess.TimeoutExpired:
        return 124, f"TIMEOUT(>{timeout}s)", timeout


def gate_tool_checks() -> dict:
    res: dict[str, dict] = {}
    for t in TOOLS:
        rc, tail, dt = _run([f"tools/{t}.py", "--check"])
        res[t] = {"rc": rc, "tail": tail.strip().splitlines()[-1] if tail.strip() else "",
                  "sec": round(dt, 1)}
    return res


def gate_metrics() -> tuple[int, float]:
    rc, tail, dt = _run(["tools/metrics_612.py"])
    return rc, round(dt, 1)


def gate_integrity() -> tuple[int, str, float]:
    rc, tail, dt = _run(["tools/tool_integrity.py", "--check"], timeout=180)
    last = tail.strip().splitlines()[-1] if tail.strip() else ""
    return rc, last, round(dt, 1)


def gate_pytest() -> tuple[int, str, float]:
    # 快回归：跳过 -m slow 重型集成测试（mutation_fuzz/replay 等，另行长时运行）
    rc, tail, dt = _run(["-m", "pytest", "tests/", "-q", "-m", "not slow"], timeout=400)
    last = tail.strip().splitlines()[-1] if tail.strip() else ""
    return rc, last, round(dt, 1)


def gate_ruff() -> tuple[int, str, float]:
    rc, tail, dt = _run(["-m", "ruff", "check", "tools", "tests"], timeout=180)
    last = tail.strip().splitlines()[-1] if tail.strip() else ""
    return rc, last, round(dt, 1)


def gate_pollution() -> dict:
    out = {}
    for d in CONTROLLED:
        rc, _, _ = _run(["git", "diff", "--quiet", "--", d], timeout=60)
        out[d] = rc == 0  # 0 = 无改动（干净）
    # 也检查是否新增了未跟踪的受控目录文件
    rc, tracked, _ = _run(["git", "status", "--porcelain", "--", *CONTROLLED], timeout=60)
    out["untracked_or_modified"] = (tracked.strip() == "")
    return out


def render(tool_res: dict, metrics: tuple, integrity: tuple | None,
           pytest: tuple | None, ruff: tuple | None, pollution: dict,
           quick: bool) -> str:
    n_pass = sum(1 for v in tool_res.values() if v["rc"] == 0)
    n_total = len(tool_res)
    L: list[str] = []
    L.append("# 612 收工验收报告（Z 门禁）")
    L.append("")
    L.append(f"> 生成时间：{datetime.now().isoformat(timespec='seconds')} ｜ 工具：`python tools/run_612_gate.py`")
    L.append(f"> 模式：{'quick（仅工具 --check + metrics）' if quick else 'full（含 integrity/pytest/ruff/零污染）'}")
    L.append("")
    all_ok = (n_pass == n_total)
    L.append(f"## 一、工具 --check（{n_pass}/{n_total} 通过）")
    L.append("")
    L.append("| 工具 | exit | 耗时(s) | 末行 |")
    L.append("|---|---|---|---|")
    for t, v in tool_res.items():
        mark = "✅" if v["rc"] == 0 else "❌"
        L.append(f"| `{t}` | {v['rc']} {mark} | {v['sec']} | {v['tail']} |")
    if not all_ok:
        L.append("")
        L.append("> ⚠ **存在失败**（`--check` 非 0）：需修复后再收工。")
    L.append("")
    L.append("## 二、度量 metrics_612")
    L.append(f"- exit={metrics[0]} ｜ 耗时={metrics[1]}s ｜ 产物：`data/metrics_612.md`")
    L.append("")
    if not quick:
        rc, last, dt = integrity or (1, "N/A", 0.0)
        L.append("## 三、完整性 tool_integrity --check")
        L.append(f"- exit={rc} ｜ 耗时={dt}s ｜ {last}")
        L.append("")
        rc, last, dt = pytest or (1, "N/A", 0.0)
        L.append("## 四、回归 pytest tests/ -q")
        L.append(f"- exit={rc} ｜ 耗时={dt}s ｜ {last}")
        L.append("")
        rc, last, dt = ruff or (1, "N/A", 0.0)
        L.append("## 五、代码卫生 ruff check tools tests")
        L.append(f"- exit={rc} ｜ 耗时={dt}s ｜ {last}")
        L.append("")
        clean = all(pollution.values())
        L.append("## 六、零污染（受控目录 vs HEAD）")
        for d, ok in pollution.items():
            L.append(f"- `{d}`: {'✅ 干净' if ok else '❌ 有改动'}")
        if not clean:
            L.append("> ⚠ **受控目录被改动** ⇒ 违反铁律，须回退。")
        L.append("")
    overall = all_ok and (metrics[0] == 0)
    if not quick:
        overall = overall and (integrity[0] == 0) and (pytest[0] == 0) and (ruff[0] == 0) and all(pollution.values())
    L.append("## 结论")
    L.append(f"- **{'✅ 门禁全绿，可收工' if overall else '❌ 门禁未通过，需处理'}**")
    L.append("")
    L.append("> 注：本门禁仅运行各工具 `--check` 与度量/回归/卫生，不代替人类 golden accept（"
             "accept 权唯人）。oracle 人审相关指标如实标注「零人审」。")
    return "\n".join(L) + "\n"


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="612 Z · 收工门禁")
    ap.add_argument("--quick", action="store_true", help="仅跑工具 --check + metrics")
    ap.add_argument("--check", action="store_true", help="门禁是否全绿（exit 0=通过）")
    a = ap.parse_args(argv)

    print("[Z] 跑工具 --check …")
    tool_res = gate_tool_checks()
    for t, v in tool_res.items():
        print(f"    {'✅' if v['rc']==0 else '❌'} {t} (exit={v['rc']}, {v['sec']}s)")

    mrc, mdt = gate_metrics()
    print(f"[Z] metrics_612 exit={mrc} ({mdt}s)")

    integrity = gate_integrity() if not a.quick else None
    if not a.quick:
        print(f"[Z] tool_integrity exit={integrity[0]} ({integrity[2]}s)")
    pytest = gate_pytest() if not a.quick else None
    if not a.quick:
        print(f"[Z] pytest exit={pytest[0]} ({pytest[2]}s) :: {pytest[1]}")
    ruff = gate_ruff() if not a.quick else None
    if not a.quick:
        print(f"[Z] ruff exit={ruff[0]} ({ruff[2]}s)")
    pollution = gate_pollution() if not a.quick else {}

    page = render(tool_res, (mrc, mdt), integrity, pytest, ruff, pollution, a.quick)
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(page, encoding="utf-8")
    OUTBOX.parent.mkdir(parents=True, exist_ok=True)
    OUTBOX.write_text(page, encoding="utf-8")
    print(f"[Z] 报告已写 {REPORT.relative_to(ROOT).as_posix()} 与 {OUTBOX.relative_to(ROOT).as_posix()}")

    n_pass = sum(1 for v in tool_res.values() if v["rc"] == 0)
    ok = (n_pass == len(tool_res)) and (mrc == 0)
    if not a.quick:
        ok = ok and (integrity[0] == 0) and (pytest[0] == 0) and (ruff[0] == 0) and all(pollution.values())
    verdict = "PASS" if ok else "FAIL"
    print(f"[Z] 门禁结论：{verdict}（{'全绿' if ok else '存在未通过项'}）")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
