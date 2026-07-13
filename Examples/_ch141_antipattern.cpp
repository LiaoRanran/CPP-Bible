// Examples/_ch141_antipattern.cpp
// DI 反模式：在构造函数里 new 具体依赖、或让依赖自己 new 依赖（service locator 伪装成 DI）。
#include <iostream>
#include <memory>

struct ILog { virtual ~ILog() = default; virtual void w() = 0; };
struct Log : ILog { void w() override { std::cout << "w\n"; } };

// ❌ 反模式：构造里 new 具体类，无法替换/测试
class BadService {
    std::unique_ptr<ILog> log_ = std::make_unique<Log>();
public:
    void go() { log_->w(); }
};

// ✅ 正确：依赖由外部注入
class GoodService {
    std::unique_ptr<ILog> log_;
public:
    explicit GoodService(std::unique_ptr<ILog> l) : log_(std::move(l)) {}
    void go() { log_->w(); }
};

int main() {
    GoodService g(std::make_unique<Log>());
    g.go();
}
