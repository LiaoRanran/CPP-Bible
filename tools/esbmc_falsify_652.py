#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""esbmc_falsify_652.py — H6 ESBMC falsification 试点（652 B，**可界算小探针 → witness**）。

为什么（652 B-H6）：真机实测只能给"这个编译器这个档位"的行为；对**有界**小探针，可用
有界模型检查（BMC）自动找反例（witness）。本工具对 H5 的可界算积木跑 ESBMC：

- **esbmc 可用** ⇒ 跑 `esbmc <file> --unwind N`，解析 VERIFICATION FAILED/SUCCESSFUL 与 witness；
- **esbmc 不可用**（本环境实测**未安装**）⇒ 状态 `tool_unavailable`，输出**拟执行命令**供人/CI 复核；
- 结果语义（诚实）：BMC **失败** ⇒ `fail(有 witness)` 是**硬结论**；
  BMC **成功**（无越界）**只入 `unknown(bounded)`**——有界通过 ≠ 全称成立。

用法
====
    python tools/esbmc_falsify_652.py --check
    python tools/esbmc_falsify_652.py --run        # → data/652_h6_falsify.json/md
"""
from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(HERE))

try:
    from utf8_console import ensure_utf8

    ensure_utf8()
except Exception:  # noqa: BLE001
    pass

QUEYI_PLUGIN = {"kind": "adapter", "name": "esbmc_falsify_652", "entry": "run_falsify",
                "description": "H6 ESBMC falsification 试点（不可用则降级 + 拟命令）"}

OUT_JSON = ROOT / "data" / "652_h6_falsify.json"
OUT_MD = ROOT / "data" / "652_h6_falsify.md"
UNWIND = 8


def esbmc_path() -> str | None:
    return shutil.which("esbmc")


def plan_command(probe_file: str) -> list[str]:
    """拟执行命令（esbmc 缺席时给人/CI 复核用）。"""
    return ["esbmc", probe_file, "--unwind", str(UNWIND), "--no-div-by-zero-check"]


def classify(stdout: str, rc: int) -> str:
    low = stdout.lower()
    if "verification failed" in low:
        return "fail(witness)"      # 硬结论：有反例
    if "verification successful" in low:
        return "unknown(bounded)"   # 诚实：有界通过 ≠ 全称
    return "error" if rc != 0 else "unknown(bounded)"


def falsify(probe_files: list[str]) -> dict:
    exe = esbmc_path()
    rows = []
    for pf in probe_files:
        row: dict = {"probe": pf, "esbmc": exe or None}
        if not exe:
            row.update(status="tool_unavailable",
                       plan_command=" ".join(plan_command(pf)),
                       note="ESBMC 未安装：本行未执行，命令留人/CI 复核（不伪造结论）")
            rows.append(row)
            continue
        try:
            r = subprocess.run(plan_command(pf), cwd=str(ROOT), capture_output=True,
                               text=True, timeout=300, check=False)
        except (OSError, subprocess.TimeoutExpired) as e:
            row.update(status="run_error", note=str(e)[:150])
            rows.append(row)
            continue
        row.update(status=classify(r.stdout, r.returncode), rc=r.returncode,
                   tail=(r.stdout or "")[-300:])
        rows.append(row)
    return {"esbmc_available": bool(exe), "unwind": UNWIND, "probes": probe_files,
            "rows": rows, "note": "BMC 失败=硬结论(witness)；BMC 成功仅 unknown(bounded)。"}


def _default_probes() -> list[str]:
    """可界算的小探针（H5 积木生成的单文件）。"""
    out = []
    for name in ("652_h5_probe.c",):
        p = ROOT / "data" / name
        if p.is_file():
            out.append(str(p.relative_to(ROOT)).replace("\\", "/"))
    return out


def selftest() -> int:
    ok = True

    def chk(name: str, cond: bool, extra: str = "") -> None:
        nonlocal ok
        print(f"  [{'ok' if cond else 'FAIL'}] {name} {extra}")
        ok = ok and cond

    chk("failed ⇒ fail(witness)", classify("VERIFICATION FAILED\n", 1) == "fail(witness)")
    chk("successful ⇒ unknown(bounded)", classify("VERIFICATION SUCCESSFUL\n", 0) == "unknown(bounded)")
    chk("拟命令含 --unwind", "--unwind" in plan_command("x.c"))
    rep = falsify(["data/652_h5_probe.c"])
    chk("esbmc 缺失时降级为 tool_unavailable 或真跑",
        rep["rows"][0]["status"] in ("tool_unavailable", "fail(witness)", "unknown(bounded)", "error"))
    if not rep["esbmc_available"]:
        chk("缺失时给拟命令", "esbmc" in rep["rows"][0]["plan_command"])
    print(f"esbmc_falsify_652 selftest: {'PASS' if ok else 'FAIL'}")
    return 0 if ok else 1


def run_falsify() -> dict:
    probes = _default_probes()
    rep = falsify(probes or ["(无探针：先跑 probe_assembler_652 --build)"])
    OUT_JSON.write_text(json.dumps(rep, ensure_ascii=False, indent=2), encoding="utf-8")
    lines = ["# 652 H6 · ESBMC falsification 试点\n",
             f"- esbmc 可用：**{rep['esbmc_available']}**｜unwind={rep['unwind']}｜探针 {len(rep['rows'])}\n",
             "| 探针 | 状态 | 说明 |", "|---|---|---|"]
    for r in rep["rows"]:
        lines.append(f"| {r['probe']} | {r['status']} | {r.get('plan_command') or r.get('note', '')[:60]} |")
    lines.append("\n> 语义：BMC 失败=硬结论(witness)；BMC 成功**仅** unknown(bounded)（有界通过≠全称）。")
    OUT_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return rep


if __name__ == "__main__":
    ap = argparse.ArgumentParser(description="652 H6 ESBMC falsification 试点")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--run", action="store_true")
    a = ap.parse_args()
    if a.check:
        raise SystemExit(selftest())
    rep = run_falsify()
    print(f"esbmc_available={rep['esbmc_available']}｜→ {OUT_MD.name}")
    raise SystemExit(0)
