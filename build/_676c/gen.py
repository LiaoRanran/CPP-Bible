#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""676c 扩样数据生成器（扩样-A）。
生成 100 个独立 C++ 缺陷候选样本 + JSON 标注，写入 data/expansion_676c/。
不修改任何现有文件，不修改检测器 tools/holdout_reveal_661.py。
缺陷类型受控词表：undefined_behavior / memory_safety / uninitialized_read /
null_pointer_deref / out_of_bounds。
每个样本代码里用 /*DEFECT: ...*/ 标记缺陷所在行（生成器据此自动算行号）。
"""
import json
import os

REPO = "C:/CodeLearnling/note/note/C++/CPP-Bible"
OUT = os.path.join(REPO, "data", "expansion_676c")
os.makedirs(OUT, exist_ok=True)

# 受控词表
TYPES = ["undefined_behavior", "memory_safety", "uninitialized_read",
         "null_pointer_deref", "out_of_bounds"]

# 每个样本: code(含 /*DEFECT*/ 标记), defect_type, func, severity,
#           expected_verdict, expected_detectors, notes
S = []


def add(code, defect_type, func, severity, expected_verdict, expected_detectors, notes):
    assert code.count("/*DEFECT") == 1, "each sample needs exactly one /*DEFECT marker"
    S.append(dict(code=code, defect_type=defect_type, func=func,
                  severity=severity, expected_verdict=expected_verdict,
                  expected_detectors=expected_detectors, notes=notes))


# ============================ memory_safety (001-020) -> asan catch ==========
add(
"""#include <cstdio>
int main(){
  int* p = new int[4];
  delete[] p;
  p[0] = 42; /*DEFECT: use-after-free write (heap) */
  std::printf("%d\\n", p[0]);
  return 0;
}""", "memory_safety", "main", "high", "catch", ["asan"],
    "释放后写堆内存。ASan 在 -O0/-O2 均能在运行时捕获 use-after-free。触发靠 p[0]=42 真正落盘。")

add(
"""#include <cstdio>
int main(){
  int* p = new int[4];
  delete[] p;
  int x = p[0]; /*DEFECT: use-after-free read (heap) */
  std::printf("%d\\n", x);
  return 0;
}""", "memory_safety", "main", "high", "catch", ["asan"],
    "释放后读堆内存。ASan 运行时捕获 UAF 读。")

add(
"""#include <cstdio>
int main(){
  int* p = new int(1);
  delete p;
  delete p; /*DEFECT: double-free */
  return 0;
}""", "memory_safety", "main", "high", "catch", ["asan"],
    "对同一指针二次释放。ASan/LSan 报告 double-free。")

add(
"""#include <cstdio>
int main(){
  int* a = new int[3];
  a[5] = 1; /*DEFECT: heap buffer overflow (write past end) */
  std::printf("%d\\n", a[5]);
  delete[] a;
  return 0;
}""", "memory_safety", "main", "high", "catch", ["asan"],
    "堆数组越界写，越界量（索引5 vs 大小3）远超 redzone，ASan 必捕。")

add(
"""#include <cstdio>
int main(){
  int* a = new int[3];
  int x = a[10]; /*DEFECT: heap buffer overflow (read far past end) */
  std::printf("%d\\n", x);
  delete[] a;
  return 0;
}""", "memory_safety", "main", "high", "catch", ["asan"],
    "堆数组远越界读，ASan 捕获 heap-buffer-overflow。")

add(
"""#include <cstdio>
int main(){
  int b[4] = {0};
  b[8] = 1; /*DEFECT: stack buffer overflow (write) */
  std::printf("%d\\n", b[8]);
  return 0;
}""", "memory_safety", "main", "high", "catch", ["asan"],
    "栈数组越界写，ASan 栈 redzone 捕获 stack-buffer-overflow。")

add(
"""#include <cstdio>
int main(){
  int b[4] = {0};
  int x = b[10]; /*DEFECT: stack buffer overflow (read) */
  std::printf("%d\\n", x);
  return 0;
}""", "memory_safety", "main", "high", "catch", ["asan"],
    "栈数组越界读，ASan 捕获。")

add(
"""#include <cstdio>
int g[4] = {0};
int main(){
  g[10] = 5; /*DEFECT: global buffer overflow (write) */
  std::printf("%d\\n", g[10]);
  return 0;
}""", "memory_safety", "main", "high", "catch", ["asan"],
    "全局数组越界写，ASan 全局 redzone 捕获。")

add(
"""#include <cstdlib>
#include <cstdio>
int main(){
  int* p = (int*)std::malloc(4 * sizeof(int));
  int* q = (int*)std::realloc(p, 8 * sizeof(int));
  *p = 1; /*DEFECT: use-after-realloc (p freed by realloc) */
  std::printf("%d\\n", *p);
  std::free(q);
  return 0;
}""", "memory_safety", "main", "high", "catch", ["asan"],
    "realloc 释放旧指针 p 后仍通过 p 写，ASan 捕获 UAF。")

add(
"""#include <cstdio>
int main(){
  int* p = new int(1);
  int* q = p;
  delete p;
  delete q; /*DEFECT: double-free via aliased pointer */
  return 0;
}""", "memory_safety", "main", "high", "catch", ["asan"],
    "别名指针重复释放，ASan 报告 double-free。")

add(
"""#include <vector>
#include <cstdio>
int main(){
  std::vector<int> v(4);
  int* d = v.data();
  v.clear();
  d[0] = 1; /*DEFECT: use-after-free via cleared vector's data() */
  std::printf("%d\\n", d[0]);
  return 0;
}""", "memory_safety", "main", "high", "catch", ["asan"],
    "vector clear 后其 data() 指针悬空，再写即 UAF，ASan 捕获。")

add(
"""#include <cstring>
#include <cstdio>
int main(){
  int dst[2] = {0};
  int src[5] = {1,2,3,4,5};
  std::memcpy(dst, src, 5 * sizeof(int)); /*DEFECT: memcpy overflow (5>2) */
  std::printf("%d\\n", dst[1]);
  return 0;
}""", "memory_safety", "main", "high", "catch", ["asan"],
    "memcpy 目的小于源，ASan 在 memcpy 处报 stack-buffer-overflow。")

add(
"""#include <cstring>
#include <cstdio>
int main(){
  int a[3] = {0};
  std::memset(a, 0, 10 * sizeof(int)); /*DEFECT: memset overflow */
  std::printf("%d\\n", a[0]);
  return 0;
}""", "memory_safety", "main", "high", "catch", ["asan"],
    "memset 写入长度超过数组，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  int a[4] = {0};
  int i = -3;
  a[i] = 1; /*DEFECT: negative-index out-of-bounds write */
  std::printf("%d\\n", a[i]);
  return 0;
}""", "memory_safety", "main", "high", "catch", ["asan"],
    "负索引越界写，ASan 捕获（underflow）。")

