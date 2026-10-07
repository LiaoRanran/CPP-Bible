// RW-044 | CVE-2022-25315 | expat | defect_type: integer_overflow
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-25315
// project_url: https://libexpat.github.io/
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: storeAtts 中命名空间前缀/属性数组的容量计算整数溢出（ntmp 累加），
//   分配不足后写入越界。
// notes: 最小重构。UBSan 先报有符号溢出；ASan 报越界写。
#include <cstdio>
#include <cstdlib>
#include <cstring>

// BUG: `n` accumulates attribute counts in int; crafted XML with two huge
// DTD-injected attribute groups overflows the allocation arithmetic.
char** store_atts(int n_attrs_a, int n_attrs_b) {
    int n = n_attrs_a + n_attrs_b;              // integer overflow
    char** arr = static_cast<char**>(std::malloc(sizeof(char*) * (size_t)(n + 2)));
    if (!arr) return nullptr;
    for (int i = 0; i < n_attrs_a; ++i) arr[i] = (char*)"a";       // writes past the
    for (int i = 0; i < n_attrs_b; ++i) arr[n_attrs_a + i] = (char*)"b"; // tiny alloc
    return arr;
}

int main() {
    // crafted counts near INT_MAX summing to a negative value
    char** t = store_atts(0x7FFFFFF0, 64);
    std::printf("atts stored, table=%p\n", (void*)t);
    std::free(t);
    return 0;
}
