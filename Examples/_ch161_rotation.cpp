// 文件：Examples/_ch161_rotation.cpp
// 取证：g++ -std=c++20 -O2 真实编译运行（本机）；按大小轮转日志文件
#include <cstdio>
#include <ctime>
#include <fstream>
#include <iostream>
#include <string>

// ⑦ 日志轮转（rotation）：单文件超过 max_bytes 就重命名备份，开新文件
struct RotatingFile {
    std::string base;
    std::size_t max_bytes;
    std::ofstream ofs;
    std::size_t written = 0;

    RotatingFile(std::string b, std::size_t max)
        : base(std::move(b)), max_bytes(max) {
        ofs.open(base, std::ios::app);
    }
    void rotate() {
        ofs.close();
        std::string bak = base + "." + std::to_string(std::time(nullptr));
        std::rename(base.c_str(), bak.c_str());   // 本机真实 rename
        ofs.open(base, std::ios::trunc);
        std::cout << "rotated -> " << bak << "\n";
    }
    void write(std::string_view msg) {
        if (written + msg.size() > max_bytes) rotate();
        ofs << msg << "\n";
        written += msg.size() + 1;
    }
    ~RotatingFile() { if (ofs) ofs.flush(); }
};

int main() {
    // 故意给很小的阈值，真实触发轮转
    RotatingFile rf("Examples/_ch161_rotate.log", 40);
    for (int i = 0; i < 6; ++i)
        rf.write("line " + std::to_string(i) + " payload-abcde");
    std::cout << "done\n";
    return 0;
}
