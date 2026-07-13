// Examples/_ch141_perf.cpp
// DI 性能取证：接口注入（虚 / 运行时多态） vs 模板注入（静态多态，无虚调用）。
// 编译：g++ -std=c++23 -O2 -S -masm=intel -o _ch141_perf.asm _ch141_perf.cpp
//       g++ -std=c++23 -O0 -S -masm=intel -o _ch141_perf_O0.asm _ch141_perf.cpp
#include <cstdio>

// ---- 接口（运行时多态）：有 vtable、有间接调用 ----
struct IStorage { virtual ~IStorage() = default; virtual int get() const = 0; };
struct MemStorage : IStorage { int get() const override { return 42; } };
int via_virtual(const IStorage& s) { return s.get(); }      // 经 vtable（除非被去虚化）

// ---- 模板（编译期绑定，静态多态，无虚）----
struct FastStorage { int get() const { return 42; } };       // 故意无 virtual
template <class S>
int via_template(const S& s) { return s.get(); }             // 直接调用 / 内联

int main() {
    MemStorage ms;
    FastStorage fs;
    volatile int a = via_virtual(ms);    // 间接调用（vtable）
    volatile int b = via_template(fs);   // 直接内联，无 vtable
    return a + b;
}
