#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Examples/*.asm 复现性 spot-check（对抗式审计，非零确认）。

目标：对证据库中每个存储的 .asm（来自 `g++ -S -masm=intel`，MinGW 生成），
用本地 MinGW GCC 15.3.0 以「可推断的标准约定 + 书内记载命令」重新编译其源，
归一化后在「用户符号作用域」比较，判定 MATCH / DRIFT / COMPILE_FAIL / NO_SOURCE。

为什么这是本地门禁而非 CI ubuntu：
  证据库是 MinGW 生成的（.seh_proc / .def / __main / x86_64-posix-seh），
  调用约定与 ubuntu gcc-15（CFI / AT&T / SysV）不同，ubuntu 无法复现 MinGW asm。
  故本工具在 Windows + MinGW 下运行，作为本地对抗式审计（pre-push 自检）。

归一化（对齐 skill 方法论）：
  - 丢弃 .file / .ident / .section(.rdata 等)
  - 仅保留 .text 代码段
  - 去行首地址列、去偏移（+0xNN）、去 GCC 内部标号数字（.LFB4103 -> .LFB）
  - 用户符号作用域比较：仅比双方都出现的用户符号体（忽略库代码重排）

用法:
  python tools/asm_repro_spotcheck.py --gpp <g++.exe> --examples Examples [--out report.json] [--only 15.3.0|13.1.0|unmarked|all] [--name-substr X]
