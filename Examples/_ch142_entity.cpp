// 文件：Examples/_ch142_entity.cpp
// 行号：3
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 -S -masm=intel Examples/_ch142_entity.cpp -o Examples/_ch142_entity.asm
// Entity 只是一个稳定的整型 ID，本身不携带任何数据或行为。
#include <cstdint>

using Entity = std::uint32_t;          // 32 位索引即"实体"
constexpr Entity NULL_ENTITY = 0u;     // 约定 0 为无效实体

int main() {
    Entity e = 1;                       // 创建实体 = 分配一个空闲 ID
    return (int)e;
}
