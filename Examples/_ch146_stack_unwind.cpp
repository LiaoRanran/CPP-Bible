// _ch146_stack_unwind.cpp
// ④ 栈展开与 RAII：异常抛出时，已构造的局部对象按逆序析构。
#include <cstdio>
#include <stdexcept>

struct Guard {
    const char* name;
    Guard(const char* n) : name(n) { std::printf("[构造] %s\n", name); }
    ~Guard() { std::printf("[析构] %s\n", name); } // 展开时务必执行
};

void deep(int depth) {
    Guard g("帧");
    if (depth <= 0) throw std::runtime_error("boom"); // 触发栈展开
    deep(depth - 1);
}

int main() {
    try {
        Guard a("main-A");
        deep(2);
    } catch (const std::exception& e) {
        std::printf("捕获: %s\n", e.what());
    }
    return 0;
}
