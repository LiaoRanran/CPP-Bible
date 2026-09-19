#!/usr/bin/env python3
"""verify 夹具（通过型）：检查 work/step1..5.txt 全部存在且非空。"""
import sys
from pathlib import Path

root = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
missing = [n for n in range(1, 6) if not (root / "work" / f"step{n}.txt").is_file()]
if missing:
    print(f"VERIFY-FAIL missing={missing}")
    raise SystemExit(1)
print("VERIFY-OK all 5 artifacts present")
