#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阶段3 P0: 把 DRIFT 工件重生成对齐 canonical gcc-15.3.0 + -masm=intel
=====================================================================
严格复刻 _verify_asm_evidence.py 的 "fresh 参考" 生成命令：
  - GPP_S (stored .s):  g++ <flags> -S [-masm=intel] <cpp> -o <name>.s
  - OBJDUMP (stored .o): g++ <flags> -c <cpp> -o <name>.o
重生成后存储工件 == 验证器 fresh 参考 → 下次抽查即 MATCH。
真实编译器产物，红线允许；工件 git 跟踪，可逆。
"""
import os, re, subprocess, json, glob, importlib.util

# 复用验证器的 flags_for / STORED_ALIAS / GPP / AT&T 检测语义（不触发 main）
spec = importlib.util.spec_from_file_location("V", os.path.join(os.path.dirname(os.path.abspath(__file__)), "_verify_asm_evidence.py"))
V = importlib.util.module_from_spec(spec); spec.loader.exec_module(V)

GPP = V.GPP
DEMO = V.DEMO

def stored_path(name: str):
    if name in V.STORED_ALIAS:
        return os.path.join(DEMO, V.STORED_ALIAS[name])
    s = os.path.join(DEMO, name + ".s")
    if os.path.exists(s): return s
    o = os.path.join(DEMO, name + ".o")
    if os.path.exists(o): return o
    return None

def att_of(path: str) -> bool:
    t = open(path, encoding="utf-8", errors="replace").read()
    return bool(re.search(r'%(rax|rcx|rdx|rbx|rsp|rbp|rsi|rdi|r8|r9|'
                          r'eax|ebx|ecx|edx|esi|edi)\b', t)) or \
           bool(re.search(r'\b(movl|addq|subq|xorl|testq|cmpq|leaq)\b', t))

def main():
    data = json.load(open(os.path.join(DEMO, "_evidence_spotcheck_v4.json"), encoding="utf-8"))
    drift = [r["name"] for r in data["results"] if r["status"] == "DRIFT"]
    print(f"=== P0 重生成 {len(drift)} 个 DRIFT 工件 (canonical gcc-15.3.0) ===\n")
    ok, fail = [], []
    for name in drift:
        cpp = os.path.join(DEMO, name + ".cpp")
        p = stored_path(name)
        if not cpp or not p:
            print(f"[SKIP] {name}: cpp={bool(cpp)} stored={p}"); fail.append(name); continue
        flags = V.flags_for(name)
        ext = p.rsplit(".", 1)[1]
        if ext == "s":
            att = att_of(p)
            sflags = ["-S"] + (["-masm=intel"] if not att else []) + [cpp]
            cmd = [GPP] + flags + sflags + ["-o", p]
        else:  # .o
            cmd = [GPP] + flags + ["-c", cpp, "-o", p]
        before = os.path.getsize(p)
        r = subprocess.run(cmd, capture_output=True, text=True)
        if r.returncode != 0:
            print(f"[FAIL] {name} (rc={r.returncode}): {(r.stderr.strip().splitlines() or ['?'])[0][:120]}")
            fail.append(name); continue
        # .s 文本件统一 LF（规避 CRLF 伪 diff，与 g++ 原生输出一致）
        if ext == "s":
            b = open(p, "rb").read()
            if b"\r\n" in b:
                open(p, "wb").write(b.replace(b"\r\n", b"\n"))
        after = os.path.getsize(p)
        print(f"[OK]   {name:<32} {ext}  flags={' '.join(flags)}  {before}B->{after}B")
        ok.append(name)
    print(f"\n重生成完成: OK={len(ok)} FAIL={len(fail)}")
    if fail:
        print("FAIL 列表:", fail)

if __name__ == "__main__":
    main()
