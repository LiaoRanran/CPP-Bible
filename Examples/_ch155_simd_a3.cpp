// ⑫ AoS：x/y/z 交错，向量化需跨步/广播，浪费 lane
struct Vec3 { float x, y, z; };
void aos_scale(Vec3* __restrict p, int n, float s) {
    for (int i = 0; i < n; ++i) {
        p[i].x *= s; p[i].y *= s; p[i].z *= s;
    }
}
// ⑫ SoA：每字段连续，向量化最干净
void soa_scale(float* __restrict x, float* __restrict y,
               float* __restrict z, int n, float s) {
    for (int i = 0; i < n; ++i) { x[i] *= s; y[i] *= s; z[i] *= s; }
}