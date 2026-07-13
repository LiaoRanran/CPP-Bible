#include <cstddef>
#include <vector>

// ④ SoA：Structure of Arrays —— 每个字段独立成连续数组
struct Enemies {
    std::vector<float> hp;
    std::vector<float> x, y;
    std::vector<int>   kind;
    std::vector<char>  alive;
};

constexpr std::size_t N = 1024;
Enemies g_e;

float total_hp_soa() {
    float s = 0.0f;
    for (std::size_t i = 0; i < N; ++i)
        s += g_e.hp[i];
    return s;
}
