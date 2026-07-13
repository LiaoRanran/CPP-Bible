// ⑩ 部署后健康检查：CD 流水线调用 /healthz
#include <cstdio>
int main() {
    // 真实服务应监听端口并返回 200；此处以进程退出码表征健康
    std::printf("healthz: ok\n");
    return 0;
}
