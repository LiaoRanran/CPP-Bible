#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""verify_676c.py — 676c 扩样-A 验证器（Task B + C）。

Task B（编译校验）：本机 g++ -std=c++17 -O0 -fsyntax-only 做语法校验
  （本地 MinGW 13.1 缺 libasan，无法链接 -fsanitize，故语法检查用 -fsyntax-only；
   sanitizer 链接与运行由 Task C 的 detect()->WSL 完成，等价更强校验）。

Task C（检测器复现）：调用 tools/holdout_reveal_661.detect() 真实跑检测器
  - memory_safety / out_of_bounds / null_pointer_deref -> asan (WSL)
  - undefined_behavior                            -> ubsan (WSL)
  - uninitialized_read                            -> compiler-warn (本机)
  与标注 expected_verdict / expected_detectors 比对并调和：
    - 一致 -> pass（入池候选）
    - expected=miss 但实测=catch -> 更新标注为 catch（合理），pass
    - expected=catch 但实测=miss/unknown -> 淘汰（缺陷不实或检测器不覆盖）

结果写回各 sample_NNN.json 的 "verification" 字段，并汇总结算。
"""
import os
import sys
import json
import time
import shutil
import argparse
import importlib.util

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))  # repo root
TOOLS = os.path.join(REPO, "tools")
ATOMS = os.path.join(REPO, "Examples", "atoms")
EXP = os.path.join(REPO, "data", "expansion_676c")
RESULTS = os.path.join(EXP, "verify_results.json")

spec = importlib.util.spec_from_file_location(
    "holdout_reveal_661", os.path.join(TOOLS, "holdout_reveal_661.py"))
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)
detect = mod.detect


def local_syntax(cpp):
    try:
        r = subprocess.run(["g++", "-std=c++17", "-O0", "-fsyntax-only", cpp],
                           capture_output=True, text=True, timeout=120)
    except Exception as e:  # noqa
        return (-1, f"local_error:{e}", [])
    warns = [ln.strip() for ln in (r.stdout + r.stderr).splitlines() if "warning:" in ln]
    return (r.returncode, (r.stdout + r.stderr).strip(), warns)


import subprocess


def verify_one(idx):
    n3 = f"{idx:03d}"
    cpp = os.path.join(EXP, f"sample_{n3}.cpp")
    jp = os.path.join(EXP, f"sample_{n3}.json")
    rec = {"id": f"sample_{n3}", "stage": "init"}
    t0 = time.time()
    if not os.path.isfile(cpp) or not os.path.isfile(jp):
        rec.update(stage="missing", pooled=False, reason="file missing")
        return rec
    meta = json.load(open(jp, encoding="utf-8"))

    # --- Task B: 语法编译 ---
    rc, out, warns = local_syntax(cpp)
    rec["syntax_rc"] = rc
    rec["syntax_warnings"] = warns
    if rc != 0:
        rec.update(stage="compile_fail", pooled=False,
                   reason=f"syntax error: {out[:160]}")
        meta["verification"] = {k: rec[k] for k in
                                ("stage", "syntax_rc", "pooled", "reason")}
        json.dump(meta, open(jp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        return rec

    # --- Task C: detect() ---
    kind = (meta.get("expected_detectors") or ["asan"])[0]
    tmp_name = f"_676c_tmp_{n3}.cpp"
    tmp_path = os.path.join(ATOMS, tmp_name)
    shutil.copy2(cpp, tmp_path)
    try:
        verdict, note = detect(kind, [tmp_name])
    except Exception as e:  # noqa
        verdict, note = "unknown", f"detect_exception:{e}"
    finally:
        try:
            os.remove(tmp_path)
        except OSError:
            pass

    rec["detector_kind"] = kind
    rec["detector_verdict"] = verdict
    rec["detector_note"] = note[:300]

    expected = meta.get("expected_verdict")
    # 调和
    if verdict == "catch":
        if expected == "miss":
            meta["expected_verdict"] = "catch"  # 合理不一致，更新标注
            rec["reconcile"] = "updated_to_catch"
        else:
            rec["reconcile"] = "consistent"
        rec["pooled"] = True
        rec["stage"] = "pass"
    elif verdict == "miss":
        if expected == "miss":
            rec["reconcile"] = "consistent"
            rec["pooled"] = True
            rec["stage"] = "pass"
        else:
            rec["reconcile"] = "inconsistent_catch_expected"
            rec["pooled"] = False
            rec["stage"] = "detector_fail"
            rec["reason"] = "expected catch but detector miss (defect not reproduced)"
    else:  # unknown
        rec["reconcile"] = "detector_unknown"
        rec["pooled"] = False
        rec["stage"] = "detector_unknown"
        rec["reason"] = f"detector unavailable/error: {note[:120]}"

    meta["verification"] = {
        "syntax_rc": rec["syntax_rc"],
        "syntax_warnings": rec["syntax_warnings"],
        "detector_kind": rec["detector_kind"],
        "detector_verdict": rec["detector_verdict"],
        "detector_note": rec["detector_note"],
        "reconcile": rec["reconcile"],
        "pooled": rec["pooled"],
        "stage": rec["stage"],
        "reason": rec.get("reason", ""),
    }
    json.dump(meta, open(jp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    rec["elapsed_s"] = round(time.time() - t0, 2)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--end", type=int, default=100)
    a = ap.parse_args()
    results = {}
    if os.path.isfile(RESULTS):
        results = json.load(open(RESULTS, encoding="utf-8"))
    passed = failed = 0
    for idx in range(a.start, a.end + 1):
        rec = verify_one(idx)
        results[rec["id"]] = rec
        if rec.get("pooled"):
            passed += 1
        else:
            failed += 1
        print(f"  {rec['id']} pooled={rec.get('pooled')} "
              f"stage={rec.get('stage')} det={rec.get('detector_verdict')} "
              f"kind={rec.get('detector_kind')}")
    json.dump(results, open(RESULTS, "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    total_t = sum(r.get("elapsed_s", 0) for r in results.values())
    avg_t = (total_t / len(results)) if results else 0
    print(f"\n[chunk {a.start}-{a.end}] pass_candidate={passed} fail={failed} "
          f"avg_per_sample={avg_t:.2f}s (cumulative over {len(results)} samples)")


if __name__ == "__main__":
    main()
