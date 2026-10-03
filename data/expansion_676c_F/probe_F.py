#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""probe_F.py — 实证 676c-F 六个缺陷族在真实检测器下的行为，指导生成器的 expected_verdict。"""
import os, sys, json, shutil, tempfile, importlib.util

# 环境偏差规避：WSL 横幅污染（memory 记录），所有 WSL 调用前设：
os.environ["WSL_UTF8"] = "1"
os.environ["WSLENV"] = "WSL_UTF8/u"

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLS = os.path.join(REPO, "tools")
ATOMS = os.path.join(REPO, "Examples", "atoms")
PROBE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "probe_src")
os.makedirs(PROBE, exist_ok=True)

spec = importlib.util.spec_from_file_location("hr", os.path.join(TOOLS, "holdout_reveal_661.py"))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
detect = mod.detect

# 把样本目录指向 probe_src，detect() 直接读这里
mod.ATOMS = PROBE

PATTERNS = {
    "alignment_reinterpret": (
        'int main(){ char b[16]={0}; int* p=(int*)(b+1); int x=*p; (void)x; return 0; }\n',
        ["ubsan", "compiler-warn"]),
    "alignment_packed": (
        '#pragma pack(push,1)\nstruct S{char c; int i;};#pragma pack(pop)\n'
        'int main(){ S s; s.i=42; (void)s.i; return 0; }\n',
        ["ubsan", "compiler-warn"]),
    "alignment_simd_attr": (
        '#include <cstddef>\nstruct alignas(16) A{ double a[2]; };\n'
        'int main(){ char buf[8]; A* p=(A*)(void*)buf; (void)p; return 0; }\n',
        ["ubsan", "compiler-warn"]),
    "shift_overflow_signed": (
        'int main(){ int x=1; int y=x<<31; (void)y; return 0; }\n',
        ["ubsan", "compiler-warn"]),
    "shift_negative": (
        'int main(){ int x=1; int y=x<<(-1); (void)y; return 0; }\n',
        ["ubsan", "compiler-warn"]),
    "shift_overflow_unsigned": (
        'int main(){ unsigned x=1u; unsigned y=x<<31; (void)y; return 0; }\n',
        ["ubsan", "compiler-warn"]),
    "endian_network_nohtonl": (
        '#include <cstdio>\nint main(){ unsigned char raw[4]={0x12,0x34,0x56,0x78};'
        ' unsigned v=*(unsigned*)raw; (void)v; std::printf("%u\\n",v); return 0; }\n',
        ["ubsan", "compiler-warn"]),
    "volatile_sync_flag": (
        'int main(){ volatile int f=0; (void)f; while(f==0){} return 0; }\n',
        ["ubsan", "compiler-warn"]),
    "volatile_constcast": (
        'int main(){ volatile int v=0; int* p=const_cast<int*>((volatile int*)&v); (void)*p; return 0; }\n',
        ["ubsan", "compiler-warn"]),
    "interrupt_signal_nonreentrant": (
        '#include <csignal>\n#include <cstdio>\nstatic int shared=0;\n'
        'extern "C" void h(int){ std::printf("x"); shared++; }\n'
        'int main(){ std::signal(SIGUSR1,h); raise(SIGUSR1); (void)shared; return 0; }\n',
        ["ubsan", "compiler-warn"]),
    "setjmp_longjmp_skip_dtor": (
        '#include <csetjmp>\n#include <string>\njmp_buf env;\n'
        'int main(){ volatile int once=0; if(setjmp(env)==0){ std::string s="hi";'
        ' if(!once){once=1; longjmp(env,1);} } return 0; }\n',
        ["ubsan", "compiler-warn"]),
    "register_keyword": (
        'int main(){ register int x=0; (void)x; return 0; }\n',
        ["ubsan", "compiler-warn"]),
    "bitfield_overflow": (
        'struct B{ unsigned a:3; };\nint main(){ B b; b.a=9; (void)b.a; return 0; }\n',
        ["ubsan", "compiler-warn"]),
    "bitset_oob": (
        '#include <bitset>\nint main(){ std::bitset<8> bs; (void)bs.test(9); return 0; }\n',
        ["ubsan", "compiler-warn"]),
}

def run():
    out = {}
    for name, (src, kinds) in PATTERNS.items():
        fn = name + ".cpp"
        open(os.path.join(PROBE, fn), "w").write(src)
        sub = {}
        for k in kinds:
            try:
                v, note = detect(k, [fn])
            except Exception as e:
                v, note = "exception", str(e)[:80]
            sub[k] = (v, note[:120])
        out[name] = sub
        print(f"[{name}] " + " | ".join(f"{k}={v}" for k, (v, _) in sub.items()))
        for k, (v, note) in sub.items():
            if v != "miss":
                print(f"      {k}: {note}")
    json.dump(out, open(os.path.join(os.path.dirname(__file__), "probe_results.json"), "w"),
              ensure_ascii=False, indent=2)
    print("\n已写 probe_results.json")

if __name__ == "__main__":
    run()
