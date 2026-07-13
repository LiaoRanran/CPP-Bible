// ④' 时钟选择：steady_clock 单调不被 NTP 调，适合基准
// 见 Examples/_ch151_clock_choice.cpp
#include <cstdio>
#include <chrono>
#include <type_traits>

int main() {
    // 在本机 libstdc++ 中 high_resolution_clock 即 steady_clock 别名
    constexpr bool hr_is_steady =
        std::chrono::high_resolution_clock::is_steady;  // bool 常量
    std::printf("clock_choice: high_resolution_clock::is_steady=%d\n", (int)hr_is_steady);
    std::printf("  use steady_clock for benchmarks (never system_clock)\n");
    return 0;
}
