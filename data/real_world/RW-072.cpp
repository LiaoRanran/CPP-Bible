// RW-072 | CVE-2023-32762 | Qt | defect_type: logic_error
// source_url: https://nvd.nist.gov/vuln/detail/CVE-2023-32762
// project_url: https://www.qt.io/
// year: 2023 | severity: MEDIUM | source_type: cve
// mechanism: QHttp2 的 DATA/HEADERS 帧流控窗口计数错误，攻击者可让连接进入
//   无法推进的状态（CPU 消耗型 DoS）。
// notes: 最小重构（流控状态机缺陷；不实际联网）。
#include <cstdio>
#include <cstdint>

struct Http2Conn {
    int32_t window_local;      // we advertise this to the peer
    int32_t window_remote;     // peer-configured send window
    uint32_t pad_len;          // crafted padding in DATA frames
};

// BUG: padding bytes are subtracted from window_remote but never credited back
// to window_local; a crafted stream of padded DATA frames wedges the connection
// (window_local drifts negative -> no progress loop).
void on_data_frame(Http2Conn& c, uint32_t payload_len, uint32_t pad_len) {
    c.window_local -= (int32_t)payload_len;
    c.window_remote -= (int32_t)(payload_len + pad_len);   // padding not accounted
}

int main() {
    Http2Conn c{65535, 65535, 0};
    for (int i = 0; i < 200; ++i) {
        on_data_frame(c, 256, 200);            // padded frames shrink windows unevenly
    }
    std::printf("window_local=%d window_remote=%d -> stalled=%s\n",
                c.window_local, c.window_remote,
                (c.window_local > 0 && c.window_remote <= 0) ? "YES (bug)" : "no");
    return 0;
}
