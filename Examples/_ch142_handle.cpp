// 文件：Examples/_ch142_handle.cpp
// 行号：3
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 -S -masm=intel Examples/_ch142_handle.cpp -o Examples/_ch142_handle.asm
// 句柄（handle）= index + version：即使底层 slot 被复用，旧句柄也会因版本不符而失效。
#include <cstdint>

struct EntityHandle {
    std::uint32_t index;    // 指向存储槽
    std::uint32_t version;  // 槽的"代际"戳，用于检测悬空引用
};

// 用 32 位打包：高 12 位版本 + 低 20 位索引（也可分两个字段，见 mini ECS）
constexpr std::uint32_t make_handle(std::uint32_t idx, std::uint32_t gen) {
    return (gen << 20) | (idx & 0xFFFFFu);
}
constexpr std::uint32_t idx_of(std::uint32_t h)  { return h & 0xFFFFFu; }
constexpr std::uint32_t gen_of(std::uint32_t h)  { return h >> 20; }

int main() {
    EntityHandle h{42u, 7u};
    std::uint32_t packed = make_handle(42u, 7u);
    return (int)(h.index + idx_of(packed) + gen_of(packed));
}
