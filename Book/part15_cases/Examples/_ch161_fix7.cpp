// 文件：Examples/_ch161_fix7.cpp
// 主题：⑧ 线程安全锁 —— std::shared_mutex 读写锁（多读少写场景）
#include <cstdio>
#include <mutex>
#include <shared_mutex>
#include <string>
#include <string_view>
#include <thread>
#include <vector>

struct RwLogger {
    mutable std::shared_mutex m;
    std::string last;
    void write(std::string_view msg) {            // 写：独占
        std::unique_lock lk(m);
        last = std::string(msg);
    }
    std::string read() const {                     // 读：共享
        std::shared_lock lk(m);
        return last;
    }
};

int main() {
    RwLogger log;
    std::vector<std::thread> ws, rs;
    for (int i = 0; i < 4; ++i)
        ws.emplace_back([&log, i] { log.write("m" + std::to_string(i)); });
    for (int i = 0; i < 4; ++i)
        rs.emplace_back([&log] { (void)log.read(); });
    for (auto& t : ws) t.join();
    for (auto& t : rs) t.join();
    std::printf("final=%s\n", log.read().c_str());
    return 0;
}
