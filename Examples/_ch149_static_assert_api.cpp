// ⑥ 编译期契约：静态分析门禁的零成本前置
#include <cstddef>

template <typename T, std::size_t N>
struct FixedBuffer {
    static_assert(N > 0, "buffer size must be positive");
    static_assert(sizeof(T) >= 1, "T must be a complete type");
    T data[N];
};

int main() {
    FixedBuffer<int, 8> b{};
    (void)b;
    return 0;
}
