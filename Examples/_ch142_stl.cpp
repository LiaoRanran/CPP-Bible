// 文件：Examples/_ch142_stl.cpp
// 行号：5
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 -S -masm=intel Examples/_ch142_stl.cpp -o Examples/_ch142_stl.asm
// ECS 与标准库：用 unordered_map 做"实体 -> 组件包"的稀疏映射，入门级但不是最优布局。
#include <unordered_map>
#include <vector>
#include <cstdint>

using Entity = std::uint32_t;

struct Transform { float x, y, z; };

// 把每个实体的组件直接挂在一个 map 值里（"map of structs" 反例，见 ⑯）
std::unordered_map<Entity, Transform> g_transforms;

int main() {
    g_transforms[1] = Transform{1.0f, 2.0f, 3.0f};
    g_transforms[2] = Transform{4.0f, 5.0f, 6.0f};
    // 遍历所有 transform 做位移
    float sum = 0.0f;
    for (auto& kv : g_transforms) {
        kv.second.x += 0.1f;
        sum += kv.second.x;
    }
    return (int)sum;
}
