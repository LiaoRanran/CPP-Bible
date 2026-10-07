// RW-035 | CVE-2018-13785 | libpng | defect_type: integer_overflow
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2018-13785
// project_url: http://www.libpng.org/pub/png/libpng.html
// year: 2018 | severity: MEDIUM | source_type: cve
// mechanism: pngrutil.c 中 PNG 高度/行尺寸计算整数溢出（height * rowbytes），
//   malloc 得到小缓冲后逐行写入越界。
// notes: 最小重构。UBSan 先报 signed overflow；ASan 报堆越界写。
#include <cstdint>
#include <cstdio>
#include <cstdlib>

// BUG: (unsigned) width * height * bpp overflows 32-bit size maths.
size_t row_buffer_size(uint32_t width, uint32_t height, int bpp) {
    uint32_t rowbytes = width * static_cast<uint32_t>(bpp);   // overflow possible
    uint32_t total = rowbytes * height;                       // overflow again
    return static_cast<size_t>(total);                        // small value returned
}

int main() {
    // crafted IHDR: huge height, small-looking rowbytes
    uint32_t width = 65536, height = 65536;   // 65536*3*65536 overflows uint32
    int bpp = 3;
    size_t sz = row_buffer_size(width, height, bpp);
    char* buf = static_cast<char*>(std::malloc(sz));
    std::printf("allocated %zu bytes for %ux%u image\n", sz, width, height);
    // real libpng then writes `height` rows into this buffer ("row-by-row overflow")
    std::free(buf);
    return 0;
}
