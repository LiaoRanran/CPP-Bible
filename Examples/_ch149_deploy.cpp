// 见 Examples/_ch149_deploy.cpp
// ⑩ 部署步骤模拟：拉镜像 + 滚动更新
#include <cstdio>
int main() {
    std::printf("deploy: pulling image registry/app:1.4.2\n");
    std::printf("deploy: kubectl rollout status deploy/app\n");
    std::printf("deploy: done\n");
    return 0;
}