add(
"""#include <cstdio>
int main(){
  int* p = new int(0);
  for (int k = 0; k < 2; k++){
    delete p;
    p[0] = k; /*DEFECT: use-after-free inside loop */
  }
  std::printf("%d\\n", p[0]);
  return 0;
}""", "memory_safety", "main", "high", "catch", ["asan"],
    "循环内释放后立即写，ASan 捕获 UAF。")

add(
"""#include <cstring>
#include <cstdio>
int main(){
  char buf[4] = {0};
  std::strcpy(buf, "abcdef"); /*DEFECT: strcpy buffer overflow */
  std::printf("%s\\n", buf);
  return 0;
}""", "memory_safety", "main", "high", "catch", ["asan"],
    "strcpy 写入超 buf 容量，ASan 捕获 stack-buffer-overflow。")

add(
"""#include <cstdio>
int main(){
  int* a = new int[4];
  int* q = a + 6;
  *q = 9; /*DEFECT: out-of-bounds via pointer arithmetic */
  std::printf("%d\\n", *q);
  delete[] a;
  return 0;
}""", "memory_safety", "main", "high", "catch", ["asan"],
    "指针算术越过分配边界写，ASan 捕获 heap-buffer-overflow。")

add(
"""#include <cstdio>
int* leak(){
  int* p = new int(7);
  return p;
}
int main(){
  int* p = leak();
  delete p;
  std::printf("%d\\n", *p); /*DEFECT: use-after-free after delete */
  return 0;
}""", "memory_safety", "leak", "high", "catch", ["asan"],
    "函数返回堆指针，main 释放后解引用，ASan 捕获 UAF。")

