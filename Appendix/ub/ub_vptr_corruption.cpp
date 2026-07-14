// UB-L3 vptr corruption：破坏多态对象的虚表指针
// 编译: g++ -std=c++23 -O2 -o vptr ub_vptr_corruption.cpp
// 运行: ./vptr  →  虚调用经损坏的 vptr 解引用 → 崩溃（本机实测 access violation）
#include <cstdio>

struct Base {
    virtual int f() { return 1; }
    virtual ~Base() = default;
};

int main() {
    Base b;
    // ❌ 把对象首字（vptr）覆写成 nullptr，随后虚调用解引用 0 → UB / 崩溃
    *reinterpret_cast<void**>(&b) = nullptr;   // 破坏 vptr
    std::printf("calling virtual...\n");
    return b.f();                               // ❌ 经损坏 vptr 的虚调用
}
