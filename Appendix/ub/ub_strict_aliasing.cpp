// UB-05 strict-aliasing violation：经不兼容类型的指针写同一内存，破坏别名规则
// 注意：UBSan 不会捕获此类 UB（无运行时检查器覆盖别名规则）。
//       证据来自 -O0 与 -O2 -fstrict-aliasing 的**输出差异** + -Wstrict-aliasing 警告。
// 编译对比:
//   g++ -std=c++23 -O0                  -o sa0 ub_strict_aliasing.cpp
//   g++ -std=c++23 -O2 -fstrict-aliasing -Wall -Wstrict-aliasing=2 -o sa2 ub_strict_aliasing.cpp
//   ./sa0   ;   ./sa2
#include <cstdio>

// pi 与 pf 在源码层指向同一对象，但 int* 与 float* 不是「相容类型」
void f(int* pi, float* pf) {
    *pi = 0;          // 经 int* 写
    *pf = 1.0f;       // ❌ UB：经 float* 写同一内存（编译器可假定不别名）
    *pi = *pi + 1;    // -O2 可能直接使用寄存器中的旧值 0，忽略上方 float 写
}

int main() {
    int x = 0;
    f(&x, reinterpret_cast<float*>(&x));
    std::printf("x = %d\n", x);   // -O0 与 -O2 可能输出不同
    return 0;
}
