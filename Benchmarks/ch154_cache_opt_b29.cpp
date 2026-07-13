// 补-H 矩阵行优先 vs 列优先：缓存局部性对性能的极端影响
#include <iostream>
#include <vector>
#include <chrono>
int main() {
    const int N = 4096;
    std::vector<int> m(N * N, 1);
    volatile long long s = 0;
    { auto t0 = std::chrono::steady_clock::now();
      for (int i = 0; i < N; ++i)           // 行优先（连续访问）
          for (int j = 0; j < N; ++j) s += m[i * N + j];
      auto t1 = std::chrono::steady_clock::now();
      std::cout << "row-major=" << std::chrono::duration<double, std::milli>(t1 - t0).count() << "ms\n"; }
    { auto t0 = std::chrono::steady_clock::now();
      for (int j = 0; j < N; ++j)           // 列优先（跨越 4KB 步长）
          for (int i = 0; i < N; ++i) s += m[i * N + j];
      auto t1 = std::chrono::steady_clock::now();
      std::cout << "col-major=" << std::chrono::duration<double, std::milli>(t1 - t0).count() << "ms\n"; }
    return 0;
}