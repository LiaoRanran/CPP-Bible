// 文件：Examples/_ch128_scope_exit.cpp
// 说明：自包含 ScopeExit（RAII 守卫），演示 Boost.ScopeExit 解决的核心需求：
//       在作用域退出时无条件执行清理（类似 Go defer）。无虚函数、无 Boost。
#include <cstdio>

struct scope_exit {
    using Fn = void(*)(void*);
    Fn  fn;
    void* ctx;
    ~scope_exit() { if (fn) fn(ctx); }
};

static void close_file(void* p) {
    FILE* f = (FILE*)p;
    if (f) std::fclose(f);
}

int main() {
    FILE* f = std::fopen("/tmp/x.log", "w");
    scope_exit guard{ close_file, (void*)f };   // 离开作用域必关闭
    if (f) std::fputs("hi", f);
    return f ? 0 : 1;
}
