// ⑫ 同一份数据两种布局计时对比（自包含，可直接跑）
#include <iostream>
#include <vector>
#include <chrono>

struct Vec3 { float x, y, z; };

int main() {
    constexpr int N = 4'000'000;
    std::vector<Vec3> aos(N, {1.0f, 2.0f, 3.0f});
    std::vector<float> soax(N, 1.0f);

    float sa = 0.0f;
    auto t0 = std::chrono::steady_clock::now();
    for (auto& e : aos) sa += e.x;
    auto t1 = std::chrono::steady_clock::now();

    float ss = 0.0f;
    for (float v : soax) ss += v;
    auto t2 = std::chrono::steady_clock::now();

    std::cout << "AoS  =" << std::chrono::duration<double, std::milli>(t1 - t0).count() << "ms\n";
    std::cout << "SoA  =" << std::chrono::duration<double, std::milli>(t2 - t1).count() << "ms\n";
    return 0;
}