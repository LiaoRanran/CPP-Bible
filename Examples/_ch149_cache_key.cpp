// 见 Examples/_ch149_cache_key.cpp
// ④ 构建缓存键：用 FNV-1a 把 (编译器,平台,标准) 压成稳定哈希
#include <cstdio>
#include <string>
unsigned long long fnv1a(const std::string& s) {
    unsigned long long h = 1469598103934665603ULL;
    for (unsigned char c : s) { h ^= c; h *= 1099511628211ULL; }
    return h;
}
int main() {
    std::printf("key(gcc,linux,c++17)=%llx\n", fnv1a("gcc-13;linux;c++17"));
    return 0;
}
