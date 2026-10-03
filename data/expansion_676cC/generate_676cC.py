#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# SPDX-License-Identifier: Apache-2.0
"""generate_676cC.py — 676c 扩样-C 候选样本生成器（数据标注 Agent）。
类别：C（C++ 特定 + 复杂组合 + 难例，检测器易翻车）。
产物：data/expansion_676cC/sample_NNN.cpp[+ .h/_a.cpp/_main.cpp] + sample_NNN.json

设计原则（诚实 + 可复现）：
- 只使用经 probe 实证过的"可抓"模式（catch）与"盲区"模式（miss）。
- cross_tu_ub 多文件：不同 TU 分别 include 不同头，ODR 跨 TU（非同 TU 重定义）。
- del-nonvirtual-dtor：基类必须有虚函数，否则 -Wdelete-non-virtual-dtor 不报。
- 缺陷行嵌入 `// <<PLANTED-DEFECT>>` 哨兵，精确计算 defect_location。
- planted 全 true（LLM 植入，如实标注）。
- 多文件样本用 __SID__ 占位文件名，emit 时替换为样本 id。
"""
import os, json

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = HERE
os.makedirs(OUT, exist_ok=True)
SENT = "<<PLANTED-DEFECT>>"


def emit(idx, files, defect_suffix, defect_func, meta):
    stem = f"sample_{idx:03d}"
    written = {}
    for suf, content in files.items():
        content2 = content.replace("__SID__", stem)
        suf2 = suf if (suf.startswith(".") or "." in suf) else "." + suf
        fname = stem + suf2
        open(os.path.join(OUT, fname), "w", encoding="utf-8").write(content2 + "\n")
        written[suf] = fname
    # 缺陷行定位
    dfile = written[defect_suffix]
    lines = open(os.path.join(OUT, dfile), encoding="utf-8").read().splitlines()
    dline = None
    for i, ln in enumerate(lines, 1):
        if SENT in ln:
            dline = i
            break
    assert dline is not None, f"{stem}: missing sentinel in {dfile}"
    src_files = [written[s] for s in files]
    meta = dict(meta)
    meta.update({
        "id": stem,
        "category": "C",
        "defect_location": {"line": dline, "function": defect_func,
                            "note": lines[dline - 1].strip()},
        "planted": True,
        "source_files": src_files,
        "generator": "676c-expC-generate",
    })
    json.dump(meta, open(os.path.join(OUT, stem + ".json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    return stem


# ============================ move_semantics ============================
def ms_self(name, field):
    code = r'''#include <utility>
struct __NAME__ { int __FIELD__; };
int main(){
  __NAME__ a{1};
  a = std::move(a); // ''' + SENT + r''' 自移动（self-move）：对象移动给自身
  (void)a;
  return 0;
}
'''
    code = code.replace("__NAME__", name).replace("__FIELD__", field)
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "move_semantics", "expected_detectors": ["compiler-warn"],
             "expected_verdict": "catch", "severity": "medium",
             "trigger_condition": "无条件（始终触发）", "optimization_sensitivity": "n/a",
             "notes": "自移动 a=std::move(a) 触发 -Wself-move（compiler-warn 抓）。移动语义误用。"})


def ms_retlocal(kind):
    if kind == "ref":
        code = r'''int& f(){ int x = 5; return x; } // ''' + SENT + r''' 返回局部变量引用（dangling）
int main(){ (void)f(); return 0; }
'''
    elif kind == "arr":
        code = r'''int* g(){ int a[3] = {1,2,3}; return a; } // ''' + SENT + r''' 返回局部数组指针
int main(){ (void)g(); return 0; }
'''
    else:
        code = r'''struct S{int v;};
S& h(){ S s{7}; return s; } // ''' + SENT + r''' 返回局部对象引用
int main(){ (void)h(); return 0; }
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "move_semantics", "expected_detectors": ["compiler-warn"],
             "expected_verdict": "catch", "severity": "high",
             "trigger_condition": "无条件", "optimization_sensitivity": "n/a",
             "notes": "返回指向已销毁栈对象的引用/指针，触发 -Wreturn-local-addr（compiler-warn 抓）。"})


def ms_uaf_move(t):
    body = {
        "string": r'''#include <string>
int main(){
  std::string s = "hello";
  std::string t = std::move(s);
  if (s.empty()) { (void)0; } // ''' + SENT + r''' 使用已移动对象 s（有效但处于未指定状态）
  return 0;
}
''',
        "vector": r'''#include <vector>
int main(){
  std::vector<int> v{1,2,3};
  std::vector<int> w = std::move(v);
  (void)v.size(); // ''' + SENT + r''' 使用已移动对象 v（size() 结果未指定）
  return 0;
}
''',
        "unique": r'''#include <memory>
int main(){
  std::unique_ptr<int> p(new int(5));
  std::unique_ptr<int> q = std::move(p);
  (void)*p; // ''' + SENT + r''' 解引用已移动走的 p（可能为 nullptr）
  return 0;
}
''',
        "map": r'''#include <map>
int main(){
  std::map<int,int> m{{1,2}};
  std::map<int,int> n = std::move(m);
  (void)m.empty(); // ''' + SENT + r''' 使用已移动对象 m
  return 0;
}
''',
    }[t]
    return ({"cpp": body}, "cpp", "main",
            {"defect_type": "move_semantics", "expected_detectors": ["compiler-warn"],
             "expected_verdict": "miss", "severity": "low",
             "trigger_condition": "无条件", "optimization_sensitivity": "n/a",
             "notes": f"对已移动自 {t} 的对象继续访问：C++ 允许但结果未指定；无检测器可抓（盲区）。"})


def ms_dblmove(t):
    if t == "two":
        code = r'''#include <utility>
struct S{int x;};
int main(){
  S a{1}, b{2};
  b = std::move(a);
  a = std::move(b); // ''' + SENT + r''' 双移动：a、b 均处于已移动状态，逻辑混乱
  (void)a; (void)b;
  return 0;
}
'''
    else:
        code = r'''#include <utility>
struct S{int x;};
int main(){
  S a{1};
  auto f = [&](){ return std::move(a); }; // 捕获引用后移动
  S b = f();
  S c = f(); // ''' + SENT + r''' 对同一对象二次移动（通过 lambda 捕获）
  (void)b; (void)c;
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "move_semantics", "expected_detectors": ["compiler-warn"],
             "expected_verdict": "miss", "severity": "low",
             "trigger_condition": "无条件", "optimization_sensitivity": "n/a",
             "notes": "多次移动同一对象：合法但语义可疑，无检测器可抓（盲区）。"})


