# -*- coding: utf-8 -*-
"""676c-G 冒烟校准: 验证检测器机制在本机工具链下的行为，再批量生成样本。"""
import os, subprocess, sys, tempfile

SMOKE = os.path.dirname(os.path.abspath(__file__))

PROBES = {
# ---- compiler-warn 探针（本地 MinGW g++ -Wall -Wextra）----
"p_warn_unused_result": r'''
#include <cstdlib>
int main(){ char* p = (char*)malloc(10); realloc(p, 20); return p != 0 ? 0 : 1; }
''',
"p_warn_dangling_ref": r'''
#include <string>
const std::string& get(const std::string& s){ return s; }
int main(){ const std::string& r = get(std::string("tmp")); return (int)r.size(); }
''',
"p_warn_stringop": r'''
#include <cstring>
int main(){ char d[8]; const char* s = "012345678901234567890123456789"; memcpy(d, s, 30); return d[0]; }
''',
"p_warn_uninit": r'''
#include <cstdio>
int main(){ int a[10]; a[0] = 1; printf("%d\n", a[5]); return 0; }
''',
# ---- asan 探针（WSL）----
"p_asan_heap_overread": r'''
int main(){ char* p = new char[4]; char c = p[4]; delete[] p; return c; }
''',
"p_asan_heap_oobwrite": r'''
int main(){ char* p = new char[4]; p[4] = 'x'; return 0; }
''',
"p_asan_stack_overread": r'''
int f(char* p){ return p[5]; }
int main(){ char a[4] = {1,2,3,4}; return f(a); }
''',
"p_asan_leak": r'''
int main(){ char* p = new char[100]; p[0] = 1; return p[0]; }
''',
"p_asan_null": r'''
struct S{ int x; };
int main(){ S* p = 0; return p->x; }
''',
"p_asan_recursion": r'''
int rec(int n){ char pad[16]; pad[0] = (char)n; if (n <= 0) return 0; return 1 + rec(n - 1) + pad[0]; }
int main(){ return rec(5000000) > 0 ? 1 : 0; }
''',
# ---- ubsan 探针（WSL）----
"p_ubsan_signed": r'''
#include <cstdio>
int main(){ volatile int v = 2147483647; int y = v + 1; printf("%d\n", y); return 0; }
''',
"p_ubsan_div0": r'''
#include <cstdio>
int main(){ volatile int z = 0; int x = 100 / z; printf("%d\n", x); return 0; }
''',
"p_ubsan_ptr_overflow": r'''
#include <cstdio>
int main(){ volatile long off = -2147483647L; const char* p = (const char*)0x1000; const char* q = p + off; printf("%p\n", (void*)q); return 0; }
''',
# ---- miss 盲区确认（应无任何报告）----
"p_miss_uninit_read": r'''
int main(){ int a[10]; a[0] = 1; a[1] = 2; if (a[5] == 42) return 1; return 0; }
''',
}

def wsl(cmd, timeout=120):
    r = subprocess.run(["wsl", "-e", "bash", "-lc", cmd], capture_output=True, text=True, timeout=timeout,
                       env={**os.environ, "WSL_UTF8": "1", "WSLENV": "WSL_UTF8/u"})
    return r.returncode, (r.stdout or "") + (r.stderr or "")

def local(cmd, timeout=60):
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return r.returncode, (r.stdout or "") + (r.stderr or "")

results = []
for name, code in PROBES.items():
    path = os.path.join(SMOKE, name + ".cpp")
    with open(path, "w", encoding="utf-8") as f:
        f.write(code)
    # 1) 本地 -Wall -Wextra（看告警）
    rc, out = local(["g++", "-std=c++17", "-Wall", "-Wextra", "-fsyntax-only", path])
    warns = [l.strip()[:110] for l in out.splitlines() if "warning:" in l]
    # 2) WSL asan
    wa = wsl(f"g++ -std=c++17 -O0 -g -fsanitize=address -pthread /mnt/c/CodeLearnling/note/note/C++/CPP-Bible/data/expansion_676c_G/{name}.cpp -o /tmp/{name}_a 2>&1 && timeout 20 /tmp/{name}_a 2>&1 | head -4")
    hit_a = any(k in wa[1] for k in ("AddressSanitizer", "LeakSanitizer", "detected memory leaks"))
    # 3) WSL ubsan
    wu = wsl(f"g++ -std=c++17 -O0 -g -fsanitize=undefined -pthread /mnt/c/CodeLearnling/note/note/C++/CPP-Bible/data/expansion_676c_G/{name}.cpp -o /tmp/{name}_u 2>&1 && timeout 20 /tmp/{name}_u 2>&1 | head -4")
    hit_u = "runtime error" in wu[1]
    results.append((name, len(warns), warns[0] if warns else "", hit_a, hit_u))
    print(f"{name:24} warn={len(warns)} asan={hit_a} ubsan={hit_u}")
    if warns:
        print(f"    W: {warns[0]}")
    if hit_a:
        print(f"    A: {wa[1].strip().splitlines()[0][:110] if wa[1].strip() else ''}")
    if hit_u:
        print(f"    U: {wu[1].strip().splitlines()[0][:110] if wu[1].strip() else ''}")
print("\nDONE")
