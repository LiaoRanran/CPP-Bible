// 文件：Examples/_ch161_fix6.cpp
// 主题：⑦ 轮转触发条件 —— 按时间间隔触发（与按大小互补）
#include <chrono>
#include <cstdio>

bool should_rotate(std::chrono::steady_clock::time_point last,
                   std::chrono::seconds interval) {
    return (std::chrono::steady_clock::now() - last) >= interval;
}

int main() {
    using namespace std::chrono;
    auto last = steady_clock::now() - seconds(61);  // 模拟已过去 61s
    bool rot = should_rotate(last, seconds(60));
    std::printf("should_rotate=%d (期望1)\n", rot ? 1 : 0);
    return 0;
}