# ============================ raii_violation ============================
def raii_leak_exc(n):
    code = r'''int main(){
  try {
    int* p = new int[16];
    if (%d) throw 1;
    delete[] p;
  } catch (int) {}
  return 0;
} // ''' % n + SENT + r''' 异常路径下 new[] 未释放 -> 泄漏
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "raii_violation", "expected_detectors": ["asan"],
             "expected_verdict": "catch", "severity": "high",
             "trigger_condition": "异常被抛出时（始终触发）", "optimization_sensitivity": "n/a",
             "notes": "异常安全漏洞：分配后抛异常未释放，LeakSanitizer 抓。"})


def raii_mismatch(kind):
    if kind == "arrdel":
        code = r'''int main(){
  int* p = new int[10];
  delete p; // ''' + SENT + r''' new[] / delete 不匹配
  return 0;
}
'''
    elif kind == "delarr":
        code = r'''int main(){
  int* p = new int(10);
  delete[] p; // ''' + SENT + r''' new / delete[] 不匹配
  return 0;
}
'''
    else:
        code = r'''#include <cstdlib>
int main(){
  int* p = (int*)malloc(40);
  delete p; // ''' + SENT + r''' malloc / delete 不匹配
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "raii_violation", "expected_detectors": ["asan"],
             "expected_verdict": "catch", "severity": "high",
             "trigger_condition": "无条件", "optimization_sensitivity": "n/a",
             "notes": "new/delete 或 malloc/free 不匹配：AddressSanitizer 抓 allocation-deallocation-mismatch。"})


