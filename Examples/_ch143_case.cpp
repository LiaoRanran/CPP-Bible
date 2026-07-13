#include <vector>
#include <cmath>
#include <cstdio>

// ⑰ 真实案例（物理积分）：对若干刚体做半隐式欧拉积分，纯 SoA + 批处理
struct Bodies {
    std::vector<float> x, y;       // 位置
    std::vector<float> vx, vy;     // 速度
    std::vector<float> mass;       // 质量
};

void integrate(Bodies& b, float dt) {
    const int n = static_cast<int>(b.x.size());
    for (int i = 0; i < n; ++i) {
        // 朝原点受引力（示意）：a = -k * r / |r|
        float r = std::sqrt(b.x[i] * b.x[i] + b.y[i] * b.y[i]) + 1e-3f;
        float ax = -b.x[i] / r, ay = -b.y[i] / r;
        b.vx[i] += ax * dt / b.mass[i];
        b.vy[i] += ay * dt / b.mass[i];
        b.x[i]  += b.vx[i] * dt;
        b.y[i]  += b.vy[i] * dt;
    }
}

int main() {
    Bodies b;
    const int N = 500'000;
    b.x.resize(N); b.y.resize(N); b.vx.resize(N); b.vy.resize(N); b.mass.resize(N);
    for (int i = 0; i < N; ++i) {
        b.x[i] = static_cast<float>(i % 1000); b.y[i] = static_cast<float>(i / 1000);
        b.vx[i] = 0; b.vy[i] = 0; b.mass[i] = 1.0f;
    }
    integrate(b, 0.01f);
    std::printf("after step: x0=%f y0=%f\n", static_cast<double>(b.x[0]), static_cast<double>(b.y[0]));
    return 0;
}
