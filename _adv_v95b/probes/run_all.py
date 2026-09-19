#!/usr/bin/env python3
"""547 对抗探针总入口：跑 B/C/D 三面，汇总 ESCAPE 数。

用法：.venv/Scripts/python.exe _adv_v95b/probes/run_all.py
退出码：任一 ESCAPE ⇒ 1（红）；否则 0（绿，但"绿"只表示本批没找到新洞，
不表示系统无洞——见 REPORT.md 的未覆盖清单）。
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
PROBES = ["probe_mutation_fuzz.py", "probe_viso_negative.py", "probe_seams.py"]


def main() -> int:
    print("########## 547 第五轮对抗续打 总跑 ##########")
    rc = 0
    for p in PROBES:
        r = subprocess.run([sys.executable, str(HERE / p)], cwd=HERE.parent.parent)
        if r.returncode != 0:
            rc = 1
    print("########## 汇总 ##########")
    print("红(有 ESCAPE)" if rc else "绿(本批无新 ESCAPE；见 REPORT.md 未覆盖清单)")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