def raii_delnonvirt(vm):
    code = r'''#include <cstdio>
struct B { virtual void hi(){} ~B(){} }; // 非虚析构
struct D : B { ~D(){ printf("~D\n"); } };
int main(){
  B* p = new D;
  delete p; // ''' + SENT + r''' 经非虚析构基类指针删除派生 -> 仅 ~B，~D 不跑
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "raii_violation", "expected_detectors": ["compiler-warn"],
             "expected_verdict": "catch", "severity": "high",
             "trigger_condition": "无条件", "optimization_sensitivity": "n/a",
             "notes": "经非虚析构基类删除派生对象：-Wdelete-non-virtual-dtor（compiler-warn 抓）。"})


def raii_lock():
    code = r'''#include <mutex>
std::mutex m;
int worker(){
  m.lock();
  if (true) return -1; // ''' + SENT + r''' 提前返回，未 unlock -> 锁泄漏
  m.unlock();
  return 0;
}
int main(){ return worker(); }
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "raii_violation", "expected_detectors": ["asan"],
             "expected_verdict": "miss", "severity": "medium",
             "trigger_condition": "提前返回分支", "optimization_sensitivity": "n/a",
             "notes": "手动加锁后提前返回未解锁：锁泄漏，无 sanitizer 可抓（盲区）。"})


def raii_file():
    code = r'''#include <cstdio>
int main(){
  FILE* fp = fopen("__SID__tmp.dat", "w");
  if (!fp) return 1;
  // ''' + SENT + r''' 文件句柄未 fclose 即返回 -> 句柄泄漏
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "raii_violation", "expected_detectors": ["asan"],
             "expected_verdict": "miss", "severity": "medium",
             "trigger_condition": "无条件", "optimization_sensitivity": "n/a",
             "notes": "FILE* 未关闭即返回：句柄泄漏，AddressSanitizer 不追踪 FILE（盲区）。"})


def raii_exc_nonheap():
    code = r'''#include <mutex>
std::mutex m;
int main(){
  m.lock();
  try { throw 1; } catch (int) { return 1; } // ''' + SENT + r''' 异常路径未 unlock
  m.unlock();
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "raii_violation", "expected_detectors": ["asan"],
             "expected_verdict": "miss", "severity": "medium",
             "trigger_condition": "异常抛出", "optimization_sensitivity": "n/a",
             "notes": "异常安全：锁在异常路径未释放，无 sanitizer 可抓（盲区）。"})


# ============================ virtual_function ============================
def vf_ctor():
    code = r'''#include <cstdio>
struct B { B(){ vf(); } virtual void vf(){ printf("B\n"); } };
struct D : B { void vf() override { printf("D\n"); } };
int main(){ D d; return 0; } // ''' + SENT + r''' 构造期间调用虚函数 -> 调用 B::vf 而非 D::vf
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "virtual_function", "expected_detectors": ["asan"],
             "expected_verdict": "miss", "severity": "high",
             "trigger_condition": "无条件", "optimization_sensitivity": "n/a",
             "notes": "构造函数在基类构造阶段调用虚函数，静态绑定到基类版本，逻辑错误；无检测器可抓（盲区）。"})


def vf_dtor():
    code = r'''#include <cstdio>
struct B { virtual ~B(){ vf(); } virtual void vf(){ printf("B\n"); } };
struct D : B { void vf() override { printf("D\n"); } };
int main(){ D d; return 0; } // ''' + SENT + r''' 析构期间调用虚函数 -> 调用 B::vf
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "virtual_function", "expected_detectors": ["asan"],
             "expected_verdict": "miss", "severity": "high",
             "trigger_condition": "无条件", "optimization_sensitivity": "n/a",
             "notes": "析构函数在基类析构阶段调用虚函数，绑定基类版本；无检测器可抓（盲区）。"})


