// RW-051 | CVE-2023-49502 | FFmpeg | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2023-49502
// project_url: https://ffmpeg.org/
// year: 2023 | severity: HIGH | source_type: cve
// mechanism: vf_bwdif 反交错滤镜对奇数行尺寸/边界像素处理越界（堆缓冲区溢出）。
// notes: 最小重构。ASan 应报 heap-buffer-overflow。
#include <cstdio>
#include <cstdlib>
#include <cstring>

struct Plane {
    unsigned char* data;
    int w, h, stride;
};

// BUG: vertical filter taps read rows y-1 and y+1 without clamping at the
// bottom row (h-1) / with odd heights.
void bwdif_filter_row(const Plane& p, int y, unsigned char* out) {
    const unsigned char* r0 = p.data + (size_t)(y - 1) * p.stride;
    const unsigned char* r1 = p.data + (size_t)y * p.stride;
    const unsigned char* r2 = p.data + (size_t)(y + 1) * p.stride;   // y+1 == h at bottom
    for (int x = 0; x < p.w; ++x) {
        out[x] = (unsigned char)((r0[x] + 2u * r1[x] + r2[x]) / 4u); // OOB read at bottom
    }
}

int main() {
    Plane p{};
    p.w = 64; p.h = 33; p.stride = 64;         // odd height, common in interlaced input
    p.data = static_cast<unsigned char*>(std::malloc((size_t)p.stride * p.h));
    std::memset(p.data, 0x10, (size_t)p.stride * p.h);
    unsigned char out[64];
    bwdif_filter_row(p, p.h - 1, out);          // bottom row: r2 out of range
    std::printf("filtered bottom row, out[0]=%u\n", out[0]);
    std::free(p.data);
    return 0;
}
