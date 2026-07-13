// 文件：Examples/_ch128_filesystem.cpp
// 说明：自包含的"路径拼接 + 是否存在"逻辑，演示 Boost.Filesystem 在
//       C++17 入标准前解决的痛点（跨平台路径、目录遍历）。
//       此处用 C 标准库模拟等效语义，证明机制本身（不依赖 Boost）。
#include <cstdio>
#include <cstring>

// 简易跨平台路径拼接：把 base 与 name 用 '/' 连接
void join_path(char* out, const char* base, const char* name, int cap) {
    int n = snprintf(out, cap, "%s/%s", base, name);
    (void)n;
}

int main() {
    char path[256];
    join_path(path, "/var/log", "app.log", (int)sizeof(path));
    // 真实场景会调用 stat()/access() 检查存在性；此处仅演示拼接语义
    return (int)strlen(path);   // 返回拼接后长度
}
