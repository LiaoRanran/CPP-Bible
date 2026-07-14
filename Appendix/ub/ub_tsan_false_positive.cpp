// UB-C4 TSan 误报（benign race）识别与抑制
// 某些「良性竞争」——如初始化完成标志、调试计数器——TSan 会报 race，但工程上可接受。
// 用注解 [[gnu::no_sanitize("thread")]] 或 TSan suppression 文件抑制，而非改逻辑。
// 编译: g++ -std=c++23 -O1 -g -fsanitize=thread -pthread -o fp ub_tsan_false_positive.cpp
//
// benign race 示例：once 标志用 relaxed atomic 保护初始化（实际安全，TSan 仍可能标 race）
#include <atomic>
#include <cstdio>
#include <thread>

std::atomic<bool> initialized{false};
int config = 0;

void init_once() {
    if (!initialized.load(std::memory_order_relaxed)) {
        config = 42;                                       // 写受 initialized 保护（单写者）
        initialized.store(true, std::memory_order_relaxed);
    }
}

int main() {
    std::thread t1(init_once), t2(init_once);
    t1.join(); t2.join();
    std::printf("config = %d\n", config);
    return 0;
}
