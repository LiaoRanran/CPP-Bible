// 文件：Examples/_ch161_fix2.cpp
// 主题：③ 自定义 sink —— 用 std::function 注入任意落地逻辑（此处落内存 vector）
#include <cstdio>
#include <functional>
#include <string>
#include <string_view>
#include <vector>

struct Sink {
    using Fn = std::function<void(std::string_view, std::string_view)>;
    Fn fn;
    explicit Sink(Fn f) : fn(std::move(f)) {}
    void write(std::string_view lvl, std::string_view msg) const { fn(lvl, msg); }
};

int main() {
    std::vector<std::string> store;
    Sink mem_sink([&](std::string_view lvl, std::string_view msg) {
        store.emplace_back(std::string(lvl) + ":" + std::string(msg));
        std::printf("[%s] %s\n", std::string(lvl).c_str(), std::string(msg).c_str());
    });
    mem_sink.write("info", "custom sink works");
    std::printf("store.size=%zu\n", store.size());
    return 0;
}
