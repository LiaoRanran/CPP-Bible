// RW-038 | CVE-2023-4863 | libwebp | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2023-4863
// project_url: https://chromium.googlesource.com/webm/libwebp
// year: 2023 | severity: CRITICAL | source_type: cve
// mechanism: WebP lossless (VP8L) 解码时 Huffman 表构建缓冲区边界检查缺失，
//   堆越界写（2023 年影响 Chrome/Firefox/所有内嵌 libwebp 的产品）。
// notes: 最小重构。ASan 应报 heap-buffer-overflow write。
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>

struct HuffmanTable {
    int num_symbols;
    uint16_t codes[64];   // fixed capacity
};

// BUG: symbol count from the bitstream is trusted up to 256, but the table
// array holds only 64 entries (VP8LBuildHuffmanTable bound-check gap shape).
int build_huffman_table(HuffmanTable* tbl, const uint8_t* stream, size_t stream_len) {
    uint8_t declared = stream[0];      // attacker declares up to 255 symbols
    tbl->num_symbols = declared;
    for (int i = 0; i < declared; ++i) {
        tbl->codes[i] = (uint16_t)(stream[1 + (i % (stream_len - 1))] << 8 | i); // overflow
    }
    return declared;
}

int main() {
    HuffmanTable tbl{};
    uint8_t crafted[16] = {200};       // declares 200 symbols; capacity is 64
    std::memset(crafted + 1, 0x7F, 15);
    int n = build_huffman_table(&tbl, crafted, sizeof(crafted));
    std::printf("built table with %d symbols\n", n);
    return 0;
}
