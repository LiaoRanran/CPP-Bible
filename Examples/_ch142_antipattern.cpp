// 文件：Examples/_ch142_antipattern.cpp
// 行号：5
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 -S -masm=intel Examples/_ch142_antipattern.cpp -o Examples/_ch142_antipattern.asm
// 反模式：GameObject 继承 + 虚函数 update()，百万对象 = 虚表散乱 + 缓存不友好（见 ⑯）。
#include <vector>

struct GameObject {
    virtual ~GameObject() = default;
    virtual void update() = 0;   // ❌ 每对象一个虚表指针，行为塞进数据里
    float x, y;
};

struct Monster : GameObject {
    void update() override { x += 1.0f; }  // ❌ 逻辑与数据耦合
};

// ✅ 对比：ECS 把 update 逻辑提到 system 外，数据留在紧凑数组
struct MonsterData { float x, y; };
void monster_system(std::vector<MonsterData>& m) {
    for (auto& d : m) d.x += 1.0f;          // ✅ 连续、可向量化
}

int main() {
    std::vector<Monster> ms(64);
    monster_system(reinterpret_cast<std::vector<MonsterData>&>(ms));
    return (int)ms[0].x;
}
