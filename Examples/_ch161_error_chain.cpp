// 文件：Examples/_ch161_error_chain.cpp
// 取证：g++ -std=c++20 -O2 真实编译运行（本机）
// ⑱ 与错误处理衔接：日志不是错误处理本身，错误码/异常负责控制流，日志负责可观测性
#include <cstdio>
#include <string>

// 简化错误码（对应第146章"错误处理"思想：用返回类型表达失败，而非仅靠日志）
enum class Err { ok = 0, not_found = 1, timeout = 2 };

// 业务函数：返回错误，并由日志记录现场（日志只旁观，不替代返回）
Err fetch(std::string_view key, std::string& out) {
    if (key.empty()) {
        std::printf("[error] fetch: empty key at %s\n", "fetch");
        return Err::not_found;
    }
    out = "value-of-" + std::string(key);
    std::printf("[info] fetch: ok key=%s\n", std::string(key).c_str());
    return Err::ok;
}

int main() {
    std::string v;
    Err e = fetch("", v);                 // 失败 -> 日志已记录现场
    if (e != Err::ok) std::printf("caller handles error code=%d\n", (int)e);
    fetch("user42", v);
    return 0;
}
