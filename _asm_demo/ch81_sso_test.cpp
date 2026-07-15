// ASM-81-sso : std::string 小字符串优化 (SSO) 零堆分配实证
// 编译: g++ -std=c++26 -O2 -c ch81_sso_test.cpp -o ch81_sso_test.o
// 链接: g++ -std=c++26 -O2 ch81_sso_test.cpp -o ch81_sso_test.exe  (main 仅用于链接以显示符号名)
// 反汇编: objdump -d -M intel -C ch81_sso_test.exe
#include <string>

// 全局 volatile 副作用, 强制 std::string 构造无法被优化消除
volatile int g_obs = 0;

// 短串: 走 SSO, 构造不调 operator new (零堆分配)
[[gnu::noinline]] void make_short() {
    std::string s("hi");
    g_obs = (int)s.size();
    g_obs = (int)(intptr_t)s.data();   // data() 返回运行时地址, 强制真实构造
}

// 长串: 超过 SSO 容量 -> 构造调 operator new (堆分配)
[[gnu::noinline]] void make_long() {
    std::string s("this string is definitely longer than the SSO buffer and must go to the heap");
    g_obs = (int)s.size();
    g_obs = (int)(intptr_t)s.data();
}

// c_str 位置对比: SSO 返回对象内部缓冲地址; 堆串返回 data 指针字段(堆地址)
// 用 static 延长生命周期避免 return-local-addr 警告
[[gnu::noinline]] const char* short_cstr() {
    static std::string s("abc");
    return s.c_str();
}
[[gnu::noinline]] const char* long_cstr() {
    static std::string s("a string far exceeding the fifteen-byte small string optimization buffer xxxxx");
    return s.c_str();
}

int main() {
    make_short(); make_long();
    (void)short_cstr(); (void)long_cstr();
    return 0;
}
