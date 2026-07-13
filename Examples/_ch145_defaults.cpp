// _ch145_defaults.cpp —— 默认值与重载顺序（g++ 编译取证，warnings clean）
#include <cstdio>
#include <string>

// 反例：默认参数 + 重载组合易触发歧义
void open(const std::string& path)        { std::printf("open(%s)\n", path.c_str()); }
// void open(const std::string& path, int flags = 0) { } // ❌ 与上一行在 open("x") 处歧义

// 正例：用重载分层，不用默认参数拼装大接口
void open(const std::string& path, int flags) { std::printf("open(%s,%d)\n", path.c_str(), flags); }

int main() {
    open("a.txt");
    open("b.txt", 0644);
    return 0;
}
