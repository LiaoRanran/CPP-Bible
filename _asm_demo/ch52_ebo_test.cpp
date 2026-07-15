// ch52 空基类优化 (EBO) 汇编实证
// 编译: g++ -std=c++23 -O2 -c ch52_ebo_test.cpp && objdump -d ch52_ebo_test.o
#include <cstddef>

struct Empty {};                              // 空类，sizeof==1（独立时）

struct WithEBO : Empty { int x; };            // 继承空基类 —— EBO: sizeof==4
struct NoEBO  { Empty e; int x; };            // 空类做成员 —— 无 EBO: sizeof==8

// 编译期证明布局差异
static_assert(sizeof(Empty)   == 1, "空类独立占 1 字节");
static_assert(sizeof(WithEBO) == 4, "EBO: 空基类零开销");
static_assert(sizeof(NoEBO)   == 8, "空成员占 1 字节 + 3 填充");

// [[no_unique_address]] (C++20) 让空成员也享受 EBO
struct NoUniqAddr { [[no_unique_address]] Empty e; int x; };
static_assert(sizeof(NoUniqAddr) == 4, "no_unique_address: 空成员零开销");

int read_ebo(WithEBO& w)   { return w.x; }    // x 在偏移 0
int read_noebo(NoEBO& n)   { return n.x; }    // x 在偏移 0（e 被压缩）或 4
int read_nua(NoUniqAddr& n){ return n.x; }    // x 在偏移 0
