// ⑬ 制品签名：用 GPG 对发布物签名（命令见正文）
#include <cstdio>
int main() {
    std::printf("gpg --detach-sign artifact.tar.gz  (run in CI runner)\n");
    return 0;
}
