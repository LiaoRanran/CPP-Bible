// sample_G059
// defect_type: heap_overflow
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2023-4863 (https://nvd.nist.gov/vuln/detail/CVE-2023-4863) [libwebp]
// (authoritative annotation in sample_G059.json)
#include <cstdio>
#include <cstring>
// CVE-2023-4863: BuildHuffmanTable 未校验码长分布 → 表项越界写
static const int ROOT_BITS = 4;                 // 根表 16 项
static const int MAX_CODE_BITS = 4;

static int BuildHuffmanTable(const int* code_lengths, int n_symbols, unsigned int* table, int table_cap) {
    // 统计各码长数量
    int count[MAX_CODE_BITS + 1] = { 0 };
    for (int s = 0; s < n_symbols; ++s)
        if (code_lengths[s]) ++count[code_lengths[s]];
    // 原始缺陷: 缺少合法性校验 sum(count[i] << (MAX-i)) <= (1 << ROOT_BITS)
    // (修复版: if (total > (1 << ROOT_BITS)) return 0;)
    int key = 0;
    int written = 0;
    for (int len = 1; len <= MAX_CODE_BITS; ++len) {
        for (int s = 0; s < n_symbols; ++s) {
            if (code_lengths[s] != len) continue;
            int step = 1 << (MAX_CODE_BITS - len);       // 该码占用的表项数
            /* DEFECT */ for (int i = 0; i < step; ++i) {
                table[key + i] = (unsigned int)s;        // 无任何边界检查: 越过 table_cap 继续写
                ++written;
            }
            key += step;
        }
    }
    return written;
}

int main() {
    unsigned int* table = new unsigned int[1 << ROOT_BITS];   // 分配 16 项
    std::memset(table, 0xEE, (1 << ROOT_BITS) * sizeof(unsigned int));
    // crafted 码长: 5 个长度为 2 的码 → 每个 4 项 → 需要 20 项 > 16
    int code_lengths[5] = { 2, 2, 2, 2, 2 };
    int n = BuildHuffmanTable(code_lengths, 5, table, 1 << ROOT_BITS);
    std::printf("huffman entries written=%d (表容量 16)\n", n);
    delete[] table;
    return 0;
}
