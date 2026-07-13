// ⑬ 密钥管理：运行时从环境变量读取，绝不硬编码
#include <cstdio>
#include <cstdlib>

int main() {
    const char* tok = std::getenv("CI_DEPLOY_TOKEN");
    if (!tok) { std::printf("secrets: token NOT found in env (expected in CI)\n"); return 0; }
    std::printf("secrets: token length=%zu (never print the value!)\n", __builtin_strlen(tok));
    return 0;
}
