// RW-041 | CVE-2022-0561 | libtiff | defect_type: null_pointer_deref
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-0561
// project_url: https://libtiff.gitlab.io/libtiff/
// year: 2022 | severity: MEDIUM | source_type: cve
// mechanism: TIFFReadDirectory 对 StripOffsets/StripByteCounts 缺失或零值的
//   畸形 TIFF 访问空表指针（DoS）。
// notes: 最小重构。ASan/UBSan 命中空指针。
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>

struct TiffDir {
    std::vector<uint32_t> strip_offsets;
    std::vector<uint32_t> strip_byte_counts;
    bool missing_counts;     // crafted IFD: counts tag absent
};

// BUG: computes strips-per-image using strip_byte_counts even when the tag is
// missing (empty vector => operator[] UB / null payload in the real code).
int read_strips(const TiffDir& d) {
    uint32_t first_count = d.strip_byte_counts[0];   // empty vector access (UB/null read)
    return static_cast<int>(d.strip_offsets.size() / first_count);
}

int main() {
    TiffDir d;
    d.strip_offsets = {8, 32, 64};
    d.missing_counts = true;                          // crafted: no byte-counts tag
    // d.strip_byte_counts stays empty
    int n = read_strips(d);
    std::printf("strips = %d\n", n);
    return 0;
}
