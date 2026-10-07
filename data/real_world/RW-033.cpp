// RW-033 | CVE-2022-37434 | zlib | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2022-37434
// project_url: https://zlib.net/
// year: 2022 | severity: HIGH | source_type: cve
// mechanism: inflateGetHeader 对 gzip 头 extra 字段长度复制越界（extra_max 与实际
//   复制长度不一致，堆越界写）。
// notes: 最小重构。ASan 应报 heap-buffer-overflow write。
#include <cstdint>
#include <cstdio>
#include <cstring>
#include <vector>

struct GzState {
    std::vector<uint8_t> head_extra;  // user-provided destination
    size_t extra_max;                 // declared capacity of head_extra
};

// BUG: copies `len` bytes from the stream into head_extra even when len > extra_max.
void gz_extra_copy(GzState& st, const uint8_t* stream, size_t len) {
    if (st.head_extra.size() < st.extra_max) return;
    std::memcpy(st.head_extra.data(), stream, len);   // no min(len, extra_max) clamp
}

int main() {
    GzState st;
    st.head_extra.resize(16);      // caller promised only 16 bytes of space
    st.extra_max = 16;
    std::vector<uint8_t> crafted(300, 0xEE);          // gzip header with 300-byte extra
    gz_extra_copy(st, crafted.data(), crafted.size()); // 300 > 16 -> overflow
    std::printf("extra field copied\n");
    return 0;
}
