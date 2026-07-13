// 文件：Examples/_ch142_system.cpp
// 行号：5
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 -S -masm=intel Examples/_ch142_system.cpp -o Examples/_ch142_system.asm
// System 是"逻辑"：批量遍历拥有特定组件集合的实体，对组件做纯函数式变换。
#include <vector>

struct Position { float x, y; };
struct Velocity { float vx, vy; };

// 移动系统：遍历所有 [Position, Velocity] 实体，按速度积分位置。
void movement_system(std::vector<Position>& pos,
                     const std::vector<Velocity>& vel, float dt) {
    const std::size_t n = pos.size() < vel.size() ? pos.size() : vel.size();
    for (std::size_t i = 0; i < n; ++i) {
        pos[i].x += vel[i].vx * dt;
        pos[i].y += vel[i].vy * dt;
    }
}

int main() {
    std::vector<Position> pos(512, {0.0f, 0.0f});
    std::vector<Velocity> vel(512, {1.0f, 0.5f});
    movement_system(pos, vel, 0.016f);
    return (int)(pos[0].x * 1000);
}
