// 文件：Examples/_ch142_aos.cpp
// 行号：5
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 -S -masm=intel Examples/_ch142_aos.cpp -o Examples/_ch142_aos.asm
// AoS（Array of Structures）：所有组件打包进一个结构体，实体数组按"行"存储。
#include <vector>

struct Particle {          // 一个实体拥有全部组件字段
    float x, y, z;         // Position
    float vx, vy, vz;      // Velocity
};

// 只更新 x 分量，但仍要按 stride=24 字节跨过整个结构体
void integrate_aos(Particle* p, int n, float dt) {
    for (int i = 0; i < n; ++i) {
        p[i].x += p[i].vx * dt;
    }
}

int main() {
    std::vector<Particle> ps(1024);
    integrate_aos(ps.data(), (int)ps.size(), 0.016f);
    return (int)ps[0].x;
}
