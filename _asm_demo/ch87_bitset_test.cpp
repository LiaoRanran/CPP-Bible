// ASM-87-bitset : std::bitset 真机汇编实证（GCC 15.3.0, C++26, -O2）
// 目标：证明 bitset<N> 是底层字（word）的薄封装；count()/test()/flip() 编译为
//       字级位指令（popcount / bt / 位运算），无循环、无堆分配、零抽象开销。
#include <bitset>
#include <iostream>

// count()：对 64 位字做 popcount（下文 ch87_bit_test 进一步对比 -mpopcnt 硬件指令）
std::size_t bitset_count(const std::bitset<64>& b) {
    return b.count();
}

// test(i)：读取第 i 位
bool bitset_test(const std::bitset<64>& b, std::size_t i) {
    return b.test(i);
}

// flip()：按位取反全部位（返回副本）
std::bitset<64> bitset_flip(std::bitset<64> b) {
    return b.flip();
}

// set(i)：置位第 i 位
std::bitset<64> bitset_set(std::bitset<64> b, std::size_t i) {
    b.set(i);
    return b;
}

int main() {
    std::bitset<64> b(0x1234'5678'9ABC'DEF0ULL);
    volatile std::size_t sink = 0;
    sink = bitset_count(b);          // 期望：popcount 字级指令
    sink = bitset_test(b, 5);        // 期望：bt / 移位+test
    auto f = bitset_flip(b);         // 期望：not 指令（整字取反）
    auto s = bitset_set(f, 7);       // 期望：bts / or 立即数
    sink += f.count() + s.count();
    return (int)sink;
}
