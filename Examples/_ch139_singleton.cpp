// _ch139_singleton.cpp
// 取证目的：CRTP 实现「零样板」单例基类。
#include <iostream>

template <typename T>
struct Singleton {
    static T& instance() {
        static T inst;
        return inst;
    }
    Singleton(const Singleton&) = delete;
    Singleton& operator=(const Singleton&) = delete;
protected:
    Singleton() = default;
};

struct Config : Singleton<Config> {
    int timeout = 30;
    friend struct Singleton<Config>;  // 允许基类构造
protected:
    Config() = default;
};

int main() {
    std::cout << "timeout=" << Config::instance().timeout << "\n";
    Config::instance().timeout = 42;
    std::cout << "timeout=" << Config::instance().timeout << "\n";
}
