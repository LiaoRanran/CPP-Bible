// sample_G032
// defect_type: heap_overread
// severity: high
// planted: false
// expected_verdict: catch
// expected_detectors: asan
// source: CVE-2018-1000122 (https://nvd.nist.gov/vuln/detail/CVE-2018-1000122) [curl]
// (authoritative annotation in sample_G032.json)
#include <cstdio>
#include <cstdint>
// CVE-2018-1000122: RTSP interleaved RTP 帧头固定偏移读取 → 越界读
static int rtp_parse(const char* frame, size_t len) {
    const char* p = frame;
    const char* end = frame + len;
    while (p + 1 < end) {
        if (*p == '$') {   // interleaved 帧头: '$' channel seq_len(2)
            /* DEFECT */ // 原始缺陷: 未检查 p+3 < end
            unsigned short plen = (unsigned short)(((unsigned char)p[2] << 8) | (unsigned char)p[3]);
            return plen;
        }
        ++p;
    }
    return -1;
}

int main() {
    // crafted RTSP 帧: 仅 "$C" → 读 p[2]/p[3] 越过 2 字节堆分配
    char* frame = new char[2]{ '$', 'C' };
    std::printf("rtp len=%d\n", rtp_parse(frame, 2));
    delete[] frame;
    return 0;
}
