// 文件：Examples/_ch155_aos.cpp
// 行号：4
// AoS vs SoA：结构数组 vs 数组结构，对向量化的影响
struct Vec3 { float x, y, z; };

void aos_scale(Vec3* __restrict p, int n, float s) {
    for (int i = 0; i < n; ++i) {
        p[i].x *= s;
        p[i].y *= s;
        p[i].z *= s;
    }
}

void soa_scale(float* __restrict x, float* __restrict y,
               float* __restrict z, int n, float s) {
    for (int i = 0; i < n; ++i) {
        x[i] *= s;
        y[i] *= s;
        z[i] *= s;
    }
}
