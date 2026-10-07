// RW-094 | CVE-2021-45960 | expat | defect_type: integer_overflow
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-45960
// project_url: https://libexpat.github.io/
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: storeAtts 中前缀/属性哈希槽计数以 int 存储，构造大量唯一前缀的
//   XML 使其整数溢出后重建哈希表时越界。
// notes: 最小重构。UBSan + ASan 命中。
#include <cstdio>
#include <cstdlib>
#include <cstring>

// BUG: prefix_count * bucket_factor overflows int when thousands of crafted
// prefixes arrive (real code: `nsAtts` array growth)
char** rebuild_prefix_table(int prefix_count, int factor) {
    int slots = prefix_count * factor;             // signed overflow for large counts
    size_t sz = (slots > 0) ? (size_t)slots : 8;
    char** table = static_cast<char**>(std::malloc(sz * sizeof(char*)));
    for (int i = 0; i < prefix_count && i < 64; ++i) {
        table[i] = (char*)"ns";                    // writes up to min(count,64) slots
    }
    std::printf("slots=%d (as int), allocated=%zu entries\n", slots, sz);
    return table;
}

int main() {
    // crafted XML: ~2^18 unique namespace prefixes with factor 2^13
    char** t = rebuild_prefix_table(0x40000, 0x2000); // product overflows int
    std::free(t);
    return 0;
}
