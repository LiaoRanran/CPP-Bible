// RW-043 | CVE-2016-5321 | libtiff | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2016-5321
// project_url: https://libtiff.gitlab.io/libtiff/
// year: 2016 | severity: MEDIUM | source_type: cve
// mechanism: DumpModeDecode（未压缩 raw 模式）中扫描行尺寸计算与实际读取不一致，
//   越界读。
// notes: 最小重构。ASan 应报 heap-buffer-overflow read。
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>

struct RawStrip {
    std::vector<uint8_t> data;   // strip payload as stored in file
    uint32_t row_size;           // scanline size from IFD
    uint32_t rows;
};

// BUG: reads row_size * rows bytes from a strip that may be shorter (raw mode
// trusts the IFD over the actual file size).
size_t dump_mode_decode(const RawStrip& s, uint8_t* out) {
    size_t total = (size_t)s.row_size * s.rows;
    std::memcpy(out, s.data.data(), total);   // OOB read when total > data.size()
    return total;
}

int main() {
    RawStrip s;
    s.data.assign(64, 0xCD);       // file provides 64 bytes
    s.row_size = 40;
    s.rows = 8;                    // IFD claims 320 bytes
    std::vector<uint8_t> out(320);
    size_t n = dump_mode_decode(s, out.data());
    std::printf("decoded %zu bytes from a 64-byte strip\n", n);
    return 0;
}
