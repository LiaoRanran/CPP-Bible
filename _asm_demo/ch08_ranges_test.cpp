// Phase 4.5 实证：std::ranges 零成本抽象（GCC 15.3.0 真机）
//
// 编译：
//   g++ -std=c++26 -O2 -c ch08_ranges_test.cpp -o ranges.o
//   objdump -d -M intel -C ranges.o | sed -n '/<sort_std>/,/ret/p'
//   objdump -d -M intel -C ranges.o | sed -n '/<sort_ranges>/,/ret/p'
//   objdump -d -M intel -C ranges.o | sed -n '/<count_even>/,/ret/p'
//
// 验证两点：
//   (1) std::ranges::sort 与 std::sort 生成等价代码（无额外开销）
//   (2) std::views::filter 的 lambda 被内联进循环，无运行时分发开销
#include <algorithm>
#include <ranges>
#include <vector>
#include <cstdio>

[[gnu::noinline]]
void sort_std(std::vector<int>& v) { std::sort(v.begin(), v.end()); }

[[gnu::noinline]]
void sort_ranges(std::vector<int>& v) { std::ranges::sort(v); }

[[gnu::noinline]]
long count_even(const std::vector<int>& v) {
    auto even = v | std::views::filter([](int x) { return (x & 1) == 0; });
    long c = 0;
    for (int x : even) c += x;
    return c;
}

int main() {
    std::vector<int> v(64);
    for (int i = 0; i < 64; ++i) v[i] = 64 - i;
    sort_std(v);
    sort_ranges(v);
    std::printf("%ld\n", count_even(v));
}
