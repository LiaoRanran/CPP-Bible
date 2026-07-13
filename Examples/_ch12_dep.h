// ⑪ _ch12_dep.h：被两个翻译单元包含的头，用于演示头依赖
#pragma once
namespace ch12 {
    inline int version() { return 3; }
    int add(int a, int b);
}
