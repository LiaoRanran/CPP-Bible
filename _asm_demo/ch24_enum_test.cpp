// ASM-24-enum : enum class 真机汇编实证（GCC 15.3.0, C++26, -O2）
// 目标：证明 enum class 的"强类型"是纯编译期约束，运行期与裸 int/无作用域 enum 逐字节同码；
//       同时揭示无作用域 enum 的隐式 int 转换是零成本（正是它危险的根源）。
#include <cstdint>
#include <iostream>

enum class Color : uint8_t { red, green, blue };
enum Plain { A, B, C };

// enum class 上的 switch：与 int switch 同码（比较链 / 跳转表）
int use_enum(Color c) {
    switch (c) {
        case Color::red:   return 1;
        case Color::green: return 2;
        case Color::blue:  return 3;
    }
    return 0;
}

// 无作用域 enum：隐式转换为 int（零指令），但允许与任意 int 混用 → bug 温床
int use_plain(Plain p) {
    return (int)p + 1;   // 隐式 int 转换，免费
}

// enum class 取出底层值：必须显式 static_cast（仍是单条 mov）
uint8_t enum_underlying(Color c) {
    return static_cast<uint8_t>(c);
}

int main() {
    volatile int sink = 0;
    sink = use_enum(Color::green);     // 期望：cmp+je 链，同 int switch
    sink += use_plain(A);              // 期望：隐式转换 + 1，免费
    sink += (int)enum_underlying(Color::blue); // 期望：mov，零扩展
    return sink;
}
