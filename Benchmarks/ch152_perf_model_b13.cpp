// C14 面试题2演示：system_clock 可能因 NTP 回拨给出"负耗时"
#include <iostream>
#include <chrono>
int main() {
    using namespace std::chrono;
    auto a = system_clock::now();
    // 假设此刻系统时间被 NTP 往回调 → b-a 可能 < 0（错误基准）
    auto b = system_clock::now();
    std::cout << "system dt(ms)=" << duration_cast<milliseconds>(b - a).count() << "\n";
    // steady 永不回拨，基准唯一正确选择
    auto c = steady_clock::now();
    auto d = steady_clock::now();
    std::cout << "steady dt(ns)=" << duration_cast<nanoseconds>(d - c).count() << "\n";
    return 0;
}