// 文件：Examples/_ch142_component.cpp
// 行号：3
// 编译：C:/Qt/Tools/mingw1310_64/bin/g++.exe -std=c++23 -O2 -S -masm=intel Examples/_ch142_component.cpp -o Examples/_ch142_component.asm
// Component 是"纯数据"：没有虚函数、没有逻辑，只有平凡字段（最好是 trivially copyable）。
#include <cstdint>

struct Position { float x, y, z; };     // 纯数据组件
struct Velocity { float vx, vy, vz; };  // 纯数据组件
struct Tag { std::uint32_t id; };       // 标签组件（零/极少数据）

// ❌ 反例：组件里塞逻辑与状态机，破坏"数据/逻辑分离"原则
// struct BadComponent { virtual void update() {} int hp; };

int main() {
    Position p{1.0f, 2.0f, 3.0f};
    Velocity v{0.0f, 0.0f, 9.8f};
    return (int)(p.z + v.vz);
}
