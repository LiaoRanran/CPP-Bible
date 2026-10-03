#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""probe_E.py — 开发期定位：对指定样本在 WSL 编译并**直接运行**，打印真实输出。

用途：区分「缺陷导致的挂起」与「样本编排写错导致的挂起」（例如门闸变量
根本没人置位）。verify_E.py 只能看到 rc=124，看不出死在哪。
"""
import re
import subprocess
import sys

HERE = r"C:\CodeLearnling\note\note\C++\CPP-Bible\data\expansion_676c_E"
WSL_DIR = "/mnt/c/CodeLearnling/note/note/C++/CPP-Bible/data/expansion_676c_E"


def to_wsl(p):
    return p.replace("\\", "/").replace("C:", "/mnt/c")


def run(sid, san="address", opt="-O0", tmo=5):
    src = f"{WSL_DIR}/sample_{sid}.cpp"
    exe = f"/tmp/probe_{sid}"
    cc = (f"g++ -std=c++17 {opt} -g -fsanitize={san} -pthread {src} -o {exe}")
    r = subprocess.run(["wsl", "-e", "bash", "-lc", cc], capture_output=True,
                       text=True, timeout=300)
    if r.returncode != 0:
        print(f"{sid} COMPILE FAIL: {(r.stdout + r.stderr)[:300]}")
        return
    r2 = subprocess.run(["wsl", "-e", "bash", "-lc", f"timeout {tmo} {exe}"],
                        capture_output=True, text=True, timeout=60)
    out = (r2.stdout or "") + (r2.stderr or "")
    print(f"--- {sid} [{san} {opt}] rc={r2.returncode} ---")
    print(out.strip()[:900] or "(无输出)")
    print()


if __name__ == "__main__":
    sans = {"asan": "address", "tsan": "thread", "ubsan": "undefined"}
    for arg in sys.argv[1:]:
        sid, _, s = arg.partition(":")
        run(sid, sans.get(s, "address"))
