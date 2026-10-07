// RW-071 | CVE-2021-38593 | Qt | defect_type: integer_overflow
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2021-38593
// project_url: https://www.qt.io/
// year: 2021 | severity: MEDIUM | source_type: cve
// mechanism: QImage 尺寸计算（宽×高×深度）整数溢出，分配不足（图像解码路径）。
// notes: 最小重构。UBSan + ASan 命中。
#include <cstdio>
#include <cstdlib>
#include <cstring>

// BUG: bytes = (w * h * depth + 7) / 8 computed in int.
unsigned char* qimage_alloc(int w, int h, int depth) {
    int bytes = (w * h * depth + 7) / 8;        // overflow for crafted dims
    if (bytes <= 0) bytes = 16;
    return static_cast<unsigned char*>(std::malloc((size_t)bytes));
}

int main() {
    int w = 65536, h = 32768, depth = 4;        // product overflows int32
    unsigned char* buf = qimage_alloc(w, h, depth);
    std::memset(buf, 0x42, 65536);              // scanline writes proceed "logically"
    std::printf("QImage %dx%d allocated=%p\n", w, h, (void*)buf);
    std::free(buf);
    return 0;
}
