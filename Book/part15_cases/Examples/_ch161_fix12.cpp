// 文件：Examples/_ch161_fix12.cpp
// 主题：⑯ 性能测量 —— RAII 计时器，析构自动打印耗时
#include <chrono>
#include <cstdio>

struct Timer {
    std::chrono::steady_clock::time_point t0;
    const char* name;
    explicit Timer(const char* n) : t0(std::chrono::steady_clock::now()), name(n) {}
    ~Timer() {
        double ms = std::chrono::duration<double, std::milli>(
                        std::chrono::steady_clock::now() - t0).count();
        std::printf("[bench] %s took %.3f ms\n", name, ms);
    }
};

int main() {
    Timer t("loop");
    volatile long long s = 0;
    for (int i = 0; i < 1000000; ++i) s += i;
    (void)s;
    return 0;
}
