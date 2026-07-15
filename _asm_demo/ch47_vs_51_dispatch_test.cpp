// ASM-47-vs-51: 虚函数动态分派 vs CRTP 静态分派 —— GCC 15.3.0 真机实证
// 重点：单点调用之外，额外展示「循环内分派」——虚调用无法内联/提升，
//       CRTP 的派生实现被完全内联进循环体，优化器可看穿调用边界。
#include <cstdint>

// ===================== 动态多态：虚函数 =====================
struct ShapeV {
    int k;
    virtual int area() const = 0;
    virtual ~ShapeV() = default;
};
struct CircV : ShapeV {
    int r;
    int area() const override { return r * r; }
};
struct RectV : ShapeV {
    int w, h;
    int area() const override { return w * h; }
};

// 强制不内联：让虚分派以独立符号呈现，objdump 稳定可观测
[[gnu::noinline]] long v_dispatch(const ShapeV& s) {
    return s.area();                         // 运行时经 vtable 间接调用
}
[[gnu::noinline]] long v_loop(const ShapeV* const* arr, int n) {
    long sum = 0;
    for (int i = 0; i < n; ++i) sum += arr[i]->area();  // 每轮迭代查 vtable
    return sum;
}

// ===================== 静态多态：CRTP =====================
template <typename D>
struct ShapeBase {
    const D& self() const { return static_cast<const D&>(*this); }
    int area() const { return self().area_impl(); }
};
struct CircC : ShapeBase<CircC> {
    int r;
    int area_impl() const { return r * r; }
};
struct RectC : ShapeBase<RectC> {
    int w, h;
    int area_impl() const { return w * h; }
};

[[gnu::noinline]] long c_dispatch(const CircC& c) {
    return c.area();                         // 编译期确定，area_impl 内联
}
template <typename D>
[[gnu::noinline]] long c_loop(const D* arr, int n) {
    long sum = 0;
    for (int i = 0; i < n; ++i) sum += arr[i].area();  // 循环体内联展开
    return sum;
}
// 显式实例化以生成符号
template long c_loop<CircC>(const CircC*, int);
template long c_loop<RectC>(const RectC*, int);
