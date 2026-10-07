// RW-049 | CVE-2020-12284 | FFmpeg | defect_type: out_of_bounds
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2020-12284
// project_url: https://ffmpeg.org/
// year: 2020 | severity: HIGH | source_type: cve
// mechanism: cbs_jpeg（JPEG 码流解析）中熵段长度处理越界写。
// notes: 最小重构。ASan 应报 heap-buffer-overflow write。
#include <cstdint>
#include <cstdio>
#include <vector>

struct JpegCBS {
    std::vector<uint8_t> seg;   // current segment buffer
    size_t write_pos;
};

// BUG: segment payload length taken from the bitstream is copied without
// clamping to the allocated segment size.
void cbs_jpeg_read_segment(JpegCBS& cbs, const uint8_t* payload, size_t len) {
    for (size_t i = 0; i < len; ++i) {
        cbs.seg[cbs.write_pos + i] = payload[i];   // no bound check against seg.size()
    }
    cbs.write_pos += len;
}

int main() {
    JpegCBS cbs;
    cbs.seg.resize(64);
    cbs.write_pos = 8;
    std::vector<uint8_t> crafted(200, 0x55);       // declared DHT/DQT payload
    cbs_jpeg_read_segment(cbs, crafted.data(), crafted.size());
    std::printf("segment written to pos %zu\n", cbs.write_pos);
    return 0;
}
