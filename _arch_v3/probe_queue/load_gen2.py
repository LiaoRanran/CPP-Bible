#!/usr/bin/env python3
"""S7 写压力：N 次 enqueue（独立 touch 文件，避免 touch 互锁——本场景测 WAL 写锁）。"""
import os
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PY = sys.executable
DB = sys.argv[1]
N = int(sys.argv[2])
TAG = sys.argv[3]
errs = []
for i in range(N):
    tid = f"load-{TAG}-{os.getpid()}-{i}"
    p = subprocess.run(
        [PY, str(HERE / "tq_ext.py"), "--db", DB, "--json", "enqueue",
         "--type", "custom", "--id", tid, "--payload-ref", f"docs/{tid}.md",
         "--touch", f"w/{TAG}-{i}.txt"],
        capture_output=True, text=True, encoding="utf-8", errors="replace")
    if p.returncode != 0:
        errs.append((tid, p.returncode, (p.stderr or p.stdout)[:160]))
print(f"loadgen {TAG} pid={os.getpid()} enqueued={N} errors={len(errs)}")
for e in errs:
    print("ERR", e)
sys.exit(1 if errs else 0)