def vf_slice():
    code = r'''#include <cstdio>
struct B { virtual void vf(){ printf("B\n"); } virtual ~B(){} };
struct D : B { void vf() override { printf("D\n"); } };
int main(){
  D d;
  B b = d; // ''' + SENT + r''' 对象切片：b 仅含 B 子对象
  b.vf();  // 输出 B 而非 D
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "virtual_function", "expected_detectors": ["asan"],
             "expected_verdict": "miss", "severity": "medium",
             "trigger_condition": "无条件", "optimization_sensitivity": "n/a",
             "notes": "对象切片后用基类对象调用虚函数，丢失派生行为；无检测器可抓（盲区）。"})


def vf_defarg():
    code = r'''#include <cstdio>
struct B { virtual void f(int x=1){ printf("%d\n", x); } };
struct D : B { void f(int x=2) override { printf("%d\n", x); } };
int main(){
  B* p = new D;
  p->f(); // ''' + SENT + r''' 默认实参按静态类型 B 解析 -> 打印 1 而非 2
  delete p;
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "virtual_function", "expected_detectors": ["asan"],
             "expected_verdict": "miss", "severity": "medium",
             "trigger_condition": "无条件", "optimization_sensitivity": "n/a",
             "notes": "虚函数默认实参按静态类型解析（非动态），导致意外值；无检测器可抓（盲区）。"})


def vf_hide():
    code = r'''#include <cstdio>
struct B { void f(){ printf("B\n"); } };
struct D : B { void f(int){ printf("D\n"); } }; // 名字隐藏（非 virtual）
int main(){
  D d;
  d.f(); // ''' + SENT + r''' 编译错误？实际 B::f() 被隐藏，d.f() 无匹配 -> 误用
  return 0;
}
'''
    # 修正：D::f(int) 隐藏 B::f()，d.f() 无参不匹配。改为显式调用基类。
    code = r'''#include <cstdio>
struct B { void f(){ printf("B\n"); } };
struct D : B { void f(int){ printf("D\n"); } }; // 名字隐藏（非 virtual）
int main(){
  D d;
  d.B::f(); // ''' + SENT + r''' 开发者误以为会调用 D 的 f，实则基类版本（隐藏导致歧义/误用）
  d.f(1);
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "virtual_function", "expected_detectors": ["asan"],
             "expected_verdict": "miss", "severity": "low",
             "trigger_condition": "无条件", "optimization_sensitivity": "n/a",
             "notes": "非虚函数名字隐藏导致调用基类版本；逻辑错误，无检测器可抓（盲区）。"})


def vf_uaf_virtual():
    code = r'''#include <cstdio>
struct B { virtual void vf(){ printf("B\n"); } virtual ~B(){} };
struct D : B { void vf() override { printf("D\n"); } };
int main(){
  B* p = new D;
  delete p;          // 释放
  p->vf();           // ''' + SENT + r''' 释放后经基类指针调用虚函数（UAF）
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "virtual_function", "expected_detectors": ["asan"],
             "expected_verdict": "catch", "severity": "high",
             "trigger_condition": "无条件", "optimization_sensitivity": "n/a",
             "notes": "经基类指针在 delete 后调用虚函数 = use-after-free，AddressSanitizer 抓（根因是内存安全，经虚分派触发）。"})


# ============================ cross_tu_ub ============================
def ct_strong(fname):
    h = "#ifndef __SID___H\n#define __SID___H\nint %s(){ return 1; }\n#endif\n" % fname
    a = '#include "__SID__.h"\n'
    main = '#include "__SID__.h"\nint main(){ return %s(); }\n' % fname
    files = {"h": h, "_a.cpp": a, "_main.cpp": main}
    h2 = h.replace("%s(){ return 1; }" % fname, "%s(){ return 1; } // %s" % (fname, SENT + " 头文件定义非 inline 函数，被多 TU 包含 -> 强多重定义"))
    files["h"] = h2
    return (files, "h", "(global)",
            {"defect_type": "cross_tu_ub", "expected_detectors": ["linker"],
             "expected_verdict": "catch", "severity": "high",
             "trigger_condition": "链接阶段（多 TU 包含同一定义）", "optimization_sensitivity": "n/a",
             "notes": "头文件中定义非 inline 函数并被多个翻译单元包含：强多重定义，链接器抓。"})


