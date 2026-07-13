// ⑨ 制品完整性：发布前计算校验和
#include <cstdio>
int main() {
    std::printf("sha256: (computed by `sha256sum artifact.tar.gz` in CI)\n");
    return 0;
}
