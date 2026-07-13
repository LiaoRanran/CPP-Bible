// ④/⑦ AoS 热循环：每次迭代读取整个结构（含不需要的字段）
struct P { float x, y, vx, vy; };

float step_aos(P* p, int n, float dt) {
    float s = 0;
    for (int i = 0; i < n; ++i) {
        p[i].x += p[i].vx * dt;
        p[i].y += p[i].vy * dt;
        s += p[i].x;
    }
    return s;
}
