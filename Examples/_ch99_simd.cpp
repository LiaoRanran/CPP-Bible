// 文件：Examples/_ch99_simd.cpp
// 行号：11 (manual_simd_friendly) / 19 (compare_tr)
// 编译-取证：g++ -std=c++23 -O3 -mavx2 -ffast-math -S -masm=intel _ch99_simd.cpp -o _ch99_simd.asm
//   该手写循环在本机 -O3 -mavx2 下被向量化为 vmulpd/vaddpd（见第⑬节汇编对比）。
//   注：本机 GCC13 MinGW 未捆绑 <experimental/simd>（TS），故用"规整循环 + 自动向量化"示范衔接。
#include <numeric>
#include <vector>
#include <execution>
#include <iostream>

// 手写循环：规整、迭代间无数据依赖，编译器可在 -O3 -mavx2 下自动向量化为 vmulpd/vaddpd
double manual_simd_friendly(const std::vector<double>& a) {
    double s = 0.0;
    for (double x : a) s += x * x;
    return s;
}

// 等价的标准算法版本（第⑥节汇编显示 transform_reduce 同样可被向量化）
double compare_tr(const std::vector<double>& a) {
    return std::transform_reduce(std::execution::seq, a.begin(), a.end(), 0.0,
        std::plus<>(), [](double x){ return x * x; });
}

int main() {
    std::vector<double> a(1024, 2.0);
    std::cout << manual_simd_friendly(a) << " " << compare_tr(a) << "\n";
}
