// Examples/_ch141_overview.cpp
// 依赖注入（DI）最小完整示例：将 Logger 注入 Service，而非在 Service 内部 new Logger。
#include <iostream>
#include <string>

struct Logger {
    void log(const std::string& msg) { std::cout << "[log] " << msg << "\n"; }
};

struct Service {
    Logger& log;                       // 依赖通过引用持有（无所有权）
    explicit Service(Logger& l) : log(l) {}
    void handle(const std::string& s) { log.log("handle: " + s); }
};

int main() {
    Logger logger;                     // 依赖由“外部”创建并注入
    Service svc(logger);               // ✅ 构造注入
    svc.handle("hello");
}
