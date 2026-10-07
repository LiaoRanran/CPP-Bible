// [redacted]
// [redacted]
//       证据来自 -O0 与 -O2 -fstrict-aliasing 的**输出差异** + -Wstrict-aliasing 警告。
// 编译对比:
// [redacted]
// [redacted]
//   ./sa0   ;   ./sa2
#include <cstdio>

// pi 与 pf 在源码层指向同一对象，但 int* 与 float* 不是「相容类型」
void f(int* pi, float* pf) {
    *pi = 0;          // 经 int* 写
    *pf = 1.0f;       // [redacted]
    *pi = *pi + 1;    // -O2 可能直接使用寄存器中的旧值 0，忽略上方 float 写
}

int main() {
    int x = 0;
    f(&x, reinterpret_cast<float*>(&x));
    std::printf("x = %d\n", x);   // -O0 与 -O2 可能输出不同
    return 0;
}
