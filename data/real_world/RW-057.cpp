// RW-057 | CVE-2021-30663 | WebKit | defect_type: integer_overflow
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-30663
// project_url: https://webkit.org/
// year: 2021 | severity: HIGH | source_type: cve
// mechanism: WebKit 图像/画布尺寸计算整数溢出导致缓冲不足（恶意网页内存破坏）。
// notes: 最小重构（C++ 复刻）。UBSan + ASan 命中。
#include <cstdint>
#include <cstdio>
#include <cstdlib>
#include <cstring>

// BUG: canvas area computed as uint32 (width*height*4) wraps for crafted sizes.
void* alloc_canvas_buffer(uint32_t width, uint32_t height) {
    uint32_t bytes = width * height * 4u;                  // wraps
    return std::malloc(bytes);                             // tiny allocation
}

int main() {
    uint32_t w = 0x00010001, h = 0x00010000;               // product wraps to small
    void* buf = alloc_canvas_buffer(w, h);
    // renderer then clears width*height*4 "logical" bytes:
    std::memset(buf, 0, 0x10000u);                         // >> allocation
    std::printf("canvas %ux%u buffer=%p\n", w, h, buf);
    std::free(buf);
    return 0;
}
