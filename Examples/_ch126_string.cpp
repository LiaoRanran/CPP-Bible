// 文件：Examples/_ch126_string.cpp
// 演示 std::string 的小字符串优化（SSO）：短串不分配堆。
// 本例用 MinGW/g++ (libstdc++) 真实编译，用来说明 MS STL 同样实现的 SSO 机制（见 ⑧）。
#include <string>
#include <cstdio>

int main() {
    std::string small = "hello";                       // 短串：存对象内本地缓冲
    std::string big   = "this string is clearly longer than fifteen bytes!!"; // 长串：堆
    std::printf("small=%s big_len=%zu\n", small.c_str(), big.size());
    return (int)(small.size() + big.size());
}