add(
"""#include <cstdio>
int main(){
  int* p = new int[100];
  p[0] = 1;
  /*DEFECT: memory leak (no delete) -- LSan reports at exit */
  std::printf("%d\\n", p[0]);
  return 0;
}""", "memory_safety", "main", "medium", "catch", ["asan"],
    "分配后未释放，ASan 套件内的 LeakSanitizer 在退出时报告泄漏。")

# ============================ null_pointer_deref (021-040) -> asan catch ====
add(
"""#include <cstdio>
int main(){
  int* p = nullptr;
  std::printf("%d\\n", *p); /*DEFECT: null pointer dereference (read) */
  return 0;
}""", "null_pointer_deref", "main", "high", "catch", ["asan"],
    "解引用空指针读，ASan 报告 SEGV/null。")

add(
"""#include <cstdio>
int main(){
  int* p = nullptr;
  *p = 5; /*DEFECT: null pointer dereference (write) */
  return 0;
}""", "null_pointer_deref", "main", "high", "catch", ["asan"],
    "解引用空指针写，ASan 捕获。")

add(
"""#include <cstdio>
int* getnull(){ return nullptr; }
int main(){
  int* p = getnull();
  std::printf("%d\\n", *p); /*DEFECT: null pointer dereference */
  return 0;
}""", "null_pointer_deref", "getnull", "high", "catch", ["asan"],
    "函数返回空指针后在 main 解引用，ASan 捕获。")

add(
"""#include <cstdio>
struct S { int x; };
int main(){
  S* s = nullptr;
  s->x = 3; /*DEFECT: null pointer member write */
  return 0;
}""", "null_pointer_deref", "main", "high", "catch", ["asan"],
    "通过空结构体指针写成员，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  int* p = nullptr;
  p[0] = 1; /*DEFECT: null pointer array write */
  return 0;
}""", "null_pointer_deref", "main", "high", "catch", ["asan"],
    "以空指针作数组基地址写，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  int* p = nullptr;
  int a = *p; int b = *p; /*DEFECT: repeated null pointer dereference */
  std::printf("%d\\n", a + b);
  return 0;
}""", "null_pointer_deref", "main", "high", "catch", ["asan"],
    "两次解引用空指针，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  int* p = nullptr;
  int& r = *p;
  std::printf("%d\\n", r); /*DEFECT: null reference dereference */
  return 0;
}""", "null_pointer_deref", "main", "high", "catch", ["asan"],
    "绑定空引用并读取，ASan 在读取处捕获。")

add(
"""#include <cstdio>
void f(int* q){ std::printf("%d\\n", *q); /*DEFECT: null deref in callee */ }
int main(){ f(nullptr); return 0; }""", "null_pointer_deref", "f", "high", "catch", ["asan"],
    "空指针作为参数传入函数后解引用，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  int* p = nullptr;
  if (p == nullptr) { /* no-op guard */ }
  std::printf("%d\\n", *p); /*DEFECT: null deref despite guard */
  return 0;
}""", "null_pointer_deref", "main", "high", "catch", ["asan"],
    "空守卫未改值，仍解引用空指针，ASan 捕获。")

