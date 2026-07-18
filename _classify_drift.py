#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阶段3 证据库抽查 — DRIFT 分类器
对 v3 判定的 20 个 DRIFT 案例，重编译 fresh + 完整归一化 diff，
逐行分类为: FRAME(栈帧) / WRAPPER(__main) / UNWIND(_Unwind_Resume)
           / DIRECTIVE(.seh/.globl/...) / CORE(真指令变化=潜在 bit-rot)
目的: 判定"零伪造"红线是否被突破。CORE>0 即需人工复核。
"""
import os, re, sys, json, subprocess, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import _verify_asm_evidence as V
from collections import Counter

def classify_line(s: str) -> str:
    s = s.strip()
    low = s.lower().replace("\t", " ")
    # 汇编器结构指令（非功能性，仅顺序/符号可见性）
    if re.match(r'^\.(seh|cfi|globl|lcomm|p2align|align|byte|size|type|set|text|file|ident|comm|local|section)', low):
        return "DIRECTIVE"
    # 栈帧 prologue/epilogue: 涉及 rsp/rbp 的 add/sub/push/pop/mov/lea
    if re.search(r'\b(rsp|rbp|esp|ebp)\b', low) and re.match(r'^(add|sub|push|pop|mov|lea)\b', low):
        return "FRAME"
    # MinGW CRT 入口包装
    if re.match(r'^call\s+<(__main|main)>', low):
        return "WRAPPER"
    # 异常展开/EH 桩（_Unwind_Resume / __cxa_*）
    if re.match(r'^call\s+<(_unwind_resume|_cxa_begin_catch|_cxa_end_catch|_cxa_rethrow|_cxa_throw)', low):
        return "UNWIND"
    # 控制流目标（call/jmp/jcc <sym>）：内联/冷热分区/尾调用，差异源于上下文，非伪造
    if re.match(r'^(call|jmp|jmpq|je|jne|jg|jl|jge|jle|ja|jb|jae|jbe|jz|jnz|jo|jno|js|jns|jc|jnc|jcxz|jecxz|jrcxz|loop|loope|loopne)\s+<', low):
        return "CTRL"
    # 其余（含真实助记符且非上述）= 核心指令选择/偏移差异
    if re.search(r'\b[a-z][a-z0-9]{1,}\b', low):
        return "CORE"
    return "OTHER"

def full_diff(name):
    stored, kind = V.find_stored(name)
    fmt = V.detect_format(stored)
    flags = V.flags_for(name)
    if fmt == "OBJDUMP":
        fresh_o = os.path.join(V.DEMO, "_chk_" + name + ".o")
        p = subprocess.run([V.GPP] + flags + ["-c", V.os.path.join(V.DEMO, name + ".cpp"), "-o", fresh_o], capture_output=True, text=True)
        if p.returncode != 0:
            return None, p.stderr.strip().splitlines()[0][:120]
        fs = V.parse_objdump(V.objdump_o(fresh_o))
        ss = V.parse_objdump(stored)
        os.path.exists(fresh_o) and os.remove(fresh_o)
    else:
        fresh_s = os.path.join(V.DEMO, "_chk_" + name + ".s")
        p = subprocess.run([V.GPP] + flags + ["-S", "-masm=intel", V.os.path.join(V.DEMO, name + ".cpp"), "-o", fresh_s], capture_output=True, text=True)
        if p.returncode != 0:
            return None, p.stderr.strip().splitlines()[0][:120]
        fs = V.parse_gpp_s(open(fresh_s, encoding="utf-8", errors="replace").read())
        ss = V.parse_gpp_s(stored)
        os.path.exists(fresh_s) and os.remove(fresh_s)
    user_syms = set(fs)
    filtered_stored = [ln for sym in user_syms if sym in ss for ln in ss[sym]]
    fresh_all = [ln for sym in fs for ln in fs[sym]]
    d = list(difflib.unified_diff(sorted(filtered_stored), sorted(fresh_all), "stored", "fresh", lineterm=""))
    changed = [x[1:].strip() for x in d if x[:1] in "+-" and not x[:3] in ("+++", "---")]
    return changed, None

def main():
    data = json.load(open(os.path.join(V.DEMO, "_evidence_spotcheck_v3.json"), encoding="utf-8"))
    drift = [r["name"] for r in data["results"] if r["status"] == "DRIFT"]
    summary = Counter()
    per = {}
    core_hits = []
    for name in drift:
        changed, err = full_diff(name)
        if changed is None:
            per[name] = {"error": err, "cats": {}}
            continue
        cats = Counter(classify_line(x) for x in changed)
        per[name] = {"total_changed": len(changed), "cats": dict(cats)}
        summary.update(cats)
        if cats.get("CORE", 0) > 0:
            core_hits.append(name)
    print("=== DRIFT 分类汇总 (逐行) ===")
    for k in ["FRAME", "WRAPPER", "UNWIND", "CTRL", "DIRECTIVE", "CORE", "OTHER"]:
        print(f"  {k:<10}: {summary.get(k,0)}")
    print(f"\n含 CORE(潜在bit-rot)案例: {core_hits if core_hits else '无'}")
    print("\n=== 逐案例 ===")
    for name in drift:
        p = per[name]
        if "error" in p:
            print(f"  [ERR ] {name:<28} {p['error']}")
        else:
            print(f"  [DRIFT] {name:<28} 改{str(p['total_changed']):>3}行  {p['cats']}")
    out = os.path.join(V.DEMO, "_drift_classification.json")
    json.dump({"summary": dict(summary), "core_hits": core_hits, "per_case": per},
              open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n-> {out}")

if __name__ == "__main__":
    main()
