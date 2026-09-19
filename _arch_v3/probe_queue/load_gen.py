#!/usr/bin/env python3
"""load_gen.py — 多进程写压力（S7）：每进程 enqueue N 个 custom 任务 + 半数带 heartbeat。"""
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = sys.executable
N = int(sys.argv[1]) if len(sys.argv) > 1 else 20
TAG = sys.argv[2] if len(sys.argv) > 2 else "g"
errors = []
for i in range(N):
    tid = f"load-{TAG}-{os.getpid()}-{i}"
    p = subprocess.run([PY, str(HERE / "tq.py"), "enqueue", "--type", "custom",
                        "--id", tid, "--goal", "load", "--worker", f"load-{TAG}"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0 or "locked" in (p.stderr + p.stdout):
        errors.append((tid, p.returncode, (p.stderr or p.stdout)[:120]))
print(f"loadgen {TAG} pid={os.getpid()} enqueued={N} errors={len(errors)}")
for e in errors:
    print("ERR", e)
sys.exit(1 if errors else 0)
