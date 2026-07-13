// ① 基准测试陷阱：死代码消除（Dead Code Elimination, DCE）
// 见 Examples/_ch151_dce_trap.cpp
// 若计算结果从未被"观察"，优化器会把整个循环删掉，计时毫无意义。
#include <cstdio>
#include <chrono>

int main() {
    const int N = 100'000'000;
    long long sink = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < N; ++i) {
        sink += i;            // 结果从未输出 → 可能被 DCE 删除
    }
    auto t1 = std::chrono::steady_clock::now();
    // 仅在最后伪"使用"，但优化器可证明循环无副作用而整体删除。
    std::printf("dce_trap: elapsed_ms=%.3f (sink hint=%lld)\n",
                std::chrono::duration<double, std::milli>(t1 - t0).count(),
                (long long)(sink & 0));  // &0 强制丢弃，暴露 DCE
    return 0;
}
