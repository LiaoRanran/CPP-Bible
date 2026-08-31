#include <iostream>
#include <vector>
#include <cmath>
#include <cassert>

struct Particle {
    double x, y, z;
    double vx, vy, vz;
    char pad[16]; // 凑满 64B = 恰好一整条缓存行
};

int main() {
    const int N = 1024;
    const double dt = 0.01;

    std::vector<Particle> aos(N);
    std::vector<double> soa_x(N), soa_y(N), soa_z(N);
    std::vector<double> soa_vx(N), soa_vy(N), soa_vz(N);

    for (int i = 0; i < N; ++i) {
        aos[i].x = soa_x[i] = static_cast<double>(i);
        aos[i].vx = soa_vx[i] = static_cast<double>(i) * 0.5;
    }

    // AoS partial update：只动 x / vx 两字段
    for (int i = 0; i < N; ++i) {
        aos[i].vx += 1.0 * dt;
        aos[i].x  += aos[i].vx * dt;
    }
    // SoA partial update：同样只动 x / vx
    for (int i = 0; i < N; ++i) {
        soa_vx[i] += 1.0 * dt;
        soa_x[i]  += soa_vx[i] * dt;
    }

    double sum_aos = 0.0, sum_soa = 0.0;
    for (int i = 0; i < N; ++i) {
        sum_aos += aos[i].x;
        sum_soa += soa_x[i];
    }

    // 功能正确性：两种布局跑同一算法，结果必须一致（浮点容差）
    assert(std::fabs(sum_aos - sum_soa) < 1e-6);
    std::cout << "AoS sum(x) = " << sum_aos << std::endl;
    std::cout << "SoA sum(x) = " << sum_soa << std::endl;
    std::cout << "DOD layout demo ok" << std::endl;
    return 0;
}