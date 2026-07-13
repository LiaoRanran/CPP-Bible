// 文件：Examples/_ch159_jthread.cpp
// 行号：1
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 Examples/_ch159_jthread.cpp -o Examples/_ch159_jthread.exe
// 说明：C++20 std::jthread + std::stop_token 协作式取消演示。
#include <chrono>
#include <cstdio>
#include <stop_token>
#include <thread>

void worker(std::stop_token st, int id) {
    while (!st.stop_requested()) {
        std::printf("worker %d tick\n", id);
        std::this_thread::sleep_for(std::chrono::milliseconds(120));
    }
    std::printf("worker %d stopped\n", id);
}

int main() {
    std::jthread a([](std::stop_token st) { worker(st, 1); });
    std::jthread b([](std::stop_token st) { worker(st, 2); });
    std::this_thread::sleep_for(std::chrono::milliseconds(500));
    // 析构自动调用 request_stop() + join()
}
