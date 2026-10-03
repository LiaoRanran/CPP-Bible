#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""诊断：对淘汰样本重新跑检测器，打印去横幅后的原始输出，判断该 relabel 还是 eliminate。"""
import os
import sys
import json

os.environ["WSL_UTF8"] = "1"
os.environ["WSLENV"] = "WSL_UTF8/u"
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import validate_B as V  # noqa: E402

det = V.det
SAMPLE_DIR = V.SAMPLE_DIR
BANNER = "wsl: 检测到 localhost 代理配置，但未镜像到 WSL。NAT 模式下的 WSL 不支持 localhost 代理。"


def strip(s):
    return s.replace(BANNER, "").strip()


def run_san(sid, san):
    src = det._to_wsl(os.path.join(SAMPLE_DIR, sid + ".cpp"))
    out_all = {}
    for opt in det.OPT_LEVELS:
        exe = det._to_wsl(f"/tmp/diag_{sid}_{opt}.exe")
        cc = f"g++ -std=c++17 {opt} -g -fsanitize={san} -pthread -o {exe} {src}"
        rc, o = det._wsl(cc, timeout=120)
        if rc != 0:
            out_all[opt] = f"[COMPILE FAIL rc={rc}] {strip(o)[:300]}"
            continue
        pre = det._setarch_prefix() if san == "thread" else ""
        rc, o = det._wsl(pre + exe, timeout=120)
        out_all[opt] = f"[rc={rc}] {strip(o)[:400]}"
    return out_all


def main():
    targets = {
        "sample_B002": "thread", "sample_B005": "thread", "sample_B006": "thread",
        "sample_B011": "thread", "sample_B012": "thread", "sample_B020": "thread",
        "sample_B027": "undefined", "sample_B028": "undefined", "sample_B029": "undefined",
        "sample_B030": "undefined", "sample_B086": "undefined", "sample_B077": "undefined",
        "sample_B047": "address", "sample_B050": "address", "sample_B054": "address",
        "sample_B057": "address", "sample_B090": "address",
    }
    for sid, san in targets.items():
        print(f"\n===== {sid} [{san}] =====")
        for opt, out in run_san(sid, san).items():
            print(f"  [{opt}] {out}")


if __name__ == "__main__":
    main()
