// ch51 CRTP 汇编实证 —— 编译期多态 vs 虚函数对比
#include <cstdint>

// --- 方案 A: CRTP 静态多态 ---
template <typename Derived>
struct AnimalCRTP {
    void speak() { static_cast<Derived*>(this)->speak_impl(); }
};

struct DogCRTP : AnimalCRTP<DogCRTP> {
    int age;
    void speak_impl() { age += 1; }
};

void crtp_dispatch(DogCRTP& d) {
    d.speak();  // 编译期确定 → 直接 inline
}

// --- 方案 B: 虚函数动态多态 ---
struct AnimalVirt {
    int age;
    virtual void speak() { age += 1; }
    virtual ~AnimalVirt() = default;
};

void virt_dispatch(AnimalVirt* a) {
    a->speak();  // 运行时通过 vtable 查函数指针
}

// --- 方案 C: final 类去虚拟化 ---
struct DogFinal final : AnimalVirt {
    void speak() override { age += 2; }
};

void final_call(DogFinal* d) {
    d->speak();  // 编译器知道 d 一定是 DogFinal → 去虚拟化
}

// --- 观测: sizeof 对比 ---
static_assert(sizeof(DogCRTP) == sizeof(int), "CRTP: 无虚表指针");
// AnimalVirt: 8B vptr + 4B age + 4B padding = 16B (Win64 alignment)
