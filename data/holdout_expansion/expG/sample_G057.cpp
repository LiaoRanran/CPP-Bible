// sample_G057
// defect_type: heap_overflow
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2015-8126 (https://nvd.nist.gov/vuln/detail/CVE-2015-8126) [libpng]
// (authoritative annotation in sample_G057.json)
#include <cstdio>
#include <cstring>
#include <cstdint>
// CVE-2015-8126: png_set_PLTE 未校验调色板数量上限 → 堆溢出
static const int PNG_MAX_PALETTE_LENGTH = 256;

struct PngInfo {
    unsigned char  palette[PNG_MAX_PALETTE_LENGTH * 3];   // 256 项 × RGB
    int            num_palette;
};

static void png_set_PLTE(PngInfo* info, const unsigned char* chunk, int chunk_len) {
    int num = chunk_len / 3;
    /* DEFECT */ // 原始缺陷: 未校验 num <= PNG_MAX_PALETTE_LENGTH
    std::memcpy(info->palette, chunk, (size_t)num * 3);
    info->num_palette = num;
}

int main() {
    // crafted PNG: PLTE chunk 长度 1200 字节(400 项)
    unsigned char* chunk = new unsigned char[1200];
    std::memset(chunk, 0x7F, 1200);
    PngInfo info;
    std::memset(&info, 0, sizeof(info));
    png_set_PLTE(&info, chunk, 1200);   // 400 项 × 3 = 1200 > 768 → 越界写 432 字节
    std::printf("num_palette=%d\n", info.num_palette);
    delete[] chunk;
    return 0;
}
