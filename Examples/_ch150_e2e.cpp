// ⑨ 端到端测试：模拟 HTTP 请求 -> 处理 -> 响应 全链路
#include <cstdio>
#include <cstring>
#include <cassert>
static int handle(const char* req, char* resp, int cap) {
    if (std::strcmp(req, "PING") == 0) return std::snprintf(resp, cap, "PONG");
    return std::snprintf(resp, cap, "ERR");
}
int main() {
    char resp[64];
    handle("PING", resp, sizeof resp);
    assert(std::strcmp(resp, "PONG") == 0);
    std::printf("e2e: request PING -> response '%s'\n", resp);
    handle("XYZ", resp, sizeof resp);
    assert(std::strcmp(resp, "ERR") == 0);
    return 0;
}
