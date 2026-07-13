#include <cstddef>

// ③/④ AoS：Array of Structures —— 同类对象的不同字段交错存放
struct Enemy {
    float hp;
    float x, y;
    int   kind;
    bool  alive;
};

constexpr std::size_t N = 1024;
Enemy g_enemies[N];          // 连续内存，但字段交错

float total_hp_aos() {
    float s = 0.0f;
    for (std::size_t i = 0; i < N; ++i)
        s += g_enemies[i].hp;
    return s;
}
