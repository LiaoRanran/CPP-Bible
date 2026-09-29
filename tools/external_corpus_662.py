#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# Copyright 2026 LiaoRanran (阿信)
"""external_corpus_662.py — 662 B1：外部 corpus D3 检出率。

对 corpus 中每个带 code 的样本，按 expected_detector 真跑：
  - compiler-warn / wunsequenced → 本机 g++ -Wall -Wextra 告警
  - cross-compile → 本机 g++ vs clang++ 运行结果差分
  - ubsan / asan / tsan → WSL g++ -fsanitize=...
  - measure → 测量类（非错误）→ not_error（不计入检出率）
  - code=null 或 detector=unknown → unknown

输出：data/external_corpus_reveal_662.json
"""
from __future__ import annotations

import json
import os
import subprocess
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CORPUS = os.path.join(ROOT, "data", "external_corpus", "external_corpus_662.json")
OUT = os.path.join(ROOT, "data", "external_corpus_reveal_662.json")
SAN = {"tsan": "thread", "asan": "address", "ubsan": "undefined"}


def _to_wsl(p):
    p = p.replace("\\", "/")
    return ("/mnt/" + p[0].lower() + p[2:]) if len(p) > 1 and p[1] == ":" else p


def _sh(cmd, timeout=180):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:  # noqa: BLE001
        return -1, f"err:{e}"


def _wsl(cmd, timeout=180):
    return _sh(["wsl", "-e", "bash", "-lc", cmd], timeout)


def detect(kind, code):
    if not code or kind == "unknown":
        return ("unknown", "无本地检测器/无片段")
    d = tempfile.mkdtemp(prefix="d3_")
    src = os.path.join(d, "s.cpp")
    open(src, "w", encoding="utf-8").write(code)
    exe = os.path.join(d, "s.exe")

    if kind in ("compiler-warn", "wunsequenced"):
        extra = ["-Wunsequenced"] if kind == "wunsequenced" else []
        rc, out = _sh(["g++", "-std=c++17", "-Wall", "-Wextra", "-pthread", "-fsyntax-only"] + extra + [src])
        warns = [ln for ln in out.splitlines() if "warning:" in ln]
        return (("catch", f"告警 {len(warns)}: {warns[0][:70]}") if warns else ("miss", "无告警"))

    if kind == "cross-compile":
        outs = []
        for cc in ("g++", "clang++"):
            rc, out = _sh([cc, "-std=c++17", "-O2", "-pthread", src, "-o", exe])
            if rc != 0:
                return ("unknown", f"{cc} 编译失败: {out.strip()[:60]}")
            rc, out = _sh([exe], timeout=30)
            outs.append(out.strip())
        return (("catch", "g++/clang++ 结果不同") if outs[0] != outs[1] else ("miss", "两编译器一致"))

    if kind in SAN:
        w = _to_wsl(src)
        rc, out = _wsl(f"g++ -std=c++17 -O1 -g -fsanitize={SAN[kind]} -pthread {w} -o /tmp/d3bin")
        if rc != 0:
            return ("unknown", f"编译失败: {out.strip()[:60]}")
        rc, out = _wsl("/tmp/d3bin", timeout=60)
        low = out.lower()
        if kind == "tsan" and "FATAL: ThreadSanitizer" in out:
            return ("unknown", "TSan 无法初始化（WSL 不兼容）")
        hit = (("ThreadSanitizer" in out or "data race" in low or rc == 66) if kind == "tsan"
               else any(s in out for s in ("AddressSanitizer", "LeakSanitizer", "runtime error")))
        return (("catch", f"{kind} 命中(rc={rc})") if hit else ("miss", f"{kind} 无报告(rc={rc})"))

    if kind == "measure":
        return ("not_error", "测量类，非错误")
    return ("unknown", "未支持")


def main() -> int:
    c = json.load(open(CORPUS, encoding="utf-8"))
    results = []
    catch = miss = unknown = not_error = 0
    for s in c["samples"]:
        v, note = detect(s["expected_detector"], s.get("code"))
        {"catch": None}.get(v)
        if v == "catch":
            catch += 1
        elif v == "miss":
            miss += 1
        elif v == "not_error":
            not_error += 1
        else:
            unknown += 1
        results.append({"id": s["id"], "category": s["category"], "source": s["source"],
                        "verified_source": s["verified_source"], "detector": s["expected_detector"],
                        "verdict": v, "note": note})
        print(f"  {s['id']:<6} {v.upper():<10} {s['expected_detector']:<14} {note[:60]}")

    denom = catch + miss
    rep = {
        "schema": "queyi-external-corpus-reveal/v1",
        "generated_at": "2026-09-28",
        "generated_by": "tools/external_corpus_662.py",
        "total": len(c["samples"]),
        "catch": catch, "miss": miss, "unknown": unknown, "not_error": not_error,
        "detect_rate_pct": round(catch / denom * 100, 1) if denom else 0.0,
        "source_verified_ratio": f"{sum(1 for r in results if r['verified_source'])}/{len(results)}",
        "honest_note": "detect_rate 分母 = catch+miss（可测且非测量类）；unknown 含无本地检测器/无片段；source 只写类别级出处，未编造具体 issue 编号。",
        "results": results,
    }
    json.dump(rep, open(OUT, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\ncatch={catch} miss={miss} unknown={unknown} not_error={not_error} "
          f"→ 检出率={rep['detect_rate_pct']}%  源可验证={rep['source_verified_ratio']}")
    print(f"已写 {os.path.relpath(OUT, ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
