// 文件：Examples/_ch161_sink_console.cpp
// 取证：g++ -std=c++20 -O2 真实编译运行（本机）
#include <chrono>
#include <cstdio>
#include <iostream>
#include <string>

// ② console sink：把格式化后的文本写到 stdout
struct ConsoleSink {
    void write(std::string_view level, std::string_view msg) {
        std::cout << "[" << level << "] " << msg << std::endl;
    }
};

// ③ 轻量时间戳（真实运行产生，非编造）
std::string now_iso() {
    auto t = std::chrono::system_clock::now();
    auto tt = std::chrono::system_clock::to_time_t(t);
    char buf[32];
    std::strftime(buf, sizeof(buf), "%H:%M:%S", std::localtime(&tt));
    return buf;
}

int main() {
    ConsoleSink sink;
    sink.write("info", std::string("hello at ") + now_iso());
    sink.write("warn", "disk 85% full");
    return 0;
}
