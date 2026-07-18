#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
阶段3 证据库抽查验证器 v3 (符号作用域比对 + 完整归一化)
=====================================================
根因修正：
  - 大 STL 例子存储件是整 .exe 反汇编（含链接库码），须按"用户符号作用域"比对，
    滤掉 libstdc++/CRT 库码，只比用户函数体。
  - 剥 call/jmp 操作数中的 +0xNN 偏移、GCC 内部标号号（.LFB/.LLSDA/.LHOTB...）。
  - 丢弃 .text 节内对齐填充字节（纯 00 行，无助记符）。
  - ch87_bit_test_popcnt 等需 -mpopcnt 特例标志。
判定: MATCH / DRIFT / COMPILE_FAIL / NO_ARTIFACT / FORMAT_SKIP
"""
import os, re, subprocess, json, glob, difflib
from collections import Counter

GPP = "C:/Qt/Tools/mingw1530_64/bin/g++.EXE"
OBJDUMP = "C:/Qt/Tools/mingw1530_64/bin/objdump.exe"
DEMO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "_asm_demo"))

CALL_RE = (r'\b(call|callq|jmp|jmpq|je|jne|jg|jl|jge|jle|ja|jb|jae|jbe|'
           r'jz|jnz|jo|jno|js|jns|jc|jnc|jcxz|jecxz|jrcxz|loop|loope|loopne)\s+'
           r'[0-9a-fA-F]+\s+(<[^>]+>)')

def flags_for(name: str) -> list:
    base = ["-std=c++26", "-O2"]
    low = name.lower()
    if "_o0" in low or low.endswith("o0"):   base = ["-std=c++26", "-O0"]
    elif "_o1" in low:                        base = ["-std=c++26", "-O1"]
    elif "_os" in low:                        base = ["-std=c++26", "-Os"]
    if "ch09" in low or "contract" in low:    base += ["-fcontracts"]
    if "popcnt" in low:                       base += ["-mpopcnt"]
    return base

def detect_format(stored: str) -> str:
    if "file format" in stored or "Disassembly of section" in stored:
        return "OBJDUMP"
    if re.search(r'^\s*\.(text|globl|p2align|seh_|file)\b', stored, re.M):
        return "GPP_S"
    return "UNKNOWN"

# -------- OBJDUMP 解析：按 .text 节内符号切分函数体 --------
def parse_objdump(t: str) -> dict:
    syms, cur, in_code = {}, None, False
    for line in t.splitlines():
        s = line.rstrip()
        if not s.strip():
            continue
        msec = re.match(r'^\s*Disassembly of section\s+(\.\S+):', s)
        if msec:
            in_code = msec.group(1).startswith('.text'); cur = None; continue
        if not in_code:
            continue
        if re.match(r'^[^\s].*:\s*file format', s):   continue
        if re.match(r'^\s*\.file\s', s):               continue
        if re.match(r'^\s*\.ident\s', s):              continue
        msym = re.match(r'^\s*[0-9a-fA-F]*\s*<(.+?)>:', s)
        if msym:
            cur = msym.group(1); syms.setdefault(cur, []); continue
        s2 = re.sub(r'^\s*[0-9a-fA-F]{1,16}:', '', s)
        s2 = re.sub(CALL_RE, r'\1 \2', s2)             # 去 call 偏移,留符号
        s2 = re.sub(r'^(\s*[0-9a-fA-F]{2}(\s+[0-9a-fA-F]{2})*\s+)', '', s2)  # 去整列操作码字节
        s2 = re.sub(r'\+0x[0-9a-fA-F]+', '', s2)       # 去 <sym+0xNN>
        s2 = re.sub(r'#.*$', '', s2).strip()
        s2 = re.sub(r'\.L([A-Za-z]*)\d+', r'.L\1', s2) # 去 GCC 标号号
        if not s2:
            continue
        if s2.startswith('<'):
            continue
        if s2.startswith('.'):                          # .seh_/.cfi_/.p2align 等指令结构
            if cur is not None: syms[cur].append(s2)
            continue
        if re.search(r'\b[a-z][a-z0-9]{1,}\b', s2):     # 含助记符=真指令
            if cur is not None: syms[cur].append(s2)
        # 其余(纯 00 填充字节)丢弃
    return syms

# -------- GPP -S 解析：.text 节内标签切分 --------
def parse_gpp_s(t: str) -> dict:
    syms, cur, in_code = {}, None, True
    SKIP = ('.p2align', '.globl', '.def', '.set', '.type', '.size', '.section',
            '.ident', '.file', '.comm', '.local', '.align', '.balign')
    for line in t.splitlines():
        s = line.rstrip()
        if not s.strip():
            continue
        msec = re.match(r'^\s*\.section\s+(\.\S+)', s)
        if msec and not msec.group(1).startswith('.text'):
            in_code = False; cur = None; continue
        if re.match(r'^\s*\.text\b', s):
            in_code = True; continue
        if not in_code:
            continue
        if re.match(r'^\s*\.file\s', s) or re.match(r'^\s*\.ident\s', s):
            continue
        st = s.strip()
        mlbl = re.match(r'^\s*(\.?[A-Za-z_][\w$.]*):', st)
        if mlbl and not st.startswith(SKIP):
            cur = mlbl.group(1); syms.setdefault(cur, []); continue
        s2 = re.sub(r'#.*$', '', st).strip()
        s2 = re.sub(r'\.L([A-Za-z]*)\d+', r'.L\1', s2)
        if not s2:
            continue
        if re.search(r'\b[a-z][a-z0-9]{1,}\b', s2) or s2.startswith('.'):
            if cur is not None: syms[cur].append(s2)
    return syms

def objdump_o(o_path: str) -> str:
    return subprocess.run([OBJDUMP, "-d", "-M", "intel", "-C", o_path],
                          capture_output=True, text=True).stdout

def find_stored(name: str):
    s_file = os.path.join(DEMO, name + ".s")
    if os.path.exists(s_file):
        return open(s_file, encoding="utf-8", errors="replace").read(), "stored_s"
    o_file = os.path.join(DEMO, name + ".o")
    if os.path.exists(o_file):
        return objdump_o(o_file), "stored_o"
    return None, "none"

def main():
    cpp_files = sorted(glob.glob(os.path.join(DEMO, "*.cpp")))
    results = []
    for cpp in cpp_files:
        name = os.path.splitext(os.path.basename(cpp))[0]
        if name.startswith("_pilot") or name.startswith("_chk"):
            continue
        stored, kind = find_stored(name)
        if stored is None:
            results.append({"name": name, "status": "NO_ARTIFACT", "detail": "无配对 .s/.o"})
            continue
        fmt = detect_format(stored)
        if fmt == "UNKNOWN":
            results.append({"name": name, "status": "FORMAT_SKIP", "detail": "非标准工件"})
            continue
        flags = flags_for(name)
        rc = 0; err = ""
        if fmt == "OBJDUMP":
            fresh_o = os.path.join(DEMO, "_chk_" + name + ".o")
            p = subprocess.run([GPP] + flags + ["-c", cpp, "-o", fresh_o], capture_output=True, text=True)
            rc, err = p.returncode, p.stderr
            if rc == 0:
                fresh_syms = parse_objdump(objdump_o(fresh_o))
                stored_syms = parse_objdump(stored)
            os.path.exists(fresh_o) and os.remove(fresh_o)
        else:
            # AT&T vs Intel 语法自适应：若存储件为 AT&T(含 %(reg) 或 movl/addq 后缀)，
            # 则 fresh 也用 AT&T 编译，保证同种语法比对，避免伪 DRIFT。
            att = bool(re.search(r'%(rax|rcx|rdx|rbx|rsp|rbp|rsi|rdi|r8|r9|'
                                  r'eax|ebx|ecx|edx|esi|edi)\b', stored)) or \
                  bool(re.search(r'\b(movl|addq|subq|xorl|testq|cmpq|leaq)\b', stored))
            sflags = ["-S"] + (["-masm=intel"] if not att else []) + [cpp]
            fresh_s = os.path.join(DEMO, "_chk_" + name + ".s")
            p = subprocess.run([GPP] + flags + sflags + ["-o", fresh_s], capture_output=True, text=True)
            rc, err = p.returncode, p.stderr
            if rc == 0:
                fresh_syms = parse_gpp_s(open(fresh_s, encoding="utf-8", errors="replace").read())
                stored_syms = parse_gpp_s(stored)
            os.path.exists(fresh_s) and os.remove(fresh_s)
        if rc != 0:
            results.append({"name": name, "status": "COMPILE_FAIL", "fmt": fmt,
                            "flags": " ".join(flags),
                            "detail": (err.strip().splitlines() or ["?"])[0][:130]})
            continue
        # 符号作用域比对：只比 fresh 中出现的用户符号
        user_syms = set(fresh_syms)
        filtered_stored = [ln for sym in user_syms if sym in stored_syms for ln in stored_syms[sym]]
        fresh_all = [ln for sym in fresh_syms for ln in fresh_syms[sym]]
        if sorted(filtered_stored) == sorted(fresh_all):
            results.append({"name": name, "status": "MATCH", "fmt": fmt,
                            "detail": f"用户符号 {len(user_syms)} 个, 规范化代码零差异 ({kind})"})
        else:
            d = list(difflib.unified_diff(sorted(filtered_stored), sorted(fresh_all),
                                          "stored", "fresh", lineterm=""))
            ndiff = sum(1 for x in d if x[:1] in "+-" and not x[:3] in ("+++", "---"))
            results.append({"name": name, "status": "DRIFT", "fmt": fmt,
                            "flags": " ".join(flags),
                            "detail": f"真差异 {ndiff} 处; 示例: " + " | ".join(d[2:7])[:150]})
    cnt = Counter(r["status"] for r in results)
    print("=== 证据库抽查汇总 v3 (mingw1530 GCC 15.3.0, 符号作用域比对) ===")
    print(f"总检查 {len(results)} | MATCH={cnt['MATCH']} DRIFT={cnt['DRIFT']} "
          f"COMPILE_FAIL={cnt['COMPILE_FAIL']} NO_ARTIFACT={cnt['NO_ARTIFACT']} FORMAT_SKIP={cnt['FORMAT_SKIP']}")
    print()
    for r in results:
        print(f"[{r['status']:<11}] {r['name']:<32} {r.get('fmt',''):<9} {r['detail'][:100]}")
    out = os.path.join(DEMO, "_evidence_spotcheck_v3.json")
    json.dump({"toolchain": "mingw1530 GCC 15.3.0", "summary": dict(cnt), "results": results},
              open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"\n详细 JSON -> {out}")

if __name__ == "__main__":
    main()
