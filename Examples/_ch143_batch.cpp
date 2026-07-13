#include <vector>

// ⑦ 批处理：把同类操作聚合成“对数组的一次扫描”，避免逐对象回调
struct Bullet { float x, y, vx, vy; bool dead; };

// 反例：每颗子弹单独调用（隐含函数调用开销、破坏流水线）
void update_one(Bullet& b, float dt) {
    b.x += b.vx * dt; b.y += b.vy * dt;
}

// 正例：批量更新，循环扁平、可被编译器向量化
void update_batch(std::vector<Bullet>& bs, float dt) {
    for (auto& b : bs) {
        b.x += b.vx * dt;
        b.y += b.vy * dt;
    }
}
