// 文件：Examples/_ch142_archetype.cpp
// 行号：5
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 -S -masm=intel Examples/_ch142_archetype.cpp -o Examples/_ch142_archetype.asm
// Archetype（原型/归档）：把"拥有完全相同组件集合"的实体放到同一块连续内存里。
#include <cstddef>
#include <vector>

struct Archetype {
    std::size_t        entity_size;  // 单个实体所有组件的总字节数
    std::vector<char>  buffer;       // 行主序：实体0的全部组件、实体1的全部组件……
    std::vector<bool>  alive;        // 每个实体的存活位
};

// 给定组件布局，计算一行（一个实体）的字节宽度
constexpr std::size_t row_size(std::size_t pos, std::size_t vel) {
    return pos + vel;  // Position 字节 + Velocity 字节
}

int main() {
    Archetype a;
    a.entity_size = row_size(sizeof(float) * 3, sizeof(float) * 3);  // 24
    a.buffer.resize(a.entity_size * 64);  // 预存 64 个实体
    a.alive.assign(64, false);
    return (int)a.entity_size;
}
