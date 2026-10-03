#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# -*- probe: 实证每个扩样-C 缺陷族的检测器行为，再决定模板（不猜测） -*-
import os, sys, json, shutil, tempfile, importlib.util

REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLS = os.path.join(REPO, "tools")
ATOMS = os.path.join(REPO, "Examples", "atoms")
spec = importlib.util.spec_from_file_location("hr", os.path.join(TOOLS, "holdout_reveal_661.py"))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
detect = mod.detect

def wsan(kind, files, opt):
    """单档位 WSL sanitizer 运行（用于 optimization_sensitivity 判定）。"""
    srcs = [os.path.join(ATOMS, f) for f in files]
    tmp = tempfile.mkdtemp()
    copies = []
    for s in srcs:
        d = os.path.join(tmp, os.path.basename(s)); shutil.copy2(s, d); copies.append(d)
    w = [mod._to_wsl(c) for c in copies]
    san = mod.SAN[kind]
    exe = "/tmp/probe_opt"
    c = f"g++ -std=c++17 {opt} -g -fsanitize={san} -pthread {' '.join(w)} -o {exe}"
    rc, out = mod._wsl(c)
    if rc != 0:
        shutil.rmtree(tmp, ignore_errors=True); return ("compile_fail", out[:100])
    rc, out = mod._wsl(mod._setarch_prefix() + exe, timeout=120)
    low = out.lower()
    if kind == "ubsan":
        hit = "runtime error" in out
    else:
        hit = ("AddressSanitizer" in out or "LeakSanitizer" in out
               or "detected memory leaks" in low or "double-free" in low)
    shutil.rmtree(tmp, ignore_errors=True)
    return (("catch" if hit else "miss"), out.strip()[:100])

def run(name, files, kind, opt_check=None):
    written = []
    try:
        for fn, content in files.items():
            p = os.path.join(ATOMS, fn)
            open(p, "w").write(content)
            written.append(p)
        if opt_check:
            o0 = wsan(opt_check[0], list(files.keys()), "-O0")
            o2 = wsan(opt_check[0], list(files.keys()), "-O2")
            print(f"[{name}] opt {opt_check[0]}: O0={o0} O2={o2}")
        v, note = detect(kind, list(files.keys()))
        print(f"[{name}] detect({kind}) -> {v} | {note[:90]}")
    finally:
        for p in written:
            try: os.remove(p)
            except OSError: pass

H = ('#include <cstdio>\n'
     '#ifndef H_XXX\n#define H_XXX\n'
     'inline int f(){return 1;}\n'
     'int g();\n'
     '#endif\n')

# P1 自移动 self-move (compiler-warn 应 catch)
P1 = {"p1.cpp": 'int main(){ struct S{int x;}; S a{1}; a = std::move(a); (void)a; return 0; }\n'
      .replace("std::move", "std::move")}
P1 = {"p1.cpp": '#include <utility>\nint main(){ struct S{int x;}; S a{1}; a = std::move(a); (void)a; return 0; }\n'}

# P2 use-after-move (compiler-warn 应 miss)
P2 = {'#include <string>\nint main(){ std::string s="x"; auto t=std::move(s); (void)s.empty(); return 0; }\n' and
      'p2.cpp': '#include <string>\nint main(){ std::string s="x"; auto t=std::move(s); (void)s.empty(); return 0; }\n'}

# P3 return local ref (compiler-warn 应 catch)
P3 = {"p3.cpp": 'int& f(){ int x=1; return x; }\nint main(){ (void)f(); return 0; }\n'}

# P4 raii heap leak on exception (asan 应 catch via LeakSanitizer)
P4 = {"p4.cpp": 'int main(){ try{ int* p=new int[10]; throw 1; }catch(int){} return 0; }\n'}

# P5 raii new[]/delete mismatch (asan 应 catch)
P5 = {"p5.cpp": 'int main(){ int* p=new int[10]; delete p; return 0; }\n'}

# P6 raii lock leak (asan 应 miss)
P6 = {"p6.cpp": '#include <mutex>\nstd::mutex m;\nint main(){ m.lock(); if(true) return 1; m.unlock(); return 0; }\n'}

