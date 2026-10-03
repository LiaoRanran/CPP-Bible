#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""verify_676cC.py — 676c 扩样-C 验证器（Task B + C + 优化敏感性）。

Task B：本机 g++ -std=c++17 -fsyntax-only（语法）+ -O0 -g 完整编译（跨文件一起编）。
  - 跨 TU 强多重定义样本"完整编译失败"是预期行为（linker 检测器据此抓），不淘汰。
  - 其余类型完整编译失败 = 真实编译错误 -> 淘汰。
Task C：调用 detect() 真实跑检测器（asan/ubsan 经 WSL；compiler-warn/linker 本机）。
  - miss 样本额外跑 compiler-warn，确认无检测器可抓（真盲区）。
  - optimization_dependent：额外做 O0/O2 单档位检测 + 本机 O0/O2 输出比对，验证优化敏感性；
    若实测 O0/O2 无差异则诚实改标 optimization_sensitivity="none"。
调和：catch==expected -> pass；expected miss 但实测 catch -> 更新标注为 catch（合理）；
     expected catch 但实测 miss/unknown -> 淘汰（缺陷不实/检测器不覆盖）。
"""
import os, sys, json, time, shutil, tempfile, importlib.util

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLS = os.path.join(REPO, "tools")
ATOMS = os.path.join(REPO, "Examples", "atoms")
EXP = os.path.join(REPO, "data", "expansion_676cC")
RESULTS = os.path.join(EXP, "verify_results.json")

spec = importlib.util.spec_from_file_location("hr", os.path.join(TOOLS, "holdout_reveal_661.py"))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
detect = mod.detect

import subprocess

def local_syntax(files):
    fails = []
    for f in files:
        p = os.path.join(EXP, f)
        rc, out = _local(["g++", "-std=c++17", "-fsyntax-only", p])
        if rc != 0:
            fails.append((f, out.strip()[:150]))
    return fails

def local_full_compile(files):
    tmp = tempfile.mkdtemp()
    try:
        copies = []
        for f in files:
            d = os.path.join(tmp, os.path.basename(f)); shutil.copy2(os.path.join(EXP, f), d); copies.append(d)
        exe = os.path.join(tmp, "t.exe")
        rc, out = _local(["g++", "-std=c++17", "-O0", "-g"] + copies + ["-o", exe])
        return rc, out.strip()[:200]
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

def _local(cmd, timeout=120):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return -1, f"local_error:{e}"

def local_run(files, opt):
    """本机无 sanitizer 编译运行，返回 stdout（用于优化前后输出比对）。"""
    tmp = tempfile.mkdtemp()
    try:
        copies = []
        for f in files:
            d = os.path.join(tmp, os.path.basename(f)); shutil.copy2(os.path.join(EXP, f), d); copies.append(d)
        exe = os.path.join(tmp, "t.exe")
        rc, _ = _local(["g++", "-std=c++17", opt, "-O0"] + copies + ["-o", exe]) if False else _local(["g++", "-std=c++17", opt] + copies + ["-o", exe])
        if rc != 0:
            return f"<compile_fail rc={rc}>"
        r = _local([exe])
        return (r[1] or "").strip()
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

def wsan_level(kind, files, opt):
    """单档位 WSL sanitizer 检测（用于优化敏感性）。"""
    srcs = [os.path.join(EXP, f) for f in files]
    tmp = tempfile.mkdtemp()
    copies = []
    for s in srcs:
        d = os.path.join(tmp, os.path.basename(s)); shutil.copy2(s, d); copies.append(d)
    w = [mod._to_wsl(c) for c in copies]; exe = "/tmp/rv_lvl"
    c = f"g++ -std=c++17 {opt} -g -fsanitize={mod.SAN[kind]} -pthread {' '.join(w)} -o {exe}"
    rc, out = mod._wsl(c)
    if rc != 0:
        shutil.rmtree(tmp, ignore_errors=True); return "compile_fail"
    rc, out = mod._wsl(mod._setarch_prefix() + exe, timeout=120); low = out.lower()
    if kind == "ubsan":
        hit = "runtime error" in out
    else:
        hit = ("AddressSanitizer" in out or "LeakSanitizer" in out or "detected memory leaks" in low or "double-free" in low)
    shutil.rmtree(tmp, ignore_errors=True)
    return "catch" if hit else "miss"


def verify_one(idx):
    n3 = f"sample_{idx:03d}"
    jp = os.path.join(EXP, n3 + ".json")
    rec = {"id": n3, "stage": "init"}
    if not os.path.isfile(jp):
        rec.update(stage="missing", pooled=False, reason="json missing"); return rec
    meta = json.load(open(jp, encoding="utf-8"))
    files = meta.get("source_files") or [n3 + ".cpp"]
    dkind = (meta.get("expected_detectors") or ["asan"])[0]
    rec["defect_type"] = meta["defect_type"]
    rec["detector_kind"] = dkind

    t0 = time.time()
    # --- Task B 语法 + 完整编译 ---
    syn_fail = local_syntax(files)
    rec["syntax_fail"] = syn_fail
    if syn_fail:
        rec.update(stage="compile_fail", pooled=False, reason=f"syntax error: {syn_fail[0][1]}")
        _write_meta(meta, rec, n3); return rec
    rc, fout = local_full_compile(files)
    rec["full_compile_rc"] = rc
    is_cross_strong = (meta["defect_type"] == "cross_tu_ub" and "linker" in meta.get("expected_detectors", []))
    if rc != 0 and not is_cross_strong:
        rec.update(stage="compile_fail", pooled=False, reason=f"compile/link fail: {fout}")
        _write_meta(meta, rec, n3); return rec
    rec["full_compile_note"] = "link-fail(expected ODR)" if (rc != 0 and is_cross_strong) else "ok"

    # --- Task C detect() ---
    # miss 样本额外跑 compiler-warn 以确认真盲区
    detectors = list(meta.get("expected_detectors") or [dkind])
    if meta.get("expected_verdict") == "miss" and "compiler-warn" not in detectors:
        detectors.append("compiler-warn")
    verdicts = {}
    for k in detectors:
        tmp_files = [os.path.basename(f) for f in files]
        written = []
        try:
            for f in files:
                p = os.path.join(ATOMS, os.path.basename(f))
                shutil.copy2(os.path.join(EXP, f), p); written.append(p)
            v, note = detect(k, tmp_files)
        except Exception as e:
            v, note = "unknown", f"detect_exception:{e}"
        finally:
            for p in written:
                try: os.remove(p)
                except OSError: pass
        verdicts[k] = (v, note[:200])
    rec["verdicts"] = {k: v for k, (v, _) in verdicts.items()}
    # 合并：任一 catch -> catch；全 miss -> miss；否则 unknown
    if any(v == "catch" for v, _ in verdicts.values()):
        combined = "catch"
    elif all(v == "miss" for v, _ in verdicts.values()):
        combined = "miss"
    else:
        combined = "unknown"
    rec["detector_verdict"] = combined

    # --- optimization_dependent 优化敏感性 ---
    if meta["defect_type"] == "optimization_dependent":
        o0 = wsan_level(dkind, [os.path.basename(f) for f in files], "-O0")
        o2 = wsan_level(dkind, [os.path.basename(f) for f in files], "-O2")
        out0 = local_run(files, "-O0"); out2 = local_run(files, "-O2")
        rec["opt_O0_detector"] = o0; rec["opt_O2_detector"] = o2
        rec["opt_output_differs"] = (out0 != out2)
        # 诚实改标：若检测器两档均无报告 且 输出也无差异 -> 非优化敏感
        if o0 == "miss" and o2 == "miss" and out0 == out2:
            meta["optimization_sensitivity"] = "none（实测 O0/O2 无差异，非优化敏感 UB）"
            rec["opt_relabeled"] = True
        rec["opt_note"] = f"detector O0={o0} O2={o2}; output_diff={rec['opt_output_differs']}"
        # optimization_dependent：只要某一档位能被检测器抓到，即视为真实可检缺陷
        # （优化敏感性的本质：同一 UB 在不同 -O 下检测器表现不同）。聚合 detect()
        # 用两档 OR，理论上已覆盖；此处兜底，避免 WSL 单次抖动误判为 miss。
        if combined != "catch" and (o0 == "catch" or o2 == "catch"):
            combined = "catch"; rec["opt_real_catch"] = True

    expected = meta.get("expected_verdict")
    if combined == "catch":
        if expected == "miss":
            meta["expected_verdict"] = "catch"; rec["reconcile"] = "updated_to_catch"
        else:
            rec["reconcile"] = "consistent"
        rec["pooled"] = True; rec["stage"] = "pass"
    elif combined == "miss":
        if expected == "miss":
            rec["reconcile"] = "consistent"; rec["pooled"] = True; rec["stage"] = "pass"
        else:
            rec["reconcile"] = "inconsistent_catch_expected"; rec["pooled"] = False
            rec["stage"] = "detector_fail"; rec["reason"] = "expected catch but detector miss"
    else:
        rec["reconcile"] = "detector_unknown"; rec["pooled"] = False
        rec["stage"] = "detector_unknown"; rec["reason"] = "detector unavailable/error"
    rec["elapsed_s"] = round(time.time() - t0, 2)
    _write_meta(meta, rec, n3)
    return rec


def _write_meta(meta, rec, n3):
    meta["verification"] = {
        "syntax_fail": rec.get("syntax_fail"),
        "full_compile": rec.get("full_compile_note"),
        "detector_kind": rec.get("detector_kind"),
        "verdicts": rec.get("verdicts"),
        "detector_verdict": rec.get("detector_verdict"),
        "opt_O0_detector": rec.get("opt_O0_detector"),
        "opt_O2_detector": rec.get("opt_O2_detector"),
        "opt_output_differs": rec.get("opt_output_differs"),
        "reconcile": rec.get("reconcile"),
        "pooled": rec.get("pooled"),
        "stage": rec.get("stage"),
        "reason": rec.get("reason", ""),
    }
    json.dump(meta, open(os.path.join(EXP, n3 + ".json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)


def main():
    import argparse
    ap = argparse.ArgumentParser(); ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--end", type=int, default=200); a = ap.parse_args()
    results = json.load(open(RESULTS, encoding="utf-8")) if os.path.isfile(RESULTS) else {}
    passed = failed = 0
    for idx in range(a.start, a.end + 1):
        rec = verify_one(idx); results[rec["id"]] = rec
        if rec.get("pooled"):
            passed += 1
        else:
            failed += 1
        print(f"  {rec['id']} pooled={rec.get('pooled')} stage={rec.get('stage')} "
              f"det={rec.get('detector_verdict')} kind={rec.get('detector_kind')} "
              f"type={rec.get('defect_type')}")
    json.dump(results, open(RESULTS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n[chunk {a.start}-{a.end}] pass_candidate={passed} fail={failed}")


if __name__ == "__main__":
    main()
