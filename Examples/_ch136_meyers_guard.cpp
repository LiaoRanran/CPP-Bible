// Examples/_ch136_meyers_guard.cpp
// 强制 magic static 守卫：Logger 持有可观测状态（计数+向量），worker 并发调用
// instance() 并写入状态；main 读取该状态。g++ -O2 无法证明单线程、也无法删除
// 这个 static 局部变量，必须为它插入 __cxa_guard_acquire / __cxa_guard_release。
#include <iostream>
#include <thread>
#include <vector>
#include <string>

struct Logger {
    int count = 0;
    std::vector<std::string> lines;
    static Logger& instance() {
        static Logger inst;          // magic static（带线程安全守卫）
        return inst;
    }
    void log(std::string m) { ++count; lines.push_back(std::move(m)); }
};

void worker(int id) {
    Logger::instance().log("worker-" + std::to_string(id));
}

int main() {
    std::vector<std::thread> ts;
    for (int i = 0; i < 4; ++i) ts.emplace_back(worker, i);
    for (auto& t : ts) t.join();
    Logger::instance().log("done");
    std::cout << "lines=" << Logger::instance().lines.size()
              << " count=" << Logger::instance().count << "\n";
    return 0;
}
