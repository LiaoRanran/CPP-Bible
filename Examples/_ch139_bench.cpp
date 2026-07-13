// _ch139_bench.cpp
// 取证目的：真实微基准——虚调用 vs CRTP 静态调用，用 std::chrono 计时。
#include <chrono>
#include <iostream>
#include <vector>

struct ShapeV {
    virtual double area() const = 0;
    virtual ~ShapeV() = default;
};
struct CircleV : ShapeV {
    double r = 2.0;
    double area() const override { return 3.141592653589793 * r * r; }
};

template <typename D>
struct ShapeC {
    double area() const { return static_cast<const D*>(this)->area_impl(); }
};
struct CircleC : ShapeC<CircleC> {
    double r = 2.0;
    double area_impl() const { return 3.141592653589793 * r * r; }
};

template <typename F>
long long bench(const char* name, F f) {
    volatile double sink = 0;
    auto t0 = std::chrono::steady_clock::now();
    for (int i = 0; i < 100'000'000; ++i) sink += f();
    auto t1 = std::chrono::steady_clock::now();
    auto ns = std::chrono::duration_cast<std::chrono::nanoseconds>(t1 - t0).count();
    std::cout << name << ": " << ns << " ns (" << sink << ")\n";
    return ns;
}

int main() {
    CircleV cv;
    CircleC cc;
    bench("virtual  ", [&] { return cv.area(); });
    bench("crtp     ", [&] { return cc.area(); });
}