def ct_inline():
    ha = "#ifndef __SID___A\n#define __SID___A\ninline int f(){ return 1; }\n#endif\n"
    hb = "#ifndef __SID___B\n#define __SID___B\ninline int f(){ return 2; }\n#endif\n"
    a = '#include "__SID__.h_a"\nint fa(){ return f(); }\n'
    b = '#include "__SID__.h_b"\nint fb(){ return f(); }\n'
    main = "int fa(); int fb();\nint main(){ return fa()+fb(); }\n"
    files = {"h_a": ha, "h_b": hb, "_a.cpp": a, "_b.cpp": b, "_main.cpp": main}
    a2 = a.replace('return f();', 'return f(); } // ' + SENT + ' 不同 TU 中 inline f 定义不一致（ODR 违例）')
    files["_a.cpp"] = a2
    return (files, "_a.cpp", "fa",
            {"defect_type": "cross_tu_ub", "expected_detectors": ["asan"],
             "expected_verdict": "miss", "severity": "high",
             "trigger_condition": "链接/运行", "optimization_sensitivity": "n/a",
             "notes": "不同 TU 的 inline 函数 f 体不同：ODR 违例（弱符号），链接通过但行为未定义；无检测器可抓（盲区）。"})


def ct_initorder():
    a = "extern int y;\nint x = y + 1; // " + SENT + " 依赖 y，但 y 可能尚未构造（静态初始化顺序未定义）\n"
    b = "int y = 5;\n"
    main = "extern int x;\nint main(){ (void)x; return 0; }\n"
    files = {"_a.cpp": a, "_b.cpp": b, "_main.cpp": main}
    return (files, "_a.cpp", "(global)",
            {"defect_type": "cross_tu_ub", "expected_detectors": ["asan"],
             "expected_verdict": "miss", "severity": "high",
             "trigger_condition": "程序启动静态初始化阶段", "optimization_sensitivity": "n/a",
             "notes": "跨 TU 全局变量初始化顺序：x 依赖 y 但顺序未定义（静态初始化顺序 fiasco）；无检测器可抓（盲区）。"})


def ct_weakvar():
    ha = "#ifndef __SID___A\n#define __SID___A\ninline int g = 1;\n#endif\n"
    hb = "#ifndef __SID___B\n#define __SID___B\ninline int g = 2;\n#endif\n"
    a = '#include "__SID__.h_a"\nint ga(){ return g; }\n'
    b = '#include "__SID__.h_b"\nint gb(){ return g; }\n'
    main = "int ga(); int gb();\nint main(){ return ga()+gb(); }\n"
    files = {"h_a": ha, "h_b": hb, "_a.cpp": a, "_b.cpp": b, "_main.cpp": main}
    a2 = a.replace('return g;', 'return g; } // ' + SENT + ' 不同 TU 中 inline 变量 g 初值不一致（ODR 违例）')
    files["_a.cpp"] = a2
    return (files, "_a.cpp", "ga",
            {"defect_type": "cross_tu_ub", "expected_detectors": ["asan"],
             "expected_verdict": "miss", "severity": "high",
             "trigger_condition": "链接/运行", "optimization_sensitivity": "n/a",
             "notes": "不同 TU 的 inline 变量 g 初值不同：ODR 违例（弱符号），链接通过行为未定义；无检测器可抓（盲区）。"})