"""
import os, re, sys, subprocess, json, glob, difflib, argparse
from collections import Counter

CALL_RE = (r'\b(call|callq|jmp|jmpq|je|jne|jg|jl|jge|jle|ja|jb|jae|jbe|'
           r'jz|jnz|jo|jno|js|jns|jc|jnc|jcxz|jecxz|jrcxz|loop|loope|loopne)\s+'
           r'[0-9a-fA-F]+\s+(<[^>]+>)')


def flags_for(name):
    """可推断的标准约定：c++23，默认 -O2；_O0->O0，_O1->O1，_OS->Os；
    ch14 特例（-g -O0，书内记载含调试信息）；ch47 vtable 特例（-O1 -fno-inline，
    书 D4.3 记载 `g++ -std=c++23 -O1 -fno-inline`，否则 -O2 会内联析构函数
    导致 vtable 符号消失，误报 DRIFT）。

    文件级标志覆盖约定：
      - 文件名含 _O0/_O1/_OS 时，对应优化等级优先；
      - ch14* → -g -O0（调试信息示例）；
      - _ch47_d4_vtable → -O1 -fno-inline（书 D4.3 显记）。
    """
    low = name.lower()
    base = ["-std=c++23", "-O2"]
    if "_o0" in low or low.endswith("o0"):
        base = ["-std=c++23", "-O0"]
    elif "_o1" in low:
        base = ["-std=c++23", "-O1"]
    elif "_os" in low:
        base = ["-std=c++23", "-Os"]
    if "ch14" in low:
        base = ["-std=c++23", "-g", "-O0"]
    if "_ch47_d4_vtable" in low:
        base = ["-std=c++23", "-O1", "-fno-inline"]
    return base


def detect_format(stored):
    if "file format" in stored or "Disassembly of section" in stored:
        return "OBJDUMP"
    if re.search(r'^\s*\.(text|globl|p2align|seh_|file)\b', stored, re.M):
        return "GPP_S"
    return "OTHER"


def parse_gpp_s(t):
    syms, cur, in_code = {}, None, False
    SKIP = ('.p2align', '.globl', '.def', '.set', '.type', '.size', '.section',
            '.ident', '.file', '.comm', '.local', '.align', '.balign')
    for line in t.splitlines():
        s = line.rstrip()
        if not s.strip():
            continue
        msec = re.match(r'^\s*\.section\s+(\.\S+)', s)
        if msec and not msec.group(1).startswith('.text'):
            in_code = False
            cur = None
            continue
        if re.match(r'^\s*\.text\b', s):
            in_code = True
            continue
        if not in_code:
            continue
        if re.match(r'^\s*\.file\s', s) or re.match(r'^\s*\.ident\s', s):
            continue
        st = s.strip()
        mlbl = re.match(r'^\s*(\.?[A-Za-z_][\w$.]*):', st)
        if mlbl and not st.startswith(SKIP):
            # 对符号 KEY 也做内部标号归一化（与行内容一致），否则
            # 不同编译期的 .LFB394/.L4 等任意数字会污染双向符号集比较。
            cur = re.sub(r'\.L([A-Za-z]*)\d+', r'.L\1', mlbl.group(1))
            syms.setdefault(cur, [])
            continue
        s2 = re.sub(r'#.*$', '', st).strip()
        s2 = re.sub(r'\.L([A-Za-z]*)\d+', r'.L\1', s2)
        if not s2:
            continue
        if re.search(r'\b[a-z][a-z0-9]{1,}\b', s2) or s2.startswith('.'):
            if cur is not None:
                syms[cur].append(s2)
    return syms


def detect_version(stored):
    m = re.search(r'GCC:.*?(\d+\.\d+\.\d+)', stored)
    return m.group(1) if m else "UNMARKED"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--gpp", required=True, help="MinGW g++.exe (>=15.3.0)")
    ap.add_argument("--examples", required=True)
    ap.add_argument("--out", default=None)
    ap.add_argument("--only", default="all",
                    help="15.3.0 | 13.1.0 | unmarked | all")
    ap.add_argument("--name-substr", default=None)
    a = ap.parse_args()
    GPP, EX = a.gpp, a.examples

    asm_files = sorted(glob.glob(os.path.join(EX, "*.asm")))
    results = []
    for asm in asm_files:
        name = os.path.splitext(os.path.basename(asm))[0]
        if a.name_substr and a.name_substr not in name:
            continue
        stored = open(asm, encoding="utf-8", errors="replace").read()
        ver = detect_version(stored)
        if a.only != "all" and ver.lower() != a.only.lower():
            continue
        # 源文件来自 .file 指令
        mfile = re.search(r'^\s*\.file\s+"([^"]+)"', stored, re.M)
        if not mfile:
            results.append({"name": name, "ver": ver, "status": "NO_SOURCE"})
            continue
        src = os.path.join(EX, mfile.group(1))
        if not os.path.exists(src):
            results.append({"name": name, "ver": ver, "status": "NO_SOURCE",
                            "detail": mfile.group(1)})
            continue
        fmt = detect_format(stored)
        if fmt != "GPP_S":
            results.append({"name": name, "ver": ver, "status": "FORMAT_SKIP",
                            "fmt": fmt})
            continue
        flags = flags_for(name)
        fs_ = os.path.join(EX, "_chk_" + name + ".s")
        p = subprocess.run([GPP] + flags + ["-S", "-masm=intel", src, "-o", fs_],
                           capture_output=True, text=True)
        rc, err = p.returncode, p.stderr
        if rc != 0:
            results.append({"name": name, "ver": ver, "status": "COMPILE_FAIL",
                            "detail": (err.strip().splitlines() or ["?"])[0][:130]})
            if os.path.exists(fs_):
                os.remove(fs_)
            continue
        fresh = open(fs_, encoding="utf-8", errors="replace").read()
        fs = parse_gpp_s(fresh)
        ss = parse_gpp_s(stored)
        os.remove(fs_)
        fs_syms = set(fs)
        ss_syms = set(ss)
        # 双向符号集校验（红线核心）：存储侧与重编侧符号集必须互含，
        # 否则存在「幽灵符号」(stored 多出、疑似伪造) 或「版本漂移」(fresh 多出)。
        extra_stored = ss_syms - fs_syms   # stored 有、fresh 无 -> 疑似伪造/篡改
        extra_fresh = fs_syms - ss_syms    # fresh 有、stored 无 -> 版本/优化档漂移
        if not extra_stored and not extra_fresh:
            # 符号集双向一致 -> 再比体（内部标号数字已归一化）
            fst = [ln for sym in fs_syms for ln in ss[sym]]
            fa = [ln for sym in fs_syms for ln in fs[sym]]
            if sorted(fst) == sorted(fa):
                results.append({"name": name, "ver": ver, "status": "MATCH",
                                "syms": len(fs_syms)})
            else:
                d = list(difflib.unified_diff(sorted(fst), sorted(fa),
                                              "stored", "fresh", lineterm=""))
                n = sum(1 for x in d if x[:1] in "+-" and not x[:3] in ("+++", "---"))
                results.append({"name": name, "ver": ver, "status": "DRIFT",
                                "drift_kind": "LINES",
                                "ndiff": n, "fresh_syms": len(fs_syms),
                                "stored_syms": len(ss_syms)})
        else:
            # 符号集不对称 -> 必为 DRIFT；标注方向以区分伪造嫌疑与版本漂移
            kind = "STORED_EXTRA" if extra_stored else "FRESH_EXTRA"
            results.append({"name": name, "ver": ver, "status": "DRIFT",
                            "drift_kind": kind,
                            "extra_stored": sorted(extra_stored)[:5],
                            "extra_fresh": sorted(extra_fresh)[:5],
                            "n_extra_stored": len(extra_stored),
                            "n_extra_fresh": len(extra_fresh),
                            "fresh_syms": len(fs_syms),
                            "stored_syms": len(ss_syms)})

    cnt = Counter(r["status"] for r in results)
    print(f"scanned={len(results)}  MATCH={cnt['MATCH']}  DRIFT={cnt['DRIFT']}  "
          f"COMPILE_FAIL={cnt['COMPILE_FAIL']}  NO_SOURCE={cnt['NO_SOURCE']}  "
          f"FORMAT_SKIP={cnt['FORMAT_SKIP']}")
    out = a.out or os.path.join(EX, "_repro_spotcheck.json")
    json.dump({"summary": dict(cnt), "results": results},
              open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print(f"-> {out}")


if __name__ == "__main__":
    main()
