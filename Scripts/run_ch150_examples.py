#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""编译并运行第150章全部自包含示例，真实输出写入 _run/ch150_mine.log。"""
import os, subprocess, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
EX = os.path.join(ROOT, "Examples")
RUN = os.path.join(ROOT, "_run")
os.makedirs(RUN, exist_ok=True)
GPP = r"C:/Qt/Tools/mingw1530_64/bin/g++.exe"
LOG = os.path.join(RUN, "ch150_mine.log")

cpps = sorted(glob.glob(os.path.join(EX, "_ch150_*.cpp")))
lines = []
ok = fail = 0
for cpp in cpps:
    base = os.path.splitext(os.path.basename(cpp))[0]
    exe = os.path.join(RUN, base + ".exe")
    comp = [GPP, "-std=c++17", "-O2", "-Wall", "-Wextra", "-o", exe, cpp]
    rc = subprocess.run(comp, capture_output=True, text=True)
    if rc.returncode != 0:
        fail += 1
        lines.append(f"### {base}\n[COMPILE FAIL]\n{rc.stdout}\n{rc.stderr}\n")
        continue
    rr = subprocess.run([exe], capture_output=True, text=True)
    if rr.returncode != 0:
        fail += 1
        lines.append(f"### {base}\n[RUN rc={rr.returncode}]\n{rr.stdout}\n{rr.stderr}\n")
    else:
        ok += 1
        lines.append(f"### {base}\n{rr.stdout.rstrip()}\n")

with open(LOG, "w", encoding="utf-8") as f:
    f.write("\n".join(lines) + "\n")
print(f"[run] ok={ok} fail={fail} examples={len(cpps)}")
print(f"[run] log -> {LOG}")
