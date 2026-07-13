// 文件：Examples/_ch161_sink_file.cpp
// 取证：g++ -std=c++20 -O2 真实编译运行（本机）；生成 Examples/_ch161_file.log
#include <cstdio>
#include <fstream>
#include <iostream>
#include <string>

// ③ file sink：把日志写入文件（生产常用，便于事后排查）
struct FileSink {
    std::ofstream ofs;
    explicit FileSink(const char* path) : ofs(path, std::ios::app) {}
    void write(std::string_view level, std::string_view msg) {
        if (ofs) ofs << "[" << level << "] " << msg << "\n";
    }
    ~FileSink() { if (ofs) ofs.flush(); }
};

int main() {
    FileSink sink("Examples/_ch161_file.log");
    sink.write("info", "application started");
    sink.write("error", "connection refused: 127.0.0.1:8080");
    std::cout << "wrote Examples/_ch161_file.log\n";
    return 0;
}
