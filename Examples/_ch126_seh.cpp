// 文件：Examples/_ch126_seh.cpp
// 用 C++ 异常演示 Windows 上的结构化异常处理（SEH）机制。
// 在 MinGW-w64 (x86_64, seh) 上，C++ throw/catch 由 libgcc 的 SEH 展开支持，
// 汇编里会出现 .seh_proc / .seh_handler / .seh_endprologue 等指令。
// 这正是 MS STL 在 Windows 上依赖的同一种底层机制（见 ⑥）。
#include <stdexcept>
#include <cstdio>

[[gnu::noinline]]
int may_throw(int x) {
    if (x < 0) throw std::runtime_error("neg");
    return x * 2;
}

int safe_call(int x) {
    try {
        return may_throw(x) + 1;
    } catch (const std::exception& e) {
        std::printf("caught: %s\n", e.what());
        return -1;
    }
}

int main() {
    return safe_call(10) + safe_call(-3);
}
