// 文件：Examples/_ch142_chunk.cpp
// 行号：3
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 -S -masm=intel Examples/_ch142_chunk.cpp -o Examples/_ch142_chunk.asm
// Chunk（分块）：超大世界无法放进单块连续内存，按固定容量（如 16k 实体/块）切分。
#include <cstddef>

constexpr std::size_t CHUNK_ENTITY_COUNT = 16;          // 每块的实体数
constexpr std::size_t CHUNK_COMPONENT_BYTES = 32;       // 每实体的组件集字节

struct Chunk {
    alignas(64) char data[CHUNK_ENTITY_COUNT * CHUNK_COMPONENT_BYTES];
    std::size_t      used = 0;
};

// 计算第 i 个实体在块内的字节偏移（连续、可预测、缓存友好）
constexpr std::size_t offset_of(std::size_t i) {
    return i * CHUNK_COMPONENT_BYTES;
}

int main() {
    Chunk c;
    return (int)(sizeof(c.data) + offset_of(CHUNK_ENTITY_COUNT - 1));
}
