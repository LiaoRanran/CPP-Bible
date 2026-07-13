// 文件: Examples/_ch137_facade.cpp
// Facade：为复杂子系统提供统一、简单的入口接口
#include <iostream>

struct CPU { void freeze() { std::cout << "CPU freeze\n"; }
            void execute() { std::cout << "CPU execute\n"; } };
struct Memory { void load() { std::cout << "Memory load\n"; } };
struct Disk { void read() { std::cout << "Disk read\n"; } };

struct Computer {                  // 门面
    void start() {
        cpu_.freeze();
        mem_.load();
        disk_.read();
        cpu_.execute();
    }
private:
    CPU cpu_; Memory mem_; Disk disk_;
};

int main() {
    Computer c;
    c.start();         // 客户端只看到一个高層接口
}
