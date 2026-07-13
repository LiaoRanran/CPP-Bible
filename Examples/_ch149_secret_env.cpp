// 见 Examples/_ch149_secret_env.cpp
// ⑬ 密钥管理：仅从环境变量读取，绝不硬编码进源码
#include <cstdio>
#include <cstdlib>
#include <cstring>
int main() {
    const char* token = std::getenv("CI_TOKEN");
    if (!token) { std::printf("error: CI_TOKEN not set\n"); return 1; }
    std::printf("token length=%zu (not printed)\n", std::strlen(token));
    return 0;
}
