// Examples/_ch136_meyers_singleton.cpp
// Meyers Singleton：验证 C++11 magic static 的线程安全由编译器插入
// __cxa_guard_acquire / __cxa_guard_release 实现（带锁），而非用户手写锁。
#include <iostream>

struct Logger {
    static Logger& instance() {
        static Logger inst;          // magic static
        return inst;
    }
    void log(const char* m) { std::cout << m << "\n"; }
    int id() const { return 42; }
};

int main() {
    Logger::instance().log("hello");
    return Logger::instance().id();
}
