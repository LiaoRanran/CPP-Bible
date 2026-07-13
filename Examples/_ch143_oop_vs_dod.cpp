#include <cstddef>

// ② OOP 多态更新：每个对象通过虚函数各自更新
struct GameObject {
    virtual void update(float dt) = 0;
    virtual ~GameObject() = default;
};

struct Monster : GameObject {
    float x, y, vx, vy;
    void update(float dt) override { x += vx * dt; y += vy * dt; }
};

void update_oop(GameObject** objs, int n, float dt) {
    for (int i = 0; i < n; ++i)
        objs[i]->update(dt);   // 间接调用 + 指针追踪
}

// DOD 等价物：相同布局的数据连续排列，无虚函数
struct GPos { float x, y, vx, vy; };
void update_dod(GPos* o, int n, float dt) {
    for (int i = 0; i < n; ++i) {
        o[i].x += o[i].vx * dt;
        o[i].y += o[i].vy * dt;
    }
}

int main() { (void)sizeof(Monster); return 0; }
