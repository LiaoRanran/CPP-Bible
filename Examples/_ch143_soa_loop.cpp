// ④/⑦ SoA 热循环：每个字段是独立连续数组，单字段访问密度最高
struct SoA { float* x; float* y; float* vx; float* vy; };

float step_soa(SoA p, int n, float dt) {
    float s = 0;
    for (int i = 0; i < n; ++i) {
        p.x[i] += p.vx[i] * dt;
        p.y[i] += p.vy[i] * dt;
        s += p.x[i];
    }
    return s;
}
