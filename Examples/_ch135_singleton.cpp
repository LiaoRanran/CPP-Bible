// _ch135_singleton.cpp
// 取证目标（第⑫节）：Meyers singleton（线程安全、零裸指针），对比被滥用的反面教材。
#include <cstdio>

struct Config {
    static Config& instance() {
        static Config inst; // C++11 起静态局部变量初始化线程安全
        return inst;
    }
    int value = 42;
    Config(const Config&) = delete;
    Config& operator=(const Config&) = delete;
private:
    Config() = default;
};

int main() {
    std::printf("%d\n", Config::instance().value);
}
