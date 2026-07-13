// _ch165_raii.cpp : RAII 与智能指针（工程必会）
#include <fstream>
#include <iostream>
#include <memory>

struct FileGuard {
    std::ofstream f;
    FileGuard(const char* name) : f(name) {}   // 构造即获取
    ~FileGuard() { if (f) f.close(); }          // 析构即释放
};

int main() {
    { FileGuard g("tmp_ch165.txt"); g.f << "hello\n"; }  // 离开作用域自动关闭

    auto up = std::make_unique<int>(7);     // unique_ptr：独占
    std::cout << *up << "\n";

    auto sp = std::make_shared<int>(9);     // shared_ptr：引用计数
    auto sp2 = sp;
    std::cout << "use_count = " << sp.use_count() << "\n";  // 2
    return 0;
}
