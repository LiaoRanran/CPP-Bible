// Examples/_ch141_singleton.cpp
// DI 替代单例：单例把“如何获取”和“全局可见性”硬编码；DI 把依赖当作普通参数传入。
#include <iostream>

// ❌ 反例：全局单例，难以测试、隐式耦合
struct EvilConfig { static EvilConfig& instance() { static EvilConfig c; return c; } int port{0}; };

// ✅ 正解：把配置当作依赖注入，单例只在外层装配一次
struct Config { int port{0}; };
class App { const Config& cfg_; public: explicit App(const Config& c):cfg_(c){} void go()const{ std::cout << cfg_.port; } };

int main() {
    Config cfg; cfg.port = 8080;
    App app(cfg);                      // 引用注入：单例在外层持有，内部无全局状态
    app.go();
}
