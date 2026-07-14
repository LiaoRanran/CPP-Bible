// UB-L4 ODR violation（单定义规则违反）：同一 inline 实体在不同 TU 定义不同
// 本文件演示「单 TU 内的等价结构」；真正的 ODR 违反需多 TU，复现命令见 .md。
// 编译（单 TU 版本，仅作结构示意）: g++ -std=c++23 -O2 -o odr ub_odr_violation.cpp
#include <cstdio>

// 头文件 h.hpp 被 a.cpp 与 b.cpp 包含，但两份定义不一致：
//   // h.hpp
//   inline int config() { return 1; }   // a.cpp 看到的定义
//   inline int config() { return 2; }   // b.cpp 看到的定义  ❌ ODR 违反
//
// 这里用匿名命名空间模拟「两份不一致定义」：
namespace {
    inline int config() { return 1; }
}
int main() {
    std::printf("config() = %d\n", config());
    return 0;
}