add(
"""#include <cstdio>
int* bad(){ int* p = nullptr; return p; }
int main(){
  int* q = bad();
  std::printf("%d\\n", *q); /*DEFECT: null deref of returned pointer */
  return 0;
}""", "null_pointer_deref", "bad", "high", "catch", ["asan"],
    "返回空指针并在 main 解引用，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  int* p = nullptr;
  for (int i = 0; i < 3; i++){ std::printf("%d\\n", *p); /*DEFECT: null deref in loop */ }
  return 0;
}""", "null_pointer_deref", "main", "high", "catch", ["asan"],
    "循环内反复解引用空指针，ASan 捕获。")

add(
"""#include <cstdio>
struct S { int* p; };
int main(){
  S s;
  s.p = nullptr;
  std::printf("%d\\n", *s.p); /*DEFECT: null deref of member pointer */
  return 0;
}""", "null_pointer_deref", "main", "high", "catch", ["asan"],
    "成员指针为空后解引用，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  void* v = nullptr;
  int* p = (int*)v;
  std::printf("%d\\n", *p); /*DEFECT: null deref after cast */
  return 0;
}""", "null_pointer_deref", "main", "high", "catch", ["asan"],
    "void* 空转 int* 后解引用，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  int* p = nullptr;
  int x = p ? *p : *p; /*DEFECT: null deref in both ternary branches */
  std::printf("%d\\n", x);
  return 0;
}""", "null_pointer_deref", "main", "high", "catch", ["asan"],
    "三目两侧都解引用空指针，ASan 捕获。")

add(
"""#include <cstdio>
int* gp = nullptr;
int main(){
  std::printf("%d\\n", *gp); /*DEFECT: null deref of global pointer */
  return 0;
}""", "null_pointer_deref", "main", "high", "catch", ["asan"],
    "全局空指针解引用，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  auto l = [](int* q){ std::printf("%d\\n", *q); /*DEFECT: null deref in lambda */ };
  l(nullptr);
  return 0;
}""", "null_pointer_deref", "main", "high", "catch", ["asan"],
    "lambda 内解引用空指针，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  int* p = nullptr;
  int* q = p + 5;
  std::printf("%d\\n", *q); /*DEFECT: null pointer + offset dereference */
  return 0;
}""", "null_pointer_deref", "main", "high", "catch", ["asan"],
    "空指针加偏移后解引用，ASan 捕获。")

add(
"""#include <cstdio>
int** pp = nullptr;
int main(){
  std::printf("%d\\n", **pp); /*DEFECT: null double-pointer dereference */
  return 0;
}""", "null_pointer_deref", "main", "high", "catch", ["asan"],
    "二级空指针解引用，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  int* p = nullptr;
  while (true){ std::printf("%d\\n", *p); /*DEFECT: null deref in while */ break; }
  return 0;
}""", "null_pointer_deref", "main", "high", "catch", ["asan"],
    "while 内解引用空指针，ASan 捕获。")

add(
"""#include <cstdio>
int& bad(){ int* p = nullptr; return *p; }
int main(){
  std::printf("%d\\n", bad()); /*DEFECT: null reference returned and used */
  return 0;
}""", "null_pointer_deref", "bad", "high", "catch", ["asan"],
    "返回空引用并立即使用，ASan 捕获。")

