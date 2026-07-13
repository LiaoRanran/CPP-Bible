// 文件: Examples/_ch137_raii.cpp
// 结构型模式与 RAII 结合：门面同时充当加锁代理，构造加锁、析构解锁
#include <iostream>
#include <mutex>

struct Subsystem {
    void op() { std::cout << "op\n"; }
};

class FacadeGuard {                  // 既是门面又是 RAII 代理
public:
    FacadeGuard(Subsystem& s, std::mutex& m) : s_(s), lk_(m) {}
    void op() { s_.op(); }
private:
    Subsystem& s_;
    std::unique_lock<std::mutex> lk_;
};

int main() {
    Subsystem sys;
    std::mutex m;
    {
        FacadeGuard g{sys, m};      // 构造即加锁，析构即解锁
        g.op();
    }
}
