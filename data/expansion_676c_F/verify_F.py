#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""verify_F.py — 676c-F 编译验证（Task B）+ 检测器复现（Task C）。

Task B：本地 g++ -std=c++17 -fsyntax-only（语法）+ -O0 -g 完整编译。
Task C：monkeypatch hr.ATOMS = expansion_676c_F，对每样本真实调用 detect()：
  - catch 样本（alignment 未对齐解引用 / shift 负移位·超宽 / register / 位域越界）→ 跑对应检测器
  - miss 样本（endianness/volatile/interrupt/setjmp/inline-asm/packed 等）→ 跑 compiler-warn
调和：catch 一致或通过（expected miss 实测 catch 则改标）；expected catch 但 miss/unknown → 淘汰。
环境：所有 WSL 调用前设 WSL_UTF8=1 / WSLENV（避免横幅污染 stderr 致 decode 异常→假 miss）。
"""
import os, sys, json, time, tempfile, shutil, importlib.util, subprocess

# —— 环境偏差规避（memory 记录）：WSL 横幅污染 ——
os.environ["WSL_UTF8"] = "1"
os.environ["WSLENV"] = "WSL_UTF8/u"

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLS = os.path.join(REPO, "tools")
EXP = os.path.abspath(os.path.dirname(os.path.abspath(__file__)))

spec = importlib.util.spec_from_file_location("hr", os.path.join(TOOLS, "holdout_reveal_661.py"))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
detect = mod.detect
mod.ATOMS = EXP  # 直接读扩样目录

RESULTS = os.path.join(EXP, "verify_results.json")


def local(cmd, timeout=120):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:  # noqa
        return -1, f"local_error:{e}"


def verify_one(idx):
    sid = f"F{idx:03d}"
    jp = os.path.join(EXP, f"sample_{sid}.json")
    rec = {"id": sid, "stage": "init"}
    if not os.path.isfile(jp):
        rec.update(stage="missing", pooled=False, reason="json missing"); return rec
    meta = json.load(open(jp, encoding="utf-8"))
    fn = f"sample_{sid}.cpp"
    dkind = (meta.get("expected_detectors") or ["compiler-warn"])[0]
    rec["defect_type"] = meta["defect_type"]
    rec["detector_kind"] = dkind
    rec["expected_verdict"] = meta.get("expected_verdict")

    t0 = time.time()
    # ---- Task B 语法 ----
    rc, out = local(["g++", "-std=c++17", "-fsyntax-only", os.path.join(EXP, fn)])
    if rc != 0:
        rec.update(stage="compile_fail", pooled=False, reason=f"syntax: {out.strip()[:150]}")
        _write(meta, rec, sid); return rec
    # ---- Task B 完整编译（本地）----
    tmp = tempfile.mkdtemp()
    try:
        exe = os.path.join(tmp, "t.exe")
        rc, out = local(["g++", "-std=c++17", "-O0", "-g", os.path.join(EXP, fn), "-o", exe])
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    if rc != 0:
        rec.update(stage="compile_fail", pooled=False, reason=f"full_compile: {out.strip()[:150]}")
        _write(meta, rec, sid); return rec
    rec["full_compile"] = "ok"

    # ---- Task C detect() ----
    detectors = list(meta.get("expected_detectors") or [dkind])
    verdicts = {}
    for k in detectors:
        try:
            v, note = detect(k, [fn])
        except Exception as e:  # noqa
            v, note = "unknown", f"detect_exception:{e}"
        verdicts[k] = (v, note[:200])
    rec["verdicts"] = {k: v for k, (v, _n) in verdicts.items()}
    # 合并（unknown 视为中性，不拖垮盲点样本）
    if any(v == "catch" for v, _ in verdicts.values()):
        combined = "catch"
    elif any(v == "miss" for v, _ in verdicts.values()):
        combined = "miss"
    else:
        combined = "unknown"
    rec["detector_verdict"] = combined

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
    _write(meta, rec, sid)
    return rec


def _write(meta, rec, sid):
    meta["verification"] = {
        "syntax_fail": rec.get("stage") == "compile_fail" and "syntax" in (rec.get("reason") or ""),
        "full_compile": rec.get("full_compile"),
        "detector_kind": rec.get("detector_kind"),
        "verdicts": rec.get("verdicts"),
        "detector_verdict": rec.get("detector_verdict"),
        "reconcile": rec.get("reconcile"),
        "pooled": rec.get("pooled"),
        "stage": rec.get("stage"),
        "reason": rec.get("reason", ""),
    }
    json.dump(meta, open(os.path.join(EXP, f"sample_{sid}.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)


def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--start", type=int, default=1)
    ap.add_argument("--end", type=int, default=200)
    a = ap.parse_args()
    results = json.load(open(RESULTS, encoding="utf-8")) if os.path.isfile(RESULTS) else {}
    passed = failed = 0
    for idx in range(a.start, a.end + 1):
        rec = verify_one(idx)
        results[rec["id"]] = rec
        if rec.get("pooled"):
            passed += 1
        else:
            failed += 1
        print(f"  {rec['id']} pool={rec.get('pooled')} stage={rec.get('stage')} "
              f"det={rec.get('detector_verdict')} kind={rec.get('detector_kind')} "
              f"type={rec.get('defect_type')}")
    json.dump(results, open(RESULTS, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n[chunk {a.start}-{a.end}] pass_candidate={passed} fail={failed}")


if __name__ == "__main__":
    main()
