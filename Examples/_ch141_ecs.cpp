// Examples/_ch141_ecs.cpp
// DI 与 ECS 衔接：系统（System）通过“组件存储（World）”依赖注入，而非全局单例（预告 ch142）。
#include <iostream>
#include <vector>

struct Position { int x, y; };
struct World {
    std::vector<Position> positions;
    Position& get(int i) { return positions[i]; }
};

class MovementSystem {
    World& world_;                     // 注入 World（组件存储）
public:
    explicit MovementSystem(World& w) : world_(w) {}
    void step(int i, int dx, int dy) { auto& p = world_.get(i); p.x += dx; p.y += dy; }
};

int main() {
    World w; w.positions.push_back({0, 0});
    MovementSystem sys(w);             // ✅ World 作为依赖注入系统
    sys.step(0, 1, 2);
    std::cout << w.positions[0].x << "," << w.positions[0].y << "\n";
}
