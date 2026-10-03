#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import os, importlib.util, shutil, tempfile
REPO = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
TOOLS = os.path.join(REPO, "tools"); ATOMS = os.path.join(REPO, "Examples", "atoms")
spec = importlib.util.spec_from_file_location("hr", os.path.join(TOOLS, "holdout_reveal_661.py"))
mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
detect = mod.detect

def wsan(kind, files, opt):
    srcs=[os.path.join(ATOMS,f) for f in files]; tmp=tempfile.mkdtemp(); copies=[]
    for s in srcs:
        d=os.path.join(tmp,os.path.basename(s)); shutil.copy2(s,d); copies.append(d)
    w=[mod._to_wsl(c) for c in copies]; exe="/tmp/probe_opt"
    rc,out=mod._wsl(f"g++ -std=c++17 {opt} -g -fsanitize={mod.SAN[kind]} -pthread {' '.join(w)} -o {exe}")
    if rc!=0: shutil.rmtree(tmp,ignore_errors=True); return ("compile_fail",out[:80])
    rc,out=mod._wsl(mod._setarch_prefix()+exe,timeout=120); low=out.lower()
    hit = ("runtime error" in out) if kind=="ubsan" else ("AddressSanitizer" in out or "LeakSanitizer" in out or "detected memory leaks" in low or "double-free" in low)
    shutil.rmtree(tmp,ignore_errors=True)
    return (("catch" if hit else "miss"), out.strip()[:80])

def run(name, files, kind, opt_check=None):
    written=[]
    try:
        for fn,c in files.items():
            p=os.path.join(ATOMS,fn); open(p,"w").write(c); written.append(p)
        if opt_check:
            print(f"[{name}] {opt_check[0]} O0={wsan(opt_check[0],list(files.keys()),'-O0')} O2={wsan(opt_check[0],list(files.keys()),'-O2')}")
        v,note=detect(kind,list(files.keys())); print(f"[{name}] detect({kind}) -> {v} | {note[:80]}")
    finally:
        for p in written:
            try: os.remove(p)
            except OSError: pass

# 修正后的 virtual_function 模式（均可编译运行，预期 miss）
P7b = {"p7b.cpp": ('#include <cstdio>\n'
  'class B{ public: B(){ vf(); } virtual void vf(){ printf("B\\n"); } };\n'
  'class D: public B{ public: void vf() override { printf("D\\n"); } };\n'
  'int main(){ D d; return 0; }\n')}
P8b = {"p8b.cpp": ('#include <cstdio>\n'
  'class B{ public: virtual ~B(){ vf(); } virtual void vf(){ printf("B\\n"); } };\n'
  'class D: public B{ public: void vf() override { printf("D\\n"); } };\n'
  'int main(){ D d; return 0; }\n')}
P8c = {"p8c.cpp": ('#include <cstdio>\n'
  'struct B{ virtual void vf(){ printf("B\\n"); } virtual ~B(){} };\n'
  'struct D: B{ void vf() override { printf("D\\n"); } };\n'
  'int main(){ D d; B b = d; b.vf(); return 0; }\n')}

# cross_tu inline ODR（分 TU，预期 miss）
P10b = {
  "p10a.h": "#ifndef P10A\n#define P10A\ninline int f(){ return 1; }\n#endif\n",
  "p10b.h": "#ifndef P10B\n#define P10B\ninline int f(){ return 2; }\n#endif\n",
  "p10a.cpp": '#include "p10a.h"\nint fa(){ return f(); }\n',
  "p10b.cpp": '#include "p10b.h"\nint fb(){ return f(); }\n',
  "p10main.cpp": "int fa(); int fb();\nint main(){ return fa()+fb(); }\n"}

# strict aliasing（预期 miss，但 O0/O2 输出可能不同）
P13b = {"p13b.cpp": ('#include <cstdio>\n'
  'void f(int* pi, float* pf){ *pi = 1; *pf = 2.0f; }\n'
  'int main(){ float x=0; f((int*)&x, &x); printf("%f\\n", x); return 0; }\n')}

# raii catch: 非虚析构删除派生 (compiler-warn 应 catch)
P16 = {"p16.cpp": ('#include <cstdio>\n'
  'struct B{ ~B(){ printf("~B\\n"); } };\n'
  'struct D: B{ ~D(){ printf("~D\\n"); } };\n'
  'int main(){ B* p=new D; delete p; return 0; }\n')}

# raii miss: 文件句柄泄漏 (asan 应 miss)
P17 = {"p17.cpp": ('#include <cstdio>\n'
  'int main(){ FILE* fp=fopen("__nope.tmp","w"); (void)fp; return 0; }\n')}

# move catch: redundant move / 自移动变体
P18 = {"p18.cpp": ('#include <utility>\n'
  'struct S{int x;};\nint main(){ S a{1}; S b{2}; b = std::move(a); b = std::move(a); (void)b; return 0; }\n')}

print("=== virtual (修正) ===")
run("P7b ctor-virtual", P7b, "asan")
run("P8b dtor-virtual", P8b, "asan")
run("P8c slicing", P8c, "asan")
print("=== cross_tu inline ODR ===")
run("P10b inline-diff", P10b, "asan")
print("=== strict aliasing ===")
run("P13b strict-alias", P13b, "asan", opt_check=("asan",))
print("=== raii/delete-non-virtual-dtor ===")
run("P16 del-nonvirt-dtor", P16, "compiler-warn")
run("P17 file-leak", P17, "asan")
print("=== move redundant ===")
run("P18 redundant-move", P18, "compiler-warn")
