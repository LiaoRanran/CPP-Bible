#!/usr/bin/env python3
"""一键门禁汇总：跑 gate / poison / replay / pytest，输出一行可读报告。

用法：
    python scripts/door_check.py            # 全量（约 2-3 分钟，replay 最慢）
    python scripts/door_check.py --fast     # 跳过 replay（约 10 秒，快速看规则层）
    python scripts/door_check.py --json     # 机器可读输出

只读，不修改任何文件。退出码：全绿=0，任一失败=1。
"""
from __future__ import annotations
import argparse
import json
import re
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable


def run(cmd: list[str], timeout: int = 300) -> tuple[int, str]:
    """跑命令，返回 (exit_code, 尾部输出)。"""
    try:
        p = subprocess.run(
            cmd, cwd=ROOT, capture_output=True, text=True,
            timeout=timeout, encoding="utf-8", errors="replace",
        )
        out = (p.stdout or "") + (p.stderr or "")
        return p.returncode, out
    except subprocess.TimeoutExpired:
        return 124, f"[TIMEOUT after {timeout}s]"
    except FileNotFoundError as e:
        return 127, f"[NOT FOUND] {e}"


def last_nonempty(text: str, n: int = 3) -> str:
    lines = [l.rstrip() for l in text.splitlines() if l.strip()]
    return " | ".join(lines[-n:]) if lines else "(no output)"


def parse_gate(text: str) -> dict:
    """从 gate --check 输出提取 block/warn/advice 计数。"""
    block = len(re.findall(r"\[BLOCK\s*\]", text))
    warn = len(re.findall(r"\[WARN\s*\]", text))
    advice = len(re.findall(r"\[ADVICE\s*\]", text))
    # 也尝试匹配汇总行
    m = re.search(r"block=(\d+).*warn=(\d+).*advice=(\d+)", text)
    if m:
        block, warn, advice = int(m[1]), int(m[2]), int(m[3])
    return {"block": block, "warn": warn, "advice": advice}


def parse_poison(text: str) -> dict:
    # 精确匹配汇总行：[poison] 46/46 —— ...
    m = re.search(r"\[poison\]\s+(\d+)/(\d+)", text)
    if m:
        return {"passed": int(m.group(1)), "total": int(m.group(2))}
    # 兜底：RULE-COVERAGE 行
    m2 = re.search(r"RULE-COVERAGE:\s+(\d+)/(\d+)", text)
    if m2:
        return {"passed": int(m2.group(1)), "total": int(m2.group(2)), "note": "coverage only"}
    return {"passed": 0, "total": 0, "raw": last_nonempty(text, 1)}


def parse_replay(text: str) -> dict:
    m = re.search(r"confirm=(\d+).*refute=(\d+)(?:.*infra_error=(\d+))?", text)
    if m:
        return {"confirm": int(m[1]), "refute": int(m[2]),
                "infra_error": int(m.group(3) or 0)}
    return {"raw": last_nonempty(text, 1)}


def parse_pytest(text: str) -> dict:
    m = re.search(r"(\d+)\s+passed", text)
    failed = re.search(r"(\d+)\s+failed", text)
    return {"passed": int(m.group(1)) if m else 0,
            "failed": int(failed.group(1)) if failed else 0,
            "raw": last_nonempty(text, 1) if not m else ""}


def main() -> int:
    ap = argparse.ArgumentParser(description="一键门禁汇总")
    ap.add_argument("--fast", action="store_true", help="跳过 replay（快速看规则层）")
    ap.add_argument("--json", action="store_true", help="JSON 输出")
    args = ap.parse_args()

    results: dict[str, dict] = {}
    t0 = time.time()

    # 1. gate
    rc, out = run([PY, "tools/gate_engine.py", "--check"], timeout=60)
    results["gate"] = {**parse_gate(out), "rc": rc}

    # 2. poison（编译毒样例慢，给足时间）
    rc, out = run([PY, "tools/poison_drill.py"], timeout=300)
    results["poison"] = {**parse_poison(out), "rc": rc}

    # 3. replay（可选跳过）
    if not args.fast:
        rc, out = run([PY, "tools/atom_evidence_replay.py", "--check"], timeout=600)
        results["replay"] = {**parse_replay(out), "rc": rc}
    else:
        results["replay"] = {"skipped": True}

    # 4. pytest
    rc, out = run([PY, "-m", "pytest", "tests/", "-q"], timeout=120)
    results["pytest"] = {**parse_pytest(out), "rc": rc}

    elapsed = time.time() - t0
    results["elapsed_s"] = round(elapsed, 1)

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print(f"{'='*60}")
        print(f"  阙疑门禁汇总  ({elapsed:.0f}s)")
        print(f"{'='*60}")
        g = results["gate"]
        gate_ok = g.get("block", 1) == 0
        print(f"  gate     : block={g.get('block')}  warn={g.get('warn')}  advice={g.get('advice')}  {'✅' if gate_ok else '🔴 BLOCK'}")
        p = results["poison"]
        poison_ok = p.get("passed", 0) == p.get("total", 1) and p.get("total", 0) > 0
        print(f"  poison   : {p.get('passed')}/{p.get('total')}  {'✅' if poison_ok else '🔴'}")
        r = results["replay"]
        if r.get("skipped"):
            print(f"  replay   : (skipped --fast)")
        else:
            replay_ok = r.get("refute", 1) == 0 and r.get("confirm", 0) > 0
            print(f"  replay   : confirm={r.get('confirm')}  refute={r.get('refute')}  infra={r.get('infra_error')}  {'✅' if replay_ok else '🔴'}")
        pt = results["pytest"]
        pytest_ok = pt.get("failed", 1) == 0 and pt.get("passed", 0) > 0
        print(f"  pytest   : {pt.get('passed')} passed  {pt.get('failed')} failed  {'✅' if pytest_ok else '🔴'}")
        print(f"{'='*60}")
        all_ok = gate_ok and poison_ok and (r.get("skipped") or replay_ok) and pytest_ok
        print(f"  总体: {'✅ 全绿' if all_ok else '🔴 有失败'}")

    return 0 if (results["gate"].get("block", 1) == 0
                 and results["poison"].get("passed", 0) == results["poison"].get("total", 1)
                 and (args.fast or results["replay"].get("refute", 1) == 0)
                 and results["pytest"].get("failed", 1) == 0) else 1


if __name__ == "__main__":
    sys.exit(main())
