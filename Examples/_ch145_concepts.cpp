// _ch145_concepts.cpp —— 概念作为接口文档（g++ 编译取证，warnings clean）
#include <concepts>
#include <cstdio>

template <typename T>
concept Arithmetic = std::integral<T> || std::floating_point<T>;

template <Arithmetic T>
T clamp(T x, T lo, T hi) { return x < lo ? lo : (x > hi ? hi : x); }

template <typename T>
concept Drawable = requires(T t) {
    { t.draw() } -> std::same_as<void>;
};

template <Drawable T>
void render(T& t) { t.draw(); }

struct Circle { void draw() { std::printf("circle\n"); } };

int main() {
    std::printf("%ld\n", static_cast<long>(clamp(5L, 0L, 10L)));
    Circle c; render(c);
    return 0;
}
