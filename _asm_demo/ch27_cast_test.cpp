// ch27 cast 汇编实证 —— GCC15 -O2 真实输出
#include <cstdint>
#include <type_traits>

// 1. static_cast<int>(double) —— 浮点转整型
int static_cast_double_to_int(double d) {
    return static_cast<int>(d);
}

// 2. const_cast<T*>(const T*) —— 移除 const
const int* const_cast_remove(const int* p) {
    return const_cast<int*>(p);
}

// 3. reinterpret_cast<uintptr_t>(void*) —— 指针转整数
uintptr_t reinterpret_cast_ptr_to_int(void* p) {
    return reinterpret_cast<uintptr_t>(p);
}

// 4. static_cast<void*>(int*) —— void* 转换
void* static_cast_to_void(int* p) {
    return static_cast<void*>(p);
}

// 5. dynamic_cast<Derived*>(Base*) —— RTTI 运行时检查
struct Base {
    virtual ~Base() = default;
    virtual void f() {}
};
struct Derived : Base {
    void f() override {}
};
struct Unrelated : Base {
    void f() override {}
};

Derived* dynamic_cast_down(Base* p) {
    return dynamic_cast<Derived*>(p);
}

// 6. 不用 cast 的隐式转换对照
int implicit_int_from_double(double d) {
    return d;  // 隐式截断
}
