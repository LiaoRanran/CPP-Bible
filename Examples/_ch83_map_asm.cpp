// Examples/_ch83_map_asm.cpp  —— 仅用于抽取真实汇编证据（附录 E/H）
// 编译: g++ -O2 -std=c++23 -m64 -masm=intel -S _ch83_map_asm.cpp -o _ch83_map_asm.asm
// 目的：为 ch83_map.md 附录 E(红黑树 vs flat_map) / H(map vs unordered_map)
//        提供真实汇编，替换原先"注释式假 asm"。展示：
//        - probe_map_find  : 红黑树下降（指针间接寻址 _M_left/_M_right）
//        - probe_flat_find : 连续内存二分（std::lower_bound）
//        - probe_umap_find : 哈希 + 桶数组一次访存
#include <map>
#include <vector>
#include <unordered_map>
#include <algorithm>
#include <utility>
#include <cstddef>

[[gnu::noinline]] int probe_map_find(const std::map<int,int>& m, int k) {
    auto it = m.find(k);
    return it == m.end() ? 0 : it->second;
}
[[gnu::noinline]] int probe_flat_find(const std::vector<std::pair<int,int>>& v, int k) {
    auto it = std::lower_bound(v.begin(), v.end(), std::pair<int,int>{k, 0});
    if (it != v.end() && it->first == k) return it->second;
    return 0;
}
[[gnu::noinline]] int probe_umap_find(const std::unordered_map<int,int>& m, int k) {
    auto it = m.find(k);
    return it == m.end() ? 0 : it->second;
}
int main(){ std::map<int,int> a; (void)probe_map_find(a,1); return 0; }