# P7 virtual ctor-calls-virtual (asan 应 miss)
P7 = {"p7.cpp": ('class B{ public: B(){ vf(); } virtual void vf(){ printf("B\\n"); } };\n'
                 'class D: public B{ public: void vf() override { printf("D\\n"); } };\n'
                 '#include <cstdio>\n'
                 'int main(){ D d; return 0; }\n')}

# P8 virtual pure call in ctor (asan 应 miss)
P8 = {"p8.cpp": ('#include <cstdio>\n'
                 'class B{ public: B(){ pure(); } virtual void pure()=0; };\n'
                 'class D: public B{ public: void pure() override { printf("D\\n"); } };\n'
                 'int main(){ try{ D d; }catch(...){} return 0; }\n')}

# P9 cross_tu strong multiple def (linker 应 catch)
P9 = {"p9a.h": '#ifndef P9H\n#define P9H\nint f(){ return 1; }\n#endif\n',
      "p9a.cpp": '#include "p9a.h"\n',
      "p9main.cpp": '#include "p9a.h"\nint main(){ return f(); }\n'}

# P10 cross_tu inline different def (asan 应 miss)
P10 = {"p10a.h": '#ifndef P10A\n#define P10A\ninline int f(){ return 1; }\n#endif\n',
       "p10b.h": '#ifndef P10B\n#define P10B\ninline int f(){ return 2; }\n#endif\n',
       "p10main.cpp": '#include "p10a.h"\n#include "p10b.h"\nint main(){ return f(); }\n'}

# P11 cross_tu static init order (asan 应 miss)
P11 = {"p11a.cpp": 'extern int y;\nint x = y + 1;\n',
       "p11b.cpp": 'int y = 5;\n',
       "p11main.cpp": 'extern int x; int main(){ (void)x; return 0; }\n'}

# P12 opt-dep signed overflow (ubsan 应 catch，O0 抓 O2 可能消除)
P12 = {"p12.cpp": '#include <climits>\nint main(){ int x=INT_MAX; x=x+1; (void)x; return 0; }\n'}

# P13 opt-dep strict aliasing (ubsan 应 miss，但 O0/O2 输出不同)
P13 = {"p13.cpp": ('#include <cstdio>\nint main(){\n'
                   '  int i=0x3f800000; float f=1.0f;\n'
                   '  int* ip=(int*)&f; *ip=0x3f800000; float r=f+1.0f;\n'
                   '  printf("%f\\n", r); return 0;\n}\n')}

# P14 conditional trigger off-by-one when n=8 (asan 应 catch)
P14 = {"p14.cpp": 'int main(){ int n=8; int a[4]; for(int i=0;i<n;i++) a[i]=i; return 0; }\n'}

# P15 conditional trigger logic bug (asan 应 miss，触发可复现)
P15 = {"p15.cpp": ('#include <cstdio>\nint main(){ int k=3; int r=0;\n'
                   '  if(k==3){ r = 100/k; } else { r = 1; }\n'
                   '  printf("%d\\n", r); return 0; }\n')}

print("=== move_semantics ===")
run("P1 self-move", P1, "compiler-warn")
run("P2 use-after-move", P2, "compiler-warn")
run("P3 return-local-ref", P3, "compiler-warn")
print("=== raii_violation ===")
run("P4 leak-on-exc", P4, "asan")
run("P5 new/delete mismatch", P5, "asan")
run("P6 lock leak", P6, "asan")
print("=== virtual_function ===")
run("P7 ctor-virtual", P7, "asan")
run("P8 pure-call-ctor", P8, "asan")
print("=== cross_tu_ub ===")
run("P9 strong multidef", P9, "linker")
run("P10 inline diff", P10, "asan")
run("P11 static-init-order", P11, "asan")
print("=== optimization_dependent ===")
run("P12 signed-overflow", P12, "ubsan", opt_check=("ubsan",))
run("P13 strict-aliasing", P13, "ubsan", opt_check=("asan",))
print("=== conditional_trigger ===")
run("P14 oob-when-n8", P14, "asan")
run("P15 logic-bug", P15, "asan")
