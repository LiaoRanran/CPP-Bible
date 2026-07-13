#include <vector>

// ⑧ 最小化 ECS：组件即“列”，实体即“行”，系统即批量算法
struct Position { float x, y; };
struct Velocity { float x, y; };

std::vector<Position> g_position;
std::vector<Velocity> g_velocity;

// 移动系统：只对两个相关组件数组做连续遍历（典型 SoA + 批处理）
void system_move(int n, float dt) {
    for (int i = 0; i < n; ++i) {
        g_position[i].x += g_velocity[i].x * dt;
        g_position[i].y += g_velocity[i].y * dt;
    }
}

// 创建实体＝在每列尾部各推入一个分量
void spawn(float x, float y, float vx, float vy) {
    g_position.push_back({x, y});
    g_velocity.push_back({vx, vy});
}
