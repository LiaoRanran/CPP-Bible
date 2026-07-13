// 见 Examples/_ch149_health_check.cpp
// ⑩ CD 健康检查：部署后探针，决定流量是否切入
#include <cstdio>
bool health_ok() { return true; }
int main() {
    if (health_ok()) std::printf("GET /healthz -> 200 OK\n");
    else             std::printf("GET /healthz -> 503\n");
    return 0;
}
