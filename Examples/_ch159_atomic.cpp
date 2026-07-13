// 文件：Examples/_ch159_atomic.cpp
// 行号：1
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 -S -masm=intel Examples/_ch159_atomic.cpp -o Examples/_ch159_atomic.asm
// 说明：用于观察 std::atomic 在 -O2 下被编译为 lock xadd 指令。
#include <atomic>

std::atomic<int> g{0};

int bump(int n) {
    int s = 0;
    for (int i = 0; i < n; ++i)
        s += g.fetch_add(1, std::memory_order_relaxed);
    return s;
}

int read_stop() {
    return g.load(std::memory_order_acquire);
}
