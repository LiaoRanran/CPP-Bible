// 文件：Examples/_ch161_full.cpp
// 取证：g++ -std=c++20 -O2 -pthread 真实编译运行（本机）；自包含工业级 logger 雏形
#include <chrono>
#include <condition_variable>
#include <cstdio>
#include <ctime>
#include <atomic>
#include <format>
#include <fstream>
#include <mutex>
#include <queue>
#include <string>
#include <string_view>
#include <thread>
#include <vector>

enum class Level : int { trace = 0, debug = 1, info = 2, warn = 3, error = 4, off = 5 };

constexpr const char* level_str(Level l) {
    switch (l) {
        case Level::trace: return "trace";
        case Level::debug: return "debug";
        case Level::info:  return "info";
        case Level::warn:  return "warn";
        case Level::error: return "error";
        default: return "off";
    }
}

// 时间戳
std::string ts() {
    auto t = std::chrono::system_clock::now();
    std::time_t tt = std::chrono::system_clock::to_time_t(t);
    char b[32]; std::strftime(b, sizeof b, "%Y-%m-%d %H:%M:%S", std::localtime(&tt));
    return b;
}

class Logger {
    Level thr_ = Level::info;
    std::ofstream file_;
    mutable std::mutex mtx_;
    // 异步队列
    std::queue<std::string> q_;
    std::condition_variable cv_;
    std::atomic<bool> stop_{false};
    std::thread worker_;

    void drain() {
        std::unique_lock<std::mutex> lk(mtx_);
        cv_.wait(lk, [this] { return stop_.load() || !q_.empty(); });
        while (!q_.empty()) {
            auto s = std::move(q_.front()); q_.pop();
            lk.unlock();
            std::printf("%s\n", s.c_str());
            if (file_) file_ << s << "\n";
            lk.lock();
        }
    }
public:
    explicit Logger(const char* file = nullptr) {
        if (file) file_.open(file, std::ios::app);
        worker_ = std::thread([this] {
            while (!(stop_.load() && q_.empty())) drain();
        });
    }
    ~Logger() {
        stop_.store(true); cv_.notify_one();
        if (worker_.joinable()) worker_.join();
    }
    void set_level(Level l) { thr_ = l; }
    template <typename... Args>
    void log(Level lvl, const char* file, int line, std::string_view fmt, Args&&... a) {
        if (static_cast<int>(lvl) < static_cast<int>(thr_)) return;  // 运行时门控
        std::string body = std::vformat(fmt, std::make_format_args(a...));
        std::string s = ts() + " [" + level_str(lvl) + "] " + file + ":" +
                        std::to_string(line) + " " + body;
        {
            std::lock_guard<std::mutex> lk(mtx_);
            q_.push(std::move(s));
        }
        cv_.notify_one();
    }
};

#define LOG(logger, lvl, ...) (logger).log(lvl, __FILE__, __LINE__, __VA_ARGS__)

int main() {
    Logger log("Examples/_ch161_full.log");
    LOG(log, Level::info,  "service {} started on port {}", "api", 8080);
    LOG(log, Level::warn,  "retry {}/{} after timeout", 2, 5);
    LOG(log, Level::error, "unhandled exception: {}", "bad_alloc");
    std::this_thread::sleep_for(std::chrono::milliseconds(60));  // 等后台线程消费
    return 0;
}
