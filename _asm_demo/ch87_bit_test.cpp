// ASM-87-bit : <bit> 工具真机汇编实证（GCC 15.3.0, C++26, -O2）
// 目标：证明 std::popcount / std::byteswap / std::bit_cast 的零成本本质，
//       并指出 popcount 在默认（无 -mpopcnt）下是软件 SWAR 循环、加 -mpopcnt 才变硬件单指令。
#include <bit>
#include <cstdint>
#include <iostream>

// popcount：默认无 -mpopcnt 时是软件 SWAR 算法；加 -mpopcnt 后变为硬件 popcnt 单指令
unsigned popcnt_u(unsigned x) {
    return std::popcount(x);
}

// byteswap：编译为 bswap 指令（x86 原生）
unsigned bswap_u(unsigned x) {
    return std::byteswap(x);
}

// bit_cast：同尺寸类型的纯重解释，运行时零指令（位不变，只是类型视图切换）
float to_float(uint32_t u) {
    return std::bit_cast<float>(u);
}

// has_single_bit：编译期常量折叠；运行期变量走位运算 (x & (x-1)) == 0
bool is_pow2(unsigned x) {
    return std::has_single_bit(x);
}

int main() {
    volatile unsigned sink = 0;
    sink = popcnt_u(0xABCD'1234u);   // 期望（默认）：SWAR 循环；(-mpopcnt)：popcnt eax,edi
    sink = bswap_u(0x1234'5678u);    // 期望：bswap eax
    sink = (unsigned)to_float(0x3F80'0000u); // 期望：mov，无重排
    sink += is_pow2(64u) ? 1u : 0u;  // 期望：(x & (x-1)) == 0
    return (int)sink;
}
