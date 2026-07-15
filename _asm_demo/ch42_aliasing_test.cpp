// ch42 strict aliasing 汇编实证
// 编译: g++ -std=c++23 -O2 -c ch42_aliasing_test.cpp && objdump -d ch42_aliasing_test.o
// 对比: g++ -std=c++23 -O2 -fno-strict-aliasing -c ...
#include <cstdint>

// ① 不同类型指针 —— strict aliasing 假定不重叠，*pi 可缓存进寄存器
int no_alias(int* pi, float* pf) {
    *pi = 1;          // 写 int
    *pf = 2.0f;       // 写 float —— -fstrict-aliasing 下假定与 *pi 不重叠
    return *pi;       // 严格别名: 返回常量 1（不重载内存）
}

// ② 同类型指针 —— 可能重叠，必须重载
int same_type(int* pi, int* pj) {
    *pi = 1;
    *pj = 2;          // pj 可能别名 pi
    return *pi;       // 必须从内存重载（可能是 1 或 2）
}

// ③ 通过 char* 打洞 —— char 可别名任意类型，强制重载
int char_pun(int* pi, char* pc) {
    *pi = 1;
    *pc = 0;          // char* 合法别名任意类型
    return *pi;       // 必须重载
}
