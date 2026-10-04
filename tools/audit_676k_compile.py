#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""audit_676k_compile.py — 676k 任务C：全量编译抽检（独立复核）。

按批次分层抽 20%（种子 6761），用 **WSL g++ 13.3** 做语法检查：
    g++ -std=c++17 -O0 -g -fsyntax-only <file>

只读：不修改任何样本。

WSL 调用注意（673u 记录）：WSL 2.7 + Windows 系统代理开启时，wsl.exe 每次调用会向 stderr
写一条 UTF-16LE 横幅，Python text=True 解码会抛异常。本脚本强制
`WSL_UTF8=1` + `WSLENV=WSL_UTF8/u`，并用 errors="replace" 兜底。

用法：
  python tools/audit_676k_compile.py --sample          # 写抽检清单
  python tools/audit_676k_compile.py --run --json OUT  # 执行编译并写结果
  python tools/audit_676k_compile.py --report OUT.md   # 生成报告
"""
from __future__ import annotations

import argparse
import collections
import json
import os
import random
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BLINDSPOT = os.path.join(ROOT, "data", "blindspot_676g_sample_manifest.json")
MANIFEST = os.path.join(ROOT, "data", "676k_compile_sample.json")
RESULT = os.path.join(ROOT, "data", "676k_compile_results.json")
SEED = 6761
FRACTION = 0.20
CXXFLAGS = ["-std=c++17", "-O0", "-g", "-fsyntax-only"]


def to_wsl(p: str) -> str:
    """Windows 绝对路径 → WSL /mnt/<drive>/... 形式。"""
    p = os.path.abspath(p).replace("\\", "/")
    if len(p) > 1 and p[1] == ":":
        return "/mnt/" + p[0].lower() + p[2:]
    return p


def load() -> list[dict]:
    bs = json.load(open(BLINDSPOT, encoding="utf-8"))
    out = []
    for e in bs["samples"]:
        d = e.get("dir") or ""
        files = e.get("files") or []
        paths = []
        for f in files:
            p = os.path.join(ROOT, d, f) if d else os.path.join(ROOT, f)
            if os.path.exists(p):
                paths.append(p)
        out.append({
            "uid": e["uid"],
            "batch": e["source_batch"],
            "defect_type": e.get("defect_type"),
            "files": paths,
            "n_files": len(paths),
        })
    return out


def do_sample(recs: list[dict]) -> dict:
    rng = random.Random(SEED)
    by_batch = collections.defaultdict(list)
    for r in recs:
        by_batch[r["batch"]].append(r)
    picked, per_batch = [], {}
    for b in sorted(by_batch):
        ms = sorted(by_batch[b], key=lambda x: x["uid"])
        k = max(1, int(round(FRACTION * len(ms))))
        chosen = rng.sample(ms, k)
        per_batch[b] = {"n": len(ms), "k": k}
        picked.extend(chosen)
    picked.sort(key=lambda x: x["uid"])
    man = {
        "schema": "queyi-audit-676k-compile-sample/v1",
        "generated_by": "tools/audit_676k_compile.py",
        "seed": SEED,
        "fraction": FRACTION,
        "n_population": len(recs),
        "n_sampled": len(picked),
        "n_files": sum(r["n_files"] for r in picked),
        "per_batch": per_batch,
        "sampled": [{"uid": r["uid"], "batch": r["batch"], "defect_type": r["defect_type"],
                     "files": [os.path.relpath(p, ROOT).replace("\\", "/") for p in r["files"]]}
                    for r in picked],
    }
    json.dump(man, open(MANIFEST, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return man


def run_compile() -> dict:
    man = json.load(open(MANIFEST, encoding="utf-8"))
    recs = {r["uid"]: r for r in load()}

    jobs = []  # (uid, wsl_path)
    for s in man["sampled"]:
        for p in recs[s["uid"]]["files"]:
            jobs.append((s["uid"], to_wsl(p)))

    # 一次 WSL 调用完成全部编译（避免每次调用 ~200ms 的启动开销）
    lines = []
    for uid, wp in jobs:
        lines.append(f'{uid}\t{wp}')
    payload = "\n".join(lines) + "\n"

    script = (
        'export WSL_UTF8=1\n'
        'while IFS=$\'\\t\' read -r uid f; do\n'
        '  [ -z "$uid" ] && continue\n'
        '  err=$(g++ ' + " ".join(CXXFLAGS) + ' "$f" 2>&1)\n'
        '  rc=$?\n'
        '  err=$(printf "%s" "$err" | head -c 400 | tr "\\n" "|" | tr "\\t" " ")\n'
        '  printf "%s\\t%d\\t%s\\n" "$uid" "$rc" "$err"\n'
        'done\n'
    )

    env = dict(os.environ)
    env["WSL_UTF8"] = "1"
    env["WSLENV"] = (env.get("WSLENV", "") + ":WSLUTF8/u").lstrip(":")

    proc = subprocess.run(
        ["wsl.exe", "-e", "bash", "-lc", script],
        input=payload.encode("utf-8"),
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env,
    )
    out = proc.stdout.decode("utf-8", errors="replace")
    err = proc.stderr.decode("utf-8", errors="replace")

    per_file = []
    for ln in out.splitlines():
        parts = ln.split("\t")
        if len(parts) < 2:
            continue
        uid, rc = parts[0], parts[1]
        msg = parts[2] if len(parts) > 2 else ""
        per_file.append({"uid": uid, "rc": int(rc), "msg": msg[:400]})

    by_uid = collections.defaultdict(list)
    for r in per_file:
        by_uid[r["uid"]].append(r)

    samples = []
    for s in man["sampled"]:
        uid = s["uid"]
        rs = by_uid.get(uid, [])
        failed = [r for r in rs if r["rc"] != 0]
        status = "no_source" if not recs[uid]["files"] else ("pass" if not failed else "fail")
        samples.append({
            "uid": uid, "batch": s["batch"], "defect_type": s["defect_type"],
            "n_files": len(recs[uid]["files"]),
            "n_compiled": len(rs),
            "status": status,
            "pass": status == "pass",
            "files": rs,
        })

    result = {
        "schema": "queyi-audit-676k-compile/v1",
        "generated_by": "tools/audit_676k_compile.py",
        "compiler": "WSL g++ 13.3.0 (Ubuntu 13.3.0-6ubuntu2~24.04.1)",
        "flags": " ".join(CXXFLAGS),
        "seed": SEED,
        "n_sampled": len(man["sampled"]),
        "n_files": len(jobs),
        "n_file_results": len(per_file),
        "wsl_rc": proc.returncode,
        "wsl_stderr_head": err[:300],
        "samples": samples,
    }
    json.dump(result, open(RESULT, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    return result


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--sample", action="store_true")
    ap.add_argument("--run", action="store_true")
    ap.add_argument("--json")
    args = ap.parse_args()

    if args.sample:
        m = do_sample(load())
        print(f"抽检清单：总体 {m['n_population']}，抽中 {m['n_sampled']} 样本 / "
              f"{m['n_files']} 个文件 → {MANIFEST}")
        for b, v in sorted(m["per_batch"].items()):
            print(f"   {b}: {v['k']}/{v['n']}")
        return 0
    if args.run:
        r = run_compile()
        ok = sum(1 for s in r["samples"] if s["status"] == "pass")
        ns = sum(1 for s in r["samples"] if s["status"] == "no_source")
        fail = sum(1 for s in r["samples"] if s["status"] == "fail")
        print(f"编译抽检：pass={ok}  fail={fail}  no_source={ns}  合计={r['n_sampled']}")
        print(f"文件级结果 {r['n_file_results']}/{r['n_files']}，wsl_rc={r['wsl_rc']}")
        if r["wsl_stderr_head"]:
            print("wsl stderr head:", r["wsl_stderr_head"][:200])
        print("结果已写入", RESULT)
        return 0
    ap.print_help()
    return 0


if __name__ == "__main__":
    sys.exit(main())
