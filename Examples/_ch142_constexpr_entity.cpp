// 文件：Examples/_ch142_constexpr_entity.cpp
// 行号：3
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 -S -masm=intel Examples/_ch142_constexpr_entity.cpp -o Examples/_ch142_constexpr_entity.asm
// 编译期实体：把 index/version 打包做成 constexpr，让"实体定义"在编译期完成并参与静态检查。
#include <cstdint>

constexpr std::uint32_t make_entity(std::uint32_t idx, std::uint32_t gen) {
    return (gen << 20) | (idx & 0xFFFFFu);
}
constexpr std::uint32_t idx_of(std::uint32_t e) { return e & 0xFFFFFu; }
constexpr std::uint32_t gen_of(std::uint32_t e) { return e >> 20; }

// 编译期常量实体（static_assert 证明它确实在编译期求值，见 ⑫ 汇编取证）
constexpr std::uint32_t PLAYER  = make_entity(7u, 3u);
constexpr std::uint32_t CAMERA  = make_entity(8u, 1u);
static_assert(idx_of(PLAYER) == 7u);
static_assert(gen_of(PLAYER) == 3u);
static_assert(PLAYER != CAMERA);

int main() {
    return (int)(PLAYER + CAMERA);
}
