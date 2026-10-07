// RW-048 | CVE-2021-20309 | ImageMagick | defect_type: integer_overflow
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-20309
// project_url: https://imagemagick.org/
// year: 2021 | severity: HIGH | source_type: cve
// mechanism: WriteTHUMBNAILImage（缩略图写出）中图像尺寸乘积整数溢出，
//   分配小缓冲后按大尺寸写（堆越界）。
// notes: 最小重构。UBSan 有符号溢出 + ASan 越界写。
#include <cstdio>
#include <cstdlib>
#include <cstring>

// BUG: width * height * channels in 32-bit arithmetic overflows.
unsigned char* alloc_thumbnail_buffer(int width, int height, int channels) {
    int total = width * height * channels;                  // signed overflow (UB)
    size_t sz = (total > 0) ? (size_t)total : 64;
    return static_cast<unsigned char*>(std::malloc(sz));
}

int main() {
    // crafted MIFF header: enormous declared dimensions
    int w = 65536, h = 65536, ch = 4;    // product overflows int
    unsigned char* buf = alloc_thumbnail_buffer(w, h, ch);
    std::memset(buf, 0x77, 65536 * 4);   // writer proceeds at "real" size
    std::printf("thumbnail buffer=%p\n", (void*)buf);
    std::free(buf);
    return 0;
}
