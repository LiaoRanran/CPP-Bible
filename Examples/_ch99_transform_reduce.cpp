// 文件：Examples/_ch99_transform_reduce.cpp
// 行号：9  (tr_square) / 16 (tr_mul) / 23 (tr_fast)  —— 见下方注释
// 编译：
//   g++ -std=c++23 -O2 -S -masm=intel Examples/_ch99_transform_reduce.cpp -o Examples/_ch99_transform_reduce.asm
//   g++ -std=c++23 -O2 -ffast-math -S -masm=intel Examples/_ch99_transform_reduce.cpp -o Examples/_ch99_transform_reduce_fast.asm
#include <numeric>
#include <cstddef>

// 逐元素平方再求和（自定义 op）：默认不向量化（含函数对象 + FP 重排）
double tr_square(const double* p, std::size_t n) {
    return std::transform_reduce(p, p + n, 0.0,
        [](double a, double b) { return a + b; },
        [](double x) { return x * x; });
}

// 两个等长数组的逐元素乘加（点积式）
double tr_mul(const double* a, const double* b, std::size_t n) {
    return std::transform_reduce(a, a + n, b, 0.0,
        [](double x, double y) { return x + y; },
        [](double u, double v) { return u * v; });
}

// 整数版本：整数乘法 + 加法满足结合律，可能被向量化
long long tr_int(const long long* a, const long long* b, std::size_t n) {
    return std::transform_reduce(a, a + n, b, 0LL,
        [](long long x, long long y) { return x + y; },
        [](long long u, long long v) { return u * v; });
}
