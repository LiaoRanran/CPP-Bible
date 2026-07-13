// ⑰ 源码编码门禁：CI 必须统一 UTF-8 无 BOM
#include <cstdio>
int main() {
    // 中文标识符仅作"源码能被编译器正确解码"的取证
    const char* 消息 = "CI source encoded as UTF-8";
    std::printf("%s\n", 消息);
    return 0;
}
