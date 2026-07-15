// ASM-80-array : std::array 零开销实证（GCC 15.3.0, C++26, -O2）
// 目标：证明 std::array<T,N> 与裸 T[N] 逐字节同布局、同代码生成；
//       operator[] 无边界检查、at() 有运行时边界检查、data() 退化为指针、传值整段拷贝。
#include <array>
#include <iostream>

// (1) operator[]：与裸数组下标完全相同 —— base + idx*4，单条 mov，无边界检查
int access_by_index(const std::array<int, 8>& a, int i) {
    return a[i];
}

// (2) 裸数组下标作为对照
int access_raw(const int* a, int i) {
    return a[i];
}

// (3) at()：带运行时边界检查，越界走 __throw_out_of_range
int access_at(const std::array<int, 8>& a, int i) {
    return a.at(i);
}

// (4) data()：退化为指针，与 a 的首地址相同（lea/mov 直接返回）
const int* get_data(const std::array<int, 8>& a) {
    return a.data();
}

// (5) 传值：std::array 按值传递会逐元素整段拷贝（8*4=32B），非仅传指针
std::array<int, 8> by_value_copy(std::array<int, 8> a) {
    return a;
}

// (6) 布局常量：sizeof(std::array<int,8>) == sizeof(int[8]) == 32
constexpr std::size_t sz_arr  = sizeof(std::array<int, 8>);
constexpr std::size_t sz_raw  = sizeof(int[8]);
static_assert(sz_arr == sz_raw, "layout must match raw array");
static_assert(sz_arr == 32, "8 ints => 32 bytes, no hidden pointer/size");

int main() {
    std::array<int, 8> a{1, 2, 3, 4, 5, 6, 7, 8};
    volatile int sink = 0;
    sink = access_by_index(a, 3);   // 期望：mov eax, [rdi+rsi*4]
    sink = access_raw(a.data(), 3); // 期望：与上面逐字节相同
    sink = access_at(a, 2);         // 期望：含 cmp + call __throw_out_of_range 路径
    sink = *get_data(a);            // 期望：直接返回指针
    auto b = by_value_copy(a);      // 期望：32B 整段 mov 拷贝
    sink += (int)b[0];
    return (int)sink + (int)sz_arr;
}