# ============================ optimization_dependent ============================
def opt_signedoverflow():
    code = r'''#include <climits>
int main(){
  int x = INT_MAX;
  x = x + 1; // ''' + SENT + r''' 有符号整数溢出（UB）
  (void)x;
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "optimization_dependent", "expected_detectors": ["ubsan"],
             "expected_verdict": "catch", "severity": "high",
             "trigger_condition": "无条件", "optimization_sensitivity": "O0: ubsan 抓；O2: 编译器按 UB 假设消除，常不报",
             "notes": "有符号溢出 UB；-fsanitize=undefined 在 -O0 抓，但 -O2 下常被优化器消除（优化敏感）。"})


def opt_shift():
    code = r'''int main(){
  int r = 1 << 40; // ''' + SENT + r''' 移位量超出 int 位宽（UB）
  (void)r;
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "optimization_dependent", "expected_detectors": ["ubsan"],
             "expected_verdict": "catch", "severity": "high",
             "trigger_condition": "无条件", "optimization_sensitivity": "O0: ubsan 抓；O2: 移位结果可能被常量折叠，未必报",
             "notes": "左移量超位宽 UB；ubsan 在 -O0 抓，优化档位下行为可能改变。"})


def opt_divzero():
    code = r'''int main(){
  int a = 10;
  int r = a / 0; // ''' + SENT + r''' 整数除以零（UB）
  (void)r;
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "optimization_dependent", "expected_detectors": ["ubsan"],
             "expected_verdict": "catch", "severity": "high",
             "trigger_condition": "无条件", "optimization_sensitivity": "O0: ubsan 抓；O2: 可能被识别为不可达/常量",
             "notes": "整数除以零 UB；ubsan 在 -O0 抓，优化档位下可能不同。"})


def opt_strictalias():
    code = r'''#include <cstdio>
float g(float* pf, int* pi){ *pi = 1; return *pf; } // ''' + SENT + r''' 通过 int* 写后通过 float* 读（严格别名违例）
int main(){
  float x = 2.0f;
  int r = (int)g(&x, (int*)&x);
  printf("%d\n", r);
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "optimization_dependent", "expected_detectors": ["asan"],
             "expected_verdict": "miss", "severity": "medium",
             "trigger_condition": "无条件", "optimization_sensitivity": "O0: 返回 float 位模式被 int 写破坏后的值；O2: 假设无别名，返回原 2.0f -> 输出不同",
             "notes": "严格别名违例：经不同类型指针访问同一对象。无 sanitizer 直接抓，但 O0/O2 输出不同（优化敏感）。"})


# ============================ conditional_trigger ============================
def cond_oob(n, sz):
    code = r'''int main(){
  int n = %d;
  int a[%d] = {0};
  for (int i = 0; i < n; ++i) a[i] = i; // ''' % (n, sz) + SENT + r''' 当 n>=%d 时越界写
  return 0;
}
''' % sz
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "conditional_trigger", "expected_detectors": ["asan"],
             "expected_verdict": "catch", "severity": "high",
             "trigger_condition": f"n={n}（>= 数组大小 {sz}）时触发越界", "optimization_sensitivity": "n/a",
             "notes": f"仅当输入 n>= {sz} 时越界写；main 内构造触发输入，AddressSanitizer 抓。"})


def cond_uaf(flag):
    code = r'''int main(){
  int flag = %d;
  int* p = new int[4];
  if (flag) { delete[] p; }
  int v = p[0]; // ''' % flag + SENT + r''' flag 为真时 p 已释放 -> 释放后使用
  (void)v;
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "conditional_trigger", "expected_detectors": ["asan"],
             "expected_verdict": "catch", "severity": "high",
             "trigger_condition": f"flag={flag}（为真）时触发 UAF", "optimization_sensitivity": "n/a",
             "notes": f"仅当 flag={flag} 时释放后继续访问；main 内构造触发条件，AddressSanitizer 抓。"})


def cond_doublefree(input):
    code = r'''int main(){
  int input = %d;
  int* p = new int[2];
  if (input == %d) { delete[] p; } // ''' % (input, input) + SENT + r''' 特定输入时重复释放
  delete[] p;
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "conditional_trigger", "expected_detectors": ["asan"],
             "expected_verdict": "catch", "severity": "high",
             "trigger_condition": f"input=={input} 时触发双释放", "optimization_sensitivity": "n/a",
             "notes": f"仅当 input=={input} 时二次释放；main 内构造触发输入，AddressSanitizer 抓。"})


