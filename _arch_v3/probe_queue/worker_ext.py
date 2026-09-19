#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""worker_ext.py — 被 harness 驱动的"苦力 worker"（新会话=新进程=零上下文）。

只知道环境变量给的 DB/ROOT/WORKER 身份与接管参数，不接收任何其它上下文：
  TQEXT_DB        沙箱 queue.db
  TQEXT_ROOT      锚根（handoff 锚点/touch 审计/git 的基准）
  TQEXT_WORKDIR   产物目录
  TQEXT_WORKER    worker 身份
  TQEXT_TAKEOVER  非空=认领时带 --takeover <id>
  TQEXT_FORCE / TQEXT_REASON  接管 force 与原因
  TQEXT_YIELD_AFTER  做到该步后 yield（预算写满 480）
流程：claim（可能接管）→ 盘上哈希独立核对 steps_done → 做剩余步骤并逐步 checkpoint
      → yield 或 complete（verify 由队列绑定，worker 无法自证）。
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
DB = os.environ["TQEXT_DB"]
ROOT = Path(os.environ["TQEXT_ROOT"])
WORKDIR = Path(os.environ["TQEXT_WORKDIR"])
WORKER = os.environ["TQEXT_WORKER"]
TAKEOVER = os.environ.get("TQEXT_TAKEOVER", "")
FORCE = os.environ.get("TQEXT_FORCE", "") == "1"
REASON = os.environ.get("TQEXT_REASON", "")
YIELD_AFTER = int(os.environ.get("TQEXT_YIELD_AFTER", "0"))
STEP_SLEEP = float(os.environ.get("TQEXT_STEP_SLEEP", "0.8"))


def tqext(*args: str) -> tuple[int, str, str]:
    p = subprocess.run([PY, str(HERE / "tq_ext.py"), "--db", DB, *args],
                       capture_output=True, text=True, encoding="utf-8",
                       errors="replace", cwd=str(ROOT))
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
    rel = f.relative_to(ROOT).as_posix()
    return {"n": n, "title": f"step {n}",
            "outputs": [{"path": rel, "sha256": sha(f)}]}


def main() -> int:
    args = ["--json", "claim", "--worker", WORKER]
    if TAKEOVER:
        args += ["--takeover", TAKEOVER]
        if FORCE:
            args += ["--force", "--reason", REASON or "旧会话已死，人工开新会话接管"]
    rc, out, err = tqext(*args)
    if rc != 0 or not out.strip():
        journal(f"NO-TASK rc={rc} {err.strip()[:160]}")
        return 0
    r = json.loads(out)
    t = r.get("claimed")
    if not t:
        journal(f"NO-TASK blocked_by_touch={r.get('blocked_by_touch')}")
        return 0
    tid = t["id"]
    total = int(t.get("steps_total") or 0) or 5
    handoff = t.get("handoff") or {}
    journal(f"CLAIMED {tid} attempt={t['attempts']} inherited={t['steps_done']} "
            f"takeover={bool(TAKEOVER)} next_action={handoff.get('next_action')}")

    # 零上下文核对：handoff 说做过的，逐一对盘上产物验哈希；不符就重做
    done_nums: set[int] = set()
    for st in handoff.get("steps_done") or []:
        n = int(st["n"])
        ok = True
        for o in st.get("outputs") or []:
            f = ROOT / o["path"]
            if not f.is_file() or sha(f) != o["sha256"]:
                ok = False
                journal(f"MISTRUST step {n}（产物缺失/哈希不符）→ 重做")
        if ok:
            done_nums.add(n)
            journal(f"TRUST step {n}（盘上哈希一致，不重做）")

    declared = [int(x["n"]) for x in handoff.get("steps_remaining") or []]
    remaining = declared or [n for n in range(1, total + 1) if n not in done_nums]
    remaining = [n for n in remaining if n not in done_nums]

    steps_done = list(handoff.get("steps_done") or [])
    for idx, n in enumerate(remaining):
        steps_done = [s for s in steps_done if int(s["n"]) != n]
        steps_done.append(do_step(n, total))
        steps_done.sort(key=lambda s: int(s["n"]))
        later = remaining[idx + 1:]
        hp = WORKDIR / f"{tid}.handoff.json"
        h = {
            "schema": "tq-handoff/v1", "task_id": tid,
            "goal": handoff.get("goal") or t.get("goal") or f"完成 {total} 步流水线",
            "steps_done": steps_done,
            "steps_remaining": [{"n": x, "title": f"step {x}",
                                 "action": "worker_ext.py（写 stepX.txt + checkpoint）",
                                 "touch": [f"work/step{x}.txt"]} for x in later],
            "verified_facts": [
                {"fact": f"step1..{n} 产物在盘且哈希已记录", "trust": "L1",
                 "anchor": f"work/step{n}.txt:1"}],
            "tried_and_failed": handoff.get("tried_and_failed", []),
            "next_action": f"继续 step{n + 1}（claim 后逐步 checkpoint）" if later
                           else "complete（队列自动跑绑定的 verify_cmd）",
            "touched_files": [s["outputs"][0]["path"] for s in steps_done],
            "budget_used": 300 + n * 25,
            "open_questions": [],
        }
        hp.write_text(json.dumps(h, ensure_ascii=False, indent=1), encoding="utf-8")
        rc2, o2, e2 = tqext("--json", "checkpoint", tid, "--worker", WORKER,
                           "--handoff", str(hp))
        if rc2 != 0:
            journal(f"CHECKPOINT-FAIL step {n}: {e2.strip()[:200]}")
            return 3
        if YIELD_AFTER and n == YIELD_AFTER:
            h["budget_used"] = 480
            hp.write_text(json.dumps(h, ensure_ascii=False, indent=1), encoding="utf-8")
            rc3, o3, e3 = tqext("--json", "yield", tid, "--worker", WORKER,
                               "--handoff", str(hp), "--force")
            journal(f"YIELD rc={rc3} {o3.strip() or e3.strip()[:200]}")
            return 0 if rc3 == 0 else 4

    rc4, o4, e4 = tqext("--json", "complete", tid, "--worker", WORKER)
    journal(f"COMPLETE rc={rc4} {o4.strip() or e4.strip()[:240]}")
    return 0 if rc4 == 0 else 5


if __name__ == "__main__":
    raise SystemExit(main())