# ============================ out_of_bounds (041-060) -> asan catch =========
add(
"""#include <cstdio>
int main(){
  int* a = new int[3];
  a[3] = 1; /*DEFECT: heap buffer overflow (off-by-one write) */
  std::printf("%d\\n", a[3]);
  delete[] a;
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "堆数组 off-by-one 写，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  int* a = new int[3];
  int x = a[100]; /*DEFECT: heap buffer overflow (read) */
  std::printf("%d\\n", x);
  delete[] a;
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "堆数组远越界读，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  int b[3] = {0};
  b[5] = 2; /*DEFECT: stack buffer overflow (write) */
  std::printf("%d\\n", b[5]);
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "栈数组越界写，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  int b[3] = {0};
  int x = b[-1]; /*DEFECT: stack buffer underflow (read) */
  std::printf("%d\\n", x);
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "栈数组负索引读，ASan 捕获。")

add(
"""#include <vector>
#include <cstdio>
int main(){
  std::vector<int> v(3);
  v[5] = 1; /*DEFECT: std::vector out-of-bounds write */
  std::printf("%d\\n", v[5]);
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "vector::operator[] 不做边界检查，越界写被 ASan 捕获。")

add(
"""#include <vector>
#include <cstdio>
int main(){
  std::vector<int> v(3);
  int x = v[10]; /*DEFECT: std::vector out-of-bounds read */
  std::printf("%d\\n", x);
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "vector 越界读，ASan 捕获。")

add(
"""#include <string>
#include <cstdio>
int main(){
  std::string s = "abc";
  char c = s[5]; /*DEFECT: std::string out-of-bounds read */
  std::printf("%c\\n", c);
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "std::string::operator[] 越界读，ASan 捕获。")

add(
"""#include <cstdio>
void f(int* a){ a[10] = 1; /*DEFECT: out-of-bounds write in callee */ }
int main(){ int b[4] = {0}; f(b); std::printf("%d\\n", b[0]); return 0; }""",
    "out_of_bounds", "f", "high", "catch", ["asan"],
    "被调函数对传入的小数组越界写，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  int a[4] = {0};
  for (int i = 0; i <= 4; i++){ a[i] = i; /*DEFECT: off-by-one OOB at i=4 */ }
  std::printf("%d\\n", a[3]);
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "循环条件 i<=4 导致末次越界写，ASan 捕获。")

add(
"""#include <cstring>
#include <cstdio>
int main(){
  int dst[2] = {0};
  int src[2] = {1, 2};
  std::memcpy(dst, src, 4 * sizeof(int)); /*DEFECT: memcpy overflow (4>2) */
  std::printf("%d\\n", dst[1]);
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "memcpy 长度超出目的，ASan 捕获。")

add(
"""#include <cstring>
#include <cstdio>
int main(){
  int a[2] = {0};
  std::memset(a, 0, 5 * sizeof(int)); /*DEFECT: memset overflow */
  std::printf("%d\\n", a[0]);
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "memset 长度超出数组，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  int a[4] = {0};
  int* p = a; p = p + 10; *p = 1; /*DEFECT: OOB via pointer arithmetic */
  std::printf("%d\\n", *p);
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "指针算术越过分配边界写，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  int m[3][3] = {{0}};
  m[0][9] = 1; /*DEFECT: row out-of-bounds write */
  std::printf("%d\\n", m[0][9]);
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "二维数组行内越界写，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  char s[5] = "hello";
  char c = s[10]; /*DEFECT: char array out-of-bounds read */
  std::printf("%c\\n", c);
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "char 数组越界读，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  int a[3] = {0};
  const int idx = 7;
  a[idx] = 1; /*DEFECT: constant-index out-of-bounds write */
  std::printf("%d\\n", a[idx]);
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "常量索引越界写，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  int a[3] = {0};
  int i = 0;
  while (i < 10){ a[i] = i; /*DEFECT: OOB when i>=3 */ i++; }
  std::printf("%d\\n", a[2]);
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "while 越界写，ASan 捕获。")

add(
"""#include <cstdio>
int ga[3] = {0};
int main(){
  ga[8] = 1; /*DEFECT: global buffer out-of-bounds write */
  std::printf("%d\\n", ga[8]);
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "全局数组越界写，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  char buf[4] = {0};
  std::snprintf(buf, 10, "abcdef"); /*DEFECT: snprintf overflow (10>4) */
  std::printf("%s\\n", buf);
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "snprintf 长度参数超出缓冲区，ASan 捕获。")

add(
"""#include <algorithm>
#include <cstdio>
int main(){
  int a[3] = {0};
  int b[5] = {1,2,3,4,5};
  std::copy(b, b + 5, a); /*DEFECT: std::copy overflow (5 into size-3) */
  std::printf("%d\\n", a[2]);
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "std::copy 写入超出目的大小，ASan 捕获。")

add(
"""#include <array>
#include <cstdio>
int main(){
  std::array<int,3> a{};
  int x = a[5]; /*DEFECT: std::array out-of-bounds read */
  std::printf("%d\\n", x);
  return 0;
}""", "out_of_bounds", "main", "high", "catch", ["asan"],
    "std::array::operator[] 不做边界检查，越界读被 ASan 捕获。")

# ===================== undefined_behavior (061-080) -> ubsan/asan ===========
add(
"""#include <cstdio>
int main(){
  volatile int x = 2147483647;
  volatile int y = x + 1; /*DEFECT: signed integer overflow (add) */
  std::printf("%d\\n", (int)y);
  return 0;
}""", "undefined_behavior", "main", "high", "catch", ["ubsan"],
    "有符号整数加法溢出（UB），UBSan 在运行时报 signed integer overflow。用 volatile 防常量折叠。")

add(
"""#include <cstdio>
int main(){
  volatile int a = 46341;
  volatile int b = a * a; /*DEFECT: signed integer overflow (multiply) */
  std::printf("%d\\n", (int)b);
  return 0;
}""", "undefined_behavior", "main", "high", "catch", ["ubsan"],
    "有符号乘法溢出，UBSan 捕获。")

add(
"""#include <cstdio>
int main(){
  volatile int x = 1;
  volatile int y = x << 31; /*DEFECT: left shift into sign bit (UB) */
  std::printf("%d\\n", (int)y);
  return 0;
}""", "undefined_behavior", "main", "medium", "catch", ["ubsan"],
    "左移进入符号位（UB），UBSan 捕获 shift。")

add(
"""#include <cstdio>
int main(){
  volatile int x = 1;
  volatile int y = x << 40; /*DEFECT: shift count >= width (UB) */
  std::printf("%d\\n", (int)y);
  return 0;
}""", "undefined_behavior", "main", "medium", "catch", ["ubsan"],
    "移位量 >= 类型宽度（UB），UBSan 捕获。")

add(
"""#include <cstdio>
int main(){
  volatile int b = 0;
  int c = 5 / b; /*DEFECT: division by zero (UB) */
  std::printf("%d\\n", c);
  return 0;
}""", "undefined_behavior", "main", "high", "catch", ["ubsan"],
    "除以零（UB），UBSan 报 division by zero。volatile 防编译期折叠。")

add(
"""#include <climits>
#include <cstdio>
int main(){
  volatile int m = INT_MIN;
  volatile int r = m / -1; /*DEFECT: INT_MIN / -1 overflow (UB) */
  std::printf("%d\\n", (int)r);
  return 0;
}""", "undefined_behavior", "main", "high", "catch", ["ubsan"],
    "INT_MIN 除以 -1 溢出（UB），UBSan 捕获。")

add(
"""#include <cstdio>
int main(){
  volatile int x = -1;
  volatile int y = x << 2; /*DEFECT: left shift of negative value (UB) */
  std::printf("%d\\n", (int)y);
  return 0;
}""", "undefined_behavior", "main", "medium", "catch", ["ubsan"],
    "对负值左移（UB），UBSan 捕获。")

add(
"""#include <cstdio>
int main(){
  alignas(1) char buf[8] = {0};
  int* p = (int*)(buf + 1); /*DEFECT: misaligned 4-byte access (UB) */
  *p = 5;
  std::printf("%d\\n", *p);
  return 0;
}""", "undefined_behavior", "main", "medium", "catch", ["ubsan"],
    "未对齐的 4 字节访问（UB），UBSan alignment 检查捕获。")

add(
"""#include <cstdio>
int main(){
  char* s = (char*)"hello";
  s[0] = 'H'; /*DEFECT: modify string literal (UB) -> RO write */
  std::printf("%s\\n", s);
  return 0;
}""", "undefined_behavior", "main", "high", "catch", ["asan"],
    "修改字符串字面量（UB），写入只读段，ASan 捕获。")

add(
"""#include <cstdio>
int main(){
  volatile int m = -2147483648;
  volatile int r = -m; /*DEFECT: unary minus overflow on INT_MIN (UB) */
  std::printf("%d\\n", (int)r);
  return 0;
}""", "undefined_behavior", "main", "high", "catch", ["ubsan"],
    "对 INT_MIN 取负溢出（UB），UBSan 捕获。")

add(
"""#include <cstdio>
int main(){
  volatile int a = 2000000000;
  a *= 2; /*DEFECT: signed overflow via *= */
  std::printf("%d\\n", (int)a);
  return 0;
}""", "undefined_behavior", "main", "high", "catch", ["ubsan"],
    "复合赋值乘法溢出（UB），UBSan 捕获。")

add(
"""#include <cstdio>
int main(){
  volatile int x = 1;
  volatile int c = -2;
  volatile int y = x << c; /*DEFECT: negative shift count (UB) */
  std::printf("%d\\n", (int)y);
  return 0;
}""", "undefined_behavior", "main", "medium", "catch", ["ubsan"],
    "负移位量（UB），UBSan 捕获。")

add(
"""#include <cstdio>
int main(){
  char buf[8] = {0};
  long long* p = (long long*)(buf + 3); /*DEFECT: misaligned 8-byte access (UB) */
  *p = 1;
  std::printf("%lld\\n", *p);
  return 0;
}""", "undefined_behavior", "main", "medium", "catch", ["ubsan"],
    "未对齐的 8 字节访问（UB），UBSan alignment 捕获。")

add(
"""#include <cstdio>
int main(){
  char* s = "abc";
  s[1] = 'x'; /*DEFECT: modify string literal (UB) */
  std::printf("%s\\n", s);
  return 0;
}""", "undefined_behavior", "main", "high", "catch", ["asan"],
    "修改字符串字面量（UB），ASan 捕获 RO 写。")

add(
"""#include <cstdio>
int main(){
  double d = 2.0;
  int* ip = (int*)&d; /*DEFECT: strict-aliasing violation (UB); ubsan cannot catch at -O0 */
  *ip = 12345;
  std::printf("%f\\n", d);
  return 0;
}""", "undefined_behavior", "main", "low", "miss", ["ubsan"],
    "严格别名违规（UB）：以 int* 写 double 存储。UBSan 在 -O0/-O2 均无运行时陷阱，是检测器盲区（边界案例）。")

add(
"""#include <cstdio>
int main(){
  int i = 0x3f800000;
  float f = *(float*)&i; /*DEFECT: strict-aliasing: read int storage as float (UB) */
  std::printf("%f\\n", f);
  return 0;
}""", "undefined_behavior", "main", "low", "miss", ["ubsan"],
    "严格别名违规（UB）：把 int 存储当 float 读。无运行时陷阱，UBSan 抓不到（边界案例）。")

add(
"""#include <cstdio>
int main(){
  int i = 0;
  float f = reinterpret_cast<float&>(i); /*DEFECT: type pun via reinterpret (UB), no runtime trap */
  std::printf("%f\\n", f);
  return 0;
}""", "undefined_behavior", "main", "low", "miss", ["ubsan"],
    "reinterpret_cast 类型双关（UB），对齐满足所以 UBSan 无运行时报告（边界案例）。")

add(
"""#include <cstdio>
int main(){
  volatile int a = -2147483640;
  volatile int b = a - 100; /*DEFECT: signed overflow (subtract) */
  std::printf("%d\\n", (int)b);
  return 0;
}""", "undefined_behavior", "main", "high", "catch", ["ubsan"],
    "有符号减法溢出（UB），UBSan 捕获。")

add(
"""#include <cstdio>
int main(){
  volatile int a = -100000;
  volatile int b = a * 100000; /*DEFECT: signed overflow (neg multiply) */
  std::printf("%d\\n", (int)b);
  return 0;
}""", "undefined_behavior", "main", "high", "catch", ["ubsan"],
    "负数乘法溢出（UB），UBSan 捕获。")

add(
"""#include <cstdio>
int main(){
  volatile int b = 0;
  int c = 5 % b; /*DEFECT: modulo by zero (UB) */
  std::printf("%d\\n", c);
  return 0;
}""", "undefined_behavior", "main", "high", "catch", ["ubsan"],
    "取模除以零（UB），UBSan 捕获。")

# ===================== uninitialized_read (081-100) -> compiler-warn miss ====
add(
"""#include <cstdio>
int main(){
  int x;
  std::printf("%d\\n", x); /*DEFECT: uninitialized read */
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "读取未初始化局部变量。本机工具链：compiler-warn(-fsyntax-only)与 asan/ubsan(-O0) 均不报（需 MSan，未部署），属检测器盲区。")

add(
"""#include <cstdio>
int main(){
  int a[3];
  std::printf("%d\\n", a[0]); /*DEFECT: uninitialized array read */
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "读取未初始化数组元素，同样无本地检测器可抓。")

add(
"""#include <cstdio>
int main(){
  int* p = new int;
  std::printf("%d\\n", *p); /*DEFECT: uninitialized heap read */
  delete p;
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "读取未初始化堆对象，本地检测器盲区。")

add(
"""#include <cstdio>
struct S { int x; int y; };
int main(){
  S s;
  std::printf("%d\\n", s.x); /*DEFECT: uninitialized struct member read */
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "读取未初始化结构体成员，盲区。")

add(
"""#include <cstdio>
int main(){
  int x;
  if (x > 0) std::printf("pos"); else std::printf("neg"); /*DEFECT: branch on uninitialized */
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "基于未初始化变量分支，盲区。")

add(
"""#include <cstdio>
int main(){
  int a, b;
  int sum = a + b; /*DEFECT: uninitialized arithmetic */
  std::printf("%d\\n", sum);
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "未初始化变量参与算术，盲区。")

add(
"""#include <cstdio>
int main(){
  int x;
  for (int i = 0; i < x; i++){} /*DEFECT: loop bound from uninitialized */
  std::printf("done\\n");
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "用未初始化变量作循环边界，盲区。")

add(
"""#include <cstdio>
int main(){
  double d;
  std::printf("%f\\n", d); /*DEFECT: uninitialized double read */
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "读取未初始化 double，盲区。")

add(
"""#include <cstdio>
int main(){
  int x;
  int* p = &x;
  std::printf("%d\\n", *p); /*DEFECT: uninitialized read via pointer */
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "通过指针读未初始化变量，盲区。")

add(
"""#include <cstdio>
int main(){
  int x;
  int& r = x;
  std::printf("%d\\n", r); /*DEFECT: uninitialized read via reference */
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "通过引用读未初始化变量，盲区。")

add(
"""#include <cstdio>
int main(){
  int arr[5];
  int* p = arr;
  std::printf("%d\\n", p[3]); /*DEFECT: uninitialized read via pointer */
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "指针读未初始化数组元素，盲区。")

add(
"""#include <cstdio>
int main(){
  char buf[16];
  std::printf("%c\\n", buf[0]); /*DEFECT: uninitialized char read */
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "读取未初始化字符，盲区（注意避免 %s 以防越界）。")

add(
"""#include <cstdio>
int main(){
  int x;
  int y = x + 1; /*DEFECT: uninitialized increment */
  std::printf("%d\\n", y);
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "未初始化变量自增后使用，盲区。")

add(
"""#include <cstdio>
int main(){
  bool flag;
  if (flag) std::printf("y"); else std::printf("n"); /*DEFECT: uninitialized bool */
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "使用未初始化 bool，盲区。")

add(
"""#include <cstdio>
int main(){
  int x;
  switch (x) { default: std::printf("d"); } /*DEFECT: switch on uninitialized */
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "对未初始化变量做 switch，盲区。")

add(
"""#include <cstdio>
int main(){
  int a[3] = {1, 2};
  int y = a[2]; /*DEFECT: partially-initialized array, a[2] uninitialized */
  std::printf("%d\\n", y);
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "部分初始化数组的未初始化元素被读，盲区。")

add(
"""#include <cstdio>
int main(){
  int* p;
  std::printf("%p\\n", (void*)p); /*DEFECT: uninitialized pointer (garbage address) */
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "打印未初始化指针（仅打印地址不解引用，安全），盲区。")

add(
"""#include <cstring>
#include <cstdio>
int main(){
  int x;
  int y;
  std::memcpy(&y, &x, sizeof(int)); /*DEFECT: copy uninitialized value */
  std::printf("%d\\n", y);
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "memcpy 复制未初始化值，盲区。")

add(
"""#include <cstdio>
class C { public: int v; };
int main(){
  C c;
  std::printf("%d\\n", c.v); /*DEFECT: uninitialized class member read */
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "读取未初始化类成员，盲区。")

add(
"""#include <cstdio>
int main(){
  long long L;
  std::printf("%lld\\n", L); /*DEFECT: uninitialized long long read */
  return 0;
}""", "uninitialized_read", "main", "low", "miss", ["compiler-warn"],
    "读取未初始化 long long，盲区。")

# ============================ write files ============================
def defect_line(code: str) -> int:
    for i, ln in enumerate(code.splitlines(), 1):
        if "/*DEFECT" in ln:
            return i
    raise RuntimeError("no DEFECT marker")

assert len(S) == 100, f"expected 100, got {len(S)}"

summary = {t: 0 for t in TYPES}
for idx, s in enumerate(S, 1):
    sid = f"sample_{idx:03d}"
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

print("generated", len(S), "samples")
print("by type:", summary)
print("expected verdict counts:",
      {v: sum(1 for x in S if x["expected_verdict"] == v) for v in ("catch", "miss")})
print("planted=true:", sum(1 for x in S if x["planted"]))