def cond_leak(input):
    code = r'''int main(){
  int input = %d;
  int* p = new int[8];
  if (input > 0) { return 0; } // ''' % input + SENT + r''' 特定分支提前返回 -> 泄漏
  delete[] p;
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "conditional_trigger", "expected_detectors": ["asan"],
             "expected_verdict": "catch", "severity": "high",
             "trigger_condition": f"input>0（input={input}）时提前返回触发泄漏", "optimization_sensitivity": "n/a",
             "notes": f"仅当 input>0 时走泄漏分支；main 内构造触发输入，LeakSanitizer 抓。"})


def cond_logic_offbyone(n):
    code = r'''int main(){
  int n = %d;
  int sum = 0;
  for (int i = 0; i <= n; ++i) sum += i; // ''' % n + SENT + r''' 边界 off-by-one：多算一项（结果错但无越界）
  (void)sum;
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "conditional_trigger", "expected_detectors": ["asan"],
             "expected_verdict": "miss", "severity": "low",
             "trigger_condition": f"n={n} 时循环多迭代一次（结果错误，但无内存越界）", "optimization_sensitivity": "n/a",
             "notes": f"off-by-one 导致结果错误但数组在界内；无 sanitizer 可抓（盲区）。触发条件由 main 构造，可复现。"})


