// _ch165_log.cpp : 线程安全日志片段（从零项目，见第161章 日志）
#include <chrono>
#include <fstream>
#include <iomanip>
#include <iostream>
#include <mutex>
#include <sstream>
#include <string>

class Logger {
    std::ofstream f_;
    std::mutex mtx_;
    std::string stamp() {
        auto t = std::chrono::system_clock::now();
        auto tt = std::chrono::system_clock::to_time_t(t);
        std::ostringstream os;
        os << std::put_time(std::localtime(&tt), "%Y-%m-%d %H:%M:%S");
        return os.str();
    }
public:
    Logger(const char* path) : f_(path, std::ios::app) {}
    void info(const std::string& msg) {
        std::lock_guard<std::mutex> lk(mtx_);
        std::string line = "[" + stamp() + "] INFO  " + msg + "\n";
        std::cout << line; if (f_) f_ << line;
    }
};

int main() {
    Logger log("app_ch165.log");
    log.info("server start");
    log.info("recv 1024 bytes");
    return 0;
}
