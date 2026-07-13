// 文件：Examples/_ch99_accumulate.cpp
// 行号：8  (reduce_int) / 11 (accum_int) / 16 (reduce_dbl) / 19 (accum_dbl)
// 编译：
//   g++ -std=c++23 -O2 -S -masm=intel Examples/_ch99_accumulate.cpp -o Examples/_ch99_accumulate.asm
//   g++ -std=c++23 -O2 -ffast-math -S -masm=intel Examples/_ch99_accumulate.cpp -o Examples/_ch99_accumulate_fast.asm
#include <numeric>
#include <cstddef>

// 整数求和：可被 GCC 自动向量化（整数加法满足结合律）
long long reduce_int(const long long* p, std::size_t n) {
    return std::reduce(p, p + n, 0LL);
}
long long accum_int(const long long* p, std::size_t n) {
    return std::accumulate(p, p + n, 0LL);
}

// 双精度求和：浮点加法不满足结合律，默认不重排 -> 不向量化
double reduce_dbl(const double* p, std::size_t n) {
    return std::reduce(p, p + n, 0.0);
}
double accum_dbl(const double* p, std::size_t n) {
    return std::accumulate(p, p + n, 0.0);
}