def cond_trunc():
    code = r'''int main(){
  double d = 3.999;
  int r = (int)d; // ''' + SENT + r''' 浮点截断：r=3 而非 4（特定输入下逻辑错误）
  (void)r;
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "conditional_trigger", "expected_detectors": ["asan"],
             "expected_verdict": "miss", "severity": "low",
             "trigger_condition": "输入为 3.999（非整数）时截断丢精度", "optimization_sensitivity": "n/a",
             "notes": "浮点截断导致逻辑错误但无内存问题；无检测器可抓（盲区），触发可复现。"})


def cond_intdiv():
    code = r'''int main(){
  int total = 10, n = 3;
  int avg = total / n; // ''' + SENT + r''' 整数除法：avg=3 而非 3.33（特定输入下语义错误）
  (void)avg;
  return 0;
}
'''
    return ({"cpp": code}, "cpp", "main",
            {"defect_type": "conditional_trigger", "expected_detectors": ["asan"],
             "expected_verdict": "miss", "severity": "low",
             "trigger_condition": "total=10,n=3（不能整除）时取整丢精度", "optimization_sensitivity": "n/a",
             "notes": "整数除法语义错误（应为浮点）；无内存问题，无检测器可抓（盲区），触发可复现。"})


# ============================ 组装 200 ============================
PLAN = []
# move_semantics (30)
PLAN += [("ms_self", dict(name=n, field=f)) for n, f in
         [("A", "x"), ("Bx", "val"), ("Cc", "data"), ("Dd", "n"), ("Ee", "y"), ("Ff", "z"), ("Gg", "k"), ("Hh", "w")]]
PLAN += [("ms_retlocal", dict(kind=k)) for k in ["ref", "arr", "obj", "ref", "arr", "obj"]]
PLAN += [("ms_uaf_move", dict(t=t)) for t in ["string", "vector", "unique", "map", "string", "vector", "unique", "map", "string", "vector"]]
PLAN += [("ms_dblmove", dict(t=t)) for t in ["two", "lambda", "two", "lambda", "two", "lambda"]]
# raii_violation (30)
PLAN += [("raii_leak_exc", dict(n=n)) for n in [1, 0, 1, 0, 1, 0]]
PLAN += [("raii_mismatch", dict(kind=k)) for k in ["arrdel", "delarr", "malloc", "arrdel", "delarr", "malloc"]]
PLAN += [("raii_delnonvirt", dict(vm=0)) for _ in range(6)]
PLAN += [("raii_lock", {}) for _ in range(4)]
PLAN += [("raii_file", {}) for _ in range(4)]
PLAN += [("raii_exc_nonheap", {}) for _ in range(4)]
# virtual_function (30)
PLAN += [("vf_ctor", {}) for _ in range(5)]
PLAN += [("vf_dtor", {}) for _ in range(5)]
PLAN += [("vf_slice", {}) for _ in range(5)]
PLAN += [("vf_defarg", {}) for _ in range(5)]
PLAN += [("vf_hide", {}) for _ in range(5)]
PLAN += [("vf_uaf_virtual", {}) for _ in range(5)]
# cross_tu_ub (30)
PLAN += [("ct_strong", dict(fname=f"f{i}")) for i in range(8)]
PLAN += [("ct_inline", {}) for _ in range(8)]
PLAN += [("ct_initorder", {}) for _ in range(7)]
PLAN += [("ct_weakvar", {}) for _ in range(7)]
# optimization_dependent (40)
PLAN += [("opt_signedoverflow", {}) for _ in range(12)]
PLAN += [("opt_shift", {}) for _ in range(8)]
PLAN += [("opt_divzero", {}) for _ in range(8)]
PLAN += [("opt_strictalias", {}) for _ in range(12)]
# conditional_trigger (40)
PLAN += [("cond_oob", dict(n=n, sz=s)) for (n, s) in [(8, 4), (5, 4), (10, 6), (3, 2), (16, 8), (7, 4), (12, 8), (20, 10), (9, 5), (6, 3)]]
PLAN += [("cond_uaf", dict(flag=f)) for f in [1, 1, 1, 0, 1, 1]]
PLAN += [("cond_doublefree", dict(input=i)) for i in [7, 3, 9, 5, 2, 8]]
PLAN += [("cond_leak", dict(input=i)) for i in [1, 5, 9, 2, 4, 6]]
PLAN += [("cond_logic_offbyone", dict(n=n)) for n in [4, 10, 7, 3, 8, 12]]
PLAN += [("cond_trunc", {}) for _ in range(3)]
PLAN += [("cond_intdiv", {}) for _ in range(3)]

assert len(PLAN) == 200, f"PLAN size {len(PLAN)} != 200"


def main():
    from collections import Counter
    builders = {k: globals()[k] for k in
                ("ms_self", "ms_retlocal", "ms_uaf_move", "ms_dblmove",
                 "raii_leak_exc", "raii_mismatch", "raii_delnonvirt", "raii_lock",
                 "raii_file", "raii_exc_nonheap", "vf_ctor", "vf_dtor", "vf_slice",
                 "vf_defarg", "vf_hide", "vf_uaf_virtual", "ct_strong", "ct_inline",
                 "ct_initorder", "ct_weakvar", "opt_signedoverflow", "opt_shift",
                 "opt_divzero", "opt_strictalias", "cond_oob", "cond_uaf",
                 "cond_doublefree", "cond_leak", "cond_logic_offbyone", "cond_trunc",
                 "cond_intdiv")}
    manifest = {}
    for i, (name, kw) in enumerate(PLAN, 1):
        files, dsuf, dfunc, meta = builders[name](**kw)
        stem = emit(i, files, dsuf, dfunc, meta)
        manifest[stem] = meta
    json.dump(manifest, open(os.path.join(OUT, "manifest.json"), "w", encoding="utf-8"),
              ensure_ascii=False, indent=2)
    c = Counter(m["defect_type"] for m in manifest.values())
    vc = Counter((m["defect_type"], m["expected_verdict"]) for m in manifest.values())
    print(f"generated {len(manifest)} samples")
    for k, v in sorted(c.items()):
        cc = vc[(k, "catch")]; mm = vc[(k, "miss")]
        print(f"  {k}: {v} (catch={cc}, miss={mm})")


if __name__ == "__main__":
    main()
