#include <vector>
#include <cstdio>

// ① 面向数据设计的最小示例：批量推进粒子位置
struct Particle {            // AoS：位置与速度打包在同一结构里
    float x, y, vx, vy;
};

// DOD 关注点：对“所有粒子”做同一件事，循环连续、可预测
void step(std::vector<Particle>& ps, float dt) {
    for (auto& p : ps) {
        p.x += p.vx * dt;
        p.y += p.vy * dt;
    }
}

int main() {
    std::vector<Particle> ps(1'000'000);
    for (std::size_t i = 0; i < ps.size(); ++i) {
        ps[i].vx = 1.0f;
        ps[i].vy = 1.0f;
    }
    step(ps, 0.016f);
    std::printf("px=%f\n", static_cast<double>(ps[0].x));
    return 0;
}
