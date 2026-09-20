#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""worker_sim.py — 被 harness 驱动的"苦力 worker"进程（新会话=新进程=零上下文）。

它只知道三件事：
  1) 调 tq.py next --worker <id> 领任务（不接收任何其它上下文参数）；
  2) 从 handoff 的 steps_done 独立核对产物哈希（L1 不信任继承，只信任盘上哈希）；
  3) 做剩余步骤：每步写产物 → checkpoint；做完 complete。
日志 journal.log 只追加，供 harness 事后证明"谁做了哪几步、有无重跑"。
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = sys.executable
WORKDIR = Path(os.environ["TQ_WORKDIR"])
WORKER = os.environ["TQ_WORKER"]
MAX_STEPS = int(os.environ.get("TQ_MAX_STEPS", "0"))      # >0 时只做到该步
YIELD_AFTER = os.environ.get("TQ_YIELD_AFTER", "")        # 做到该步后 yield（逗号分隔剩余）
STEP_SLEEP = float(os.environ.get("TQ_STEP_SLEEP", "0.8"))


def tq(*args: str) -> tuple[int, str, str]:
    p = subprocess.run([PY, str(HERE / "tq.py"), *args], capture_output=True,
                       text=True, errors="replace", encoding="utf-8")
    return p.returncode, p.stdout, p.stderr


def journal(line: str) -> None:
    with (WORKDIR / "journal.log").open("a", encoding="utf-8") as f:
        f.write(f"{time.strftime('%H:%M:%S')} {WORKER} {line}\n")


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def do_step(n: int, total: int) -> dict:
    f = WORKDIR / f"step{n}.txt"
    f.write_text(f"step{n}-artifact by {WORKER} pid={os.getpid()}\n", encoding="utf-8")
    time.sleep(STEP_SLEEP)
    journal(f"DID step {n}/{total}")
    return {"n": n, "title": f"step {n}",
            "outputs": [{"path": str(f.relative_to(Path(os.environ["TQ_ROOT"]))),
                         "sha256": sha(f)}]}


def main() -> int:
    rc, out, err = tq("next", "--worker", WORKER)
    if rc != 0:
        journal(f"NO-TASK rc={rc} {err.strip()[:120]}")
        return 0
    t = json.loads(out)
    tid = t["task_id"]
    total = t["steps_total"] or 5
    handoff = t.get("handoff") or {}
    journal(f"CLAIMED {tid} attempt={t['attempts']} inherited_steps={t['steps_done']} "
            f"next_action={t.get('next_action')}")

    # 零上下文核对：handoff 说做过的步骤，逐一对盘上产物验哈希；不符就重做
    done_nums: set[int] = set()
    for st in handoff.get("steps_done") or []:
        n = int(st["n"])
        ok = True
        for o in st.get("outputs") or []:
            f = Path(os.environ["TQ_ROOT"]) / o["path"]
            if not f.is_file() or sha(f) != o["sha256"]:
                ok = False
                journal(f"MISTRUST step {n}（产物缺失/哈希不符）→ 重做")
        if ok:
            done_nums.add(n)
            journal(f"TRUST step {n}（盘上哈希一致，不重做）")

    # 剩余步骤号：有 handoff 时以 steps_remaining 的绝对编号为权威（子任务场景），
    # 全新任务才按 steps_total 生成 1..N
    rem_declared = [int(x["n"]) for x in (handoff.get("steps_remaining") or [])]
    if rem_declared:
        remaining = [n for n in rem_declared if n not in done_nums]
    else:
        remaining = [n for n in range(1, total + 1) if n not in done_nums]
    if MAX_STEPS:
        remaining = [n for n in remaining if n <= MAX_STEPS]
    yield_at = int(YIELD_AFTER) if YIELD_AFTER else 0

    steps_done = list(handoff.get("steps_done") or [])
    anchor_root = Path(os.environ["TQ_ROOT"])
    for idx, n in enumerate(remaining):
        steps_done = [s for s in steps_done if int(s["n"]) != n]
        steps_done.append(do_step(n, total))
        steps_done.sort(key=lambda s: int(s["n"]))
        later = remaining[idx + 1:]
        hp = WORKDIR / f"{tid}.handoff.json"
        h = {
            "schema": "tq-handoff/v1", "task_id": tid,
            "goal": t.get("goal") or f"完成 {total} 步产物流水线",
            "steps_done": steps_done,
            "steps_remaining": [{"n": x, "title": f"step {x}",
                                 "action": f"python worker_sim.py（写 step{x}.txt）",
                                 "touch": [str((WORKDIR.relative_to(anchor_root)) / f"step{x}.txt")]}
                                for x in later],
            "verified_facts": [
                {"fact": f"step1..{n} 产物在盘且哈希已记录", "trust": "L1",
                 "anchor": f"{WORKDIR.relative_to(anchor_root)}/step{n}.txt:1"}],
            "tried_and_failed": [],
            "next_action": f"继续 step{n + 1}" if later else "complete（verify_checker.py）",
            "touched_files": [s["outputs"][0]["path"] for s in steps_done],
            "budget_used": 300 + n * 25,
            "open_questions": [],
        }
        hp.write_text(json.dumps(h, ensure_ascii=False, indent=1), encoding="utf-8")
        rc2, o2, e2 = tq("checkpoint", tid, "--worker", WORKER, "--handoff", str(hp))
        if rc2 != 0:
            journal(f"CHECKPOINT-FAIL step {n}: {e2.strip()[:200]}")
            return 3
        if yield_at and n == yield_at:
            # 模拟到顶让出：预算打满强制 yield
            h["budget_used"] = 480
            h["steps_remaining"] = [{"n": x, "title": f"step {x}",
                                     "action": f"python worker_sim.py（写 step{x}.txt）",
                                     "touch": [str((WORKDIR.relative_to(anchor_root)) / f"step{x}.txt")]}
                                    for x in later]
            hp.write_text(json.dumps(h, ensure_ascii=False, indent=1), encoding="utf-8")
            rc3, o3, e3 = tq("yield", tid, "--worker", WORKER, "--handoff", str(hp), "--force")
            journal(f"YIELD rc={rc3} {o3.strip() or e3.strip()[:160]}")
            return 0 if rc3 == 0 else 4

    # 全部步骤完成：complete（verify_cmd 已在 enqueue 绑定）
    rc4, o4, e4 = tq("complete", tid, "--worker", WORKER)
    journal(f"COMPLETE rc={rc4} {o4.strip() or e4.strip()[:200]}")
    return 0 if rc4 == 0 else 5


if __name__ == "__main__":
    raise SystemExit(main())
