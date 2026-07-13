// _ch125_sso.cpp —— 真实取证：libstdc++ 的短字符串优化（SSO）容量
// 编译（本机 libstdc++ / MinGW GCC 13.1.0）：
//   g++ -std=c++23 -O2 -S -masm=intel _ch125_sso.cpp -o _ch125_sso.asm
//   g++ -std=c++23 -O2 _ch125_sso.cpp -o _ch125_sso.exe && _ch125_sso.exe
#include <string>
#include <cstdio>

// 观察短/长字符串在 libstdc++ 下分别如何分配
int main() {
    std::string a = "hello";                       // 短字符串：留在栈内联缓冲区
    std::string b = "this string is definitely longer than the sso buffer";
    std::printf("a.cap=%zu b.cap=%zu size=%zu\n",
                a.capacity(), b.capacity(), sizeof(std::string));
    // 强制一次可能触发扩容的写入，便于在汇编中观察 capacity 检查
    a.reserve(64);
    std::printf("a.cap_after_reserve=%zu\n", a.capacity());
    return 0;
}
