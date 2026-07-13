// 文件：Examples/_ch161_case.cpp
// 取证：g++ -std=c++20 -O2 真实编译运行（本机）；⑲ 真实案例：HTTP 服务访问日志
#include <chrono>
#include <cstdio>
#include <ctime>
#include <string>
#include <string_view>
#include <vector>

enum class Lv { info = 2, warn = 3, error = 4 };
constexpr Lv THR = Lv::info;

std::string now() {
    auto t = std::chrono::system_clock::now();
    std::time_t tt = std::chrono::system_clock::to_time_t(t);
    char b[32]; std::strftime(b, sizeof b, "%H:%M:%S", std::localtime(&tt));
    return b;
}

void log(Lv l, std::string_view msg) {
    if (static_cast<int>(l) < static_cast<int>(THR)) return;
    const char* tag = l == Lv::info ? "info" : l == Lv::warn ? "warn" : "error";
    std::printf("%s [%s] %s\n", now().c_str(), tag, std::string(msg).c_str());
}

struct Req { std::string method, path; int status; int ms; };

int main() {
    std::vector<Req> requests = {
        {"GET", "/api/users", 200, 12},
        {"POST", "/api/login", 200, 33},
        {"GET", "/api/admin", 403, 5},
        {"GET", "/api/export", 500, 1200},
    };
    log(Lv::info, "server listening on :8080");
    for (auto& r : requests) {
        Lv l = r.status >= 500 ? Lv::error : r.status >= 400 ? Lv::warn : Lv::info;
        std::string msg = r.method + " " + r.path + " -> " +
                          std::to_string(r.status) + " in " + std::to_string(r.ms) + "ms";
        log(l, msg);
    }
    log(Lv::info, "server shutdown");
    return 0;
}
