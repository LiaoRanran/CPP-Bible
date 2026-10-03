#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""676c 扩样数据生成器（扩样-B）。
生成 100 个独立 C++ 缺陷候选样本 + JSON 标注，写入 data/expansion_676c_B/。
不修改任何现有文件，不修改检测器 tools/holdout_reveal_661.py。
缺陷类型受控词表（扩样-B）：data_race / integer_overflow / type_punning /
resource_leak / other_ub。
每个样本用 /*DEFECT: ...*/ 标记缺陷所在行，生成器据此自动算行号。
入池文件名用 sample_B001.. 前缀，避免与扩样-A(expA) 的 sample_001.. 冲突。
"""
import json
import os

REPO = "C:/CodeLearnling/note/note/C++/CPP-Bible"
OUT = os.path.join(REPO, "data", "expansion_676c_B")
os.makedirs(OUT, exist_ok=True)

TYPES = ["data_race", "integer_overflow", "type_punning",
         "resource_leak", "other_ub"]

S = []


def add(code, defect_type, func, severity, expected_verdict, expected_detectors, notes):
    assert code.count("/*DEFECT") == 1, "each sample needs exactly one /*DEFECT marker"
    S.append(dict(code=code, defect_type=defect_type, func=func,
                  severity=severity, expected_verdict=expected_verdict,
                  expected_detectors=expected_detectors, notes=notes))


# ===================== data_race (001-020) -> tsan catch =====================
def dr(code, notes, func="main", sev="high"):
    add(code, "data_race", func, sev, "catch", ["tsan"], notes)


dr(
"""#include <thread>
#include <cstdio>
int g = 0;
void f(){ for (int i = 0; i < 2000000; i++) g++; /*DEFECT: data race: concurrent RMW on g */ }
int main(){
  std::thread a(f), b(f);
  a.join(); b.join();
  std::printf("%d\\n", g);
  return 0;
}""", "两个线程无同步地对全局 g 做读-改-写（++），TSan 捕获数据竞争。")

dr(
"""#include <thread>
#include <cstdio>
int g = 0;
void w(){ for (int i = 0; i < 2000000; i++) g = i; /*DEFECT: data race: concurrent write to g */ }
void r(){ for (int i = 0; i < 2000000; i++) (void)g; /* racy read of g (also unsynchronized) */ }
int main(){
  std::thread a(w), b(r);
  a.join(); b.join();
  std::printf("%d\\n", g);
  return 0;
}""", "一个线程反复写 g、另一个反复读 g，TSan 捕获读写竞争。", func="main")

dr(
"""#include <thread>
#include <cstdio>
struct Counter { int x = 0; };
Counter c;
void f(){ for (int i = 0; i < 2000000; i++) c.x++; /*DEFECT: data race on member c.x */ }
int main(){
  std::thread a(f), b(f);
  a.join(); b.join();
  std::printf("%d\\n", c.x);
  return 0;
}""", "两个线程竞争修改结构体成员 c.x，TSan 捕获。", func="main")

dr(
"""#include <thread>
#include <cstdio>
int arr[4] = {0};
void f(){ for (int i = 0; i < 2000000; i++) arr[0]++; /*DEFECT: data race on arr[0] */ }
int main(){
  std::thread a(f), b(f);
  a.join(); b.join();
  std::printf("%d\\n", arr[0]);
  return 0;
}""", "两线程竞争同一数组元素，TSan 捕获。", func="main")

dr(
"""#include <thread>
#include <cstdio>
int* p = nullptr;
void w(){ for (int i = 0; i < 2000000; i++) *p = i; /*DEFECT: data race: concurrent write through p */ }
void r(){ for (int i = 0; i < 2000000; i++) (void)*p; /* racy read through p (also unsynchronized) */ }
int main(){
  int v = 0; p = &v;
  std::thread a(w), b(r);
  a.join(); b.join();
  std::printf("%d\\n", v);
  return 0;
}""", "两线程通过同一指针 p 竞争读写，TSan 捕获。", func="main")

dr(
"""#include <thread>
#include <cstdio>
int flag = 0;
void w(){ for (int i = 0; i < 2000000; i++) flag = 1; /*DEFECT: data race: concurrent write to flag */ }
void r(){ for (int i = 0; i < 2000000; i++) (void)flag; /* racy read of flag (also unsynchronized) */ }
int main(){
  std::thread a(w), b(r);
  a.join(); b.join();
  std::printf("%d\\n", flag);
  return 0;
}""", "写线程反复置 flag、读线程反复读，TSan 捕获竞争。", func="main")

dr(
"""#include <thread>
#include <cstdio>
int g = 0;
void f(){ for (int i = 0; i < 2000000; i++) g++; /*DEFECT: data race (compound RMW) */ }
int main(){
  std::thread t[2] = { std::thread(f), std::thread(f) };
  t[0].join(); t[1].join();
  std::printf("%d\\n", g);
  return 0;
}""", "数组形式起两个线程竞争 g，TSan 捕获。", func="main")

dr(
"""#include <thread>
#include <cstdio>
double d = 0.0;
void f(){ for (int i = 0; i < 2000000; i++) d += 1.0; /*DEFECT: data race on double d */ }
int main(){
  std::thread a(f), b(f);
  a.join(); b.join();
  std::printf("%f\\n", d);
  return 0;
}""", "浮点全局 d 被两线程并发 +=，TSan 捕获。", func="main")

dr(
"""#include <thread>
#include <cstdio>
int* heap = nullptr;
void f(){ for (int i = 0; i < 2000000; i++) *heap = i; /*DEFECT: data race on heap int */ }
int main(){
  int v = 0; heap = &v;
  std::thread a(f), b(f);
  a.join(); b.join();
  std::printf("%d\\n", v);
  return 0;
}""", "堆对象被两线程并发写，TSan 捕获。", func="main")

dr(
"""#include <thread>
#include <cstdio>
int g = 0;
void f(int n){ for (int i = 0; i < n; i++) g++; /*DEFECT: data race on g (passed-by-value count) */ }
int main(){
  std::thread a(f, 2000000), b(f, 2000000);
  a.join(); b.join();
  std::printf("%d\\n", g);
  return 0;
}""", "两线程各自传参循环竞争 g，TSan 捕获。", func="main")

dr(
"""#include <thread>
#include <cstdio>
bool done = false;
void w(){ for (int i = 0; i < 2000000; i++) done = true; /*DEFECT: data race on bool done */ }
void r(){ for (int i = 0; i < 2000000; i++) (void)done; /* racy read of done (also unsynchronized) */ }
int main(){
  std::thread a(w), b(r);
  a.join(); b.join();
  std::printf("%d\\n", (int)done);
  return 0;
}""", "布尔标志被写/读两线程并发访问，TSan 捕获。", func="main")

dr(
"""#include <thread>
#include <cstdio>
int* gp = nullptr;
void w(){ for (int i = 0; i < 2000000; i++) gp = (int*)&i; /*DEFECT: data race: concurrent pointer assignment */ }
int main(){
  int v = 0;
  std::thread a(w), b([&]{ for (int i=0;i<2000000;i++) (void)gp; }); /* racy read of gp (also unsynchronized) */
  a.join(); b.join();
  std::printf("%d\\n", v);
  return 0;
}""", "指针 gp 被一线程写、另一线程读，TSan 捕获。", func="main")

dr(
"""#include <thread>
#include <cstdio>
int g = 0;
void f(){ for (int i = 0; i < 2000000; i++) g++; /*DEFECT: data race in parallel loop */ }
int main(){
  std::thread t1(f), t2(f), t3(f);
  t1.join(); t2.join(); t3.join();
  std::printf("%d\\n", g);
  return 0;
}""", "三个线程并行循环竞争 g，TSan 捕获。", func="main")

dr(
"""#include <thread>
#include <cstdio>
int arr[4] = {0};
void f(){ for (int i = 0; i < 2000000; i++) arr[2]++; /*DEFECT: data race on arr[2] */ }
int main(){
  std::thread a(f), b(f);
  a.join(); b.join();
  std::printf("%d\\n", arr[2]);
  return 0;
}""", "两线程竞争 arr[2]，TSan 捕获。", func="main")

dr(
"""#include <thread>
#include <cstdio>
int g = 0;
void f(){ for (int i = 0; i < 2000000; i++) g++; /*DEFECT: data race (RMW) */ }
int main(){
  std::thread a(f);
  std::thread b(f);
  a.join(); b.join();
  std::printf("%d\\n", g);
  return 0;
}""", "以两个独立 thread 对象竞争 g，TSan 捕获。", func="main")

dr(
"""#include <thread>
#include <cstdio>
long long g = 0;
void f(){ for (int i = 0; i < 2000000; i++) g++; /*DEFECT: data race on long long g */ }
int main(){
  std::thread a(f), b(f);
  a.join(); b.join();
  std::printf("%lld\\n", g);
  return 0;
}""", "64 位全局计数器被两线程竞争，TSan 捕获。", func="main")

dr(
"""#include <thread>
#include <cstdio>
int g = 0;
void w(){ for (int i = 0; i < 2000000; i++) g = i; /*DEFECT: data race: write */ }
void w2(){ for (int i = 0; i < 2000000; i++) g = -i; /* racy write (also unsynchronized) */ }
int main(){
  std::thread a(w), b(w2);
  a.join(); b.join();
  std::printf("%d\\n", g);
  return 0;
}""", "两个线程都写 g（不同值），TSan 捕获写-写竞争。", func="main")

dr(
"""#include <thread>
#include <cstdio>
int main(){
  int v = 0;
  auto f = [&]{ for (int i = 0; i < 2000000; i++) v++; /*DEFECT: data race on captured local v */ };
  std::thread a(f), b(f);
  a.join(); b.join();
  std::printf("%d\\n", v);
  return 0;
}""", "局部变量被引用捕获后由两个线程并发 ++，TSan 捕获。")

dr(
"""#include <thread>
#include <cstdio>
int arr[4] = {0};
void f(){ for (int i = 0; i < 2000000; i++) arr[1]++; /*DEFECT: data race on arr[1] */ }
int main(){
  std::thread a(f), b(f);
  a.join(); b.join();
  std::printf("%d\\n", arr[1]);
  return 0;
}""", "两线程竞争 arr[1]，TSan 捕获。", func="main")

dr(
"""#include <thread>
#include <cstdio>
struct S { int x; int y; };
S s;
void w(){ for (int i = 0; i < 2000000; i++) s.y = i; /*DEFECT: data race on s.y */ }
void r(){ for (int i = 0; i < 2000000; i++) (void)s.y; /* racy read of s.y */ }
int main(){
  std::thread a(w), b(r);
  a.join(); b.join();
  std::printf("%d\\n", s.y);
  return 0;
}""", "一线程写结构体字段 s.y、另一线程读，TSan 捕获。", func="main")

# ===================== integer_overflow (021-040) -> ubsan catch =============
def iov(code, notes, sev="high"):
    add(code, "integer_overflow", "main", sev, "catch", ["ubsan"], notes)


iov(
"""#include <cstdio>
int main(){
  volatile int x = 2147483647;
  volatile int y = x + 1; /*DEFECT: signed integer overflow (add) */
  std::printf("%d\\n", (int)y);
  return 0;
}""", "有符号加法溢出，UBSan 运行时报 signed integer overflow；volatile 防常量折叠。")

iov(
"""#include <cstdio>
int main(){
  volatile int a = 46341;
  volatile int b = a * a; /*DEFECT: signed integer overflow (multiply) */
  std::printf("%d\\n", (int)b);
  return 0;
}""", "有符号乘法溢出，UBSan 捕获。")

iov(
"""#include <cstdio>
int main(){
  volatile int a = -2147483640;
  volatile int b = a - 100; /*DEFECT: signed integer overflow (subtract) */
  std::printf("%d\\n", (int)b);
  return 0;
}""", "有符号减法溢出，UBSan 捕获。")

iov(
"""#include <cstdio>
int main(){
  volatile int m = -2147483648;
  volatile int r = -m; /*DEFECT: unary minus overflow on INT_MIN */
  std::printf("%d\\n", (int)r);
  return 0;
}""", "对 INT_MIN 取负溢出，UBSan 捕获。")

iov(
"""#include <climits>
#include <cstdio>
int main(){
  volatile int m = INT_MIN;
  volatile int r = m / -1; /*DEFECT: INT_MIN / -1 overflow */
  std::printf("%d\\n", (int)r);
  return 0;
}""", "INT_MIN 除以 -1 溢出，UBSan 捕获。")

iov(
"""#include <cstdio>
int main(){
  volatile int a = 2000000000;
  a *= 2; /*DEFECT: signed overflow via *= */
  std::printf("%d\\n", (int)a);
  return 0;
}""", "复合赋值乘法溢出，UBSan 捕获。")

iov(
"""#include <cstdio>
int main(){
  volatile long long a = 5000000000LL;
  volatile long long b = a * 5; /*DEFECT: signed 64-bit overflow */
  std::printf("%lld\\n", b);
  return 0;
}""", "64 位有符号乘法溢出，UBSan 捕获。")

iov(
"""#include <cstdio>
int main(){
  volatile signed char c = 120;
  volatile signed char d = c + 20; /*DEFECT: signed char overflow */
  std::printf("%d\\n", (int)d);
  return 0;
}""", "有符号 char 溢出（UB），UBSan 捕获。")

iov(
"""#include <cstdio>
int main(){
  volatile short s = 30000;
  volatile short t = s * 2; /*DEFECT: short overflow */
  std::printf("%d\\n", (int)t);
  return 0;
}""", "short 溢出（UB），UBSan 捕获。")

iov(
"""#include <cstdio>
int main(){
  volatile int i = 0;
  for (volatile int k = 0; k < 2000000000; k++){ i++; /*DEFECT: overflow inside loop bound increment */ }
  std::printf("%d\\n", (int)i);
  return 0;
}""", "循环内 int 自增溢出，UBSan 捕获。")

iov(
"""#include <cstdio>
int main(){
  volatile int sum = 0;
  volatile int x = 2000000000;
  sum = sum + x + x; /*DEFECT: signed overflow in summation */
  std::printf("%d\\n", (int)sum);
  return 0;
}""", "累加导致有符号溢出，UBSan 捕获。")

iov(
"""#include <cstdio>
int main(){
  volatile int a = 100000;
  volatile int b = 100000;
  volatile int dot = a * b + a * b; /*DEFECT: overflow in dot-product-like expr */
  std::printf("%d\\n", (int)dot);
  return 0;
}""", "点积式表达式溢出，UBSan 捕获。")

iov(
"""#include <cstdio>
int main(){
  volatile int n = 13;
  volatile int f = 1;
  for (volatile int k = 2; k <= n; k++){ f = f * k; /*DEFECT: factorial overflow */ }
  std::printf("%d\\n", (int)f);
  return 0;
}""", "阶乘溢出（UB），UBSan 捕获。")

iov(
"""#include <cstdio>
int main(){
  volatile int x = 2000000000;
  volatile int y = x * 2 + 3; /*DEFECT: signed overflow (combined) */
  std::printf("%d\\n", (int)y);
  return 0;
}""", "组合算术溢出，UBSan 捕获。")

iov(
"""#include <cstdio>
int main(){
  volatile int m = -2147483648;
  volatile int r = m + m; /*DEFECT: INT_MIN+INT_MIN overflow */
  std::printf("%d\\n", (int)r);
  return 0;
}""", "INT_MIN 自加溢出（UB），UBSan 捕获。")

iov(
"""#include <cstdio>
int main(){
  volatile int a = 1500000000;
  volatile int b = 3;
  volatile int c = (a + b) * 2; /*DEFECT: signed overflow in parenthesized expr */
  std::printf("%d\\n", (int)c);
  return 0;
}""", "括号表达式内溢出，UBSan 捕获。")

iov(
"""#include <cstdio>
int main(){
  volatile int a = -100000;
  volatile int b = 100000;
  volatile int c = a * b; /*DEFECT: signed overflow (neg*pos large) */
  std::printf("%d\\n", (int)c);
  return 0;
}""", "负数大数乘法溢出，UBSan 捕获。")

iov(
"""#include <cstdio>
int main(){
  volatile int a = 2147483640;
  volatile int b = a - (-10); /*DEFECT: signed overflow in subtract (neg operand) */
  std::printf("%d\\n", (int)b);
  return 0;
}""", "减法因负操作数溢出，UBSan 捕获。")

iov(
"""#include <cstdio>
int main(){
  volatile int x = 123456789;
  volatile int y = x * x; /*DEFECT: signed overflow (square) */
  std::printf("%d\\n", (int)y);
  return 0;
}""", "平方导致溢出，UBSan 捕获。")

iov(
"""#include <cstdio>
int main(){
  volatile int a = -2000000000;
  volatile int b = a - 1000000000; /*DEFECT: signed overflow in subtraction (negative side) */
  std::printf("%d\\n", (int)b);
  return 0;
}""", "有符号减法在负侧溢出（UB），UBSan 捕获。")

# ===================== resource_leak (041-060) -> asan/LSan catch ============
def leak(code, notes, sev="medium", func="main"):
    add(code, "resource_leak", func, sev, "catch", ["asan"], notes)


leak(
"""#include <cstdio>
int main(){
  int* p = new int(1);
  std::printf("%d\\n", *p);
  /*DEFECT: resource leak: no delete (LSan reports at exit) */
  return 0;
}""", "new 后未 delete，LeakSanitizer 在退出时报告泄漏。")

leak(
"""#include <cstdio>
int main(){
  int* a = new int[10];
  a[0] = 1;
  std::printf("%d\\n", a[0]);
  /*DEFECT: resource leak: array new not deleted[] */
  return 0;
}""", "new[] 后未 delete[]，LSan 报告。")

leak(
"""#include <cstdlib>
#include <cstdio>
int main(){
  int* p = (int*)std::malloc(4 * sizeof(int));
  p[0] = 1;
  std::printf("%d\\n", p[0]);
  /*DEFECT: resource leak: malloc not freed */
  return 0;
}""", "malloc 后未 free，LSan 报告。")

leak(
"""#include <cstdio>
int* make(){ int* p = new int(7); return p; /*DEFECT: leak: caller never frees */ }
int main(){
  int* q = make();
  std::printf("%d\\n", *q);
  return 0;
}""", "函数内分配并返回，调用方未释放，LSan 报告。", func="make")

leak(
"""#include <cstdio>
int main(){
  int* p = new int(1);
  p = new int(2); /*DEFECT: resource leak: old pointer overwritten, lost */
  std::printf("%d\\n", *p);
  delete p;
  return 0;
}""", "指针被重新赋值覆盖，旧分配丢失泄漏。")

leak(
"""#include <cstdio>
int main(){
  for (int i = 0; i < 5; i++){
    int* p = new int(i); /*DEFECT: resource leak: per-iteration alloc never freed */
    std::printf("%d\\n", *p);
  }
  return 0;
}""", "循环内每次分配都未释放，LSan 报告多次泄漏。")

leak(
"""#include <cstdio>
int main(){
  FILE* f = std::fopen("nonexistent_676c.tmp", "r");
  /*DEFECT: resource leak: FILE* not closed (even if open failed) */
  return 0;
}""", "fopen 后未 fclose（文件描述符泄漏），LSan/ASan 可标记。")

leak(
"""#include <vector>
#include <cstdio>
int main(){
  std::vector<int*> v;
  for (int i = 0; i < 5; i++) v.push_back(new int(i));
  std::printf("%d\\n", v.size());
  /*DEFECT: resource leak: vector of pointers cleared without delete */
  return 0;
}""", "vector 持有裸指针但析构前未 delete，LSan 报告。")

leak(
"""#include <cstring>
#include <cstdio>
int main(){
  char* s = std::strdup("leak"); /*DEFECT: resource leak: strdup not freed */
  std::printf("%s\\n", s);
  return 0;
}""", "strdup 分配未 free，LSan 报告。")

leak(
"""#include <cstdio>
int* gp = new int(99);
int main(){
  std::printf("%d\\n", *gp);
  /*DEFECT: resource leak: global allocation never freed */
  return 0;
}""", "全局 new 分配未释放，LSan 报告。")

leak(
"""#include <cstdio>
int* ignored(){ int* p = new int(5); return p; }
int main(){
  ignored(); /*DEFECT: resource leak: returned allocation discarded */
  std::printf("ok\\n");
  return 0;
}""", "返回的分配被调用方丢弃，泄漏。", func="ignored")

leak(
"""#include <cstdio>
int main(){
  int* a = new int(1);
  int* b = new int(2);
  delete a;
  std::printf("%d\\n", *b);
  /*DEFECT: resource leak: b never deleted */
  return 0;
}""", "两处分配只释放一处，另一处泄漏。")

leak(
"""#include <cstdio>
int main(){
  if (true){ int* p = new int(1); std::printf("%d\\n", *p); /*DEFECT: leak inside branch, no delete */ }
  return 0;
}""", "分支内分配后无释放路径，LSan 报告。")

leak(
"""#include <cstdlib>
#include <cstdio>
int main(){
  int* p = (int*)std::malloc(8);
  int* q = (int*)std::realloc(p, 16); /*DEFECT: if realloc moves, old p lost; here discard p */
  std::printf("%d\\n", q ? 1 : 0);
  std::free(q);
  return 0;
}""", "realloc 后丢弃旧指针 p（移动即泄漏），LSan 报告。")

leak(
"""#include <cstdio>
int main(){
  int* p = new int(1);
  try { throw 1; } catch (...) { }
  std::printf("%d\\n", *p);
  /*DEFECT: resource leak: p not freed after exception path */
  return 0;
}""", "异常路径后未释放 p，LSan 退出时报告。")

leak(
"""#include <cstdio>
int recurse(int n){ int* p = new int(n); std::printf("%d\\n", *p); if (n>0) recurse(n-1); /*DEFECT: each frame leaks p */ return 0; }
int main(){ recurse(4); return 0; }""", "递归每帧分配未释放，多层泄漏。", func="recurse")

leak(
"""#include <cstdio>
int main(){
  FILE* f = std::fopen("676c_w.txt", "w");
  std::fprintf(f, "x");
  /*DEFECT: resource leak: fopen for write not closed */
  return 0;
}""", "写模式 fopen 后未 fclose，文件描述符泄漏。")

leak(
"""#include <cstdio>
int main(){
  int* p = new int(1);
  p[0] = 5;
  std::printf("%d\\n", p[0]);
  /*DEFECT: resource leak: forgot delete */
  return 0;
}""", "分配并使用后忘记 delete，LSan 报告。")

leak(
"""#include <cstdlib>
#include <cstdio>
int main(){
  void* p = std::malloc(1024);
  std::printf("%p\\n", p);
  /*DEFECT: resource leak: large malloc not freed */
  return 0;
}""", "大块 malloc 未 free，LSan 报告。")

leak(
"""#include <cstdlib>
#include <cstdio>
int main(){
  int* p = (int*)std::calloc(5, sizeof(int));
  p[0] = 1;
  std::printf("%d\\n", p[0]);
  /*DEFECT: resource leak: calloc not freed */
  return 0;
}""", "calloc 分配后未 free，LSan 报告（与 malloc 不同的分配器变体）。")

# ===================== type_punning (061-080) -> ubsan (catch/miss) ==========
def tp(code, verdict, notes, sev="medium"):
    add(code, "type_punning", "main", sev, verdict, ["ubsan"], notes)


# --- catch (misaligned punning, UBSan alignment 捕获) ---
tp(
"""#include <cstdio>
int main(){
  alignas(1) char buf[8] = {0};
  int* p = (int*)(buf + 1); /*DEFECT: misaligned int access (UB) -> UBSan alignment catch */
  *p = 5;
  std::printf("%d\\n", *p);
  return 0;
}""", "catch", "char 缓冲偏移 1 字节后以 int* 访问，未对齐，UBSan alignment 捕获。")

tp(
"""#include <cstdio>
int main(){
  char buf[8] = {0};
  long long* p = (long long*)(buf + 3); /*DEFECT: misaligned 8-byte access -> UBSan catch */
  *p = 1;
  std::printf("%lld\\n", *p);
  return 0;
}""", "catch", "char 缓冲偏移 3 后以 long long* 访问，未对齐，UBSan 捕获。")

tp(
"""#include <cstdio>
int main(){
  char buf[8] = {0};
  short* p = (short*)(buf + 1); /*DEFECT: misaligned short access -> UBSan catch */
  *p = 1;
  std::printf("%d\\n", (int)*p);
  return 0;
}""", "catch", "char 缓冲偏移 1 后以 short* 访问，未对齐，UBSan 捕获。")

tp(
"""#include <cstdio>
int main(){
  alignas(1) char b[16] = {0};
  double* p = (double*)(b + 1); /*DEFECT: misaligned double access -> UBSan catch */
  *p = 1.0;
  std::printf("%f\\n", *p);
  return 0;
}""", "catch", "char 缓冲偏移 1 后以 double* 访问（需 8 对齐），UBSan 捕获。")

tp(
"""#include <cstdio>
int main(){
  char buf[4] = {0};
  int* p = (int*)(buf + 2); /*DEFECT: misaligned int access -> UBSan catch */
  *p = 9;
  std::printf("%d\\n", *p);
  return 0;
}""", "catch", "char 缓冲偏移 2 后以 int* 访问，未对齐，UBSan 捕获。")

tp(
"""#include <cstdio>
int main(){
  char buf[16] = {0};
  float* p = (float*)(buf + 1); /*DEFECT: misaligned float access -> UBSan catch */
  *p = 1.0f;
  std::printf("%f\\n", *p);
  return 0;
}""", "catch", "char 缓冲偏移 1 后以 float* 访问，未对齐，UBSan 捕获。")

tp(
"""#include <cstdio>
int main(){
  char a[8] = {0};
  int* p = (int*)(a + 1);
  *p = 42; /*DEFECT: misaligned int punning write -> UBSan catch */
  std::printf("%d\\n", *p);
  return 0;
}""", "catch", "通过 char 缓冲错位做 int 类型双关写，未对齐，UBSan 捕获。")

tp(
"""#include <cstdio>
int main(){
  alignas(1) char s[12] = {0};
  int* p = (int*)(s + 5); /*DEFECT: misaligned int access -> UBSan catch */
  *p = 7;
  std::printf("%d\\n", *p);
  return 0;
}""", "catch", "char 缓冲偏移 5 后以 int* 访问，未对齐，UBSan 捕获。")

tp(
"""#include <cstdio>
int main(){
  char buf[8] = {0};
  int* p = (int*)(buf + 1); /*DEFECT: misaligned read+write punning -> UBSan catch */
  *p = *p + 1;
  std::printf("%d\\n", *p);
  return 0;
}""", "catch", "错位 int 双关读改写，未对齐，UBSan 捕获。")

tp(
"""#include <cstdio>
int main(){
  char b[16] = {0};
  double* p = (double*)(b + 7); /*DEFECT: misaligned double access -> UBSan catch */
  *p = 3.14;
  std::printf("%f\\n", *p);
  return 0;
}""", "catch", "char 缓冲偏移 7 后以 double* 访问，未对齐，UBSan 捕获。")

# --- miss (strict-aliasing / union, 无运行时陷阱, 盲区) ---
tp(
"""#include <cstdio>
int main(){
  int i = 0x3f800000;
  float f = *(float*)&i; /*DEFECT: strict-aliasing punning (UB); UBSan cannot trap at -O0/-O2 */
  std::printf("%f\\n", f);
  return 0;
}""", "miss", "把 int 存储当 float 读（严格别名违规 UB），对齐满足故 UBSan 无运行时报告，属检测器盲区（边界案例）。", sev="low")

tp(
"""#include <cstdio>
int main(){
  float f = 1.0f;
  int i = *(int*)&f; /*DEFECT: strict-aliasing punning (UB); no runtime trap */
  std::printf("%d\\n", i);
  return 0;
}""", "miss", "把 float 存储当 int 读（严格别名违规 UB），UBSan 抓不到（边界案例）。", sev="low")

tp(
"""#include <cstdio>
int main(){
  int i = 0;
  float f = reinterpret_cast<float&>(i); /*DEFECT: reinterpret_cast type pun (UB), no runtime trap */
  std::printf("%f\\n", f);
  return 0;
}""", "miss", "reinterpret_cast 把 int 双关成 float（UB），对齐满足，UBSan 无报告（边界案例）。", sev="low")

tp(
"""#include <cstdio>
union U { int i; float f; };
int main(){
  U u; u.i = 7;
  float x = u.f; /*DEFECT: union punning inactive member (UB in C++); no runtime trap */
  std::printf("%f\\n", x);
  return 0;
}""", "miss", "读取 union 非活跃成员（C++ 中 UB），UBSan 无运行时陷阱（边界案例）。", sev="low")

tp(
"""#include <cstdio>
int main(){
  int i = 42;
  short* sp = (short*)&i; /*DEFECT: int->short strict-aliasing pun (UB); aligned, no trap */
  short s = *sp;
  std::printf("%d\\n", (int)s);
  return 0;
}""", "miss", "int 以 short* 读（严格别名 UB），对齐满足，UBSan 不报（边界案例）。", sev="low")

tp(
"""#include <cstdio>
int main(){
  double d = 3.0;
  int* ip = (int*)&d; /*DEFECT: double->int strict-aliasing pun (UB); aligned, no trap */
  int x = *ip;
  std::printf("%d\\n", x);
  return 0;
}""", "miss", "double 存储以 int* 读（严格别名 UB），对齐满足，UBSan 不报（边界案例）。", sev="low")

tp(
"""#include <cstdio>
int main(){
  long L = 5;
  float* fp = (float*)&L; /*DEFECT: long->float strict-aliasing pun (UB); aligned, no trap */
  float x = *fp;
  std::printf("%f\\n", x);
  return 0;
}""", "miss", "long 以 float* 读（严格别名 UB），对齐满足，UBSan 不报（边界案例）。", sev="low")

tp(
"""#include <cstdio>
struct RGB { int r, g, b; };
struct BGR { int b, g, r; };
int main(){
  RGB c{1, 2,3};
  BGR* p = (BGR*)&c; /*DEFECT: reinterpret between layout-incompatible structs (UB); aligned */
  int x = p->r;
  std::printf("%d\\n", x);
  return 0;
}""", "miss", "把 RGB 结构按 BGR 解释（严格别名 UB），对齐满足，UBSan 不报（边界案例）。", sev="low")

tp(
"""#include <cstdio>
int main(){
  int i = 0x40490FDB;
  float f = *(float*)&i; /*DEFECT: int->float punning (UB); same 4-byte alignment, no trap */
  std::printf("%f\\n", f);
  return 0;
}""", "miss", "int 与 float 同 4 字节对齐双关（严格别名 UB），UBSan 无运行时报告（边界案例）。", sev="low")

tp(
"""#include <cstdio>
int main(){
  long long L = 0x3FF0000000000000LL;
  double d = reinterpret_cast<double&>(L); /*DEFECT: reinterpret long long as double (UB); aligned, no trap */
  std::printf("%f\\n", d);
  return 0;
}""", "miss", "把 long long 存储按 double 重解释（严格别名 UB），对齐满足，UBSan 无报告（边界案例）。", sev="low")

# ===================== other_ub (081-100) -> ubsan/asan (catch/miss) =========
def oub(code, verdict, detectors, notes, sev="high"):
    add(code, "other_ub", "main", sev, verdict, detectors, notes)


oub(
"""#include <cstdio>
int main(){
  volatile int b = 0;
  int c = 5 / b; /*DEFECT: division by zero (UB) */
  std::printf("%d\\n", c);
  return 0;
}""", "catch", ["ubsan"], "除以零（UB），UBSan 报 division by zero。")

oub(
"""#include <cstdio>
int main(){
  volatile int b = 0;
  int c = 5 % b; /*DEFECT: modulo by zero (UB) */
  std::printf("%d\\n", c);
  return 0;
}""", "catch", ["ubsan"], "取模除以零（UB），UBSan 捕获。")

oub(
"""#include <cstdio>
int main(){
  volatile int x = 1;
  volatile int y = x << 40; /*DEFECT: shift count >= width (UB) */
  std::printf("%d\\n", (int)y);
  return 0;
}""", "catch", ["ubsan"], "移位量 >= 类型宽度（UB），UBSan 捕获。")

oub(
"""#include <cstdio>
int main(){
  volatile int x = 1;
  volatile int c = -2;
  volatile int y = x << c; /*DEFECT: negative shift count (UB) */
  std::printf("%d\\n", (int)y);
  return 0;
}""", "catch", ["ubsan"], "负移位量（UB），UBSan 捕获。")

oub(
"""#include <cstdio>
int main(){
  volatile int x = -1;
  volatile int y = x << 2; /*DEFECT: left shift of negative value (UB) */
  std::printf("%d\\n", (int)y);
  return 0;
}""", "catch", ["ubsan"], "对负值左移（UB），UBSan 捕获。")

oub(
"""#include <cstdio>
int main(){
  volatile int x = 1;
  volatile int y = x << 31; /*DEFECT: left shift into sign bit (UB) */
  std::printf("%d\\n", (int)y);
  return 0;
}""", "catch", ["ubsan"], "左移进入符号位（UB），UBSan 捕获。")

oub(
"""#include <cstdio>
int main(){
  char* s = (char*)"hello";
  s[0] = 'H'; /*DEFECT: modify string literal (UB) -> ASan RO write */
  std::printf("%s\\n", s);
  return 0;
}""", "catch", ["asan"], "修改字符串字面量（UB），写入只读段，ASan 捕获。")

oub(
"""#include <cstdio>
int main(){
  void (*fp)() = nullptr;
  fp(); /*DEFECT: call through null function pointer (UB) -> ASan */
  return 0;
}""", "catch", ["asan"], "通过空函数指针调用（UB），ASan 捕获空解引用。")

oub(
"""#include <cstring>
#include <cstdio>
int main(){
  int dst[4] = {0};
  std::memcpy(dst, nullptr, 4 * sizeof(int)); /*DEFECT: memcpy from null source (UB) -> ASan */
  std::printf("%d\\n", dst[0]);
  return 0;
}""", "catch", ["asan"], "memcpy 以空指针为源（UB），ASan 捕获空读。")

oub(
"""#include <cstdio>
struct S { void f(){ std::printf("ok\\n"); } };
int main(){
  S* s = nullptr;
  s->f(); /*DEFECT: call member function through null pointer (UB) -> ASan */
  return 0;
}""", "catch", ["asan"], "通过空对象指针调成员函数（UB），ASan 捕获。")

oub(
"""#include <cstdio>
int main(){
  alignas(1) char buf[8] = {0};
  int* p = (int*)(buf + 1); /*DEFECT: misaligned access (UB) -> UBSan alignment catch */
  *p = 5;
  std::printf("%d\\n", *p);
  return 0;
}""", "catch", ["ubsan"], "未对齐访问（UB），UBSan alignment 捕获。")

oub(
"""#include <cstdio>
int main(){
  int x = 0x1;
  int y = x << 32; /*DEFECT: shift by exactly width (UB) -> UBSan catch */
  std::printf("%d\\n", (int)y);
  return 0;
}""", "catch", ["ubsan"], "移位量恰等于类型宽度（UB），UBSan 捕获。")

oub(
"""#include <cstdio>
int main(){
  int* p = nullptr;
  *p = 5; /*DEFECT: null pointer dereference (UB) -> ASan */
  return 0;
}""", "catch", ["asan"], "空指针解引用写（UB），ASan 捕获。")

oub(
"""#include <cstdio>
int main(){
  int i = 0;
  int a[3];
  a[i++] = i++ + i++; /*DEFECT: unsequenced modification/access (UB); wunsequenced N/A here -> blind spot */
  std::printf("%d\\n", a[0]);
  return 0;
}""", "miss", ["ubsan"], "未序列化的多次修改/读取同一变量（UB）。本机 wunsequenced 资产对 MinGW 不可用（unknown），UBSan 无运行时陷阱，属盲区（边界案例）。", sev="low")

oub(
"""#include <cstdio>
int f(int x, int y){ return x + y; }
int main(){
  volatile int i = 0;
  int r = f(i++, i++); /*DEFECT: unsequenced function args (UB); no runtime trap */
  std::printf("%d\\n", r);
  return 0;
}""", "miss", ["ubsan"], "函数实参求值顺序未定（UB）。UBSan 无运行时陷阱，属盲区（边界案例）。", sev="low", )

oub(
"""#include <cstdio>
int main(){
  int a[3] = {0};
  int i = 0;
  a[i] = i++ * 2; /*DEFECT: unsequenced: i used and modified in same full-expression (UB) */
  std::printf("%d\\n", a[0]);
  return 0;
}""", "miss", ["ubsan"], "同一全表达式内 i 被改又被用（UB）。UBSan 无运行时陷阱，盲区（边界案例）。", sev="low")

oub(
"""#include <cstdio>
int main() noexcept {
  throw 1; /*DEFECT: throwing out of noexcept (UB); std::terminate, no sanitizer trap */
  return 0;
}""", "miss", ["asan"], "在 noexcept 函数中抛异常（UB），运行期 terminate；ASan/UBSan 均不报，属盲区（边界案例）。", sev="low")

oub(
"""#include <cstdio>
struct D { ~D() noexcept(false) { throw 2; } };
int main(){
  try { D d; } catch (...) { } /*DEFECT: destructor throws (UB when unwinding); terminate, no trap */
  std::printf("done\\n");
  return 0;
}""", "miss", ["asan"], "析构函数抛异常（展开期 UB），运行期 terminate；无 sanitizer 陷阱，盲区（边界案例）。", sev="low")

oub(
"""#include <cstdio>
union U { int i; double d; };
int main(){
  U u; u.d = 3.14;
  int x = u.i; /*DEFECT: inactive union member read (UB); aligned, no runtime trap */
  std::printf("%d\\n", x);
  return 0;
}""", "miss", ["ubsan"], "读 union 非活跃成员 double→int（UB），对齐满足，UBSan 不报（边界案例）。", sev="low")

oub(
"""#include <cstdio>
int main(){
  int i = 0x3f800000;
  float f = *(float*)&i; /*DEFECT: strict-aliasing (UB); aligned, no runtime trap */
  std::printf("%f\\n", f);
  return 0;
}""", "miss", ["ubsan"], "int/float 严格别名双关（UB），对齐满足，UBSan 无报告（边界案例）。", sev="low")



# ============================ write files ============================
def defect_line(code: str) -> int:
    for i, ln in enumerate(code.splitlines(), 1):
        if "/*DEFECT" in ln:
            return i
    raise RuntimeError("no DEFECT marker")


assert len(S) == 100, f"expected 100, got {len(S)}"

summary = {t: 0 for t in TYPES}
for idx, s in enumerate(S, 1):
    sid = f"sample_B{idx:03d}"
    dt = s["defect_type"]
    assert dt in TYPES, dt
    summary[dt] += 1
    dline = defect_line(s["code"])
    cpp = (
        f"// {sid}\n"
        f"// defect_type: {dt}\n"
        f"// severity: {s['severity']}\n"
        f"// planted: true\n"
        f"// expected_verdict: {s['expected_verdict']}\n"
        f"// expected_detectors: {','.join(s['expected_detectors'])}\n"
        f"// (authoritative annotation in {sid}.json)\n\n"
        + s["code"]
    )
    with open(os.path.join(OUT, f"{sid}.cpp"), "w", encoding="utf-8") as f:
        f.write(cpp)
    ann = {
        "sample_id": sid,
        "defect_type": dt,
        "defect_location": {"line": dline, "function": s["func"]},
        "severity": s["severity"],
        "planted": True,
        "expected_verdict": s["expected_verdict"],
        "expected_detectors": s["expected_detectors"],
        "notes": s["notes"],
    }
    with open(os.path.join(OUT, f"{sid}.json"), "w", encoding="utf-8") as f:
        json.dump(ann, f, ensure_ascii=False, indent=2)

print("generated", len(S), "samples (扩样-B)")
print("by type:", summary)
print("expected verdict:",
      {v: sum(1 for x in S if x["expected_verdict"] == v) for v in ("catch", "miss")})
print("planted=true:", len(S), "(all samples are planted per design)")
