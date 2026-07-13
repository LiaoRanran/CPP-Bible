// 文件：Examples/_ch142_soa.cpp
// 行号：5
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 -S -masm=intel Examples/_ch142_soa.cpp -o Examples/_ch142_soa.asm
// SoA（Structure of Arrays）：每个组件是独立数组，实体按"列"存储。
#include <vector>

struct ParticlesSoA {
    std::vector<float> x, y, z;
    std::vector<float> vx, vy, vz;
};

// 只更新 x 分量：只遍历 x 与 vx 两个紧凑数组，stride=4 字节。
void integrate_soa(ParticlesSoA& ps, float dt) {
    for (std::size_t i = 0; i < ps.x.size(); ++i) {
        ps.x[i] += ps.vx[i] * dt;
    }
}

int main() {
    ParticlesSoA ps;
    ps.x.assign(1024, 0.0f);
    ps.vx.assign(1024, 1.0f);
    integrate_soa(ps, 0.016f);
    return (int)ps.x[0];
}
