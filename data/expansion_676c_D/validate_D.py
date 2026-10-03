#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
# 676c-D 验证编排器：对每个样本做
#   1) 本地语法校验 (g++ -std=c++17 -Wall -Wextra -fsyntax-only)
#   2) 真实 detect() 复现：asan / ubsan (WSL) + compiler-warn (本地)
# 然后把真实结果写回每个 sample_Dxxx.json 的 verification 块，并据实更新
# expected_verdict / expected_detectors（卡要求：若实际与预期不同可合理更新标注）。
# 判定口径（诚实边界）：actual_verdict 以 asan/ubsan 是否抓到 UB/内存错误为准；
#   compiler-warn 仅作信息记录（模板生成的告警常常是无关噪声，不据此翻转判定）。
# 可重入：已写入有效 verification 的样本会被跳过；--maxtime 用于控制单命令时长以便分片续跑。
import os
import sys
import json
import time
import subprocess as _sp

OUT = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(OUT))          # CPP-Bible 仓库根
TOOLS = os.path.join(ROOT, "tools")
sys.path.insert(0, TOOLS)

import holdout_reveal_661 as hr

# ---- 运行时 monkeypatch（不改检测器源码） ----
hr.ATOMS = OUT
# WSL UTF-8 横幅净化：subprocess 以 errors=replace 读取，避免 UTF-16LE 横幅致解码异常。
def _wsl_safe(cmd, timeout=150):
    try:
        r = _sp.run(["wsl", "-e", "bash", "-lc", cmd], capture_output=True,
                    text=True, timeout=timeout, encoding="utf-8", errors="replace")
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:  # noqa
        return -1, f"wsl_error:{e}"
def _local_safe(cmd, timeout=120):
    try:
        r = _sp.run(cmd, capture_output=True, text=True, timeout=timeout,
                    encoding="utf-8", errors="replace")
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:  # noqa
        return -1, f"local_error:{e}"
hr._wsl = _wsl_safe
hr._local = _local_safe
# 设置 WSL UTF-8 环境变量，抑制代理横幅污染
os.environ["WSL_UTF8"] = "1"
os.environ["WSLENV"] = "WSL_UTF8/u"

KINDS = ["asan", "ubsan", "compiler-warn"]

def local_syntax(cpp_path):
    rc, out = _local_safe(["g++", "-std=c++17", "-Wall", "-Wextra", "-fsyntax-only", cpp_path])
    warns = [ln for ln in out.splitlines() if "warning:" in ln]
    return rc, warns, out.strip()

def _atomic_dump(obj, jpath):
    tmp = jpath + ".tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
    os.replace(tmp, jpath)

def process_one(sid):
    cpp = os.path.join(OUT, f"sample_{sid}.cpp")
    jpath = os.path.join(OUT, f"sample_{sid}.json")
    if not os.path.isfile(cpp) or not os.path.isfile(jpath):
        return None
    obj = json.load(open(jpath, encoding="utf-8"))
    # 已处理则跳过
    if obj.get("verification", {}).get("actual_verdict") in ("catch", "miss"):
        return obj.get("verification")
    rc, warns, syn_out = local_syntax(cpp)
    rec = {"syntax_rc": rc, "syntax_warnings": warns, "per_kind": {}, "reconcile": "n/a"}
    if rc != 0:
        rec.update(actual_verdict="eliminated", pooled=False, stage="syntax_fail",
                   reason=f"语法校验失败: {syn_out[:200]}")
        obj["verification"] = rec
        _atomic_dump(obj, jpath)
        return rec
    # 跑真实检测器
    kind_results = {}
    for k in KINDS:
        try:
            v, note = hr.detect(k, [f"sample_{sid}.cpp"])
        except Exception as e:  # noqa
            v, note = "unknown", f"detect_exception:{e}"
        kind_results[k] = {"verdict": v, "note": note[:300]}
    rec["per_kind"] = kind_results
    asan_v = kind_results["asan"]["verdict"]
    ubsan_v = kind_results["ubsan"]["verdict"]
    cwarn_v = kind_results["compiler-warn"]["verdict"]
    sanitizer_catch = (asan_v == "catch" or ubsan_v == "catch")
    actual = "catch" if sanitizer_catch else "miss"
    actual_det = [k for k in ("asan", "ubsan") if kind_results[k]["verdict"] == "catch"]
    # 判定有效性：sanitizer 必须可用（非 unknown），否则本次无法判定 -> 淘汰（记录原因）
    sanitizer_unavail = (asan_v == "unknown" or ubsan_v == "unknown")
    if sanitizer_unavail:
        rec.update(actual_verdict="eliminated", pooled=False, stage="sanitizer_unavailable",
                   reason=f"asan={asan_v} ubsan={ubsan_v}（检测器不可用，无法复现）",
                   compiler_warn=cwarn_v)
        obj["verification"] = rec
        _atomic_dump(obj, jpath)
        return rec
    # 更新标注为真实结果（卡允许合理更新标注）
    obj["expected_verdict"] = actual
    obj["expected_detectors"] = actual_det
    rec.update(actual_verdict=actual, actual_detectors=actual_det,
               compiler_warn=cwarn_v, pooled=True, stage="pass", reason="")
    # 真实性备注（保留原 notes，附检测细节）
    obj["verification"] = rec
    json.dump(obj, open(jpath, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    return rec

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--maxtime", type=int, default=480, help="单命令最长运行秒数")
    a = ap.parse_args()
    sids = [f"D{i:03d}" for i in range(1, 201)]
    start = time.time()
    stats = {"total": 0, "catch": 0, "miss": 0, "eliminated": 0, "syntax_fail": 0,
             "sanitizer_unavailable": 0, "by_type": {}}
    for sid in sids:
        rec = process_one(sid)
        if rec is None:
            continue
        stats["total"] += 1
        av = rec.get("actual_verdict")
        if av == "catch":
            stats["catch"] += 1
        elif av == "miss":
            stats["miss"] += 1
        else:
            stats["eliminated"] += 1
            if rec.get("stage") == "syntax_fail":
                stats["syntax_fail"] += 1
            elif rec.get("stage") == "sanitizer_unavailable":
                stats["sanitizer_unavailable"] += 1
        # 类型统计
        jp = os.path.join(OUT, f"sample_{sid}.json")
        obj = json.load(open(jp, encoding="utf-8"))
        dt = obj.get("defect_type", "?")
        stats["by_type"].setdefault(dt, {"catch": 0, "miss": 0, "elim": 0})
        if av == "catch":
            stats["by_type"][dt]["catch"] += 1
        elif av == "miss":
            stats["by_type"][dt]["miss"] += 1
        else:
            stats["by_type"][dt]["elim"] += 1
        if time.time() - start > a.maxtime:
            print(f"[maxtime] 已运行 {int(time.time()-start)}s，于 {sid} 处暂停；重跑可续。")
            break
    json.dump(stats, open(os.path.join(OUT, "validation_summary.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    print(json.dumps(stats, ensure_ascii=False))

if __name__ == "__main__":
    main()
